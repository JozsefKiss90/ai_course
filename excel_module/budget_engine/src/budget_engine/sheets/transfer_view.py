"""Transfer View per Beneficiary, row for row like the Submission Budget's breakdown.

Row order comes from the profile's ``transfer_view.rows``. A cost line shows number of items,
average cost per item and total, summed over every Estimation Method contributing to it; lines no
switched-on method fills stay blank.
"""

from __future__ import annotations

from collections import defaultdict

from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Contribution
from budget_engine.sheets.styles import BOLD, MONEY, QUANTITY, TITLE, name_formula, put_derived, put_header

HEADER_ROW = 3
GAP_AFTER_WP = 2


def sheet_name(be: str) -> str:
    return f"Transfer View {be}"


def _sum(refs: list[str]) -> str:
    return "=" + "+".join(refs)


def build_transfer_views(ctx: BuildContext) -> None:
    by_line: dict[tuple[str, str, str], list[Contribution]] = defaultdict(list)
    for c in ctx.contributions:
        by_line[(c.be, c.wp, c.line)].append(c)
    for be in ctx.shape.be_codes:
        _build_one(ctx, be, by_line)


def _build_one(ctx: BuildContext, be: str, by_line: dict[tuple[str, str, str], list[Contribution]]) -> None:
    profile = ctx.profile
    ws = ctx.wb.create_sheet(sheet_name(be))
    ws["A1"] = f"{be} - TRANSFER VIEW (copy into the {be} budget sheet of the Official Budget Table)"
    ws["A1"].font = TITLE
    ws["A2"] = name_formula(ctx.layout.inputs[("be_name", be)].ref)
    for col, header in zip("ABCD", profile.transfer_view_headers):
        put_header(ws, f"{col}{HEADER_ROW}", header)

    row = HEADER_ROW + 2
    for n, wp in enumerate(ctx.shape.wp_codes, start=1):
        title = profile.wp_title.format(n=n)
        wp_name = ctx.layout.inputs[("wp_name", wp)].ref
        ws[f"A{row}"] = f'="{title}"&{wp_name}'
        ws[f"A{row}"].font = BOLD
        row += 2
        row = _wp_block(ctx, ws, be, wp, row, by_line) + GAP_AFTER_WP

    ws.column_dimensions["A"].width = 70
    for col in "BCD":
        ws.column_dimensions[col].width = 16
    ws.freeze_panes = f"A{HEADER_ROW + 1}"


def _wp_block(
    ctx: BuildContext, ws: Worksheet, be: str, wp: str, row: int,
    by_line: dict[tuple[str, str, str], list[Contribution]],
) -> int:
    """Write one work package's rows; return the next free row."""
    line_rows: dict[str, tuple[int, str]] = {}  # line id -> (row, group)
    total_rows: dict[str, int] = {}
    outputs = ctx.layout.outputs
    sheet = ws.title

    def total_of(groups: tuple[str, ...]) -> str:
        cells = [f"D{r}" for r, g in line_rows.values() if g in groups]
        return f"SUM({','.join(cells)})"

    for spec in ctx.profile.transfer_view_rows:
        if spec.kind == "blank":
            row += 1
            continue
        if spec.label:
            ws[f"A{row}"] = spec.label
        if spec.kind == "heading":
            ws[f"A{row}"].font = BOLD
        elif spec.kind == "line":
            line_rows[spec.id] = (row, spec.group)
            sources = by_line.get((be, wp, spec.id), [])
            if sources:
                put_derived(ws, f"B{row}", _sum([s.items.ref for s in sources]), QUANTITY)
                put_derived(ws, f"D{row}", _sum([s.total.ref for s in sources]), MONEY)
                put_derived(ws, f"C{row}", f"=IF(B{row}>0,D{row}/B{row},0)", MONEY)
                for col, what in (("B", "items"), ("C", "avg"), ("D", "total")):
                    outputs[("tv", be, wp, spec.id, what)] = Cell(sheet, f"{col}{row}")
        else:
            if spec.kind == "total":
                formula = "=" + total_of(spec.sum_groups)
            elif spec.kind == "indirect":
                rule = ctx.profile.indirect_rule
                rate = ctx.layout.constants[rule.rate_constant].ref
                formula = f"={total_of(rule.base_groups)}*{rate}"
            elif spec.kind == "grand_total":
                formula = "=" + "+".join(f"D{total_rows[i]}" for i in spec.add)
            else:
                raise ValueError(f"unknown Transfer View row kind {spec.kind!r}")
            ws[f"A{row}"].font = BOLD
            put_derived(ws, f"D{row}", formula, MONEY, bold=True)
            total_rows[spec.id] = row
            outputs[("tv", be, wp, spec.id, "total")] = Cell(sheet, f"D{row}")
        row += 1
    return row

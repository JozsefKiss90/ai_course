"""Transfer View per Beneficiary, per AE and per spare block, row for row like the Submission Budget's breakdown.

Row order comes from the profile's ``transfer_view.rows``. A cost line shows number of items,
average cost per item and total, summed over every Estimation Method contributing to it; lines no
switched-on method fills stay blank. Names come from the Reference Lists by code, so they follow
rows a human adds there; a spare block shows the name of whichever late partner claims it.
"""

from __future__ import annotations

from collections import defaultdict

from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Contribution
from budget_engine.shape import SPARE_PREFIX, is_affiliated, is_spare
from budget_engine.sheets.reference_lists import be_field, lookup
from budget_engine.sheets.styles import BOLD, MONEY, QUANTITY, TITLE, put_derived, put_header

HEADER_ROW = 3
GAP_AFTER_WP = 2


SHEET_PREFIX = "Transfer View "


def sheet_name(slot: str) -> str:
    if is_spare(slot):
        return f"{SHEET_PREFIX}spare {slot.removeprefix(SPARE_PREFIX)}"
    return f"{SHEET_PREFIX}{slot}"


def _title(slot: str, code: str) -> str:
    if is_spare(slot):
        unused = f"SPARE BLOCK {slot.removeprefix(SPARE_PREFIX)} - unused until a BE/AE nr is entered in the Rate Table"
        return f'=IF({code}="","{unused}",{code}&" - TRANSFER VIEW (copy into its budget sheet of the Official Budget Table)")'
    if is_affiliated(slot):
        be = slot.split("-")[0]
        return f"{slot} - TRANSFER VIEW (copy into the affiliated entity columns of the {be} budget sheet of the Official Budget Table)"
    return f"{slot} - TRANSFER VIEW (copy into the {slot} budget sheet of the Official Budget Table)"


def _sum(refs: list[str]) -> str:
    return "=" + "+".join(refs)


def build_transfer_views(ctx: BuildContext) -> None:
    by_line: dict[tuple[str, str, str], list[Contribution]] = defaultdict(list)
    for c in ctx.contributions:
        by_line[(c.be, c.wp, c.line)].append(c)
    for slot in ctx.shape.slots:
        _build_one(ctx, slot, by_line)


def _build_one(ctx: BuildContext, slot: str, by_line: dict[tuple[str, str, str], list[Contribution]]) -> None:
    profile = ctx.profile
    ws = ctx.wb.create_sheet(sheet_name(slot))
    code = ctx.layout.slot_codes[slot]
    ws["A1"] = _title(slot, code)
    ws["A1"].font = TITLE
    ws["A2"] = "=" + be_field(ctx, "be_name", code)
    ctx.layout.outputs[("tv", slot, "name")] = Cell(ws.title, "A2")
    for col, header in zip("ABCD", profile.transfer_view_headers):
        put_header(ws, f"{col}{HEADER_ROW}", header)

    row = HEADER_ROW + 2
    for n, wp in enumerate(ctx.shape.wp_codes, start=1):
        title = profile.wp_title.format(n=n)
        ws[f"A{row}"] = f'="{title}"&' + lookup(profile, "wp_list", "B", f'"{wp}"')
        ws[f"A{row}"].font = BOLD
        row += 2
        row = _wp_block(ctx, ws, slot, wp, row, by_line) + GAP_AFTER_WP

    ws.column_dimensions["A"].width = 70
    for col in "BCD":
        ws.column_dimensions[col].width = 16
    ws.freeze_panes = f"A{HEADER_ROW + 1}"


def _wp_block(
    ctx: BuildContext, ws: Worksheet, slot: str, wp: str, row: int,
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
            sources = by_line.get((slot, wp, spec.id), [])
            if sources:
                put_derived(ws, f"B{row}", _sum([s.items.ref for s in sources]), QUANTITY)
                put_derived(ws, f"D{row}", _sum([s.total.ref for s in sources]), MONEY)
                put_derived(ws, f"C{row}", f"=IF(B{row}>0,D{row}/B{row},0)", MONEY)
                for col, what in (("B", "items"), ("C", "avg"), ("D", "total")):
                    outputs[("tv", slot, wp, spec.id, what)] = Cell(sheet, f"{col}{row}")
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
            outputs[("tv", slot, wp, spec.id, "total")] = Cell(sheet, f"D{row}")
        row += 1
    return row

"""Check Summaries: the Submission Budget's own summaries, mirrored by formula from the Transfer Views.

For Horizon Europe these are the Official Budget Table's lump sum breakdown, person-months overview
and summary per WP, one sheet each. The two grids (BE/AE block × WP) carry the % shares of budget
and effort per block (last column) and per WP (last row). The summary per WP adds the Transfer Views
up per WP and over all WPs, split into Beneficiaries and AEs as the Official Budget Table does; a
spare block counts as an AE when the code typed in for it is an AE code.

Every figure is a formula over the Transfer Views (no PivotTables, ADR-0002). Sheets, titles,
headers, the Transfer View row the lump sum is taken of and the cost categories counted as effort
come from the profile's ``check_summaries``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Key
from budget_engine.profiles import LayoutRow, Profile
from budget_engine.shape import ShapeParameters, is_affiliated, is_spare
from budget_engine.sheets import transfer_view
from budget_engine.sheets.breakdown import TOTAL_KINDS, write_breakdown
from budget_engine.sheets.reference_lists import be_field, be_number, lookup
from budget_engine.sheets.styles import BOLD, MONEY, QUANTITY, TITLE, put_derived, put_header

GRID_HEADER_ROW = 2
GRID_FIRST_ROW = 3
PERCENT = "0.00%"
RATE = "0%"
SUMMARIES = ("lump_sum", "effort", "per_wp")

# Summary per WP: column groups for Beneficiaries, AEs and both, each items | cost per item | total.
PARTS = ("be", "ae", "all")
SPARE_COUNTED_AS = {"be": "BE", "ae": "AE"}  # what the spare block helper shows
SPARE_COLUMN, SPARE_PART_COLUMN = "L", "M"


def sheets(profile: Profile) -> list[str]:
    """The Check Summary sheets, in build order."""
    return [str(profile.check_summaries[s]["sheet"]) for s in SUMMARIES]


def grid_columns(shape: ShapeParameters) -> tuple[list[str], str, str, str]:
    """A grid's WP columns, then its total, share and (lump sum only) funding rate columns."""
    n = shape.work_packages
    total, share, rate = (get_column_letter(2 + n + k) for k in range(3))
    return [get_column_letter(2 + j) for j in range(n)], total, share, rate


def part_columns(part: str) -> tuple[str, str, str]:
    """Summary per WP: the items, cost per item and total columns of one column group."""
    first = 2 + 3 * PARTS.index(part)
    return get_column_letter(first), get_column_letter(first + 1), get_column_letter(first + 2)


def build_check_summaries(ctx: BuildContext) -> None:
    """Write the Check Summary sheets after the Transfer Views, whose output cells they add up."""
    cs = ctx.profile.check_summaries
    _build_lump_sum(ctx, cs["lump_sum"])
    _build_effort(ctx, cs["effort"])
    _build_per_wp(ctx, cs["per_wp"])


def _lump_sum(total: str, rate: str) -> str:
    return f"={total}*{rate}"


def _share(part: str, whole: str) -> str:
    return f"=IF({whole}>0,{part}/{whole},0)"


def _spare_part(code: str) -> str:
    """Formula text: "AE" when the code typed in for a spare block is an AE code, else "BE".
    FIND is case-sensitive, like ``shape.is_affiliated``."""
    return f'IF(ISNUMBER(FIND("-AE",{code})),"{SPARE_COUNTED_AS["ae"]}","{SPARE_COUNTED_AS["be"]}")'


def slot_label(ctx: BuildContext, slot: str) -> str:
    """'BE1: <name>', as the Official Budget Table labels a Beneficiary's row."""
    code = ctx.layout.slot_codes[slot]
    name = be_field(ctx, "be_name", code)
    if is_spare(slot):
        unused = transfer_view.sheet_name(slot).removeprefix(transfer_view.SHEET_PREFIX)
        return f'=IF({code}="","{unused} (unused)",{code}&": "&{name})'
    return f'="{slot}: "&{name}'


def _build_lump_sum(ctx: BuildContext, spec: dict[str, Any]) -> None:
    outputs = ctx.layout.outputs
    *_, rate_col = grid_columns(ctx.shape)

    def value(slot: str, wp: str, row: int) -> str:
        return _lump_sum(outputs[("tv", slot, wp, spec["of_row"], "total")].ref, f"${rate_col}{row}")

    ws = _grid(ctx, "ls", spec, value, MONEY)
    put_header(ws, f"{rate_col}{GRID_HEADER_ROW}", spec["rate_header"])
    for i, slot in enumerate(ctx.shape.slots):
        coord = f"{rate_col}{GRID_FIRST_ROW + i}"
        put_derived(ws, coord, "=" + be_number(ctx, "be_funding_rate", ctx.layout.slot_codes[slot]), RATE)
        outputs[("ls", slot, "rate")] = Cell(ws.title, coord)
    ws.column_dimensions[rate_col].width = 12


def _build_effort(ctx: BuildContext, spec: dict[str, Any]) -> None:
    outputs = ctx.layout.outputs
    lines = effort_lines(ctx.profile)

    def value(slot: str, wp: str, row: int) -> str:
        refs = [outputs[k].ref for line in lines if (k := ("tv", slot, wp, line, "items")) in outputs]
        return "=" + ("+".join(refs) or "0")

    _grid(ctx, "pm", spec, value, QUANTITY)


def effort_lines(profile: Profile) -> list[str]:
    """The cost lines whose number of items is effort (person-months for Horizon Europe)."""
    groups = profile.check_summaries["effort"]["groups"]
    return [r.id for r in profile.transfer_view_rows if r.kind == "line" and r.group in groups]


def _grid(
    ctx: BuildContext, kind: str, spec: dict[str, Any], value: Callable[[str, str, int], str], number_format: str
) -> Worksheet:
    """A BE/AE block × WP grid with row and column totals and % shares, keyed (kind, block|"total"|"share", WP|"total"|"share")."""
    shape = ctx.shape
    grid = ctx.profile.check_summaries["grid"]
    outputs = ctx.layout.outputs
    ws: Worksheet = ctx.wb.create_sheet(spec["sheet"])
    ws["A1"] = spec["title"]
    ws["A1"].font = TITLE
    wp_cols, total_col, share_col, _ = grid_columns(shape)
    put_header(ws, f"A{GRID_HEADER_ROW}", grid["corner"])
    for col, wp in zip(wp_cols, shape.wp_codes):
        put_header(ws, f"{col}{GRID_HEADER_ROW}", f'="{wp} "&' + lookup(ctx.profile, "wp_list", "B", f'"{wp}"'))
    put_header(ws, f"{total_col}{GRID_HEADER_ROW}", grid["total"])
    put_header(ws, f"{share_col}{GRID_HEADER_ROW}", grid["share"])

    first = GRID_FIRST_ROW
    last = first + len(shape.slots) - 1
    total_row, share_row = last + 1, last + 2
    grand = f"${total_col}${total_row}"

    def put(coord: str, formula: str, fmt: str, key: Key | None = None, bold: bool = False) -> None:
        put_derived(ws, coord, formula, fmt, bold=bold)
        if key is not None:
            outputs[(kind, *key)] = Cell(ws.title, coord)

    for i, slot in enumerate(shape.slots):
        r = first + i
        ws[f"A{r}"] = slot_label(ctx, slot)
        for col, wp in zip(wp_cols, shape.wp_codes):
            put(f"{col}{r}", value(slot, wp, r), number_format, (slot, wp))
        put(f"{total_col}{r}", f"=SUM({wp_cols[0]}{r}:{wp_cols[-1]}{r})", number_format, (slot, "total"))
        put(f"{share_col}{r}", _share(f"{total_col}{r}", grand), PERCENT, (slot, "share"))

    ws[f"A{total_row}"] = grid["total_row"]
    ws[f"A{share_row}"] = grid["share_row"]
    for col, wp in zip([*wp_cols, total_col], [*shape.wp_codes, "total"]):
        put(f"{col}{total_row}", f"=SUM({col}{first}:{col}{last})", number_format, ("total", wp), bold=True)
        put(f"{col}{share_row}", _share(f"{col}{total_row}", grand), PERCENT, ("share", wp) if wp != "total" else None)
    put(f"{share_col}{total_row}", _share(f"{total_col}{total_row}", grand), PERCENT)
    for r in (total_row, share_row):
        ws[f"A{r}"].font = BOLD

    ws.column_dimensions["A"].width = 50
    for col in [*wp_cols, total_col, share_col]:
        ws.column_dimensions[col].width = 16
    ws.freeze_panes = f"B{first}"
    return ws


def _build_per_wp(ctx: BuildContext, spec: dict[str, Any]) -> None:
    profile, shape = ctx.profile, ctx.shape
    outputs = ctx.layout.outputs
    ws = ctx.wb.create_sheet(spec["sheet"])
    ws["A1"] = spec["title"]
    ws["A1"].font = TITLE
    header_row = transfer_view.HEADER_ROW
    put_header(ws, f"A{header_row}", profile.transfer_view_headers[0])
    for part in PARTS:
        cols = part_columns(part)
        put_header(ws, f"{cols[0]}{header_row - 1}", spec["parts"][part]["header"])
        for col, header in zip(cols, spec["parts"][part]["columns"]):
            put_header(ws, f"{col}{header_row}", header)

    spare_part: dict[str, str] = {}  # spare block -> cell showing whether it counts as BE or AE
    if shape.spare_slots:
        for col, header in zip((SPARE_COLUMN, SPARE_PART_COLUMN), spec["spare_headers"]):
            put_header(ws, f"{col}{header_row}", header)
        for i, slot in enumerate(shape.spare_slots, start=header_row + 1):
            put_derived(ws, f"{SPARE_COLUMN}{i}", transfer_view.sheet_name(slot).removeprefix(transfer_view.SHEET_PREFIX))
            put_derived(ws, f"{SPARE_PART_COLUMN}{i}", "=" + _spare_part(ctx.layout.slot_codes[slot]))
            spare_part[slot] = f"${SPARE_PART_COLUMN}${i}"

    def from_transfer_views(part: str, wp: str, line: str, what: str) -> list[str]:
        terms = []
        for slot in shape.slots:
            key = ("tv", slot, wp, line, what)
            if key not in outputs:
                continue
            if is_spare(slot):
                terms.append(f'IF({spare_part[slot]}="{SPARE_COUNTED_AS[part]}",{outputs[key].ref},0)')
            elif (part == "ae") == is_affiliated(slot):
                terms.append(outputs[key].ref)
        return terms

    def fill_line(block: str, line: str, r: int, terms: Callable[[str, str], list[str]]) -> None:
        """One cost line: Beneficiaries and AEs from ``terms(part, what)``, both added up, and averages."""
        for part in PARTS:
            items, avg, total = part_columns(part)
            for col, what, fmt in ((items, "items", QUANTITY), (total, "total", MONEY)):
                if part == "all":
                    k = 0 if what == "items" else 2
                    formula = f"={part_columns('be')[k]}{r}+{part_columns('ae')[k]}{r}"
                else:
                    formula = "=" + ("+".join(terms(part, what)) or "0")
                put_derived(ws, f"{col}{r}", formula, fmt)
            put_derived(ws, f"{avg}{r}", f"=IF({items}{r}>0,{total}{r}/{items}{r},0)", MONEY)
            for col, what in ((items, "items"), (avg, "avg"), (total, "total")):
                outputs[("wps", block, line, part, what)] = Cell(ws.title, f"{col}{r}")

    def register_totals(block: str, rows: dict[str, int]) -> None:
        for row_spec in profile.transfer_view_rows:
            if row_spec.kind in TOTAL_KINDS:
                for part in PARTS:
                    outputs[("wps", block, row_spec.id, part, "total")] = Cell(ws.title, f"{part_columns(part)[2]}{rows[row_spec.id]}")

    total_columns = [part_columns(p)[2] for p in PARTS]
    rows_by_wp: dict[str, dict[str, int]] = {}
    row = header_row + 2
    for n, wp in enumerate(shape.wp_codes, start=1):
        ws[f"A{row}"] = f'="{profile.wp_title.format(n=n)}"&' + lookup(profile, "wp_list", "B", f'"{wp}"')
        ws[f"A{row}"].font = BOLD
        row += 2

        def write_wp_line(line: LayoutRow, r: int, wp: str = wp) -> bool:
            if not any(("tv", slot, wp, line.id, "items") in outputs for slot in shape.slots):
                return False
            fill_line(wp, line.id, r, lambda part, what: from_transfer_views(part, wp, line.id, what))
            return True

        row, rows_by_wp[wp] = write_breakdown(ctx, ws, row, total_columns, write_wp_line)
        register_totals(wp, rows_by_wp[wp])
        row += transfer_view.GAP_AFTER_WP

    ws[f"A{row}"] = spec["all_title"]
    ws[f"A{row}"].font = BOLD
    row += 2

    def write_all_line(line: LayoutRow, r: int) -> bool:
        wp_rows = [rows[line.id] for rows in rows_by_wp.values() if line.id in rows]
        if not wp_rows:
            return False

        def terms(part: str, what: str) -> list[str]:
            col = part_columns(part)[0 if what == "items" else 2]
            return [f"{col}{wr}" for wr in wp_rows]

        fill_line("all", line.id, r, terms)
        return True

    _, all_rows = write_breakdown(ctx, ws, row, total_columns, write_all_line)
    register_totals("all", all_rows)

    ws.column_dimensions["A"].width = 70
    for part in PARTS:
        for col in part_columns(part):
            ws.column_dimensions[col].width = 16
    for col in (SPARE_COLUMN, SPARE_PART_COLUMN):
        ws.column_dimensions[col].width = 14
    ws.freeze_panes = f"B{header_row + 1}"

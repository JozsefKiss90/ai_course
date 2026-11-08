"""Equipment depreciation: only the share of each item's depreciation that falls in the project is costed.

An item is a row of the `Equipment` Excel Table: who buys it (BE/AE nr), for which WP, which C.2
cost line (equipment, infrastructure, other assets), what it is, its purchase cost, its
depreciation period in months and the share of its use that goes to the action. Those are Human
Inputs. The rest are calculated columns:
- months in the project = MIN(project duration, depreciation period); the duration is the labelled
  cell on the `Profile Constants` sheet, so no constant sits in a formula
- share of useful life in the project = months in the project ÷ depreciation period
- eligible cost = purchase cost × usage share × share of useful life in the project

This matches the Official Budget Table's "Depreciation costs" sheet (K = purchase cost × % used for
the project × % of useful life in the project). It assumes purchase in month 1: there is no
purchase-month input. Because the prices are calculated columns, a row a human adds is costed too.

The `Equipment summary` sums the Table with SUMIFS/COUNTIFS per BE/AE block × WP × cost line.
Output per BE × WP × cost line: items = equipment items (rows with a purchase cost), total = their
eligible cost.
"""

from __future__ import annotations

from collections.abc import Mapping

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableColumn, TableFormula
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Contribution, Key
from budget_engine.methods.base import Figures, number
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import validation
from budget_engine.sheets.constants import DURATION
from budget_engine.sheets.reference_lists import be_field, column_ref
from budget_engine.sheets.styles import MONEY, QUANTITY, TITLE, put_derived, put_header, put_input

ID = "equipment_depreciation"
SHEET = "Equipment depreciation"
SUMMARY_SHEET = "Equipment summary"
TABLE = "Equipment"

HEADER_ROW = 3
FIRST_DATA_ROW = HEADER_ROW + 1
ITEM_ROWS = 10  # blank equipment rows to start from; the Table grows beyond them

# (input key, Table column) per Human Input, in column order from A.
INPUTS = (
    ("be", "BE/AE nr"),
    ("wp", "WP"),
    ("line", "Cost line"),
    ("item", "Item"),
    ("cost", "Purchase cost (EUR)"),
    ("period", "Depreciation period (months)"),
    ("usage", "Usage share for the action"),
)
COLUMN = dict(INPUTS)  # input key -> Table column
MONTHS = "Months in the project"
LIFE_SHARE = "Share of useful life in the project"
ELIGIBLE = "Eligible cost (EUR)"
CALCULATED = (MONTHS, LIFE_SHARE, ELIGIBLE)
HEADERS = tuple(name for _, name in INPUTS) + CALCULATED
SUMMARY_HEADERS = ("BE/AE nr", "Acronym", "WP", "Cost line", "Items", "Eligible cost (EUR)")


def _col(name: str) -> str:
    return f"{TABLE}[[{name}]]"


def _this_row(name: str) -> str:
    return f"{TABLE}[[#This Row],[{name}]]"


def calculated_formulas(duration: str) -> dict[str, str]:
    """The calculated column formulas of the Equipment Table (without the leading "=").

    ``duration`` is the formula operand of the project duration cell.
    """
    period = _this_row(COLUMN["period"])
    return {
        MONTHS: f"IF({period}>0,MIN({duration},{period}),0)",
        LIFE_SHARE: f"IF({period}>0,{_this_row(MONTHS)}/{period},0)",
        ELIGIBLE: f"{_this_row(COLUMN['cost'])}*{_this_row(COLUMN['usage'])}*{_this_row(LIFE_SHARE)}",
    }


def cost_lines(profile: Profile) -> dict[str, str]:
    """Transfer View line id -> the label a human picks in the Cost line column, in profile order."""
    labels = {r.id: r.label for r in profile.transfer_view_rows if r.kind == "line"}
    return {line: labels[line] for line in profile.method_settings[ID]["cost_lines"]}


def build(ctx: BuildContext) -> None:
    _build_items(ctx)
    _build_summary(ctx)


def _build_items(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = "Equipment depreciation: one row per item; only the depreciation within the project is costed"
    ws["A1"].font = TITLE
    ws["A2"] = (
        "Enter BE/AE nr, WP, cost line, item, purchase cost, depreciation period (months) and the share of its use "
        "for the action. Add rows at the bottom of the Table. Purchase is assumed in the first project month."
    )
    for i, header in enumerate(HEADERS, start=1):
        put_header(ws, f"{get_column_letter(i)}{HEADER_ROW}", header)
    formulas = calculated_formulas(ctx.layout.constants[DURATION].ref)
    formats = {"cost": MONEY, "usage": "0%"}
    last_row = FIRST_DATA_ROW + ITEM_ROWS - 1
    for n in range(1, ITEM_ROWS + 1):
        row = FIRST_DATA_ROW + n - 1
        for i, (key, _) in enumerate(INPUTS, start=1):
            put_input(ctx, ws, f"{get_column_letter(i)}{row}", ("equipment", str(n), key), formats.get(key), free_text=key == "item")
        for i, header in enumerate(CALCULATED, start=len(INPUTS) + 1):
            fmt = MONEY if header == ELIGIBLE else ("0%" if header == LIFE_SHARE else QUANTITY)
            put_derived(ws, f"{get_column_letter(i)}{row}", "=" + formulas[header], fmt)

    table = Table(displayName=TABLE, ref=f"A{HEADER_ROW}:{get_column_letter(len(HEADERS))}{last_row}")
    for i, header in enumerate(HEADERS, start=1):
        calculated = TableFormula(attr_text=formulas[header]) if header in formulas else None
        table.tableColumns.append(TableColumn(id=i, name=header, calculatedColumnFormula=calculated))
    ws.add_table(table)
    _add_validations(ctx, ws, last_row)

    for i, width in enumerate((12, 8, 16, 28, 14, 14, 12, 12, 14, 16), start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[HEADER_ROW].height = 45
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def _add_validations(ctx: BuildContext, ws: Worksheet, last_row: int) -> None:
    def column_range(key: str) -> str:
        letter = get_column_letter(1 + [k for k, _ in INPUTS].index(key))
        return f"{letter}{FIRST_DATA_ROW}:{letter}{last_row}"

    for key, source in (("be", column_ref(ctx.profile, "be_list", "A")), ("wp", column_ref(ctx.profile, "wp_list", "A"))):
        validation.apply(ws, validation.list_of(f'INDIRECT("{source}")'), column_range(key))
    lines = validation.list_of('"' + ",".join(cost_lines(ctx.profile).values()) + '"')
    period = validation.at_least("1", whole=True)
    usage = validation.between("0", "1")
    for dv, key in ((lines, "line"), (validation.non_negative(), "cost"), (period, "period"), (usage, "usage")):
        validation.apply(ws, dv, column_range(key))


def _criteria(code: str, wp: str, label: str) -> str:
    """The SUMIFS/COUNTIFS criteria pairs for one BE/AE code (a formula operand), WP and cost line."""
    return f'{_col(COLUMN["be"])},{code},{_col(COLUMN["wp"])},"{wp}",{_col(COLUMN["line"])},"{label}"'


def _items(code: str, wp: str, label: str) -> str:
    return f'COUNTIFS({_col(COLUMN["cost"])},">0",{_criteria(code, wp, label)})'


def _eligible(code: str, wp: str, label: str) -> str:
    return f"SUMIFS({_col(ELIGIBLE)},{_criteria(code, wp, label)})"


def _build_summary(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SUMMARY_SHEET)
    ws["A1"] = "Equipment summary per BE/AE, work package and cost line (formulas over the Equipment Table)"
    ws["A1"].font = TITLE
    for i, header in enumerate(SUMMARY_HEADERS, start=1):
        put_header(ws, f"{get_column_letter(i)}{HEADER_ROW}", header)
    row = FIRST_DATA_ROW
    for slot in ctx.shape.slots:
        code = ctx.layout.slot_codes[slot]
        for wp in ctx.shape.wp_codes:
            for line, label in cost_lines(ctx.profile).items():
                put_derived(ws, f"A{row}", ctx.layout.slot_label(slot))
                put_derived(ws, f"B{row}", "=" + be_field(ctx, "be_acronym", code))
                put_derived(ws, f"C{row}", wp)
                put_derived(ws, f"D{row}", label)
                for col, figure, fmt in (("E", _items, QUANTITY), ("F", _eligible, MONEY)):
                    total = figure(code, wp, label)
                    # An unclaimed spare block has no code, and must not pick up items without one.
                    put_derived(ws, f"{col}{row}", f'=IF({code}="",0,{total})' if is_spare(slot) else "=" + total, fmt)
                if is_spare(slot):
                    ws.row_dimensions[row].outline_level = 1
                ctx.contributions.append(
                    Contribution(slot, wp, line, Cell(SUMMARY_SHEET, f"E{row}"), Cell(SUMMARY_SHEET, f"F{row}"))
                )
                row += 1
    for col, width in zip("ABCDEF", (12, 14, 8, 16, 10, 16)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def reference(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """Expected items and total per (BE, WP, cost line), from the equipment inputs and the duration.

    Items are the ("equipment", n, field) inputs, including rows added to the Table after the build.
    Eligible cost = purchase cost × usage share × min(duration, period) ÷ period; an item counts
    once it has a purchase cost above zero.
    """
    by_label = {label: line for line, label in cost_lines(profile).items()}
    rows: dict[str, dict[Key, object]] = {}
    for key, value in inputs.items():
        if key[0] == "equipment":
            rows.setdefault(key[1], {})[(key[2],)] = value

    def eligible(item: dict[Key, object]) -> float:
        period = number(item, ("period",))
        if period <= 0:
            return 0.0
        return number(item, ("cost",)) * number(item, ("usage",)) * min(shape.duration_months, period) / period

    figures: Figures = {}
    for slot in shape.slots:
        code = inputs.get(("slot_code", slot)) if is_spare(slot) else slot
        for wp in shape.wp_codes:
            for line in by_label.values():
                figures[(slot, wp, line)] = (0.0, 0.0)
            for item in rows.values():
                picked = by_label.get(str(item.get(("line",))))
                if code is None or picked is None or item.get(("be",)) != code or item.get(("wp",)) != wp:
                    continue
                items, total = figures[(slot, wp, picked)]
                counted = 1.0 if number(item, ("cost",)) > 0 else 0.0
                figures[(slot, wp, picked)] = (items + counted, total + eligible(item))
    return figures

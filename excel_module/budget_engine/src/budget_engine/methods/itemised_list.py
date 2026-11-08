"""Itemised list: any other cost line entered as number of items × cost per item.

An item is a row of the `Items` Excel Table: who incurs it (BE/AE nr), for which WP, which cost
line, what it is, the number of items and the cost per item. Those are Human Inputs; the total is a
calculated column, so a row a human adds is costed too. The cost lines a human can pick are the
profile's ``method_settings.itemised_list.cost_lines``, listed by label beside the Table (a line
without its own label, such as HE's B, takes the label of the heading above it).

The `Itemised list summary` sums the Table with SUMIFS per BE/AE block × WP × cost line.
Output per BE × WP × cost line: items = the number of items, total = the sum of their totals.
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
from budget_engine.sheets.reference_lists import be_field, column_ref
from budget_engine.sheets.styles import MONEY, QUANTITY, TITLE, put_derived, put_header, put_input

ID = "itemised_list"
SHEET = "Itemised list"
SUMMARY_SHEET = "Itemised list summary"
TABLE = "Items"

HEADER_ROW = 3
FIRST_DATA_ROW = HEADER_ROW + 1
ITEM_ROWS = 15  # blank item rows to start from; the Table grows beyond them

# (input key, Table column) per Human Input, in column order from A.
INPUTS = (
    ("be", "BE/AE nr"),
    ("wp", "WP"),
    ("line", "Cost line"),
    ("item", "Item"),
    ("number", "Number of items"),
    ("cost", "Cost per item (EUR)"),
)
COLUMN = dict(INPUTS)  # input key -> Table column
TOTAL = "Total (EUR)"
HEADERS = tuple(name for _, name in INPUTS) + (TOTAL,)
# The cost line labels a human picks from, one column right of the Table after a gap.
PICK_COLUMN = get_column_letter(len(HEADERS) + 2)
PICK_HEADER = "Cost lines"
SUMMARY_HEADERS = ("BE/AE nr", "Acronym", "WP", "Cost line", "Items", "Total (EUR)")


def _col(name: str) -> str:
    return f"{TABLE}[[{name}]]"


def _this_row(name: str) -> str:
    return f"{TABLE}[[#This Row],[{name}]]"


def total_formula() -> str:
    """The Total column's calculated formula (without the leading "=")."""
    return f"{_this_row(COLUMN['number'])}*{_this_row(COLUMN['cost'])}"


def cost_lines(profile: Profile) -> dict[str, str]:
    """Transfer View line id -> the label a human picks in the Cost line column, in profile order."""
    labels: dict[str, str] = {}
    heading = ""
    for r in profile.transfer_view_rows:
        if r.kind == "heading":
            heading = r.label
        elif r.kind == "line":
            labels[r.id] = r.label or heading
    picked = {line: labels[line] for line in profile.method_settings[ID]["cost_lines"]}
    # The summary matches labels with SUMIFS, the reference model by equality: they agree only for
    # distinct labels free of SUMIFS wildcards and comparison operators.
    for label in picked.values():
        if any(ch in label for ch in "*?~") or label[:1] in "<>=":
            raise ValueError(f"itemised list cost line label {label!r} would act as a SUMIFS wildcard or operator")
    if len(set(picked.values())) != len(picked):
        raise ValueError("itemised list cost lines must have distinct labels")
    return picked


def pick_range(profile: Profile) -> tuple[int, int]:
    """First and last row of the cost line pick list."""
    return FIRST_DATA_ROW, FIRST_DATA_ROW + len(cost_lines(profile)) - 1


def pick_list_source(profile: Profile) -> str:
    """The Cost line validation's list source: the pick list range."""
    first, last = pick_range(profile)
    return f"${PICK_COLUMN}${first}:${PICK_COLUMN}${last}"


def build(ctx: BuildContext) -> None:
    _build_items(ctx)
    _build_summary(ctx)


def _build_items(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = "Itemised list: one row per item; total = number of items x cost per item"
    ws["A1"].font = TITLE
    ws["A2"] = (
        "Enter BE/AE nr, WP, cost line, item, number of items and cost per item. "
        "Add rows at the bottom of the Table. The cost lines are listed on the right."
    )
    for i, header in enumerate(HEADERS, start=1):
        put_header(ws, f"{get_column_letter(i)}{HEADER_ROW}", header)
    formats = {"number": QUANTITY, "cost": MONEY}
    last_row = FIRST_DATA_ROW + ITEM_ROWS - 1
    total_col = get_column_letter(len(HEADERS))
    for n in range(1, ITEM_ROWS + 1):
        row = FIRST_DATA_ROW + n - 1
        for i, (key, _) in enumerate(INPUTS, start=1):
            put_input(ctx, ws, f"{get_column_letter(i)}{row}", ("itemised", str(n), key), formats.get(key), free_text=key == "item")
        put_derived(ws, f"{total_col}{row}", "=" + total_formula(), MONEY)

    table = Table(displayName=TABLE, ref=f"A{HEADER_ROW}:{total_col}{last_row}")
    for i, header in enumerate(HEADERS, start=1):
        calculated = TableFormula(attr_text=total_formula()) if header == TOTAL else None
        table.tableColumns.append(TableColumn(id=i, name=header, calculatedColumnFormula=calculated))
    ws.add_table(table)

    put_header(ws, f"{PICK_COLUMN}{HEADER_ROW}", PICK_HEADER)
    for row, label in enumerate(cost_lines(ctx.profile).values(), start=FIRST_DATA_ROW):
        put_derived(ws, f"{PICK_COLUMN}{row}", label)
    _add_validations(ctx, ws, last_row)

    for i, width in enumerate((12, 8, 40, 28, 12, 14, 14, 4, 50), start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[HEADER_ROW].height = 30
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def _add_validations(ctx: BuildContext, ws: Worksheet, last_row: int) -> None:
    def column_range(key: str) -> str:
        letter = get_column_letter(1 + [k for k, _ in INPUTS].index(key))
        return f"{letter}{FIRST_DATA_ROW}:{letter}{last_row}"

    for key, source in (("be", column_ref(ctx.profile, "be_list", "A")), ("wp", column_ref(ctx.profile, "wp_list", "A"))):
        validation.apply(ws, validation.list_of(f'INDIRECT("{source}")'), column_range(key))
    # A range, not an inline list: labels hold commas and together exceed Excel's 255-character limit.
    validation.apply(ws, validation.list_of(pick_list_source(ctx.profile)), column_range("line"))
    validation.apply(ws, validation.non_negative(), column_range("number"), column_range("cost"))


def _sumifs(column: str, code: str, wp: str, label: str) -> str:
    """SUMIFS of one Table column for one BE/AE code, WP and cost line label (formula operands)."""
    return f"SUMIFS({_col(column)},{_col(COLUMN['be'])},{code},{_col(COLUMN['wp'])},{wp},{_col(COLUMN['line'])},{label})"


def _build_summary(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SUMMARY_SHEET)
    ws["A1"] = "Itemised list summary per BE/AE, work package and cost line (formulas over the Items Table)"
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
                # The criteria point at this row's WP and label cells: labels may hold quotes or commas.
                for col, column, fmt in (("E", COLUMN["number"], QUANTITY), ("F", TOTAL, MONEY)):
                    total = _sumifs(column, code, f"C{row}", f"D{row}")
                    # An unclaimed spare block has no code, and must not pick up items without one.
                    put_derived(ws, f"{col}{row}", f'=IF({code}="",0,{total})' if is_spare(slot) else "=" + total, fmt)
                if is_spare(slot):
                    ws.row_dimensions[row].outline_level = 1
                ctx.contributions.append(
                    Contribution(slot, wp, line, Cell(SUMMARY_SHEET, f"E{row}"), Cell(SUMMARY_SHEET, f"F{row}"))
                )
                row += 1
    for col, width in zip("ABCDEF", (12, 14, 8, 50, 10, 16)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def reference(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """Expected items and total per (BE, WP, cost line), from the itemised inputs.

    Items are the ("itemised", n, field) inputs, including rows added to the Table after the build.
    Items = the sum of the numbers of items; total = the sum of number × cost per item.
    """
    by_label = {label: line for line, label in cost_lines(profile).items()}
    rows: dict[str, dict[Key, object]] = {}
    for key, value in inputs.items():
        if key[0] == "itemised":
            rows.setdefault(key[1], {})[(key[2],)] = value

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
                count = number(item, ("number",))
                figures[(slot, wp, picked)] = (items + count, total + count * number(item, ("cost",)))
    return figures

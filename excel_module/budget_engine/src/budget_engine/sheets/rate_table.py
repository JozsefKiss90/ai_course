"""Rate Table: one rate per BE/AE block × Staff Category, in the profile's native unit.

There is a row per Beneficiary and AE, then one per spare block up to the headroom. A spare row's
BE/AE nr is a Human Input: a late partner added to the `BE list` claims a spare block by typing its
code there, and every per-BE/AE structure of that block follows. This sheet comes first among the
per-BE/AE structures, so it owns the block codes the others refer to.
"""

from __future__ import annotations

from openpyxl.utils import get_column_letter

from budget_engine.layout import BuildContext
from budget_engine.shape import is_spare
from budget_engine.sheets import validation
from budget_engine.sheets.reference_lists import be_field, column_ref
from budget_engine.sheets.styles import MONEY, TITLE, put_derived, put_header, put_input

SHEET = "Rate Table"
HEADER_ROW = 3
FIRST_COL = 3  # A: BE/AE nr, B: acronym, then one column per Staff Category


def build_rate_table(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = f"Rate Table ({ctx.profile.rate_unit})"
    ws["A1"].font = TITLE
    ws["A2"] = "Spare rows: type the BE/AE nr of a Beneficiary or AE added late to the BE list, then fill its rates."
    put_header(ws, f"A{HEADER_ROW}", "BE/AE nr")
    put_header(ws, f"B{HEADER_ROW}", "Acronym")
    categories = ctx.profile.staff_categories
    for j, category in enumerate(categories):
        put_header(ws, f"{get_column_letter(FIRST_COL + j)}{HEADER_ROW}", category.label)
    last_row = HEADER_ROW + len(ctx.shape.slots)
    last_col = get_column_letter(FIRST_COL + len(categories) - 1)
    validation.apply(ws, validation.non_negative(), f"{get_column_letter(FIRST_COL)}{HEADER_ROW + 1}:{last_col}{last_row}")
    codes = validation.list_of(f'INDIRECT("{column_ref(ctx.profile, "be_list", "A")}")')
    ws.add_data_validation(codes)
    for i, slot in enumerate(ctx.shape.slots):
        row = HEADER_ROW + 1 + i
        if is_spare(slot):
            ctx.layout.slot_codes[slot] = put_input(ctx, ws, f"A{row}", ("slot_code", slot)).ref
            codes.add(f"A{row}")
            ws.row_dimensions[row].outline_level = 1  # grouped, not hidden: nobody misses a spare block
        else:
            put_derived(ws, f"A{row}", slot)
            ctx.layout.slot_codes[slot] = f'"{slot}"'
        put_derived(ws, f"B{row}", "=" + be_field(ctx, "be_acronym", ctx.layout.slot_codes[slot]))
        for j, category in enumerate(categories):
            put_input(ctx, ws, f"{get_column_letter(FIRST_COL + j)}{row}", ("rate", slot, category.id), MONEY)
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 14
    for j in range(len(categories)):
        ws.column_dimensions[get_column_letter(FIRST_COL + j)].width = 16
    ws.row_dimensions[HEADER_ROW].height = 45
    ws.freeze_panes = f"C{HEADER_ROW + 1}"

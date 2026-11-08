"""Rate Table: one rate per Beneficiary × Staff Category, in the profile's native unit."""

from __future__ import annotations

from openpyxl.utils import get_column_letter

from budget_engine.layout import BuildContext
from budget_engine.sheets.styles import MONEY, TITLE, name_formula, put_derived, put_header, put_input

SHEET = "Rate Table"
HEADER_ROW = 3
FIRST_COL = 3  # A: BE/AE nr, B: acronym, then one column per Staff Category


def build_rate_table(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = f"Rate Table ({ctx.profile.rate_unit})"
    ws["A1"].font = TITLE
    put_header(ws, f"A{HEADER_ROW}", "BE/AE nr")
    put_header(ws, f"B{HEADER_ROW}", "Acronym")
    categories = ctx.profile.staff_categories
    for j, category in enumerate(categories):
        put_header(ws, f"{get_column_letter(FIRST_COL + j)}{HEADER_ROW}", category.label)
    for i, be in enumerate(ctx.shape.be_codes):
        row = HEADER_ROW + 1 + i
        put_derived(ws, f"A{row}", be)
        put_derived(ws, f"B{row}", name_formula(ctx.layout.inputs[("be_acronym", be)].ref))
        for j, category in enumerate(categories):
            put_input(ctx, ws, f"{get_column_letter(FIRST_COL + j)}{row}", ("rate", be, category.id), MONEY)
    ws.column_dimensions["B"].width = 14
    for j in range(len(categories)):
        ws.column_dimensions[get_column_letter(FIRST_COL + j)].width = 16
    ws.row_dimensions[HEADER_ROW].height = 45
    ws.freeze_panes = f"C{HEADER_ROW + 1}"

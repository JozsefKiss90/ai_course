"""Profile Constants: every convention a formula uses, in a labelled, visible cell."""

from __future__ import annotations

from budget_engine.layout import BuildContext, Cell
from budget_engine.sheets.styles import TITLE, WRAP, put_derived, put_header

SHEET = "Profile Constants"
FIRST_ROW = 4
# The project duration is a Shape Parameter, not profile data, but formulas use it the same way:
# it gets its own labelled row under the profile's constants.
DURATION = "duration_months"
DURATION_LABEL = "Project duration (months)"


def build_constants(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = f"Profile Constants - {ctx.profile.name} {ctx.profile.version}"
    ws["A1"].font = TITLE
    ws["A2"] = "Conventions of the Funding Profile. Formulas reference these cells; change one only if the rule itself changes."
    for col, header in zip("ABCD", ("Constant", "Value", "Unit", "Source")):
        put_header(ws, f"{col}3", header)
    for i, constant in enumerate(ctx.profile.constants):
        row = FIRST_ROW + i
        put_derived(ws, f"A{row}", constant.label)
        put_derived(ws, f"B{row}", constant.value)
        put_derived(ws, f"C{row}", constant.unit)
        put_derived(ws, f"D{row}", constant.source)
        ws[f"D{row}"].alignment = WRAP
        ctx.layout.constants[constant.id] = Cell(SHEET, f"B{row}")
    row = FIRST_ROW + len(ctx.profile.constants)
    for col, value in zip("ABCD", (DURATION_LABEL, ctx.shape.duration_months, "months", "Shape Parameter (see the Cover Sheet)")):
        put_derived(ws, f"{col}{row}", value)
    ctx.layout.constants[DURATION] = Cell(SHEET, f"B{row}")
    for col, width in zip("ABCD", (45, 12, 18, 70)):
        ws.column_dimensions[col].width = width

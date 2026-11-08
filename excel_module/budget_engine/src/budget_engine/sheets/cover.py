"""Cover Sheet: provenance, fill-in order and colour legend.

The provenance block is a contract the structural checks read: label in column A, value in B.
"""

from __future__ import annotations

from datetime import date

from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters
from budget_engine.sheets.styles import BOLD, INPUT_FILL, TITLE, BOX, put_derived

SHEET = "Cover"


def provenance(profile: Profile, shape: ShapeParameters, build_date: date | None) -> list[tuple[str, str | int]]:
    """The provenance block, label then value; without a build date, that entry is left out."""
    dated: list[tuple[str, str | int]] = [("Build date", build_date.isoformat())] if build_date else []
    return [
        ("Funding Profile", profile.id),
        ("Profile version", profile.version),
        *dated,
        ("Beneficiaries", shape.beneficiaries),
        ("Work packages", shape.work_packages),
        ("Duration (months)", shape.duration_months),
        ("Estimation Methods", ", ".join(shape.methods)),
        ("Headroom", shape.headroom),
    ]


def build_cover(ctx: BuildContext, ws: Worksheet, fill_in_order: list[str], build_date: date) -> None:
    ws["A1"] = f"Planning Workbook - {ctx.profile.name}"
    ws["A1"].font = TITLE
    ws["A2"] = "Blank workbook. Enter Human Inputs only in light-yellow cells. Never submitted; transfer the Transfer View by hand."

    row = 4
    ws[f"A{row}"] = "Provenance"
    ws[f"A{row}"].font = BOLD
    for label, value in provenance(ctx.profile, ctx.shape, build_date):
        row += 1
        put_derived(ws, f"A{row}", label)
        put_derived(ws, f"B{row}", value)

    row += 2
    ws[f"A{row}"] = "Fill-in order"
    ws[f"A{row}"].font = BOLD
    for i, sheet in enumerate(fill_in_order, start=1):
        row += 1
        ws[f"A{row}"] = f"{i}. {sheet}"

    row += 2
    ws[f"A{row}"] = "Colour legend"
    ws[f"A{row}"].font = BOLD
    row += 1
    ws[f"A{row}"] = "Light yellow: Human Input (you type here)"
    ws[f"B{row}"].fill = INPUT_FILL
    ws[f"B{row}"].border = BOX
    row += 1
    ws[f"A{row}"] = "White: derived by formula (do not overwrite)"
    ws[f"B{row}"].border = BOX

    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 36

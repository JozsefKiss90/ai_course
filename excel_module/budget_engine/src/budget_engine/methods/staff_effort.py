"""Staff effort: effort per WP × Beneficiary × Staff Category, priced from the Rate Table.

Output per BE × WP × cost line: items = effort (in the profile's effort unit), total = effort × rate.
"""

from __future__ import annotations

from collections.abc import Mapping

from openpyxl.utils import get_column_letter

from budget_engine.layout import BuildContext, Cell, Contribution, Key
from budget_engine.methods.base import Figures, number
from budget_engine.profiles import Profile
from budget_engine.sheets.styles import MONEY, QUANTITY, TITLE, name_formula, put_derived, put_header, put_input
from budget_engine.shape import ShapeParameters

ID = "staff_effort"
SHEET = "Staff effort"
HEADER_ROW = 3
FIRST_COL = 4  # A: WP, B: BE/AE nr, C: acronym, then effort columns, then cost columns


def build(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = f"Staff effort ({ctx.profile.effort_unit}) per work package, Beneficiary and Staff Category"
    ws["A1"].font = TITLE
    categories = ctx.profile.staff_categories
    n = len(categories)
    for col, header in zip("ABC", ("WP", "BE/AE nr", "Acronym")):
        put_header(ws, f"{col}{HEADER_ROW}", header)
    for j, category in enumerate(categories):
        put_header(ws, f"{get_column_letter(FIRST_COL + j)}{HEADER_ROW}", f"{category.label} ({ctx.profile.effort_unit})")
        put_header(ws, f"{get_column_letter(FIRST_COL + n + j)}{HEADER_ROW}", f"{category.label} (EUR)")

    row = HEADER_ROW + 1
    for wp in ctx.shape.wp_codes:
        for be in ctx.shape.be_codes:
            put_derived(ws, f"A{row}", wp)
            put_derived(ws, f"B{row}", be)
            put_derived(ws, f"C{row}", name_formula(ctx.layout.inputs[("be_acronym", be)].ref))
            for j, category in enumerate(categories):
                effort_coord = f"{get_column_letter(FIRST_COL + j)}{row}"
                cost_coord = f"{get_column_letter(FIRST_COL + n + j)}{row}"
                put_input(ctx, ws, effort_coord, ("effort", wp, be, category.id), QUANTITY)
                rate = ctx.layout.inputs[("rate", be, category.id)].ref
                put_derived(ws, cost_coord, f"={effort_coord}*{rate}", MONEY)
                ctx.contributions.append(
                    Contribution(be, wp, category.cost_line, Cell(SHEET, effort_coord), Cell(SHEET, cost_coord))
                )
            row += 1

    for j in range(2 * n):
        ws.column_dimensions[get_column_letter(FIRST_COL + j)].width = 14
    ws.row_dimensions[HEADER_ROW].height = 60
    ws.freeze_panes = f"D{HEADER_ROW + 1}"


def reference(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """Expected items and total per (BE, WP, cost line), computed from the inputs alone."""
    figures: Figures = {}
    for wp in shape.wp_codes:
        for be in shape.be_codes:
            for category in profile.staff_categories:
                effort = number(inputs, ("effort", wp, be, category.id))
                rate = number(inputs, ("rate", be, category.id))
                items, total = figures.get((be, wp, category.cost_line), (0.0, 0.0))
                figures[(be, wp, category.cost_line)] = (items + effort, total + effort * rate)
    return figures

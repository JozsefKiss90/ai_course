"""Staff effort: effort per Task (or WP) × BE/AE block × Staff Category, priced from the Rate Table.

With a Task List, effort is planned per task and each task's rows contribute to its WP; without
one, per WP. Spare blocks get rows too, so a late partner's effort needs no rebuild.

Output per BE × WP × cost line: items = effort (in the profile's effort unit), total = effort × rate.
"""

from __future__ import annotations

from collections.abc import Mapping

from openpyxl.utils import get_column_letter

from budget_engine.layout import BuildContext, Cell, Contribution, Key
from budget_engine.methods.base import Figures, number
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import validation
from budget_engine.sheets.reference_lists import be_field
from budget_engine.sheets.styles import MONEY, QUANTITY, TITLE, put_derived, put_header, put_input

ID = "staff_effort"
SHEET = "Staff effort"
HEADER_ROW = 3


def label_headers(shape: ShapeParameters) -> tuple[str, ...]:
    """The label columns from A, before the effort and cost columns."""
    task = ("Task",) if shape.tasks is not None else ()
    return ("WP", *task, "BE/AE nr", "Acronym")


def build(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    grain = "task" if ctx.shape.tasks is not None else "work package"
    ws["A1"] = f"Staff effort ({ctx.profile.effort_unit}) per {grain}, Beneficiary and Staff Category"
    ws["A1"].font = TITLE
    categories = ctx.profile.staff_categories
    n = len(categories)
    headers = label_headers(ctx.shape)
    first_col = len(headers) + 1
    for i, header in enumerate(headers):
        put_header(ws, f"{get_column_letter(i + 1)}{HEADER_ROW}", header)
    for j, category in enumerate(categories):
        put_header(ws, f"{get_column_letter(first_col + j)}{HEADER_ROW}", f"{category.label} ({ctx.profile.effort_unit})")
        put_header(ws, f"{get_column_letter(first_col + n + j)}{HEADER_ROW}", f"{category.label} (EUR)")

    row = HEADER_ROW + 1
    for wp, unit in ctx.shape.effort_units:
        task = (unit,) if ctx.shape.tasks is not None else ()
        for slot in ctx.shape.slots:
            labels = (wp, *task, ctx.layout.slot_label(slot), "=" + be_field(ctx, "be_acronym", ctx.layout.slot_codes[slot]))
            for i, label in enumerate(labels):
                put_derived(ws, f"{get_column_letter(i + 1)}{row}", label)
            if is_spare(slot):
                ws.row_dimensions[row].outline_level = 1
            for j, category in enumerate(categories):
                effort_coord = f"{get_column_letter(first_col + j)}{row}"
                cost_coord = f"{get_column_letter(first_col + n + j)}{row}"
                put_input(ctx, ws, effort_coord, ("effort", unit, slot, category.id), QUANTITY)
                rate = ctx.layout.inputs[("rate", slot, category.id)].ref
                put_derived(ws, cost_coord, f"={effort_coord}*{rate}", MONEY)
                ctx.contributions.append(
                    Contribution(slot, wp, category.cost_line, Cell(SHEET, effort_coord), Cell(SHEET, cost_coord))
                )
            row += 1

    effort = f"{get_column_letter(first_col)}{HEADER_ROW + 1}:{get_column_letter(first_col + n - 1)}{row - 1}"
    validation.apply(ws, validation.non_negative(), effort)
    for j in range(2 * n):
        ws.column_dimensions[get_column_letter(first_col + j)].width = 14
    ws.row_dimensions[HEADER_ROW].height = 60
    ws.freeze_panes = f"{get_column_letter(first_col)}{HEADER_ROW + 1}"


def reference(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """Expected items and total per (BE, WP, cost line), computed from the inputs alone.

    Task effort counts towards the WP the task sits under.
    """
    figures: Figures = {}
    for wp, unit in shape.effort_units:
        for be in shape.slots:
            for category in profile.staff_categories:
                effort = number(inputs, ("effort", unit, be, category.id))
                rate = number(inputs, ("rate", be, category.id))
                items, total = figures.get((be, wp, category.cost_line), (0.0, 0.0))
                figures[(be, wp, category.cost_line)] = (items + effort, total + effort * rate)
    return figures

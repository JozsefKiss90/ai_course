"""Cover Sheet: provenance, the Checks panel, fill-in order and colour legend.

The provenance block is a contract the structural checks read: label in column A, value in B.
So are the fill-in order (one numbered step per row under its heading, see ``sheets/fill_in_order.py``)
and the colour legend (a swatch in column B beside each label).
The Checks panel has a row per Input Guard (label, status, count, kind, where to look) and an
Overall row with the worst status; statuses are formulas, coloured by conditional formatting.
"""

from __future__ import annotations

from datetime import date

from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters
from budget_engine.sheets.input_guards import ERROR, OK, STATUS_FILLS, WARNING, GuardSpec, colour_when
from budget_engine.sheets.styles import BOLD, INPUT_FILL, TITLE, BOX, put_derived, put_header

SHEET = "Cover"
PANEL_TITLE = "Checks panel"
PANEL_HEADERS = ("Guard", "Status", "Count", "Kind", "Where to look")
OVERALL = "Overall"
FILL_IN_ORDER = "Fill-in order"
LEGEND = "Colour legend"
LEGEND_INPUT = "Light yellow: Human Input (you type here)"
LEGEND_DERIVED = "White: derived by formula (do not overwrite)"
LEGEND_HEADER = "Blue: column headers"
LEGEND_GUARDS = "Guards: green OK, amber warning, red error (conditionally coloured)"


def provenance(profile: Profile, shape: ShapeParameters, build_date: date | None) -> list[tuple[str, str | int]]:
    """The provenance block, label then value; without a build date, that entry is left out."""
    tasks = ", ".join(map(str, shape.tasks)) if shape.tasks is not None else "none (effort per work package)"
    dated: list[tuple[str, str | int]] = [("Build date", build_date.isoformat())] if build_date else []
    return [
        ("Funding Profile", profile.id),
        ("Profile version", profile.version),
        *dated,
        ("Beneficiaries", shape.beneficiaries),
        ("Affiliated Entities per Beneficiary", ", ".join(map(str, shape.affiliated_entities))),
        ("Work packages", shape.work_packages),
        ("Tasks per work package", tasks),
        ("Duration (months)", shape.duration_months),
        ("Estimation Methods", ", ".join(shape.methods)),
        ("Headroom (spare BE/AE blocks)", shape.headroom),
    ]


def build_cover(
    ctx: BuildContext, ws: Worksheet, fill_in_order: list[str], build_date: date, guards: list[tuple[GuardSpec, str]]
) -> None:
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

    row = _build_panel(ctx, ws, row + 2, guards)

    row += 2
    ws[f"A{row}"] = FILL_IN_ORDER
    ws[f"A{row}"].font = BOLD
    for i, step in enumerate(fill_in_order, start=1):
        row += 1
        ws[f"A{row}"] = f"{i}. {step}"

    row += 2
    ws[f"A{row}"] = LEGEND
    ws[f"A{row}"].font = BOLD
    row += 1
    ws[f"A{row}"] = LEGEND_INPUT
    ws[f"B{row}"].fill = INPUT_FILL
    ws[f"B{row}"].border = BOX
    row += 1
    ws[f"A{row}"] = LEGEND_DERIVED
    put_derived(ws, f"B{row}", None)
    row += 1
    ws[f"A{row}"] = LEGEND_HEADER
    put_header(ws, f"B{row}", "")
    row += 1
    ws[f"A{row}"] = LEGEND_GUARDS
    for col, status in zip("BCD", (OK, WARNING, ERROR)):
        put_derived(ws, f"{col}{row}", status)
        ws[f"{col}{row}"].fill = STATUS_FILLS[status]

    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 36
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 60


def _build_panel(ctx: BuildContext, ws: Worksheet, row: int, guards: list[tuple[GuardSpec, str]]) -> int:
    """The Checks panel from ``row``; returns its last row."""
    ws[f"A{row}"] = PANEL_TITLE
    ws[f"A{row}"].font = BOLD
    for col, header in zip("ABCDE", PANEL_HEADERS):
        put_header(ws, f"{col}{row + 1}", header)
    first = row + 2
    for i, (spec, count) in enumerate(guards):
        r = first + i
        put_derived(ws, f"A{r}", spec.label)
        put_derived(ws, f"B{r}", f'=IF(C{r}>0,"{spec.severity}","{OK}")')
        put_derived(ws, f"C{r}", f"={count}")
        put_derived(ws, f"D{r}", spec.kind)
        put_derived(ws, f"E{r}", spec.where)
        ctx.layout.outputs[("guard", spec.id, "status")] = Cell(ws.title, f"B{r}")
        ctx.layout.outputs[("guard", spec.id, "count")] = Cell(ws.title, f"C{r}")
    last = first + len(guards) - 1
    overall = last + 1
    statuses = f"B{first}:B{last}"
    put_derived(ws, f"A{overall}", OVERALL, bold=True)
    put_derived(
        ws, f"B{overall}",
        f'=IF(COUNTIF({statuses},"{ERROR}")>0,"{ERROR}",IF(COUNTIF({statuses},"{WARNING}")>0,"{WARNING}","{OK}"))',
        bold=True,
    )
    ctx.layout.outputs[("guard", "overall", "status")] = Cell(ws.title, f"B{overall}")
    for status, fill in STATUS_FILLS.items():
        colour_when(ws, f"B{first}:B{overall}", status, fill)
    note = overall + 2
    if not ctx.profile.rule_checks:
        ws[f"A{note}"] = f"Profile rule checks: {ctx.profile.id} {ctx.profile.version} declares no rule checks."
    else:
        ws[f"A{note}"] = f"Profile rule checks: the rows marked 'rule', as declared by {ctx.profile.id} {ctx.profile.version}."
    return note

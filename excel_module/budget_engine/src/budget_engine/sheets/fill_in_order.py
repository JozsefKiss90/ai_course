"""Fill-in order: the sheets with Human Inputs, in the order their formulas depend on each other.

A sheet depends on another when one of its formulas or data validations reads a cell there that a
human fills in or that a formula fills: by cell reference (`'Rate Table'!$C$4`) or through one of
its Excel Tables (`BEList[[BE/AE nr]]`, also inside an INDIRECT text). Plain constants do not count,
so the duration on the `Profile Constants` sheet ties nothing to it; its plausibility thresholds do.

The order is a topological sort of that graph, read from the workbook itself rather than declared
by hand, so a new sheet or reference cannot silently put a step before what it needs. Among the
sheets whose dependencies are all listed, the next one is the earliest in the workbook; an optional
step (the thresholds) goes only once nothing required is left to list. Reading steps (copy the
Transfer Views, compare the Check sheets, review the Checks panel) follow.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from openpyxl.utils import coordinate_to_tuple, range_boundaries
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import Layout
from budget_engine.methods import equipment_depreciation, itemised_list, staff_effort, travel_planner
from budget_engine.sheets import constants, input_guards, rate_table, task_list

# What a human does on each sheet, shown after the sheet name; the Reference Lists take theirs from the profile.
NOTES = {
    task_list.SHEET: "task titles",
    input_guards.SHEET: "the lead of each work package",
    rate_table.SHEET: "personnel rates per Beneficiary/AE",
    staff_effort.SHEET: "effort per work package (or task)",
    travel_planner.SHEET: "trips",
    equipment_depreciation.SHEET: "equipment items",
    itemised_list.SHEET: "other cost items",
    constants.SHEET: "plausibility thresholds, if you want the warnings (optional)",
}
OPTIONAL = {constants.SHEET}
READING_STEPS = (
    "Transfer View sheets: copy into the Submission Budget",
    "Check sheets: compare with the Submission Budget's own summaries",
    "Cover: review the Checks panel",
)

SHEET_REFERENCE = re.compile(r"(?:'((?:[^']|'')+)'|([A-Za-z_][\w.]*))!(\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)")
TABLE_REFERENCE = re.compile(r"([A-Za-z_][\w.]*)\[")


def input_sheets(wb: Workbook, layout: Layout) -> list[str]:
    """The sheets holding Human Inputs, in workbook order."""
    holding = {c.sheet for c in layout.inputs.values()}
    return [s for s in wb.sheetnames if s in holding]


def dependencies(wb: Workbook, layout: Layout) -> dict[str, set[str]]:
    """Per sheet with Human Inputs, the other such sheets it reads filled cells from."""
    sheets = input_sheets(wb, layout)
    tables = {name: ws.title for ws in wb.worksheets for name in ws.tables}
    # Per sheet, the cells that are not fixed constants: Human Inputs and formulas.
    feeding = {s: {coordinate_to_tuple(c.coord) for c in layout.inputs.values() if c.sheet == s} for s in sheets}
    for s in sheets:
        feeding[s] |= {coordinate_to_tuple(c.coordinate) for row in wb[s].iter_rows() for c in row if _is_formula(c.value)}
    deps: dict[str, set[str]] = {s: set() for s in sheets}
    for sheet in sheets:
        for formula in _formulas(wb[sheet]):
            for table in TABLE_REFERENCE.findall(formula):
                source = tables.get(table)
                if source in deps and source != sheet:
                    deps[sheet].add(source)
            for quoted, plain, area in SHEET_REFERENCE.findall(formula):
                source = quoted.replace("''", "'") or plain
                if source in deps and source != sheet and _feeds(area, feeding[source]):
                    deps[sheet].add(source)
    return deps


def order(wb: Workbook, layout: Layout) -> list[str]:
    """The sheets with Human Inputs, each after every sheet it depends on."""
    deps = dependencies(wb, layout)
    position = {s: i for i, s in enumerate(wb.sheetnames)}
    listed: list[str] = []
    while len(listed) < len(deps):
        ready = [s for s in deps if s not in listed and deps[s] <= set(listed)]
        if not ready:
            raise ValueError(f"circular dependency between sheets {sorted(set(deps) - set(listed))}")
        listed.append(min(ready, key=lambda s: (s in OPTIONAL, position[s])))
    return listed


def steps(wb: Workbook, layout: Layout, notes: dict[str, str]) -> list[str]:
    """The fill-in order as the Cover Sheet lists it: "<sheet>: <what to enter>", then the reading steps."""
    every = {**NOTES, **notes}
    return [f"{s}: {every[s]}" if s in every else s for s in order(wb, layout)] + list(READING_STEPS)


def step_sheet(step: str) -> str:
    """The sheet a listed step names (sheet names cannot contain a colon)."""
    return step.split(":", 1)[0]


def _is_formula(value: object) -> bool:
    return isinstance(value, str) and value.startswith("=")


def _formulas(ws: Worksheet) -> Iterable[str]:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and _is_formula(c.value):
                yield c.value
    for dv in ws.data_validations.dataValidation:
        yield from (f for f in (dv.formula1, dv.formula2) if f)


def _feeds(area: str, feeding: set[tuple[int, int]]) -> bool:
    """True if the area holds a Human Input or a formula (read by position: looking a cell up would create it)."""
    min_col, min_row, max_col, max_row = (int(b or 0) for b in range_boundaries(area.replace("$", "")))
    return any(min_row <= r <= max_row and min_col <= c <= max_col for r, c in feeding)

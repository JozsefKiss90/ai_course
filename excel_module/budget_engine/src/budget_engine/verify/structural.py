"""Structural checks on a blank Planning Workbook (seam 2). No Excel needed.

``check_structure`` returns a list of problems; an empty list means the workbook passes.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.formula.tokenizer import Token, Tokenizer
from openpyxl.utils import get_column_letter
from openpyxl.workbook.workbook import Workbook

from budget_engine.layout import Layout
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import cover, rate_table, reference_lists, transfer_view
from budget_engine.sheets.styles import is_input

TRIVIAL_NUMBERS = {0.0, 1.0}
SPARE_ROWS_CHECKED = 5  # rows below a list that must stay empty
WIDTH_TOLERANCE = 0.01


def check_structure(path: Path, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    problems: list[str] = []
    problems += _check_package(path)
    wb = load_workbook(path)
    problems += _check_reference_lists(wb, shape, profile)
    problems += _check_tables(wb, shape, profile)
    problems += _check_no_cell_references_into_lists(wb, profile)
    problems += _check_blocks(wb, shape, profile, layout)
    problems += _check_inputs_empty(wb, layout)
    problems += _check_no_bare_numbers(wb)
    problems += _check_constants_labelled(wb, layout)
    problems += _check_metadata(wb)
    problems += _check_cover(wb, shape, profile)
    return problems


def _check_package(path: Path) -> list[str]:
    problems = []
    if path.suffix.lower() != ".xlsx":
        problems.append(f"not an .xlsx file: {path.name}")
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
    if any("vbaproject" in n.lower() for n in names):
        problems.append("workbook contains VBA")
    if any(re.search(r"pivot(table|cache)", n, re.I) for n in names):
        problems.append("workbook contains a PivotTable or pivot cache")
    if any(re.search(r"comments\d*\.xml|threadedcomment", n, re.I) for n in names):
        problems.append("workbook contains cell comments")
    return problems


def _check_reference_lists(wb: Workbook, shape: ShapeParameters, profile: Profile) -> list[str]:
    problems: list[str] = []
    expected_codes = {"be_list": shape.entity_codes, "wp_list": shape.wp_codes}
    for which, spec in profile.reference_lists.items():
        name = spec["sheet"]
        if name not in wb.sheetnames:
            problems.append(f"missing Reference List sheet {name!r}")
            continue
        ws = wb[name]
        if ws[spec["title_cell"]].value != spec["title"]:
            problems.append(f"{name}!{spec['title_cell']}: title differs from the Official Budget Table")
        if spec["title_merge"] not in {str(r) for r in ws.merged_cells.ranges}:
            problems.append(f"{name}: title is not merged over {spec['title_merge']}")
        for i, header in enumerate(spec["headers"]):
            coord = f"{get_column_letter(i + 1)}{spec['header_row']}"
            if ws[coord].value != header:
                problems.append(f"{name}!{coord}: header {ws[coord].value!r}, expected {header!r}")
        first = spec["first_data_row"]
        codes = expected_codes[which]
        for i, code in enumerate(codes):
            if ws[f"A{first + i}"].value != code:
                problems.append(f"{name}!A{first + i}: {ws[f'A{first + i}'].value!r}, expected {code!r}")
        for r in range(first + len(codes), first + len(codes) + SPARE_ROWS_CHECKED):
            if ws[f"A{r}"].value is not None:
                problems.append(f"{name}!A{r}: unexpected entry below the list")
        if ws.freeze_panes != f"A{first}":
            problems.append(f"{name}: panes frozen at {ws.freeze_panes}, expected A{first}")
        for col, width in spec["column_widths"].items():
            if abs((ws.column_dimensions[col].width or 0) - width) > WIDTH_TOLERANCE:
                problems.append(f"{name}: column {col} width {ws.column_dimensions[col].width}, expected {width}")
        for r, height in spec["row_heights"].items():
            if ws.row_dimensions[int(r)].height != height:
                problems.append(f"{name}: row {r} height {ws.row_dimensions[int(r)].height}, expected {height}")
        for col, fmt in spec["number_formats"].items():
            for i in range(len(codes)):
                if ws[f"{col}{first + i}"].number_format != fmt:
                    problems.append(f"{name}!{col}{first + i}: number format is not {fmt!r}")
        if which == "be_list":
            for i, code in enumerate(codes):
                expected = reference_lists.role(spec, code)
                if ws[f"B{first + i}"].value != expected:
                    problems.append(f"{name}!B{first + i}: role {ws[f'B{first + i}'].value!r}, expected {expected!r}")
    return problems


def _check_tables(wb: Workbook, shape: ShapeParameters, profile: Profile) -> list[str]:
    """Each Reference List is one Excel Table spanning its headers and every entry, so it can grow."""
    problems = []
    counts = {"be_list": len(shape.entity_codes), "wp_list": shape.work_packages}
    for which, spec in profile.reference_lists.items():
        if spec["sheet"] not in wb.sheetnames:
            continue  # reported with the Reference Lists
        name = reference_lists.TABLES[which]
        tables = wb[spec["sheet"]].tables
        if list(tables) != [name]:
            problems.append(f"{spec['sheet']}: Excel Tables {list(tables)}, expected [{name!r}]")
            continue
        last = spec["first_data_row"] + counts[which] - 1
        ref = f"A{spec['header_row']}:{get_column_letter(len(spec['headers']))}{last}"
        if tables[name].ref != ref:
            problems.append(f"{spec['sheet']}: Table {name} spans {tables[name].ref}, expected {ref}")
        columns = [c.name for c in tables[name].tableColumns]
        if columns != list(spec["headers"]):
            problems.append(f"{spec['sheet']}: Table {name} columns {columns}, expected {spec['headers']}")
    return problems


def _check_no_cell_references_into_lists(wb: Workbook, profile: Profile) -> list[str]:
    """Other sheets reach the Reference Lists by structured reference only: an added row moves cells."""
    list_sheets = [spec["sheet"] for spec in profile.reference_lists.values()]
    prefixes = [f"'{name}'!" for name in list_sheets] + [f"{name}!" for name in list_sheets if " " not in name]
    problems = []
    for ws in wb.worksheets:
        if ws.title in list_sheets:
            continue
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("=") and any(p in c.value for p in prefixes):
                    problems.append(f"{ws.title}!{c.coordinate}: refers to a Reference List cell instead of its Table")
    return problems


def _check_blocks(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """Per BE/AE block, spare ones included: a Transfer View holding one block per WP, a Rate Table
    row, and one staff effort row per WP."""
    problems = []
    expected_tv = [transfer_view.sheet_name(slot) for slot in shape.slots]
    found_tv = [s for s in wb.sheetnames if s.startswith(transfer_view.SHEET_PREFIX)]
    if found_tv != expected_tv:
        problems.append(f"Transfer View sheets {found_tv}, expected {expected_tv}")
    for sheet in set(found_tv) & set(expected_tv):
        titles = [c.value for c in wb[sheet]["A"] if isinstance(c.value, str)]
        for n in range(1, shape.work_packages + 1):
            prefix = '="' + profile.wp_title.format(n=n) + '"'
            count = sum(t.startswith(prefix) for t in titles)
            if count != 1:
                problems.append(f"{sheet}: {count} blocks for WP{n}, expected 1")

    if rate_table.SHEET in wb.sheetnames:
        ws = wb[rate_table.SHEET]
        for i, slot in enumerate(shape.slots):
            coord = f"A{rate_table.HEADER_ROW + 1 + i}"
            if is_spare(slot):
                if not is_input(ws[coord].fill):
                    problems.append(f"{rate_table.SHEET}!{coord}: spare block {slot} has no BE/AE nr input")
            elif ws[coord].value != slot:
                problems.append(f"{rate_table.SHEET}!{coord}: {ws[coord].value!r}, expected {slot!r}")
        below = f"A{rate_table.HEADER_ROW + 1 + len(shape.slots)}"
        if ws[below].value is not None or is_input(ws[below].fill):
            problems.append(f"{rate_table.SHEET}!{below}: unexpected row below the last block")
    else:
        problems.append(f"missing sheet {rate_table.SHEET!r}")

    effort_blocks: set[tuple[str, str]] = set()
    for key, cell in layout.inputs.items():
        if key[0] != "effort" or cell.sheet not in wb.sheetnames:
            continue
        ws = wb[cell.sheet]
        row = cell.row
        wp, slot = key[1:3]
        expected = (wp, layout.slot_label(slot))
        labels = (ws[f"A{row}"].value, ws[f"B{row}"].value)
        if labels != expected:
            problems.append(f"{cell.sheet}!{cell.coord}: staff effort row labelled {labels}, expected {expected}")
        else:
            effort_blocks.add((wp, slot))
    for wp in shape.wp_codes:
        for be in shape.slots:
            if (wp, be) not in effort_blocks:
                problems.append(f"no staff effort block for {wp} x {be}")
    return problems


def _check_inputs_empty(wb: Workbook, layout: Layout) -> list[str]:
    problems = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if is_input(c.fill) and c.value is not None:
                    problems.append(f"{ws.title}!{c.coordinate}: Human Input cell is not empty")
    for key, cell in layout.inputs.items():
        if not is_input(wb[cell.sheet][cell.coord].fill):
            problems.append(f"{cell.sheet}!{cell.coord}: input {key} is not styled as a Human Input")
    return problems


def bare_numbers(formula: str) -> list[float]:
    """Numeric literals in a formula other than the trivial 0 and 1."""
    tokens = Tokenizer(formula).items
    found = []
    for t in tokens:
        if t.type == Token.OPERAND and t.subtype == Token.NUMBER:
            value = float(t.value.rstrip("%")) / (100 if t.value.endswith("%") else 1)
            if value not in TRIVIAL_NUMBERS:
                found.append(value)
    return found


def _check_no_bare_numbers(wb: Workbook) -> list[str]:
    problems = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    numbers = bare_numbers(c.value)
                    if numbers:
                        problems.append(f"{ws.title}!{c.coordinate}: bare numeric literal(s) {numbers} in formula")
    return problems


def _check_constants_labelled(wb: Workbook, layout: Layout) -> list[str]:
    problems = []
    for constant_id, cell in layout.constants.items():
        ws = wb[cell.sheet]
        label_coord = f"A{cell.row}"
        if not isinstance(ws[label_coord].value, str) or not ws[label_coord].value:
            problems.append(f"Profile Constant {constant_id} at {cell.sheet}!{cell.coord} has no label")
        if not isinstance(ws[cell.coord].value, (int, float)):
            problems.append(f"Profile Constant {constant_id} at {cell.sheet}!{cell.coord} has no value")
    return problems


def _check_metadata(wb: Workbook) -> list[str]:
    props = wb.properties
    return [
        f"document property {name} is set ({value!r})"
        for name in ("creator", "lastModifiedBy", "title", "subject", "description", "keywords")
        if (value := getattr(props, name))
    ]


def _check_cover(wb: Workbook, shape: ShapeParameters, profile: Profile) -> list[str]:
    if wb.sheetnames[0] != cover.SHEET:
        return [f"first sheet is {wb.sheetnames[0]!r}, expected the Cover Sheet"]
    ws = wb[cover.SHEET]
    recorded = {r[0].value: r[1].value for r in ws.iter_rows(max_col=2) if r[0].value is not None}
    # The build date is the one entry not fixed by the profile and Shape Parameters.
    expected = dict(cover.provenance(profile, shape, None))
    return [
        f"Cover Sheet records {label} = {recorded.get(label)!r}, expected {value!r}"
        for label, value in expected.items()
        if recorded.get(label) != value
    ]

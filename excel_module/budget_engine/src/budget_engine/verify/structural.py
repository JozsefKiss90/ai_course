"""Structural checks on a blank Planning Workbook (seam 2). No Excel needed.

``check_structure`` returns a list of problems; an empty list means the workbook passes.
"""

from __future__ import annotations

import re
import warnings
import zipfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from lxml import etree
from openpyxl import load_workbook
from openpyxl.formula.tokenizer import Token, Tokenizer
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.cell_range import MultiCellRange
from openpyxl.workbook.workbook import Workbook

from budget_engine.layout import Layout
from budget_engine.methods import equipment_depreciation, itemised_list, travel_planner
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import (
    check_summaries, constants, cover, fill_in_order, input_guards, rate_table, reference_lists, task_list,
    transfer_view, validation,
)
from budget_engine.sheets.styles import is_derived, is_input
from budget_engine.verify.scenario import provisional_scenario

TRIVIAL_NUMBERS = {0.0, 1.0}
SPARE_ROWS_CHECKED = 5  # rows below a list that must stay empty
WIDTH_TOLERANCE = 0.01


def check_structure(path: Path, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    problems: list[str] = []
    problems += _check_package(path)
    with warnings.catch_warnings():
        # openpyxl does not read x14 data validations (the Country dropdown); _check_validations does.
        warnings.filterwarnings("ignore", message="Data Validation extension is not supported")
        wb = load_workbook(path)
    problems += _check_reference_lists(wb, shape, profile)
    problems += _check_tables(wb, shape, profile)
    problems += _check_task_list(wb, shape)
    problems += _check_no_cell_references_into_lists(wb, profile)
    problems += _check_blocks(wb, shape, profile, layout)
    problems += _check_travel(wb, shape, profile, layout)
    problems += _check_equipment(wb, shape, profile, layout)
    problems += _check_itemised(wb, shape, profile, layout)
    problems += _check_summaries(wb, shape, profile, layout)
    problems += _check_duration(wb, shape, layout)
    problems += _check_country_list(wb, profile)
    problems += _check_validations(path, wb, layout)
    problems += _check_guards(wb, shape, profile, layout)
    problems += _check_inputs_empty(wb, layout)
    problems += _check_no_bare_numbers(wb)
    problems += _check_constants_labelled(wb, layout)
    problems += _check_no_synthetic_values(wb, shape, profile, layout)
    problems += _check_styling(wb, layout)
    problems += _check_metadata(path, wb)
    problems += _check_cover(wb, shape, profile)
    problems += _check_fill_in_order(wb, layout)
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


def _check_task_list(wb: Workbook, shape: ShapeParameters) -> list[str]:
    """With tasks, one Excel Table row per task under its WP; without, no Task List at all."""
    name = task_list.SHEET
    if shape.tasks is None:
        return [f"unexpected {name!r} sheet in a build without tasks"] if name in wb.sheetnames else []
    if name not in wb.sheetnames:
        return [f"missing sheet {name!r}"]
    ws = wb[name]
    problems = []
    units = shape.effort_units
    first = task_list.FIRST_DATA_ROW
    for i, entry in enumerate(units):
        for col, expected in zip("BA", entry):  # effort_units are (WP, task); the sheet shows task, WP
            if ws[f"{col}{first + i}"].value != expected:
                problems.append(f"{name}!{col}{first + i}: {ws[f'{col}{first + i}'].value!r}, expected {expected!r}")
    for r in range(first + len(units), first + len(units) + SPARE_ROWS_CHECKED):
        if ws[f"A{r}"].value is not None:
            problems.append(f"{name}!A{r}: unexpected entry below the list")
    table = task_list.TABLE
    if list(ws.tables) != [table]:
        return problems + [f"{name}: Excel Tables {list(ws.tables)}, expected [{table!r}]"]
    ref = f"A{task_list.HEADER_ROW}:C{first + len(units) - 1}"
    if ws.tables[table].ref != ref:
        problems.append(f"{name}: Table {table} spans {ws.tables[table].ref}, expected {ref}")
    columns = [c.name for c in ws.tables[table].tableColumns]
    if columns != list(task_list.HEADERS):
        problems.append(f"{name}: Table {table} columns {columns}, expected {list(task_list.HEADERS)}")
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
    row, and one staff effort row per WP (per task, with a Task List)."""
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

    wp_of = {unit: wp for wp, unit in shape.effort_units}
    effort_blocks: set[tuple[str, str]] = set()
    for key, cell in layout.inputs.items():
        if key[0] != "effort" or cell.sheet not in wb.sheetnames:
            continue
        ws = wb[cell.sheet]
        unit, slot = key[1:3]
        task = (unit,) if shape.tasks is not None else ()
        expected = (wp_of.get(unit), *task, layout.slot_label(slot))
        labels = tuple(ws[f"{get_column_letter(i + 1)}{cell.row}"].value for i in range(len(expected)))
        if labels != expected:
            problems.append(f"{cell.sheet}!{cell.coord}: staff effort row labelled {labels}, expected {expected}")
        else:
            effort_blocks.add((unit, slot))
    for _, unit in shape.effort_units:
        for be in shape.slots:
            if (unit, be) not in effort_blocks:
                problems.append(f"no staff effort block for {unit} x {be}")
    return problems


def _check_travel(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """With the travel planner: the Trips Table priced by formula, the unit costs exactly as in the
    profile data, and one summary row per BE/AE block × WP. Without it: no travel sheets."""
    tp = travel_planner
    sheets = (tp.SHEET, tp.SUMMARY_SHEET, tp.UNIT_COSTS_SHEET)
    if tp.ID not in shape.methods:
        return [f"unexpected {name!r} sheet: the travel planner is switched off" for name in sheets if name in wb.sheetnames]
    missing = [f"missing sheet {name!r}" for name in sheets if name not in wb.sheetnames]
    if missing:
        return missing
    problems: list[str] = []

    ws = wb[tp.SHEET]
    last = tp.FIRST_DATA_ROW + tp.TRIP_ROWS - 1
    formulas = tp.price_formulas()
    if list(ws.tables) != [tp.TABLE]:
        problems.append(f"{tp.SHEET}: Excel Tables {list(ws.tables)}, expected [{tp.TABLE!r}]")
    else:
        table = ws.tables[tp.TABLE]
        ref = f"A{tp.HEADER_ROW}:{get_column_letter(len(tp.HEADERS))}{last}"
        if table.ref != ref:
            problems.append(f"{tp.SHEET}: Table {tp.TABLE} spans {table.ref}, expected {ref}")
        columns = [(c.name, c.calculatedColumnFormula.attr_text if c.calculatedColumnFormula else None) for c in table.tableColumns]
        expected = [(name, formulas.get(name)) for name in tp.HEADERS]
        if columns != expected:
            problems.append(f"{tp.SHEET}: Table {tp.TABLE} columns or calculated formulas differ from the travel planner's")
    for i, header in enumerate(tp.PRICES, start=len(tp.INPUTS) + 1):
        for row in range(tp.FIRST_DATA_ROW, last + 1):
            coord = f"{get_column_letter(i)}{row}"
            if ws[coord].value != "=" + formulas[header]:
                problems.append(f"{tp.SHEET}!{coord}: {header} is not the unit-cost lookup formula")

    ws = wb[tp.UNIT_COSTS_SHEET]
    for first_col, name, rows in zip(
        (tp.BANDS_FIRST_COL, tp.RATES_FIRST_COL), (tp.BANDS_TABLE, tp.RATES_TABLE), tp.unit_cost_rows(profile)
    ):
        last_cell = f"{get_column_letter(first_col + len(rows[0]) - 1)}{tp.FIRST_DATA_ROW + len(rows) - 1}"
        ref = f"{get_column_letter(first_col)}{tp.HEADER_ROW}:{last_cell}"
        if name not in ws.tables or ws.tables[name].ref != ref:
            problems.append(f"{tp.UNIT_COSTS_SHEET}: Table {name} missing or not spanning {ref}")
        for i, values in enumerate(rows):
            for j, value in enumerate(values):
                coord = f"{get_column_letter(first_col + j)}{tp.FIRST_DATA_ROW + i}"
                if ws[coord].value != value:
                    problems.append(f"{tp.UNIT_COSTS_SHEET}!{coord}: {ws[coord].value!r}, profile data has {value!r}")

    ws = wb[tp.SUMMARY_SHEET]
    row = tp.FIRST_DATA_ROW
    for slot in shape.slots:
        for wp in shape.wp_codes:
            labels = (ws[f"A{row}"].value, ws[f"C{row}"].value)
            if labels != (layout.slot_label(slot), wp):
                problems.append(f"{tp.SUMMARY_SHEET}!A{row}: row labelled {labels}, expected {(layout.slot_label(slot), wp)}")
            row += 1
    if ws[f"C{row}"].value is not None:
        problems.append(f"{tp.SUMMARY_SHEET}!C{row}: unexpected row below the last block")
    return problems


def _check_equipment(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """With equipment depreciation: the Equipment Table costed by formula from the project duration,
    and one summary row per BE/AE block × WP × C.2 cost line. Without it: no equipment sheets."""
    ed = equipment_depreciation
    sheets = (ed.SHEET, ed.SUMMARY_SHEET)
    if ed.ID not in shape.methods:
        return [f"unexpected {name!r} sheet: equipment depreciation is switched off" for name in sheets if name in wb.sheetnames]
    missing = [f"missing sheet {name!r}" for name in sheets if name not in wb.sheetnames]
    if missing:
        return missing
    problems: list[str] = []

    ws = wb[ed.SHEET]
    last = ed.FIRST_DATA_ROW + ed.ITEM_ROWS - 1
    formulas = ed.calculated_formulas(layout.constants[constants.DURATION].ref)
    if list(ws.tables) != [ed.TABLE]:
        problems.append(f"{ed.SHEET}: Excel Tables {list(ws.tables)}, expected [{ed.TABLE!r}]")
    else:
        table = ws.tables[ed.TABLE]
        ref = f"A{ed.HEADER_ROW}:{get_column_letter(len(ed.HEADERS))}{last}"
        if table.ref != ref:
            problems.append(f"{ed.SHEET}: Table {ed.TABLE} spans {table.ref}, expected {ref}")
        columns = [(c.name, c.calculatedColumnFormula.attr_text if c.calculatedColumnFormula else None) for c in table.tableColumns]
        if columns != [(name, formulas.get(name)) for name in ed.HEADERS]:
            problems.append(f"{ed.SHEET}: Table {ed.TABLE} columns or calculated formulas differ from equipment depreciation's")
    for i, header in enumerate(ed.CALCULATED, start=len(ed.INPUTS) + 1):
        for row in range(ed.FIRST_DATA_ROW, last + 1):
            coord = f"{get_column_letter(i)}{row}"
            if ws[coord].value != "=" + formulas[header]:
                problems.append(f"{ed.SHEET}!{coord}: {header} is not the depreciation formula")

    ws = wb[ed.SUMMARY_SHEET]
    row = ed.FIRST_DATA_ROW
    for slot in shape.slots:
        for wp in shape.wp_codes:
            for label in ed.cost_lines(profile).values():
                labels = (ws[f"A{row}"].value, ws[f"C{row}"].value, ws[f"D{row}"].value)
                expected = (layout.slot_label(slot), wp, label)
                if labels != expected:
                    problems.append(f"{ed.SUMMARY_SHEET}!A{row}: row labelled {labels}, expected {expected}")
                row += 1
    if ws[f"C{row}"].value is not None:
        problems.append(f"{ed.SUMMARY_SHEET}!C{row}: unexpected row below the last block")
    return problems


def _check_itemised(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """With the itemised list: the Items Table totalled by formula, the profile's cost lines as the
    pick list, and one summary row per BE/AE block × WP × cost line. Without it: no itemised sheets."""
    il = itemised_list
    sheets = (il.SHEET, il.SUMMARY_SHEET)
    if il.ID not in shape.methods:
        return [f"unexpected {name!r} sheet: the itemised list is switched off" for name in sheets if name in wb.sheetnames]
    missing = [f"missing sheet {name!r}" for name in sheets if name not in wb.sheetnames]
    if missing:
        return missing
    problems: list[str] = []
    labels = list(il.cost_lines(profile).values())

    ws = wb[il.SHEET]
    last = il.FIRST_DATA_ROW + il.ITEM_ROWS - 1
    total_col = get_column_letter(len(il.HEADERS))
    if list(ws.tables) != [il.TABLE]:
        problems.append(f"{il.SHEET}: Excel Tables {list(ws.tables)}, expected [{il.TABLE!r}]")
    else:
        table = ws.tables[il.TABLE]
        ref = f"A{il.HEADER_ROW}:{total_col}{last}"
        if table.ref != ref:
            problems.append(f"{il.SHEET}: Table {il.TABLE} spans {table.ref}, expected {ref}")
        columns = [(c.name, c.calculatedColumnFormula.attr_text if c.calculatedColumnFormula else None) for c in table.tableColumns]
        expected = [(name, il.total_formula() if name == il.TOTAL else None) for name in il.HEADERS]
        if columns != expected:
            problems.append(f"{il.SHEET}: Table {il.TABLE} columns or calculated formulas differ from the itemised list's")
    for row in range(il.FIRST_DATA_ROW, last + 1):
        if ws[f"{total_col}{row}"].value != "=" + il.total_formula():
            problems.append(f"{il.SHEET}!{total_col}{row}: {il.TOTAL} is not number of items x cost per item")
    first, _ = il.pick_range(profile)
    for row, label in enumerate(labels, start=first):
        if ws[f"{il.PICK_COLUMN}{row}"].value != label:
            problems.append(f"{il.SHEET}!{il.PICK_COLUMN}{row}: pick list entry {ws[f'{il.PICK_COLUMN}{row}'].value!r}, expected {label!r}")
    line_column = f"C{il.FIRST_DATA_ROW}:C{last}"
    picks = [dv for dv in ws.data_validations.dataValidation if line_column in str(dv.sqref)]
    if not picks or picks[0].type != "list" or picks[0].formula1 != il.pick_list_source(profile):
        problems.append(f"{il.SHEET}!{line_column}: the Cost line is not validated against the pick list")

    ws = wb[il.SUMMARY_SHEET]
    row = il.FIRST_DATA_ROW
    for slot in shape.slots:
        for wp in shape.wp_codes:
            for label in labels:
                found = (ws[f"A{row}"].value, ws[f"C{row}"].value, ws[f"D{row}"].value)
                expected_labels = (layout.slot_label(slot), wp, label)
                if found != expected_labels:
                    problems.append(f"{il.SUMMARY_SHEET}!A{row}: row labelled {found}, expected {expected_labels}")
                row += 1
    if ws[f"C{row}"].value is not None:
        problems.append(f"{il.SUMMARY_SHEET}!C{row}: unexpected row below the last block")
    return problems


def _check_summaries(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """The Check Summaries after the Transfer Views: a grid row per BE/AE block with total and share
    rows, the summary per WP's rows in the profile's order per WP and for all WPs, and a formula in
    every figure cell (no typed-in figures, no PivotTables)."""
    names = check_summaries.sheets(profile)
    missing = [f"missing sheet {name!r}" for name in names if name not in wb.sheetnames]
    if missing:
        return missing
    problems: list[str] = []
    if wb.sheetnames[-len(names):] != names:
        problems.append(f"the Check Summaries {names} are not the last sheets")
    cs = profile.check_summaries

    for summary in ("lump_sum", "effort"):
        spec = cs[summary]
        ws = wb[spec["sheet"]]
        if ws["A1"].value != spec["title"]:
            problems.append(f"{ws.title}!A1: title {ws['A1'].value!r}, expected {spec['title']!r}")
        row = check_summaries.GRID_FIRST_ROW
        for slot in shape.slots:
            label = ws[f"A{row}"].value
            expected = _grid_label_mark(slot, layout)
            if not (isinstance(label, str) and expected in label):
                problems.append(f"{ws.title}!A{row}: row label {label!r} is not the one of block {slot}")
            row += 1
        for key in ("total_row", "share_row"):
            if ws[f"A{row}"].value != cs["grid"][key]:
                problems.append(f"{ws.title}!A{row}: {ws[f'A{row}'].value!r}, expected {cs['grid'][key]!r}")
            row += 1

    spec = cs["per_wp"]
    ws = wb[spec["sheet"]]
    row = transfer_view.HEADER_ROW + 2
    for n in range(1, shape.work_packages + 2):
        title = ws[f"A{row}"].value
        if n > shape.work_packages:
            if title != spec["all_title"]:
                problems.append(f"{ws.title}!A{row}: {title!r}, expected {spec['all_title']!r}")
        elif not (isinstance(title, str) and title.startswith('="' + profile.wp_title.format(n=n) + '"')):
            problems.append(f"{ws.title}!A{row}: {title!r} is not the title of WP{n}")
        row += 2
        for row_spec in profile.transfer_view_rows:
            if row_spec.label and ws[f"A{row}"].value != row_spec.label:
                problems.append(f"{ws.title}!A{row}: label {ws[f'A{row}'].value!r}, expected {row_spec.label!r}")
            row += 1
        row += transfer_view.GAP_AFTER_WP

    for figure, cell in layout.outputs.items():
        if cell.sheet in names:
            value = wb[cell.sheet][cell.coord].value
            if not (isinstance(value, str) and value.startswith("=")):
                problems.append(f"{cell.sheet}!{cell.coord}: {' '.join(figure)} is not a formula")
    return problems


def _grid_label_mark(slot: str, layout: Layout) -> str:
    """What a grid row label of a block must contain: its code, or for a spare block the code's cell."""
    return layout.slot_codes[slot] if is_spare(slot) else f'="{slot}: "'


def _check_country_list(wb: Workbook, profile: Profile) -> list[str]:
    """The hidden CountryList sheet holds the profile's countries, header first, as the Official's does."""
    name = reference_lists.COUNTRY_SHEET
    if name not in wb.sheetnames:
        return [f"missing sheet {name!r}"]
    ws = wb[name]
    problems = [] if ws.sheet_state == "hidden" else [f"{name}: not hidden, as in the Official Budget Table"]
    expected = [reference_lists.COUNTRY_HEADER, *profile.countries, None]
    for row, value in enumerate(expected, start=1):
        if ws[f"A{row}"].value != value:
            problems.append(f"{name}!A{row}: {ws[f'A{row}'].value!r}, expected {value!r}")
    return problems


@dataclass(frozen=True)
class _Validation:
    type: str
    cells: MultiCellRange
    formula1: str | None
    blocking: bool


def _read_validations(path: Path, sheets: set[str]) -> dict[str, list[_Validation]]:
    """The data validations of ``sheets`` as written in the file, the x14 ones openpyxl skips included."""
    found: dict[str, list[_Validation]] = {}
    m, x14, xm = validation.MAIN, validation.X14, validation.XM
    with zipfile.ZipFile(path) as z:
        for sheet in sheets:
            root = etree.fromstring(z.read(validation.sheet_part(z, sheet)))
            standard = [
                (dv, dv.get("sqref"), dv.findtext(f"{{{m}}}formula1")) for dv in root.iter(f"{{{m}}}dataValidation")
            ]
            extension = [
                (dv, dv.findtext(f"{{{xm}}}sqref"), dv.findtext(f"{{{x14}}}formula1/{{{xm}}}f"))
                for dv in root.iter(f"{{{x14}}}dataValidation")
            ]
            found[sheet] = [
                _Validation(str(dv.get("type")), MultiCellRange(sqref or ""), formula, dv.get("showErrorMessage") in ("1", "true"))
                for dv, sqref, formula in standard + extension
            ]
    return found


def _check_validations(path: Path, wb: Workbook, layout: Layout) -> list[str]:
    """Every Human Input but free text has one data validation that refuses invalid entries; numbers
    are never allowed below zero."""
    checked = {k: c for k, c in layout.inputs.items() if k not in layout.free_text and c.sheet in wb.sheetnames}
    by_sheet = _read_validations(path, {c.sheet for c in checked.values()})
    problems = []
    for key, cell in checked.items():
        covering = [v for v in by_sheet[cell.sheet] if cell.coord in v.cells]
        where = f"{cell.sheet}!{cell.coord}: Human Input {' '.join(key)}"
        if len(covering) != 1:
            problems.append(f"{where} has {len(covering)} data validations, expected 1")
            continue
        v = covering[0]
        if not v.blocking:
            problems.append(f"{where} has a data validation that does not refuse invalid entries")
        if v.type in ("decimal", "whole") and not _at_least_zero(v.formula1):
            problems.append(f"{where} has a data validation that allows negative numbers")
    return problems


def _at_least_zero(formula: str | None) -> bool:
    try:
        return formula is not None and float(formula) >= 0
    except ValueError:
        return False


def _check_guards(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """The Input Guards sheet, and a Checks panel row with formula status and count for every guard."""
    problems = [] if input_guards.SHEET in wb.sheetnames else [f"missing sheet {input_guards.SHEET!r}"]
    expected = [s.id for s in input_guards.guard_specs(profile, shape)] + ["overall"]
    found = list(dict.fromkeys(k[1] for k in layout.outputs if k[0] == "guard"))
    if found != expected:
        problems.append(f"Checks panel guards {found}, expected {expected}")
    for figure, cell in layout.outputs.items():
        if figure[0] != "guard":
            continue
        value = wb[cell.sheet][cell.coord].value
        if not (isinstance(value, str) and value.startswith("=")):
            problems.append(f"{cell.sheet}!{cell.coord}: {' '.join(figure)} is not a formula")
    return problems


def _check_duration(wb: Workbook, shape: ShapeParameters, layout: Layout) -> list[str]:
    """The project duration formulas use sits in its labelled cell and equals the Shape Parameter."""
    cell = layout.constants[constants.DURATION]
    ws = wb[cell.sheet]
    problems = []
    if ws[f"A{cell.row}"].value != constants.DURATION_LABEL:
        problems.append(f"{cell.sheet}!A{cell.row}: {ws[f'A{cell.row}'].value!r}, expected {constants.DURATION_LABEL!r}")
    if ws[cell.coord].value != shape.duration_months:
        problems.append(f"{cell.sheet}!{cell.coord}: project duration {ws[cell.coord].value!r}, expected {shape.duration_months}")
    return problems


def _check_inputs_empty(wb: Workbook, layout: Layout) -> list[str]:
    problems = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if is_input(c.fill) and c.value is not None:
                    problems.append(f"{ws.title}!{c.coordinate}: Human Input cell is not empty")
    for key, cell in layout.inputs.items():
        if cell.sheet in wb.sheetnames and not is_input(wb[cell.sheet][cell.coord].fill):
            problems.append(f"{cell.sheet}!{cell.coord}: input {key} is not styled as a Human Input")
    return problems


# A cell reference such as E4 or $B$12 (not the exponent of a literal like 1E3).
CELL_REFERENCE = re.compile(r"(?<![0-9.])\$?[A-Z]{1,3}\$?[0-9]+")


def bare_numbers(formula: str) -> list[float]:
    """Numeric literals in a formula other than the trivial 0 and 1."""
    # Row after row repeats a formula with other cell references; tokenizing each one once keeps
    # the check fast for large shapes. Replacing references never adds or removes a numeric literal.
    return list(_bare_numbers(CELL_REFERENCE.sub("A1", formula)))


@lru_cache(maxsize=4096)
def _bare_numbers(formula: str) -> tuple[float, ...]:
    tokens = Tokenizer(formula).items
    found = []
    for t in tokens:
        if t.type == Token.OPERAND and t.subtype == Token.NUMBER:
            value = float(t.value.rstrip("%")) / (100 if t.value.endswith("%") else 1)
            if value not in TRIVIAL_NUMBERS:
                found.append(value)
    return tuple(found)


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


EXTENDED_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
APP_PROPERTIES = "docProps/app.xml"
# Extended properties that name a person, an organisation or a location.
PERSONAL_APP_PROPERTIES = ("Company", "Manager", "HyperlinkBase")
# A saved path: a drive letter, a UNC share or a file URL.
SAVE_PATH = re.compile(rb"[A-Za-z]:\\|\\\\[A-Za-z0-9]|file:/", re.I)


def _check_metadata(path: Path, wb: Workbook) -> list[str]:
    """No author, last-modified-by or other identifying property, and no save path anywhere in the package."""
    props = wb.properties
    problems = [
        f"document property {name} is set ({value!r})"
        for name in ("creator", "lastModifiedBy", "title", "subject", "description", "keywords", "category")
        if (value := getattr(props, name))
    ]
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "docProps/custom.xml" in names:
            problems.append("workbook has custom document properties")
        if APP_PROPERTIES in names:
            app = etree.fromstring(z.read(APP_PROPERTIES))
            for name in PERSONAL_APP_PROPERTIES:
                found = app.find(f"{{{EXTENDED_NS}}}{name}")
                if found is not None and (found.text or "").strip():
                    problems.append(f"document property {name} is set ({found.text!r})")
        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            data = z.read(name)
            if b"absPath" in data:
                problems.append(f"{name}: records the path the workbook was saved at (absPath)")
            if SAVE_PATH.search(data):
                problems.append(f"{name}: contains a file path")
    return problems


def _check_no_synthetic_values(wb: Workbook, shape: ShapeParameters, profile: Profile, layout: Layout) -> list[str]:
    """No value the Synthetic Check types into its copy may appear in the deliverable.

    Every Human Input must be empty (``_check_inputs_empty``); on top, the scenario's free text
    (fake names, titles, item descriptions) must not sit in any cell at all.
    """
    scenario = provisional_scenario(profile, shape, layout)
    free_text = {(k[0], k[-1]) for k in layout.free_text}
    entries = {**scenario.inputs, **scenario.added_inputs}
    fake = {v for k, v in entries.items() if isinstance(v, str) and (k[0], k[-1]) in free_text}
    return [
        f"{ws.title}!{c.coordinate}: synthetic value {c.value!r}"
        for ws in wb.worksheets
        for row in ws.iter_rows()
        for c in row
        if isinstance(c.value, str) and c.value in fake
    ]


def _check_styling(wb: Workbook, layout: Layout) -> list[str]:
    """Light yellow marks Human Inputs and nothing else; every figure the engine reads back is derived (white)."""
    inputs = {(c.sheet, c.coord) for c in layout.inputs.values()}
    swatch = _legend_swatches(wb).get(cover.LEGEND_INPUT)
    problems = [
        f"{ws.title}!{c.coordinate}: light yellow but not a Human Input"
        for ws in wb.worksheets
        for row in ws.iter_rows()
        for c in row
        if is_input(c.fill) and (ws.title, c.coordinate) not in inputs and (ws.title, c.coordinate) != swatch
    ]
    for key, cell in layout.outputs.items():
        if cell.sheet in wb.sheetnames and not is_derived(wb[cell.sheet][cell.coord].fill):
            problems.append(f"{cell.sheet}!{cell.coord}: derived figure {' '.join(key)} is not styled as derived")
    return problems


LEGEND_LABELS = (cover.LEGEND_INPUT, cover.LEGEND_DERIVED, cover.LEGEND_HEADER, cover.LEGEND_GUARDS)


def _legend_swatches(wb: Workbook) -> dict[str, tuple[str, str]]:
    """Cover legend label -> its swatch cell (column B of the label's row)."""
    if cover.SHEET not in wb.sheetnames:
        return {}
    ws = wb[cover.SHEET]
    return {c.value: (ws.title, f"B{c.row}") for c in ws["A"] if c.value in LEGEND_LABELS}


def _check_legend(wb: Workbook) -> list[str]:
    swatches = _legend_swatches(wb)
    ws = wb[cover.SHEET]
    problems = [f"Cover Sheet colour legend has no entry {label!r}" for label in LEGEND_LABELS if label not in swatches]
    fills = {cover.LEGEND_INPUT: is_input, cover.LEGEND_DERIVED: is_derived}
    for label, matches in fills.items():
        if label in swatches and not matches(ws[swatches[label][1]].fill):
            problems.append(f"Cover Sheet colour legend: the swatch for {label!r} has the wrong fill")
    return problems


def _check_fill_in_order(wb: Workbook, layout: Layout) -> list[str]:
    """The Cover's fill-in order lists every sheet with Human Inputs, each after the sheets it depends on."""
    if cover.SHEET not in wb.sheetnames:
        return []
    column = [c.value for c in wb[cover.SHEET]["A"]]
    if cover.FILL_IN_ORDER not in column:
        return ["Cover Sheet has no fill-in order"]
    listed = []
    for value in column[column.index(cover.FILL_IN_ORDER) + 1:]:
        if not isinstance(value, str) or not re.match(r"\d+\. ", value):
            break
        listed.append(fill_in_order.step_sheet(value.split(". ", 1)[1]))
    position = {sheet: i for i, sheet in enumerate(listed)}
    problems = [f"fill-in order does not list {s!r}" for s in fill_in_order.input_sheets(wb, layout) if s not in position]
    for sheet, needs in fill_in_order.dependencies(wb, layout).items():
        for need in sorted(needs):
            if sheet in position and need in position and position[need] > position[sheet]:
                problems.append(f"fill-in order lists {sheet!r} before {need!r}, which it depends on")
    return problems


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
    ] + _check_legend(wb)

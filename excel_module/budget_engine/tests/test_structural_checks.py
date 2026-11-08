"""Seam 2: structural checks on the blank Planning Workbook, without Excel.

Every workbook comes from the build entry point. The checks must pass on what the build writes and
must fail on a copy that breaks one of the rules.
"""

import shutil
import time
import warnings
import zipfile
from pathlib import Path

import pytest
from openpyxl import load_workbook

from budget_engine import build, check_structure

HE = {"id": "he-lump-sum", "version": "1.0"}
OFFICIAL_BUDGET_TABLE = Path(__file__).parents[2] / "docs" / "detailed-budget-table_he-ls-euratom_en.xlsm"


def shape(**overrides: object) -> dict[str, object]:
    params: dict[str, object] = {"profile": HE, "beneficiaries": 2, "work_packages": 3, "duration_months": 36}
    params.update(overrides)
    return params


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    return build(shape(), tmp_path_factory.mktemp("built") / "planning.xlsx")


@pytest.mark.parametrize(
    "beneficiaries, work_packages, duration_months, headroom",
    [(1, 1, 1, 0), (2, 3, 36, 3), (5, 7, 48, None), (12, 10, 60, 1), (25, 15, 84, 0)],
)
def test_structural_checks_pass_across_shapes(tmp_path, beneficiaries, work_packages, duration_months, headroom):
    params = shape(beneficiaries=beneficiaries, work_packages=work_packages, duration_months=duration_months)
    if headroom is not None:
        params["headroom"] = headroom
    started = time.perf_counter()
    result = build(params, tmp_path / "planning.xlsx")  # raises BuildError if a check fails
    assert time.perf_counter() - started < 10, "structural checks must be fast enough for every build"

    wb = load_workbook(result.path)
    spare = 3 if headroom is None else headroom
    expected_tv = [f"Transfer View BE{i}" for i in range(1, beneficiaries + 1)]
    expected_tv += [f"Transfer View spare {i}" for i in range(1, spare + 1)]
    assert [s for s in wb.sheetnames if s.startswith("Transfer View")] == expected_tv
    assert wb.sheetnames[:3] == ["Cover", "BE list", "WP list"]
    assert {"Profile Constants", "Rate Table", "Staff effort"} <= set(wb.sheetnames)


@pytest.mark.parametrize(
    "affiliated_entities, headroom",
    [([0, 0, 0], 0), ([1, 0, 0], 3), ([0, 2, 1], 1), ([3, 3, 3], 5)],
)
def test_affiliated_entities_and_spare_blocks_across_combinations(tmp_path, affiliated_entities, headroom):
    result = build(shape(beneficiaries=3, affiliated_entities=affiliated_entities, headroom=headroom), tmp_path / "p.xlsx")
    wb = load_workbook(result.path)

    entities = []
    for be, aes in enumerate(affiliated_entities, start=1):
        entities += [f"BE{be}"] + [f"BE{be}-AE{a}" for a in range(1, aes + 1)]
    be_list = wb["BE list"]
    assert [be_list[f"A{4 + i}"].value for i in range(len(entities))] == entities
    roles = [be_list[f"B{4 + i}"].value for i in range(len(entities))]
    assert roles == ["Coordinator" if e == "BE1" else "Affiliated entity" if "-AE" in e else "Beneficiary" for e in entities]

    spares = [f"spare {i}" for i in range(1, headroom + 1)]
    assert [s.removeprefix("Transfer View ") for s in wb.sheetnames if s.startswith("Transfer View")] == entities + spares
    rate_rows = wb["Rate Table"].max_row - 3
    assert rate_rows == len(entities) + headroom
    effort_rows = wb["Staff effort"].max_row - 3
    assert effort_rows == 3 * (len(entities) + headroom)  # every WP x BE/AE slot, spare ones included


@pytest.mark.parametrize("tasks", [[1], [2, 1, 3], [4] * 6])
def test_a_task_list_puts_effort_at_task_grain(tmp_path, tasks):
    result = build(shape(work_packages=len(tasks), tasks=tasks, headroom=1), tmp_path / "planning.xlsx")
    wb = load_workbook(result.path)
    assert wb.sheetnames[:4] == ["Cover", "BE list", "WP list", "Task List"]

    codes = [(f"T{w}.{t}", f"WP{w}") for w, n in enumerate(tasks, start=1) for t in range(1, n + 1)]
    ws = wb["Task List"]
    assert [c.name for c in ws.tables["TaskList"].tableColumns] == ["Task nr", "WP", "Task title"]
    assert ws.tables["TaskList"].ref == f"A3:C{3 + len(codes)}"
    assert [(ws[f"A{4 + i}"].value, ws[f"B{4 + i}"].value) for i in range(len(codes))] == codes
    for i, (code, _) in enumerate(codes):
        title = result.layout.inputs[("task_title", code)]
        assert (title.sheet, title.coord) == ("Task List", f"C{4 + i}")
        assert ws[title.coord].value is None

    effort = wb["Staff effort"]
    slots = ["BE1", "BE2", "spare 1"]
    assert effort.max_row - 3 == len(codes) * len(slots)
    assert [effort[f"{c}3"].value for c in "ABC"] == ["WP", "Task", "BE/AE nr"]
    assert (effort["A4"].value, effort["B4"].value, effort["C4"].value) == ("WP1", "T1.1", "BE1")
    assert len([k for k in result.layout.inputs if k[0] == "effort"]) == len(codes) * len(slots) * len(result.profile.staff_categories)


def test_without_tasks_there_is_no_task_list_and_effort_stays_at_wp_grain(built):
    wb = load_workbook(built.path)
    assert "Task List" not in wb.sheetnames
    effort = wb["Staff effort"]
    assert [effort[f"{c}3"].value for c in "AB"] == ["WP", "BE/AE nr"]
    assert {k[1] for k in built.layout.inputs if k[0] == "effort"} == {"WP1", "WP2", "WP3"}
    assert "none" in str(next(r[1].value for r in wb["Cover"].iter_rows(max_col=2) if r[0].value == "Tasks per work package"))


def test_reference_lists_grow_through_excel_tables(tmp_path):
    result = build(shape(affiliated_entities=[1, 0]), tmp_path / "planning.xlsx")
    wb = load_workbook(result.path)
    be_tables = wb["BE list"].tables
    assert {n: be_tables[n].ref for n in be_tables} == {"BEList": "A3:F6"}
    assert [c.name for c in be_tables["BEList"].tableColumns] == [
        "BE/AE nr", "Role", "BE/AE name", "Acronym", "Country", "Funding rate",
    ]
    wp_tables = wb["WP list"].tables
    assert {n: wp_tables[n].ref for n in wp_tables} == {"WPList": "A3:B6"}

    # Every other sheet reaches the Reference Lists by structured reference, never by cell address,
    # so a row a human adds (e.g. an AE inserted under its Beneficiary) keeps every formula working.
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    assert "'BE list'!" not in c.value and "'WP list'!" not in c.value, f"{ws.title}!{c.coordinate}"
    assert "BEList[" in wb["Transfer View BE1-AE1"]["A2"].value
    assert "WPList[" in wb["Transfer View BE1"]["A5"].value


def test_a_spare_block_takes_its_code_from_a_human_input(tmp_path):
    result = build(shape(headroom=1), tmp_path / "planning.xlsx")
    code = result.layout.inputs[("slot_code", "SPARE1")]
    assert code.sheet == "Rate Table"
    wb = load_workbook(result.path)
    assert wb[code.sheet][code.coord].value is None
    assert code.ref in wb["Transfer View spare 1"]["A2"].value  # the name is looked up by that code


def _official(sheet: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # the xlsm's x14 validations and print areas are not read
        return load_workbook(OFFICIAL_BUDGET_TABLE)[sheet]


@pytest.mark.parametrize("sheet, columns", [("BE list", "ABCDEF"), ("WP list", "AB")])
def test_reference_lists_match_the_official_budget_table(built, sheet, columns):
    ours = load_workbook(built.path)[sheet]
    official = _official(sheet)

    assert {str(r) for r in ours.merged_cells.ranges} == {str(r) for r in official.merged_cells.ranges}
    assert ours.freeze_panes == official.freeze_panes
    for row in (1, 2, 3):
        assert ours.row_dimensions[row].height == official.row_dimensions[row].height, f"row {row} height"
    for col in columns:
        assert ours.column_dimensions[col].width == pytest.approx(official.column_dimensions[col].width, abs=0.01)
        for row in (2, 3):  # title and headers, verbatim
            assert ours[f"{col}{row}"].value == official[f"{col}{row}"].value, f"{sheet}!{col}{row}"
        assert ours[f"{col}4"].number_format == official[f"{col}4"].number_format, f"{sheet}!{col}4 format"
    # First data row: the code (and, on BE list, the role) in the same cells; names left blank.
    assert ours["A4"].value == official["A4"].value
    if sheet == "BE list":
        assert ours["B4"].value == official["B4"].value
        assert ours["B5"].value == "Beneficiary"
        assert [str(dv.sqref) for dv in ours.data_validations.dataValidation if dv.formula1 == '"70%,100%"']


def test_indirect_costs_reference_the_labelled_flat_rate(built):
    wb = load_workbook(built.path)
    constants = wb["Profile Constants"]
    rate_row = next(r for r in range(1, constants.max_row + 1) if constants[f"B{r}"].value == 0.25)
    assert "Indirect" in constants[f"A{rate_row}"].value

    tv = wb["Transfer View BE1"]
    e_rows = [r for r in range(1, tv.max_row + 1) if str(tv[f"A{r}"].value).startswith("E. INDIRECT")]
    assert len(e_rows) == built.shape.work_packages
    for r in e_rows:
        assert f"'Profile Constants'!$B${rate_row}" in tv[f"D{r}"].value
    a1_rows = [r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == "A.1 Employees (or equivalent)"]
    assert len(a1_rows) == built.shape.work_packages


def test_no_personal_metadata(built):
    props = load_workbook(built.path).properties
    assert not props.creator and not props.lastModifiedBy and not props.title


# --- The checks have teeth: each rule, broken on a copy, is reported. -------------------------


def _tampered(built, tmp_path: Path, edit) -> list[str]:
    copy = tmp_path / "tampered.xlsx"
    shutil.copy(built.path, copy)
    wb = load_workbook(copy)
    edit(wb)
    wb.save(copy)
    return check_structure(copy, built.shape, built.profile, built.layout)


def _first_formula(ws, prefix: str) -> str:
    return next(
        c.coordinate for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith(prefix)
    )


TAMPERING = {
    "filled Human Input": (lambda wb: wb["BE list"].__setitem__("C4", "Acme University"), "Human Input cell is not empty"),
    "renamed header": (lambda wb: wb["WP list"].__setitem__("B3", "Title"), "WP list!B3"),
    "unmerged title": (lambda wb: wb["BE list"].unmerge_cells("A2:F2"), "not merged"),
    "missing BE row": (lambda wb: wb["BE list"].__setitem__("A5", None), "BE list!A5"),
    "bare number": (
        lambda wb: wb["Transfer View BE1"].__setitem__(_first_formula(wb["Transfer View BE1"], "=SUM("), "=SUM(D5)*0.25"),
        "bare numeric literal",
    ),
    "author in properties": (lambda wb: setattr(wb.properties, "creator", "Jane Doe"), "creator"),
    "wrong profile version on Cover": (
        lambda wb: wb["Cover"].__setitem__(
            next(f"B{c.row}" for c in wb["Cover"]["A"] if c.value == "Profile version"), "0.9"
        ),
        "Profile version",
    ),
    "unlabelled constant": (lambda wb: wb["Profile Constants"].__setitem__("A4", None), "has no label"),
    "missing Transfer View": (lambda wb: wb.remove(wb["Transfer View BE2"]), "Transfer View BE2"),
    "missing spare Transfer View": (lambda wb: wb.remove(wb["Transfer View spare 3"]), "Transfer View spare 3"),
    "missing BE list Table": (lambda wb: wb["BE list"].tables.pop("BEList"), "BEList"),
    "shrunk WP list Table": (lambda wb: setattr(wb["WP list"].tables["WPList"], "ref", "A3:B5"), "WPList"),
    "cell reference into a Reference List": (
        lambda wb: wb["Rate Table"].__setitem__("B4", "='BE list'!$D$4"),
        "Rate Table!B4: refers to a Reference List cell",
    ),
    "spare code typed in": (lambda wb: wb["Rate Table"].__setitem__("A6", "BE3"), "Rate Table!A6"),
    "narrowed column": (lambda wb: setattr(wb["BE list"].column_dimensions["C"], "width", 20), "column C width"),
    "funding rate format": (lambda wb: setattr(wb["BE list"]["F4"], "number_format", "General"), "BE list!F4"),
}


@pytest.mark.parametrize("case", TAMPERING)
def test_structural_checks_catch(built, tmp_path, case):
    edit, expected = TAMPERING[case]
    problems = _tampered(built, tmp_path, edit)
    assert any(expected in p for p in problems), problems


def test_structural_checks_catch_vba(built, tmp_path):
    copy = tmp_path / "with_vba.xlsx"
    shutil.copy(built.path, copy)
    with zipfile.ZipFile(copy, "a") as z:
        z.writestr("xl/vbaProject.bin", b"")
    assert "workbook contains VBA" in check_structure(copy, built.shape, built.profile, built.layout)


def test_structural_checks_catch_a_missing_staff_effort_block(built, tmp_path):
    def relabel_last_block(wb):
        ws = wb["Staff effort"]
        row = next(r for r in range(1, ws.max_row + 1) if (ws[f"A{r}"].value, ws[f"B{r}"].value) == ("WP3", "BE2"))
        ws[f"B{row}"] = "BE1"  # the last WP now shows BE1 twice and no BE2

    problems = _tampered(built, tmp_path, relabel_last_block)
    assert "no staff effort block for WP3 x BE2" in problems, problems


def test_structural_checks_catch_an_affiliated_entity_out_of_place(tmp_path):
    result = build(shape(affiliated_entities=[1, 0]), tmp_path / "planning.xlsx")

    def demote_ae(wb):
        wb["BE list"]["B5"] = "Beneficiary"

    def drop_ae_transfer_view(wb):
        wb.remove(wb["Transfer View BE1-AE1"])

    for edit, expected in ((demote_ae, "BE list!B5"), (drop_ae_transfer_view, "Transfer View BE1-AE1")):
        problems = _tampered(result, tmp_path, edit)
        assert any(expected in p for p in problems), problems


@pytest.fixture(scope="module")
def built_with_tasks(tmp_path_factory):
    return build(shape(tasks=[2, 1, 2]), tmp_path_factory.mktemp("tasks") / "planning.xlsx")


TASK_TAMPERING = {
    "missing Task List": (lambda wb: wb.remove(wb["Task List"]), "Task List"),
    "shrunk Task List Table": (lambda wb: setattr(wb["Task List"].tables["TaskList"], "ref", "A3:C5"), "TaskList"),
    "filled task title": (lambda wb: wb["Task List"].__setitem__("C4", "Kick-off"), "Human Input cell is not empty"),
    "task under the wrong WP": (lambda wb: wb["Task List"].__setitem__("B6", "WP3"), "Task List!B6"),
    "relabelled task effort row": (
        lambda wb: wb["Staff effort"].__setitem__("B4", "T1.2"),
        "Staff effort!",
    ),
}


@pytest.mark.parametrize("case", TASK_TAMPERING)
def test_structural_checks_catch_task_list_breakage(built_with_tasks, tmp_path, case):
    edit, expected = TASK_TAMPERING[case]
    problems = _tampered(built_with_tasks, tmp_path, edit)
    assert any(expected in p for p in problems), problems


def test_structural_checks_catch_a_task_list_in_a_build_without_tasks(built, tmp_path):
    problems = _tampered(built, tmp_path, lambda wb: wb.create_sheet("Task List"))
    assert any("Task List" in p for p in problems), problems


def test_transfer_view_rows_match_the_official_budget_table(built):
    """A human copies the Transfer View row for row, so labels and positions are verbatim."""
    ours = load_workbook(built.path)["Transfer View BE1"]
    official = _official("BE tpl")
    for r in range(7, 44):  # first WP block: A. DIRECT PERSONNEL COSTS ... F. TOTAL COSTS
        assert (ours[f"A{r}"].value or None) == official[f"A{r}"].value, f"row {r}"


# --- Travel planner (ticket 08) ----------------------------------------------------------------

TRIP_INPUTS = ["BE/AE nr", "WP", "Travellers", "One-way distance (km)", "Nights", "Days", "Destination country"]
TRIP_PRICES = [
    "Travel (EUR per traveller)", "Accommodation (EUR per night)", "Subsistence (EUR per day)",
    "Cost per traveller (EUR)", "Trip cost (EUR)",
]


def test_trips_grow_through_an_excel_table_with_human_inputs_and_priced_columns(built):
    wb = load_workbook(built.path)
    ws = wb["Travel planner"]
    assert list(ws.tables) == ["Trips"]
    table = ws.tables["Trips"]
    assert [c.name for c in table.tableColumns] == TRIP_INPUTS + TRIP_PRICES
    first, last = table.ref.split(":")
    assert first == "A3" and int(last[1:]) > 4  # blank trip rows to start from

    # Inputs are empty Human Inputs; prices are calculated columns, so a row a human adds is priced too.
    trip_keys = [k for k in built.layout.inputs if k[0] == "trip"]
    assert {k[2] for k in trip_keys} == {"be", "wp", "travellers", "distance", "nights", "days", "country"}
    assert all(built.layout.inputs[k].sheet == "Travel planner" for k in trip_keys)
    for column in table.tableColumns[len(TRIP_INPUTS):]:
        assert column.calculatedColumnFormula is not None, column.name
    assert ws["H4"].value.startswith("=") and "TravelBands" in ws["H4"].value
    assert "TravelRates" in ws["I4"].value and "TravelRates" in ws["J4"].value


def test_unit_costs_come_from_the_profile_data_and_prices_are_looked_up_by_formula(built):
    from budget_engine.profiles import load_travel_unit_costs

    data = {t["id"]: t for t in load_travel_unit_costs()["tables"]}
    ws = load_workbook(built.path)["Travel unit costs"]
    assert set(ws.tables) == {"TravelBands", "TravelRates"}

    bands = data["travel_bands"]["rows"]
    rows = list(ws.iter_rows(min_row=4, max_row=3 + len(bands), max_col=3, values_only=True))
    assert rows == [(b["from_km"], b["to_km"], b["amount"]) for b in bands]
    rates = data["subsistence"]["rows"]  # calls opening from 13 May 2025
    assert ws.tables["TravelRates"].ref == f"E3:G{3 + len(rates)}"
    belgium = next(r for r in ws.iter_rows(min_row=4, min_col=5, max_col=7, values_only=True) if r[0] == "Belgium")
    assert belgium == ("Belgium", 171, 132)
    assert "C(2024)5405" in ws["A2"].value and "Annex 2a" in ws["E2"].value


def test_the_travel_summary_is_formula_based_and_feeds_the_transfer_view(built):
    wb = load_workbook(built.path)
    summary = wb["Travel summary"]
    rows = [
        (summary[f"A{r}"].value, summary[f"C{r}"].value)
        for r in range(4, summary.max_row + 1)
        if summary[f"C{r}"].value
    ]
    slots = ["BE1", "BE2"] + [None] * 3  # spare blocks show a code typed in the Rate Table
    assert len(rows) == len(slots) * 3
    assert rows[:4] == [("BE1", "WP1"), ("BE1", "WP2"), ("BE1", "WP3"), ("BE2", "WP1")]
    assert summary["D4"].value.startswith("=SUMIFS(Trips[") and summary["E4"].value.startswith("=SUMIFS(Trips[")

    tv = wb["Transfer View BE1"]
    c1 = next(r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == "C.1 Travel and subsistence")
    assert tv[f"B{c1}"].value == "='Travel summary'!$D$4"
    assert tv[f"D{c1}"].value == "='Travel summary'!$E$4"


def test_without_the_travel_planner_there_are_no_travel_sheets(tmp_path):
    result = build(shape(methods=["staff_effort"]), tmp_path / "planning.xlsx")
    names = load_workbook(result.path).sheetnames
    assert not [n for n in names if n.startswith("Travel")]


TRAVEL_TAMPERING = {
    "changed unit cost": (lambda wb: wb["Travel unit costs"].__setitem__("C5", 999), "Travel unit costs!C5"),
    "missing Trips Table": (lambda wb: wb["Travel planner"].tables.pop("Trips"), "Trips"),
    "trip price typed in": (lambda wb: wb["Travel planner"].__setitem__("H4", 365), "Travel planner!H4"),
    "relabelled summary row": (lambda wb: wb["Travel summary"].__setitem__("C5", "WP3"), "Travel summary!"),
    "missing travel sheet": (lambda wb: wb.remove(wb["Travel summary"]), "Travel summary"),
}


@pytest.mark.parametrize("case", TRAVEL_TAMPERING)
def test_structural_checks_catch_travel_planner_breakage(built, tmp_path, case):
    edit, expected = TRAVEL_TAMPERING[case]
    problems = _tampered(built, tmp_path, edit)
    assert any(expected in p for p in problems), problems


# --- Equipment depreciation (ticket 09) ---------------------------------------------------------

EQUIPMENT_INPUTS = [
    "BE/AE nr", "WP", "Cost line", "Item", "Purchase cost (EUR)", "Depreciation period (months)",
    "Usage share for the action",
]
EQUIPMENT_CALCULATED = ["Months in the project", "Share of useful life in the project", "Eligible cost (EUR)"]


def test_equipment_grows_through_an_excel_table_with_human_inputs_and_calculated_columns(built):
    ws = load_workbook(built.path)["Equipment depreciation"]
    assert list(ws.tables) == ["Equipment"]
    table = ws.tables["Equipment"]
    assert [c.name for c in table.tableColumns] == EQUIPMENT_INPUTS + EQUIPMENT_CALCULATED
    first, last = table.ref.split(":")
    assert first == "A3" and int(last[1:]) > 4  # blank item rows to start from

    keys = [k for k in built.layout.inputs if k[0] == "equipment"]
    assert {k[2] for k in keys} == {"be", "wp", "line", "item", "cost", "period", "usage"}
    assert all(built.layout.inputs[k].sheet == "Equipment depreciation" for k in keys)
    for column in table.tableColumns[len(EQUIPMENT_INPUTS):]:
        assert column.calculatedColumnFormula is not None, column.name


def test_the_eligible_share_uses_the_labelled_project_duration(built):
    wb = load_workbook(built.path)
    constants = wb["Profile Constants"]
    row = next(r for r in range(1, constants.max_row + 1) if constants[f"A{r}"].value == "Project duration (months)")
    assert constants[f"B{row}"].value == 36  # the duration_months Shape Parameter

    ws = wb["Equipment depreciation"]
    months, share, eligible = ws["H4"].value, ws["I4"].value, ws["J4"].value
    assert f"MIN('Profile Constants'!$B${row}," in months
    assert "[Months in the project]" in share and "[Depreciation period (months)]" in share
    assert all(name in eligible for name in ("[Purchase cost (EUR)]", "[Usage share for the action]"))


def test_the_equipment_summary_feeds_the_c2_lines_of_the_transfer_view(built):
    wb = load_workbook(built.path)
    summary = wb["Equipment summary"]
    rows = [
        (summary[f"A{r}"].value, summary[f"C{r}"].value, summary[f"D{r}"].value)
        for r in range(4, summary.max_row + 1)
        if summary[f"C{r}"].value
    ]
    assert len(rows) == 5 * 3 * 3  # BE/AE blocks (spare ones included) x WPs x C.2 lines
    assert rows[:4] == [
        ("BE1", "WP1", "Equipment"), ("BE1", "WP1", "Infrastructure"), ("BE1", "WP1", "Other assets"),
        ("BE1", "WP2", "Equipment"),
    ]
    assert summary["E4"].value.startswith("=COUNTIFS(Equipment[") and summary["F4"].value.startswith("=SUMIFS(Equipment[")

    tv = wb["Transfer View BE1"]
    for label, row in (("Equipment", 4), ("Infrastructure", 5), ("Other assets", 6)):
        line = next(r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == label)
        assert tv[f"B{line}"].value == f"='Equipment summary'!$E${row}"
        assert tv[f"D{line}"].value == f"='Equipment summary'!$F${row}"


def test_without_equipment_depreciation_there_are_no_equipment_sheets(tmp_path):
    result = build(shape(methods=["staff_effort"]), tmp_path / "planning.xlsx")
    names = load_workbook(result.path).sheetnames
    assert not [n for n in names if n.startswith("Equipment")]


def _duration_row(wb) -> int:
    ws = wb["Profile Constants"]
    return next(r for r in range(1, ws.max_row + 1) if ws[f"A{r}"].value == "Project duration (months)")


EQUIPMENT_TAMPERING = {
    "missing Equipment Table": (lambda wb: wb["Equipment depreciation"].tables.pop("Equipment"), "Equipment"),
    "eligible cost typed in": (lambda wb: wb["Equipment depreciation"].__setitem__("J4", 500), "Equipment depreciation!J4"),
    "duration typed into a formula": (
        lambda wb: wb["Equipment depreciation"].__setitem__("H5", "=MIN(36,F5)"), "Equipment depreciation!H5"
    ),
    "changed project duration": (
        lambda wb: wb["Profile Constants"].__setitem__(f"B{_duration_row(wb)}", 24), "project duration 24"
    ),
    "relabelled summary row": (lambda wb: wb["Equipment summary"].__setitem__("D5", "Equipment"), "Equipment summary!"),
    "missing equipment sheet": (lambda wb: wb.remove(wb["Equipment summary"]), "Equipment summary"),
}


@pytest.mark.parametrize("case", EQUIPMENT_TAMPERING)
def test_structural_checks_catch_equipment_depreciation_breakage(built, tmp_path, case):
    edit, expected = EQUIPMENT_TAMPERING[case]
    problems = _tampered(built, tmp_path, edit)
    assert any(expected in p for p in problems), problems


# --- Itemised list (ticket 10) --------------------------------------------------------------------

ITEMISED_INPUTS = ["BE/AE nr", "WP", "Cost line", "Item", "Number of items", "Cost per item (EUR)"]
ITEMISED_LINES = [
    "B. DIRECT SUBCONTRACTING COSTS", "Consumables", "Services for meetings, seminars",
    "Services for dissemination activities (including website)", "Publication fees",
    "Other (shipment, insurance, translation, etc.)",
]


def test_items_grow_through_an_excel_table_with_number_and_cost_per_item_as_human_inputs(built):
    ws = load_workbook(built.path)["Itemised list"]
    assert list(ws.tables) == ["Items"]
    table = ws.tables["Items"]
    assert [c.name for c in table.tableColumns] == ITEMISED_INPUTS + ["Total (EUR)"]
    assert table.tableColumns[-1].calculatedColumnFormula is not None
    first, last = table.ref.split(":")
    assert first == "A3" and int(last[1:]) > 4

    keys = [k for k in built.layout.inputs if k[0] == "itemised"]
    assert {k[2] for k in keys} == {"be", "wp", "line", "item", "number", "cost"}
    assert all(built.layout.inputs[k].sheet == "Itemised list" for k in keys)
    total = ws["G4"].value
    assert "[Number of items]" in total and "[Cost per item (EUR)]" in total


def test_the_cost_line_is_picked_from_the_profiles_cost_lines(built):
    ws = load_workbook(built.path)["Itemised list"]
    pick = next(dv for dv in ws.data_validations.dataValidation if "C4" in str(dv.sqref))
    assert pick.type == "list"
    first, last = pick.formula1.replace("$", "").split(":")
    column, start, end = first[0], int(first[1:]), int(last[1:])
    labels = [ws[f"{column}{r}"].value for r in range(start, end + 1)]
    assert labels[: len(ITEMISED_LINES)] == ITEMISED_LINES  # B (named after its heading), then C.3
    assert labels[-1].startswith("D.5 ") and len(labels) == len(ITEMISED_LINES) + 5


def test_the_itemised_summary_feeds_the_matching_transfer_view_lines(built):
    wb = load_workbook(built.path)
    summary = wb["Itemised list summary"]
    rows = [
        (summary[f"A{r}"].value, summary[f"C{r}"].value, summary[f"D{r}"].value)
        for r in range(4, summary.max_row + 1)
        if summary[f"C{r}"].value
    ]
    assert len(rows) == 5 * 3 * 11  # BE/AE blocks (spare ones included) x WPs x cost lines
    assert rows[:2] == [("BE1", "WP1", ITEMISED_LINES[0]), ("BE1", "WP1", "Consumables")]
    assert summary["E4"].value.startswith("=SUMIFS(Items[") and summary["F4"].value.startswith("=SUMIFS(Items[")

    tv = wb["Transfer View BE1"]
    for label, row in (("Consumables", 5), ("Publication fees", 8)):
        line = next(r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == label)
        assert tv[f"B{line}"].value == f"='Itemised list summary'!$E${row}"
        assert tv[f"D{line}"].value == f"='Itemised list summary'!$F${row}"
    subcontracting = next(r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == ITEMISED_LINES[0]) + 1
    assert tv[f"D{subcontracting}"].value == "='Itemised list summary'!$F$4"


@pytest.mark.parametrize("label", ["Fees *", "Fees?", "<Fees", "Consumables"])
def test_cost_line_labels_sumifs_would_not_match_exactly_are_refused(built, label):
    from dataclasses import replace

    from budget_engine.methods import itemised_list

    rows = tuple(replace(r, label=label) if r.id == "C3_publication" else r for r in built.profile.transfer_view_rows)
    with pytest.raises(ValueError):
        itemised_list.cost_lines(replace(built.profile, transfer_view_rows=rows))


def test_without_the_itemised_list_there_are_no_itemised_sheets(tmp_path):
    result = build(shape(methods=["staff_effort"]), tmp_path / "planning.xlsx")
    names = load_workbook(result.path).sheetnames
    assert not [n for n in names if n.startswith("Itemised")]


ITEMISED_TAMPERING = {
    "missing Items Table": (lambda wb: wb["Itemised list"].tables.pop("Items"), "Items"),
    "total typed in": (lambda wb: wb["Itemised list"].__setitem__("G4", 500), "Itemised list!G4"),
    "pick list edited": (lambda wb: wb["Itemised list"].__setitem__("I4", "Subcontracting"), "Itemised list!I4"),
    "cost line not validated": (
        lambda wb: wb["Itemised list"].data_validations.dataValidation.__setitem__(
            slice(None), [dv for dv in wb["Itemised list"].data_validations.dataValidation if dv.type != "list" or "C4" not in str(dv.sqref)]
        ),
        "not validated against the pick list",
    ),
    "relabelled summary row": (lambda wb: wb["Itemised list summary"].__setitem__("D5", "Fees"), "Itemised list summary!"),
    "missing itemised sheet": (lambda wb: wb.remove(wb["Itemised list summary"]), "Itemised list summary"),
}


@pytest.mark.parametrize("case", ITEMISED_TAMPERING)
def test_structural_checks_catch_itemised_list_breakage(built, tmp_path, case):
    edit, expected = ITEMISED_TAMPERING[case]
    problems = _tampered(built, tmp_path, edit)
    assert any(expected in p for p in problems), problems


def test_structural_checks_catch_a_pivot_table(built, tmp_path):
    copy = tmp_path / "with_pivot.xlsx"
    shutil.copy(built.path, copy)
    with zipfile.ZipFile(copy, "a") as z:
        z.writestr("xl/pivotCache/pivotCacheDefinition1.xml", b"")
    assert "workbook contains a PivotTable or pivot cache" in check_structure(copy, built.shape, built.profile, built.layout)


# --- Full Transfer View and Check Summaries (ticket 11) ----------------------------------------

LUMP_SUM = "Check - Lump sum breakdown"
PERSON_MONTHS = "Check - Person-months overview"
PER_WP = "Check - Summary per WP"
CHECK_SHEETS = [LUMP_SUM, PERSON_MONTHS, PER_WP]


@pytest.fixture(scope="module")
def built_with_aes(tmp_path_factory):
    """Two Beneficiaries, one AE under BE1, one spare block and two WPs."""
    params = shape(affiliated_entities=[1, 0], headroom=1, work_packages=2)
    return build(params, tmp_path_factory.mktemp("aes") / "planning.xlsx")


def _labels(ws, rows) -> list[object]:
    return [ws[f"A{r}"].value or None for r in rows]


def test_the_check_summaries_follow_the_transfer_views(built):
    names = load_workbook(built.path).sheetnames
    assert names[-3:] == CHECK_SHEETS
    assert names[-4] == "Transfer View spare 3"


def test_every_category_has_its_transfer_view_row_even_when_no_method_fills_it(tmp_path):
    """With only staff effort switched on, B, C and D lines keep their rows, labelled and blank."""
    result = build(shape(methods=["staff_effort"]), tmp_path / "planning.xlsx")
    tv = load_workbook(result.path)["Transfer View BE1"]
    official = _official("BE tpl")
    for r in range(7, 44):
        assert (tv[f"A{r}"].value or None) == official[f"A{r}"].value, f"row {r}"
    d2 = next(r for r in range(7, 44) if tv[f"A{r}"].value == "D.2 Internally invoiced goods and services")
    for r in [d2, d2 + 1, d2 + 2, d2 + 3, 18, 20]:  # D.2-D.5, B, C.1
        assert [tv[f"{c}{r}"].value for c in "BCD"] == [None, None, None], f"row {r}"
    assert tv["D9"].value is not None  # A.1 senior is filled by staff effort


def test_the_transfer_view_row_order_comes_from_the_profile(tmp_path, monkeypatch):
    from dataclasses import replace

    from budget_engine import shape as shape_module
    from budget_engine.profiles import LayoutRow, load_profile

    real = load_profile("he-lump-sum", "1.0")
    rows = real.transfer_view_rows
    i = next(n for n, r in enumerate(rows) if r.id == "C1")
    reordered = rows[:i] + (LayoutRow(kind="heading", label="NOT IN THE BUILDER"),) + rows[i:]
    monkeypatch.setattr(shape_module, "load_profile", lambda *_: replace(real, transfer_view_rows=reordered))

    result = build(shape(), tmp_path / "planning.xlsx")

    wb = load_workbook(result.path)
    for sheet in ("Transfer View BE1", PER_WP):
        labels = [c.value for c in wb[sheet]["A"]]
        at = labels.index("NOT IN THE BUILDER")
        assert labels[at + 1] == "C.1 Travel and subsistence", sheet


@pytest.mark.parametrize(
    "sheet, title",
    [(LUMP_SUM, "ESTIMATED BREAKDOWN OF THE LUMP SUM"), (PERSON_MONTHS, "TOTAL PERSON-MONTHS")],
)
def test_lump_sum_and_person_month_grids_have_a_row_per_block_and_a_column_per_wp(built_with_aes, sheet, title):
    ws = load_workbook(built_with_aes.path)[sheet]
    assert ws["A1"].value == title
    assert ws["A2"].value == "BENEFICIARIES \\ WORK PACKAGES"
    assert '"WP1 "' in ws["B2"].value and '"WP2 "' in ws["C2"].value
    assert [ws["D2"].value, ws["E2"].value] == ["Total", "Pct %"]
    labels = _labels(ws, range(3, 9))
    for label, code in zip(labels, ["BE1", "BE1-AE1", "BE2"]):
        assert str(label).startswith(f'="{code}: "'), label
    assert "'Rate Table'!" in str(labels[3])  # the spare block shows the code typed into the Rate Table
    assert labels[4:] == ["Total: ", "Percentage: "]
    figures = [f"{c}{r}" for r in range(3, 8) for c in "BCDE"] + ["B8", "C8", "D8"]
    for coord in figures:
        assert str(ws[coord].value).startswith("="), f"{sheet}!{coord} is not a formula"


def test_the_lump_sum_applies_each_blocks_funding_rate_to_its_total_costs(built_with_aes):
    wb = load_workbook(built_with_aes.path)
    ws = wb[LUMP_SUM]
    assert ws["F2"].value == "Funding rate"
    assert "BEList[[Funding rate]]" in ws["F3"].value
    tv = wb["Transfer View BE1-AE1"]
    f_row = next(r for r in range(1, tv.max_row + 1) if tv[f"A{r}"].value == "F. TOTAL COSTS (A+B+C+D+E)")
    assert f"'Transfer View BE1-AE1'!$D${f_row}" in ws["B4"].value and "$F4" in ws["B4"].value


def test_person_months_add_up_the_personnel_items(built_with_aes):
    ws = load_workbook(built_with_aes.path)[PERSON_MONTHS]
    assert ws["B3"].value.count("'Transfer View BE1'!$B$") == 8  # A.1 (five lines), A.2, A.3, A.4


def test_the_summary_per_wp_mirrors_the_official_rows_for_each_wp_and_all_wps(built_with_aes):
    ws = load_workbook(built_with_aes.path)[PER_WP]
    official = _official("BE tpl")
    assert ws["A1"].value == "SUM OF ALL BENEFICIARIES (including AFFILIATED ENTITIES) FOR ALL THE WORK PACKAGES"
    assert [ws["B2"].value, ws["E2"].value, ws["H2"].value] == [
        "ALL BENEFICIARIES \n(without affiliated entities)", "ALL AFFILIATED ENTITIES",
        "ALL BENEFICIARIES \n(with affiliated entities)",
    ]
    assert [ws[f"{c}3"].value for c in "BCDEFGHIJ"] == [
        "ITEMS", "COST PER ITEM", "BE TOTAL COSTS", "ITEMS", "COST PER ITEM", "AE TOTAL COSTS",
        "ITEMS\n(TOTAL)", "AVERAGE COST PER ITEM", "TOTAL COSTS",
    ]
    for r in range(7, 44):
        assert (ws[f"A{r}"].value or None) == official[f"A{r}"].value, f"row {r}"
    titles = [
        c.value for c in ws["A"]
        if isinstance(c.value, str) and c.value.startswith(('="COSTS WORK PACKAGE', "SUM OF ALL WORK"))
    ]
    assert len(titles) == 3 and titles[-1] == "SUM OF ALL WORK PACKAGES FOR ALL BENEFICIARIES"


def test_the_summary_per_wp_splits_beneficiaries_from_affiliated_entities(built_with_aes):
    ws = load_workbook(built_with_aes.path)[PER_WP]
    be_items, ae_items = ws["B9"].value, ws["E9"].value  # A.1 senior scientists, WP1
    assert "'Transfer View BE1'!" in be_items and "'Transfer View BE2'!" in be_items
    assert "'Transfer View BE1-AE1'!" in ae_items and "'Transfer View BE1-AE1'!" not in be_items
    # The spare block counts as an AE or a Beneficiary by the code typed in for it.
    assert "'Transfer View spare 1'!" in be_items and "'Transfer View spare 1'!" in ae_items
    assert ws["L3"].value == "Spare block" and ws["L4"].value == "spare 1"
    assert '"-AE"' in ws["M4"].value


def test_indirect_costs_in_the_summary_per_wp_follow_the_profile_rule(built_with_aes):
    wb = load_workbook(built_with_aes.path)
    constants = wb["Profile Constants"]
    rate_row = next(r for r in range(1, constants.max_row + 1) if constants[f"B{r}"].value == 0.25)
    ws = wb[PER_WP]
    e_rows = [r for r in range(1, ws.max_row + 1) if str(ws[f"A{r}"].value).startswith("E. INDIRECT")]
    assert len(e_rows) == built_with_aes.shape.work_packages + 1
    for r in e_rows:
        for col in "DGJ":
            assert f"'Profile Constants'!$B${rate_row}" in ws[f"{col}{r}"].value, f"{col}{r}"


SUMMARY_TAMPERING = {
    "missing summary sheet": (lambda wb: wb.remove(wb[PERSON_MONTHS]), PERSON_MONTHS),
    "lump sum typed in": (lambda wb: wb[LUMP_SUM].__setitem__("B3", 10000), f"{LUMP_SUM}!B3"),
    "share typed in": (lambda wb: wb[PERSON_MONTHS].__setitem__("F3", 0.5), f"{PERSON_MONTHS}!F3"),
    "relabelled summary per WP row": (lambda wb: wb[PER_WP].__setitem__("A9", "Seniors"), f"{PER_WP}!A9"),
    "summary per WP figure typed in": (lambda wb: wb[PER_WP].__setitem__("D9", 5000), f"{PER_WP}!D9"),
    "missing block row": (lambda wb: wb[LUMP_SUM].__setitem__("A4", None), f"{LUMP_SUM}!A4"),
}


@pytest.mark.parametrize("case", SUMMARY_TAMPERING)
def test_structural_checks_catch_check_summary_breakage(built, tmp_path, case):
    edit, expected = SUMMARY_TAMPERING[case]
    problems = _tampered(built, tmp_path, edit)
    assert any(expected in p for p in problems), problems

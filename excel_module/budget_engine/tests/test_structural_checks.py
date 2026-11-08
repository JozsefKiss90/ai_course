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
    assert time.perf_counter() - started < 5, "structural checks must be fast enough for every build"

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


def test_structural_checks_catch_a_pivot_table(built, tmp_path):
    copy = tmp_path / "with_pivot.xlsx"
    shutil.copy(built.path, copy)
    with zipfile.ZipFile(copy, "a") as z:
        z.writestr("xl/pivotCache/pivotCacheDefinition1.xml", b"")
    assert "workbook contains a PivotTable or pivot cache" in check_structure(copy, built.shape, built.profile, built.layout)

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
    expected_tv = [f"Transfer View BE{i}" for i in range(1, beneficiaries + 1)]
    assert [s for s in wb.sheetnames if s.startswith("Transfer View")] == expected_tv
    assert wb.sheetnames[:3] == ["Cover", "BE list", "WP list"]
    assert {"Profile Constants", "Rate Table", "Staff effort"} <= set(wb.sheetnames)


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
        ws[f"B{ws.max_row}"] = "BE1"  # the last WP now shows BE1 twice and no BE2

    problems = _tampered(built, tmp_path, relabel_last_block)
    assert "no staff effort block for WP3 x BE2" in problems, problems


def test_transfer_view_rows_match_the_official_budget_table(built):
    """A human copies the Transfer View row for row, so labels and positions are verbatim."""
    ours = load_workbook(built.path)["Transfer View BE1"]
    official = _official("BE tpl")
    for r in range(7, 44):  # first WP block: A. DIRECT PERSONNEL COSTS ... F. TOTAL COSTS
        assert (ours[f"A{r}"].value or None) == official[f"A{r}"].value, f"row {r}"

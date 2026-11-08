"""The Handover Package and its fill-in guide.

Every package comes from ``deliver``. Most tests stand in for the Synthetic Check (Excel) with a
passing or failing report, so packaging is tested on its own; the test marked ``excel`` runs the
real check end to end.
"""

import importlib
from dataclasses import replace
from pathlib import Path

import pytest

from budget_engine import BuildError, SyntheticCheckFailed, SyntheticCheckReport, build, check_structure, deliver, fill_in_guide
from budget_engine.handover import GUIDE, REPORT, WORKBOOK
from budget_engine.verify.synthetic import Mismatch

HE = {"id": "he-lump-sum", "version": "1.0"}
# The module, not the build function the package exports under the same name.
BUILD_MODULE = importlib.import_module("budget_engine.build")


def shape(**overrides: object) -> dict[str, object]:
    params: dict[str, object] = {"profile": HE, "beneficiaries": 2, "work_packages": 3, "duration_months": 36}
    params.update(overrides)
    return params


def _report(result, mismatches=()) -> SyntheticCheckReport:
    return SyntheticCheckReport(
        workbook=result.path.name,
        scenario="stand-in",
        scenario_provenance="Stand-in for the Synthetic Check in a test without Excel.",
        human_owned=False,
        figures=("BE1 WP1 A1_senior total",),
        table_rows_added=(),
        mismatches=tuple(mismatches),
        copy_path=Path("unused"),
        copy_deleted=True,
    )


@pytest.fixture
def check_passes(monkeypatch):
    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", lambda result: _report(result))


@pytest.fixture
def check_fails(monkeypatch):
    mismatch = Mismatch("BE1 WP1 A1_senior total", "'Transfer View BE1'!D9", 1100.0, 2200.0, 1100.0)
    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", lambda result: _report(result, [mismatch]))


def test_a_passed_check_delivers_workbook_report_and_guide(tmp_path, check_passes):
    package = deliver(shape(), tmp_path / "package")

    assert sorted(p.name for p in package.directory.iterdir()) == sorted([WORKBOOK, REPORT, GUIDE])
    assert package.workbook == package.directory / WORKBOOK
    assert "Result: **PASS**" in package.report.read_text(encoding="utf-8")
    assert f"`{WORKBOOK}`" in package.guide.read_text(encoding="utf-8")
    built = package.build
    assert check_structure(package.workbook, built.shape, built.profile, built.layout) == []


def test_a_failing_check_delivers_only_the_failure_report(tmp_path, check_fails):
    out = tmp_path / "package"
    with pytest.raises(SyntheticCheckFailed):
        deliver(shape(), out)

    assert [p.name for p in out.iterdir()] == [REPORT]
    report = (out / REPORT).read_text(encoding="utf-8")
    assert "Result: **FAIL**" in report and "'Transfer View BE1'!D9" in report


def test_a_workbook_changed_during_the_check_is_not_delivered(tmp_path, monkeypatch):
    def check_that_writes_into_the_deliverable(result):
        with result.path.open("ab") as f:
            f.write(b"\0")
        return _report(result)

    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", check_that_writes_into_the_deliverable)
    out = tmp_path / "package"
    with pytest.raises(BuildError, match="changed during the Synthetic Check"):
        deliver(shape(), out)
    assert list(out.iterdir()) == []


def test_a_package_goes_into_a_new_or_empty_directory(tmp_path, check_passes):
    out = tmp_path / "package"
    out.mkdir()
    (out / "fill-in-guide.md").write_text("from an earlier build", encoding="utf-8")

    with pytest.raises(ValueError, match="new or empty directory"):
        deliver(shape(), out)


def _sections(guide: str) -> list[str]:
    part = guide.split("## Sheet by sheet", 1)[1].split("\n## ", 1)[0]
    return [line.removeprefix("### ") for line in part.splitlines() if line.startswith("### ")]


def test_the_guide_has_a_section_per_sheet_in_workbook_order(tmp_path):
    result = build(
        shape(affiliated_entities=[1, 0], tasks=[2, 1, 1], methods=["staff_effort", "travel_planner", "equipment_depreciation", "itemised_list"]),
        tmp_path / "planning.xlsx",
    )
    guide = fill_in_guide(result)

    expected = []
    for sheet in result.sheets:
        group = "Transfer View sheets" if sheet.startswith("Transfer View ") else "Check sheets" if sheet.startswith("Check - ") else sheet
        if group not in expected:
            expected.append(group)
    assert _sections(guide) == expected
    for step in result.fill_in_order:
        assert step in guide


def test_the_guide_gives_what_to_enter_unit_and_source_from_the_profile(tmp_path):
    result = build(shape(), tmp_path / "planning.xlsx")
    guide = fill_in_guide(result)
    profile = result.profile

    for section in guide.split("\n### ")[1:]:
        assert "**What to enter:**" in section and "**Unit:**" in section and "**Source:**" in section, section
    rate_table = guide.split("### Rate Table", 1)[1].split("###", 1)[0]
    assert profile.rate_unit in rate_table
    assert all(c.label in rate_table for c in profile.staff_categories)
    assert profile.effort_unit in guide.split("### Staff effort", 1)[1].split("###", 1)[0]
    assert "C(2024) 5405" in guide or "C(2024)5405" in guide  # the travel unit-cost decision
    for t in profile.plausibility:
        assert t.label in guide


def test_the_guide_explains_the_transfer_into_the_submission_budget(tmp_path):
    result = build(shape(), tmp_path / "planning.xlsx")
    guide = fill_in_guide(result)

    transfer = guide.split(f"## Transferring the Transfer Views into {result.profile.submission_budget}", 1)[1]
    assert [line.split(". ", 1)[1] for line in transfer.strip().splitlines()] == list(result.profile.transfer_steps)
    assert "ITEMS and COST PER ITEM" in transfer


def test_a_switched_off_method_or_task_list_has_no_section(tmp_path):
    result = build(shape(methods=["staff_effort"]), tmp_path / "planning.xlsx")
    sections = _sections(fill_in_guide(result))

    assert "Staff effort" in sections
    assert not {"Task List", "Travel planner", "Travel summary", "Equipment depreciation", "Itemised list"} & set(sections)
    assert "Effort per work package" in fill_in_guide(result)


def test_a_sheet_without_a_guide_section_fails_the_guide(tmp_path):
    result = build(shape(), tmp_path / "planning.xlsx")
    with pytest.raises(KeyError, match="Mystery"):
        fill_in_guide(replace(result, sheets=(*result.sheets, "Mystery")))


@pytest.mark.excel
def test_a_real_synthetic_check_delivers_the_package(tmp_path):
    pytest.importorskip("win32com.client", reason="the Synthetic Check needs Excel via COM (Windows)")
    package = deliver(shape(affiliated_entities=[1, 0], tasks=[2, 1, 1]), tmp_path / "package")

    assert sorted(p.name for p in package.directory.iterdir()) == sorted([WORKBOOK, REPORT, GUIDE])
    report = package.report.read_text(encoding="utf-8")
    assert "Result: **PASS**" in report and "Disposable copy deleted: yes" in report
    built = package.build
    assert check_structure(package.workbook, built.shape, built.profile, built.layout) == []

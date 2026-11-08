"""Seam 1: build + Synthetic Check, recalculated in real Excel via COM.

Every workbook comes from the build entry point. The check fills a disposable copy with the
provisional scenario, recalculates it in Excel and compares the Transfer View with the reference
model. These tests need Microsoft Excel and are marked ``excel``.
"""

import hashlib
from pathlib import Path

import pytest

from budget_engine import SyntheticCheckFailed, build, run_synthetic_check

pytestmark = pytest.mark.excel
pytest.importorskip("win32com.client", reason="the Synthetic Check needs Excel via COM (Windows)")

HE = {"id": "he-lump-sum", "version": "1.0"}


def shape(**overrides: object) -> dict[str, object]:
    params: dict[str, object] = {"profile": HE, "beneficiaries": 2, "work_packages": 3, "duration_months": 36}
    params.update(overrides)
    return params


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_a_clean_build_passes_and_the_deliverable_is_untouched(tmp_path):
    result = build(shape(), tmp_path / "deliverable" / "planning.xlsx")
    before = digest(result.path)

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    assert report.figures_compared > 0
    assert report.mismatches == ()
    assert digest(result.path) == before
    assert report.copy_path is not None
    assert result.path.parent not in report.copy_path.parents
    assert not report.copy_path.exists() and report.copy_deleted


def test_a_broken_formula_in_the_generator_fails_with_a_useful_report(tmp_path, monkeypatch):
    from budget_engine.sheets import transfer_view

    # Sabotage: every Transfer View cost line doubles its first source instead of summing them.
    monkeypatch.setattr(transfer_view, "_sum", lambda refs: f"={refs[0]}+{refs[0]}")
    result = build(shape(beneficiaries=1, work_packages=1), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    by_figure = {m.figure: m for m in report.mismatches}
    # Rate for BE1 senior is 1,100 and effort for WP1/BE1/senior is 0.5 x ((3+2+1) % 4) = 1.0.
    senior = by_figure["BE1 WP1 A1_senior total"]
    assert senior.location == "'Transfer View BE1'!D9"
    assert (senior.expected, senior.actual, senior.difference) == (1100.0, 2200.0, 1100.0)
    assert "BE1 WP1 F total" in by_figure  # the error carries through to the grand total
    assert "BE1 WP1 A1_senior avg" not in by_figure  # average per item is unaffected by doubling both
    markdown = report.to_markdown()
    assert "FAIL" in markdown and "'Transfer View BE1'!D9" in markdown and "1,100.00" in markdown
    assert report.copy_path is not None and not report.copy_path.exists()
    assert report.copy_deleted


def test_a_failed_check_stops_delivery(tmp_path, monkeypatch):
    from budget_engine.sheets import transfer_view

    monkeypatch.setattr(transfer_view, "_sum", lambda refs: f"={refs[0]}+{refs[0]}")
    out = tmp_path / "planning.xlsx"

    with pytest.raises(SyntheticCheckFailed) as failed:
        build(shape(), out, synthetic_check=True)

    assert not out.exists()
    assert failed.value.report.mismatches
    assert "'Transfer View BE1'!D9" in str(failed.value)


@pytest.mark.parametrize("beneficiaries, work_packages", [(1, 1), (4, 2)])
def test_a_build_that_passes_is_delivered_with_its_report(tmp_path, beneficiaries, work_packages):
    out = tmp_path / "planning.xlsx"

    result = build(shape(beneficiaries=beneficiaries, work_packages=work_packages), out, synthetic_check=True)

    assert out.exists()
    assert result.synthetic_check is not None and result.synthetic_check.passed
    markdown = result.synthetic_check.to_markdown()
    assert "PASS" in markdown and "PROVISIONAL, not human-owned" in markdown


def test_a_late_partner_in_a_spare_block_and_a_new_table_row_flow_through(tmp_path):
    """The scenario inserts a late AE under BE1 in the BE list Table and fills the first spare block for it."""
    result = build(shape(affiliated_entities=[1, 0], headroom=2), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    assert "BEList: BE1-AE2 under BE1" in report.table_rows_added
    figures = set(report.figures)
    assert "SPARE1 name" in figures  # the late AE's name, typed into the new Table row
    assert "SPARE1 WP1 A1_senior total" in figures and "SPARE2 WP3 F total" in figures
    assert "BE1-AE1 WP2 F total" in figures


def test_task_grain_effort_rolls_up_to_the_work_package(tmp_path):
    result = build(shape(tasks=[2, 1, 3], affiliated_entities=[1, 0], headroom=1), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    figures = set(report.figures)
    assert "BE1 WP1 A1_senior total" in figures and "SPARE1 WP3 F total" in figures
    assert not any(" T" in f for f in figures)  # the Transfer View stays at WP grain


def test_a_task_left_out_of_the_roll_up_fails_the_check(tmp_path, monkeypatch):
    from budget_engine.sheets import transfer_view

    real = transfer_view._sum
    # Sabotage: each Transfer View cost line drops its last task row.
    monkeypatch.setattr(transfer_view, "_sum", lambda refs: real(refs[:-1]) if len(refs) > 1 else real(refs))
    result = build(shape(beneficiaries=1, work_packages=1, tasks=[2], headroom=0), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    assert "BE1 WP1 F total" in {m.figure for m in report.mismatches}


def test_a_spare_block_that_does_not_calculate_fails_the_check(tmp_path, monkeypatch):
    from budget_engine.sheets import transfer_view

    real = transfer_view._sum
    # Sabotage: the spare block's Transfer View cost lines are wired to nothing.
    monkeypatch.setattr(transfer_view, "_sum", lambda refs: "=0" if _spare(refs) else real(refs))
    result = build(shape(beneficiaries=1, work_packages=1, headroom=1), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    assert {m.figure.split()[0] for m in report.mismatches} == {"SPARE1"}


def _spare(refs: list[str]) -> bool:
    """True for the refs of the last Staff effort row, which with one BE and headroom 1 is the spare block."""
    return all(r.startswith("'Staff effort'!") and r.endswith("$5") for r in refs)


def test_the_copy_is_deleted_when_the_check_breaks_down(tmp_path, monkeypatch):
    from budget_engine.verify import synthetic

    seen: list[Path] = []

    def excel_crashes(copy, fill, cells, table_rows=()):
        seen.append(copy)
        assert copy.exists()
        raise RuntimeError("Excel went away")

    monkeypatch.setattr(synthetic, "recalculate_and_read", excel_crashes)
    out = tmp_path / "planning.xlsx"

    with pytest.raises(RuntimeError, match="Excel went away"):
        build(shape(), out, synthetic_check=True)

    assert seen and not seen[0].parent.exists()
    assert not out.exists()


def test_trips_across_several_partners_and_work_packages_are_priced_and_summed(tmp_path):
    """The scenario enters trips for every BE/AE, a late AE in a spare block and several WPs, then
    appends a trip row to the Trips Table as a human would; its prices must fill in by themselves."""
    result = build(shape(affiliated_entities=[1, 0], headroom=2), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    assert any(r.startswith("Trips: ") for r in report.table_rows_added)
    c1 = {f for f in report.figures if " C1 " in f}
    for block in ("BE1", "BE1-AE1", "BE2", "SPARE1"):
        assert {f"{block} WP{n} C1 total" for n in (1, 2, 3)} <= c1, block


def test_a_travel_summary_that_ignores_the_work_package_fails_the_check(tmp_path, monkeypatch):
    from budget_engine.methods import travel_planner

    real = travel_planner._sumifs
    # Sabotage: every summary row adds up the trips of its BE/AE in all work packages.
    monkeypatch.setattr(travel_planner, "_sumifs", lambda column, code, wp: _without_wp(real(column, code, wp)))
    result = build(shape(beneficiaries=2, work_packages=2, headroom=0), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    assert any(m.figure.endswith("C1 total") for m in report.mismatches)


def _without_wp(sumifs: str) -> str:
    """Drop the last criteria pair (the WP) from a SUMIFS formula."""
    return sumifs.rsplit(",", 2)[0] + ")"


def test_equipment_depreciated_over_longer_and_shorter_periods_than_the_project(tmp_path):
    """The scenario enters items whose depreciation period is longer than, shorter than and equal to
    the project, over the C.2 lines and several BE/AEs, then appends an item to the Equipment Table."""
    result = build(shape(affiliated_entities=[1, 0], headroom=2, duration_months=24), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    assert any(r.startswith("Equipment: ") for r in report.table_rows_added)
    figures = set(report.figures)
    for line in ("C2_equipment", "C2_infrastructure", "C2_other_assets"):
        assert f"BE1 WP1 {line} total" in figures and f"SPARE1 WP3 {line} items" in figures


def test_equipment_costed_in_full_beyond_the_project_fails_the_check(tmp_path, monkeypatch):
    from budget_engine.methods import equipment_depreciation

    real = equipment_depreciation.calculated_formulas

    def uncapped(duration: str) -> dict[str, str]:
        # Sabotage: the months in the project ignore the project duration.
        period = "Equipment[[#This Row],[Depreciation period (months)]]"
        return {**real(duration), equipment_depreciation.MONTHS: f"IF({period}>0,{period},0)"}

    monkeypatch.setattr(equipment_depreciation, "calculated_formulas", uncapped)
    result = build(shape(beneficiaries=1, work_packages=1, headroom=0), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    assert any(" C2_" in m.figure and m.figure.endswith("total") for m in report.mismatches)


def test_items_spread_across_several_cost_lines(tmp_path):
    """The scenario enters items over several cost lines and BE/AEs, two of them on the same line,
    then appends an item to the Items Table."""
    result = build(shape(affiliated_entities=[1, 0], headroom=2), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert report.passed, report.to_markdown()
    assert any(r.startswith("Items: ") for r in report.table_rows_added)
    figures = set(report.figures)
    for line in ("B", "C3_consumables", "C3_other", "D1", "D5"):
        assert f"BE1 WP1 {line} total" in figures and f"SPARE1 WP3 {line} items" in figures


def test_an_itemised_total_that_ignores_the_number_of_items_fails_the_check(tmp_path, monkeypatch):
    from budget_engine.methods import itemised_list

    # Sabotage: the total is the cost per item alone.
    monkeypatch.setattr(itemised_list, "total_formula", lambda: "Items[[#This Row],[Cost per item (EUR)]]")
    result = build(shape(beneficiaries=1, work_packages=1, headroom=0), tmp_path / "planning.xlsx")

    report = run_synthetic_check(result)

    assert not report.passed
    assert any(m.figure.endswith("total") for m in report.mismatches)

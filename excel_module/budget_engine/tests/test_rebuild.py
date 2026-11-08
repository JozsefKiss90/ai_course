"""The rebuild flow: old + new Shape Parameters -> a fresh Handover Package plus a re-paste guide.

A rebuild never sees the old workbook (ADR-0001). The re-paste guide comes from comparing the
input layouts the two sets of Shape Parameters produce, so the tests check it the same way a human
would use it: fill every Human Input of a blank old workbook with a marker, carry out the guide's
block copies, and see that every marker lands on the same Human Input in the new workbook.
"""

import json
import shutil
from collections import defaultdict

import pytest
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter, range_boundaries

from budget_engine import ShapeError, build, check_structure, rebuild, repaste_plan
from budget_engine.handover import GUIDE, REPASTE_GUIDE, REPORT, WORKBOOK
from budget_engine.layout import Cell
from budget_engine.repaste import row_owner
from test_handover import check_passes, shape  # noqa: F401 (fixture)

# Pairs of (old, new) Shape Parameters that reshape the consortium in different ways.
RESHAPES = {
    "a Beneficiary more": (shape(), shape(beneficiaries=3)),
    "a Beneficiary fewer": (shape(beneficiaries=3), shape()),
    "an AE under the first Beneficiary": (shape(affiliated_entities=[0, 1]), shape(affiliated_entities=[1, 1])),
    "a work package more": (shape(), shape(work_packages=4)),
    "a work package fewer": (shape(work_packages=4), shape()),
    "more headroom": (shape(headroom=1), shape(headroom=4)),
    "Task List switched on": (shape(), shape(tasks=[2, 0, 1])),
    "tasks added": (shape(tasks=[2, 0, 1]), shape(tasks=[3, 1, 1])),
    "travel switched off": (shape(), shape(methods=["staff_effort"])),
    "everything at once": (
        shape(affiliated_entities=[1, 0], tasks=[1, 2, 1], methods=["travel_planner"], headroom=2),
        shape(beneficiaries=4, affiliated_entities=[0, 2, 0, 1], work_packages=5, tasks=[1, 2, 0, 1, 3],
              methods=["travel_planner", "equipment_depreciation", "itemised_list"], headroom=3),
    ),
}


def _cells(sheet: str, area: str) -> list[Cell]:
    min_col, min_row, max_col, max_row = range_boundaries(area)
    return [
        Cell(sheet, f"{get_column_letter(c)}{r}")
        for r in range(min_row, max_row + 1)
        for c in range(min_col, max_col + 1)
    ]


def _paste(plan) -> dict[Cell, tuple[str, ...]]:
    """Fill every old Human Input with its own key, then carry out the plan's block copies."""
    old_values = {cell: key for key, cell in plan.old_layout.inputs.items()}
    pasted: dict[Cell, tuple[str, ...]] = {}
    for copy in plan.copies:
        sources, targets = _cells(copy.sheet, copy.old_range), _cells(copy.sheet, copy.new_range)
        assert len(sources) == len(targets), copy
        for source, target in zip(sources, targets):
            assert source in old_values, f"{copy}: {source} is no Human Input of the old workbook"
            assert target not in pasted, f"{copy}: {target} is pasted twice"
            pasted[target] = old_values[source]
    return pasted


@pytest.mark.parametrize("old, new", RESHAPES.values(), ids=RESHAPES.keys())
def test_every_copied_input_lands_on_the_same_input_of_the_new_workbook(old, new):
    plan = repaste_plan(old, new)
    pasted = _paste(plan)

    new_inputs = plan.new_layout.inputs
    new_cells = {cell: key for key, cell in new_inputs.items()}
    for cell, key in pasted.items():
        assert new_cells.get(cell) == key, f"old {key} pasted onto {cell}, which holds {new_cells.get(cell)}"
    # Nothing that has a counterpart is left behind.
    assert {k for k in plan.old_layout.inputs if k in new_inputs} == set(pasted.values())


@pytest.mark.parametrize("old, new", RESHAPES.values(), ids=RESHAPES.keys())
def test_inputs_without_a_counterpart_are_listed_as_dropped_or_new(old, new):
    plan = repaste_plan(old, new)

    old_inputs, new_inputs = plan.old_layout.inputs, plan.new_layout.inputs
    dropped = {cell for block in plan.dropped for cell in _cells(block.sheet, block.range)}
    fresh = {cell for block in plan.new for cell in _cells(block.sheet, block.range)}
    assert dropped == {cell for key, cell in old_inputs.items() if key not in new_inputs}
    assert fresh == {cell for key, cell in new_inputs.items() if key not in old_inputs}


def _row_layouts(layout) -> dict[tuple[str, tuple[str, ...]], tuple[tuple[str, int], ...]]:
    """Per (sheet, row owner): each Human Input's key kind and field with its column offset in the row."""
    rows: dict[tuple[str, int], list[tuple[tuple[str, ...], Cell]]] = defaultdict(list)
    for key, cell in layout.inputs.items():
        rows[(cell.sheet, cell.row)].append((key, cell))
    layouts = {}
    for (sheet, _), entries in rows.items():
        first = min(column_index_from_string(c.column) for _, c in entries)
        owners = {row_owner(key) for key, _ in entries}
        assert len(owners) == 1, f"{sheet}: one row holds inputs of {owners}"
        fields = sorted(
            (f"{key[0]}:{key[-1]}" if len(key) > 2 else key[0], column_index_from_string(c.column) - first)
            for key, c in entries
        )
        layouts[(sheet, owners.pop())] = tuple(fields)
    return layouts


@pytest.mark.parametrize("old, new", RESHAPES.values(), ids=RESHAPES.keys())
def test_input_block_layouts_are_identical_across_builds_under_one_profile_version(tmp_path, old, new):
    old_built = build(old, tmp_path / "old.xlsx")
    new_built = build(new, tmp_path / "new.xlsx")

    old_rows, new_rows = _row_layouts(old_built.layout), _row_layouts(new_built.layout)
    common = old_rows.keys() & new_rows.keys()
    assert common, "the two builds share no input rows"
    for row in common:
        assert old_rows[row] == new_rows[row], row


def test_unchanged_shape_maps_every_block_onto_itself():
    plan = repaste_plan(shape(tasks=[1, 1, 2]), shape(tasks=[1, 1, 2]))

    assert plan.copies and not plan.dropped and not plan.new
    assert all(c.old_range == c.new_range for c in plan.copies)


def test_a_beneficiary_more_moves_the_spare_blocks_down():
    plan = repaste_plan(shape(), shape(beneficiaries=3))

    be_list = [c for c in plan.copies if c.sheet == "BE list"]
    assert [(c.label, c.old_range, c.new_range) for c in be_list] == [("BE1 - BE2", "C4:F5", "C4:F5")]
    assert [(b.sheet, b.label) for b in plan.new if b.sheet == "BE list"] == [("BE list", "BE3")]
    rate_rates = [c for c in plan.copies if c.sheet == "Rate Table" and c.label.startswith("spare")]
    assert [(c.label, c.old_range, c.new_range) for c in rate_rates] == [
        ("spare 1 - spare 3", "A6:A8", "A7:A9"),
        ("spare 1 - spare 3", "C6:J8", "C7:J9"),
    ]


def test_switching_on_the_task_list_drops_work_package_effort_and_says_so():
    plan = repaste_plan(shape(), shape(tasks=[2, 0, 1]))

    dropped = {(b.sheet, b.label) for b in plan.dropped}
    assert ("Staff effort", "WP1: BE1 - spare 3") in dropped
    assert ("Staff effort", "WP2: BE1 - spare 3") not in dropped  # WP2 has no tasks: still at WP grain
    assert ("Task List", "T1.1 - T3.1") in {(b.sheet, b.label) for b in plan.new}
    assert "effort per work package" in plan.to_markdown() and "per task" in plan.to_markdown()


def test_a_switched_off_method_drops_its_sheet():
    plan = repaste_plan(shape(), shape(methods=["staff_effort"]))

    assert "Travel planner" in {b.sheet for b in plan.dropped}
    assert "Travel planner" not in {c.sheet for c in plan.copies}


def test_the_guide_lists_changes_copies_and_what_has_no_place():
    text = repaste_plan(shape(beneficiaries=3, work_packages=4), shape(work_packages=3)).to_markdown()

    assert text.startswith("# Re-paste guide")
    assert "| Beneficiaries | 3 | 2 |" in text
    assert "| Work packages | 4 | 3 |" in text
    assert "Paste Special > Values" in text
    assert "| BE1 - BE2 | C4:F5 | C4:F5 |" in text
    assert "BE3" in text and "WP4" in text
    assert "not the last one" in text  # BE and WP numbers map by position


def test_the_old_profile_version_is_kept_and_a_different_one_refused():
    plan = repaste_plan(shape(), {k: v for k, v in shape(beneficiaries=3).items() if k != "profile"})
    assert plan.new_shape.profile_version == "1.0"

    with pytest.raises(ShapeError, match="new Shape Parameters"):
        repaste_plan(shape(), shape(profile={"id": "he-lump-sum", "version": "9.9"}))


def test_invalid_old_or_new_shape_parameters_are_refused_and_named():
    with pytest.raises(ShapeError, match="old Shape Parameters: not a Shape Parameter: acronym"):
        repaste_plan(shape(acronym="ACME"), shape())
    with pytest.raises(ShapeError, match="new Shape Parameters: beneficiaries"):
        repaste_plan(shape(), shape(beneficiaries=0))


@pytest.fixture
def newer_profile_version(tmp_path, monkeypatch):
    """A profiles data directory where he-lump-sum 1.1 exists beside 1.0."""
    import budget_engine.profiles as profiles

    data = tmp_path / "profile-data"
    shutil.copytree(profiles.DATA_DIR, data)
    newer = json.loads((data / "he-lump-sum" / "1.0.json").read_text(encoding="utf-8"))
    newer["version"] = "1.1"
    (data / "he-lump-sum" / "1.1.json").write_text(json.dumps(newer), encoding="utf-8")
    monkeypatch.setattr(profiles, "DATA_DIR", data)
    assert ("he-lump-sum", "1.1") in profiles.available_profiles()


def test_a_rebuild_delivers_the_package_with_the_repaste_guide(tmp_path, check_passes):
    package = rebuild(shape(), shape(beneficiaries=3), tmp_path / "package")

    assert sorted(p.name for p in package.directory.iterdir()) == sorted([WORKBOOK, REPORT, GUIDE, REPASTE_GUIDE])
    assert package.repaste_guide == package.directory / REPASTE_GUIDE
    assert "| Beneficiaries | 2 | 3 |" in package.repaste_guide.read_text(encoding="utf-8")
    assert package.build.shape.beneficiaries == 3


def test_a_rebuild_under_an_older_profile_version_records_that_version(tmp_path, check_passes, newer_profile_version):
    new = {k: v for k, v in shape(beneficiaries=3).items() if k != "profile"}  # takes the old version, not 1.1
    package = rebuild(shape(), new, tmp_path / "package")

    built = package.build
    assert built.profile.version == "1.0"
    cover = load_workbook(package.workbook)["Cover"]
    provenance = {row[0].value: row[1].value for row in cover.iter_rows(min_row=5, max_row=7, max_col=2)}
    assert provenance["Profile version"] == "1.0"
    assert check_structure(package.workbook, built.shape, built.profile, built.layout) == []


def test_a_refused_rebuild_writes_nothing(tmp_path, check_passes):
    out = tmp_path / "package"
    with pytest.raises(ShapeError):
        rebuild(shape(acronym="ACME"), shape(), out)
    assert not out.exists()


@pytest.mark.excel
def test_a_real_rebuild_passes_the_synthetic_check(tmp_path):
    pytest.importorskip("win32com.client", reason="the Synthetic Check needs Excel via COM (Windows)")
    package = rebuild(shape(), shape(beneficiaries=3, affiliated_entities=[1, 0, 0], tasks=[2, 1, 1]), tmp_path / "pkg")

    assert sorted(p.name for p in package.directory.iterdir()) == sorted([WORKBOOK, REPORT, GUIDE, REPASTE_GUIDE])
    assert "Result: **PASS**" in package.report.read_text(encoding="utf-8")

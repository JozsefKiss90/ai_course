"""The command line the budget-planner skill drives: ``python -m budget_engine <command>``.

Shape Parameters arrive as JSON on stdin, so they never land in a file. ``profiles`` lists what
each Funding Profile allows, ``confirm`` reads the Shape Parameters back for the human to confirm,
and ``deliver`` builds, checks and packages. The Synthetic Check is stood in for as in
``test_handover``; the real Excel run is covered there.
"""

import importlib
import io
import json
from pathlib import Path

import pytest

from budget_engine.cli import main
from budget_engine.handover import GUIDE, REPORT, WORKBOOK

from budget_engine.verify.excel import ExcelUnavailable
from test_handover import check_fails, check_passes, shape  # noqa: F401 (fixtures)

BUILD_MODULE = importlib.import_module("budget_engine.build")


def run(*argv: str, stdin: object = None) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    text = stdin if isinstance(stdin, str) or stdin is None else json.dumps(stdin)
    code = main(list(argv), stdin=io.StringIO(text or ""), stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


# profiles


def test_profiles_lists_each_profile_with_its_method_rules_and_default_headroom():
    code, out, _ = run("profiles")

    assert code == 0
    he = next(p for p in json.loads(out) if (p["id"], p["version"]) == ("he-lump-sum", "1.0"))
    assert he["name"] == "Horizon Europe lump sum"
    assert he["default_headroom"] == 3
    assert he["effort_unit"] == "person-months"
    methods = {m["id"]: m for m in he["methods"]}
    assert list(methods) == ["staff_effort", "travel_planner", "equipment_depreciation", "itemised_list"]
    assert methods["staff_effort"] == {"id": "staff_effort", "label": "Staff effort", "default": True, "mandatory": True}
    assert methods["travel_planner"]["mandatory"] is False and methods["travel_planner"]["default"] is True


# confirm


def test_confirm_reads_back_every_shape_parameter():
    code, out, _ = run("confirm", stdin=shape(affiliated_entities=[1, 0], tasks=[2, 1, 3]))

    assert code == 0
    assert "Funding Profile: Horizon Europe lump sum (he-lump-sum 1.0)" in out
    assert "Beneficiaries: 2" in out
    assert "Affiliated Entities: BE1: 1, BE2: 0 (1 in all)" in out
    assert "Work packages: 3" in out
    assert "Tasks: WP1: 2, WP2: 1, WP3: 3 (Task List on, effort per task)" in out
    assert "Duration: 36 months" in out
    assert "Headroom: 3 spare blocks (profile default)" in out


def test_confirm_without_tasks_plans_effort_per_work_package():
    _, out, _ = run("confirm", stdin=shape())

    assert "Tasks: none (no Task List, effort per work package)" in out
    assert "Affiliated Entities: none" in out


def test_confirm_switches_mandatory_methods_on_and_marks_them_locked():
    _, out, _ = run("confirm", stdin=shape(methods=["travel_planner"]))

    methods = out.split("Estimation Methods:", 1)[1].split("\nHeadroom", 1)[0]
    assert "[on] Staff effort (mandatory, locked on)" in methods
    assert "[on] Travel planner" in methods
    assert "[off] Equipment depreciation" in methods
    assert "[off] Itemised list" in methods


def test_confirm_without_methods_takes_the_profile_defaults():
    _, out, _ = run("confirm", stdin=shape())

    assert "[off]" not in out


def test_confirm_shows_a_headroom_override_against_the_profile_default():
    _, out, _ = run("confirm", stdin=shape(headroom=5))

    assert "Headroom: 5 spare blocks (override; profile default 3)" in out


def test_confirm_reads_an_explicit_default_headroom_as_the_default():
    _, out, _ = run("confirm", stdin=shape(headroom=3))

    assert "Headroom: 3 spare blocks (profile default)" in out


def test_confirm_refuses_anything_outside_the_shape_parameters_without_echoing_its_value():
    code, out, err = run("confirm", stdin=shape(partner_names=["Acme University"], budget=250000))

    assert code == 2 and out == ""
    assert "not a Shape Parameter: budget, partner_names" in err
    assert "Acme" not in err and "250000" not in err


def test_confirm_refuses_a_count_given_as_text_without_echoing_it():
    code, _, err = run("confirm", stdin=shape(beneficiaries="Acme and Beta"))

    assert code == 2
    assert "beneficiaries must be a whole number" in err
    assert "Acme" not in err


def test_confirm_refuses_a_method_the_profile_does_not_allow():
    code, _, err = run("confirm", stdin=shape(methods=["staff_effort", "Acme visit"]))

    assert code == 2 and "1 Estimation Method(s) not allowed by he-lump-sum 1.0" in err
    assert "allowed: staff_effort, travel_planner" in err and "Acme" not in err


def test_confirm_refuses_an_unknown_profile_without_echoing_it():
    code, _, err = run("confirm", stdin=shape(profile={"id": "Acme proposal", "version": "1.0"}))

    assert code == 2 and "no such Funding Profile version (available: he-lump-sum 1.0)" in err
    assert "Acme" not in err


def test_confirm_refuses_input_that_is_not_a_json_object():
    assert run("confirm", stdin="beneficiaries: 3")[0] == 2
    assert run("confirm", stdin=[1, 2])[0] == 2


# deliver


def test_deliver_writes_the_handover_package_and_says_where(tmp_path, check_passes):
    out_dir = tmp_path / "package"
    code, out, _ = run("deliver", "--out", str(out_dir), stdin=shape())

    assert code == 0
    assert sorted(p.name for p in out_dir.iterdir()) == sorted([WORKBOOK, REPORT, GUIDE])
    assert "Synthetic Check: PASS" in out
    for name in (WORKBOOK, REPORT, GUIDE):
        assert str(out_dir / name) in out


def test_deliver_stops_on_a_failing_synthetic_check_and_points_to_the_report(tmp_path, check_fails):
    out_dir = tmp_path / "package"
    code, out, err = run("deliver", "--out", str(out_dir), stdin=shape())

    assert code == 1 and out == ""
    assert [p.name for p in out_dir.iterdir()] == [REPORT]
    assert "Synthetic Check failed" in err and "No Handover Package" in err
    assert str(out_dir / REPORT) in err


def test_deliver_refuses_a_shape_outside_the_contract_and_writes_nothing(tmp_path, check_passes):
    out_dir = tmp_path / "package"
    code, _, err = run("deliver", "--out", str(out_dir), stdin=shape(project_acronym="SECRET"))

    assert code == 2 and "not a Shape Parameter: project_acronym" in err
    assert "SECRET" not in err
    assert not out_dir.exists()


def test_deliver_refuses_a_non_empty_directory(tmp_path, check_passes):
    out_dir = tmp_path / "package"
    out_dir.mkdir()
    (out_dir / "old.txt").write_text("earlier", encoding="utf-8")

    code, _, err = run("deliver", "--out", str(out_dir), stdin=shape())

    assert code == 1 and "new or empty directory" in err
    assert [p.name for p in out_dir.iterdir()] == ["old.txt"]


def test_deliver_stops_when_a_structural_check_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(BUILD_MODULE, "check_structure", lambda *a: ["Cover Sheet lacks the profile version"])
    out_dir = tmp_path / "package"

    code, out, err = run("deliver", "--out", str(out_dir), stdin=shape())

    assert code == 1 and out == ""
    assert "structural checks failed" in err and "Cover Sheet lacks the profile version" in err
    assert "No Handover Package" in err
    assert list(out_dir.iterdir()) == []


def test_deliver_needs_an_output_directory():
    with pytest.raises(SystemExit):
        run("deliver", stdin=shape())



def test_deliver_stops_when_excel_is_unavailable(tmp_path, monkeypatch):
    def no_excel(result):
        raise ExcelUnavailable("could not start Excel via COM")

    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", no_excel)
    out_dir = tmp_path / "package"
    code, out, err = run("deliver", "--out", str(out_dir), stdin=shape())

    assert code == 1 and out == ""
    assert "could not start Excel" in err and "No Handover Package" in err
    assert list(out_dir.iterdir()) == []


def test_deliver_reports_a_directory_it_cannot_write(tmp_path, check_passes):
    blocker = tmp_path / "a-file"
    blocker.write_text("not a directory", encoding="utf-8")

    code, out, err = run("deliver", "--out", str(blocker / "package"), stdin=shape())

    assert code == 1 and out == "" and "No Handover Package" in err

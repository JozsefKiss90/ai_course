"""The budget-profile-maintainer's engine side: draft, diff, expectation proposal, check and acceptance.

Every test but the first works in a sandbox: a copy of the Funding Profile data, the Golden Scenario
transcriptions and the worksheets, so no test writes a profile version or an expected figure into the
repo. The Synthetic Check is stood in for, except in the demo marked ``excel``.
"""

import importlib
import json
import shutil
from datetime import date
from pathlib import Path

import pytest

from budget_engine import maintain, profiles
from budget_engine.build import SyntheticCheckFailed
from budget_engine.verify import golden
from budget_engine.verify.synthetic import Mismatch, SyntheticCheckReport

HE = "he-lump-sum"
TRAVEL = "he_travel_unit_costs_c2024_5405.json"
DEMO_TRAVEL = "he_travel_unit_costs_demo.json"
# The module, not the build function the package exports under the same name.
BUILD_MODULE = importlib.import_module("budget_engine.build")


def test_accepted_profile_versions_are_unchanged():
    """The immutability check on the repo itself: every accepted version, and every shared data file
    it reads, is byte for byte (line endings aside) what was accepted."""
    assert maintain.immutability_problems() == []
    assert maintain.is_accepted(HE, "1.0")


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    data, transcriptions, worksheets = tmp_path / "data", tmp_path / "transcriptions", tmp_path / "worksheets"
    shutil.copytree(profiles.DATA_DIR, data)
    shutil.copytree(golden.GOLDEN_DIR, transcriptions)
    shutil.copytree(golden.WORKSHEET_DIR, worksheets)
    monkeypatch.setattr(profiles, "DATA_DIR", data)
    monkeypatch.setattr(golden, "GOLDEN_DIR", transcriptions)
    monkeypatch.setattr(golden, "WORKSHEET_DIR", worksheets)
    return tmp_path


def _edit(path: Path, change) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    change(raw)
    path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")


def _demo_version(sandbox: Path, amount: int = 370) -> Path:
    """Version 1.1: one travel unit cost changed (601-1600 km, 365 -> ``amount``), from a new data file."""
    data = profiles.DATA_DIR
    path = maintain.draft_version(HE, "1.0", "1.1")

    def band(raw):
        rows = next(t for t in raw["tables"] if t["id"] == "travel_bands")["rows"]
        next(r for r in rows if r["from_km"] == 601)["amount"] = amount
        raw["source"]["version"] = "Demo amendment of C(2024)5405 (test data)"

    shutil.copy(data / TRAVEL, data / DEMO_TRAVEL)
    _edit(data / DEMO_TRAVEL, band)

    def point_at_demo(raw):
        for ref in raw["unit_cost_tables"].values():
            ref["file"] = DEMO_TRAVEL
        for entry in raw["provenance"]:
            entry.setdefault("version", "as in 1.0")
            if entry.get("file", "").endswith(TRAVEL):
                entry.update(version="Demo amendment of C(2024)5405 (test data)", file=f"profiles/data/{DEMO_TRAVEL}")

    _edit(path, point_at_demo)
    return path


def _approve(version: str, **kwargs):
    """Approve the proposal for ``version`` as it stands, quoting its id as the human saw it."""
    proposal_id = maintain.propose_expectations(HE, version, "1.0").proposal_id
    return maintain.approve_expectations(HE, version, "1.0", proposal_id=proposal_id, **kwargs)


def _stand_in(human_owned=True, mismatches=()):
    def check(result):
        return SyntheticCheckReport(
            workbook=result.path.name, scenario="stand-in", scenario_provenance="stand-in", human_owned=human_owned,
            figures=("BE1 WP1 F total",), table_rows_added=(), mismatches=tuple(mismatches),
            copy_path=Path("unused"), copy_deleted=True, pinned_figures=1 if human_owned else 0,
        )
    return check


@pytest.fixture
def check_passes(monkeypatch):
    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", _stand_in())


# immutability


def test_changing_an_accepted_version_or_a_data_file_it_reads_is_reported(sandbox):
    _edit(profiles.DATA_DIR / HE / "1.0.json", lambda raw: raw.update(default_headroom=4))
    _edit(profiles.DATA_DIR / TRAVEL, lambda raw: raw["source"].update(date="2025-01-01"))

    problems = maintain.immutability_problems()

    assert any(f"{HE}/1.0.json" in p for p in problems)
    assert any(TRAVEL in p for p in problems)


def test_changing_the_golden_scenario_an_accepted_version_rests_on_is_reported(sandbox):
    _edit(golden.transcription_path(HE, "1.0"), lambda raw: raw["expected"]["trip_totals"].update({"1": 1.0}))

    assert any(f"{HE}-1.0.json" in p for p in maintain.immutability_problems())


def test_line_endings_alone_do_not_count_as_a_change(sandbox):
    path = profiles.DATA_DIR / HE / "1.0.json"
    path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))

    assert maintain.immutability_problems() == []


def test_a_deleted_accepted_version_is_reported(sandbox):
    (profiles.DATA_DIR / HE / "1.0.json").unlink()

    assert any("missing" in p for p in maintain.immutability_problems())


# draft


def test_a_draft_is_written_alongside_the_old_version_and_is_not_accepted(sandbox):
    old = (profiles.DATA_DIR / HE / "1.0.json").read_bytes()

    path = maintain.draft_version(HE, "1.0", "1.1")

    assert path == profiles.DATA_DIR / HE / "1.1.json"
    assert json.loads(path.read_text(encoding="utf-8"))["version"] == "1.1"
    assert (profiles.DATA_DIR / HE / "1.0.json").read_bytes() == old
    assert not maintain.is_accepted(HE, "1.1")
    assert maintain.immutability_problems() == []


def test_a_draft_never_overwrites_an_existing_version(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")

    with pytest.raises(FileExistsError):
        maintain.draft_version(HE, "1.0", "1.1")
    with pytest.raises(FileExistsError):
        maintain.draft_version(HE, "1.1", "1.0")


def test_every_source_document_of_a_new_version_needs_its_version(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")  # 1.0 names three documents without a version

    problems = maintain.source_document_problems(HE, "1.1")

    assert len(problems) == 3 and all("version" in p for p in problems)
    _edit(profiles.DATA_DIR / HE / "1.1.json", lambda raw: [e.setdefault("version", "x") for e in raw["provenance"]])
    assert maintain.source_document_problems(HE, "1.1") == []


def test_a_new_data_file_must_be_among_the_source_documents(sandbox):
    _demo_version(sandbox)
    assert maintain.source_document_problems(HE, "1.1") == []

    _edit(profiles.DATA_DIR / HE / "1.1.json", lambda raw: [e.pop("file", None) for e in raw["provenance"]])

    assert maintain.source_document_problems(HE, "1.1") == [f"new data file {DEMO_TRAVEL} is not among the source documents"]


# diff


def test_the_diff_shows_a_changed_unit_cost_value_and_the_new_source(sandbox):
    _demo_version(sandbox)

    diff = maintain.profile_diff(HE, "1.0", "1.1")

    assert diff.startswith(f"# Funding Profile {HE}: 1.0 -> 1.1")
    assert "## Unit-cost tables" in diff
    band = next(line for line in diff.splitlines() if "601" in line and "365" in line)
    assert "370" in band
    assert "Demo amendment of C(2024)5405" in diff  # the source document, in provenance and the table source


def test_the_diff_has_a_section_for_every_part_of_a_profile(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")

    def change(raw):
        next(c for c in raw["profile_constants"] if c["id"] == "indirect_rate")["value"] = 0.3
        raw["transfer_view"]["rows"][0]["label"] = "Renamed heading"
        raw["estimation_methods"]["default"] = ["staff_effort"]
        raw["input_guards"]["rule_checks"] = [{"id": "wp_share", "kind": "share_limit", "label": "WP share above",
                                               "severity": "warning", "params": {"limit": "max_wp_share"}}]
        raw["lump_sum_tiers"] = [120000, 250000]

    _edit(profiles.DATA_DIR / HE / "1.1.json", change)

    diff = maintain.profile_diff(HE, "1.0", "1.1")

    for heading in ("Source documents", "Profile Constants", "Unit-cost tables", "Layout", "Estimation Methods",
                    "Rule checks", "Lump Sum Tiers"):
        assert f"## {heading}" in diff
    sections = dict(s.split("\n", 1) for s in diff.split("\n## ")[1:])
    assert "0.25" in sections["Profile Constants"] and "0.3" in sections["Profile Constants"]
    assert "Renamed heading" in sections["Layout"]
    assert "travel_planner" in sections["Estimation Methods"]
    assert "wp_share" in sections["Rule checks"] and "share_limit" in sections["Rule checks"]
    assert "250000" in sections["Lump Sum Tiers"]
    assert "No change." in sections["Unit-cost tables"]


def test_identical_versions_diff_to_no_change(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")

    diff = maintain.profile_diff(HE, "1.0", "1.1")

    assert diff.count("No change.") == len(maintain.DIFF_SECTIONS)


# expectations


def test_recomputing_the_signed_off_figures_under_their_own_version_changes_nothing(sandbox):
    """The proposal machinery reproduces every figure of the 1.0 worksheet from its inputs."""
    maintain.draft_version(HE, "1.0", "1.1")

    proposal = maintain.propose_expectations(HE, "1.1", "1.0")

    assert proposal.changes == ()
    assert proposal.figures_compared > 100
    assert "No expected figure changes" in proposal.to_markdown()


def test_a_unit_cost_change_proposes_new_figures_and_writes_nothing(sandbox):
    _demo_version(sandbox)
    before = sorted(p.name for p in golden.GOLDEN_DIR.iterdir()) + sorted(p.name for p in golden.WORKSHEET_DIR.iterdir())

    proposal = maintain.propose_expectations(HE, "1.1", "1.0")

    changed = {c.figure: (c.before, c.after) for c in proposal.changes}
    # Trip 1 (BE1, WP1): 2 travellers, 1100 km, so 2 x (370 - 365) more.
    assert changed["trip_totals.1"] == (2206.0, 2216.0)
    assert changed["transfer_view.BE1.WP1.lines.C1"] == ([2, 1103.0, 2206.0], [2, 1108.0, 2216.0])
    assert changed["transfer_view.BE1.WP1.F"] == (60257.5, 60270.0)
    assert "trip_totals.2" not in changed  # 2900 km: another band
    text = proposal.to_markdown()
    assert "PROPOSAL" in text and "not applied" in text and "2216" in text
    after = sorted(p.name for p in golden.GOLDEN_DIR.iterdir()) + sorted(p.name for p in golden.WORKSHEET_DIR.iterdir())
    assert after == before


def test_approved_expectations_become_the_new_versions_golden_scenario(sandbox):
    _demo_version(sandbox)

    written = _approve("1.1", approved_by="the profile owner", on=date(2026, 11, 9))

    raw = json.loads((golden.GOLDEN_DIR / f"{HE}-1.1.json").read_text(encoding="utf-8"))
    assert raw["shape"]["profile"] == {"id": HE, "version": "1.1"}
    assert raw["expected"]["trip_totals"]["1"] == 2216.0
    assert raw["worksheet"] == f"golden/{HE}-1.1.md"
    worksheet = (golden.WORKSHEET_DIR / f"{HE}-1.1.md").read_text(encoding="utf-8")
    assert "the profile owner" in worksheet and "2026-11-09" in worksheet and "2216" in worksheet
    assert set(written) == {golden.GOLDEN_DIR / f"{HE}-1.1.json", golden.WORKSHEET_DIR / f"{HE}-1.1.md"}
    assert golden.load_golden(profiles.load_profile(HE, "1.1")).expected["trip_totals"]["1"] == 2216.0


def test_approval_never_overwrites_a_golden_scenario(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")
    _approve("1.1", approved_by="the profile owner")

    with pytest.raises(FileExistsError):
        _approve("1.1", approved_by="the profile owner")
    with pytest.raises(FileExistsError):
        _approve("1.0", approved_by="the profile owner")


def test_approval_writes_only_the_proposal_the_human_saw(sandbox):
    _demo_version(sandbox, amount=370)
    shown = maintain.propose_expectations(HE, "1.1", "1.0").proposal_id
    _edit(profiles.DATA_DIR / DEMO_TRAVEL, lambda raw: next(
        r for r in next(t for t in raw["tables"] if t["id"] == "travel_bands")["rows"] if r["from_km"] == 601
    ).update(amount=380))  # the draft changes after the proposal was shown

    with pytest.raises(ValueError, match=shown):
        maintain.approve_expectations(HE, "1.1", "1.0", proposal_id=shown, approved_by="the profile owner")
    assert not golden.transcription_path(HE, "1.1").exists()


def test_approval_needs_a_named_approver(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")

    with pytest.raises(ValueError):
        _approve("1.1", approved_by="  ")


# check and acceptance


def _ready(sandbox):
    _demo_version(sandbox)
    _approve("1.1", approved_by="the profile owner")


def test_a_version_with_a_passing_check_is_accepted_and_then_immutable(sandbox, check_passes):
    _ready(sandbox)

    report = maintain.accept_version(HE, "1.1", sandbox / "check")

    assert report.passed and maintain.is_accepted(HE, "1.1")
    assert (sandbox / "check" / maintain.CHECK_REPORT).exists()
    assert maintain.immutability_problems() == []
    _edit(profiles.DATA_DIR / DEMO_TRAVEL, lambda raw: raw["source"].update(date="2030-01-01"))
    assert any(DEMO_TRAVEL in p for p in maintain.immutability_problems())


def test_the_check_runs_at_the_golden_shape_of_the_version(sandbox, monkeypatch):
    _ready(sandbox)
    seen = []

    def check(result):
        seen.append((result.profile.version, result.shape))
        return _stand_in()(result)

    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", check)

    maintain.check_version(HE, "1.1", sandbox / "check")

    gold = golden.load_golden(profiles.load_profile(HE, "1.1"))
    assert seen == [("1.1", gold.shape)]
    assert not any((sandbox / "check").glob("*.xlsx"))  # the check's workbook is not kept


@pytest.mark.parametrize(
    "spoil, needle",
    [
        (lambda s: (golden.GOLDEN_DIR / f"{HE}-1.1.json").unlink(), "Golden Scenario"),
        (lambda s: _edit(profiles.DATA_DIR / HE / "1.1.json", lambda raw: raw["provenance"][0].pop("version")), "version"),
        (lambda s: _edit(profiles.DATA_DIR / HE / "1.0.json", lambda raw: raw.update(name="edited")), "1.0.json"),
    ],
)
def test_acceptance_is_refused_before_any_check_runs(sandbox, check_passes, spoil, needle):
    _ready(sandbox)
    spoil(sandbox)

    with pytest.raises(maintain.NotAccepted, match=needle):
        maintain.accept_version(HE, "1.1", sandbox / "check")
    assert not maintain.is_accepted(HE, "1.1")


def test_a_failing_check_is_not_accepted(sandbox, monkeypatch):
    _ready(sandbox)
    mismatch = Mismatch("BE1 WP1 F total", "'Transfer View BE1'!D40", 60270.0, 60257.5, 12.5)
    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", _stand_in(mismatches=[mismatch]))

    with pytest.raises(SyntheticCheckFailed):
        maintain.accept_version(HE, "1.1", sandbox / "check")
    assert not maintain.is_accepted(HE, "1.1")
    assert "FAIL" in (sandbox / "check" / maintain.CHECK_REPORT).read_text(encoding="utf-8")


def test_a_check_not_against_the_signed_off_figures_is_not_accepted(sandbox, monkeypatch):
    _ready(sandbox)
    monkeypatch.setattr(BUILD_MODULE, "run_synthetic_check", _stand_in(human_owned=False))

    with pytest.raises(maintain.NotAccepted, match="signed-off"):
        maintain.accept_version(HE, "1.1", sandbox / "check")


def test_an_accepted_version_is_not_accepted_again(sandbox, check_passes):
    with pytest.raises(maintain.NotAccepted, match="already accepted"):
        maintain.accept_version(HE, "1.0", sandbox / "check")


# demo


@pytest.mark.excel
def test_demo_one_unit_cost_value_through_draft_diff_check_and_approval(sandbox):
    """Ticket 17's demo, with real Excel: 601-1600 km travel 365 -> 370 EUR as version 1.1."""
    _demo_version(sandbox)
    assert "370" in maintain.profile_diff(HE, "1.0", "1.1")

    proposal = maintain.propose_expectations(HE, "1.1", "1.0")
    assert proposal.changes  # the human sees these before anything is written
    with pytest.raises(maintain.NotAccepted, match="Golden Scenario"):
        maintain.accept_version(HE, "1.1", sandbox / "refused")  # no approval yet

    _approve("1.1", approved_by="the profile owner")
    report = maintain.accept_version(HE, "1.1", sandbox / "check")

    assert report.passed and report.human_owned and report.pinned_figures > 0
    assert maintain.is_accepted(HE, "1.1") and maintain.immutability_problems() == []


# command line


def run(*argv: str, stdin: object = None) -> tuple[int, str, str]:
    import io

    from budget_engine.cli import main

    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), stdin=io.StringIO(json.dumps(stdin) if stdin else ""), stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def test_the_planner_is_offered_accepted_versions_only(sandbox):
    maintain.draft_version(HE, "1.0", "1.1")

    code, out, _ = run("profiles")
    listed = [(p["id"], p["version"]) for p in json.loads(out)]
    refused, _, err = run("confirm", stdin={"profile": {"id": HE, "version": "1.1"}, "beneficiaries": 1,
                                            "work_packages": 1, "duration_months": 12})

    assert code == 0 and listed == [(HE, "1.0")]
    assert refused == 2 and "not accepted" in err


def test_the_maintainer_commands_take_a_version_from_draft_to_accepted(sandbox, check_passes):
    code, out, _ = run("profile-draft", HE, "--from", "1.0", "--version", "1.1")
    assert code == 0 and "1.1.json" in out
    _edit(profiles.DATA_DIR / HE / "1.1.json", lambda raw: [e.setdefault("version", "x") for e in raw["provenance"]])

    assert run("profile-diff", HE, "1.0", "1.1")[1].startswith(f"# Funding Profile {HE}: 1.0 -> 1.1")
    proposal = run("profile-propose", HE, "1.1", "--from", "1.0")[1]
    assert "PROPOSAL" in proposal
    proposal_id = proposal.split("Proposal id: `")[1].split("`")[0]
    refused = run("profile-accept", HE, "1.1", "--out", str(sandbox / "check"))
    assert refused[0] == 1 and "Golden Scenario" in refused[2]

    code, out, _ = run("profile-approve", HE, "1.1", "--from", "1.0", "--proposal", proposal_id, "--approved-by", "the profile owner")
    assert code == 0 and f"{HE}-1.1.json" in out
    code, out, _ = run("profile-check", HE, "1.1", "--out", str(sandbox / "check"))
    assert code == 0 and "Synthetic Check: PASS" in out and not maintain.is_accepted(HE, "1.1")
    code, out, _ = run("profile-accept", HE, "1.1", "--out", str(sandbox / "check"))
    assert code == 0 and "accepted" in out and maintain.is_accepted(HE, "1.1")


def test_maintainer_commands_refuse_rather_than_overwrite(sandbox):
    assert run("profile-draft", HE, "--from", "1.0", "--version", "1.0")[0] == 2
    assert run("profile-approve", HE, "1.0", "--from", "1.0", "--proposal", "x", "--approved-by", "x")[0] == 2
    assert run("profile-diff", HE, "1.0", "9.9")[0] == 2


@pytest.mark.excel
def test_demo_the_old_expected_figures_under_the_changed_version_fail_the_check(sandbox):
    """Copying 1.0's Golden Scenario forward unchanged, instead of approving the proposed figures, is caught."""
    _demo_version(sandbox)
    copied = golden.GOLDEN_DIR / f"{HE}-1.1.json"
    shutil.copy(golden.GOLDEN_DIR / f"{HE}-1.0.json", copied)
    _edit(copied, lambda raw: raw["shape"]["profile"].update(version="1.1"))

    with pytest.raises(SyntheticCheckFailed):
        maintain.accept_version(HE, "1.1", sandbox / "check")
    assert not maintain.is_accepted(HE, "1.1")
    assert "| 60,257.50 | 60,270.00 |" in (sandbox / "check" / maintain.CHECK_REPORT).read_text(encoding="utf-8")

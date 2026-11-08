"""The profile maintainer's side of the engine: draft, diff, propose expectations, check and accept.

A Funding Profile version is data (``profiles/data/<id>/<version>.json``). A new version starts as a
draft written alongside the old ones, and is accepted only when it records a version for every source
document, has a Golden Scenario the human approved, and passes the Synthetic Check against it.

Accepted versions are listed in ``profiles/data/accepted.json`` with a SHA-256 of every file they are
read from: the version itself and the shared data files it names (unit-cost tables, country lists).
``immutability_problems`` compares those digests with the files, so an accepted version, or a data
file one reads, can never change unnoticed. A changed rule goes into a new version and new data file.

Golden Scenario expectations stay human-owned. ``propose_expectations`` reads the previous version's
Golden Scenario under the new version and recomputes its expected figures with the reference model,
writing nothing; only ``approve_expectations``, run after the human approved the proposal, writes the
new version's Golden Scenario. It never overwrites one.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from budget_engine import profiles
from budget_engine.build import SyntheticCheckFailed, build
from budget_engine.methods import travel_planner
from budget_engine.profiles import ProfileNotFound, load_profile
from budget_engine.verify import golden
from budget_engine.verify.golden import GoldenScenario
from budget_engine.verify.reference import expected_check_summaries, expected_transfer_view
from budget_engine.verify.synthetic import SyntheticCheckReport

REGISTRY = "accepted.json"
CHECK_REPORT = "synthetic-check-report.md"
TOLERANCE = 0.005

# Each part of a profile version, as the diff groups it: section -> its top-level keys. "Other"
# takes every key no section names, so no change is left out of the diff.
DIFF_SECTIONS: dict[str, tuple[str, ...]] = {
    "Source documents": ("provenance",),
    "Profile Constants": ("profile_constants",),
    "Unit-cost tables": ("unit_cost_tables",),
    "Layout": (
        "name", "effort_unit", "rate_unit", "cost_categories", "staff_categories", "indirect_rule",
        "reference_lists", "transfer_view", "check_summaries", "handover",
    ),
    "Estimation Methods": ("estimation_methods", "method_settings", "default_headroom"),
    "Rule checks": ("input_guards",),
    "Lump Sum Tiers": ("lump_sum_tiers",),
    "Other": (),
}
IDENTITY = ("id", "document", "country", "from_km")  # fields that name an entry of a list in a diff


class NotAccepted(RuntimeError):
    """A profile version cannot be accepted (yet); the message lists every reason."""


# accepted versions


def _version_path(profile_id: str, version: str) -> Path:
    return profiles.DATA_DIR / profile_id / f"{version}.json"


def _raw(profile_id: str, version: str) -> dict[str, Any]:
    path = _version_path(profile_id, version)
    if not path.is_file():
        raise ProfileNotFound(f"no Funding Profile {profile_id!r} version {version!r}")
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return raw


def _registry() -> dict[str, dict[str, Any]]:
    path = profiles.DATA_DIR / REGISTRY
    if not path.exists():
        return {}
    registry: dict[str, dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    return registry


def is_accepted(profile_id: str, version: str) -> bool:
    return version in _registry().get(profile_id, {})


def _digest(path: Path) -> str:
    """SHA-256 of the file with its line endings normalised, so a checkout's CRLF is no change."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _files(profile_id: str, version: str) -> list[str]:
    """The files a version is read from, relative to the data directory: itself and the data files it names."""
    raw = _raw(profile_id, version)
    named: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            file = node.get("file")
            if isinstance(file, str) and (profiles.DATA_DIR / file).is_file():
                named.add(file)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk({k: v for k, v in raw.items() if k != "provenance"})  # provenance names documents, not data files
    return [f"{profile_id}/{version}.json", *sorted(named)]


def immutability_problems() -> list[str]:
    """Every file an accepted version rests on that is missing or no longer as accepted: the version, the
    data files it reads and the Golden Scenario transcription it was accepted against."""
    problems = []
    for profile_id, versions in sorted(_registry().items()):
        for version, entry in sorted(versions.items()):
            files = [(profiles.DATA_DIR / name, name, digest) for name, digest in entry["files"].items()]
            files += [(golden.GOLDEN_DIR / name, name, digest) for name, digest in entry["golden_scenario"].items()]
            for path, name, digest in files:
                if not path.is_file():
                    problems.append(f"{name} is missing, but accepted {profile_id} {version} rests on it")
                elif _digest(path) != digest:
                    problems.append(
                        f"{name} changed after {profile_id} {version} was accepted: accepted versions and the "
                        "files they rest on are immutable, so a change goes into a new version and data file"
                    )
    return problems


def _register(profile_id: str, version: str, on: date) -> None:
    registry = _registry()
    files = {name: _digest(profiles.DATA_DIR / name) for name in _files(profile_id, version)}
    transcription = golden.transcription_path(profile_id, version)
    registry.setdefault(profile_id, {})[version] = {
        "accepted": on.isoformat(), "files": files, "golden_scenario": {transcription.name: _digest(transcription)},
    }
    (profiles.DATA_DIR / REGISTRY).write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


# draft


def draft_version(profile_id: str, from_version: str, new_version: str) -> Path:
    """Start version ``new_version`` as a copy of ``from_version``, written alongside it.

    Raises FileExistsError rather than overwrite any existing version.
    """
    raw = _raw(profile_id, from_version)
    path = _version_path(profile_id, new_version)
    if path.exists():
        raise FileExistsError(f"{profile_id} {new_version} already exists: versions are never overwritten")
    raw["version"] = new_version
    path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def source_document_problems(profile_id: str, version: str) -> list[str]:
    """What the version's provenance lacks: at least one source document, each with its version, and an
    entry for every data file the version reads that no accepted version reads."""
    provenance = _raw(profile_id, version).get("provenance") or []
    if not provenance:
        return [f"{profile_id} {version} records no source documents"]
    problems = [
        f"source document {entry.get('document') or f'#{n}'!r} records no version"
        for n, entry in enumerate(provenance, start=1)
        if not entry.get("document") or not str(entry.get("version", "")).strip()
    ]
    accepted = {name for versions in _registry().values() for entry in versions.values() for name in entry["files"]}
    listed = {Path(str(entry.get("file", ""))).name for entry in provenance}
    problems += [
        f"new data file {name} is not among the source documents"
        for name in _files(profile_id, version)[1:]
        if name not in accepted and Path(name).name not in listed
    ]
    return problems


# diff


def _resolved(profile_id: str, version: str) -> dict[str, Any]:
    """The version's data with its unit-cost tables read from the data files they name."""
    raw = _raw(profile_id, version)
    tables = profiles.resolve_unit_cost_tables(raw.get("unit_cost_tables", {}))
    raw["unit_cost_tables"] = {
        key: {
            **ref, "title": tables[key].title, "source document": tables[key].source,
            "annex": tables[key].annex, "pages": tables[key].pages, "rows": list(tables[key].rows),
        }
        for key, ref in raw.get("unit_cost_tables", {}).items()
    }
    return raw


def _leaves(node: object, path: str = "") -> Iterator[tuple[str, object]]:
    """(path, value) for every leaf; a list of plain values is one leaf, an entry of a list of objects is
    named by its identity field where it has one."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _leaves(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list) and any(isinstance(v, (dict, list)) for v in node):
        for n, value in enumerate(node):
            name = next((f"{f}={value[f]}" for f in IDENTITY if isinstance(value, dict) and f in value), str(n))
            yield from _leaves(value, f"{path}[{name}]")
    else:
        yield path, node


def _show(value: object) -> str:
    if value is _ABSENT:
        return "—"
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value) or "(empty)"
    return str(value).replace("|", "\\|").replace("\n", " ")


_ABSENT = object()


def profile_diff(profile_id: str, old: str, new: str) -> str:
    """A Markdown diff of two versions, one section per part of a profile, unit-cost rows included."""
    before, after = _resolved(profile_id, old), _resolved(profile_id, new)
    named = {k for keys in DIFF_SECTIONS.values() for k in keys} | {"id", "version"}
    lines = [f"# Funding Profile {profile_id}: {old} -> {new}", ""]
    for section, keys in DIFF_SECTIONS.items():
        if not keys:
            keys = tuple(k for k in {**before, **after} if k not in named)
        left = dict(_leaves({k: before[k] for k in keys if k in before}))
        right = dict(_leaves({k: after[k] for k in keys if k in after}))
        changed = [p for p in {**left, **right} if left.get(p, _ABSENT) != right.get(p, _ABSENT)]
        lines += [f"## {section}", ""]
        if not changed:
            lines += ["No change.", ""]
            continue
        lines += [f"| What | {old} | {new} |", "|---|---|---|"]
        lines += [f"| `{p}` | {_show(left.get(p, _ABSENT))} | {_show(right.get(p, _ABSENT))} |" for p in changed]
        lines.append("")
    return "\n".join(lines)


# expectations


@dataclass(frozen=True)
class ExpectationChange:
    figure: str  # path in the Golden Scenario's expected figures, e.g. "transfer_view.BE1.WP1.F"
    before: object  # the signed-off figure; None where the previous version had none
    after: object  # the figure recomputed under the new version; None where it has none


@dataclass(frozen=True)
class ExpectationProposal:
    profile_id: str
    version: str
    previous: str
    changes: tuple[ExpectationChange, ...]
    figures_compared: int
    golden_scenario: dict[str, Any]  # the new version's Golden Scenario transcription, as it would be written

    @property
    def proposal_id(self) -> str:
        """Names exactly these figures: approval must quote it, so what is written is what the human saw."""
        return hashlib.sha256(json.dumps(self.golden_scenario, sort_keys=True).encode()).hexdigest()[:12]

    def changes_table(self, before: str, after: str) -> list[str]:
        return [f"| Figure | {before} | {after} |", "|---|---|---|"] + [
            f"| `{c.figure}` | {_show(c.before)} | {_show(c.after)} |" for c in self.changes
        ]

    def to_markdown(self) -> str:
        lines = [
            f"# PROPOSAL: Golden Scenario expected figures for {self.profile_id} {self.version}",
            "",
            f"Proposal id: `{self.proposal_id}`",
            "",
            f"This is a proposal, not applied: no expected figure has been written. It reads the human-owned "
            f"Golden Scenario of {self.profile_id} {self.previous} (same Shape Parameters, same inputs) under "
            f"{self.version} and recomputes the expected figures with the reference model. {self.figures_compared} "
            "figures compared.",
            "",
        ]
        if not self.changes:
            lines += [f"No expected figure changes: {self.version} keeps every signed-off figure of {self.previous}.", ""]
        else:
            lines += [f"{len(self.changes)} expected figures change:", ""]
            lines += self.changes_table(f"{self.previous} (signed off)", f"{self.version} (proposed)") + [""]
        lines += [
            "Only the human approves these figures. On approval, the new version's Golden Scenario is written "
            "with them; until then the version cannot be accepted.",
            "",
        ]
        return "\n".join(lines)


def _figure(value: float) -> float:
    """An expected figure as the worksheets give it: to the cent."""
    return round(value, 2)


def _pct(share: float) -> float:
    return round(share * 100, 2)


def _recompute(previous: Mapping[str, Any], gold: GoldenScenario) -> dict[str, Any]:
    """The previous expected figures' sections, each recomputed from the Golden inputs under ``gold.profile``."""
    profile, shape, inputs = gold.profile, gold.shape, gold.inputs
    tv = expected_transfer_view(profile, shape, inputs)
    summaries = expected_check_summaries(profile, shape, inputs, tv)
    group = {r.id: r.group for r in profile.transfer_view_rows if r.kind == "line"}
    totals = [r.id for r in profile.transfer_view_rows if r.kind in ("total", "indirect", "grand_total")]
    total_f, total_pm = summaries[("wps", "all", "F", "all", "total")], summaries[("pm", "total", "total")]

    def per_block(block: str, field: str) -> float:
        wps = shape.wp_codes
        if field in group.values():
            return sum(tv.get(("tv", block, wp, line, "total"), 0.0) for wp in wps for line, g in group.items() if g == field)
        return sum(tv[("tv", block, wp, field, "total")] for wp in wps)

    def transfer_view(old: Mapping[str, Any]) -> dict[str, Any]:
        tree: dict[str, Any] = {}
        for block, wps in old.items():
            tree[block] = {}
            for wp in wps:
                lines = {}
                for line in group:
                    items, total = tv.get(("tv", block, wp, line, "items"), 0.0), tv.get(("tv", block, wp, line, "total"), 0.0)
                    if items or total:
                        lines[line] = [_figure(items), _figure(tv[("tv", block, wp, line, "avg")]), _figure(total)]
                tree[block][wp] = {"lines": lines, **{r: _figure(tv[("tv", block, wp, r, "total")]) for r in totals}}
        return tree

    def grid(kind: str, old: Mapping[str, Any]) -> dict[str, Any]:
        rows = {
            row: {
                col: (_pct(summaries[(kind, row, "share")]) if row != "total" else 100.0) if col == "share_pct"
                else _figure(summaries[(kind, row, col)])
                for col in cells
            }
            for row, cells in old["rows"].items()
        }
        tree = {"rows": rows, "wp_share_pct": {wp: _pct(summaries[(kind, "share", wp)]) for wp in old["wp_share_pct"]}}
        if "rates" in old:
            tree = {"rates": {b: summaries[("ls", b, "rate")] for b in old["rates"]}, **tree}
        return tree

    def summary(old: Mapping[str, Any]) -> dict[str, Any]:
        def entry(f: float, pm: float) -> dict[str, float]:
            return {"pm": _figure(pm), "pm_share_pct": _pct(pm / total_pm), "F": _figure(f), "F_share_pct": _pct(f / total_f)}

        wps = {wp: entry(summaries[("wps", wp, "F", "all", "total")], summaries[("pm", "total", wp)]) for wp in old["wps"]}
        blocks = {}
        for members in old["blocks"]:
            parts = members.split("+")
            blocks[members] = entry(
                sum(per_block(b, "F") for b in parts), sum(summaries[("pm", b, "total")] for b in parts)
            )
        return {"wps": wps, "blocks": blocks}

    def trips(old: Mapping[str, Any]) -> dict[str, float]:
        rows = travel_planner.trip_rows(inputs)
        return {n: _figure(travel_planner.trip_figures(profile, rows[n])[1]) for n in old}

    def categories(old: Mapping[str, Any]) -> dict[str, Any]:
        blocks = [b for b in old if b != "total"]
        tree = {b: {f: _figure(per_block(b, f)) for f in old[b]} for b in blocks}
        if "total" in old:
            tree["total"] = {f: _figure(sum(per_block(b, f) for b in blocks)) for f in old["total"]}
        return tree

    sections: dict[str, Callable[[Any], Any]] = {
        "trip_totals": trips,
        "transfer_view": transfer_view,
        "category_e": categories,
        "cost_categories": categories,
        "lump_sum": lambda old: grid("ls", old),
        "person_months": lambda old: grid("pm", old),
        "per_wp_summary": summary,
    }
    unknown = [s for s in previous if s not in sections]
    if unknown:
        raise ValueError(f"the maintainer cannot recompute expected-figure sections {unknown}: a human works them out")
    return {section: sections[section](old) for section, old in previous.items()}


def _differs(before: object, after: object) -> bool:
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return abs(before - after) > TOLERANCE
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return any(_differs(b, a) for b, a in zip(before, after))
    return before != after


def _previous_golden(profile_id: str, previous: str) -> dict[str, Any]:
    path = golden.transcription_path(profile_id, previous)
    if not path.is_file():
        raise ProfileNotFound(f"{profile_id} {previous} has no Golden Scenario to carry forward")
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return raw


def propose_expectations(profile_id: str, version: str, previous: str) -> ExpectationProposal:
    """The expected figures of ``previous``'s Golden Scenario, recomputed under ``version``. Writes nothing."""
    old = _previous_golden(profile_id, previous)
    profile = load_profile(profile_id, version)
    expected = _recompute(old["expected"], golden.golden_from(profile, old))
    before, after = dict(_leaves(old["expected"])), dict(_leaves(expected))
    changes = tuple(
        ExpectationChange(path, before.get(path), after.get(path))
        for path in {**before, **after}
        if _differs(before.get(path), after.get(path))
    )
    proposed = copy.deepcopy(old)
    proposed["shape"]["profile"] = {"id": profile_id, "version": version}
    proposed["worksheet"] = f"golden/{profile_id}-{version}.md"
    proposed["expected"] = expected
    return ExpectationProposal(profile_id, version, previous, changes, len(before.keys() | after.keys()), proposed)


def approve_expectations(
    profile_id: str, version: str, previous: str, *, proposal_id: str, approved_by: str, on: date | None = None
) -> tuple[Path, Path]:
    """Write ``version``'s Golden Scenario from the proposal, once the human approved it.

    Run this only on the human's explicit approval of ``propose_expectations``'s figures. ``proposal_id``
    is the id the approved proposal showed; if anything changed since, the figures differ and this refuses.
    It writes the transcription and a worksheet recording the approval, and never overwrites a Golden Scenario.
    """
    if not approved_by.strip():
        raise ValueError("an approval names who approved it")
    on = on or date.today()
    transcription = golden.transcription_path(profile_id, version)
    worksheet = golden.WORKSHEET_DIR / f"{profile_id}-{version}.md"
    for path in (transcription, worksheet):
        if path.exists():
            raise FileExistsError(f"{path.name} already exists: a Golden Scenario is never overwritten")
    proposal = propose_expectations(profile_id, version, previous)
    if proposal.proposal_id != proposal_id:
        raise ValueError(
            f"the proposal is now {proposal.proposal_id}, not the approved {proposal_id}: something changed since "
            "it was shown, so show the new proposal and ask again"
        )
    raw = proposal.golden_scenario
    raw["about"] = (
        f"Machine-readable transcription of the human-owned Golden Scenario {raw['worksheet']} (approved by "
        f"{approved_by} on {on.isoformat()}). The worksheet is the source of truth: an agent never edits an "
        "expected figure here to make a check pass. A suspected error is raised with the human."
    )
    transcription.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    worksheet.write_text(_worksheet(proposal, approved_by, on), encoding="utf-8")
    return transcription, worksheet


def _worksheet(proposal: ExpectationProposal, approved_by: str, on: date) -> str:
    profile_id, version, previous = proposal.profile_id, proposal.version, proposal.previous
    changes = (
        proposal.changes_table(previous, version) if proposal.changes
        else [f"None: every expected figure is as signed off for {previous}."]
    )
    return "\n".join([
        f"# Golden Scenario — {profile_id}, profile version {version}",
        "",
        f"**Owner:** human. **Status:** SIGNED OFF ({on.isoformat()}), approved by {approved_by} "
        f"(proposal `{proposal.proposal_id}`).",
        "",
        f"This Golden Scenario carries forward [{profile_id} {previous}]({profile_id}-{previous}.md): the same "
        f"Shape Parameters and the same Human Inputs, built under profile version {version}. The "
        "budget-profile-maintainer recomputed the expected figures with the reference model and proposed the "
        "changes below; the approver approved them as listed. Every other expected figure is as in the "
        f"{previous} worksheet.",
        "",
        "Rules for this file:",
        "",
        "- Only the human changes expected figures.",
        "- An agent never edits an expected figure to make a check pass. A suspected error is raised with the human.",
        "",
        "## Expected figures changed from " + previous,
        "",
        *changes,
        "",
    ])


# check and acceptance


def check_version(profile_id: str, version: str, out_dir: str | Path) -> SyntheticCheckReport:
    """Run the Synthetic Check for ``version`` at its Golden Scenario's own Shape Parameters.

    Needs Excel. Writes the report into ``out_dir`` and keeps no workbook. Raises NotAccepted when the
    version has no Golden Scenario, SyntheticCheckFailed (after writing the report) when the check fails.
    """
    gold = golden.load_golden(load_profile(profile_id, version))
    if gold is None:
        raise NotAccepted(_no_golden(profile_id, version))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    workbook = out / f"golden-check-{profile_id}-{version}.xlsx"
    try:
        report = build(gold.shape_parameters, workbook, synthetic_check=True).synthetic_check
    except SyntheticCheckFailed as failed:
        (out / CHECK_REPORT).write_text(failed.report.to_markdown(), encoding="utf-8")
        raise
    finally:
        workbook.unlink(missing_ok=True)
    assert report is not None
    (out / CHECK_REPORT).write_text(report.to_markdown(), encoding="utf-8")
    return report


def _no_golden(profile_id: str, version: str) -> str:
    return f"{profile_id} {version} has no Golden Scenario: the human approves its expected figures first"


def acceptance_problems(profile_id: str, version: str) -> list[str]:
    """Why ``version`` cannot be accepted, before any check is run; empty when it can be checked."""
    if is_accepted(profile_id, version):
        return [f"{profile_id} {version} is already accepted"]
    problems = immutability_problems() + source_document_problems(profile_id, version)
    if not golden.transcription_path(profile_id, version).is_file():
        problems.append(_no_golden(profile_id, version))
    return problems


def accept_version(profile_id: str, version: str, out_dir: str | Path, *, on: date | None = None) -> SyntheticCheckReport:
    """Accept ``version`` if nothing stands in its way and it passes the Synthetic Check against its own
    Golden Scenario's signed-off figures. Run only on the human's approval of the diff and the check.

    Raises NotAccepted or SyntheticCheckFailed, and accepts nothing, otherwise.
    """
    problems = acceptance_problems(profile_id, version)
    if problems:
        raise NotAccepted(f"{profile_id} {version} not accepted:\n- " + "\n- ".join(problems))
    report = check_version(profile_id, version, out_dir)
    if not report.human_owned or report.pinned_figures == 0:
        raise NotAccepted(f"{profile_id} {version} not accepted: the check was not run against the signed-off figures")
    _register(profile_id, version, on or date.today())
    return report

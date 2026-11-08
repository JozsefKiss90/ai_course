"""The Synthetic Check: verify a freshly built workbook on a disposable, synthetically filled copy.

1. Copy the blank workbook to a fresh temporary directory outside the deliverable's directory.
2. Open the copy read-only in real Excel via COM and type the scenario into its Human Input cells.
   Then add the scenario's Table rows (e.g. a late partner, another trip), as a human would.
3. Recalculate and read the Transfer Views, Check Summaries and Checks panel back; Excel closes the copy
   without saving.
4. Compare with the reference model, which works from the scenario inputs alone. With the Golden
   Scenario at its own Shape Parameters, compare its signed-off figures too: with the workbook, and
   with the reference model, so a mistake model and workbook share still fails.

The scenario is the profile version's Golden Scenario (``verify/golden.py``), scaled to the build's
Shape Parameters where they differ; only a profile version without one falls back to the provisional
scenario.

The copy is deleted afterwards, also on failure, and the deletion is verified. The deliverable
itself is never opened by Excel or re-saved.
"""

from __future__ import annotations

import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from budget_engine.layout import Cell, Key
from budget_engine.verify.excel import recalculate_and_read
from budget_engine.verify.reference import expected_check_summaries, expected_guards, expected_names, expected_transfer_view
from budget_engine.verify.golden import synthetic_scenario
from budget_engine.verify.scenario import Scenario

if TYPE_CHECKING:
    from budget_engine.build import BuildResult

TOLERANCE = 0.005  # half a cent
REFERENCE_MODEL = "(reference model)"  # location of a figure where the reference model leaves the Golden Scenario


class CopyNotDeleted(RuntimeError):
    """The disposable copy could not be deleted; a filled synthetic workbook is left on disk."""


@dataclass(frozen=True)
class Mismatch:
    figure: str  # semantic name, e.g. "BE1 WP2 A1_senior items"
    location: str  # 'Transfer View BE1'!B7
    expected: float | str | None
    actual: object
    difference: float | None


@dataclass(frozen=True)
class SyntheticCheckReport:
    workbook: str
    scenario: str
    scenario_provenance: str
    human_owned: bool
    figures: tuple[str, ...]  # semantic names of every figure compared
    table_rows_added: tuple[str, ...]
    mismatches: tuple[Mismatch, ...]
    copy_path: Path
    copy_deleted: bool
    checks_panel: tuple[tuple[str, object], ...] = ()  # (guard id, status read back), "overall" last
    pinned_figures: int = 0  # figures also compared with the Golden Scenario's signed-off ones
    ownership: str = ""  # how the report describes the scenario; empty: from human_owned

    @property
    def figures_compared(self) -> int:
        return len(self.figures)

    @property
    def passed(self) -> bool:
        return self.figures_compared > 0 and not self.mismatches and self.copy_deleted

    def to_markdown(self) -> str:
        ownership = self.ownership or (
            "human-owned Golden Scenario" if self.human_owned else "PROVISIONAL, not human-owned"
        )
        lines = [
            "# Synthetic Check report",
            "",
            f"- Result: **{'PASS' if self.passed else 'FAIL'}**",
            f"- Workbook: {self.workbook}",
            f"- Scenario: {self.scenario} ({ownership})",
            f"- {self.scenario_provenance}",
            f"- Table rows added after the build: {', '.join(self.table_rows_added) or 'none'}",
            f"- Figures compared: {self.figures_compared}",
            *([f"- Figures pinned to the Golden Scenario: {self.pinned_figures}"] if self.pinned_figures else []),
            f"- Differing figures: {len(self.mismatches)}",
            f"- Disposable copy deleted: {'yes' if self.copy_deleted else 'NO'}",
        ]
        if self.checks_panel:
            panel = ", ".join(f"{guard} {status}" for guard, status in self.checks_panel)
            lines.append(f"- Checks panel after the synthetic fill: {panel}")
        if self.mismatches:
            lines += [
                "",
                "| Figure | Location | Expected | Actual | Difference |",
                "|---|---|---:|---:|---:|",
            ]
            for m in self.mismatches:
                lines.append(
                    f"| {m.figure} | {m.location} | {_fmt(m.expected)} | {_fmt(m.actual)} | {_fmt(m.difference)} |"
                )
        return "\n".join(lines) + "\n"


def _fmt(value: object) -> str:
    if value is None:
        return "(none)"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)


def run_synthetic_check(result: BuildResult, scenario: Scenario | None = None) -> SyntheticCheckReport:
    """Run the Synthetic Check on a freshly built workbook and return its report."""
    if scenario is None:
        scenario = synthetic_scenario(result.profile, result.shape, result.layout)
    missing = set(result.layout.inputs) - set(scenario.inputs)
    if missing:
        raise ValueError(f"scenario {scenario.name!r} has no value for {sorted(missing)[:5]}")
    fill = {result.layout.inputs[k]: v for k, v in scenario.inputs.items() if v is not None}  # None: left blank
    entries = {**scenario.inputs, **scenario.added_inputs}
    tv = expected_transfer_view(result.profile, result.shape, entries)
    summaries = expected_check_summaries(result.profile, result.shape, entries, tv)
    expected: dict[Key, float | str] = {
        **tv,
        **summaries,
        **expected_guards(result.profile, result.shape, entries, summaries),
        **expected_names(result.shape, scenario.inputs, scenario.added_inputs),
    }
    drift = _drift(scenario.pinned, expected)
    expected |= scenario.pinned  # the workbook answers to the signed-off figures where there are some
    outputs = result.layout.outputs

    workdir = Path(tempfile.mkdtemp(prefix="synthetic-check-"))
    copy = workdir / f"synthetic-{result.path.name}"
    try:
        if result.path.parent.resolve() in (workdir.resolve(), *workdir.resolve().parents):
            raise RuntimeError(f"the disposable copy would sit inside the deliverable's directory ({workdir})")
        shutil.copyfile(result.path, copy)
        actual = recalculate_and_read(copy, fill, outputs.values(), scenario.table_rows)
    finally:
        _delete(workdir)
    keys = sorted(expected.keys() | outputs.keys())
    return SyntheticCheckReport(
        workbook=result.path.name,
        scenario=scenario.name,
        scenario_provenance=scenario.provenance,
        human_owned=scenario.human_owned,
        figures=tuple(_figure_name(k) for k in keys),
        table_rows_added=tuple(r.description for r in scenario.late_rows),
        mismatches=(*drift, *_compare(keys, expected, outputs, actual)),
        copy_path=copy,
        copy_deleted=not workdir.exists(),
        checks_panel=tuple(
            (key[1], actual.get(cell)) for key, cell in outputs.items() if key[0] == "guard" and key[2] == "status"
        ),
        pinned_figures=len(scenario.pinned),
        ownership=scenario.ownership,
    )


def _drift(pinned: dict[Key, float], model: dict[Key, float | str]) -> list[Mismatch]:
    """Signed-off figures the reference model does not reproduce."""
    mismatches = []
    for key, want in sorted(pinned.items()):
        got = model.get(key)
        diff = got - want if isinstance(got, float) else None
        if diff is None or abs(diff) > TOLERANCE:
            mismatches.append(Mismatch(_figure_name(key), REFERENCE_MODEL, want, got, diff))
    return mismatches


def _figure_name(key: Key) -> str:
    """E.g. "BE1 WP2 A1_senior items" for a Transfer View figure, "ls BE1 WP2" for a Check Summary one."""
    return " ".join(key[1:] if key[0] == "tv" else key)


def _compare(
    keys: list[Key], expected: dict[Key, float | str], outputs: dict[Key, Cell], actual: dict[Cell, object]
) -> list[Mismatch]:
    mismatches = []
    for key in keys:
        want = expected.get(key)
        cell = outputs.get(key)
        location = f"'{cell.sheet}'!{cell.coord}" if cell else "(not in the workbook)"
        got = actual.get(cell) if cell else None
        if isinstance(want, str):  # text, e.g. a name looked up from a Reference List
            if got != want:
                mismatches.append(Mismatch(_figure_name(key), location, want, got, None))
            continue
        # Excel numbers come back as floats; blanks, text and cell errors never match a figure.
        diff = got - want if want is not None and isinstance(got, float) else None
        if diff is not None and abs(diff) <= TOLERANCE:
            continue
        mismatches.append(Mismatch(_figure_name(key), location, want, got, diff))
    return mismatches


def _delete(workdir: Path) -> None:
    """Delete the copy's directory; Excel can hold the file briefly after quitting, so retry."""
    for attempt in range(10):
        shutil.rmtree(workdir, ignore_errors=True)
        if not workdir.exists():
            return
        time.sleep(0.2 * (attempt + 1))
    raise CopyNotDeleted(f"could not delete the disposable Synthetic Check copy in {workdir}")

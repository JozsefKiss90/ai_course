"""The Handover Package: what a human receives from a build.

A package is a directory holding the blank Planning Workbook, the Synthetic Check report and the
fill-in guide, plus the re-paste guide on a rebuild. It is assembled only after the workbook passed
its structural checks and its Synthetic Check (``build(..., synthetic_check=True)``, which also
confirms the deliverable is byte for byte what was built). When the Synthetic Check fails, the directory receives the failure report
and nothing else: the build has already deleted the workbook, and no guide is written for it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from budget_engine.build import BuildResult, SyntheticCheckFailed, build
from budget_engine.guide import fill_in_guide
from budget_engine.repaste import compare, input_layout, parse_rebuild

WORKBOOK = "planning-workbook.xlsx"
REPORT = "synthetic-check-report.md"
GUIDE = "fill-in-guide.md"
REPASTE_GUIDE = "re-paste-guide.md"


@dataclass(frozen=True)
class HandoverPackage:
    directory: Path
    workbook: Path
    report: Path
    guide: Path
    build: BuildResult
    repaste_guide: Path | None = None  # on a rebuild only


def deliver(shape_parameters: Mapping[str, Any], directory: str | Path) -> HandoverPackage:
    """Build a Planning Workbook, verify it, and assemble its Handover Package in ``directory``.

    The directory must be new or empty, so no file of an earlier package can pass for part of this
    one. Raises ShapeError and BuildError as ``build`` does; on SyntheticCheckFailed the directory
    holds only the failure report.
    """
    out = Path(directory)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError(f"a Handover Package goes into a new or empty directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    try:
        result = build(shape_parameters, out / WORKBOOK, synthetic_check=True)
    except SyntheticCheckFailed as failed:
        (out / REPORT).write_text(failed.report.to_markdown(), encoding="utf-8")
        raise
    assert result.synthetic_check is not None and result.synthetic_check.passed
    report = out / REPORT
    report.write_text(result.synthetic_check.to_markdown(), encoding="utf-8")
    guide = out / GUIDE
    guide.write_text(fill_in_guide(result), encoding="utf-8")
    return HandoverPackage(directory=out, workbook=result.path, report=report, guide=guide, build=result)


def rebuild(old_shape_parameters: Mapping[str, Any], new_shape_parameters: Mapping[str, Any], directory: str | Path) -> HandoverPackage:
    """Deliver a fresh Planning Workbook for the new Shape Parameters, with a re-paste guide from the old ones.

    The old workbook is never asked for or opened: the guide compares the input layouts both sets of
    Shape Parameters produce. The new Shape Parameters keep the old Funding Profile version (filled
    in when they leave it out). Both are checked before anything is written; otherwise this raises
    and delivers as ``deliver`` does, and writes the re-paste guide only into a delivered package.
    """
    old_shape, _, new_raw, profile = parse_rebuild(old_shape_parameters, new_shape_parameters)
    old_layout = input_layout(old_shape, profile)
    package = deliver(new_raw, directory)
    built = package.build
    plan = compare(profile, old_shape, built.shape, old_layout, built.layout)
    guide = package.directory / REPASTE_GUIDE
    guide.write_text(plan.to_markdown(), encoding="utf-8")
    return replace(package, repaste_guide=guide)

"""The Handover Package: what a human receives from a build.

A package is a directory holding the blank Planning Workbook, the Synthetic Check report and the
fill-in guide. It is assembled only after the workbook passed its structural checks and its
Synthetic Check (``build(..., synthetic_check=True)``, which also confirms the deliverable is byte
for byte what was built). When the Synthetic Check fails, the directory receives the failure report
and nothing else: the build has already deleted the workbook, and no guide is written for it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from budget_engine.build import BuildResult, SyntheticCheckFailed, build
from budget_engine.guide import fill_in_guide

WORKBOOK = "planning-workbook.xlsx"
REPORT = "synthetic-check-report.md"
GUIDE = "fill-in-guide.md"


@dataclass(frozen=True)
class HandoverPackage:
    directory: Path
    workbook: Path
    report: Path
    guide: Path
    build: BuildResult


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

"""The build entry point: Funding Profile version + Shape Parameters -> blank Planning Workbook."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from budget_engine.layout import BuildContext, Layout
from budget_engine.methods import CATALOGUE
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, parse_shape
from budget_engine.sheets import (
    check_summaries, constants, cover, fill_in_order, input_guards, rate_table, reference_lists, task_list, transfer_view,
    validation,
)
from budget_engine.verify.structural import check_structure
from budget_engine.verify.synthetic import SyntheticCheckReport, run_synthetic_check


class BuildError(RuntimeError):
    """The generated workbook failed its checks and was not delivered."""


class SyntheticCheckFailed(BuildError):
    """The Synthetic Check found differing figures; the workbook was deleted, not delivered."""

    def __init__(self, report: SyntheticCheckReport) -> None:
        super().__init__("Synthetic Check failed:\n" + report.to_markdown())
        self.report = report


@dataclass(frozen=True)
class BuildResult:
    path: Path
    profile: Profile
    shape: ShapeParameters
    layout: Layout
    sheets: tuple[str, ...]  # in workbook order
    fill_in_order: tuple[str, ...]  # the steps listed on the Cover Sheet
    synthetic_check: SyntheticCheckReport | None = None


def build(
    shape_parameters: Mapping[str, Any], out_path: str | Path, *, synthetic_check: bool = False
) -> BuildResult:
    """Generate a blank Planning Workbook at ``out_path`` and run the structural checks on it.

    With ``synthetic_check``, also run the Synthetic Check (needs Excel) and attach its report.
    Without it the workbook is generated but unverified: anything that delivers a workbook (the
    Handover Package, the budget-planner skill) must build with ``synthetic_check=True``.

    Raises ShapeError for any input outside the Shape Parameters contract, and BuildError (after
    deleting the file) if the structural checks fail; SyntheticCheckFailed if the Synthetic Check does.
    """
    shape, profile = parse_shape(shape_parameters)
    out = Path(out_path)
    if out.suffix.lower() != ".xlsx":
        raise ValueError(f"a Planning Workbook is an .xlsx file, got {out.name}")

    wb = Workbook()
    ctx = BuildContext(profile=profile, shape=shape, wb=wb)
    cover_ws = wb.active
    assert cover_ws is not None
    cover_ws.title = cover.SHEET

    reference_lists.build_be_list(ctx)
    reference_lists.build_wp_list(ctx)
    if shape.tasks is not None:
        task_list.build_task_list(ctx)
    constants.build_constants(ctx)
    reference_lists.build_country_list(ctx)
    input_guards.build_thresholds(ctx)
    rate_table.build_rate_table(ctx)
    for method_id in shape.methods:
        CATALOGUE[method_id].build(ctx)
    transfer_view.build_transfer_views(ctx)
    check_summaries.build_check_summaries(ctx)
    guards = input_guards.build_input_guards(ctx)

    steps = fill_in_order.steps(wb, ctx.layout, {
        reference_lists_sheet(profile, "be_list"): "names, acronyms, countries and funding rates",
        reference_lists_sheet(profile, "wp_list"): "work package names",
    })
    cover.build_cover(ctx, cover_ws, steps, date.today(), guards)
    _clear_personal_metadata(wb)

    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    validation.write_ext_validations(out, ctx.ext_validations)

    problems = check_structure(out, shape, profile, ctx.layout)
    if problems:
        out.unlink()
        raise BuildError("structural checks failed:\n- " + "\n- ".join(problems))
    result = BuildResult(
        path=out, profile=profile, shape=shape, layout=ctx.layout, sheets=tuple(wb.sheetnames), fill_in_order=tuple(steps)
    )
    if not synthetic_check:
        return result
    before = _digest(out)
    try:
        report = run_synthetic_check(result)
    except BaseException:
        out.unlink()  # no workbook is delivered without a completed check
        raise
    if not report.passed:
        out.unlink()
        raise SyntheticCheckFailed(report)
    # The check worked on a copy: the deliverable must be byte for byte what was built, so no
    # synthetic value can have reached it. The structural checks confirm it once more.
    problems = [] if _digest(out) == before else ["the workbook changed during the Synthetic Check"]
    problems += check_structure(out, shape, profile, ctx.layout)
    if problems:
        out.unlink()
        raise BuildError("checks after the Synthetic Check failed:\n- " + "\n- ".join(problems))
    return replace(result, synthetic_check=report)


def reference_lists_sheet(profile: Profile, which: str) -> str:
    return str(profile.reference_lists[which]["sheet"])


def _clear_personal_metadata(wb: Workbook) -> None:
    props = wb.properties
    props.creator = ""  # openpyxl writes "openpyxl" when this is None
    props.lastModifiedBy = None
    props.title = None
    props.subject = None
    props.description = None
    props.keywords = None
    props.category = None
    props.contentStatus = None
    props.identifier = None
    props.lastPrinted = None


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

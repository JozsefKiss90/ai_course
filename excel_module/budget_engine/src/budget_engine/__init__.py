"""Budget templating engine: builds blank, project-specific Planning Workbooks."""

from budget_engine.build import BuildError, BuildResult, SyntheticCheckFailed, build
from budget_engine.guide import fill_in_guide
from budget_engine.handover import HandoverPackage, deliver
from budget_engine.shape import ShapeError, ShapeParameters
from budget_engine.verify.structural import check_structure
from budget_engine.verify.synthetic import SyntheticCheckReport, run_synthetic_check

__all__ = [
    "BuildError",
    "BuildResult",
    "HandoverPackage",
    "ShapeError",
    "ShapeParameters",
    "SyntheticCheckFailed",
    "SyntheticCheckReport",
    "build",
    "check_structure",
    "deliver",
    "fill_in_guide",
    "run_synthetic_check",
]

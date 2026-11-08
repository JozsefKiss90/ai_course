"""Budget templating engine: builds blank, project-specific Planning Workbooks."""

from budget_engine.build import BuildError, BuildResult, SyntheticCheckFailed, build
from budget_engine.shape import ShapeError, ShapeParameters
from budget_engine.verify.structural import check_structure
from budget_engine.verify.synthetic import SyntheticCheckReport, run_synthetic_check

__all__ = [
    "BuildError",
    "BuildResult",
    "ShapeError",
    "ShapeParameters",
    "SyntheticCheckFailed",
    "SyntheticCheckReport",
    "build",
    "check_structure",
    "run_synthetic_check",
]

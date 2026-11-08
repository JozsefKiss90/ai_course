"""The Estimation Method catalogue, one module per method."""

from __future__ import annotations

from typing import cast

from budget_engine.methods import staff_effort
from budget_engine.methods.base import EstimationMethod, Figures

CATALOGUE: dict[str, EstimationMethod] = {
    staff_effort.ID: cast(EstimationMethod, staff_effort),
}

__all__ = ["CATALOGUE", "EstimationMethod", "Figures"]

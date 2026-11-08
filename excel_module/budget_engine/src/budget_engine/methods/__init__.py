"""The Estimation Method catalogue, one module per method."""

from __future__ import annotations

from typing import cast

from budget_engine.methods import equipment_depreciation, itemised_list, staff_effort, travel_planner
from budget_engine.methods.base import EstimationMethod, Figures

CATALOGUE: dict[str, EstimationMethod] = {
    staff_effort.ID: cast(EstimationMethod, staff_effort),
    travel_planner.ID: cast(EstimationMethod, travel_planner),
    equipment_depreciation.ID: cast(EstimationMethod, equipment_depreciation),
    itemised_list.ID: cast(EstimationMethod, itemised_list),
}

__all__ = ["CATALOGUE", "EstimationMethod", "Figures"]

"""The Estimation Method contract.

Every method module exposes:
- ``ID``: its catalogue id; ``SHEET``: the sheet it writes
- ``build(ctx)``: writes its sheet and appends a Contribution per BE × WP × cost line
- ``reference(profile, shape, inputs)``: the same figures computed from the inputs alone,
  for the Synthetic Check's reference model
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol

from budget_engine.layout import BuildContext, Key
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters

# (BE, WP, cost line) -> (items, total)
Figures = dict[tuple[str, str, str], tuple[float, float]]


def number(inputs: Mapping[Key, object], key: Key) -> float:
    """A numeric Human Input; blank (or non-numeric) counts as zero, as it does in Excel."""
    value = inputs.get(key)
    return float(value) if isinstance(value, (int, float)) else 0.0


class EstimationMethod(Protocol):
    ID: str
    SHEET: str
    build: Callable[[BuildContext], None]
    reference: Callable[[Profile, ShapeParameters, Mapping[Key, object]], Figures]

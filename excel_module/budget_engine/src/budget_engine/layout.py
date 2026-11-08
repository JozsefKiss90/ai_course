"""Where things live in a Planning Workbook.

The Layout is filled in by the sheet builders as they write, and is the contract the rest of
the engine reads: the Synthetic Check fills Human Inputs at ``inputs`` and reads results back
from ``outputs``. Keys are semantic, e.g. ``("rate", "BE1", "A1_senior")``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from openpyxl import Workbook

from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters

Key = tuple[str, ...]


@dataclass(frozen=True)
class Cell:
    sheet: str
    coord: str

    @property
    def column(self) -> str:
        return self.coord.rstrip("0123456789")

    @property
    def row(self) -> int:
        return int(self.coord[len(self.column):])

    @property
    def ref(self) -> str:
        """Absolute cross-sheet reference for use inside formulas."""
        return f"'{self.sheet}'!${self.column}${self.row}"


@dataclass
class Layout:
    inputs: dict[Key, Cell] = field(default_factory=dict)
    outputs: dict[Key, Cell] = field(default_factory=dict)
    constants: dict[str, Cell] = field(default_factory=dict)


@dataclass(frozen=True)
class Contribution:
    """One Estimation Method output: items and total for BE × WP × cost line."""

    be: str
    wp: str
    line: str
    items: Cell
    total: Cell


@dataclass
class BuildContext:
    profile: Profile
    shape: ShapeParameters
    wb: Workbook
    layout: Layout = field(default_factory=Layout)
    contributions: list[Contribution] = field(default_factory=list)

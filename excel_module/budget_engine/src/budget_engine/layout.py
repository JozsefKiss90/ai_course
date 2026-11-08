"""Where things live in a Planning Workbook.

The Layout is filled in by the sheet builders as they write, and is the contract the rest of
the engine reads: the Synthetic Check fills Human Inputs at ``inputs`` and reads results back
from ``outputs``. Keys are semantic, e.g. ``("rate", "BE1", "A1_senior")``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from openpyxl import Workbook
from openpyxl.utils import column_index_from_string, get_column_letter

from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_spare

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


def box(cells: list[Cell]) -> str:
    """The absolute range of a rectangular block of cells on one sheet."""
    sheets = {c.sheet for c in cells}
    rows = [c.row for c in cells]
    cols = [column_index_from_string(c.column) for c in cells]
    area = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1)
    if len(sheets) != 1 or area != len(set(cells)):
        raise ValueError(f"cells do not form one rectangular block: {sorted(sheets)}, {len(cells)} cells, area {area}")
    first, last = get_column_letter(min(cols)), get_column_letter(max(cols))
    return f"'{sheets.pop()}'!${first}${min(rows)}:${last}${max(rows)}"


@dataclass
class Layout:
    inputs: dict[Key, Cell] = field(default_factory=dict)
    outputs: dict[Key, Cell] = field(default_factory=dict)
    constants: dict[str, Cell] = field(default_factory=dict)
    # Per-BE/AE block -> formula operand for its BE/AE code: a quoted literal for a built Beneficiary
    # or AE, a reference to the Human Input where the code of a late partner goes for a spare block.
    slot_codes: dict[str, str] = field(default_factory=dict)
    # Human Inputs that take free text (names, titles, item descriptions): the only ones without a
    # data validation.
    free_text: set[Key] = field(default_factory=set)

    def slot_label(self, slot: str) -> str:
        """What a per-BE/AE row shows as its BE/AE nr: the code, or a spare block's code by formula."""
        return f'={self.slot_codes[slot]}&""' if is_spare(slot) else slot


@dataclass(frozen=True)
class Contribution:
    """One Estimation Method output: items and total for BE × WP × cost line."""

    be: str
    wp: str
    line: str
    items: Cell
    total: Cell


@dataclass(frozen=True)
class ExtValidation:
    """A list validation written as an x14 extension, which openpyxl cannot express, after the save."""

    sheet: str
    sqref: str
    source: str  # the list's range, e.g. CountryList!$A$2:$A$185


@dataclass
class BuildContext:
    profile: Profile
    shape: ShapeParameters
    wb: Workbook
    layout: Layout = field(default_factory=Layout)
    contributions: list[Contribution] = field(default_factory=list)
    ext_validations: list[ExtValidation] = field(default_factory=list)

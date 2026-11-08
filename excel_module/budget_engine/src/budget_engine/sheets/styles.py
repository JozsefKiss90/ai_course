"""Cell styling and the write helpers every sheet builder uses.

Colour legend (also shown on the Cover Sheet): Human Inputs light yellow, derived cells white.
The structural checks rely on the yellow fill to find Human Input cells.
"""

from __future__ import annotations

from collections.abc import Callable
from copy import copy
from typing import Any
from weakref import WeakKeyDictionary

from openpyxl.cell.cell import Cell as XlCell
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.cell_style import StyleArray
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Key

INPUT_RGB = "FFFFF2CC"
INPUT_FILL = PatternFill("solid", fgColor=INPUT_RGB)
DERIVED_FILL = PatternFill("solid", fgColor="FFFFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="FFD9E1F2")
THIN = Side(style="thin", color="FFBFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")

MONEY = "#,##0.00"
QUANTITY = "#,##0.00"


def is_input(cell_fill: Any) -> bool:
    """True for the Human Input fill; takes a cell's ``fill`` (a PatternFill or openpyxl's StyleProxy)."""
    return bool(cell_fill.fill_type == "solid" and cell_fill.fgColor.rgb == INPUT_RGB)


# Per workbook, the style each helper gives a fresh cell. Assigning a fill or border makes openpyxl
# hash the style objects again for every cell, which dominates the build time of large shapes;
# copying the finished style is the same result (openpyxl's copy_worksheet does likewise).
_STYLES: WeakKeyDictionary[Workbook, dict[tuple[object, ...], StyleArray]] = WeakKeyDictionary()


def _style(c: XlCell, key: tuple[object, ...], apply: Callable[[XlCell], None]) -> None:
    if c.has_style:  # already styled: keep what it has and add to it
        apply(c)
        return
    wb = c.parent.parent
    assert wb is not None
    styles = _STYLES.setdefault(wb, {})
    if key in styles:
        c._style = copy(styles[key])  # type: ignore[attr-defined]
    else:
        apply(c)
        styles[key] = copy(c._style)  # type: ignore[attr-defined]


def put_input(
    ctx: BuildContext, ws: Worksheet, coord: str, key: Key, number_format: str | None = None, *, free_text: bool = False
) -> Cell:
    """Mark an empty Human Input cell and register it in the Layout.

    Every Human Input gets a data validation from its sheet builder, except free text (names,
    titles, descriptions), which is marked with ``free_text``.
    """
    def apply(c: XlCell) -> None:
        c.fill = INPUT_FILL
        c.border = BOX
        if number_format:
            c.number_format = number_format

    _style(ws[coord], ("input", number_format), apply)
    cell = Cell(ws.title, coord)
    ctx.layout.inputs[key] = cell
    if free_text:
        ctx.layout.free_text.add(key)
    return cell


def put_derived(ws: Worksheet, coord: str, value: object, number_format: str | None = None, bold: bool = False) -> None:
    def apply(c: XlCell) -> None:
        c.fill = DERIVED_FILL
        c.border = BOX
        if number_format:
            c.number_format = number_format
        if bold:
            c.font = BOLD

    c = ws[coord]
    c.value = value
    _style(c, ("derived", number_format, bold), apply)


def put_header(ws: Worksheet, coord: str, text: str) -> None:
    c = ws[coord]
    c.value = text
    c.font = BOLD
    c.fill = HEADER_FILL
    c.border = BOX
    c.alignment = WRAP

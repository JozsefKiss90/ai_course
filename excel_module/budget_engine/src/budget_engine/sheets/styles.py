"""Cell styling and the write helpers every sheet builder uses.

Colour legend (also shown on the Cover Sheet): Human Inputs light yellow, derived cells white.
The structural checks rely on the yellow fill to find Human Input cells.
"""

from __future__ import annotations

from typing import Any

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
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


def put_input(ctx: BuildContext, ws: Worksheet, coord: str, key: Key, number_format: str | None = None) -> Cell:
    """Mark an empty Human Input cell and register it in the Layout."""
    c = ws[coord]
    c.fill = INPUT_FILL
    c.border = BOX
    if number_format:
        c.number_format = number_format
    cell = Cell(ws.title, coord)
    ctx.layout.inputs[key] = cell
    return cell


def put_derived(ws: Worksheet, coord: str, value: object, number_format: str | None = None, bold: bool = False) -> None:
    c = ws[coord]
    c.value = value
    c.fill = DERIVED_FILL
    c.border = BOX
    if number_format:
        c.number_format = number_format
    if bold:
        c.font = BOLD


def put_header(ws: Worksheet, coord: str, text: str) -> None:
    c = ws[coord]
    c.value = text
    c.font = BOLD
    c.fill = HEADER_FILL
    c.border = BOX
    c.alignment = WRAP


def name_formula(code_cell_ref: str) -> str:
    """Show a Reference List entry, or nothing while the human has not filled it."""
    return f'=IF({code_cell_ref}="","",{code_cell_ref})'

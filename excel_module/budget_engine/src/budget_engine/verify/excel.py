"""Excel via COM, used only to fill, recalculate and read back the disposable Synthetic Check copy.

The copy is opened read-only, filled in memory and closed without saving, so nothing is re-saved:
Excel calculates exactly the file the build wrote.
"""

from __future__ import annotations

import gc
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from openpyxl.utils import column_index_from_string, get_column_letter

from budget_engine.layout import Cell


class ExcelUnavailable(RuntimeError):
    """Microsoft Excel could not be started through COM."""


@dataclass(frozen=True)
class TableRowAddition:
    """A row a human adds to an Excel Table: inserted at ``position`` (1-based, within the data rows)."""

    sheet: str
    table: str
    position: int
    values: tuple[object, ...]  # one per Table column, in column order


def recalculate_and_read(
    path: Path,
    fill: Mapping[Cell, object],
    cells: Iterable[Cell],
    table_rows: Sequence[TableRowAddition] = (),
) -> dict[Cell, object]:
    """Open ``path`` read-only in a private Excel instance, type in ``fill``, add ``table_rows``,
    recalculate and read ``cells``.

    ``fill`` addresses cells as built, so it is typed in before any Table row moves cells down.
    Numbers come back as floats, blanks as None and cell errors as their text (e.g. "#REF!").
    """
    try:
        import pythoncom
        import win32com.client
    except ImportError as exc:  # pragma: no cover - non-Windows
        raise ExcelUnavailable("pywin32 is not installed; the Synthetic Check needs Excel on Windows") from exc

    by_sheet: dict[str, list[Cell]] = defaultdict(list)
    for cell in cells:
        by_sheet[cell.sheet].append(cell)

    pythoncom.CoInitialize()
    try:
        try:
            app = win32com.client.DispatchEx("Excel.Application")  # type: ignore[no-untyped-call]
        except Exception as exc:
            raise ExcelUnavailable(f"could not start Excel via COM: {exc}") from exc
        try:
            app.Visible = False
            app.DisplayAlerts = False
            app.AskToUpdateLinks = False
            wb = app.Workbooks.Open(str(path.resolve()), UpdateLinks=0, ReadOnly=True)
            try:
                for cell, value in fill.items():
                    wb.Worksheets(cell.sheet).Range(cell.coord).Value = value
                for addition in table_rows:
                    table = wb.Worksheets(addition.sheet).ListObjects(addition.table)
                    table.ListRows.Add(addition.position).Range.Value = (addition.values,)
                    del table
                app.CalculateFull()
                return {cell: value for sheet, wanted in by_sheet.items() for cell, value in _read(wb, sheet, wanted)}
            finally:
                wb.Close(SaveChanges=False)
                del wb
        finally:
            # Release every proxy we can before Quit: releasing one after Excel has gone raises a
            # first-chance RPC_E_DISCONNECTED that COM handles, but pytest's faulthandler prints.
            # The app proxy itself is released on return and can still trigger it; it is benign.
            gc.collect()
            app.Quit()
    finally:
        pythoncom.CoUninitialize()


def _read(wb: object, sheet: str, cells: list[Cell]) -> list[tuple[Cell, object]]:
    """Read one sheet's cells in a single COM call over their bounding block from A1."""
    last_row = max(c.row for c in cells)
    last_col = max(column_index_from_string(c.column) for c in cells)
    block = wb.Worksheets(sheet).Range(f"A1:{get_column_letter(last_col)}{last_row}").Value  # type: ignore[attr-defined]
    if not isinstance(block, tuple):  # a one-cell range comes back as a bare value
        block = ((block,),)
    return [(c, _from_com(block[c.row - 1][column_index_from_string(c.column) - 1])) for c in cells]


# Excel numbers always come back from COM as floats; an int is a cell error code.
COM_ERROR_CODES = {
    -2146826288: "#NULL!", -2146826281: "#DIV/0!", -2146826273: "#VALUE!", -2146826265: "#REF!",
    -2146826259: "#NAME?", -2146826252: "#NUM!", -2146826246: "#N/A",
}


def _from_com(raw: object) -> object:
    if isinstance(raw, int) and not isinstance(raw, bool):
        return COM_ERROR_CODES.get(raw, f"#ERROR({raw})")
    return raw

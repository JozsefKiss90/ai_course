"""Task List (optional): task codes under each work package, with blank titles for a human to fill.

Built only when the Shape Parameters give tasks per WP. It is an Excel Table, so a human can add a
task row; that task gets no staff effort rows until a rebuild.
"""

from __future__ import annotations

from openpyxl.worksheet.table import Table

from budget_engine.layout import BuildContext
from budget_engine.sheets.styles import TITLE, put_derived, put_header, put_input

SHEET = "Task List"
TABLE = "TaskList"
HEADERS = ("Task nr", "WP", "Task title")
HEADER_ROW = 3
FIRST_DATA_ROW = HEADER_ROW + 1


def build_task_list(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = "Task List"
    ws["A1"].font = TITLE
    ws["A2"] = "Enter each task title. Effort is planned per task on the staff effort sheet."
    for col, header in zip("ABC", HEADERS):
        put_header(ws, f"{col}{HEADER_ROW}", header)
    units = ctx.shape.effort_units
    for i, (wp, task) in enumerate(units):
        row = FIRST_DATA_ROW + i
        put_derived(ws, f"A{row}", task)
        put_derived(ws, f"B{row}", wp)
        put_input(ctx, ws, f"C{row}", ("task_title", task))
    ws.add_table(Table(displayName=TABLE, ref=f"A{HEADER_ROW}:C{FIRST_DATA_ROW + len(units) - 1}"))
    for col, width in zip("ABC", (10, 8, 70)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"

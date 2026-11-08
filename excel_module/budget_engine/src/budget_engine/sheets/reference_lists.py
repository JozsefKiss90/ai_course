"""`BE list` and `WP list`, cell for cell like the Official Budget Table's.

Only the Official Budget Table's data block is reproduced; its macro buttons are not (ADR-0002).
"""

from __future__ import annotations

from typing import Any

from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext
from budget_engine.sheets.styles import TITLE, put_derived, put_header, put_input

BE_INPUT_KEYS = ("be_name", "be_acronym", "be_country", "be_funding_rate")


def _frame(ws: Worksheet, spec: dict[str, Any]) -> None:
    ws[spec["title_cell"]] = spec["title"]
    ws[spec["title_cell"]].font = TITLE
    ws[spec["title_cell"]].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(spec["title_merge"])
    for row, height in spec["row_heights"].items():
        ws.row_dimensions[int(row)].height = height
    for i, header in enumerate(spec["headers"]):
        put_header(ws, f"{get_column_letter(i + 1)}{spec['header_row']}", header)
    for col, width in spec["column_widths"].items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{spec['first_data_row']}"


def build_be_list(ctx: BuildContext) -> None:
    spec = ctx.profile.reference_lists["be_list"]
    ws = ctx.wb.create_sheet(spec["sheet"])
    _frame(ws, spec)
    roles = spec["roles"]
    rates = DataValidation(type="list", formula1='"' + ",".join(spec["funding_rates"]) + '"', allow_blank=True)
    ws.add_data_validation(rates)
    for i, be in enumerate(ctx.shape.be_codes):
        row = spec["first_data_row"] + i
        put_derived(ws, f"A{row}", be)
        put_derived(ws, f"B{row}", roles["coordinator"] if i == 0 else roles["beneficiary"])
        for col, key in zip(spec["input_columns"], BE_INPUT_KEYS):
            put_input(ctx, ws, f"{col}{row}", (key, be), spec["number_formats"].get(col))
        rates.add(f"F{row}")


def build_wp_list(ctx: BuildContext) -> None:
    spec = ctx.profile.reference_lists["wp_list"]
    ws = ctx.wb.create_sheet(spec["sheet"])
    _frame(ws, spec)
    for i, wp in enumerate(ctx.shape.wp_codes):
        row = spec["first_data_row"] + i
        put_derived(ws, f"A{row}", wp)
        put_input(ctx, ws, f"B{row}", ("wp_name", wp), spec["number_formats"].get("B"))

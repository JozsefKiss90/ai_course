"""`BE list` and `WP list`, cell for cell like the Official Budget Table's.

Only the Official Budget Table's data block is reproduced; its macro buttons are not (ADR-0002).
Each list is an Excel Table, so a human can add a row (a late Beneficiary, an AE inserted under its
Beneficiary, another WP) and every other sheet still finds its entry: other sheets look entries up
by code through structured references, never by cell address.
"""

from __future__ import annotations

from typing import Any

from openpyxl.styles import Alignment
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext
from budget_engine.profiles import Profile
from budget_engine.shape import is_affiliated
from budget_engine.sheets.styles import TITLE, put_derived, put_header, put_input

BE_INPUT_KEYS = ("be_name", "be_acronym", "be_country", "be_funding_rate")
TABLES = {"be_list": "BEList", "wp_list": "WPList"}


def _column(spec: dict[str, Any], letter: str) -> str:
    """A Table column specifier; double brackets let headers such as "BE/AE nr" carry special characters."""
    return f"[[{spec['headers'][column_index_from_string(letter) - 1]}]]"


def column_ref(profile: Profile, which: str, column: str) -> str:
    """Structured reference to one column of a Reference List Table, e.g. ``BEList[[BE/AE nr]]``."""
    return TABLES[which] + _column(profile.reference_lists[which], column)


def lookup(profile: Profile, which: str, column: str, code: str) -> str:
    """Formula text: the entry in ``column`` of the Reference List row whose code is ``code``, or "".

    ``code`` is a formula operand: a quoted literal such as ``"BE1"`` or a cell reference.
    """
    found = f"MATCH({code},{column_ref(profile, which, 'A')},0)"
    return f'IFERROR(INDEX({column_ref(profile, which, column)},{found})&"","")'


def be_field(ctx: BuildContext, key: str, code: str) -> str:
    """Formula text for a `BE list` entry (``key`` one of BE_INPUT_KEYS) of the BE/AE with ``code``."""
    column = ctx.profile.reference_lists["be_list"]["input_columns"][BE_INPUT_KEYS.index(key)]
    return lookup(ctx.profile, "be_list", column, code)


def _add_table(ws: Worksheet, which: str, spec: dict[str, Any], rows: int) -> None:
    last_col = get_column_letter(len(spec["headers"]))
    last_row = spec["first_data_row"] + rows - 1
    ws.add_table(Table(displayName=TABLES[which], ref=f"A{spec['header_row']}:{last_col}{last_row}"))


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
    rates = DataValidation(type="list", formula1='"' + ",".join(spec["funding_rates"]) + '"', allow_blank=True)
    ws.add_data_validation(rates)
    codes = ctx.shape.entity_codes
    for i, code in enumerate(codes):
        row = spec["first_data_row"] + i
        put_derived(ws, f"A{row}", code)
        put_derived(ws, f"B{row}", role(spec, code))
        for col, key in zip(spec["input_columns"], BE_INPUT_KEYS):
            put_input(ctx, ws, f"{col}{row}", (key, code), spec["number_formats"].get(col))
        rates.add(f"F{row}")
    _add_table(ws, "be_list", spec, len(codes))


def role(spec: dict[str, Any], code: str) -> str:
    """The Official Budget Table's role for a BE/AE code: BE1 coordinates, AEs sit under their BE."""
    roles = spec["roles"]
    if is_affiliated(code):
        return str(roles["affiliated"])
    return str(roles["coordinator"] if code == "BE1" else roles["beneficiary"])


def build_wp_list(ctx: BuildContext) -> None:
    spec = ctx.profile.reference_lists["wp_list"]
    ws = ctx.wb.create_sheet(spec["sheet"])
    _frame(ws, spec)
    for i, wp in enumerate(ctx.shape.wp_codes):
        row = spec["first_data_row"] + i
        put_derived(ws, f"A{row}", wp)
        put_input(ctx, ws, f"B{row}", ("wp_name", wp), spec["number_formats"].get("B"))
    _add_table(ws, "wp_list", spec, len(ctx.shape.wp_codes))

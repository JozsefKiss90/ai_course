"""Data validation on Human Input cells: the first Input Guard, refusing impossible entries as typed.

Every validation shows Excel's error message, so an invalid entry is refused rather than merely
allowed (openpyxl's default). A list validation whose shape openpyxl cannot write faithfully, such
as the Official Budget Table's x14 Country dropdown, is added to the saved file with lxml.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from collections.abc import Iterable
from pathlib import Path

from lxml import etree
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import ExtValidation

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RELS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
X14 = "http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"
XM = "http://schemas.microsoft.com/office/excel/2006/main"
X14_VALIDATIONS_URI = "{CCE6A557-97BC-4b89-ADB6-D9C93CAAB3DF}"
ERROR_TITLE = "Not a valid entry"
PICK_FROM_LIST = "Pick an entry from the list."


def _blocking(dv: DataValidation, message: str) -> DataValidation:
    dv.showErrorMessage = True
    dv.errorStyle = "stop"
    dv.errorTitle = ERROR_TITLE
    dv.error = message
    return dv


def list_of(source: str) -> DataValidation:
    """Pick from a list: a quoted inline list or a formula such as ``INDIRECT("BEList[[BE/AE nr]]")``."""
    return _blocking(DataValidation(type="list", formula1=source, allow_blank=True), PICK_FROM_LIST)


def at_least(minimum: str, whole: bool = False) -> DataValidation:
    """A number (a whole number with ``whole``) no smaller than ``minimum``."""
    dv = DataValidation(type="whole" if whole else "decimal", operator="greaterThanOrEqual", formula1=minimum, allow_blank=True)
    return _blocking(dv, f"Enter a {'whole ' if whole else ''}number of at least {minimum}.")


def non_negative(whole: bool = False) -> DataValidation:
    return at_least("0", whole)


def between(low: str, high: str) -> DataValidation:
    dv = DataValidation(type="decimal", operator="between", formula1=low, formula2=high, allow_blank=True)
    return _blocking(dv, f"Enter a number from {low} to {high}.")


def apply(ws: Worksheet, dv: DataValidation, *ranges: str) -> None:
    ws.add_data_validation(dv)
    for cells in ranges:
        dv.add(cells)


def sheet_part(z: zipfile.ZipFile, sheet: str) -> str:
    """The package part (e.g. ``xl/worksheets/sheet2.xml``) holding ``sheet``."""
    book = etree.fromstring(z.read("xl/workbook.xml"))
    rels = etree.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = next(s.get(f"{{{RELS}}}id") for s in book.iter(f"{{{MAIN}}}sheet") if s.get("name") == sheet)
    target = str(next(r.get("Target") for r in rels if r.get("Id") == rid)).lstrip("/")
    return target if target.startswith("xl/") else f"xl/{target}"


def write_ext_validations(path: Path, validations: Iterable[ExtValidation]) -> None:
    """Add x14 list validations to the saved workbook at ``path``, in place."""
    by_sheet: dict[str, list[ExtValidation]] = {}
    for v in validations:
        by_sheet.setdefault(v.sheet, []).append(v)
    if not by_sheet:
        return
    with zipfile.ZipFile(path) as z:
        parts = {sheet_part(z, sheet): items for sheet, items in by_sheet.items()}
        entries = [(info, z.read(info)) for info in z.infolist()]
    fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=path.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
            for info, data in entries:
                if info.filename in parts:
                    data = _with_ext_validations(data, parts[info.filename])
                out.writestr(info, data)
        shutil.move(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _with_ext_validations(xml: bytes, validations: list[ExtValidation]) -> bytes:
    root = etree.fromstring(xml)
    ext_lst = root.find(f"{{{MAIN}}}extLst")
    if ext_lst is None:
        ext_lst = etree.SubElement(root, f"{{{MAIN}}}extLst")  # extLst is a worksheet's last child
    ext = etree.SubElement(ext_lst, f"{{{MAIN}}}ext", nsmap={"x14": X14})
    ext.set("uri", X14_VALIDATIONS_URI)
    group = etree.SubElement(ext, f"{{{X14}}}dataValidations", nsmap={"xm": XM})
    group.set("count", str(len(validations)))
    for v in validations:
        dv = etree.SubElement(group, f"{{{X14}}}dataValidation")
        for name, value in (
            ("type", "list"), ("allowBlank", "1"), ("showInputMessage", "1"), ("showErrorMessage", "1"),
            ("errorTitle", ERROR_TITLE), ("error", PICK_FROM_LIST),
        ):
            dv.set(name, value)
        etree.SubElement(etree.SubElement(dv, f"{{{X14}}}formula1"), f"{{{XM}}}f").text = v.source
        etree.SubElement(dv, f"{{{XM}}}sqref").text = v.sqref
    return bytes(etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True))

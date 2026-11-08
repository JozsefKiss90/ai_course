"""The Submission Budget's breakdown rows, written in the profile's order.

The Transfer View and the Check Summaries' summary per WP share this: headings, cost lines, totals,
indirect costs and the grand total, all from the profile's ``transfer_view.rows``. The caller fills
the cost lines; the totals are written here by the profile's row rules, in each total column.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext
from budget_engine.profiles import LayoutRow
from budget_engine.sheets.styles import BOLD, MONEY, put_derived

TOTAL_KINDS = ("total", "indirect", "grand_total")  # rows whose figure the profile's rules compute

# Writes one cost line's figures at the given row; returns False when nothing fills the line.
LineWriter = Callable[[LayoutRow, int], bool]


def write_breakdown(
    ctx: BuildContext, ws: Worksheet, row: int, total_columns: Sequence[str], write_line: LineWriter
) -> tuple[int, dict[str, int]]:
    """Write every breakdown row from ``row``; return the next free row and the row of each filled
    cost line and each total (by row id). Totals only add up filled lines."""
    rows: dict[str, int] = {}
    groups: dict[str, str] = {}  # filled line id -> its cost category

    def total_of(sum_groups: tuple[str, ...], col: str) -> str:
        cells = [f"{col}{rows[i]}" for i, g in groups.items() if g in sum_groups]
        return f"SUM({','.join(cells)})" if cells else "0"

    for spec in ctx.profile.transfer_view_rows:
        if spec.kind == "blank":
            row += 1
            continue
        if spec.label:
            ws[f"A{row}"] = spec.label
        if spec.kind == "heading":
            ws[f"A{row}"].font = BOLD
        elif spec.kind == "line":
            if write_line(spec, row):
                rows[spec.id] = row
                groups[spec.id] = spec.group
        else:
            for col in total_columns:
                if spec.kind == "total":
                    formula = "=" + total_of(spec.sum_groups, col)
                elif spec.kind == "indirect":
                    rule = ctx.profile.indirect_rule
                    rate = ctx.layout.constants[rule.rate_constant].ref
                    formula = f"={total_of(rule.base_groups, col)}*{rate}"
                elif spec.kind == "grand_total":
                    formula = "=" + "+".join(f"{col}{rows[i]}" for i in spec.add)
                else:
                    raise ValueError(f"unknown Submission Budget row kind {spec.kind!r}")
                put_derived(ws, f"{col}{row}", formula, MONEY, bold=True)
            ws[f"A{row}"].font = BOLD
            rows[spec.id] = row
        row += 1
    return row, rows

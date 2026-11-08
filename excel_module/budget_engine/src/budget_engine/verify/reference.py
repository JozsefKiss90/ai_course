"""The reference model: expected Transfer View figures from the Human Inputs alone.

It never reads a workbook formula. Cost lines come from each switched-on Estimation Method's own
reference function; totals, indirect costs and the grand total come from the profile's row rules.
"""

from __future__ import annotations

from collections.abc import Mapping

from budget_engine.layout import Key
from budget_engine.methods import CATALOGUE, Figures
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters


def method_figures(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """(BE, WP, cost line) -> (items, total), summed over every switched-on Estimation Method."""
    combined: Figures = {}
    for method_id in shape.methods:
        for line, (items, total) in CATALOGUE[method_id].reference(profile, shape, inputs).items():
            prev_items, prev_total = combined.get(line, (0.0, 0.0))
            combined[line] = (prev_items + items, prev_total + total)
    return combined


def expected_transfer_view(
    profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]
) -> dict[Key, float]:
    """Expected figures keyed like ``Layout.outputs``: ("tv", BE, WP, row id, items|avg|total)."""
    figures = method_figures(profile, shape, inputs)
    expected: dict[Key, float] = {}
    for be in shape.be_codes:
        for wp in shape.wp_codes:
            group_totals: dict[str, float] = {}
            row_totals: dict[str, float] = {}
            for spec in profile.transfer_view_rows:
                if spec.kind == "line":
                    if (be, wp, spec.id) not in figures:
                        continue  # no switched-on method fills this line: it stays blank
                    items, total = figures[(be, wp, spec.id)]
                    expected[("tv", be, wp, spec.id, "items")] = items
                    expected[("tv", be, wp, spec.id, "avg")] = total / items if items > 0 else 0.0
                    expected[("tv", be, wp, spec.id, "total")] = total
                    group_totals[spec.group] = group_totals.get(spec.group, 0.0) + total
                    continue
                if spec.kind == "total":
                    value = sum(group_totals.get(g, 0.0) for g in spec.sum_groups)
                elif spec.kind == "indirect":
                    rule = profile.indirect_rule
                    base = sum(group_totals.get(g, 0.0) for g in rule.base_groups)
                    value = base * profile.constant(rule.rate_constant).value
                elif spec.kind == "grand_total":
                    value = sum(row_totals[i] for i in spec.add)
                elif spec.kind in ("heading", "blank"):
                    continue  # no figure
                else:
                    raise ValueError(f"the reference model has no rule for Transfer View row kind {spec.kind!r}")
                row_totals[spec.id] = value
                expected[("tv", be, wp, spec.id, "total")] = value
    return expected

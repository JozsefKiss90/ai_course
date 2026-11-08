"""The reference model: expected Transfer View and Check Summary figures from the Human Inputs alone.

It never reads a workbook formula. Cost lines come from each switched-on Estimation Method's own
reference function; totals, indirect costs and the grand total come from the profile's row rules.
The Check Summaries add the expected Transfer Views up, with the funding rates from the inputs.
"""

from __future__ import annotations

from collections.abc import Mapping

from budget_engine.layout import Key
from budget_engine.methods import CATALOGUE, Figures
from budget_engine.methods.base import number
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_affiliated, is_spare
from budget_engine.sheets.breakdown import TOTAL_KINDS
from budget_engine.sheets.check_summaries import PARTS


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
    """Expected figures keyed like ``Layout.outputs``: ("tv", BE/AE block, WP, row id, items|avg|total)."""
    figures = method_figures(profile, shape, inputs)
    expected: dict[Key, float] = {}
    for be in shape.slots:
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


def expected_names(
    shape: ShapeParameters, inputs: Mapping[Key, object], added: Mapping[Key, object]
) -> dict[Key, str]:
    """The name each Transfer View shows, keyed ("tv", block, "name"): the `BE list` name of the BE/AE
    whose code the block carries. ``added`` holds entries of rows added to the `BE list` Table."""
    entries = {**inputs, **added}
    expected: dict[Key, str] = {}
    for slot in shape.slots:
        code = entries.get(("slot_code", slot)) if is_spare(slot) else slot
        name = entries.get(("be_name", str(code))) if code else None
        expected[("tv", slot, "name")] = "" if name is None else str(name)
    return expected


def _codes(shape: ShapeParameters, entries: Mapping[Key, object]) -> dict[str, str | None]:
    """The BE/AE code each block carries: its own, or the one typed in for a spare block (None: blank)."""
    codes: dict[str, str | None] = {}
    for slot in shape.slots:
        code = entries.get(("slot_code", slot)) if is_spare(slot) else slot
        codes[slot] = str(code) if code else None
    return codes


def expected_check_summaries(
    profile: Profile, shape: ShapeParameters, entries: Mapping[Key, object], tv: Mapping[Key, float]
) -> dict[Key, float]:
    """Expected Check Summary figures keyed like ``Layout.outputs``, from the expected Transfer Views
    ``tv`` and the inputs (with the entries of added Table rows) in ``entries``."""
    codes = _codes(shape, entries)
    rates = {slot: number(entries, ("be_funding_rate", code)) if code else 0.0 for slot, code in codes.items()}
    of_row = profile.check_summaries["lump_sum"]["of_row"]
    effort_groups = profile.check_summaries["effort"]["groups"]
    effort = [r.id for r in profile.transfer_view_rows if r.kind == "line" and r.group in effort_groups]
    expected: dict[Key, float] = {("ls", slot, "rate"): rate for slot, rate in rates.items()}
    grids = {
        "ls": {
            (s, wp): tv.get(("tv", s, wp, of_row, "total"), 0.0) * rates[s]
            for s in shape.slots for wp in shape.wp_codes
        },
        "pm": {
            (s, wp): sum(tv.get(("tv", s, wp, line, "items"), 0.0) for line in effort)
            for s in shape.slots for wp in shape.wp_codes
        },
    }
    for kind, cells in grids.items():
        expected.update(_grid(kind, shape, cells))

    # A spare block counts as an AE when the code typed in for it is an AE code.
    part = {slot: "ae" if code and is_affiliated(code) else "be" for slot, code in codes.items()}
    for block, wps in [*((wp, [wp]) for wp in shape.wp_codes), ("all", shape.wp_codes)]:
        for spec in profile.transfer_view_rows:
            if spec.kind == "line":
                sums = {p: [0.0, 0.0] for p in PARTS}  # items, total
                present = False
                for slot in shape.slots:
                    for wp in wps:
                        if ("tv", slot, wp, spec.id, "items") not in tv:
                            continue
                        present = True
                        for p in (part[slot], "all"):
                            sums[p][0] += tv[("tv", slot, wp, spec.id, "items")]
                            sums[p][1] += tv[("tv", slot, wp, spec.id, "total")]
                if not present:
                    continue  # no switched-on method fills this line: it stays blank
                for p, (items, total) in sums.items():
                    expected[("wps", block, spec.id, p, "items")] = items
                    expected[("wps", block, spec.id, p, "avg")] = total / items if items > 0 else 0.0
                    expected[("wps", block, spec.id, p, "total")] = total
            elif spec.kind in TOTAL_KINDS:
                for p in PARTS:
                    expected[("wps", block, spec.id, p, "total")] = sum(
                        tv[("tv", slot, wp, spec.id, "total")]
                        for slot in shape.slots if p in (part[slot], "all") for wp in wps
                    )
    return expected


def _grid(kind: str, shape: ShapeParameters, cells: Mapping[tuple[str, str], float]) -> dict[Key, float]:
    """A block x WP grid with its row and column totals and the % shares of the grand total."""
    expected: dict[Key, float] = {(kind, slot, wp): value for (slot, wp), value in cells.items()}
    by_slot = {s: sum(cells[(s, wp)] for wp in shape.wp_codes) for s in shape.slots}
    by_wp = {wp: sum(cells[(s, wp)] for s in shape.slots) for wp in shape.wp_codes}
    grand = sum(by_slot.values())

    def share(value: float) -> float:
        return value / grand if grand > 0 else 0.0

    for slot, value in by_slot.items():
        expected[(kind, slot, "total")] = value
        expected[(kind, slot, "share")] = share(value)
    for wp, value in by_wp.items():
        expected[(kind, "total", wp)] = value
        expected[(kind, "share", wp)] = share(value)
    expected[(kind, "total", "total")] = grand
    return expected

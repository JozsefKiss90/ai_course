"""The Golden Scenario: the human-owned synthetic proposal each Funding Profile version is pinned to.

The worksheet ``budget_engine/golden/<id>-<version>.md`` is the human's; ``golden/<id>-<version>.json``
next to this module transcribes its inputs and expected figures for the engine. An agent never edits
an expected figure to make a check pass.

The Synthetic Check fills its copy from the Golden Scenario:

- A build with the Golden Scenario's own Shape Parameters gets its inputs exactly. The workbook is then
  compared with the signed-off figures as well as with the reference model.
- Any other build gets the inputs scaled to its Shape Parameters, and its expected figures come from
  the reference model alone. The tests pin that model to the signed-off figures.

Scaling: each BE/AE takes the inputs of a Golden BE/AE of its kind, cycling through them; spare blocks
stay blank, as in the Golden Scenario. Each work package (or task) takes the effort of the Golden
ones that fold onto it, or cycles through them when the build has more. Trips and items keep their
Golden rows, with their BE/AE and WP mapped onto the build's codes.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from budget_engine.layout import Key, Layout
from budget_engine.methods import equipment_depreciation, itemised_list
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters, is_affiliated, is_spare, parse_shape
from budget_engine.verify.scenario import InputValue, Scenario, provisional_scenario

GOLDEN_DIR = Path(__file__).parent / "golden"
BE_FIELDS = {"name": "be_name", "acronym": "be_acronym", "country": "be_country", "funding_rate": "be_funding_rate"}
TABLES = ("trip", "equipment", "itemised")  # input kinds keyed ("<kind>", row nr, field)


@dataclass(frozen=True)
class GoldenScenario:
    profile: Profile
    worksheet: str
    shape_parameters: Mapping[str, Any]  # as a build takes them
    shape: ShapeParameters
    inputs: dict[Key, InputValue]  # at the Golden shape, Golden codes; only the values the worksheet gives
    expected: Mapping[str, Any]  # the worksheet's expected figures, as transcribed

    @property
    def name(self) -> str:
        return f"Golden Scenario {self.profile.id} {self.profile.version}"

    def scenario(self, shape: ShapeParameters, layout: Layout) -> Scenario:
        """The Synthetic Check scenario for a build: exact at the Golden shape, else scaled."""
        if shape == self.shape:
            unknown = set(self.inputs) - set(layout.inputs)
            if unknown:
                raise ValueError(f"{self.name} gives inputs the workbook has no cell for: {sorted(unknown)[:5]}")
            return Scenario(
                name=self.name,
                provenance=(
                    f"Human-owned Golden Scenario ({self.worksheet}). The workbook is compared with its "
                    "signed-off expected figures and with the reference model."
                ),
                human_owned=True,
                inputs={key: self.inputs.get(key) for key in layout.inputs},
                pinned=self.pinned(layout),
            )
        return Scenario(
            name=f"{self.name}, scaled to the build's Shape Parameters",
            provenance=(
                f"Inputs from the human-owned Golden Scenario ({self.worksheet}), scaled to this build. "
                "Expected figures come from the reference model, which reproduces the Golden Scenario's "
                "signed-off figures exactly."
            ),
            human_owned=False,
            inputs=_scale(self, shape, layout),
            ownership="scaled from the human-owned Golden Scenario",
        )

    def pinned(self, layout: Layout) -> dict[Key, float]:
        """The signed-off figures that sit in a workbook cell, keyed like ``Layout.outputs``.

        Shares are left out: the worksheet rounds them to 0.01%, and the tests compare them that way.
        """
        pinned: dict[Key, float] = {}
        line_ids = [r.id for r in self.profile.transfer_view_rows if r.kind == "line"]
        for block, wps in self.expected["transfer_view"].items():
            for wp, figures in wps.items():
                for line in line_ids:
                    if line in figures["lines"]:
                        items, avg, total = figures["lines"][line]
                        pinned |= {("tv", block, wp, line, "items"): items, ("tv", block, wp, line, "avg"): avg}
                        pinned[("tv", block, wp, line, "total")] = total
                    elif ("tv", block, wp, line, "total") in layout.outputs:
                        pinned[("tv", block, wp, line, "total")] = 0.0  # a line not listed is empty
                for row_id, total in figures.items():
                    if row_id != "lines":
                        pinned[("tv", block, wp, row_id, "total")] = total
        for slot in self.shape.spare_slots:  # spare blocks stay empty
            for wp in self.shape.wp_codes:
                pinned[("tv", slot, wp, "F", "total")] = 0.0
        for kind, grid in (("ls", self.expected["lump_sum"]), ("pm", self.expected["person_months"])):
            for row, cells in grid["rows"].items():
                pinned |= {(kind, row, col): value for col, value in cells.items() if col != "share_pct"}
        pinned |= {("ls", block, "rate"): rate for block, rate in self.expected["lump_sum"]["rates"].items()}
        for wp, summary in self.expected["per_wp_summary"]["wps"].items():
            pinned[("wps", wp, "F", "all", "total")] = summary["F"]
        totals = self.expected["cost_categories"]["total"]
        pinned[("wps", "all", "E", "all", "total")] = totals["E"]
        pinned[("wps", "all", "F", "all", "total")] = totals["F"]
        return {key: float(value) for key, value in pinned.items()}


def load_golden(profile: Profile) -> GoldenScenario | None:
    """The profile version's Golden Scenario, or None while it has none."""
    path = GOLDEN_DIR / f"{profile.id}-{profile.version}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    shape, _ = parse_shape(raw["shape"])
    return GoldenScenario(profile, raw["worksheet"], raw["shape"], shape, _inputs(profile, raw), raw["expected"])


def synthetic_scenario(profile: Profile, shape: ShapeParameters, layout: Layout) -> Scenario:
    """What the Synthetic Check fills a build's copy with: the Golden Scenario, else the provisional one."""
    golden = load_golden(profile)
    if golden is None:
        return provisional_scenario(profile, shape, layout)
    return golden.scenario(shape, layout)


def _inputs(profile: Profile, raw: Mapping[str, Any]) -> dict[Key, InputValue]:
    """The worksheet's inputs keyed like ``Layout.inputs``, cost lines given by id turned into labels."""
    given = raw["inputs"]
    inputs: dict[Key, InputValue] = {}
    for be in given["be_list"]:
        inputs |= {(kind, be["code"]): be[field] for field, kind in BE_FIELDS.items()}
    inputs |= {("wp_name", wp["code"]): wp["name"] for wp in given["wp_list"]}
    inputs |= {("task_title", task["code"]): task["title"] for task in given["task_list"]}
    for be, rates in given["rates"].items():
        inputs |= {("rate", be, category): rate for category, rate in rates.items()}
    for row in given["effort"]:
        inputs |= {("effort", row["unit"], row["be"], c): v for c, v in row.items() if c not in ("unit", "be")}
    labels = {"equipment": equipment_depreciation.cost_lines(profile), "itemised": itemised_list.cost_lines(profile)}
    for kind, section in zip(TABLES, ("trips", "equipment", "itemised")):
        for n, row in enumerate(given[section], start=1):
            for field, value in row.items():
                inputs[(kind, str(n), field)] = labels[kind][value] if field == "line" else value
    inputs |= {("wp_lead", wp): be for wp, be in raw["supplement"]["wp_lead"].items()}
    return inputs


def _folded(build_count: int, golden_count: int) -> Callable[[int], list[int]]:
    """Build position -> the Golden positions it takes (0-based): those that fold onto it, or one in turn."""
    def sources(i: int) -> list[int]:
        return [j for j in range(golden_count) if j % build_count == i] or [i % golden_count]
    return sources


def _scale(golden: GoldenScenario, shape: ShapeParameters, layout: Layout) -> dict[Key, InputValue]:
    gshape, given = golden.shape, golden.inputs
    g_bes = gshape.be_codes
    g_aes = [c for c in gshape.entity_codes if is_affiliated(c)]
    b_aes = [c for c in shape.entity_codes if is_affiliated(c)]

    def source_entity(code: str) -> str | None:
        """The Golden BE/AE whose inputs a build BE/AE takes; None for a spare block or with no Golden AE."""
        if is_spare(code):
            return None
        if is_affiliated(code):
            return g_aes[b_aes.index(code) % len(g_aes)] if g_aes else None
        return g_bes[shape.be_codes.index(code) % len(g_bes)]

    def target_entity(code: str) -> str:
        """Where a Golden BE/AE named in a trip or item row lands in the build."""
        if code in shape.entity_codes:
            return code
        be = code.split("-")[0]
        return be if be in shape.be_codes else shape.be_codes[gshape.be_codes.index(be) % shape.beneficiaries]

    def target_wp(wp: str) -> str:
        return shape.wp_codes[gshape.wp_codes.index(wp) % shape.work_packages]

    wp_sources = _folded(shape.work_packages, gshape.work_packages)
    g_units = {wp: [u for w, u in gshape.effort_units if w == wp] for wp in gshape.wp_codes}
    unit_sources: dict[str, list[str]] = {}  # build effort unit -> the Golden units whose effort it takes
    for k, wp in enumerate(shape.wp_codes):
        units = [u for w, u in shape.effort_units if w == wp]
        sources = [u for j in wp_sources(k) for u in g_units[gshape.wp_codes[j]]]
        fold = _folded(len(units), len(sources))
        unit_sources |= {unit: [sources[j] for j in fold(t)] for t, unit in enumerate(units)}

    def first_source_wp(wp: str) -> str:
        return gshape.wp_codes[wp_sources(shape.wp_codes.index(wp))[0]]

    scaled: dict[Key, InputValue] = {}
    for key in layout.inputs:
        kind = key[0]
        value: InputValue = None
        if kind in BE_FIELDS.values() or kind == "rate":
            source = source_entity(key[1])
            value = given.get((kind, source, *key[2:])) if source else None
        elif kind == "effort":
            _, unit, slot, category = key
            source = source_entity(slot)
            efforts = [given.get(("effort", u, source, category)) for u in unit_sources[unit]] if source else []
            present = [float(e) for e in efforts if isinstance(e, (int, float))]
            value = sum(present) if present else None
        elif kind == "wp_name":
            value = given.get(("wp_name", first_source_wp(key[1])))
        elif kind == "wp_lead":
            lead = given.get(("wp_lead", first_source_wp(key[1])))
            value = target_entity(str(lead)) if lead else None
        elif kind == "task_title":
            titles = [given.get(("task_title", u)) for u in unit_sources[key[1]]]
            value = next((t for t in titles if t), next((v for k, v in given.items() if k[0] == "task_title"), None))
        elif kind in TABLES:
            value = given.get(key)
            if value is not None and key[2] == "be":
                value = target_entity(str(value))
            elif value is not None and key[2] == "wp":
                value = target_wp(str(value))
        elif kind not in ("threshold", "slot_code"):  # thresholds and spare block codes stay blank
            raise ValueError(f"the Golden Scenario cannot scale input kind {kind!r}")
        scaled[key] = value
    return scaled

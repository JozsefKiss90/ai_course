"""Synthetic Check scenarios, and the provisional scenario: obviously fake Human Inputs, scaled to the
build's Shape Parameters.

PROVISIONAL, NOT HUMAN-OWNED. The Synthetic Check uses the provisional scenario only for a profile
version without a Golden Scenario (``verify/golden.py``); its expected figures come from the
reference model alone. The tests also use it to stress corners the Golden Scenario does not reach:
a late AE in a spare block, rows appended to the Tables, every travel band, blank entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from budget_engine.layout import Key, Layout
from budget_engine.methods import equipment_depreciation, itemised_list, travel_planner
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters
from budget_engine.sheets import reference_lists
from budget_engine.verify.excel import TableRowAddition

InputValue = str | float | None

PROVENANCE = (
    "Provisional scenario, not human-owned: expected figures come from the reference model only, "
    "not from a Golden Scenario (this profile version has none yet)."
)


@dataclass(frozen=True)
class Scenario:
    name: str
    provenance: str
    human_owned: bool
    inputs: dict[Key, InputValue]  # None: left blank on purpose
    late_rows: tuple[LateRow, ...] = ()
    pinned: dict[Key, float] = field(default_factory=dict)  # signed-off Golden Scenario figures, keyed like outputs
    ownership: str = ""  # for the report; empty: from human_owned

    @property
    def table_rows(self) -> tuple[TableRowAddition, ...]:
        return tuple(r.row for r in self.late_rows)

    @property
    def added_inputs(self) -> dict[Key, InputValue]:
        """The entries of the rows added after the build, keyed like ``inputs``, for the reference model."""
        return {k: v for r in self.late_rows for k, v in r.entries.items()}


@dataclass(frozen=True)
class LateRow:
    """A row a human adds to an Excel Table after the build: a late Beneficiary or AE, another trip."""

    row: TableRowAddition
    entries: dict[Key, InputValue]  # keyed as if typed into a built row, e.g. ("be_name", "BE1-AE2")
    description: str  # for the report, e.g. "BEList: BE1-AE2 under BE1"


def _late_ae_of_be1(profile: Profile, shape: ShapeParameters) -> tuple[str, LateRow]:
    """A late AE of BE1, inserted under BE1's last AE in the `BE list` Table as a human would."""
    code = f"BE1-AE{shape.affiliated_entities[0] + 1}"
    spec = profile.reference_lists["be_list"]
    added: dict[Key, InputValue] = {
        ("be_name", code): f"SYNTHETIC {code} (fake, added late)",
        ("be_acronym", code): f"SYN-{code}",
        ("be_country", code): "Testland (fake)",
        ("be_funding_rate", code): 1,
    }
    values = (code, reference_lists.role(spec, code), *(added[(k, code)] for k in reference_lists.BE_INPUT_KEYS))
    position = 1 + 1 + shape.affiliated_entities[0]  # after BE1 and its AEs
    row = TableRowAddition(spec["sheet"], reference_lists.TABLES["be_list"], position, values)
    return code, LateRow(row, added, f"{row.table}: {code} under BE1")


# BE2 and its AEs get a reduced funding rate, so the lump sum breakdown must apply each block's own.
REDUCED_FUNDING_RATE = 0.7


# Distances (km) spanning the bands of table 5.1, both edges of a band included; none below 400.
TRIP_DISTANCES = (450, 600, 601, 1100, 2900, 12000, 4500, 7501)
TRIP_COUNTRIES = ("Belgium", "Hungary", "Other Countries")


def _fake_trips(shape: ShapeParameters, travellers_from: list[str]) -> dict[Key, InputValue]:
    """One trip per distance, cycling through the BE/AE codes and the WPs; the other trip rows stay blank."""
    trips: dict[Key, InputValue] = {}
    for i, distance in enumerate(TRIP_DISTANCES[: travel_planner.TRIP_ROWS]):
        nights = i % 4
        trip: dict[str, InputValue] = {
            "be": travellers_from[i % len(travellers_from)],
            "wp": shape.wp_codes[(i + i // len(travellers_from)) % shape.work_packages],
            "travellers": 1 + i % 3,
            "distance": distance,
            "nights": nights,
            "days": nights + 1,
            "country": TRIP_COUNTRIES[i % len(TRIP_COUNTRIES)],
        }
        trips.update(_trip_entries(str(i + 1), trip))
    return trips


def _trip_entries(n: str, trip: dict[str, InputValue]) -> dict[Key, InputValue]:
    return {("trip", n, field): value for field, value in trip.items()}


def _late_trip(shape: ShapeParameters) -> LateRow:
    """A trip appended to the Trips Table, inputs only: its prices must fill in as calculated columns."""
    n = str(travel_planner.TRIP_ROWS + 1)
    trip: dict[str, InputValue] = {
        "be": shape.entity_codes[-1], "wp": shape.wp_codes[-1], "travellers": 2, "distance": 1600,
        "nights": 2, "days": 3, "country": "Hungary",
    }
    values = tuple(trip[key] for key, _ in travel_planner.INPUTS)
    row = TableRowAddition(travel_planner.SHEET, travel_planner.TABLE, travel_planner.TRIP_ROWS + 1, values)
    return LateRow(row, _trip_entries(n, trip), f"{row.table}: trip {n} ({trip['be']}, {trip['wp']})")


def _equipment_items(duration: int) -> list[tuple[InputValue, InputValue, InputValue]]:
    """(purchase cost, depreciation period, usage share) per item: periods longer than, shorter than and
    equal to the project, a blank period, and a period without a purchase cost."""
    return [
        (12000, 3 * duration, 0.5),
        (3000, max(1, duration // 3), 1),
        (8000, duration, 0.25),
        (50000, duration + 12, 0.75),
        (4000, None, 1),
        (None, 2 * duration, 1),
    ]


def _fake_equipment(profile: Profile, shape: ShapeParameters, buyers: list[str]) -> dict[Key, InputValue]:
    """One row per item, cycling through the BE/AE codes, the WPs and the C.2 cost lines."""
    labels = list(equipment_depreciation.cost_lines(profile).values())
    entries: dict[Key, InputValue] = {}
    for i, (cost, period, usage) in enumerate(_equipment_items(shape.duration_months)[: equipment_depreciation.ITEM_ROWS]):
        item: dict[str, InputValue] = {
            "be": buyers[i % len(buyers)],
            "wp": shape.wp_codes[(i + i // len(buyers)) % shape.work_packages],
            "line": labels[i % len(labels)],
            "item": f"Synthetic item {i + 1} (fake)",
            "cost": cost,
            "period": period,
            "usage": usage,
        }
        entries.update(_equipment_entries(str(i + 1), item))
    return entries


def _equipment_entries(n: str, item: dict[str, InputValue]) -> dict[Key, InputValue]:
    return {("equipment", n, field): value for field, value in item.items()}


def _late_equipment(profile: Profile, shape: ShapeParameters) -> LateRow:
    """An item appended to the Equipment Table, inputs only: its eligible cost must fill in by itself."""
    n = str(equipment_depreciation.ITEM_ROWS + 1)
    item: dict[str, InputValue] = {
        "be": shape.entity_codes[-1], "wp": shape.wp_codes[-1],
        "line": list(equipment_depreciation.cost_lines(profile).values())[0],
        "item": f"Synthetic item {n} (fake, added late)", "cost": 6000, "period": 2 * shape.duration_months,
        "usage": 0.5,
    }
    values = tuple(item[key] for key, _ in equipment_depreciation.INPUTS)
    row = TableRowAddition(
        equipment_depreciation.SHEET, equipment_depreciation.TABLE, equipment_depreciation.ITEM_ROWS + 1, values
    )
    return LateRow(row, _equipment_entries(n, item), f"{row.table}: item {n} ({item['be']}, {item['wp']})")


# (number of items, cost per item) per item: whole and fractional numbers, a blank cost and a blank number.
ITEMS: list[tuple[InputValue, InputValue]] = [
    (1, 25000), (12, 150.5), (3, 1800), (2.5, 400), (4, None), (None, 900), (1, 30000), (6, 75),
]


def _fake_items(profile: Profile, shape: ShapeParameters, partners: list[str]) -> dict[Key, InputValue]:
    """One row per item, cycling through the BE/AE codes and the WPs, and striding over the cost
    lines so several are used. The last row repeats the first row's BE/AE, WP and cost line, so the
    summary must add two rows up."""
    labels = list(itemised_list.cost_lines(profile).values())
    stride = max(1, len(labels) // 4)
    picks = [
        (partners[i % len(partners)], shape.wp_codes[(i + i // len(partners)) % shape.work_packages], labels[(i * stride) % len(labels)])
        for i in range(len(ITEMS) - 1)
    ]
    picks.append(picks[0])
    entries: dict[Key, InputValue] = {}
    for i, ((be, wp, line), (count, cost)) in enumerate(list(zip(picks, ITEMS))[: itemised_list.ITEM_ROWS]):
        item: dict[str, InputValue] = {
            "be": be, "wp": wp, "line": line, "item": f"Synthetic item {i + 1} (fake)", "number": count, "cost": cost,
        }
        entries.update(_itemised_entries(str(i + 1), item))
    return entries


def _itemised_entries(n: str, item: dict[str, InputValue]) -> dict[Key, InputValue]:
    return {("itemised", n, field): value for field, value in item.items()}


def _late_item(profile: Profile, shape: ShapeParameters) -> LateRow:
    """An item appended to the Items Table, inputs only: its total must fill in by itself."""
    n = str(itemised_list.ITEM_ROWS + 1)
    item: dict[str, InputValue] = {
        "be": shape.entity_codes[-1], "wp": shape.wp_codes[-1],
        "line": list(itemised_list.cost_lines(profile).values())[-1],
        "item": f"Synthetic item {n} (fake, added late)", "number": 2, "cost": 1250,
    }
    values = tuple(item[key] for key, _ in itemised_list.INPUTS)
    row = TableRowAddition(itemised_list.SHEET, itemised_list.TABLE, itemised_list.ITEM_ROWS + 1, values)
    return LateRow(row, _itemised_entries(n, item), f"{row.table}: item {n} ({item['be']}, {item['wp']})")


def provisional_scenario(profile: Profile, shape: ShapeParameters, layout: Layout) -> Scenario:
    """Fake values for every Human Input cell in ``layout``.

    BE2 and its AEs have a 70% funding rate, every other BE/AE 100%.
    Rates are round numbers that encode the BE/AE block and Staff Category (second block, third
    category -> 2,300); effort, per WP or per task, cycles through blank, 0.5, 1 and 1.5 so blank
    cells are exercised too. With the travel planner, trips cycle through every BE/AE (the late AE
    included) and the WPs over the travel bands, and one more trip is appended to the Trips Table.
    With equipment depreciation, items cycle the same way over the C.2 cost lines, with depreciation
    periods shorter than, equal to and longer than the project, and one more item is appended.
    With the itemised list, items cycle the same way over several of its cost lines, two rows
    landing on the same BE/AE × WP × line, and one more item is appended.
    Every work package has a lead (the BE/AEs in turn) and the plausibility thresholds stay blank,
    so the Checks panel is all OK unless a test changes the scenario.
    With headroom, a late AE of BE1 is inserted into the `BE list` Table and claims the first spare
    block; further spare blocks keep a blank code but are filled, so they must calculate anyway.
    An input kind this function does not know raises, so a new sheet cannot slip through unfilled.
    """
    category_index = {c.id: j for j, c in enumerate(profile.staff_categories, start=1)}
    slot_index = {slot: i for i, slot in enumerate(shape.slots, start=1)}
    wp_index = {wp: i for i, wp in enumerate(shape.wp_codes, start=1)}
    unit_index = {unit: i for i, (_, unit) in enumerate(shape.effort_units, start=1)}  # = wp_index without tasks
    inputs: dict[Key, InputValue] = {}
    late_code, late_ae = _late_ae_of_be1(profile, shape) if shape.spare_slots else (None, None)
    partners = shape.entity_codes + ([late_code] if late_code else [])
    trips = _fake_trips(shape, partners)
    equipment = _fake_equipment(profile, shape, partners)
    items = _fake_items(profile, shape, partners)
    for key in layout.inputs:
        kind = key[0]
        if kind == "be_name":
            inputs[key] = f"SYNTHETIC {key[1]} (fake)"
        elif kind == "be_acronym":
            inputs[key] = f"SYN-{key[1]}"
        elif kind == "be_country":
            inputs[key] = "Testland (fake)"
        elif kind == "be_funding_rate":
            inputs[key] = REDUCED_FUNDING_RATE if key[1].split("-")[0] == "BE2" else 1
        elif kind == "wp_name":
            inputs[key] = f"Synthetic work package {wp_index[key[1]]} (fake)"
        elif kind == "task_title":
            inputs[key] = f"Synthetic task {key[1]} (fake)"
        elif kind == "wp_lead":
            inputs[key] = shape.entity_codes[(wp_index[key[1]] - 1) % len(shape.entity_codes)]
        elif kind == "threshold":
            inputs[key] = None  # no threshold: every plausibility warning stays silent
        elif kind == "slot_code":
            inputs[key] = late_code if late_code and key[1] == shape.spare_slots[0] else None
        elif kind == "rate":
            _, be, category = key
            inputs[key] = 1000 * slot_index[be] + 100 * category_index[category]
        elif kind == "effort":
            _, unit, be, category = key
            step = (3 * unit_index[unit] + 2 * slot_index[be] + category_index[category]) % 4
            inputs[key] = step * 0.5 if step else None  # None: left blank
        elif kind == "trip":
            inputs[key] = trips.get(key)
        elif kind == "equipment":
            inputs[key] = equipment.get(key)
        elif kind == "itemised":
            inputs[key] = items.get(key)
        else:
            raise ValueError(f"the provisional scenario has no fake value for input kind {kind!r}")
    return Scenario(
        name=f"provisional {profile.id} {profile.version}",
        provenance=PROVENANCE,
        human_owned=False,
        inputs=inputs,
        late_rows=(
            *((late_ae,) if late_ae else ()),
            *((_late_trip(shape),) if travel_planner.ID in shape.methods else ()),
            *((_late_equipment(profile, shape),) if equipment_depreciation.ID in shape.methods else ()),
            *((_late_item(profile, shape),) if itemised_list.ID in shape.methods else ()),
        ),
    )

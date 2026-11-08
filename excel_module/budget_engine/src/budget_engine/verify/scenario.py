"""The provisional scenario: obviously fake Human Inputs, scaled to the build's Shape Parameters.

PROVISIONAL, NOT HUMAN-OWNED. Until ticket 15 pins the profile's Golden Scenario, the Synthetic
Check fills its disposable copy with these values, and its expected figures come from the reference
model alone. A shared mistake in the reference model and the workbook would pass unnoticed.
"""

from __future__ import annotations

from dataclasses import dataclass

from budget_engine.layout import Key, Layout
from budget_engine.profiles import Profile
from budget_engine.shape import ShapeParameters
from budget_engine.sheets import reference_lists
from budget_engine.verify.excel import TableRowAddition

InputValue = str | float | None

PROVENANCE = (
    "Provisional scenario, not human-owned: expected figures come from the reference model only, "
    "not from a hand-computed Golden Scenario (replaced when ticket 15 pins the Golden Scenario)."
)


@dataclass(frozen=True)
class Scenario:
    name: str
    provenance: str
    human_owned: bool
    inputs: dict[Key, InputValue]  # None: left blank on purpose
    late_entities: tuple[LateEntity, ...] = ()

    @property
    def table_rows(self) -> tuple[TableRowAddition, ...]:
        return tuple(e.row for e in self.late_entities)

    @property
    def added_inputs(self) -> dict[Key, InputValue]:
        """The late entities' `BE list` entries, keyed like ``inputs``, for the reference model."""
        return {k: v for e in self.late_entities for k, v in e.entries.items()}


@dataclass(frozen=True)
class LateEntity:
    """A Beneficiary or AE a human adds to the `BE list` Table after the build."""

    code: str
    row: TableRowAddition
    entries: dict[Key, InputValue]  # ("be_name", code) -> ..., as if typed into the built rows
    description: str  # for the report, e.g. "BEList: BE1-AE2 under BE1"


def _late_ae_of_be1(profile: Profile, shape: ShapeParameters) -> LateEntity:
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
    return LateEntity(code, row, added, f"{row.table}: {code} under BE1")


def provisional_scenario(profile: Profile, shape: ShapeParameters, layout: Layout) -> Scenario:
    """Fake values for every Human Input cell in ``layout``.

    Rates are round numbers that encode the BE/AE block and Staff Category (second block, third
    category -> 2,300); effort, per WP or per task, cycles through blank, 0.5, 1 and 1.5 so blank
    cells are exercised too.
    With headroom, a late AE of BE1 is inserted into the `BE list` Table and claims the first spare
    block; further spare blocks keep a blank code but are filled, so they must calculate anyway.
    An input kind this function does not know raises, so a new sheet cannot slip through unfilled.
    """
    category_index = {c.id: j for j, c in enumerate(profile.staff_categories, start=1)}
    slot_index = {slot: i for i, slot in enumerate(shape.slots, start=1)}
    wp_index = {wp: i for i, wp in enumerate(shape.wp_codes, start=1)}
    unit_index = {unit: i for i, (_, unit) in enumerate(shape.effort_units, start=1)}  # = wp_index without tasks
    inputs: dict[Key, InputValue] = {}
    late = _late_ae_of_be1(profile, shape) if shape.spare_slots else None
    for key in layout.inputs:
        kind = key[0]
        if kind == "be_name":
            inputs[key] = f"SYNTHETIC {key[1]} (fake)"
        elif kind == "be_acronym":
            inputs[key] = f"SYN-{key[1]}"
        elif kind == "be_country":
            inputs[key] = "Testland (fake)"
        elif kind == "be_funding_rate":
            inputs[key] = 1
        elif kind == "wp_name":
            inputs[key] = f"Synthetic work package {wp_index[key[1]]} (fake)"
        elif kind == "task_title":
            inputs[key] = f"Synthetic task {key[1]} (fake)"
        elif kind == "slot_code":
            inputs[key] = late.code if late and key[1] == shape.spare_slots[0] else None
        elif kind == "rate":
            _, be, category = key
            inputs[key] = 1000 * slot_index[be] + 100 * category_index[category]
        elif kind == "effort":
            _, unit, be, category = key
            step = (3 * unit_index[unit] + 2 * slot_index[be] + category_index[category]) % 4
            inputs[key] = step * 0.5 if step else None  # None: left blank
        else:
            raise ValueError(f"the provisional scenario has no fake value for input kind {kind!r}")
    return Scenario(
        name=f"provisional {profile.id} {profile.version}",
        provenance=PROVENANCE,
        human_owned=False,
        inputs=inputs,
        late_entities=(late,) if late else (),
    )

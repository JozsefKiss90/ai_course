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


def provisional_scenario(profile: Profile, shape: ShapeParameters, layout: Layout) -> Scenario:
    """Fake values for every Human Input cell in ``layout``.

    Rates are round numbers that encode the BE and Staff Category (BE2, third category -> 2,300);
    effort cycles through blank, 0.5, 1 and 1.5 so blank cells are exercised too. An input kind
    this function does not know raises, so a new sheet cannot slip through the check unfilled.
    """
    category_index = {c.id: j for j, c in enumerate(profile.staff_categories, start=1)}
    be_index = {be: i for i, be in enumerate(shape.be_codes, start=1)}
    wp_index = {wp: i for i, wp in enumerate(shape.wp_codes, start=1)}
    inputs: dict[Key, InputValue] = {}
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
        elif kind == "rate":
            _, be, category = key
            inputs[key] = 1000 * be_index[be] + 100 * category_index[category]
        elif kind == "effort":
            _, wp, be, category = key
            step = (3 * wp_index[wp] + 2 * be_index[be] + category_index[category]) % 4
            inputs[key] = step * 0.5 if step else None  # None: left blank
        else:
            raise ValueError(f"the provisional scenario has no fake value for input kind {kind!r}")
    return Scenario(
        name=f"provisional {profile.id} {profile.version}",
        provenance=PROVENANCE,
        human_owned=False,
        inputs=inputs,
    )

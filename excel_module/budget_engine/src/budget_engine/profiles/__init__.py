"""Funding Profiles: versioned data files plus a loader.

A profile version lives at ``data/<id>/<version>.json`` and is immutable once accepted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"
# Shared unit-cost tables, not a profile version: kept outside data/<id>/ so
# available_profiles() never lists it.
HE_TRAVEL_UNIT_COSTS = DATA_DIR / "he_travel_unit_costs_c2024_5405.json"


class ProfileNotFound(LookupError):
    pass


@dataclass(frozen=True)
class ProfileConstant:
    id: str
    label: str
    value: float
    unit: str
    source: str


@dataclass(frozen=True)
class CostCategory:
    id: str
    label: str


@dataclass(frozen=True)
class StaffCategory:
    id: str
    label: str
    cost_line: str


@dataclass(frozen=True)
class LayoutRow:
    """One row of the Submission Budget breakdown the Transfer View mirrors."""

    kind: str  # heading | line | blank | total | indirect | grand_total
    id: str = ""
    label: str = ""
    group: str = ""
    sum_groups: tuple[str, ...] = ()
    add: tuple[str, ...] = ()


@dataclass(frozen=True)
class IndirectRule:
    line: str
    rate_constant: str
    base_groups: tuple[str, ...]


@dataclass(frozen=True)
class MethodRules:
    allowed: tuple[str, ...]
    default: tuple[str, ...]
    mandatory: tuple[str, ...]


@dataclass(frozen=True)
class Profile:
    id: str
    version: str
    name: str
    provenance: tuple[dict[str, str], ...]
    effort_unit: str
    rate_unit: str
    default_headroom: int
    constants: tuple[ProfileConstant, ...]
    cost_categories: tuple[CostCategory, ...]
    indirect_rule: IndirectRule
    staff_categories: tuple[StaffCategory, ...]
    methods: MethodRules
    reference_lists: dict[str, Any]
    transfer_view_headers: tuple[str, ...]
    wp_title: str
    transfer_view_rows: tuple[LayoutRow, ...]

    def constant(self, constant_id: str) -> ProfileConstant:
        return next(c for c in self.constants if c.id == constant_id)


def available_profiles() -> list[tuple[str, str]]:
    return sorted((p.parent.name, p.stem) for p in DATA_DIR.glob("*/*.json"))


def load_travel_unit_costs() -> dict[str, Any]:
    """HE travel, accommodation and subsistence unit costs from C(2024)5405, with provenance."""
    data: dict[str, Any] = json.loads(HE_TRAVEL_UNIT_COSTS.read_text(encoding="utf-8"))
    return data


def load_profile(profile_id: str, version: str) -> Profile:
    path = DATA_DIR / profile_id / f"{version}.json"
    if not path.is_file():
        raise ProfileNotFound(f"no Funding Profile {profile_id!r} version {version!r}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    tv = raw["transfer_view"]
    declared = {c["id"] for c in raw["cost_categories"]}
    used = {r["group"] for r in tv["rows"] if "group" in r} | {raw["indirect_rule"]["line"]}
    if used - declared:
        raise ValueError(f"{path.name}: undeclared cost categories {sorted(used - declared)}")
    return Profile(
        id=raw["id"],
        version=raw["version"],
        name=raw["name"],
        provenance=tuple(raw["provenance"]),
        effort_unit=raw["effort_unit"],
        rate_unit=raw["rate_unit"],
        default_headroom=raw["default_headroom"],
        constants=tuple(ProfileConstant(**c) for c in raw["profile_constants"]),
        cost_categories=tuple(CostCategory(**c) for c in raw["cost_categories"]),
        indirect_rule=IndirectRule(
            line=raw["indirect_rule"]["line"],
            rate_constant=raw["indirect_rule"]["rate_constant"],
            base_groups=tuple(raw["indirect_rule"]["base_groups"]),
        ),
        staff_categories=tuple(StaffCategory(**s) for s in raw["staff_categories"]),
        methods=MethodRules(**{k: tuple(v) for k, v in raw["estimation_methods"].items()}),
        reference_lists=raw["reference_lists"],
        transfer_view_headers=tuple(tv["headers"]),
        wp_title=tv["wp_title"],
        transfer_view_rows=tuple(
            LayoutRow(
                kind=r["kind"],
                id=r.get("id", ""),
                label=r.get("label", ""),
                group=r.get("group", ""),
                sum_groups=tuple(r.get("sum_groups", ())),
                add=tuple(r.get("add", ())),
            )
            for r in tv["rows"]
        ),
    )

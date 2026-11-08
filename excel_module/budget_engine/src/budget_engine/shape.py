"""The build input contract: Shape Parameters and nothing else (ADR-0001).

There is deliberately no field that could carry an identifier or an amount. Unknown keys
are rejected rather than ignored, so a mistakenly supplied name never travels further. Errors name
the offending key and never repeat the value given for it, which may be exactly such a name.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

from budget_engine.profiles import Profile, ProfileNotFound, available_profiles, load_profile

ALLOWED_KEYS = {
    "profile", "beneficiaries", "affiliated_entities", "work_packages", "tasks", "duration_months", "methods",
    "headroom",
}
REQUIRED_KEYS = {"profile", "beneficiaries", "work_packages", "duration_months"}


SPARE_PREFIX = "SPARE"  # internal key of a spare block; the workbook shows "spare <n>"


def is_spare(slot: str) -> bool:
    return slot.startswith(SPARE_PREFIX)


def is_affiliated(code: str) -> bool:
    return "-AE" in code


class ShapeError(ValueError):
    """The request is outside the Shape Parameters contract."""


@dataclass(frozen=True)
class ShapeParameters:
    profile_id: str
    profile_version: str
    beneficiaries: int
    affiliated_entities: tuple[int, ...]  # per Beneficiary, in BE order
    work_packages: int
    duration_months: int
    methods: tuple[str, ...]
    headroom: int
    tasks: tuple[int, ...] | None = None  # per WP, in WP order; None: no Task List, effort at WP grain

    @property
    def be_codes(self) -> list[str]:
        return [f"BE{i}" for i in range(1, self.beneficiaries + 1)]

    @property
    def entity_codes(self) -> list[str]:
        """Beneficiaries with their Affiliated Entities listed under them, as in the `BE list`."""
        codes = []
        for be, aes in zip(self.be_codes, self.affiliated_entities):
            codes += [be] + [f"{be}-AE{a}" for a in range(1, aes + 1)]
        return codes

    @property
    def spare_slots(self) -> list[str]:
        return [f"{SPARE_PREFIX}{i}" for i in range(1, self.headroom + 1)]

    @property
    def slots(self) -> list[str]:
        """Every per-BE/AE block: one per Beneficiary and AE, then the spare ones up to the headroom."""
        return self.entity_codes + self.spare_slots

    @property
    def wp_codes(self) -> list[str]:
        return [f"WP{i}" for i in range(1, self.work_packages + 1)]

    @property
    def task_codes(self) -> list[str]:
        return [task for _, task in self.effort_units] if self.tasks is not None else []

    @property
    def effort_units(self) -> list[tuple[str, str]]:
        """(WP, unit) per row of effort: each task under its WP with a Task List, else each WP itself."""
        if self.tasks is None:
            return [(wp, wp) for wp in self.wp_codes]
        return [(f"WP{w}", f"T{w}.{t}") for w, n in enumerate(self.tasks, start=1) for t in range(1, n + 1)]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _whole(value: object, minimum: int) -> bool:
    # bool is an int subclass; True must not pass as a count.
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def _count(raw: Mapping[str, Any], key: str, minimum: int) -> int:
    value = raw[key]
    if not _whole(value, minimum):
        raise ShapeError(f"{key} must be a whole number >= {minimum}")
    return int(value)


def _affiliated_entities(raw: Mapping[str, Any], beneficiaries: int) -> tuple[int, ...]:
    value = raw.get("affiliated_entities", [0] * beneficiaries)
    if (
        not isinstance(value, (list, tuple))
        or len(value) != beneficiaries
        or not all(_whole(v, 0) for v in value)
    ):
        raise ShapeError(
            f"affiliated_entities must list one whole number >= 0 per Beneficiary ({beneficiaries} in all)"
        )
    return tuple(value)


def _tasks(raw: Mapping[str, Any], work_packages: int) -> tuple[int, ...] | None:
    if "tasks" not in raw:
        return None
    value = raw["tasks"]
    if (
        not isinstance(value, (list, tuple))
        or len(value) != work_packages
        or not all(_whole(v, 1) for v in value)
    ):
        raise ShapeError(
            f"tasks must list one whole number >= 1 per work package ({work_packages} in all)"
        )
    return tuple(value)


def parse_shape(raw: Mapping[str, Any]) -> tuple[ShapeParameters, Profile]:
    unknown = set(raw) - ALLOWED_KEYS
    if unknown:
        raise ShapeError(
            f"not a Shape Parameter: {', '.join(sorted(unknown))} "
            f"(allowed: {', '.join(sorted(ALLOWED_KEYS))})"
        )
    missing = REQUIRED_KEYS - set(raw)
    if missing:
        raise ShapeError(f"missing Shape Parameters: {', '.join(sorted(missing))}")

    ref = raw["profile"]
    if not isinstance(ref, Mapping) or set(ref) != {"id", "version"}:
        raise ShapeError("profile must be exactly {'id': ..., 'version': ...}")
    if not all(isinstance(ref[k], str) for k in ("id", "version")):
        raise ShapeError("profile id and version must be strings")
    try:
        profile = load_profile(ref["id"], ref["version"])
    except ProfileNotFound:
        available = ", ".join(f"{i} {v}" for i, v in available_profiles())
        raise ShapeError(f"no such Funding Profile version (available: {available})") from None

    methods = raw.get("methods", list(profile.methods.default))
    if not isinstance(methods, (list, tuple)) or not all(isinstance(m, str) for m in methods):
        raise ShapeError("methods must be a list of Estimation Method ids")
    not_allowed = [m for m in methods if m not in profile.methods.allowed]
    if not_allowed:
        raise ShapeError(
            f"{len(not_allowed)} Estimation Method(s) not allowed by {profile.id} {profile.version} "
            f"(allowed: {', '.join(profile.methods.allowed)})"
        )
    switched_on = [m for m in profile.methods.allowed if m in methods or m in profile.methods.mandatory]

    headroom = _count(raw, "headroom", 0) if "headroom" in raw else profile.default_headroom

    beneficiaries = _count(raw, "beneficiaries", 1)
    work_packages = _count(raw, "work_packages", 1)
    shape = ShapeParameters(
        profile_id=profile.id,
        profile_version=profile.version,
        beneficiaries=beneficiaries,
        affiliated_entities=_affiliated_entities(raw, beneficiaries),
        work_packages=work_packages,
        duration_months=_count(raw, "duration_months", 1),
        methods=tuple(switched_on),
        headroom=headroom,
        tasks=_tasks(raw, work_packages),
    )
    return shape, profile

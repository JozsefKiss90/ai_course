"""The build input contract: Shape Parameters and nothing else (ADR-0001).

There is deliberately no field that could carry an identifier or an amount. Unknown keys
are rejected rather than ignored, so a mistakenly supplied name never travels further.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

from budget_engine.profiles import Profile, ProfileNotFound, load_profile

ALLOWED_KEYS = {"profile", "beneficiaries", "work_packages", "duration_months", "methods", "headroom"}
REQUIRED_KEYS = {"profile", "beneficiaries", "work_packages", "duration_months"}


class ShapeError(ValueError):
    """The request is outside the Shape Parameters contract."""


@dataclass(frozen=True)
class ShapeParameters:
    profile_id: str
    profile_version: str
    beneficiaries: int
    work_packages: int
    duration_months: int
    methods: tuple[str, ...]
    headroom: int

    @property
    def be_codes(self) -> list[str]:
        return [f"BE{i}" for i in range(1, self.beneficiaries + 1)]

    @property
    def wp_codes(self) -> list[str]:
        return [f"WP{i}" for i in range(1, self.work_packages + 1)]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _count(raw: Mapping[str, Any], key: str, minimum: int) -> int:
    value = raw[key]
    # bool is an int subclass; True must not pass as a count.
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ShapeError(f"{key} must be a whole number >= {minimum}, got {value!r}")
    return value


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
    except ProfileNotFound as exc:
        raise ShapeError(str(exc)) from exc

    methods = raw.get("methods", list(profile.methods.default))
    if not isinstance(methods, (list, tuple)) or not all(isinstance(m, str) for m in methods):
        raise ShapeError("methods must be a list of Estimation Method ids")
    not_allowed = [m for m in methods if m not in profile.methods.allowed]
    if not_allowed:
        raise ShapeError(
            f"Estimation Methods not allowed by {profile.id} {profile.version}: {', '.join(not_allowed)}"
        )
    switched_on = [m for m in profile.methods.allowed if m in methods or m in profile.methods.mandatory]

    headroom = _count(raw, "headroom", 0) if "headroom" in raw else profile.default_headroom

    shape = ShapeParameters(
        profile_id=profile.id,
        profile_version=profile.version,
        beneficiaries=_count(raw, "beneficiaries", 1),
        work_packages=_count(raw, "work_packages", 1),
        duration_months=_count(raw, "duration_months", 1),
        methods=tuple(switched_on),
        headroom=headroom,
    )
    return shape, profile

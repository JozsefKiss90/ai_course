"""The command line the budget-planner skill drives: ``python -m budget_engine <command>``.

- ``profiles``: each Funding Profile version with its Estimation Methods and default headroom (JSON)
- ``confirm``: reads the Shape Parameters back for the human to confirm, without building
- ``deliver --out DIR``: builds, checks and writes the Handover Package into DIR
- ``confirm-rebuild``: reads back the old and the new Shape Parameters of a rebuild
- ``rebuild --out DIR``: as ``deliver`` for the new Shape Parameters, plus the re-paste guide

Shape Parameters arrive as a JSON object on stdin (for a rebuild, ``{"old": {...}, "new": {...}}``),
so they are never written to a file. Exit codes: 0 done, 1 a build or check failed (nothing
delivered), 2 the input is outside the Shape Parameters contract. Error messages name the offending keys, never the values given for them.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, TextIO

from budget_engine.build import SyntheticCheckFailed
from budget_engine.handover import REPORT, HandoverPackage, deliver, rebuild
from budget_engine.methods import CATALOGUE
from budget_engine.profiles import Profile, available_profiles, load_profile
from budget_engine.repaste import parse_rebuild
from budget_engine.shape import ShapeError, ShapeParameters, parse_shape


class _InputError(Exception):
    pass


def _profiles() -> list[dict[str, Any]]:
    listed = []
    for profile_id, version in available_profiles():
        profile = load_profile(profile_id, version)
        listed.append({
            "id": profile.id,
            "version": profile.version,
            "name": profile.name,
            "effort_unit": profile.effort_unit,
            "default_headroom": profile.default_headroom,
            "methods": [
                {
                    "id": m,
                    "label": CATALOGUE[m].SHEET,
                    "default": m in profile.methods.default,
                    "mandatory": m in profile.methods.mandatory,
                }
                for m in profile.methods.allowed
            ],
        })
    return listed


def _codes_with_counts(codes: Sequence[str], counts: Sequence[int]) -> str:
    return ", ".join(f"{c}: {n}" for c, n in zip(codes, counts))


def read_back(shape: ShapeParameters, profile: Profile) -> str:
    """The Shape Parameters as the human confirms them, defaults and mandatory methods resolved."""
    aes = sum(shape.affiliated_entities)
    if shape.tasks is None:
        tasks = "none (no Task List, effort per work package)"
    else:
        tasks = f"{_codes_with_counts(shape.wp_codes, shape.tasks)} (Task List on, effort per {shape.effort_grain})"
    methods = []
    for m in profile.methods.allowed:
        mark = "on" if m in shape.methods else "off"
        locked = " (mandatory, locked on)" if m in profile.methods.mandatory else ""
        methods.append(f"  [{mark}] {CATALOGUE[m].SHEET}{locked}")
    if shape.headroom != profile.default_headroom:
        headroom = f"{shape.headroom} spare blocks (override; profile default {profile.default_headroom})"
    else:
        headroom = f"{shape.headroom} spare blocks (profile default)"
    return "\n".join([
        f"Funding Profile: {profile.name} ({profile.id} {profile.version})",
        f"Beneficiaries: {shape.beneficiaries}",
        f"Affiliated Entities: {_codes_with_counts(shape.be_codes, shape.affiliated_entities)} ({aes} in all)" if aes
        else "Affiliated Entities: none",
        f"Work packages: {shape.work_packages}",
        f"Tasks: {tasks}",
        f"Duration: {shape.duration_months} months",
        "Estimation Methods:",
        *methods,
        f"Headroom: {headroom}",
    ]) + "\n"


def _read_shape(stdin: TextIO) -> dict[str, Any]:
    try:
        raw = json.load(stdin)
    except json.JSONDecodeError:
        raw = None
    if not isinstance(raw, dict):
        raise _InputError("Shape Parameters must be a JSON object on stdin")
    return raw


REBUILD_KEYS = {"old", "new"}


def _read_rebuild(stdin: TextIO) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = _read_shape(stdin)
    if set(raw) != REBUILD_KEYS:
        others = ", ".join(sorted(set(raw) - REBUILD_KEYS)) or "none"
        raise _InputError(
            f"a rebuild takes exactly the keys old, new (the old and the new Shape Parameters); other keys: {others}"
        )
    return raw["old"], raw["new"]


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: TextIO = sys.stdin,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    parser = argparse.ArgumentParser(prog="python -m budget_engine")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("profiles", help="list Funding Profiles, their Estimation Methods and default headroom")
    commands.add_parser("confirm", help="read back the Shape Parameters on stdin, without building")
    deliver_cmd = commands.add_parser("deliver", help="build, check and package; Shape Parameters on stdin")
    deliver_cmd.add_argument("--out", required=True, help="a new or empty directory for the Handover Package")
    commands.add_parser("confirm-rebuild", help="read back old and new Shape Parameters on stdin, without building")
    rebuild_cmd = commands.add_parser("rebuild", help="as deliver, plus the re-paste guide; old and new Shape Parameters on stdin")
    rebuild_cmd.add_argument("--out", required=True, help="a new or empty directory for the Handover Package")
    args = parser.parse_args(argv)

    if args.command == "profiles":
        json.dump(_profiles(), stdout, indent=2)
        stdout.write("\n")
        return 0

    if args.command in ("confirm-rebuild", "rebuild"):
        try:
            old_raw, new_raw = _read_rebuild(stdin)
            old_shape, new_shape, _, profile = parse_rebuild(old_raw, new_raw)
        except (_InputError, ShapeError) as exc:
            stderr.write(f"Refused: {exc}\n")
            return 2
        if args.command == "confirm-rebuild":
            stdout.write(
                "Old Shape Parameters (from the old workbook's Cover Sheet):\n" + read_back(old_shape, profile)
                + "\nNew Shape Parameters:\n" + read_back(new_shape, profile)
            )
            return 0
        return _deliver(lambda: rebuild(old_raw, new_raw, args.out), args.out, stdout, stderr)

    try:
        raw = _read_shape(stdin)
        shape, profile = parse_shape(raw)
    except (_InputError, ShapeError) as exc:
        stderr.write(f"Refused: {exc}\n")
        return 2

    if args.command == "confirm":
        stdout.write(read_back(shape, profile))
        return 0
    return _deliver(lambda: deliver(raw, args.out), args.out, stdout, stderr)


def _deliver(make: Callable[[], HandoverPackage], out: str, stdout: TextIO, stderr: TextIO) -> int:
    """Run a delivering command and report it: the package's paths, or why nothing was delivered."""
    try:
        package = make()
    except SyntheticCheckFailed:
        stderr.write(
            f"Synthetic Check failed. No Handover Package was delivered; the workbook was deleted.\n"
            f"Failure report: {Path(out) / REPORT}\n"
        )
        return 1
    except (RuntimeError, ValueError, OSError) as exc:  # BuildError, Excel unavailable, a non-empty or unwritable directory
        stderr.write(f"{exc}\nNo Handover Package was delivered.\n")
        return 1
    repaste = f"- Re-paste guide: {package.repaste_guide}\n" if package.repaste_guide else ""
    stdout.write(
        "Synthetic Check: PASS\n"
        f"Handover Package: {package.directory}\n"
        f"- Planning Workbook: {package.workbook}\n"
        f"- Synthetic Check report: {package.report}\n"
        f"- Fill-in guide: {package.guide}\n"
        f"{repaste}"
    )
    return 0

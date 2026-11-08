"""The command line the budget-planner skill drives: ``python -m budget_engine <command>``.

- ``profiles``: each Funding Profile version with its Estimation Methods and default headroom (JSON)
- ``confirm``: reads the Shape Parameters back for the human to confirm, without building
- ``deliver --out DIR``: builds, checks and writes the Handover Package into DIR
- ``confirm-rebuild``: reads back the old and the new Shape Parameters of a rebuild
- ``rebuild --out DIR``: as ``deliver`` for the new Shape Parameters, plus the re-paste guide

The planner commands take accepted Funding Profile versions only. The budget-profile-maintainer
skill drives the ``profile-*`` commands (``budget_engine.maintain``):

- ``profile-draft ID --from V --version NEW``: start a new version as a copy of V, alongside it
- ``profile-diff ID OLD NEW``: a Markdown diff of two versions
- ``profile-propose ID V --from OLD``: proposed Golden Scenario expected figures for V; writes nothing
- ``profile-approve ID V --from OLD --proposal PID --approved-by NAME``: writes V's Golden Scenario, on the human's approval only
- ``profile-check ID V --out DIR``: the Synthetic Check against V's Golden Scenario, report into DIR
- ``profile-accept ID V --out DIR``: the same check, and V is accepted if it passes

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
from budget_engine import maintain
from budget_engine.handover import REPORT, HandoverPackage, deliver, rebuild
from budget_engine.methods import CATALOGUE
from budget_engine.profiles import Profile, ProfileNotFound, available_profiles, load_profile
from budget_engine.repaste import parse_rebuild
from budget_engine.shape import ShapeError, ShapeParameters, parse_shape


class _InputError(Exception):
    pass


def _profiles() -> list[dict[str, Any]]:
    listed = []
    for profile_id, version in available_profiles():
        if not maintain.is_accepted(profile_id, version):
            continue  # a draft is the maintainer's until it is accepted
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


def _accepted(profile: Profile) -> None:
    if not maintain.is_accepted(profile.id, profile.version):
        raise _InputError(f"Funding Profile {profile.id} {profile.version} is a draft, not accepted yet")


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
    _maintainer_commands(commands)
    args = parser.parse_args(argv)

    if args.command.startswith("profile-"):
        return _maintain(args, stdout, stderr)

    if args.command == "profiles":
        json.dump(_profiles(), stdout, indent=2)
        stdout.write("\n")
        return 0

    if args.command in ("confirm-rebuild", "rebuild"):
        try:
            old_raw, new_raw = _read_rebuild(stdin)
            old_shape, new_shape, _, profile = parse_rebuild(old_raw, new_raw)
            _accepted(profile)
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
        _accepted(profile)
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


def _maintainer_commands(commands: Any) -> None:
    draft = commands.add_parser("profile-draft", help="start a new Funding Profile version as a copy of an earlier one")
    draft.add_argument("id")
    draft.add_argument("--from", dest="previous", required=True, help="the version to copy")
    draft.add_argument("--version", required=True, help="the new version")
    diff = commands.add_parser("profile-diff", help="a Markdown diff of two Funding Profile versions")
    diff.add_argument("id")
    diff.add_argument("old")
    diff.add_argument("new")
    for name, text in (
        ("profile-propose", "propose a version's Golden Scenario expected figures; writes nothing"),
        ("profile-approve", "write a version's Golden Scenario from the proposal, on the human's approval only"),
    ):
        cmd = commands.add_parser(name, help=text)
        cmd.add_argument("id")
        cmd.add_argument("version")
        cmd.add_argument("--from", dest="previous", required=True, help="the version whose Golden Scenario carries forward")
        if name == "profile-approve":
            cmd.add_argument("--proposal", required=True, help="the id of the proposal the human approved")
            cmd.add_argument("--approved-by", required=True, help="who approved the proposed figures")
    for name, text in (
        ("profile-check", "the Synthetic Check against a version's Golden Scenario (needs Excel)"),
        ("profile-accept", "check a version against its Golden Scenario and accept it if it passes"),
    ):
        cmd = commands.add_parser(name, help=text)
        cmd.add_argument("id")
        cmd.add_argument("version")
        cmd.add_argument("--out", required=True, help="the directory for the Synthetic Check report")


def _maintain(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Run a ``profile-*`` command: 0 done, 1 a check failed or the version was not accepted, 2 refused."""
    try:
        if args.command == "profile-draft":
            stdout.write(f"Draft written: {maintain.draft_version(args.id, args.previous, args.version)}\n")
        elif args.command == "profile-diff":
            stdout.write(maintain.profile_diff(args.id, args.old, args.new))
        elif args.command == "profile-propose":
            stdout.write(maintain.propose_expectations(args.id, args.version, args.previous).to_markdown())
        elif args.command == "profile-approve":
            written = maintain.approve_expectations(
                args.id, args.version, args.previous, proposal_id=args.proposal, approved_by=args.approved_by
            )
            stdout.write("Golden Scenario written:\n" + "".join(f"- {path}\n" for path in written))
        else:
            check = maintain.accept_version if args.command == "profile-accept" else maintain.check_version
            check(args.id, args.version, args.out)
            accepted = f"{args.id} {args.version} accepted.\n" if args.command == "profile-accept" else ""
            stdout.write(f"Synthetic Check: PASS\nReport: {Path(args.out) / maintain.CHECK_REPORT}\n{accepted}")
    except (ProfileNotFound, FileExistsError, ValueError) as exc:
        stderr.write(f"Refused: {exc}\n")
        return 2
    except SyntheticCheckFailed:
        stderr.write(f"Synthetic Check failed. Not accepted.\nReport: {Path(args.out) / maintain.CHECK_REPORT}\n")
        return 1
    except (maintain.NotAccepted, RuntimeError, OSError) as exc:  # Excel unavailable, a build failure
        stderr.write(f"{exc}\n")
        return 1
    return 0

"""The re-paste guide of a rebuild: which input blocks of the old workbook go where in the new one.

A rebuild takes the old and the new Shape Parameters, never the old workbook (ADR-0001). Both
input layouts are generated in memory from the Shape Parameters and compared, so the guide is
derived from them alone. Within one Funding Profile version an input row keeps its layout: the
same Human Inputs in the same columns, whatever the counts (the contract ``test_rebuild`` pins).
That is what makes re-pasting a block copy.

Each Human Input's key names its row's owner, the BE/AE block, work package, task, Table row or
threshold the row belongs to: ``("rate", "BE2", "A1_senior")`` sits in the row of ``("BE2",)``.
Rows are matched by owner and sheet, and consecutive matched rows merge into one rectangular block
to copy. Rows whose owner is only in the old workbook have no place in the new one; rows only in
the new workbook are filled in fresh.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from typing import Any

from openpyxl.utils import column_index_from_string, get_column_letter

from budget_engine.build import generate
from budget_engine.layout import Key, Layout
from budget_engine.profiles import Profile
from budget_engine.shape import SPARE_PREFIX, ShapeError, ShapeParameters, parse_shape
from budget_engine.sheets import cover

Owner = tuple[str, ...]


def row_owner(key: Key) -> Owner:
    """What a Human Input's row belongs to: its key without the kind and, for a row of several
    inputs of one kind (rates, effort, Table columns), without the field."""
    return key[1:-1] if len(key) > 2 else key[1:]


def _field(key: Key) -> str:
    return f"{key[0]}:{key[-1]}" if len(key) > 2 else key[0]


@dataclass(frozen=True)
class _Segment:
    """A run of adjacent Human Inputs in one row: the unit a block copy is made of."""

    sheet: str
    owner: Owner
    row: int
    first_col: int
    fields: tuple[str, ...]

    @property
    def last_col(self) -> int:
        return self.first_col + len(self.fields) - 1


@dataclass(frozen=True)
class BlockCopy:
    """Copy ``old_range`` of the old workbook to ``new_range`` of the new one, same sheet."""

    sheet: str
    label: str
    old_range: str
    new_range: str


@dataclass(frozen=True)
class Block:
    """Human Inputs of one workbook only: dropped (old) or to fill in fresh (new)."""

    sheet: str
    label: str
    range: str


def _segments(layout: Layout) -> list[_Segment]:
    rows: dict[tuple[str, int], list[tuple[int, Key]]] = defaultdict(list)
    for key, cell in layout.inputs.items():
        rows[(cell.sheet, cell.row)].append((column_index_from_string(cell.column), key))
    segments = []
    for (sheet, row), entries in rows.items():
        owners = {row_owner(key) for _, key in entries}
        if len(owners) != 1:
            raise ValueError(f"{sheet} row {row} holds the inputs of {sorted(owners)}: an input row has one owner")
        owner = owners.pop()
        entries.sort()
        runs: list[list[tuple[int, Key]]] = []
        for col, key in entries:
            if runs and col == runs[-1][-1][0] + 1:
                runs[-1].append((col, key))
            else:
                runs.append([(col, key)])
        segments += [_Segment(sheet, owner, row, run[0][0], tuple(_field(k) for _, k in run)) for run in runs]
    return segments


def _area(first: _Segment, last: _Segment) -> str:
    return f"{get_column_letter(first.first_col)}{first.row}:{get_column_letter(last.last_col)}{last.row}"


def _show(part: str, names: Mapping[str, str]) -> str:
    if part.startswith(SPARE_PREFIX):
        return f"spare {part[len(SPARE_PREFIX):]}"
    return names.get(part, part)


def _label(first: Owner, last: Owner, names: Mapping[str, str]) -> str:
    """"BE1 - BE2", "WP1: BE1 - spare 3", "Table rows 1 - 20": a run of rows by its first and last owner.
    ``names`` shows an owner that is an id (a plausibility threshold) by its label."""
    if all(part.isdigit() for part in first + last):
        return f"Table row {first[0]}" if first == last else f"Table rows {first[0]} - {last[0]}"
    common = 0
    while common < min(len(first), len(last)) - 1 and first[common] == last[common]:
        common += 1

    def show(parts: Owner) -> str:
        return " ".join(_show(part, names) for part in parts)

    span = show(first[common:]) if first == last else f"{show(first[common:])} - {show(last[common:])}"
    return f"{show(first[:common])}: {span}" if common else span


def _runs(segments: Iterable[_Segment], partner: Mapping[_Segment, _Segment] | None = None) -> list[list[_Segment]]:
    """Consecutive rows of one layout (and, with ``partner``, of their counterparts too) as runs."""
    groups: dict[tuple[object, ...], list[_Segment]] = defaultdict(list)
    for s in segments:
        p = partner[s] if partner else None
        groups[(s.sheet, s.fields, s.first_col, p.first_col if p else None)].append(s)
    runs: list[list[_Segment]] = []
    for group in groups.values():
        group.sort(key=lambda s: s.row)
        run = [group[0]]
        for s in group[1:]:
            last = run[-1]
            if s.row == last.row + 1 and (partner is None or partner[s].row == partner[last].row + 1):
                run.append(s)
            else:
                runs.append(run)
                run = [s]
        runs.append(run)
    return runs


@dataclass(frozen=True)
class RepastePlan:
    """Old and new input layouts of one Funding Profile version, compared: the blocks to copy, the
    old inputs with no place in the new workbook, and the new inputs to fill in fresh."""

    profile: Profile
    old_shape: ShapeParameters
    new_shape: ShapeParameters
    old_layout: Layout
    new_layout: Layout
    copies: tuple[BlockCopy, ...]
    dropped: tuple[Block, ...]
    new: tuple[Block, ...]

    def to_markdown(self) -> str:
        profile = self.profile
        old_rows = cover.provenance(profile, self.old_shape, None)
        new_rows = cover.provenance(profile, self.new_shape, None)
        lines = [
            "# Re-paste guide",
            "",
            f"A rebuild under Funding Profile {profile.name} ({profile.id} {profile.version}), the version the "
            "old workbook was built from. This guide was worked out from the old and the new Shape Parameters "
            "alone: nobody but you has opened the old workbook.",
            "",
            "## What changed",
            "",
            "| Shape Parameter | Old | New |",
            "|---|---|---|",
            *(f"| {label} | {old} | {new} |" for (label, old), (_, new) in zip(old_rows[2:], new_rows[2:])),
            "",
            "## How to re-paste",
            "",
            "1. Open the old workbook and the new one side by side.",
            "2. Work through the blocks below, top to bottom. For each one, select the old range in the old "
            "workbook and copy it, click the first cell of the new range in the new workbook, and use "
            "Paste Special > Values. Pasting values only keeps the new workbook's own formats, dropdowns and formulas.",
            "3. Rows you added to a Table after the old build (late trips or items) sit below the listed ranges. "
            "Copy them too, and add the rows to the Table in the new workbook first.",
            "4. Fill in what is new, then check the Checks panel on the new Cover Sheet.",
            "",
            "## Blocks to copy",
        ]
        if not self.copies:
            lines += ["", "None: no input block of the old workbook has a place in the new one."]
        for sheet in _in_order(self.copies):
            lines += ["", f"### {sheet}", "", "| Block | Old range | New range |", "|---|---|---|"]
            lines += [f"| {c.label} | {c.old_range} | {c.new_range} |" for c in self.copies if c.sheet == sheet]
        lines += ["", "## New: fill in fresh", ""]
        lines += _block_list(self.new, "Nothing: every input of the new workbook has a block to copy.")
        lines += ["", "## No place in the new workbook", ""]
        lines += _block_list(self.dropped, "Nothing: every input of the old workbook has a place in the new one.")
        notes = self._notes()
        if notes:
            lines += ["", "## Notes", "", *(f"- {n}" for n in notes)]
        return "\n".join(lines) + "\n"

    def _notes(self) -> list[str]:
        old, new = self.old_shape, self.new_shape
        notes = []
        fewer = (
            new.beneficiaries < old.beneficiaries
            or new.work_packages < old.work_packages
            or any(n < o for o, n in zip(old.affiliated_entities, new.affiliated_entities))
            or (old.tasks is not None and new.tasks is not None and any(n < o for o, n in zip(old.tasks, new.tasks)))
        )
        if fewer:
            notes.append(
                "Blocks are matched by BE/AE nr, WP nr and task nr, which number Beneficiaries, Affiliated Entities, "
                "work packages and tasks by position. If the one that left was not the last one, match the blocks "
                "yourself: every BE/AE "
                "block has the same layout, so the old rows of one paste into the new rows of another, and so do "
                "work packages and tasks. Trips and items that name a BE/AE or WP that no longer exists show a "
                "dropdown error after pasting: correct or delete them."
            )
        grains = self._grains()
        to_task = [wp for wp, o, n in grains if (o, n) == ("work package", "task")]
        to_wp = [wp for wp, o, n in grains if (o, n) == ("task", "work package")]
        if to_task:
            notes.append(
                f"Staff effort per work package ({', '.join(to_task)}) has no place in the new workbook, which plans "
                "it per task: split it across the tasks by hand."
            )
        if to_wp:
            notes.append(
                f"Staff effort per task ({', '.join(to_wp)}) has no place in the new workbook, which plans it per "
                "work package: add the old task rows up and enter the sums by hand."
            )
        if old.headroom:
            notes.append(
                "Spare blocks are matched to spare blocks. A late Beneficiary or AE that claimed a spare block and is now "
                "counted in the Shape Parameters has its own BE/AE rows: paste its spare rows there instead, "
                "without the BE/AE nr you typed into the spare row."
            )
        return notes

    def _grains(self) -> list[tuple[str, str, str]]:
        """(WP, old grain, new grain) per work package in both workbooks."""
        def grain(shape: ShapeParameters, w: int) -> str:
            return "task" if shape.tasks is not None and shape.tasks[w] else "work package"

        common = min(self.old_shape.work_packages, self.new_shape.work_packages)
        return [(f"WP{w + 1}", grain(self.old_shape, w), grain(self.new_shape, w)) for w in range(common)]


def _in_order(blocks: Iterable[BlockCopy | Block]) -> list[str]:
    return list(dict.fromkeys(b.sheet for b in blocks))


def _block_list(blocks: tuple[Block, ...], none: str) -> list[str]:
    if not blocks:
        return [none]
    return [
        f"- **{sheet}**: " + "; ".join(f"{b.label} ({b.range})" for b in blocks if b.sheet == sheet)
        for sheet in _in_order(blocks)
    ]


def compare(
    profile: Profile, old_shape: ShapeParameters, new_shape: ShapeParameters, old_layout: Layout, new_layout: Layout
) -> RepastePlan:
    """The re-paste plan between two input layouts of one Funding Profile version."""
    old_segments, new_segments = _segments(old_layout), _segments(new_layout)
    by_identity = {(s.sheet, s.owner, s.fields): s for s in new_segments}
    new_owners = {(s.sheet, s.owner) for s in new_segments}
    sheet_order = {sheet: i for i, sheet in enumerate(dict.fromkeys(c.sheet for c in new_layout.inputs.values()))}

    partner: dict[_Segment, _Segment] = {}
    dropped: list[_Segment] = []
    for s in old_segments:
        match = by_identity.get((s.sheet, s.owner, s.fields))
        if match is not None:
            partner[s] = match
        elif (s.sheet, s.owner) in new_owners:
            raise ValueError(f"{s.sheet}: the input row of {' '.join(s.owner)} changed layout between the two builds")
        else:
            dropped.append(s)
    matched = set(partner.values())
    fresh = [s for s in new_segments if s not in matched]

    names = {t.id: t.label for t in profile.plausibility}

    def where(run: list[_Segment]) -> tuple[int, int, int]:
        return sheet_order.get(run[0].sheet, len(sheet_order)), run[0].row, run[0].first_col

    copies = tuple(
        BlockCopy(run[0].sheet, _label(run[0].owner, run[-1].owner, names), _area(run[0], run[-1]),
                  _area(partner[run[0]], partner[run[-1]]))
        for run in sorted(_runs(partner, partner), key=where)
    )

    def blocks(segments: list[_Segment]) -> tuple[Block, ...]:
        return tuple(
            Block(run[0].sheet, _label(run[0].owner, run[-1].owner, names), _area(run[0], run[-1]))
            for run in sorted(_runs(segments), key=where)
        )

    return RepastePlan(profile, old_shape, new_shape, old_layout, new_layout, copies, blocks(dropped), blocks(fresh))


def _parse(which: str, raw: object) -> tuple[ShapeParameters, Profile]:
    if not isinstance(raw, Mapping):
        raise ShapeError(f"{which} Shape Parameters must be a JSON object")
    try:
        return parse_shape(raw)
    except ShapeError as exc:
        raise ShapeError(f"{which} Shape Parameters: {exc}") from None


def parse_rebuild(
    old: Mapping[str, Any], new: Mapping[str, Any]
) -> tuple[ShapeParameters, ShapeParameters, dict[str, Any], Profile]:
    """Check both sets of Shape Parameters; returns the old and the new shape, the new parameters as
    given with the old Funding Profile version filled in where they leave it out (what ``deliver``
    takes), and that profile.

    A rebuild keeps the profile version of the old Shape Parameters, even when newer versions exist:
    input-block layouts are a contract within a version only.
    """
    old_shape, profile = _parse("old", old)
    if isinstance(new, Mapping) and "profile" not in new:
        new = {**new, "profile": {"id": profile.id, "version": profile.version}}
    new_shape, _ = _parse("new", new)
    if (new_shape.profile_id, new_shape.profile_version) != (profile.id, profile.version):
        raise ShapeError(
            f"new Shape Parameters: a rebuild keeps the Funding Profile version of the old Shape Parameters "
            f"({profile.id} {profile.version}), so the input blocks keep their layout. For another version, "
            "make a fresh build."
        )
    return old_shape, new_shape, dict(new), profile


def input_layout(shape: ShapeParameters, profile: Profile) -> Layout:
    """The input layout a build from these Shape Parameters has, generated in memory."""
    ctx, _ = generate(shape, profile, date.today())
    return ctx.layout


def repaste_plan(old: Mapping[str, Any], new: Mapping[str, Any]) -> RepastePlan:
    """The re-paste plan from old to new Shape Parameters, without building any workbook on disk."""
    old_shape, new_shape, _, profile = parse_rebuild(old, new)
    return compare(profile, old_shape, new_shape, input_layout(old_shape, profile), input_layout(new_shape, profile))

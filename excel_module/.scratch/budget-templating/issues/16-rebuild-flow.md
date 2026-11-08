# 16 — Rebuild flow and re-paste guide

**What to build:** The `budget-planner` skill can rebuild. Given old and new Shape Parameters (never an existing workbook), it produces:
- a fresh blank Planning Workbook, through the full build flow
- a re-paste guide mapping old input blocks to new ones, so the human can move their own inputs across

Input-block layouts are a contract within a profile version, so re-pasting is a block copy. A rebuild can target the profile version the proposal started with, even when newer versions exist.

**Blocked by:** 06 — AEs and headroom; 07 — Task List; 14 — budget-planner skill

**Status:** done

- [x] Rebuild reference file added to the skill; the skill never asks for or opens an existing workbook
- [x] Re-paste guide derived from comparing old and new Shape Parameters: which blocks move where, which are new, which are dropped
- [x] Contract test: input-block layouts identical across builds with different Shape Parameters under the same profile version
- [x] Rebuild under an older profile version produces a workbook recording that version
- [x] Rebuilt workbook passes the Synthetic Check and ships as a Handover Package with the re-paste guide

## Notes (implementation)

- **Entry points:** `rebuild(old, new, directory)` in `handover.py` delivers the usual Handover Package for the new Shape Parameters (same build, structural checks and Synthetic Check as `deliver`), then writes `re-paste-guide.md`. `repaste_plan(old, new)` gives the guide without building. The CLI has `confirm-rebuild` and `rebuild --out DIR`, both taking `{"old": {...}, "new": {...}}` on stdin.
- **No old workbook:** the old input layout is generated in memory from the old Shape Parameters. `generate()` was extracted from `build()` for this. In the skill (`rebuild.md`), the human reads the old Shape Parameters off the old workbook's Cover Sheet provenance block; the agent never asks for the file or its path.
- **Profile version:** the new Shape Parameters keep the old profile version and may leave `profile` out to inherit it, even when a newer version exists. A different version is refused, because input-block layouts are a contract within one version only. For a newer version: a fresh build, re-entering inputs by hand.
- **Block model:** each Human Input's key names its row's owner (`("rate", "BE2", cat)` belongs to `BE2`). Rows are matched by sheet and owner, split into contiguous column runs (a spare Rate Table row is A, then C:J), and consecutive matched rows merge into rectangular block copies. Owners only in the old layout are listed as having no place; owners only in the new one are listed as fill-in-fresh. An owner in both whose row layout differs raises an error, because that would break the contract.
- **Contract tests:** `test_rebuild.py` fills every old input with its own key, carries out the guide's copies and checks that each lands on the same key in the new layout, across 10 reshapes. It also checks, through `build()`, that every shared input row has identical fields at identical column offsets.
- **Known limit:** BE/AE, WP and task numbers are positional. When one that is not the last leaves, the guide's mapping is by number, and a note tells the human to match those blocks themselves. Shape Parameters cannot say which one left.

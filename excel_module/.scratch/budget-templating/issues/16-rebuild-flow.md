# 16 — Rebuild flow and re-paste guide

**What to build:** The `budget-planner` skill can rebuild. Given old and new Shape Parameters (never an existing workbook), it produces:
- a fresh blank Planning Workbook, through the full build flow
- a re-paste guide mapping old input blocks to new ones, so the human can move their own inputs across

Input-block layouts are a contract within a profile version, so re-pasting is a block copy. A rebuild can target the profile version the proposal started with, even when newer versions exist.

**Blocked by:** 06 — AEs and headroom; 07 — Task List; 14 — budget-planner skill

**Status:** ready-for-agent

- [ ] Rebuild reference file added to the skill; the skill never asks for or opens an existing workbook
- [ ] Re-paste guide derived from comparing old and new Shape Parameters: which blocks move where, which are new, which are dropped
- [ ] Contract test: input-block layouts identical across builds with different Shape Parameters under the same profile version
- [ ] Rebuild under an older profile version produces a workbook recording that version
- [ ] Rebuilt workbook passes the Synthetic Check and ships as a Handover Package with the re-paste guide

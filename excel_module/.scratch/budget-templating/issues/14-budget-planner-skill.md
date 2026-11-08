# 14 — budget-planner skill

**What to build:** The `budget-planner` Claude Code skill. It runs the full build flow end to end: interview, confirm Shape Parameters, generate, structural checks, Synthetic Check, Handover Package. The SKILL.md is thin and points to per-step reference files (Shape Parameters interview, build steps, Synthetic Check, Handover Package).

The interview asks only for Shape Parameters: Funding Profile, counts, duration, Estimation Methods and headroom. It:
- states the profile's default headroom and accepts an override
- switches mandatory methods on automatically
- refuses or ignores any identifier or amount the user mentions
- confirms all Shape Parameters before building

**Blocked by:** 01 — Skill discovery; 13 — Handover Package

**Status:** done

- [x] Skill placed where ticket 01 decided and discovered from the decided start locations
- [x] Interview offers only the methods the chosen profile allows, with defaults pre-selected and mandatory ones locked on
- [x] An identifier or amount offered by the user is not recorded in the workbook, build record or files; the skill says why
- [x] Shape Parameters read back for confirmation before generation
- [x] Any failed step stops delivery and reports the failure
- [x] Walk-through demo: an HE build from the skill yields a Handover Package

## Notes (implementation)

- **Skill**: `excel_module/.claude/skills/budget-planner/` (ticket 01's decision). `SKILL.md` holds four steps (interview, confirm, build/check/deliver, report), each with a completion criterion. It points to `interview.md` (the Shape Parameters guard and the questions), `build-steps.md`, `synthetic-check.md` and `handover-package.md`. Discovery verified with `claude -p`: listed at startup from `excel_module`. From the repo root it is listed only after a Read under `excel_module/`. `excel_module/README.md` tells users how to start.
- **Engine command line** (`budget_engine/cli.py`, `python -m budget_engine`): the skill drives the engine only through it, with the Shape Parameters as JSON on stdin (never a file).
  - `profiles` lists each profile's allowed, default and mandatory methods and its default headroom, so the interview offers only what the profile allows.
  - `confirm` reads back the validated Shape Parameters: mandatory methods shown "locked on", and headroom shown as the profile default or as an override.
  - `deliver --out DIR` calls `deliver`.
  - Exit codes: 0 delivered; 1 a step failed and nothing was delivered (structural check, Synthetic Check with the report path, Excel unavailable, unusable directory); 2 the input is outside the contract.
- **No echo of identifiers**: `ShapeError` messages name the key and never repeat the value given (counts, AE and task lists, unknown methods, unknown profiles). Unknown key *names* are still listed.
- **Walk-through demo**, a headless 3-turn `claude -p` session from `excel_module`:
  - Turn 1 supplied three partner names and "4.2 million euro". The agent left them out, said why, stated the default headroom 3 and locked Staff effort on.
  - Turn 2: it showed the `confirm` read-back and waited for a yes.
  - Turn 3: `deliver` produced the package: Synthetic Check PASS, 3541 figures, provisional scenario.
  - A grep of the unzipped workbook and both Markdown files found no name and no amount.
- Tests: `tests/test_cli.py` (20). Full suite: 231 passed, 1 failed (see below).

### Decisions / known gaps

- **Transfer steps not walked through in the Official.** Ticket 13 left this for this demo. It needs a human with the Official Budget Table v3.6 open, following `fill-in-guide.md`'s transfer section. The agent filled nothing in the Official (out of scope), so it is still open.
- **Flaky timing test.** `test_structural_checks_pass_across_shapes[25-15-84-0]` sits at 9–10 s against its 10 s limit and fails under full-suite load. It passed on its own on the previous commit as well, and this ticket does not touch the build path.
- **Paths in error messages.** An error about a non-empty or unwritable directory repeats the `--out` path. The skill proposes neutral directory names, so this is low risk.
- **Rebuild.** The skill says a rebuild is not available yet. Ticket 16 replaces that line.

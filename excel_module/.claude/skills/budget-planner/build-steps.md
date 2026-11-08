# What `deliver` does

`ENGINE deliver --out <directory>` runs the whole build flow in one process, and stops at the first failure:

1. **Validate** the Shape Parameters against the contract. Anything outside it is refused (exit 2) before anything is written.
2. **Generate** the blank Planning Workbook (`.xlsx`, no macros, no PivotTables): Cover Sheet, Reference Lists, the optional Task List, Rate Table, Profile Constants, one sheet per switched-on Estimation Method, a Transfer View per Beneficiary and Affiliated Entity plus the spare blocks, Check Summaries and Input Guards.
3. **Structural checks** on the blank workbook, without Excel: Reference Lists layout, block counts including headroom, every Human Input empty, no bare constants in formulas, no VBA, PivotTables or personal metadata, provenance on the Cover Sheet, fill-in order and colour legend. A failure deletes the workbook (exit 1, `structural checks failed: …`).
4. **Synthetic Check** on a disposable copy, in real Excel (see [synthetic-check.md](synthetic-check.md)). A failure deletes the workbook and writes only the failure report (exit 1).
5. **Re-check the deliverable**: it must be byte for byte what was built, and pass the structural checks again.
6. **Assemble the Handover Package** (see [handover-package.md](handover-package.md)).

The run takes about a minute, mostly Excel. Excel must be installed. If it can't be started, the command exits 1 with `could not start Excel via COM` and nothing is delivered. Ask the user to close any Excel dialog and try again.

A `VIRTUAL_ENV … does not match the project environment` warning from `uv` is harmless.

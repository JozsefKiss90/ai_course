# 15 — Pin the reference model to the HE Golden Scenario

**What to build:** The Synthetic Check for the HE Funding Profile runs against the human-owned Golden Scenario from ticket 03 instead of the provisional scenario. The reference model must reproduce the hand-computed figures exactly, and the workbook must match after Excel recalculation.

**Blocked by:** 03 — HE Golden Scenario; 06 — AEs and headroom; 07 — Task List; 08 — Travel planner; 09 — Equipment depreciation; 10 — Itemised list; 11 — Full HE Transfer View and Check Summaries

**Status:** done

- [x] Reference model reproduces every Golden Scenario figure exactly
- [x] Workbook matches the Golden Scenario after Excel recalculation
- [x] Provisional scenario retired for HE
- [x] Where model or workbook disagree with the Golden Scenario, the generator or model is fixed. The expected figures are never edited; a suspected error in them is raised to the human

## Notes (implementation)

- **Golden data:** `verify/golden/he-lump-sum-1.0.json` transcribes worksheet §1 (shape), §2 (inputs) and §4 (expected figures). The worksheet stays the source of truth. A review checked every number against it. Mapping: AE1.1 is `BE1-AE1`, the BE countries are the OBT list entries (`Austria (AT)`, `Portugal (PT)`), and the travel mode is not an input.
- **Supplement (human to confirm):** the worksheet gives no WP leads. The JSON adds `WP1: BE1`, `WP2: BE2` under `supplement`, so the Checks panel is not red on every check. No expected figure depends on the leads. If the human agrees, they should go into the worksheet's §2.2.
- **Generator fix:** the Golden shape has WP1 with 2 tasks and WP2 with none, which ticket 07's contract rejected. `tasks` now accepts 0 for a WP, as long as at least one WP has a task. Such a WP has no Task List rows, and its effort stays at WP grain: its effort row shows the WP code in the Task column. The interview guide is updated.
- **Reference model:** unchanged. It reproduced every figure on the first run (`tests/test_golden_scenario.py`, no Excel). Amounts compare to the cent; shares compare as the worksheet rounds them, in % to two decimals. Mutating any single figure makes the tests fail.
- **Synthetic Check:** `verify/golden.py`'s `synthetic_scenario` replaces the provisional default.
  - **Exact:** a build with the Golden Shape Parameters gets the Golden inputs exactly. The workbook is compared with the 100+ signed-off figures that have a cell. The reference model is compared with them too, so drift shows at location "(reference model)".
  - **Scaled:** any other build gets the Golden inputs scaled. BE/AEs cycle through the Golden BE/AEs of their kind; WPs and tasks fold or cycle; trips and items keep their rows, remapped to the build's codes. Its figures come from the pinned reference model.
- **Provisional scenario:** retired for HE. It remains only as the fallback for a profile version without a Golden Scenario (KA220 until ticket 22), and as an explicit stress scenario in the Excel tests: a late AE in a spare block, appended Table rows, every travel band.
- **Not pinned in the workbook:** shares. The worksheet rounds them, so they are checked against the reference model, which the unit tests pin at 0.01%. Per-block A–D and BE+AE rows also have no cell of their own; the tests cover them through the reference model.
- **Known pre-existing failure:** `test_structural_checks_pass_across_shapes[25-15-84-0]` exceeds its 10 s limit on this machine with or without this change (10.7–13 s at HEAD). Building the scenario adds about 20 ms.

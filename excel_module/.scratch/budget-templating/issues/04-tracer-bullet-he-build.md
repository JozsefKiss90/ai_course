# 04 — Tracer bullet: HE build produces a blank Planning Workbook with structural checks

**What to build:** The thinnest end-to-end path through the engine. Given the Horizon Europe lump sum Funding Profile and minimal Shape Parameters (number of Beneficiaries, number of work packages, duration), the build entry point writes a blank `.xlsx` Planning Workbook that opens in Excel 2021/365 without macro or security prompts. The structural checks (seam 2) run on it without Excel and pass.

The workbook contains:
- a Cover Sheet recording profile version, build date and Shape Parameters
- `BE list` and `WP list` with the Official Budget Table v3.6's exact layout
- labelled Profile Constants
- a Rate Table per Beneficiary × Staff Category
- a staff effort sheet at WP × Beneficiary × Staff Category grain, in person-months
- a Transfer View per Beneficiary with the A.1 personnel row and E indirect costs (25% of the eligible base, from a Profile Constant)

This establishes the modular engine (profiles, methods, sheets, verify) and the build input contract, which accepts only profile id/version, counts, duration, method switches and headroom: no field for any identifier or amount.

**Blocked by:** None — can start immediately.

**Status:** done

- [x] HE Funding Profile stored as data with a loader; holds id, version, provenance, cost categories, effort unit, Profile Constants, indirect rule, Staff Categories, allowed/default/mandatory Estimation Methods, default headroom
- [x] Build entry point rejects any input outside the Shape Parameters contract
- [x] Generated workbook is `.xlsx`, has no VBA and no PivotTables
- [x] Structural check: Reference Lists match the Official Budget Table's layout cell for cell
- [x] Structural check: one block per Beneficiary (BE1…BEn) and per WP
- [x] Structural check: every Human Input cell is empty
- [x] Structural check: no formula contains a bare numeric literal beyond trivial ones; constants live in labelled cells
- [x] Structural check: no personal metadata in document properties
- [x] Structural check: Cover Sheet records profile version and Shape Parameters
- [x] Structural checks run over several Shape Parameter combinations and are fast enough for every build
- [x] All tests go through the build entry point; none call sheet builders or method modules directly

## Outcome

- Engine package at `budget_engine/` with the four parts: `profiles` (HE lump sum 1.0 as JSON plus loader), `methods` (staff effort), `sheets` (Cover, BE/WP list, Profile Constants, Rate Table, Transfer View) and `verify/structural.py`. The build entry point is `budget_engine.build(shape_parameters, out_path)`. It runs the structural checks on every build, and deletes the file and raises `BuildError` if any check fails.
- Contract tests are in `tests/test_build_contract.py` and seam-2 tests in `tests/test_structural_checks.py`. Every workbook comes from `build()`. The checks pass over five Shape Parameter combinations, from 1×1 to 25 Beneficiaries × 15 WPs. Each rule is then broken on a copy, and the tests confirm the checks report it.
- The Reference Lists test compares the generated `BE list`/`WP list` with `docs/detailed-budget-table_he-ls-euratom_en.xlsm` itself. It covers title and header text, merges, column widths, row heights, freeze panes and number formats. Fills deliberately differ, because the Planning Workbook's colour legend applies.
- Checked once by hand in Excel via COM, read-only and closed without saving. The workbook opens as `.xlsx` (FileFormat 51) with no VB project, and no formula shows an error after a full recalculation.
- **Not here:** the Official Budget Table's Country dropdown is an x14 data-validation extension referencing its hidden `CountryList`. It needs lxml and belongs to ticket 12 (Input Guards). The funding-rate dropdown (`70%,100%`) is reproduced. Headroom is recorded on the Cover Sheet but does not yet add spare blocks; that is ticket 06.
- **Review follow-ups (two-axis review).**
  - Fixed: the Transfer View labels are now verbatim from the Official Budget Table's `BE tpl`, rows 7–43, and a test checks them. Before the fix, the E, C.2 and D.1/D.3–D.5 labels were paraphrased, and row 18 carried an invented label.
  - Fixed: the profile now has an explicit `cost_categories` field. The loader rejects a Transfer View group that is not a declared category.
  - Fixed: the Cover check derives its labels from the Cover builder, and coordinate parsing is shared.
- **Open questions:**
  - A.4 (SME owners) is priced from a Rate Table Human Input. In the Official Budget Table, A.4 is a unit cost (`ROUND(8745.4 × country coefficient)`). Decide this in ticket 11.
  - `1.0.json` does not pin the travel unit-cost JSON, although the spec makes unit-cost tables part of a profile version. Settle this in ticket 08.
  - The MGA, AGA and Handbook provenance entries carry no version. The versions were not invented; a human should fill them in.
  - Reference List fonts and borders differ from the Official Budget Table: its title is 18 pt and its borders are medium. Only the layout is matched.
  - The Transfer View already carries the full A–F breakdown, built from profile data. It runs ahead of ticket 11, so ticket 11 should verify it, not rebuild it.
  - The tamper tests call `check_structure` directly, on copies of workbooks produced by `build()`. `verify` is the seam-2 API, and neither sheet builders nor methods are called.

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

**Status:** ready-for-agent

- [ ] HE Funding Profile stored as data with a loader; holds id, version, provenance, cost categories, effort unit, Profile Constants, indirect rule, Staff Categories, allowed/default/mandatory Estimation Methods, default headroom
- [ ] Build entry point rejects any input outside the Shape Parameters contract
- [ ] Generated workbook is `.xlsx`, has no VBA and no PivotTables
- [ ] Structural check: Reference Lists match the Official Budget Table's layout cell for cell
- [ ] Structural check: one block per Beneficiary (BE1…BEn) and per WP
- [ ] Structural check: every Human Input cell is empty
- [ ] Structural check: no formula contains a bare numeric literal beyond trivial ones; constants live in labelled cells
- [ ] Structural check: no personal metadata in document properties
- [ ] Structural check: Cover Sheet records profile version and Shape Parameters
- [ ] Structural checks run over several Shape Parameter combinations and are fast enough for every build
- [ ] All tests go through the build entry point; none call sheet builders or method modules directly

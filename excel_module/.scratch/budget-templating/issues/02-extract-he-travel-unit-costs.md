# 02 — Re-extract HE travel and subsistence unit costs from C(2024)5405

**What to build:** The Horizon Europe travel and subsistence unit-cost tables taken from Commission Decision C(2024)5405 itself (not from the old manual template), captured as data ready to drop into the HE Funding Profile, with source provenance.

**Blocked by:** None — can start immediately.

**Status:** done

- [x] Official text of C(2024)5405 (and annexes) obtained and its version/date recorded
- [x] Travel bands (distance bands, amounts) and subsistence amounts (per country, per day) extracted completely
- [x] Data shaped for the Funding Profile's unit-cost tables, with source document, annex and page references per table
- [x] Spot-check of at least five values against the source, recorded in the ticket
- [x] Differences from the manual template's tables listed, for information only

## Outcome

Data file: `budget_engine/src/budget_engine/profiles/data/he_travel_unit_costs_c2024_5405.json`, loaded with `budget_engine.profiles.load_travel_unit_costs()`. Integrity and spot-check tests: `budget_engine/tests/test_travel_unit_costs.py`.

**Source.** Commission Decision C(2024) 5405 final of 31.7.2024, amending C(2021)35. Published as one consolidated 38-page PDF that also holds C(2023)4928 and C(2021)35 ([unit-cost-decision-travel_en.pdf](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/guidance/unit-cost-decision-travel_en.pdf), PDF dated 2024-07-31, downloaded 2026-11-08). It applies to calls opened after 31.7.2024.

**Accommodation and subsistence come from a second source.** The decision's Annex (points 3.2–3.4) gives no amounts. It points to the Staff Regulations hotel ceilings and daily allowances, which update automatically. The current amounts are published in *EU Grants: Additional Information on Unit Costs and Contributions — Annex 2a and 2b*, V1.11 of 01.05.2026. Two periods are captured: calls opening 31.7.2024–12.5.2025, and calls opening from 13.5.2025. The older "before 31 July 2024" table is left out on purpose.

**Tables** (each with annex point and page references in the JSON):

| Table | Annex point | Rows |
|---|---|---|
| `travel_bands` | 5.1, annex p. 7 | 9 |
| `intra_ms_land` | 5.2, annex p. 8 | 24 |
| `inter_ms_land` | 5.3, annex pp. 9–10 | 62 pairs |
| `ms_bordering_land` | 5.4, annex pp. 11–12 | 16 |
| `subsistence` (calls from 13.5.2025) | Annex 2a V1.11 pp. 13–17, 21–24 | 219 |
| `subsistence_2024_07_31_to_2025_05_12` | Annex 2a V1.11 pp. 10–13, 18–21 | 220 |

### Spot-check against the source PDFs

| Value | Source | JSON |
|---|---|---|
| Air band 4 501–6 000 km | C(2024)5405 Annex 5.1, annex p. 7: 857 | 857 ✓ |
| Air band 10 001–Max | same: 1 595 | 1 595 ✓ |
| Intra-MS land HU, 50–399 km | Annex 5.2, annex p. 8: 29, no 400–600 amount | 29 / null ✓ |
| Intra-MS land DE | same: 64 / 157 | 64 / 157 ✓ |
| Inter-MS land DE–PL | Annex 5.3 matrix, annex pp. 9–10: 96/240 | 96 / 240 ✓ |
| Subsistence Belgium, calls from 13.5.2025 | Annex 2a V1.11: 132 | 132 ✓ |
| Accommodation "Other Countries", from 13.5.2025 | Annex 2a V1.11: 145 | 145 ✓ |
| Accommodation Belgium, 31.7.2024–12.5.2025 | Annex 2a V1.11: 148 | 148 ✓ |
| Subsistence Hungary, 31.7.2024–12.5.2025 | Annex 2a V1.11: 64 | 64 ✓ |

The spot-checked values are pinned in the test file.

### Differences from the manual template (`docs/Blank_Project_Budget_Template.xlsx`), for information only

- **5.1 air bands:** amounts are identical. The template's numeric lookup helper has a typo: its second band starts at **301** km instead of 601.
- **5.2 intra-MS land and 5.4 bordering countries:** missing from the template.
- **5.3 inter-MS matrix:** same 62 pairs, same amounts. The template splits "x/y" cells across two rows inconsistently (DE row `96/` + `240` below; PL row `96` + `/240` below), and the SK row's PL–SK cell holds `52/1⏎30` (line break inside the cell) (source: 52/130). Values are right but awkward to read by formula.
- **5.5 accommodation and subsistence:** the template holds the 55-country point 5.5 list of C(2021)35. Those amounts are the floor, not the rates now in force. 44 of the 53 countries that can be matched have different amounts, e.g. Belgium 137/102 in the template against 171/132 now, and Austria 126/102 against 158/131. Kosovo and Palestine have no row of their own in the current tables, so they fall under "Other Countries".
- **Naming:** the JSON uses the source's names, e.g. "Slovak Republic" where the template has "Slovakia".

# AGRI-PULSE demo workbook: verification

Subject: `agripulse-six-partner-budget.xlsx` in this folder. It is a byte-for-byte copy of `..\agripulse-six-partner-budget.xlsx` (SHA-256 `c944485e33d156f61066f916043b6810df6225da35c8ff39ef521544fea2a4ee`).

Verified on 2026-11-08 by opening the package copy read-only in a private desktop Excel instance. Every figure below was read from that saved file. All amounts are in EUR.

## 1. Which checks ran

| Check | Ran on | Result |
|---|---|---|
| Build structural checks | The blank workbook, as `build()` wrote it | Passed |
| Desktop Excel recalculation (this document) | The populated, saved workbook (package copy) | All 311 inputs persisted. 4,310 output figures (Transfer Views, Check sheets, Checks panel, names) match the engine's reference model, both as saved and after `CalculateFull`. 0 cells changed by recalculation; 0 error cells on any sheet. |
| Synthetic Check | A separate blank build with the same shape (`template-handover/planning-workbook.xlsx`), on a disposable synthetic copy | PASS, 4,310 figures, 0 differences. See `template-handover/synthetic-check-report.md`. It does not cover the AGRI-PULSE figures. |

The reference model (`budget_engine.verify.reference`) computes expected figures from the inputs alone. It never reads a workbook formula, so a match is independent evidence.

What the Excel save preserved:

- Excel Tables: BEList, WPList, TaskList, Trips, TravelBands, TravelRates, Equipment, Items.
- 20 data validations plus the country-list validation.
- 3 conditional formats and 6,973 formulas.
- `CountryList` is hidden, as generated, and the file opens on Cover.

## 2. Structure

- **Beneficiaries:** all six are named in `BE list` C4:C9, with acronym, country and a 100% funding rate.
- **Tasks:** all 14 tasks (T1.1–T6.2) are titled and linked to their WPs in `Task List` A4:C17.
- **WP leads:** BE1–BE6 lead WP1–WP6 (`Input Guards` C6:C11).

## 3. Total costs (F) by beneficiary and WP

Source: `Check - Lump sum breakdown` B3:H9. At a 100% funding rate the lump sum (requested funding, column H) equals total costs.

| BE | WP1 | WP2 | WP3 | WP4 | WP5 | WP6 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| BE1 NIT | 210,000.00 | 14,000.00 | 24,250.00 | 15,427.50 | 0.00 | 18,500.00 | 282,177.50 |
| BE2 VARC | 25,390.00 | 280,100.00 | 13,000.00 | 1,427.50 | 15,130.00 | 9,500.00 | 344,547.50 |
| BE3 MASL | 9,890.00 | 14,625.00 | 239,031.25 | 17,640.00 | 11,565.00 | 13,878.75 | 306,630.00 |
| BE4 DDEI | 14,890.00 | 0.00 | 7,500.00 | 163,500.00 | 22,125.00 | 3,750.00 | 211,765.00 |
| BE5 AFIC | 7,765.00 | 36,250.00 | 7,000.00 | 10,500.00 | 164,425.00 | 8,378.75 | 234,318.75 |
| BE6 AKEF | 10,695.00 | 0.00 | 0.00 | 6,375.00 | 12,750.00 | 195,757.50 | 225,577.50 |
| **Total** | 278,630.00 | 344,975.00 | 290,781.25 | 214,870.00 | 225,995.00 | 249,765.00 | **1,605,016.25** |

Every beneficiary and every WP has a non-zero total. Zero cells are partners with no role in that WP.

## 4. Person-months by beneficiary and WP

Source: `Check - Person-months overview` B3:H9.

| BE | WP1 | WP2 | WP3 | WP4 | WP5 | WP6 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| BE1 | **27** | 2 | 3 | 2 | 0 | 1 | 35 |
| BE2 | 3 | **37** | 2 | 0 | 2 | 1 | 45 |
| BE3 | 1 | 3 | **39** | 3 | 2 | 1 | 49 |
| BE4 | 3 | 0 | 2 | **38** | 3 | 1 | 47 |
| BE5 | 1 | 11 | 2 | 3 | **34** | 2 | 53 |
| BE6 | 1 | 0 | 0 | 1 | 2 | **24** | 28 |
| **Total** | 36 | 53 | 48 | 47 | 43 | 30 | **257** |

WP leads are in bold: each carries 63–85% of its WP. Every WP has between three and six contributing partners.

## 5. Representative checks, one per method (hand-calculated)

| Method | Source inputs | Hand calculation | Workbook |
|---|---|---|---|
| Staff effort | BE5 senior: `Staff effort` E68 (T5.1) = 3 PM, E74 (T5.2) = 3 PM; `Rate Table` C8 = 3,900 | 6 × 3,900 = 23,400 | `Transfer View BE5` B173 = 6, C173 = 3,900, D173 = 23,400 |
| Travel | `Travel planner` row 9: BE3, WP4, 2 travellers, 1,975 km, 3 nights, 4 days, Hungary | Band 1,601–2,500 km = 429; 429 + 3 × 135 + 4 × 93 = 1,206; × 2 = 2,412 | `Travel planner` K9 = 1,206, L9 = 2,412 → `Travel summary` D19:E19 = 2 / 2,412 → `Transfer View BE3` D143 = 2,412 |
| Equipment depreciation | `Equipment depreciation` row 6: GPU server, 42,000, 48-month depreciation, 0.75 usage | min(36, 48) / 48 = 0.75; 42,000 × 0.75 × 0.75 = 23,625 (below the 42,000 price) | J6 = 23,625 → `Equipment summary` row 46 → `Transfer View BE3` D104 = 23,625 |
| Itemised (subcontract) | `Itemised list` row 12: BE4, WP4, line B, 1 × 18,000 | 18,000 | G12 = 18,000 → `Itemised list summary` row 235 → `Transfer View BE4` D141 = 18,000 |

## 6. Indirect cost reconciliation

| Case | A+C | E = 25% × (A+C) | Direct (A+B+C+D) | F = direct + E |
|---|---:|---:|---:|---:|
| BE4 WP4 (`Transfer View BE4` D161–D166) | 116,400 | 29,100 | 134,400 (includes B 18,000) | 163,500 |
| BE3 WP3 (`Transfer View BE3` D120–D125) | 191,225 | 47,806.25 | 191,225 | 239,031.25 |
| Project (`Check - Summary per WP`, "all" block) | 1,269,613.00 | 317,403.25 | 1,287,613.00 | 1,605,016.25 |

- **Subcontracting:** B is excluded from the indirect base, as the profile's `indirect_rule` (base groups A and C) requires.
- **Grand total:** the sum of the six beneficiary totals, the sum of the six WP totals, and `Check - Summary per WP` J289 all equal 1,605,016.25.

## 7. Guard status

| Guard (`Cover` row) | Status | Count |
|---|---|---|
| Negative values in numeric inputs (18) | OK | 0 |
| Beneficiary or AE with no country (19) | OK | 0 |
| Work package with no lead (20) | OK | 0 |
| Effort without a rate (21) | OK | 0 |
| Plausibility: personnel rate above 9,000 (22) | OK | 0 |
| Plausibility: PM of one BE in one WP above 45 (23) | OK | 0 |
| Plausibility: cost of one trip above 4,000 (24) | OK | 0 |
| Overall (25) | **OK** | |

The thresholds in `Profile Constants` B10:B12 are demonstration assumptions. The highest rate is 8,200, the most effort by one partner in one WP is 39 PM, and the most expensive trip is 2,904.

## 8. Known limitations and remaining warnings

- **Structural checker on the filled file:** running `check_structure` against the populated file gives 375 messages. All are expected for a filled, Excel-saved workbook:
  - Human Input cells are no longer empty;
  - Excel normalised `TravelBands[[col]]` to the equivalent `TravelBands[col]` in `Travel planner` H4:J23;
  - Excel's save wrote document metadata: "Last Modified By" carries the user's name, and `xl/workbook.xml` records the save path. The engine strips both at build time. They can be removed from the demo copy on request.
- **Travel:** the planner has no origin field. Origins are documented only in the trip list below. There is no call-date or rate-basis choice: the profile ships one basis, C(2024)5405 with the Annex 2a accommodation and subsistence amounts (V1.11). Distances under 400 km have no unit cost, so every trip is at least 400 km.
- **Equipment:** there is no project-use-months input. Months in the project = min(36, depreciation period), assuming purchase in month 1.
- **Cover:** cell A2 keeps the generator's fixed text "Blank workbook…".
- **Funding rate:** 100% for all partners is a demonstration assumption.

Trips:

- **Kick-off in Amsterdam (WP1):** BE2 from Helsinki, BE3 from Madrid, BE4 from Budapest, BE5 from Zagreb, BE6 from Vienna.
- **Technical integration meeting in Budapest (WP4):** BE3 from Madrid, BE1 from Amsterdam, BE2 from Helsinki.
- **Field pilot visit in Osijek (WP5):** BE2 from Helsinki, BE3 from Madrid.
- **Dissemination event in Brussels (WP6):** BE6 from Vienna, BE3 from Madrid, BE5 from Zagreb.

# AGRI-PULSE presenter guide

Workbook: `agripulse-six-partner-budget.xlsx` (this folder). It opens on **Cover**. All amounts are in EUR.

## Five-minute route

| Time | Sheet and cells | Show | Expected figures |
|---|---|---|---|
| 0:00–0:30 | **Cover** rows 5–14, then A17:B25 | Profile `he-lump-sum` 1.0, 6 beneficiaries, tasks `2, 3, 3, 2, 2, 2`, 36 months, four methods, headroom 0. Then the Checks panel. | Seven guards plus the overall status (B18:B25), all **OK** |
| 0:30–1:00 | **BE list** A4:F9 | The six partners with acronym, country and funding rate | NIT/Netherlands … AKEF/Austria, all at 100% |
| 1:00–1:45 | **Task List** A4:C17, then **Input Guards** A6:C11 | 14 tasks linked to WP1–WP6, then the WP leads | T1.1 "Project management and reporting" … T6.2 "Publications and uptake planning"; leads BE1–BE6 in order |
| 1:45–2:15 | **Rate Table** C8:E8 | BE5 (AFIC) monthly rates | Senior 3,900; junior 2,800; technical 2,500 |
| 2:15–2:30 | **Staff effort** rows 68 and 74 | BE5's effort on T5.1 and T5.2: person-months in E:G, costs in M:O | T5.1: 3 / 8 / 10 PM → 11,700 / 22,400 / 25,000. T5.2: 3 / 6 / 4 PM → 11,700 / 16,800 / 10,000 |
| 2:30–3:00 | **Travel planner** row 9, then **Travel summary** row 19 | Madrid → Budapest technical integration meeting (BE3, WP4) | 2 travellers, 1,975 km → band 429; Hungary 135/night × 3, 93/day × 4; 1,206 per traveller; trip 2,412. The summary gives 2 person-trips, 2,412 |
| 3:00–3:20 | **Equipment depreciation** rows 6 and 7 | Depreciation below purchase price, against an item charged in full | GPU server: 42,000 × 0.75 usage × 36/48 → **23,625**. Edge gateways: 9,600 × 1.0 × 36/36 → 9,600 |
| 3:20–3:45 | **Itemised list** row 12 | Subcontract on line B | BE4, WP4, independent security and accessibility audit, 1 × 18,000 |
| 3:45–4:10 | **Transfer View BE4**, WP4 block D132:D166 | Staff and subcontract arrive; indirect costs exclude B | D132 25,200 · D133 48,000 · D134 43,200 · D141 18,000 · D161 (A+C) 116,400 · D162 (direct) 134,400 · D164 (E = 25% × 116,400) 29,100 · D166 (F) **163,500** |
| 4:10–4:30 | **Transfer View BE3** D143, D104, D120:D125 | Travel and equipment arrive | D143 travel 2,412 (WP4) · D104 equipment 23,625 (WP3) · D120 A+C 191,225 · D123 E 47,806.25 · D125 F 239,031.25 |
| 4:30–5:00 | **Check - Lump sum breakdown** B3:J10, then **Check - Summary per WP** J289, **Check - Person-months overview** H9, and back to **Cover** | Partner × WP grid and project totals | H9 **1,605,016.25** (also at Summary per WP J289); 257 person-months; Cover all OK |

Talking point for the BE4 step: the 18,000 subcontract adds to direct costs but not to the indirect base. The profile computes E as 25% of A+C only.

## Expected totals

| BE | Total costs | PM | | WP | Total costs | PM |
|---|---:|---:|---|---|---:|---:|
| BE1 NIT | 282,177.50 | 35 | | WP1 | 278,630.00 | 36 |
| BE2 VARC | 344,547.50 | 45 | | WP2 | 344,975.00 | 53 |
| BE3 MASL | 306,630.00 | 49 | | WP3 | 290,781.25 | 48 |
| BE4 DDEI | 211,765.00 | 47 | | WP4 | 214,870.00 | 47 |
| BE5 AFIC | 234,318.75 | 53 | | WP5 | 225,995.00 | 43 |
| BE6 AKEF | 225,577.50 | 28 | | WP6 | 249,765.00 | 30 |
| **Total** | **1,605,016.25** | **257** | | | **1,605,016.25** | **257** |

## Worksheet inventory

| Sheet | What it contributes | Holds |
|---|---|---|
| Cover | Provenance, fill-in order, Checks panel (A17:C25) | Calculated |
| BE list | Partner names, acronyms, countries, funding rates (A4:F9) | Inputs |
| WP list | Work package names (B4:B9) | Inputs |
| Task List | 14 task titles under their WPs (C4:C17) | Inputs |
| Input Guards | WP leads (C6:C11); flags for missing leads and effort without a rate | Inputs + calculated |
| Profile Constants | Indirect rate 25% (B4), duration 36 (B6), plausibility thresholds (B10:B12) | Reference + inputs |
| CountryList (hidden) | Source for the country dropdown | Reference |
| Rate Table | Monthly rate per partner × staff category (C4:F9) | Inputs |
| Staff effort | Person-months per task × partner × category, with costs | Inputs + calculated |
| Travel planner | 13 trips priced by unit-cost lookup (rows 4–16) | Inputs + calculated |
| Travel summary | Person-trips and cost per partner × WP | Calculated |
| Travel unit costs | Distance bands and country accommodation/subsistence rates | Reference |
| Equipment depreciation | 4 items with eligible depreciation (rows 4–7) | Inputs + calculated |
| Equipment summary | Items and eligible cost per partner × WP × line | Calculated |
| Itemised list | 9 cost lines, including the subcontract (rows 4–12) | Inputs + calculated |
| Itemised list summary | Items and cost per partner × WP × line | Calculated |
| Transfer View BE1–BE6 | Each partner's budget per WP in Official Budget Table row order (A–F) | Calculated |
| Check - Lump sum breakdown | Total costs × funding rate per partner × WP | Calculated |
| Check - Person-months overview | Person-months per partner × WP | Calculated |
| Check - Summary per WP | All partners summed per WP and for the whole project | Calculated |

## If something goes wrong live

- If a figure changes after an accidental edit, close without saving and reopen. The verified original is also at `..\agripulse-six-partner-budget.xlsx`.
- Cover A2 says "Blank workbook…". That is fixed text from the generator and doesn't mean the workbook is empty.

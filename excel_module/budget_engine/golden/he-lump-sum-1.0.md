# Golden Scenario — Horizon Europe lump sum, profile version 1.0

**Owner:** human. **Status:** COMPUTED, AWAITING HUMAN REVIEW. The human confirmed the rules on 2026-11-08. At the human's request, an agent computed the expected figures on 2026-11-08; the human signs off after checking the working in §5.

An agent drafted the inputs and tables. The human confirmed the rules in §3. The human then asked the agent to look up the unit costs and compute §4, so the figures are **not** independent of the agent until the human has checked them. The working in §5 shows every step, so each figure can be checked against the inputs and the cited source pages. The reference model (ticket 15) must reproduce the signed-off figures exactly. Ticket 15 must not be implemented by reading these figures back; it must compute from the rules.

Rules for this file:

- Once the human signs it off (see [Sign-off](#sign-off)), only the human changes expected figures.
- An agent never edits an expected figure to make a check pass. A suspected error is raised with the human.
- The human may change any proposed input before sign-off. Change the matching rows in every table if so.

---

## 1. Shape Parameters

| Parameter | Value |
|---|---|
| Profile | `he-lump-sum` 1.0. Today 1.0 allows only staff effort and has no unit-cost tables. If tickets 08–10 add the other methods as a new version, rename this file to match |
| Beneficiaries | 2 (BE1, BE2) |
| Affiliated Entities | 1, under BE1 (written **AE1.1** here; use whatever numbering ticket 06 settles on) |
| Work packages | 2 (WP1, WP2) |
| Tasks | WP1: 2 tasks (T1.1, T1.2). WP2: none, so effort is at WP grain |
| Duration | 24 months |
| Estimation Methods switched on | staff effort, travel planner, equipment depreciation, itemised list |
| Headroom | profile default (+3). The spare-capacity column blocks stay empty |

## 2. Fake Human Inputs

The names, countries and rates are made up. The countries were picked arbitrarily.

### 2.1 BE list

| BE/AE nr | Role | Name | Acronym | Country | Funding rate |
|---|---|---|---|---|---|
| BE1 | Coordinator | Example Org One | EX1 | Austria | 100% |
| AE1.1 | Affiliated entity | Example Affiliate | EXA | Austria | 100% |
| BE2 | Beneficiary | Example Org Two | EX2 | Portugal | 70% |

### 2.2 WP list and Task List

| WP | Name | Tasks |
|---|---|---|
| WP1 | Example work package A | T1.1 Example task, T1.2 Example task |
| WP2 | Example work package B | — |

### 2.3 Rate Table (EUR per person-month)

| BE/AE | Senior scientists | Junior scientists | Technical personnel |
|---|---|---|---|
| BE1 | 6 000 | 4 000 | 3 000 |
| AE1.1 | — | 4 500 | — |
| BE2 | 5 000 | 3 500 | — |

The other Staff Categories (Administrative, Others, A.2–A.4) are left empty for every BE/AE.

### 2.4 Staff effort (person-months)

| WP / task | BE/AE | Senior | Junior | Technical |
|---|---|---|---|---|
| T1.1 | BE1 | 2 | 4 | — |
| T1.1 | BE2 | — | 6 | — |
| T1.2 | BE1 | 1 | — | 3 |
| T1.2 | AE1.1 | — | 5 | — |
| WP2 | BE1 | 1.5 | 2 | — |
| WP2 | AE1.1 | — | 2 | — |
| WP2 | BE2 | 3 | 8 | — |

### 2.5 Travel planner

These are trips, not unit costs. **The human looks up each unit cost in the source**: C(2024)5405 Annex point 5.1 for travel, and Annex 2a V1.11 for accommodation and subsistence, using the calls-from-13.5.2025 table. The ticket 02 JSON is the agent's extraction and must not be the source here. Each trip's mode is given in the table. Which unit-cost table applies follows from the mode and the distance.

| # | BE/AE | WP | Travellers | Mode | From → to (made up) | One-way distance (km) | Nights | Days | Destination country for accommodation/subsistence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BE1 | WP1 | 2 | air | own city → meeting | 1 100 | 2 | 3 | Belgium |
| 2 | BE2 | WP1 | 1 | air | own city → meeting | 2 900 | 3 | 4 | Belgium |
| 3 | AE1.1 | WP2 | 1 | combined air/rail | own city → workshop | 450 | 1 | 2 | Hungary |

### 2.6 Equipment depreciation

| # | BE/AE | WP | Cost line | Purchase cost (EUR) | Depreciation period (months) | Usage share for the action |
|---|---|---|---|---|---|---|
| 1 | BE2 | WP2 | C.2 Equipment | 12 000 | 36 (longer than the project) | 50% |
| 2 | BE1 | WP1 | C.2 Equipment | 3 000 | 12 (shorter than the project) | 100% |

### 2.7 Itemised list

| # | BE/AE | WP | Cost line | Items | Cost per item (EUR) |
|---|---|---|---|---|---|
| 1 | BE2 | WP1 | C.3 Consumables | 10 | 200 |
| 2 | BE1 | WP2 | C.3 Services for dissemination activities | 2 | 1 500 |
| 3 | AE1.1 | WP2 | C.3 Publication fees | 1 | 2 000 |
| 4 | BE2 | WP2 | B Subcontracting | 1 | 10 000 |

Row 4 is there to show that subcontracting (B) is left out of the indirect-cost base.

---

## 3. Calculation rules to apply

These rules are what the agent understands them to be. **The human confirms or corrects each one before computing.** A rule changed here must also change in tickets 08–11.

The "What the sources say" column was researched by an agent on 2026-11-08 and gives rules only, no amounts. The references are:
- **OBT:** `docs/detailed-budget-table_he-ls-euratom_en.xlsm` v3.6. "Instr. Bn" is a cell on its Instructions sheet.
- **AGA:** `docs/aga_en.pdf`, cited by page.
- **UCD:** the consolidated C(2024)5405 PDF, cited by PDF page.

`docs/Handbook-on-the-lump-sum-funding.pdf` is the Erasmus+ KA2 handbook, so it is not cited for HE.

| Rule | Proposed definition | What the sources say | Confirmed? |
|---|---|---|---|
| Staff cost | person-months × rate of that BE/AE and Staff Category. Task effort rolls up to its WP | Matches. Items = person-months and cost per item = average monthly cost; several people in one category are averaged (Instr. B14). Line total = items × cost per item (`D = B*C`) | x |
| Travel cost per trip | travellers × (travel unit cost for the distance band + nights × accommodation rate + days × subsistence rate) | The structure matches. The travel unit cost is per person per **return** trip. The band is set by the **one-way** distance from the Commission's distance calculator (UCD p11 table 5.1 fn 4–5; AGA p88–89). Accommodation is per night and subsistence per day (AGA p90–91; UCD p9). A subsistence day is a 24-hour period, rounded to the nearest whole day, and any part of the first day counts as a full day (AGA p91). The day counts in §2.5 are taken as already counted that way. The rate country is the destination (inferred: UCD p9 speaks of work trips "outside their place of employment"). The OBT itself does not require the Decision for HE lump sum; it only asks for items × average cost (Instr. B16). Using the Decision is an estimating choice | x |
| Trip 3 table | combined air/rail, 450 km | Table 5.1 covers "return air and combined air/rail journey" (UCD p11), so trip 3 takes the 400–600 km band of 5.1. Air needs a flight-calculator distance of 400 km or more (AGA p92–93). A rail-only trip would use land tables 5.2–5.4 instead, and a route with no land unit cost is paid at actual cost (UCD p7) | x |
| Equipment eligible cost | purchase cost × usage share × min(duration, depreciation period) ÷ depreciation period. This assumes purchase in month 1, since there is no purchase-month input | Matches the OBT "Depreciation costs" sheet: K = purchase cost × "% used for the project" × "% of useful life of the equipment in the project". Depreciation is the default; full purchase cost is allowed only if the topic explicitly permits it (Instr. B16, B19). The min(…) cap is implied (AGA rules apply "based on estimations", Instr. B19). The OBT sheet also records a purchase date | x |
| Itemised cost | items × cost per item | Matches (`D = B*C`, Instr. B13) | x |
| Transfer View "items" | staff lines: person-months. C.1: number of trips. C.2: number of equipment items. Itemised lines: the number of items entered | Items are "several travels, or two pieces of equipment", and cost per item is the average (Instr. B16). **Human decision (2026-11-08):** person-trips, so trip 1 = 2 items | x |
| Transfer View "cost per item" | line total ÷ items (an average where the rates are mixed) | Matches (Instr. B14, B16). The OBT asks for cost per item "preferably" in whole euros, while items may be fractions (Instr. B13). See Rounding | x |
| Indirect costs E | indirect_rate Profile Constant (25%) × (A + C), per BE/AE and WP. B and D are excluded | Matches: `=D38*0.25`, with A + C = rows A.1–A.4 and C.1–C.3. D.2 is excluded too (AGA p110), and so is D.1 (AGA p136–137). The OBT computes E separately for the BE table, the AE table and BE+AE | x |
| Rounding | none until display. Compare figures to the cent | The OBT rounds nothing, except the prefilled A.4 rate (2 decimals). The Planning Workbook's average cost per item can have cents, and a human typing it into the OBT may round it to whole euros, so the OBT total can drift from the Planning Workbook total by up to ½ euro × items. **Proposal:** expected figures unrounded, compared to the cent. The drift is a transfer note, not part of this scenario | x |
| Requested EU contribution | F × funding rate of the BE/AE | Matches the OBT "Lump sum breakdown": `='BE1'!D43*'BE list'!F4`, **per BE/AE × WP**. No rounding. Part A may request less (operating grant, own resources: Instr. B23). Funding rate: RIA/CSA always 100%; IA 70% (exceptionally 60%), up to 100% for non-profits (Instr. B11). The scenario's 70% for BE2 therefore implies an IA topic | x |
| Affiliated Entity | AE1.1 is its own BE/AE with its own Transfer View | The AE has its own BE list row, country and **funding rate**, but **no sheet of its own**. Its costs go in a second table on BE1's sheet, with BE, AE and BE+AE total columns (Instr. B13; `BE tpl` headers). The lump sum breakdown and Part A list "each beneficiary and affiliated entity" (Instr. B11, B23). Expected figures therefore stay per AE, plus a BE1 + AE1.1 column where the OBT shows one. Ticket 06 must lay the Transfer View out the same way | x |
| Person-months overview | PM per BE/AE × WP | Matches the OBT "Person-months overview": `=SUM('BE1'!B9:B16)` = items of A.1–A.4, per row × WP, with total and Pct %. No split by Staff Category | x |

---

## 4. Expected figures

Amounts are in EUR, unrounded and compared to the cent (§3 Rounding). A Transfer View line not listed is empty (zero). C.1 items are person-trips.

### 4.1 Unit costs looked up from the source

Source: `docs/additional-information-on-unit-costs-and-contributions_en.pdf`, *Annex 2a and 2b V1.11 (01.05.2026)*.
- **Travel:** the "for calls with opening date as from 31 July 2024" table for air or combined air/land travel of 400 km or more, PDF p9. It is identical to C(2024)5405 Annex point 5.1, UCD p11.
- **Accommodation:** "as from 13 May 2025", PDF p14 (the table starts on p13).
- **Subsistence:** "as from 13 May 2025", PDF p22 (the table starts on p21).

| Trip | Travel unit cost (source, page) | Accommodation per night (source, page) | Subsistence per day (source, page) | Trip total |
|---|---|---|---|---|
| 1 | 365.00: band 601–1600 km for 1 100 km (Annex 2a p9) | 171.00: Belgium (Annex 2a p14) | 132.00: Belgium (Annex 2a p22) | 2 × (365 + 2 × 171 + 3 × 132) = 2 × 1 103 = **2 206.00** |
| 2 | 541.00: band 2501–3500 km for 2 900 km (Annex 2a p9) | 171.00: Belgium (Annex 2a p14) | 132.00: Belgium (Annex 2a p22) | 1 × (541 + 3 × 171 + 4 × 132) = **1 582.00** |
| 3 | 340.00: band 400–600 km for 450 km, combined air/rail (Annex 2a p9) | 135.00: Hungary (Annex 2a p14) | 93.00: Hungary (Annex 2a p22) | 1 × (340 + 1 × 135 + 2 × 93) = **661.00** |

### 4.2 Transfer View, per BE/AE × WP

#### BE1 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | 3 | 6 000.00 | 18 000.00 |
| A.1 Junior scientists | 4 | 4 000.00 | 16 000.00 |
| A.1 Technical personnel | 3 | 3 000.00 | 9 000.00 |
| C.1 Travel and subsistence | 2 | 1 103.00 | 2 206.00 |
| C.2 Equipment | 1 | 3 000.00 | 3 000.00 |
| **A+C** | | | 48 206.00 |
| **A+B+C+D** | | | 48 206.00 |
| **E** | | | 12 051.50 |
| **F** | | | 60 257.50 |

#### BE1 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | 1.5 | 6 000.00 | 9 000.00 |
| A.1 Junior scientists | 2 | 4 000.00 | 8 000.00 |
| C.3 Services for dissemination activities | 2 | 1 500.00 | 3 000.00 |
| **A+C** | | | 20 000.00 |
| **A+B+C+D** | | | 20 000.00 |
| **E** | | | 5 000.00 |
| **F** | | | 25 000.00 |

#### AE1.1 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Junior scientists | 5 | 4 500.00 | 22 500.00 |
| **A+C** | | | 22 500.00 |
| **A+B+C+D** | | | 22 500.00 |
| **E** | | | 5 625.00 |
| **F** | | | 28 125.00 |

#### AE1.1 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Junior scientists | 2 | 4 500.00 | 9 000.00 |
| C.1 Travel and subsistence | 1 | 661.00 | 661.00 |
| C.3 Publication fees | 1 | 2 000.00 | 2 000.00 |
| **A+C** | | | 11 661.00 |
| **A+B+C+D** | | | 11 661.00 |
| **E** | | | 2 915.25 |
| **F** | | | 14 576.25 |

#### BE2 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Junior scientists | 6 | 3 500.00 | 21 000.00 |
| C.1 Travel and subsistence | 1 | 1 582.00 | 1 582.00 |
| C.3 Consumables | 10 | 200.00 | 2 000.00 |
| **A+C** | | | 24 582.00 |
| **A+B+C+D** | | | 24 582.00 |
| **E** | | | 6 145.50 |
| **F** | | | 30 727.50 |

#### BE2 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | 3 | 5 000.00 | 15 000.00 |
| A.1 Junior scientists | 8 | 3 500.00 | 28 000.00 |
| B Subcontracting | 1 | 10 000.00 | 10 000.00 |
| C.2 Equipment | 1 | 4 000.00 | 4 000.00 |
| **A+C** | | | 47 000.00 |
| **A+B+C+D** | | | 57 000.00 |
| **E** | | | 11 750.00 |
| **F** | | | 68 750.00 |

### 4.3 Check Summaries: category E per BE/AE (all WPs)

| BE/AE | A+C | E |
|---|---|---|
| BE1 | 68 206.00 | 17 051.50 |
| AE1.1 | 34 161.00 | 8 540.25 |
| BE2 | 71 582.00 | 17 895.50 |

### 4.4 Check Summaries: lump sum breakdown

Mirrors the OBT "Estimated breakdown of the lump sum": F × funding rate, per BE/AE × WP, with totals and Pct %.

| BE/AE (funding rate) | WP1 | WP2 | Total | Pct % |
|---|---|---|---|---|
| BE1 (100%) | 60 257.50 | 25 000.00 | 85 257.50 | 43.15% |
| AE1.1 (100%) | 28 125.00 | 14 576.25 | 42 701.25 | 21.61% |
| BE2 (70%) | 21 509.25 | 48 125.00 | 69 634.25 | 35.24% |
| **Total** | 109 891.75 | 87 701.25 | 197 593.00 | 100.00% |
| **Percentage** | 55.62% | 44.38% | 100.00% | |

### 4.4b Cost categories per BE/AE (all WPs)

| BE/AE | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| BE1 | 60 000.00 | 0.00 | 8 206.00 | 0.00 | 17 051.50 | 85 257.50 |
| AE1.1 | 31 500.00 | 0.00 | 2 661.00 | 0.00 | 8 540.25 | 42 701.25 |
| BE2 | 64 000.00 | 10 000.00 | 7 582.00 | 0.00 | 17 895.50 | 99 477.50 |
| **Total** | 155 500.00 | 10 000.00 | 18 449.00 | 0.00 | 43 487.25 | 227 436.25 |

### 4.5 Check Summaries: person-months overview

The OBT overview sums the A.1–A.4 items per BE/AE × WP. It has no Staff Category split (see §3).

| BE/AE | WP1 | WP2 | Total | Pct % |
|---|---|---|---|---|
| BE1 | 10 | 3.5 | 13.5 | 36.00% |
| AE1.1 | 5 | 2 | 7 | 18.67% |
| BE2 | 6 | 11 | 17 | 45.33% |
| **Total** | 21 | 16.5 | 37.5 | 100.00% |
| **Percentage** | 56.00% | 44.00% | 100.00% | |

### 4.6 Check Summaries: per-WP summary and % shares

The shares are of person-months and of total costs F, not of the lump sum. The percentages are shown to two decimals; the comparison uses the unrounded ratio.

| WP | Person-months | % of PM | Total costs F | % of F |
|---|---|---|---|---|
| WP1 | 21 | 56.00% | 119 110.00 | 52.37% |
| WP2 | 16.5 | 44.00% | 108 326.25 | 47.63% |

| BE/AE | Person-months | % of PM | Total costs F | % of F |
|---|---|---|---|---|
| BE1 | 13.5 | 36.00% | 85 257.50 | 37.49% |
| AE1.1 | 7 | 18.67% | 42 701.25 | 18.78% |
| BE1 + AE1.1 | 20.5 | 54.67% | 127 958.75 | 56.26% |
| BE2 | 17 | 45.33% | 99 477.50 | 43.74% |

The AE shares are shown separately here, with a BE1 + AE1.1 row matching the OBT's BE+AE total column.

---

## 5. Working

**Staff (A.1).** Task effort rolls up to its WP: T1.1 + T1.2 = WP1. Cost = PM × rate.
- BE1 WP1:
  - Senior: 2 (T1.1) + 1 (T1.2) = 3 PM × 6 000 = 18 000.
  - Junior: 4 PM (T1.1) × 4 000 = 16 000.
  - Technical: 3 PM (T1.2) × 3 000 = 9 000.
  - A = 43 000.
- BE1 WP2: Senior 1.5 × 6 000 = 9 000. Junior 2 × 4 000 = 8 000. A = 17 000.
- AE1.1 WP1: Junior 5 (T1.2) × 4 500 = 22 500. A = 22 500.
- AE1.1 WP2: Junior 2 × 4 500 = 9 000. A = 9 000.
- BE2 WP1: Junior 6 (T1.1) × 3 500 = 21 000. A = 21 000.
- BE2 WP2: Senior 3 × 5 000 = 15 000. Junior 8 × 3 500 = 28 000. A = 43 000.

**Travel (C.1).** Per traveller: travel unit cost + nights × accommodation + days × subsistence. Items = person-trips. See §4.1.
- Trip 1 (BE1 WP1): 365 + 342 + 396 = 1 103 per traveller. × 2 = 2 206, so 2 items at 1 103.
- Trip 2 (BE2 WP1): 541 + 513 + 528 = 1 582, so 1 item.
- Trip 3 (AE1.1 WP2): 340 + 135 + 186 = 661, so 1 item.

**Equipment (C.2).** Purchase × usage × min(24, period) ÷ period.
- #1 (BE2 WP2): 12 000 × 0.5 × 24 / 36 = 4 000, so 1 item.
- #2 (BE1 WP1): 3 000 × 1 × 12 / 12 = 3 000, so 1 item.

**Itemised (C.3, B).**
- BE2 WP1 Consumables: 10 × 200 = 2 000.
- BE1 WP2 Dissemination: 2 × 1 500 = 3 000.
- AE1.1 WP2 Publication: 1 × 2 000 = 2 000.
- BE2 WP2 Subcontracting (B): 1 × 10 000 = 10 000.

**Per BE/AE × WP.** A+C = A + C; E = 0.25 × (A+C); F = A + B + C + D + E.

| BE/AE × WP | A | B | C | A+C | E | F |
|---|---|---|---|---|---|---|
| BE1 WP1 | 43 000 | 0 | 2 206 + 3 000 = 5 206 | 48 206 | 12 051.50 | 48 206 + 12 051.50 = 60 257.50 |
| BE1 WP2 | 17 000 | 0 | 3 000 | 20 000 | 5 000.00 | 25 000.00 |
| AE1.1 WP1 | 22 500 | 0 | 0 | 22 500 | 5 625.00 | 28 125.00 |
| AE1.1 WP2 | 9 000 | 0 | 661 + 2 000 = 2 661 | 11 661 | 2 915.25 | 14 576.25 |
| BE2 WP1 | 21 000 | 0 | 1 582 + 2 000 = 3 582 | 24 582 | 6 145.50 | 30 727.50 |
| BE2 WP2 | 43 000 | 10 000 | 4 000 | 47 000 | 11 750.00 | 57 000 + 11 750 = 68 750.00 |

**Roll-ups.**
- **E per BE/AE (4.3):**
  - BE1: A+C = 48 206 + 20 000 = 68 206, and E = 12 051.50 + 5 000 = 17 051.50 (= 0.25 × 68 206).
  - AE1.1: A+C = 22 500 + 11 661 = 34 161, and E = 8 540.25.
  - BE2: A+C = 24 582 + 47 000 = 71 582, and E = 17 895.50.
- **Lump sum (4.4):** F × funding rate.
  - BE2 WP1: 30 727.50 × 0.7 = 21 509.25.
  - BE2 WP2: 68 750 × 0.7 = 48 125.00.
  - BE1 and AE1.1 are at 100%.
  - Total = 85 257.50 + 42 701.25 + 69 634.25 = 197 593.00.
  - Each Pct % = row total ÷ 197 593.00.
- **Categories (4.4b):** sums of the table above over WP1 and WP2.
  - Check: 155 500 + 10 000 + 18 449 + 43 487.25 = 227 436.25.
  - Check: F of BE2 = 30 727.50 + 68 750 = 99 477.50.
- **Person-months (4.5):**
  - BE1: WP1 = 3 + 4 + 3 = 10; WP2 = 1.5 + 2 = 3.5.
  - AE1.1: 5 and 2.
  - BE2: 6 and 3 + 8 = 11.
  - Total 37.5. Each share = PM ÷ 37.5.
- **Per WP (4.6):**
  - F of WP1 = 60 257.50 + 28 125 + 30 727.50 = 119 110.00.
  - F of WP2 = 25 000 + 14 576.25 + 68 750 = 108 326.25.
  - Sum = 227 436.25 = the 4.4b total.

The agent cross-checked these figures with a calculator script written separately from the engine code.

---

## Sign-off

| | |
|---|---|
| Computed by | Agent (Claude), at the human's request, 2026-11-08. Rules confirmed by the human, 2026-11-08 |
| Date | |
| Reviewed by | *(human: check §4.1 against Annex 2a p9/p14/p22 and the arithmetic in §5, then sign here)* |
| Status | ☐ human-owned. From this point only the human changes expected figures |

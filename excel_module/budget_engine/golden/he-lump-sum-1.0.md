# Golden Scenario — Horizon Europe lump sum, profile version 1.0

**Owner:** human. **Status:** SCAFFOLD. The inputs are proposed and no expected figure is filled in yet.

An agent drafted the inputs and the empty tables below. Every expected figure, and every unit cost looked up from a source table, is left blank on purpose: the human works them out by hand. The reference model (ticket 15) must then reproduce them exactly. That only proves something if no agent produced the numbers.

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
| Staff cost | person-months × rate of that BE/AE and Staff Category. Task effort rolls up to its WP | Matches. Items = person-months and cost per item = average monthly cost; several people in one category are averaged (Instr. B14). Line total = items × cost per item (`D = B*C`) | ☐ |
| Travel cost per trip | travellers × (travel unit cost for the distance band + nights × accommodation rate + days × subsistence rate) | The structure matches. The travel unit cost is per person per **return** trip. The band is set by the **one-way** distance from the Commission's distance calculator (UCD p11 table 5.1 fn 4–5; AGA p88–89). Accommodation is per night and subsistence per day (AGA p90–91; UCD p9). A subsistence day is a 24-hour period, rounded to the nearest whole day, and any part of the first day counts as a full day (AGA p91). The day counts in §2.5 are taken as already counted that way. The rate country is the destination (inferred: UCD p9 speaks of work trips "outside their place of employment"). The OBT itself does not require the Decision for HE lump sum; it only asks for items × average cost (Instr. B16). Using the Decision is an estimating choice | ☐ |
| Trip 3 table | combined air/rail, 450 km | Table 5.1 covers "return air and combined air/rail journey" (UCD p11), so trip 3 takes the 400–600 km band of 5.1. Air needs a flight-calculator distance of 400 km or more (AGA p92–93). A rail-only trip would use land tables 5.2–5.4 instead, and a route with no land unit cost is paid at actual cost (UCD p7) | ☐ |
| Equipment eligible cost | purchase cost × usage share × min(duration, depreciation period) ÷ depreciation period. This assumes purchase in month 1, since there is no purchase-month input | Matches the OBT "Depreciation costs" sheet: K = purchase cost × "% used for the project" × "% of useful life of the equipment in the project". Depreciation is the default; full purchase cost is allowed only if the topic explicitly permits it (Instr. B16, B19). The min(…) cap is implied (AGA rules apply "based on estimations", Instr. B19). The OBT sheet also records a purchase date | ☐ |
| Itemised cost | items × cost per item | Matches (`D = B*C`, Instr. B13) | ☐ |
| Transfer View "items" | staff lines: person-months. C.1: number of trips. C.2: number of equipment items. Itemised lines: the number of items entered | Items are "several travels, or two pieces of equipment", and cost per item is the average (Instr. B16). **Not settled:** whether a trip with 2 travellers is 1 item or 2. The unit cost is per person per return trip, which suggests **person-trips** (trip 1 = 2 items). Human decision | ☐ |
| Transfer View "cost per item" | line total ÷ items (an average where the rates are mixed) | Matches (Instr. B14, B16). The OBT asks for cost per item "preferably" in whole euros, while items may be fractions (Instr. B13). See Rounding | ☐ |
| Indirect costs E | indirect_rate Profile Constant (25%) × (A + C), per BE/AE and WP. B and D are excluded | Matches: `=D38*0.25`, with A + C = rows A.1–A.4 and C.1–C.3. D.2 is excluded too (AGA p110), and so is D.1 (AGA p136–137). The OBT computes E separately for the BE table, the AE table and BE+AE | ☐ |
| Rounding | none until display. Compare figures to the cent | The OBT rounds nothing, except the prefilled A.4 rate (2 decimals). The Planning Workbook's average cost per item can have cents, and a human typing it into the OBT may round it to whole euros, so the OBT total can drift from the Planning Workbook total by up to ½ euro × items. **Proposal:** expected figures unrounded, compared to the cent. The drift is a transfer note, not part of this scenario | ☐ |
| Requested EU contribution | F × funding rate of the BE/AE | Matches the OBT "Lump sum breakdown": `='BE1'!D43*'BE list'!F4`, **per BE/AE × WP**. No rounding. Part A may request less (operating grant, own resources: Instr. B23). Funding rate: RIA/CSA always 100%; IA 70% (exceptionally 60%), up to 100% for non-profits (Instr. B11). The scenario's 70% for BE2 therefore implies an IA topic | ☐ |
| Affiliated Entity | AE1.1 is its own BE/AE with its own Transfer View | The AE has its own BE list row, country and **funding rate**, but **no sheet of its own**. Its costs go in a second table on BE1's sheet, with BE, AE and BE+AE total columns (Instr. B13; `BE tpl` headers). The lump sum breakdown and Part A list "each beneficiary and affiliated entity" (Instr. B11, B23). Expected figures therefore stay per AE, plus a BE1 + AE1.1 column where the OBT shows one. Ticket 06 must lay the Transfer View out the same way | ☐ |
| Person-months overview | PM per BE/AE × WP | Matches the OBT "Person-months overview": `=SUM('BE1'!B9:B16)` = items of A.1–A.4, per row × WP, with total and Pct %. No split by Staff Category | ☐ |

---

## 4. Expected figures (for the human to fill in)

Show the working under each table, or in [§5](#5-working), so a reviewer can follow every number.

### 4.1 Unit costs looked up from the source

| Trip | Travel unit cost (source, page) | Accommodation per night (source, page) | Subsistence per day (source, page) | Trip total |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### 4.2 Transfer View, per BE/AE × WP

Fill in one table per combination: BE1/WP1, BE1/WP2, AE1.1/WP1, AE1.1/WP2, BE2/WP1, BE2/WP2. Leave a line empty when it is zero. AE1.1/WP1 has staff effort only, from T1.2.

#### BE1 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

#### BE1 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

#### AE1.1 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

#### AE1.1 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

#### BE2 — WP1

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

#### BE2 — WP2

| Cost line | Items | Cost per item | Total |
|---|---|---|---|
| A.1 Senior scientists | | | |
| A.1 Junior scientists | | | |
| A.1 Technical personnel | | | |
| C.1 Travel and subsistence | | | |
| C.2 Equipment | | | |
| C.3 (each line used) | | | |
| B Subcontracting | | | |
| **A+C** | | | |
| **A+B+C+D** | | | |
| **E** | | | |
| **F** | | | |

### 4.3 Check Summaries: category E per BE/AE (all WPs)

| BE/AE | A+C | E |
|---|---|---|
| BE1 | | |
| AE1.1 | | |
| BE2 | | |

### 4.4 Check Summaries: lump sum breakdown

Mirrors the OBT "Estimated breakdown of the lump sum": F × funding rate, per BE/AE × WP, with totals and Pct %. An agent reshaped this table on 2026-11-08 to match the OBT's own structure; the per-category view moved to 4.4b.

| BE/AE (funding rate) | WP1 | WP2 | Total | Pct % |
|---|---|---|---|---|
| BE1 (100%) | | | | |
| AE1.1 (100%) | | | | |
| BE2 (70%) | | | | |
| **Total** | | | | |
| **Percentage** | | | | |

### 4.4b Cost categories per BE/AE (all WPs)

| BE/AE | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| BE1 | | | | | | |
| AE1.1 | | | | | | |
| BE2 | | | | | | |
| **Total** | | | | | | |

### 4.5 Check Summaries: person-months overview

The OBT overview sums A.1–A.4 items per BE/AE × WP; it has no Staff Category split (see §3).

| BE/AE | WP1 | WP2 | Total |
|---|---|---|---|
| BE1 | | | |
| AE1.1 | | | |
| BE2 | | | |
| **Total** | | | |

### 4.6 Check Summaries: per-WP summary and % shares

| WP | Person-months | % of PM | Total costs F | % of F |
|---|---|---|---|---|
| WP1 | | | | |
| WP2 | | | | |

| BE/AE | Person-months | % of PM | Total costs F | % of F |
|---|---|---|---|---|
| BE1 | | | | |
| AE1.1 | | | | |
| BE2 | | | | |

The AE shares are shown separately here. If the Official Budget Table folds AEs into their Beneficiary for shares, say so here and add a BE1 + AE1.1 row.

---

## 5. Working

*(Human: show each computation, in a form like "BEx WPy line = effort × rate = total".)*

---

## Sign-off

| | |
|---|---|
| Computed by | |
| Date | |
| Reviewed by (optional) | |
| Status | ☐ human-owned. From this point only the human changes expected figures |

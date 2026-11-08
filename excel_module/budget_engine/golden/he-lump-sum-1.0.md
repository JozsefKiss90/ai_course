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

| Rule | Proposed definition | Confirmed? |
|---|---|---|
| Staff cost | person-months × rate of that BE/AE and Staff Category. Task effort rolls up to its WP | ☐ |
| Travel cost per trip | travellers × (travel unit cost for the distance band + nights × accommodation rate + days × subsistence rate) | ☐ |
| Equipment eligible cost | purchase cost × usage share × min(duration, depreciation period) ÷ depreciation period. This assumes purchase in month 1, since there is no purchase-month input. Check whether HE lump sum allows full purchase cost instead | ☐ |
| Itemised cost | items × cost per item | ☐ |
| Transfer View "items" | staff lines: person-months. C.1: number of trips (or person-trips? Trip 1 has 2 travellers. Check the Official Budget Table's unit). C.2: number of equipment items. Itemised lines: the number of items entered | ☐ |
| Transfer View "cost per item" | line total ÷ items (an average where the rates are mixed) | ☐ |
| Indirect costs E | indirect_rate Profile Constant (25%) × (A + C), per BE/AE and WP. B and D are excluded | ☐ |
| Rounding | none until display. Compare figures to the cent. Check how the Official Budget Table rounds averages | ☐ |
| Requested EU contribution | F × funding rate of the BE/AE | ☐ |

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

Mirrors the Official Budget Table summary.

| BE/AE | A | B | C | D | E | F | Funding rate | Requested EU contribution |
|---|---|---|---|---|---|---|---|---|
| BE1 | | | | | | | 100% | |
| AE1.1 | | | | | | | 100% | |
| BE2 | | | | | | | 70% | |
| **Total** | | | | | | | | |

### 4.5 Check Summaries: person-months overview

If the Official Budget Table's overview also splits by Staff Category, add those columns.

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

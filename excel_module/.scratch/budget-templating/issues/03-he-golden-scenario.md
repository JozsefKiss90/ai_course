# 03 — Hand-compute the HE Golden Scenario

**What to build:** The human-owned Golden Scenario for the Horizon Europe lump sum Funding Profile: a small set of obviously fake Shape Parameters and Human Inputs plus expected Transfer View and Check Summaries figures, worked out by hand once and committed. The reference model must reproduce it exactly.

**Blocked by:** None — can start immediately. (Ticket 15 consumes it.)

**Status:** ready-for-human

- [x] Shape Parameters chosen: at least two Beneficiaries, one Affiliated Entity, two or more work packages, tasks on at least one WP
- [x] Fake Human Inputs exercise all four v1 Estimation Methods: staff effort, travel planner, equipment depreciation, itemised list
- [x] Inputs are obviously fake (no real names, countries chosen arbitrarily, round synthetic rates)
- [ ] Expected figures computed by hand: items and average cost per item per BE/AE × WP × cost line, category E, the lump sum breakdown, person-months overview, per-WP summary and % shares
- [x] Working shown so a reviewer can follow every figure
- [ ] Committed and marked human-owned; changes require explicit human approval

## Comments

- **2026-11-08, agent:** the human chose "scaffold only". The worksheet is `budget_engine/golden/he-lump-sum-1.0.md`. It holds proposed fake Shape Parameters and Human Inputs covering all four v1 Estimation Methods, proposed calculation rules for the human to confirm, and blank expected-figure tables with a working section and a sign-off block. All checkboxes above stay open until the human computes the figures and signs the file off.
- **2026-11-08, agent:** the human chose "research the rules". §3 of the worksheet now has a "What the sources say" column with OBT / AGA / UCD citations for every rule; it gives rules only, no amounts and no figures. Every "Confirmed?" box is left for the human.
  - **Decisions still open for the human:** is a trip with 2 travellers 1 C.1 item or 2? Confirm the rounding proposal, and the destination-country reading for subsistence.
  - **Corrections the research found:**
    - An AE has no sheet of its own; it is a second table on its Beneficiary's sheet, with its own funding rate.
    - The OBT lump sum breakdown is F × funding rate per BE/AE × WP. §4.4 was reshaped to match, and the per-category table moved to §4.4b.
    - Trip 3, combined air/rail, takes table 5.1's 400–600 km band.
  - `docs/Handbook-on-the-lump-sum-funding.pdf` is the Erasmus+ KA2 handbook, but profile `he-lump-sum` 1.0 lists it in its provenance. That needs fixing before the version is accepted.
- **2026-11-08, agent:** the human made the open decisions (2 travellers = 2 C.1 items; rounding and destination country confirmed), ticked every §3 rule, and asked the agent to compute §4.
  - Unit costs come from Annex 2a V1.11 (`docs/additional-information-on-unit-costs-and-contributions_en.pdf`): p9 for travel (identical to C(2024)5405 point 5.1), p14 for accommodation and p22 for subsistence.
  - §4.2–4.6 are filled in with full working in §5. A calculator script written separately from the engine code cross-checked the figures.
  - **Still open:** "computed by hand" is not ticked, because an agent computed the figures. It counts as done once the human has checked §4.1 and §5. "Marked human-owned" waits for the human's sign-off in the worksheet. After that, set the status to done.

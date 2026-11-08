# 03 — Hand-compute the HE Golden Scenario

**What to build:** The human-owned Golden Scenario for the Horizon Europe lump sum Funding Profile: a small set of obviously fake Shape Parameters and Human Inputs plus expected Transfer View and Check Summaries figures, worked out by hand once and committed. The reference model must reproduce it exactly.

**Blocked by:** None — can start immediately. (Ticket 15 consumes it.)

**Status:** ready-for-human

- [ ] Shape Parameters chosen: at least two Beneficiaries, one Affiliated Entity, two or more work packages, tasks on at least one WP
- [ ] Fake Human Inputs exercise all four v1 Estimation Methods: staff effort, travel planner, equipment depreciation, itemised list
- [ ] Inputs are obviously fake (no real names, countries chosen arbitrarily, round synthetic rates)
- [ ] Expected figures computed by hand: items and average cost per item per BE/AE × WP × cost line, category E, the lump sum breakdown, person-months overview, per-WP summary and % shares
- [ ] Working shown so a reviewer can follow every figure
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

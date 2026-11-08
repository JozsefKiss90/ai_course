# 11 — Full HE Transfer View and Check Summaries

**What to build:**
- **Transfer View** per BE/AE, laid out row for row like the Official Budget Table. It covers every cost category (A.1–A.4, B, C.1–C.3, D.1–D.5 and E) and shows the number of items and average cost per item per WP, in the Official Budget Table's units. The figures can be copied straight into its input cells.
- **Check Summaries** that mirror the Official Budget Table's lump sum breakdown, person-months overview and per-WP summary.
- **% shares** of effort and budget per WP and per Beneficiary.

**Blocked by:** 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Transfer View row order taken from the profile's Submission Budget layout data, not hard-coded in a builder
- [ ] Rows present for every category, including ones no v1 method fills (D.2–D.5)
- [ ] Indirect costs (E) computed by the profile's rule, never entered by hand
- [ ] Check Summaries: lump sum breakdown, person-months overview, per-WP summary
- [ ] % shares per WP and per Beneficiary for effort and budget
- [ ] Summaries use formulas only, no PivotTables
- [ ] Synthetic Check compares the full Transfer View and Check Summaries with the reference model

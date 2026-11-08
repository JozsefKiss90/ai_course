# 11 — Full HE Transfer View and Check Summaries

**What to build:**
- **Transfer View** per BE/AE, laid out row for row like the Official Budget Table. It covers every cost category (A.1–A.4, B, C.1–C.3, D.1–D.5 and E) and shows the number of items and average cost per item per WP, in the Official Budget Table's units. The figures can be copied straight into its input cells.
- **Check Summaries** that mirror the Official Budget Table's lump sum breakdown, person-months overview and per-WP summary.
- **% shares** of effort and budget per WP and per Beneficiary.

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Transfer View row order taken from the profile's Submission Budget layout data, not hard-coded in a builder
- [x] Rows present for every category, including ones no v1 method fills (D.2–D.5)
- [x] Indirect costs (E) computed by the profile's rule, never entered by hand
- [x] Check Summaries: lump sum breakdown, person-months overview, per-WP summary
- [x] % shares per WP and per Beneficiary for effort and budget
- [x] Summaries use formulas only, no PivotTables
- [x] Synthetic Check compares the full Transfer View and Check Summaries with the reference model

## Notes (implementation)

- The Transfer View already followed the profile's `transfer_view.rows`. Its rows are now written by `sheets/breakdown.py`, which the summary per WP shares. Totals, indirect costs (E = rate x (A+C), from the labelled Profile Constant) and the grand total come from the profile's row rules in every total column. Lines no switched-on method fills keep their labelled, blank row (tested with staff effort alone).
- Three Check Summary sheets follow the Transfer Views, named after the Official Budget Table's sheets: `Check - Lump sum breakdown`, `Check - Person-months overview` and `Check - Summary per WP`. Their sheets, titles, headers, the Transfer View row the lump sum is taken of (`F`) and the effort categories (`A`) are profile data (`check_summaries` in he-lump-sum 1.0).
- Lump sum and person-month grids: one row per BE/AE block (spare blocks included) x one column per WP. Each grid has a row total and a % share per block (last column), and a column total and a % share per WP (last two rows). Lump sum = the block's Transfer View F total x its funding rate. The rate is looked up from `BE list` by code and shown in a `Funding rate` column. Person-months = the items of the A lines.
- Summary per WP: per WP and for all WPs, split into all Beneficiaries, all AEs and both (items, cost per item, total). A spare block counts as an AE when the code typed in for it contains `-AE`. The match is case-sensitive (FIND), like `shape.is_affiliated`, and a helper column (`Spare block` / `Counted as`) shows the result.
- Every summary figure is a formula; the structural checks reject a typed-in figure and check row labels and order.
- Synthetic Check: the reference model adds up the expected Transfer Views. It takes the funding rates from the inputs, and a late AE in a spare block counts with the AEs. Every registered summary cell is compared. The provisional scenario now gives BE2 and its AEs a 70% funding rate. Two sabotage tests are included: a lump sum that ignores the funding rate, and a late AE counted as a Beneficiary.

### Decisions / known gaps

- The grids have one row per BE/AE block, so the "% share per Beneficiary" is per block. The Official Budget Table has one row per Beneficiary, with its AEs inside the BE sheet. A Beneficiary's share including its AEs is the sum of its rows' shares; no rollup row is built. To confirm this is acceptable.
- Shares show 0, not the Official's `" "`, when the total is 0.
- The Official's "with affiliated entities" group has a fourth column, `TOTAL COSTS` (= `BE+TP TOTAL COSTS`). The mirror shows only the three distinct columns.
- The Lump Sum Tier gap (PRD line 27) is KA220-only (tickets 18-21); the HE profile has no tier.
- `check_summaries` was added to he-lump-sum 1.0 in place, as tickets 07-10 did, since 1.0 is not yet accepted (ticket 15 pins its Golden Scenario).
- Grid row labels and WP header names are formulas the Synthetic Check does not value-check; Transfer View names are.
- A WP a human adds to `WP list` gets no summary column or block until a rebuild (same gap as tickets 06-10).
- Review follow-up: `_build_per_wp` is dense (nested closures), and the column groups are bare 3-tuples. Consider a small typed `check_summaries` profile model and a NamedTuple for (items, avg, total) when KA220 adds its own summaries.

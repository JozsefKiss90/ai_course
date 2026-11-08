# 12 — Input Guards and the Checks panel

**What to build:** Input Guards across the Planning Workbook, and a Checks panel on the Cover Sheet showing OK / warning / error per guard. The guards are:
- **Data validation** on input cells: lists, number ranges, non-negative values.
- **Completeness flags**: a Beneficiary with no country, a WP with no lead, effort without a rate.
- **Plausibility warnings** (soft): each threshold is a blank, human-filled Profile Constant, and a warning stays silent while its threshold is empty.
- **Profile rule checks**: a hook for the Funding Profile's own rules.

**Blocked by:** 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Data validation applied to Human Input cells; anything openpyxl cannot express faithfully written with lxml
- [ ] Completeness flags evaluate by formula
- [ ] Plausibility thresholds are empty labelled cells; a guard with no threshold reports OK
- [ ] Profile rule checks declared in profile data are rendered as guards (HE may declare none)
- [ ] Guards conditionally coloured; Checks panel aggregates every guard
- [ ] Structural checks confirm validation is present on Human Input cells
- [ ] Synthetic Check includes scenarios that trip a completeness flag and a plausibility warning, and verifies the panel state after recalculation

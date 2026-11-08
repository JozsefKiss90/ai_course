# 21 — KA220 Funding Profile

**What to build:** Builds under the Erasmus+ KA220 Cooperation Partnerships Funding Profile:
- Effort is entered in days.
- Daily rates are derived by formula from each Beneficiary's country group, with a manual override cell.
- The Transfer View shows the amount per work package, in the application form's layout.
- The planner enters a chosen Lump Sum Tier (€120k / €250k / €400k) and sees the gap between the bottom-up estimate and the tier.
- Per-WP limits found in ticket 19 become profile rule checks.
- Default headroom is +2.
- Source provenance is the 2026 Programme Guide.

**Optional KA220 track:** skippable. No HE or engine ticket depends on it.

**Blocked by:** 11 — Full HE Transfer View and Check Summaries; 12 — Input Guards; 18 — KA220 form layout; 19 — KA220 per-WP limits

**Status:** ready-for-agent

- [ ] KA220 profile added as data only (no engine change needed beyond genuinely profile-independent generalisations)
- [ ] Country-group daily-rate table with provenance; override cell takes precedence when filled
- [ ] Transfer View per WP matching the form layout from ticket 18
- [ ] Lump Sum Tier input validated against the profile's tiers; gap shown in Check Summaries and Checks panel
- [ ] Rule checks from ticket 19 rendered as Input Guards
- [ ] Structural checks pass for KA220 builds
- [ ] Synthetic Check passes with a provisional KA220 scenario flagged as not human-owned
- [ ] `budget-planner` interview offers KA220 if ticket 14 is done

# 08 — Travel planner Estimation Method

**What to build:** A travel planner sheet, switched on via the method switches.
- Trips are entered per BE/AE and WP and priced with the Commission's travel and subsistence unit costs from the HE Funding Profile.
- The travel summary is built with formulas: no PivotTable, no hidden row order, no manual refresh.
- The method outputs items and total per BE/AE × WP × cost line, in the shape the Transfer View consumes.
- The method supplies its own reference-model function.

**Blocked by:** 02 — HE travel unit costs; 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Unit-cost tables from ticket 02 added to the HE profile data with provenance
- [ ] Trip rows grow through an Excel Table; trip inputs are Human Inputs
- [ ] Prices looked up by formula from the unit-cost tables; no constants in formulas
- [ ] Formula-based travel summary feeds the Transfer View's travel cost line
- [ ] Method output follows the Estimation Method contract
- [ ] Reference-model function added; Synthetic Check covers trips across several BE/AE and WPs
- [ ] Structural checks confirm no PivotTable

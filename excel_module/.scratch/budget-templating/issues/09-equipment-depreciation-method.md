# 09 — Equipment depreciation Estimation Method

**What to build:** An equipment depreciation sheet, switched on via the method switches, that costs only the eligible share of each equipment item over the project duration. It outputs items and total per BE/AE × WP × cost line in the Estimation Method contract shape and supplies its reference-model function.

**Blocked by:** 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Equipment rows grow through an Excel Table; purchase cost, depreciation period and usage share are Human Inputs
- [ ] Eligible share uses project duration and Profile Constants; no constants in formulas
- [ ] Output feeds the correct Transfer View cost line
- [ ] Reference-model function added; Synthetic Check covers items with depreciation longer and shorter than the project

# 09 — Equipment depreciation Estimation Method

**What to build:** An equipment depreciation sheet, switched on via the method switches, that costs only the eligible share of each equipment item over the project duration. It outputs items and total per BE/AE × WP × cost line in the Estimation Method contract shape and supplies its reference-model function.

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Equipment rows grow through an Excel Table; purchase cost, depreciation period and usage share are Human Inputs
- [x] Eligible share uses project duration and Profile Constants; no constants in formulas
- [x] Output feeds the correct Transfer View cost line
- [x] Reference-model function added; Synthetic Check covers items with depreciation longer and shorter than the project

## Notes (implementation)

- Profile `he-lump-sum` 1.0: `equipment_depreciation` is allowed and on by default (switch it off by leaving it out of `methods`). `method_settings.equipment_depreciation.cost_lines` lists the three C.2 lines (`C2_equipment`, `C2_infrastructure`, `C2_other_assets`). Profile 1.0 was edited in place, as in ticket 08: no Golden Scenario is pinned yet (ticket 15).
- The project duration now has its own labelled row on `Profile Constants` ("Project duration (months)", source: Shape Parameter). Formulas reference that cell. A structural check confirms it equals `duration_months`.
- `Equipment depreciation` sheet: Excel Table `Equipment`, 10 blank rows. Human Inputs `("equipment", n, field)`: BE/AE nr, WP, Cost line (a list of the three C.2 labels from the Transfer View rows), Item, Purchase cost, Depreciation period (months), Usage share for the action. Calculated columns: months in the project = MIN(duration, period); share of useful life = months ÷ period; eligible cost = cost × usage × share. This is the Golden Scenario rule and the OBT "Depreciation costs" K column. Purchase is assumed in month 1.
- `Equipment summary`: one row per BE/AE block × WP × C.2 line. Items = COUNTIFS of rows with a purchase cost above 0; total = SUMIFS of eligible cost. Each row feeds its own C.2 line of the Transfer View. A spare block sums only once a code is typed for it.
- Synthetic Check: the provisional scenario enters 6 items across the BE/AEs (the late AE included), WPs and C.2 lines. Periods are 3× the duration (longer), a third of it (shorter), equal to it, duration + 12, blank, plus one row with a period but no cost. It then appends item 11 to the Table with inputs only. A sabotage test drops the MIN cap and fails the check.
- The spare-block sabotage test helper in `test_synthetic_check.py` matched any ref on row 5. The equipment summary also has one, so the helper now matches only `Staff effort` refs.

### Known gaps / follow-ups

- No purchase-month input: an item bought late in the project is costed as if bought in month 1. The OBT sheet records a purchase date. Adding one would need a "months remaining" rule.
- Full purchase cost (allowed only where the topic permits it, Instr. B16/B19) is not modelled.
- A WP a human adds to `WP list` gets no summary rows until a rebuild (the same gap as in tickets 06–08).

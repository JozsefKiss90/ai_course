# 08 — Travel planner Estimation Method

**What to build:** A travel planner sheet, switched on via the method switches.
- Trips are entered per BE/AE and WP and priced with the Commission's travel and subsistence unit costs from the HE Funding Profile.
- The travel summary is built with formulas: no PivotTable, no hidden row order, no manual refresh.
- The method outputs items and total per BE/AE × WP × cost line, in the shape the Transfer View consumes.
- The method supplies its own reference-model function.

**Blocked by:** 02 — HE travel unit costs; 05 — Synthetic Check harness

**Status:** done

- [x] Unit-cost tables from ticket 02 added to the HE profile data with provenance (table 5.1 and the current accommodation/subsistence table; land tables 5.2-5.4 are a follow-up, see notes)
- [x] Trip rows grow through an Excel Table; trip inputs are Human Inputs
- [x] Prices looked up by formula from the unit-cost tables; no constants in formulas
- [x] Formula-based travel summary feeds the Transfer View's travel cost line
- [x] Method output follows the Estimation Method contract
- [x] Reference-model function added; Synthetic Check covers trips across several BE/AE and WPs
- [x] Structural checks confirm no PivotTable

## Notes (implementation)

- Profile `he-lump-sum` 1.0: `travel_planner` is allowed and on by default (switch it off with `methods: ["staff_effort"]`). `unit_cost_tables` points at the ticket 02 JSON: `travel_bands` (C(2024)5405 Annex 5.1) and `subsistence` (calls from 13.5.2025, Annex 2a V1.11, recorded as its own source). `method_settings.travel_planner.cost_line` is `C1`. Both sources are in the profile's provenance. Profile 1.0 was edited in place: it has no pinned Golden Scenario yet (ticket 15).
- `Travel planner` sheet: Excel Table `Trips`, 20 blank rows. Human Inputs `("trip", n, field)`: BE/AE nr, WP, Travellers, One-way distance (km), Nights, Days, Destination country, with list and number validation. The price columns are Table calculated columns, so a row added to the Table is priced too: travel by INDEX/MATCH on the band's `From km`, accommodation and subsistence by destination country. Trip cost = travellers × (travel + nights × accommodation + days × subsistence), as in the Golden Scenario rules.
- `Travel summary`: SUMIFS over `Trips` per BE/AE block × WP. Items are person-trips; the total is the trip cost. It feeds the Transfer View's C.1 line. A spare block sums only once a code is typed for it. `Travel unit costs`: Tables `TravelBands` and `TravelRates`, copied from the profile data.
- Structural checks: the Trips Table span, columns and calculated formulas; the price formulas in every row; unit costs equal to the profile data; one summary row per block × WP; no travel sheets when switched off. The PivotTable check was already there and now has a test.
- Synthetic Check: the provisional scenario enters 8 trips across every BE/AE (the late AE in a spare block included) and the WPs, over band edges (600/601, 7501, 12000). It then appends trip 21 to `Trips` with inputs only, so its prices come from the calculated columns. A sabotage test drops the WP criterion. `TableRowAddition` now writes only the leading columns it is given.

### Known gaps / follow-ups

- **Land trips (tables 5.2-5.4) are not priced.** There is no Mode column. Every trip uses table 5.1 (air or combined air/rail, 400 km and more). Land trips need a mode and a country-pair lookup. The tables are already in the ticket 02 JSON.
- **A trip under 400 km shows #N/A, and the error carries through to the summary and the Transfer View.** This is on purpose, since such trips are paid at actual cost, but no Input Guard flags it yet (ticket 12).
- A WP a human adds to `WP list` gets no summary rows until a rebuild (the same gap as in tickets 06 and 07).
- The older subsistence table (calls 31.7.2024-12.5.2025) is not selectable. Profile 1.0 uses the current one.

# 12 — Input Guards and the Checks panel

**What to build:** Input Guards across the Planning Workbook, and a Checks panel on the Cover Sheet showing OK / warning / error per guard. The guards are:
- **Data validation** on input cells: lists, number ranges, non-negative values.
- **Completeness flags**: a Beneficiary with no country, a WP with no lead, effort without a rate.
- **Plausibility warnings** (soft): each threshold is a blank, human-filled Profile Constant, and a warning stays silent while its threshold is empty.
- **Profile rule checks**: a hook for the Funding Profile's own rules.

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Data validation applied to Human Input cells; anything openpyxl cannot express faithfully written with lxml
- [x] Completeness flags evaluate by formula
- [x] Plausibility thresholds are empty labelled cells; a guard with no threshold reports OK
- [x] Profile rule checks declared in profile data are rendered as guards (HE may declare none)
- [x] Guards conditionally coloured; Checks panel aggregates every guard
- [x] Structural checks confirm validation is present on Human Input cells
- [x] Synthetic Check includes scenarios that trip a completeness flag and a plausibility warning, and verifies the panel state after recalculation

## Notes (implementation)

- **Data validation** (`sheets/validation.py`): every Human Input except free text (names, acronyms, WP and task titles, item descriptions; marked with `put_input(..., free_text=True)`) has exactly one validation, and every validation now refuses invalid entries (`showErrorMessage`; openpyxl's default only allowed them silently, which the earlier method sheets relied on). New: Rate Table rates and staff effort (decimal >= 0), the spare block code and WP leads (list of `BE list` codes), thresholds (decimal >= 0).
- **Country dropdown via lxml**: the Official Budget Table's `BE list` Country column is an x14 extension validation over a hidden `CountryList` sheet. The build mirrors both: a hidden `CountryList` sheet with the Official's 184 entries verbatim (`profiles/data/he_country_list_obt_v3_6.json`, extracted from v3.6 and tested against it) and an x14 validation written into the saved file with lxml (openpyxl drops x14 on read and cannot write it). A test asks Excel itself to read it back, including on a row added to the `BEList` Table.
- **Input Guards sheet** (after `WP list` / `Task List`): the lead of each WP (input, with a flag) and an effort-without-a-rate grid per BE/AE block x Staff Category. The Official's `WP list` has no lead column and its layout is a contract, so the lead lives here.
- **Plausibility thresholds**: blank labelled inputs under the Profile Constants (they are not in `layout.constants`, which holds valued constants only). Declared in profile data (`input_guards.plausibility`, measures `rate`, `effort_per_block_wp` (one BE/AE's person-months in one WP), `trip_cost`); a measure whose method is switched off is left out.
- **Profile rule checks**: `input_guards.rule_checks` in profile data; HE declares none and the panel says so. One rule kind is implemented as the hook: `max_share_per_wp` (a WP's share of the lump sum or person-months above a Profile Constant), meant for KA220's per-WP limits (ticket 19). An unknown kind is refused at build time.
- **Checks panel** on the Cover: one row per guard (label, status, count, kind, where to look) and an Overall row (worst status); every status and count is a formula, coloured green / amber / red by conditional formatting.
- **Severities**: negative values and completeness flags are errors; plausibility warnings are warnings; a rule check declares its own.
- **Verification**: the structural checks confirm a blocking validation on every non-free-text Human Input (x14 included, read from the XML), the CountryList content, the guard sheet and formula statuses. The Synthetic Check reads the panel back (statuses and counts) and compares it with `reference.expected_guards`; the report lists the panel state. Scenarios cover the all-OK state, completeness flags plus a plausibility warning plus a pasted negative value, warnings alone (amber overall), a sabotaged guard and a declared rule check.

### Decisions / known gaps

- The negative-values guard stands in for "data validation" on the panel: Excel's validation does not check pasted values, and no formula can test a cell against its validation, so only negatives are caught after the fact (not, e.g., a pasted country outside the list).
- A blank workbook shows the completeness guards in red (every BE lacks a country, every WP a lead). That is the "what is still missing" view, by design.
- "Effort without a rate" treats a rate of 0 like a blank one.
- A WP added to `WP list` after the build gets no lead row until a rebuild (same gap as tickets 06-11).
- The reference model reuses the guard list, the numeric input kinds and the rule's WP selection from `sheets/input_guards.py` (as it reuses `check_summaries.PARTS`); a mistake there would sit on both sides of the Synthetic Check.
- The provisional scenario still types `Testland (fake)` as the country: COM bypasses validation, and the country is not used in any HE figure.

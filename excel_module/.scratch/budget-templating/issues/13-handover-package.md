# 13 — Handover Package

**What to build:** Every successful build delivers a Handover Package:
- the blank Planning Workbook
- the Synthetic Check report
- an English fill-in guide per sheet: what to enter, unit, source, and how to transfer the Transfer View into the Submission Budget

The workbook itself:
- carries a colour legend and the fill-in order on the Cover Sheet
- colours inputs light yellow and derived cells white, with guards conditionally coloured
- has document properties cleared of personal metadata, and no synthetic values left in it

Nothing is delivered unless the Synthetic Check passed.

**Blocked by:** 05 — Synthetic Check harness; 12 — Input Guards and the Checks panel

**Status:** done

- [x] Styling applied consistently by cell role; colour legend on the Cover Sheet
- [x] Fill-in order on the Cover Sheet follows formula dependencies
- [x] Per-sheet English fill-in guide generated from the switched-on sheets and profile
- [x] Author, last-modified-by and save-path metadata absent from the delivered file
- [x] Structural checks confirm no synthetic values and no personal metadata in the deliverable
- [x] A failing Synthetic Check produces no Handover Package, only the failure report

## Notes (implementation)

- **Entry point**: `deliver(shape_parameters, directory)` (`budget_engine/handover.py`) builds with `synthetic_check=True` and writes `planning-workbook.xlsx`, `synthetic-check-report.md` and `fill-in-guide.md` into a new or empty directory (a non-empty one is refused, so no file from an earlier package can pass for part of this one). On `SyntheticCheckFailed` the directory gets only the failure report and the exception is re-raised; the build has already deleted the workbook. Any other failure (structural, Excel unavailable) leaves no package.
- **Deliverable untouched**: `build(..., synthetic_check=True)` now hashes the workbook before the check and after it, and re-runs the structural checks; a changed or failing deliverable is deleted (`BuildError`).
- **Fill-in order** (`sheets/fill_in_order.py`): read from the workbook itself. A sheet with Human Inputs depends on another when a formula or data validation reads a Human Input or formula cell there, by cell reference or through one of its Tables (also inside an `INDIRECT` text). Fixed constants do not count, so the duration on `Profile Constants` ties nothing to it. Topological sort, ties broken by workbook order; the optional thresholds go once nothing required is left. HE with every method: BE list, WP list, Task List, Rate Table, Staff effort, Input Guards (its guards read effort and rates), Travel planner, Equipment depreciation, Itemised list, Profile Constants, then the reading steps. The structural check verifies every input sheet is listed and every dependency comes first.
- **Styling by cell role**: structural checks now require light yellow on Human Inputs only (the legend swatch excepted) and the derived (white) fill on every figure the engine reads back. The Transfer View name cell was the one figure without it. The Cover legend has a swatch per role: input, derived, header, and green/amber/red guard statuses.
- **Fill-in guide** (`budget_engine/guide.py`): one section per sheet the workbook has, in workbook order (all Transfer Views share one section, all Check sheets another), each with what to enter, unit and source. Units, Staff Categories, thresholds, itemised cost lines and travel unit-cost sources come from the profile. The transfer steps and the Submission Budget's name are new profile data (`handover` in `he-lump-sum/1.0.json`). A sheet without a section fails the guide.
- **Personal metadata**: the structural check now reads the package itself. Flagged: an identifying core property (creator, lastModifiedBy, title, subject, description, keywords, category), Company/Manager/HyperlinkBase in `app.xml`, `docProps/custom.xml`, an `absPath`, or any drive, UNC or `file:` path in any XML part. The build also clears category, content status, identifier and last-printed.
- **No synthetic values**: on top of "every Human Input is empty", the provisional scenario's free text (fake names, titles, item descriptions, also from the late rows) must not appear in any cell.
- Tests: `tests/test_handover.py` (packaging with a stubbed check, plus one real Excel run; the guide) and new cases in `tests/test_structural_checks.py`. 213 tests pass.

### Decisions / known gaps

- The HE transfer steps describe the Official Budget Table v3.6 as read from its sheets (`BE1` per Beneficiary, an AE column block on its Beneficiary's sheet, totals and E calculated by the Official). Nobody has walked through them in the Official yet. Ticket 14's demo is the place to do that.
- Dependencies are tracked per sheet, not per cell: `Input Guards` comes after the method sheets it checks, though its WP leads depend on nothing but the `BE list`.
- The synthetic-value scan only knows the provisional scenario. When ticket 15 pins the Golden Scenario, `_check_no_synthetic_values` must read that scenario instead.
- The report is the existing `SyntheticCheckReport.to_markdown()`; the guide and report are Markdown, not rendered documents.

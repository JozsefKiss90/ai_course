I read the spec, the glossary and both ADRs. excel_module has no engine code yet, so there's nothing to refactor first. The first ticket is a tracer bullet: one thin path from Shape Parameters to a blank workbook.

Proposed breakdown

Each ticket is tagged [agent] (an agent can do it alone) or [human] (needs you).

Open items from the spec (Further Notes)

1. Confirm Claude Code finds skills stored in excel_module [agent]
   - Blocked by: none
   - Delivers: a yes/no answer for both start locations (repo root and excel_module), and a decision on where the skills live.
2. Get the KA220 application form's WP budget section [human]
   - Blocked by: none
   - Delivers: the exact layout, and whether it splits the budget per partner.
3. Check the 2026 Programme Guide for KA220 per-WP share limits [agent]
   - Blocked by: none
   - Delivers: any limits, written up as candidate rule checks with page references.
4. Re-extract the HE travel and subsistence unit costs from C(2024)5405 [agent]
   - Blocked by: none
   - Delivers: the tables as profile-ready data, with the source recorded.
5. Work out the HE Golden Scenario by hand [human]
   - Blocked by: none
   - Delivers: committed inputs and expected figures covering all four v1 Estimation Methods.
6. Work out the KA220 Golden Scenario by hand [human]
   - Blocked by: 2, 3

Engine and planner

7. Tracer bullet: HE build → blank Planning Workbook plus structural checks
   - Blocked by: none
   - Delivers:
     - The HE profile as data, with a loader.
     - A build entry point that takes Shape Parameters (BEs, WPs, duration) and writes a blank .xlsx with:
       - a Cover Sheet showing provenance
       - BE list and WP list in the Official Budget Table layout
       - Profile Constants
       - a Rate Table
       - staff effort at WP grain
       - a Transfer View per BE with the A.1 and E rows
     - Seam 2 (structural checks) running green.
8. Synthetic Check harness (seam 1)
   - Blocked by: 7
   - Delivers:
     - A disposable copy filled with a provisional scenario, recalculated in Excel via COM.
     - Its Transfer View compared with a staff-effort reference model.
     - A report of which figures differ, where and by how much.
     - The copy deleted afterwards. A failed check stops delivery.
9. First version of the budget-planner skill
   - Blocked by: 1, 8
   - Delivers:
     - A thin SKILL.md with reference files.
     - The Shape Parameters interview: it refuses identifiers and amounts and confirms the parameters back before building.
     - The build flow running end to end, so you can try it in Claude Code.
10. Affiliated Entities and headroom capacity
    - Blocked by: 8
    - Delivers:
      - AE blocks listed under their BE.
      - BE/AE column blocks built up to count + headroom (states the default and accepts an override).
      - Rows that grow through Excel Tables.
      - Structural and synthetic coverage for all of the above.
11. Optional Task List and task-grain effort
    - Blocked by: 8
    - Delivers: generated task codes with blank titles, effort at Task × BE/AE × Staff Category, and the WP fallback when tasks are skipped.
12. Travel planner Estimation Method
    - Blocked by: 4, 8
    - Delivers: trips priced with the unit costs, a formula-based travel summary (no PivotTable), and the method's reference-model function.
13. Equipment depreciation Estimation Method
    - Blocked by: 8
    - Delivers: the eligible share over the project duration, plus its reference-model function.
14. Itemised list Estimation Method
    - Blocked by: 8
    - Delivers: items × cost per item for any cost line, plus its reference-model function.
15. Full HE Transfer View and Check Summaries
    - Blocked by: 8
    - Delivers:
      - All rows A.1–D.5 and E, with number of items and average cost per item per WP.
      - The lump sum breakdown, person-months overview and per-WP summary.
      - % shares per WP and per BE.
16. Input Guards and the Checks panel
    - Blocked by: 8
    - Delivers:
      - Data validation, using lxml where openpyxl can't express it.
      - Completeness flags.
      - Plausibility warnings that stay silent until you fill in a threshold.
      - A rule-check hook for profiles.
      - OK / warning / error per guard on the Cover Sheet.
17. Handover Package
    - Blocked by: 9, 16
    - Delivers:
      - The colour legend and styling.
      - Personal metadata cleared from the file.
      - The fill-in order and an English fill-in guide per sheet.
      - The Synthetic Check report included.
      - Delivery only after a passing check.
18. KA220 profile
    - Blocked by: 2, 3, 15, 16
    - Delivers:
      - Effort in days.
      - Daily rates looked up from the country group, with an override cell.
      - A Transfer View showing the amount per WP.
      - A Lump Sum Tier input with the gap to the bottom-up estimate.
      - Per-WP rule checks.
19. Pin the reference model to the HE Golden Scenario
    - Blocked by: 5, 10–15
    - Delivers: the Synthetic Check runs against your hand-computed figures. The provisional scenario is retired for HE.
20. Pin the reference model to the KA220 Golden Scenario
    - Blocked by: 6, 18
21. Rebuild flow and re-paste guide
    - Blocked by: 10, 11, 17
    - Delivers:
      - A rebuild from new Shape Parameters.
      - A guide mapping old input blocks to new ones.
      - A test that input-block layouts stay stable within a profile version.
      - A rebuild under an older profile version.
22. budget-profile-maintainer skill
    - Blocked by: 19, 20
    - Delivers:
      - A new profile version drafted as data from the source documents.
      - Provenance recorded, with old versions kept unchanged.
      - A human-readable diff against the previous version.
      - A gate on the Golden Scenario check.
      - Expectation changes proposed to you for approval, never applied.

Ticket 8 needs your call. Until your Golden Scenarios land (5, 6), the harness checks against a small provisional scenario. Its expected figures come from the reference model and I'd flag them as not human-owned. They become authoritative only at 19 and 20. The alternative is to block everything after 8 on ticket 5.

Questions

Ticket 8 needs your call. Until your Golden Scenarios land (5, 6), the harness checks against a small provisional scenario. Its expected figures come from the reference model and I'd flag them as not human-owned. They become authoritative only at 19 and 20. The alternative is to block everything after 8 on ticket 5.

Questions

1. Granularity: is this the right size? Possible merges are 13+14 (small methods) and 9+17. Possible splits: 18 into "profile + staff + Transfer View" and "Lump Sum Tier + rule checks".
2. Blocking edges:
   - Should 9 wait for 17, so the first skill already delivers a full Handover Package?
   - Should 18 really wait for 15 and 16?
3. Provisional scenario: do you accept it for 8, or should the frontier stop until you've hand-computed 5?

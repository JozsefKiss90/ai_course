# Spec — Budget templating skills

Status: ready-for-agent

Context: `excel_module/CONTEXT.md` (glossary), `excel_module/docs/adr/0001-agent-never-reads-filled-planning-workbooks.md`, `excel_module/docs/adr/0002-no-macros-tables-spare-capacity-rebuild.md`. Source material: `excel_module/budget_planner_prompt.md` and the reference documents in `excel_module/docs/`.

## Problem Statement

For every Horizon Europe or Erasmus+ proposal I prepare, I need a budget planning spreadsheet sized to that proposal: its number of Beneficiaries, Affiliated Entities, work packages and tasks, and the funding model's cost categories and units. Today I adapt a manual template by hand each time. It is slow and error-prone: formulas break when partners or work packages are added, hard-coded numbers hide in formulas, and the travel summary depends on a PivotTable whose row order nobody can see. Neither the Horizon Europe Official Budget Table nor the KA220 application form shows effort or cost estimation, so I need a separate planning workbook whose outputs I can transfer mechanically into the Submission Budget.

I want an agent to do the building. But unsubmitted proposals and consortium data are confidential. The agent must never ask for, write or read partner names, countries, titles, rates, effort or amounts. Filled workbooks also leak identifiers through comments, document properties, pivot caches and save paths, as we found when sanitising a real workbook in November 2026. So the agent can only ever work with blank workbooks, and the workbook itself has to catch input mistakes, because no agent will ever see it filled in.

## Solution

Two Claude Code skills in `excel_module`:

- **`budget-planner`** builds a blank, project-specific Planning Workbook for one proposal. It asks only for Shape Parameters: the Funding Profile, counts, duration, which Estimation Methods to switch on, and the headroom. It generates the workbook and runs the Synthetic Check on a disposable copy. If the check passes, it delivers the Handover Package. It also rebuilds: for a changed consortium shape it produces a fresh blank workbook plus a re-paste guide. It never opens a filled workbook.
- **`budget-profile-maintainer`** adds or updates a Funding Profile version from its source documents, for example a new Programme Guide or new unit-cost decision. It keeps old versions. A profile version counts as done only when it passes the Synthetic Check against its own Golden Scenario. Changes to the expected figures need my explicit approval.

Every Planning Workbook contains:
- a Cover Sheet with provenance, the Checks panel, the fill-in order and the colour legend
- Reference Lists (`BE list`, `WP list`) laid out exactly like the EC's
- an optional Task List
- a Rate Table
- the switched-on Estimation Method sheets
- a Transfer View per Beneficiary/AE, laid out row for row like the Submission Budget
- Check Summaries mirroring the Submission Budget's summaries, with % shares and the gap to the Lump Sum Tier
- Input Guards

It uses no macros and no PivotTables. It grows through Excel Tables and spare capacity, and anything bigger goes through a rebuild.

## User Stories

### Building a workbook

1. As a proposal budget planner, I want to start a build by naming the Funding Profile, so that the workbook follows the right programme's cost categories, units and Submission Budget layout.
2. As a proposal budget planner, I want the agent to ask me only for Shape Parameters, so that I never have to type confidential data into the conversation.
3. As a proposal budget planner, I want the agent to refuse or ignore any identifier or amount I mention by mistake, so that confidential data never ends up in the workbook or the build record.
4. As a proposal budget planner, I want to give the number of Beneficiaries, so that the workbook has a column/row block for each one (BE1…BEn).
5. As a proposal budget planner, I want to give the number of Affiliated Entities per Beneficiary, so that each AE gets its own block, listed under its Beneficiary.
6. As a proposal budget planner, I want to give the number of work packages, so that every per-WP structure is sized correctly.
7. As a proposal budget planner, I want to optionally give the number of tasks per work package, so that effort can be planned per task when I want that detail.
8. As a proposal budget planner, I want to skip task planning entirely, so that small proposals are planned at work-package level without an empty Task List.
9. As a proposal budget planner, I want to give the project duration in months, so that duration-dependent calculations such as depreciation share and the timeline use the right length.
10. As a proposal budget planner, I want the agent to state the profile's default headroom (HE +3, KA220 +2) and let me override it, so that the workbook has spare capacity for late partners without being oversized.
11. As a proposal budget planner, I want to choose which Estimation Methods to switch on from those the profile allows, so that the workbook contains only the sheets I need.
12. As a proposal budget planner, I want methods the profile marks as mandatory switched on automatically, so that I can't build a workbook that breaks the programme's rules.
13. As a proposal budget planner, I want the agent to confirm all Shape Parameters back to me before building, so that I catch a wrong count before generation.
14. As a proposal budget planner, I want the generated workbook to open in Excel 2021/365 without macro or security prompts, so that I and my colleagues can use it anywhere.

### Workbook contents

15. As a proposal budget planner, I want `BE list` and `WP list` laid out exactly like the Official Budget Table's, so that I can paste the same block into both workbooks.
16. As a proposal budget planner, I want partner and work package names entered only in the Reference Lists, so that every other sheet picks them up by formula and I type each name once.
17. As a proposal budget planner, I want a Task List with task codes per work package and blank title cells, so that I can enter task titles myself.
18. As a proposal budget planner, I want a Rate Table per Beneficiary/AE × Staff Category in the profile's native unit, so that personnel costs use rates I control.
19. As an Erasmus+ planner, I want daily rates derived by formula from each Beneficiary's country group, with a manual override cell, so that I only enter the country unless a partner's rate differs.
20. As a Horizon Europe planner, I want effort entered in person-months, so that it matches the Official Budget Table's unit with no conversion step.
21. As an Erasmus+ planner, I want effort entered in days, so that it matches how KA220 staff costs are reasoned about.
22. As a proposal budget planner, I want Profile Constants (indirect rate, productive hours, days-per-PM factor and similar) shown in labelled, visible cells, so that I can see and audit every convention the formulas use.
23. As a proposal budget planner, I want no formula to contain a hard-coded constant, so that a changed convention is a one-cell edit.
24. As a proposal budget planner, I want a staff effort sheet at Task (or WP) × Beneficiary × Staff Category grain, so that personnel cost builds up from planned effort.
25. As a proposal budget planner, I want a travel planner priced with the Commission's travel and subsistence unit costs, so that trip costs follow the official decision without manual lookups.
26. As a proposal budget planner, I want the travel summary built with formulas instead of a PivotTable, so that it never depends on a hidden row order or a manual refresh.
27. As a proposal budget planner, I want an equipment depreciation sheet, so that only the eligible share of equipment over the project duration is costed.
28. As a proposal budget planner, I want an itemised list sheet (items × cost per item), so that I can enter any other cost line with the same structure.
29. As a proposal budget planner, I want every Estimation Method to output items and total per Beneficiary × WP × cost line, so that the Transfer View works the same no matter which methods are on.
30. As a Horizon Europe planner, I want indirect costs computed by the profile's rule (25% of the eligible base), so that category E is never entered by hand.
31. As a proposal budget planner, I want a Transfer View per Beneficiary/AE laid out row for row like the Submission Budget, so that I can copy it across unchanged.
32. As a Horizon Europe planner, I want the Transfer View to show number of items and average cost per item per WP and cost line, in the Official Budget Table's units, so that the figures go straight into its input cells.
33. As a KA220 planner, I want the Transfer View to show the amount per work package, so that it matches the application form's WP budget section.
34. As a Horizon Europe planner, I want Check Summaries that mirror the Official Budget Table's lump sum breakdown, person-months overview and per-WP summary, so that I can compare totals before and after transfer.
35. As a proposal budget planner, I want the % shares of effort and budget per work package and per Beneficiary, so that I can judge balance at a glance.
36. As a KA220 planner, I want to enter my chosen Lump Sum Tier and see the gap between my bottom-up estimate and the tier, so that I can adjust until it fits.
37. As a proposal budget planner, I want inputs coloured light yellow, derived cells white and guards conditionally coloured, so that I always know where to type.
38. As a proposal budget planner, I want all labels and guidance in English, so that the workbook can be shared with an international consortium.

### Growth and rebuild

39. As a proposal budget planner, I want rows (Beneficiaries, AEs, WPs, tasks, trips, items) to grow through Excel Tables, so that adding a row keeps every formula working.
40. As a proposal budget planner, I want spare column capacity per Beneficiary/AE up to the headroom, so that a late partner can join without a rebuild.
41. As a proposal budget planner, I want to ask for a rebuild with new Shape Parameters, so that a larger reshape gives me a fresh, correct blank workbook.
42. As a proposal budget planner, I want a rebuild to include a re-paste guide mapping old input blocks to new ones, so that I can move my own inputs across without the agent seeing them.
43. As a proposal budget planner, I want input-block layouts to stay stable across rebuilds under the same profile version, so that re-pasting is a block copy, not a cell-by-cell job.
44. As a proposal budget planner, I want to rebuild under the profile version a proposal started with, even after newer versions exist, so that rules don't change mid-proposal.

### Input Guards

45. As a proposal budget planner, I want data validation on input cells (lists, number ranges, non-negative values), so that impossible entries are blocked as I type.
46. As a proposal budget planner, I want completeness flags (a Beneficiary with no country, a WP with no lead, effort without a rate), so that I see what's still missing.
47. As a proposal budget planner, I want soft plausibility warnings with thresholds I fill in myself, so that unusual figures are flagged under my own standards.
48. As a proposal budget planner, I want a guard with no threshold to stay silent, so that I'm not flooded with warnings from defaults I never chose.
49. As a proposal budget planner, I want the Funding Profile's rule checks (for example estimate vs. Lump Sum Tier, per-WP limits where the profile defines them), so that breaches of programme rules are caught before submission.
50. As a proposal budget planner, I want a Checks panel on the Cover Sheet showing OK / warning / error per guard, so that I can judge the workbook's state from one place.

### Handover and provenance

51. As a proposal budget planner, I want the Cover Sheet to record the Funding Profile version, build date and Shape Parameters, so that anyone can tell how the workbook was made.
52. As a proposal budget planner, I want the Cover Sheet to show the fill-in order, so that I fill sheets in the sequence the formulas depend on.
53. As a proposal budget planner, I want an English fill-in guide per sheet (what to enter, unit, source, and how to transfer the Transfer View), so that a colleague can fill the workbook without me.
54. As a proposal budget planner, I want the Synthetic Check report in the Handover Package, so that I have evidence the blank workbook calculates correctly.
55. As a proposal budget planner, I want no workbook delivered unless its Synthetic Check passed, so that I never receive a broken template.
56. As a proposal budget planner, I want the delivered workbook free of personal metadata (author, last-modified-by, save paths) and of any synthetic values, so that it is clean before I add anything.

### Synthetic Check

57. As a proposal budget planner, I want every build verified on a disposable copy filled with obviously fake inputs, so that verification never touches real data and fake data can't be mistaken for real.
58. As a proposal budget planner, I want the copy recalculated in real Excel, so that dynamic arrays, structured references and validation behave as they will for me.
59. As a proposal budget planner, I want expected figures computed independently of the workbook's formulas, by a reference model of the profile and methods, so that the check is not the workbook checking itself.
60. As a proposal budget planner, I want the reference model pinned to hand-computed Golden Scenarios, so that a shared mistake in model and workbook can't pass unnoticed.
61. As a proposal budget planner, I want expected figures changed only with my explicit approval, so that a failing check is never "fixed" by editing the expectations to match the output.
62. As a proposal budget planner, I want structural checks on the blank workbook on every build, so that layout regressions are caught quickly without Excel.
63. As a proposal budget planner, I want a failed check reported as which figures differ, where and by how much, so that the cause can be fixed in the generator.
64. As a proposal budget planner, I want the disposable copy deleted after the check, so that no filled synthetic workbook is left lying around.

### Funding Profile maintenance

65. As a profile maintainer, I want to add a new profile version from updated source documents (a new Programme Guide, unit-cost decision or Official Budget Table release), so that new proposals follow current rules.
66. As a profile maintainer, I want each version to record its source documents and their versions, so that every rule can be traced to its origin.
67. As a profile maintainer, I want old versions kept unchanged, so that existing proposals can still be rebuilt under their original rules.
68. As a profile maintainer, I want a human-readable diff between the new and previous versions, so that I can review exactly what changed before approving.
69. As a profile maintainer, I want a new version accepted only after it passes the Synthetic Check against its Golden Scenario, so that a profile change can't silently break workbooks.
70. As a profile maintainer, I want the maintainer to propose Golden Scenario expectation changes for my approval instead of applying them, so that expectations stay human-owned.
71. As a profile maintainer, I want profiles stored as data, not code, so that a rule change is a data edit that can be reviewed.
72. As a profile maintainer, I want each profile to declare its allowed, default and mandatory Estimation Methods, so that the planner offers the right choices.
73. As a profile maintainer, I want the Horizon Europe travel and subsistence unit costs taken from C(2024)5405 itself, not from the old manual template, so that the tables come from the official source.

## Implementation Decisions

- **Two skills, one shared engine.** `budget-planner` (build, rebuild, Synthetic Check inside the build flow) and `budget-profile-maintainer`. Both live under `excel_module`'s Claude skills directory. Each SKILL.md is thin and points to per-step reference files, such as the Shape Parameters interview, the build steps, the rebuild and re-paste guide, the Synthetic Check, and the Handover Package. The Python engine they share is a modular package with four parts:
  - **profiles**: data plus a loader
  - **methods**: one module per Estimation Method
  - **sheets**: one builder per sheet type
  - **verify**: the reference model, Golden Scenario runner and structural checks
- **Security boundary (ADR-0001).**
  - The planner's interview collects only Shape Parameters.
  - The build input contract accepts only profile id/version, counts, duration, method switches and headroom. It has no field for any identifier or amount.
  - The engine never opens a workbook it didn't just generate. Rebuilds take Shape Parameters, never an existing workbook.
  - Country, rate and name-dependent values are always formulas over human-filled cells.
- **No macros, no PivotTables (ADR-0002).**
  - The output is `.xlsx`.
  - Row growth uses Excel Tables, structured references and dynamic-array formulas, so Excel 2021/365 is required.
  - Per-BE/AE column blocks are built up to count + headroom.
  - Summaries use formulas (for example SUMIFS or dynamic-array aggregation), not PivotTables.
- **Generation stack.** openpyxl generates the workbook, with lxml for anything openpyxl cannot express faithfully (for example data-validation extensions). Excel via COM is used only to recalculate and read back the disposable synthetic copy, never to re-save the deliverable, because COM re-saves drift widths, heights and styles.
- **Funding Profile data model.** Each profile version holds:
  - id and version
  - source-document provenance
  - cost categories and Submission Budget layout (row order of the Transfer View)
  - effort unit (PM for HE, days for KA220)
  - Profile Constants
  - indirect cost rule
  - unit-cost tables (travel/subsistence bands; KA220 country-group daily rates)
  - Staff Categories
  - allowed / default / mandatory Estimation Methods
  - default headroom
  - rule checks (for example the Lump Sum Tier gap, and per-WP limits if the source defines them)
  - Lump Sum Tiers where applicable

  Versions are immutable once accepted.
- **v1 profiles.**
  - **Horizon Europe lump sum**: cost categories A.1–A.4, B, C.1–C.3, D.1–D.5; E = 25% × (A + C); effort in person-months; Official Budget Table v3.6 layout.
  - **Erasmus+ KA220 Cooperation Partnerships**: Lump Sum Tier €120k / €250k / €400k; Submission Budget = amount per WP; bottom-up estimate fitted to the tier; source is the 2026 Programme Guide (already in `excel_module/docs/`).
- **Estimation Method contract.**
  - Inputs: the workbook context (BE/AE blocks, WPs, optional tasks, Profile Constants, Rate Table).
  - Output: number of items and total cost per Beneficiary/AE × WP × cost line, in a fixed shape the Transfer View consumes.
  - The v1 catalogue is staff effort, travel planner, equipment depreciation and itemised list.
  - Each method also supplies its own reference-model function, used by the Synthetic Check.
- **Effort grain.** Task × BE/AE × Staff Category when a Task List is present, otherwise WP × BE/AE × Staff Category. Task titles are blank input cells, and task codes are generated.
- **Reference Lists contract.** `BE list` and `WP list` keep the Official Budget Table's exact cell layout. This contract is tested.
- **Sheet set.**
  - Cover Sheet
  - BE list
  - WP list
  - Task List (optional)
  - Rate Table
  - Profile Constants (or a constants area on an existing sheet)
  - one sheet per switched-on method
  - Transfer View per BE/AE
  - Check Summaries
- **Input Guards.**
  - Data validation.
  - Completeness flags.
  - Plausibility warnings: thresholds are blank human-filled Profile Constants, and a guard stays silent while its threshold is empty.
  - Profile rule checks.
  - All guards feed the Cover Sheet's Checks panel (OK / warning / error).
- **Styling.** Inputs light yellow, derived cells white, guards conditionally coloured. English only. Document properties are cleared of personal metadata.
- **Build flow.**
  1. Interview.
  2. Confirm Shape Parameters.
  3. Generate the blank workbook.
  4. Run the structural checks.
  5. Make a disposable copy and fill it with the Golden Scenario (scaled to the Shape Parameters where needed).
  6. Recalculate it in Excel and compare against the reference model.
  7. Delete the copy.
  8. Write the Synthetic Check report.
  9. Assemble the Handover Package.

  Any failure stops delivery.
- **Rebuild flow.** The same as build, plus a re-paste guide derived from comparing the old and new Shape Parameters. Input-block layouts are a contract within a profile version.
- **Profile maintainer flow.**
  1. Read the source documents.
  2. Draft the new version as data.
  3. Present a diff against the previous version.
  4. Run the Synthetic Check against the version's Golden Scenario.
  5. Propose any expectation changes for human approval.
  6. Accept the version only on approval and a passing check.

## Testing Decisions

- **Good tests test external behaviour.** Every test goes through the build entry point (profile version + Shape Parameters → blank workbook) and observes only the workbook and Excel's recalculated results. No test calls a sheet builder or method module directly.
- **Seam 1, main: build + Synthetic Check.**
  - The build entry point produces a blank workbook.
  - A disposable copy is filled with the profile's Golden Scenario, recalculated in real Excel via COM, and its Transfer View and Check Summaries are compared with the reference model.
  - This covers every Estimation Method, sheet builder and profile version.
  - The profile maintainer has no separate seam: a profile version is tested by running this seam against its Golden Scenario.
- **Seam 2, companion: structural checks on the blank workbook, without Excel.** These are fast enough to run on every build and across many Shape Parameter combinations. They check:
  - the Reference Lists match the Official Budget Table's layout exactly
  - every count, including headroom, produced the right blocks
  - every Human Input cell is empty
  - Profile Constants sit in labelled cells, and no formula contains a bare numeric literal (beyond trivial ones such as 0 and 1)
  - there is no VBA, no PivotTables, and no personal metadata
  - the Cover Sheet records the profile version and Shape Parameters
- **Golden Scenarios are human-owned.** One per profile, worked out by hand once and committed. The reference model must reproduce them exactly. Expected figures change only with explicit human approval. An agent must never edit expectations to make a failing check pass.
- **What is tested.** The engine through its build entry point, the reference model against the Golden Scenarios, and both v1 profiles.
- **Prior art.** The November 2026 sanitisation of the manual template had three scripts: a synthetic end-to-end test on a disposable copy, a read-only Excel check, and a structural comparison against the source. Their lessons carry over:
  - Excel re-saves drift formatting, so verify on copies and never re-save the deliverable.
  - PivotTable row order was a hidden dependency.
  - That run's expectations were edited to match the observed outputs, which made its pass meaningless. This is why expectations are hand-computed and human-approved here.

## Out of Scope

- Reading, editing or validating any filled-in Planning Workbook, including small post-handover structural fixes (ADR-0001).
- Writing figures into the Official Budget Table or the KA220 application form. Transfer is always done by a human.
- VBA, macros and PivotTables (ADR-0002).
- Excel versions before 2021, Excel Online-specific behaviour, and LibreOffice.
- Estimation Methods beyond the v1 four: event planner and topic-specific D-lines (D.2–D.5) are v2.
- Funding Profiles other than Horizon Europe lump sum and Erasmus+ KA220 (for example HE actual-cost grants, other Erasmus+ actions).
- Languages other than English.
- Migrating or reusing the existing manual template. It is reference material only.

## Further Notes

- **Open items to ticket separately:**
  - Obtain a KA220 blank-draft application form (PDF or screenshots) to confirm the exact layout of the WP budget section and whether it has a per-partner split.
  - Confirm from the 2026 Programme Guide any per-WP share limits for KA220, such as a project-management share cap.
  - Hand-compute the Golden Scenarios, one per profile (`ready-for-human`).
  - Re-extract the travel and subsistence unit-cost tables from C(2024)5405.
  - Verify that Claude Code discovers skills placed under `excel_module`'s own skills directory when started from the repo root as well as from `excel_module`.
- **Reference documents** in `excel_module/docs/`:
  - the Official Budget Table v3.6 (`.xlsm`)
  - the HE Annotated Grant Agreement (AGA) and the lump sum Model Grant Agreement
  - the lump sum funding handbook
  - the 2026 Erasmus+ Programme Guide
  - the manual blank budget template
- The budget-templating glossary is the vocabulary for all tickets. Terms to use: Planning Workbook, Submission Budget, Shape Parameters, Human Inputs, Transfer View, and so on. Terms to avoid: "template", "budget table", "sensitive data".

# 07 — Optional Task List and task-grain effort

**What to build:** Builds optionally accept the number of tasks per work package.
- **With tasks:** the workbook gets a Task List with generated task codes per WP and blank task-title input cells. Staff effort is planned at Task × BE/AE × Staff Category grain and rolls up per WP.
- **Without tasks:** no Task List is generated, and effort stays at WP grain.

**Blocked by:** 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Shape Parameters contract accepts optional tasks per WP
- [ ] Task codes generated per WP; titles are empty Human Input cells
- [ ] Task List grows through an Excel Table
- [ ] With tasks: effort sheet at task grain, rolling up correctly to WP in the Transfer View
- [ ] Without tasks: no Task List sheet, effort at WP grain
- [ ] Structural checks cover both variants
- [ ] Synthetic Check covers both variants, with reference model updated

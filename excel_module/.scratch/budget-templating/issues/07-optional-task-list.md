# 07 — Optional Task List and task-grain effort

**What to build:** Builds optionally accept the number of tasks per work package.
- **With tasks:** the workbook gets a Task List with generated task codes per WP and blank task-title input cells. Staff effort is planned at Task × BE/AE × Staff Category grain and rolls up per WP.
- **Without tasks:** no Task List is generated, and effort stays at WP grain.

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Shape Parameters contract accepts optional tasks per WP
- [x] Task codes generated per WP; titles are empty Human Input cells
- [x] Task List grows through an Excel Table
- [x] With tasks: effort sheet at task grain, rolling up correctly to WP in the Transfer View
- [x] Without tasks: no Task List sheet, effort at WP grain
- [x] Structural checks cover both variants
- [x] Synthetic Check covers both variants, with reference model updated

## Notes (implementation)

- Contract: `tasks` is optional, a list with one whole number >= 1 per work package (e.g. `[2, 1, 3]`). Without it, `ShapeParameters.tasks` is `None` and there is no Task List. The Cover records "Tasks per work package" (or "none (effort per work package)").
- Task codes are `T<wp>.<n>` (T1.1, T1.2, T2.1, ...). `ShapeParameters.effort_units` lists `(WP, unit)` per effort row: each task under its WP, or each WP as its own unit when there are no tasks.
- `Task List` sits after `WP list`, with an Excel Table `TaskList` (Task nr | WP | Task title). Codes and WPs are derived cells, titles are Human Inputs (`("task_title", code)`). It also appears in the Cover's fill-in order.
- Staff effort input keys are now `("effort", unit, slot, category)`, where unit is a task code or a WP code. With tasks the sheet gains a `Task` column after `WP`. Each task row adds a Contribution to its WP, so the Transfer View sums the task rows per WP line and stays at WP grain.
- Structural checks: with tasks, the Task List entries, the `TaskList` Table span and its columns, and one effort row per task × BE/AE block, labelled (WP, task, BE/AE nr). Without tasks, a `Task List` sheet is reported as unexpected.
- Synthetic Check: the provisional scenario fills task titles and cycles effort per unit. Without tasks it gives the same values as before. Both variants are tested, plus a sabotage test where the roll-up drops a task.
- Known gap (same as for WPs in ticket 06): a task row a human adds to `TaskList` breaks no formula, but it gets no staff effort rows until a rebuild.

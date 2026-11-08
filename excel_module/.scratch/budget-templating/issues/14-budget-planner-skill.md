# 14 — budget-planner skill

**What to build:** The `budget-planner` Claude Code skill. It runs the full build flow end to end: interview, confirm Shape Parameters, generate, structural checks, Synthetic Check, Handover Package. The SKILL.md is thin and points to per-step reference files (Shape Parameters interview, build steps, Synthetic Check, Handover Package).

The interview asks only for Shape Parameters: Funding Profile, counts, duration, Estimation Methods and headroom. It:
- states the profile's default headroom and accepts an override
- switches mandatory methods on automatically
- refuses or ignores any identifier or amount the user mentions
- confirms all Shape Parameters before building

**Blocked by:** 01 — Skill discovery; 13 — Handover Package

**Status:** ready-for-agent

- [ ] Skill placed where ticket 01 decided and discovered from the decided start locations
- [ ] Interview offers only the methods the chosen profile allows, with defaults pre-selected and mandatory ones locked on
- [ ] An identifier or amount offered by the user is not recorded in the workbook, build record or files; the skill says why
- [ ] Shape Parameters read back for confirmation before generation
- [ ] Any failed step stops delivery and reports the failure
- [ ] Walk-through demo: an HE build from the skill yields a Handover Package

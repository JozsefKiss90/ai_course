# 17 — budget-profile-maintainer skill

**What to build:** The `budget-profile-maintainer` Claude Code skill. It works from updated source documents: a new Programme Guide, unit-cost decision or Official Budget Table release. It:
1. drafts a new Funding Profile version as data, recording the source documents and their versions
2. keeps old versions unchanged
3. presents a human-readable diff against the previous version
4. runs the Synthetic Check against the version's Golden Scenario
5. proposes any expectation changes for human approval instead of applying them
6. accepts the version only on approval and a passing check

**Blocked by:** 15 — Pin HE Golden Scenario

**Status:** ready-for-agent

- [ ] Thin SKILL.md with reference files for each maintainer step
- [ ] New version written alongside old ones; accepted versions are immutable (enforced by a check)
- [ ] Every new version records its source documents and versions
- [ ] Human-readable diff covers constants, unit-cost tables, layout, methods, rule checks and tiers
- [ ] Golden Scenario expectation changes are presented as a proposal; the skill never writes them without explicit approval
- [ ] Demo: a small HE profile change (e.g. one unit-cost value) goes through draft → diff → Synthetic Check → approval

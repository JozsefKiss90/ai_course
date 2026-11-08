# 17 — budget-profile-maintainer skill

**What to build:** The `budget-profile-maintainer` Claude Code skill. It works from updated source documents: a new Programme Guide, unit-cost decision or Official Budget Table release. It:
1. drafts a new Funding Profile version as data, recording the source documents and their versions
2. keeps old versions unchanged
3. presents a human-readable diff against the previous version
4. runs the Synthetic Check against the version's Golden Scenario
5. proposes any expectation changes for human approval instead of applying them
6. accepts the version only on approval and a passing check

**Blocked by:** 15 — Pin HE Golden Scenario

**Status:** done

- [x] Thin SKILL.md with reference files for each maintainer step
- [x] New version written alongside old ones; accepted versions are immutable (enforced by a check)
- [x] Every new version records its source documents and versions
- [x] Human-readable diff covers constants, unit-cost tables, layout, methods, rule checks and tiers
- [x] Golden Scenario expectation changes are presented as a proposal; the skill never writes them without explicit approval
- [x] Demo: a small HE profile change (e.g. one unit-cost value) goes through draft → diff → Synthetic Check → approval

## Notes (implementation)

- **Skill:** `.claude/skills/budget-profile-maintainer/`. A thin `SKILL.md` with six steps and one reference file per step: `source-documents.md`, `drafting.md`, `diff.md`, `expectations.md` and `check-and-accept.md`. The engine side is `budget_engine/maintain.py`, driven through the CLI's `profile-*` commands: `draft`, `diff`, `propose`, `approve`, `check` and `accept`.
- **Immutability:** `profiles/data/accepted.json` lists each accepted version with SHA-256 digests (line endings normalised) of three things: the version file, every data file it reads, and the Golden Scenario transcription it was accepted against. `immutability_problems()` runs in `test_accepted_profile_versions_are_unchanged` and before every acceptance. A changed unit-cost amount therefore goes into a new data file. `he-lump-sum` 1.0 is registered as accepted (2026-11-08).
- **Accepted versions only, for the planner:** `profiles` lists accepted versions only, and `confirm`, `deliver` and `rebuild` refuse a draft (exit 2). `build()` still takes drafts, because the maintainer's check builds them.
- **Source documents:** acceptance requires every `provenance` entry to have a `version`. Any data file the version reads that no accepted version reads must also be listed there.
- **Diff:** sections for source documents, Profile Constants, unit-cost tables (resolved from their data files, row by row), layout, Estimation Methods, rule checks, Lump Sum Tiers, and "Other" for anything else.
- **Expectations (ADR-0003):** `profile-propose` reads the previous Golden Scenario under the new version and recomputes every expected-figure section with the reference model. It writes nothing. `profile-approve` needs the proposal id the human saw, refuses if the figures have changed since, and never overwrites. It writes the transcription and a short worksheet that records the approver and the changed figures. The order is propose and approve, then check, because the check needs the approved Golden Scenario. Recomputing 1.0 under itself reproduces all 139 signed-off figures, with no changes.
- **Demo** (real Excel, `test_profile_maintainer.py`, in a sandbox copy of the data): version 1.1 changes the travel unit cost for 601–1600 km from €365 to €370, in a new data file. The diff shows that one row. The proposal lists 22 changed figures, all from trip 1 (2 travellers, so +€10 on C.1). On approval, accept runs the Synthetic Check: PASS, 1618 figures compared, 237 pinned. A second demo carries 1.0's figures forward unchanged instead, and the check fails, as it should.
- **Known limit:** the maintainer recomputes only the expected-figure sections the HE Golden Scenario uses. A KA220 Golden Scenario with other sections stops the proposal until `_recompute` learns them.

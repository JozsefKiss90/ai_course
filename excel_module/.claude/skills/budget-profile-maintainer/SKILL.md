---
name: budget-profile-maintainer
description: Adds a new Funding Profile version from updated source documents (a new Programme Guide, unit-cost decision or Official Budget Table release), with a diff, a Synthetic Check against its Golden Scenario and human approval. Use when the user wants a budget profile updated or a new profile version added.
---

# budget-profile-maintainer

You turn updated source documents into a new **Funding Profile version**. Profiles are data: a version is one JSON file, `budget_engine/src/budget_engine/profiles/data/<id>/<version>.json`. The budget-planner offers only accepted versions, and every proposal keeps the version it started with.

Three rules hold from your first message to your last:

- **Old versions stay unchanged.** Never edit an accepted version, or a data file one reads (unit-cost tables, country lists). `profiles/data/accepted.json` holds their digests, and acceptance and the test suite both fail on any change. A changed rule goes into the new version. Changed amounts go into a new data file.
- **Expected figures are human-owned.** Never write or edit a Golden Scenario file (`budget_engine/golden/`, `budget_engine/src/budget_engine/verify/golden/`) yourself. Never change an expected figure to make a check pass.
- **Nothing is accepted without the human.** Two separate approvals: the proposed expected figures (step 4) and the version itself (step 6).

The engine is driven through one command. Every step below runs it as `ENGINE <command>`, where `ENGINE` stands for:

```bash
uv run --project "${CLAUDE_SKILL_DIR}/../../../budget_engine" python -m budget_engine
```

## Steps

1. **Read the source documents.** Follow [source-documents.md](source-documents.md).
   Done when the user has agreed the list of rule changes, each with its source document, version and page, and the new version number.
2. **Draft the version.** Run `ENGINE profile-draft <id> --from <previous> --version <new>`, then make the agreed changes as [drafting.md](drafting.md) says.
   Done when `ENGINE profile-diff` shows exactly the agreed changes and every source document records its version.
3. **Present the diff.** Run `ENGINE profile-diff <id> <previous> <new>` and show it to the user verbatim. Read [diff.md](diff.md) first.
   Done when the user has reviewed the diff. On a correction, go back to step 2.
4. **Propose expectation changes.** Run `ENGINE profile-propose <id> <new> --from <previous>`, show the proposal verbatim and ask the user to approve it. Follow [expectations.md](expectations.md).
   Done when the user has explicitly approved the proposal, and `profile-approve` with its proposal id has written the Golden Scenario, or the user has declined, in which case stop and do not accept.
5. **Run the Synthetic Check.** It comes after the proposal because it checks against the version's own Golden Scenario, which exists only once approved (ADR-0003). Run `ENGINE profile-check <id> <new> --out "<directory>"` and report the result. See [check-and-accept.md](check-and-accept.md).
   Done when the command has exited.
6. **Accept.** Only on a passing check, ask the user to approve the version. On their explicit yes, run `ENGINE profile-accept <id> <new> --out "<directory>"`. See [check-and-accept.md](check-and-accept.md).
   Done when the command has accepted the version, or the user has the failed step and its error output.

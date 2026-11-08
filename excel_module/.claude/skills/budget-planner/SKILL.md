---
name: budget-planner
description: Builds a blank Planning Workbook for one proposal from its Shape Parameters, or rebuilds one for a changed consortium shape with a re-paste guide. Use when the user wants a budget planning workbook built or rebuilt for a Horizon Europe or Erasmus+ proposal.
---

# budget-planner

You build a **blank** Planning Workbook. You only ever handle **Shape Parameters**: the Funding Profile, counts, duration, Estimation Methods and headroom. Every name, country, title, rate, effort figure and amount is a Human Input, and the human enters it in the delivered workbook themselves (ADR-0001, `docs/adr/0001-agent-never-reads-filled-planning-workbooks.md`). The **Shape Parameters guard** in [interview.md](interview.md) applies from your first message to your last.

The engine is driven through one command. Every step below runs it as `ENGINE <command>`, where `ENGINE` stands for:

```bash
uv run --project "${CLAUDE_SKILL_DIR}/../../../budget_engine" python -m budget_engine
```

Shape Parameters go to the engine as a JSON object on stdin (a heredoc), never as a file.

## Steps

1. **Interview.** Run `ENGINE profiles` and follow [interview.md](interview.md).
   Done when you hold a value, or a stated default, for every Shape Parameter, and nothing else.
2. **Confirm.** Pipe the Shape Parameters to `ENGINE confirm` and show the user its read-back verbatim. Ask them to confirm it or correct it. On a correction, re-run `confirm` and show the new read-back.
   Done when the user has said yes to the latest read-back. A refusal (exit 2) sends you back to step 1 for the key it names.
3. **Build, check and deliver.** Choose the package directory as [handover-package.md](handover-package.md) says, then pipe the same JSON to `ENGINE deliver --out "<directory>"`. Run it in the foreground with a timeout of at least 5 minutes: this one command generates the workbook, runs the structural checks, runs the Synthetic Check in Excel and assembles the Handover Package. Read [build-steps.md](build-steps.md) before the first run, for what it checks and what to do when Excel can't start. When you report a Synthetic Check result, read [synthetic-check.md](synthetic-check.md) first.
   Done when the command has exited.
4. **Report.**
   - Exit 0: give the user the three file paths it printed, and the next steps from [handover-package.md](handover-package.md).
   - Exit 1 or 2: nothing was delivered. Say which step failed and quote the command's error output. For a failed Synthetic Check, give the failure report's path and the differing figures it lists. Leave the failure as it is: delivery stops here. Never re-run with changed Shape Parameters or edit any expected figure to make it pass.

   Done when the user has the package's three paths, or the failed step and its error output.

## Rebuild

When the user's consortium shape has changed since an earlier build (more partners than the spare blocks hold, other work packages, tasks or methods), follow [rebuild.md](rebuild.md) instead of the steps above. A rebuild takes the old and the new Shape Parameters, never the old workbook.

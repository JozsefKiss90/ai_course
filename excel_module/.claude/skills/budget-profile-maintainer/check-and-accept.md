# Synthetic Check and acceptance

## Check

`ENGINE profile-check <id> <new> --out "<directory>"` builds a workbook under the new version at its Golden Scenario's own Shape Parameters. It runs the structural checks and the Synthetic Check in real Excel, and compares every Transfer View and Check Summary figure with the reference model and with the approved figures. It writes `synthetic-check-report.md` into the directory and keeps no workbook. Use a new directory under the scratchpad, never the repo. Run it in the foreground with a timeout of at least 5 minutes. Excel must be installed. If it cannot be started, the command exits 1 with `could not start Excel via COM`.

- Exit 0: `Synthetic Check: PASS`. Give the user the report path, the number of figures compared and the number pinned to the Golden Scenario.
- Exit 1: give the user the error output, or for a failed check the report path and the differing figures it lists. A missing Golden Scenario also exits 1: go back to step 4. A failure is a defect in the draft or the engine. Never edit expected figures, or change the draft just to pass, without going back through steps 2–4 with the user.
- Exit 2: the command was refused (an unknown profile or version). Quote the message.

## Accept

Ask the user to approve the version, with the diff and the passing check in front of them. On their explicit yes, run:

```bash
ENGINE profile-accept <id> <new> --out "<directory>"
```

Before it runs the check again, it refuses (exit 1, listing every reason) when:

- the version is already accepted
- any accepted version, a data file one reads, or the Golden Scenario it was accepted against has changed
- a source document lacks its version, or a new data file is not among the source documents
- the version has no Golden Scenario

It then runs the same Synthetic Check, and accepts only if it passes against the approved figures. Acceptance adds the version, with the digests of its files and of its Golden Scenario transcription, to `profiles/data/accepted.json`. From then on the version is immutable and `ENGINE profiles` offers it to the budget-planner.

Report the outcome. Then tell the user which files to review and commit: the new version, any new data file, the Golden Scenario files and `accepted.json`.

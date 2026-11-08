# Expectation changes

Every version is pinned to its own Golden Scenario. A new version carries the previous version's Golden Scenario forward: the same Shape Parameters and the same fake Human Inputs. Its expected figures may change, for example when a unit cost changes a trip total and everything built on it.

## Propose

`ENGINE profile-propose <id> <new> --from <previous>` reads the previous Golden Scenario under the new version and recomputes every expected figure with the reference model. It writes nothing. It prints:

- the proposal id, which names exactly these figures
- the number of figures compared
- each figure that changes: its path, the signed-off value and the proposed value
- or "No expected figure changes" when the new version keeps them all

Show the proposal verbatim. Then explain each change in one line, tracing it to a row of the diff. For example: "Trip 1 is 2 travellers at 1100 km: 2 × (370 − 365) = +10 on C.1, so +2.50 on E and +12.50 on F." Ask the user to approve the figures. Make the approval its own question, separate from anything else.

A proposed figure the user disputes, or a change you cannot trace to the diff, is a defect in the draft or the engine. Stop and raise it. Never "fix" the figures.

## Approve

Only after the user explicitly approves in this conversation, run:

```bash
ENGINE profile-approve <id> <new> --from <previous> --proposal <proposal id> --approved-by "<who, as the user gives it>"
```

`--proposal` is the id the approved proposal showed. If the draft or a data file changed since, the figures differ and the command refuses (exit 2): show the new proposal and ask again.

It writes the new version's Golden Scenario, both the transcription and a worksheet that records the approver, the date and the changed figures. It never overwrites an existing Golden Scenario. Approval is needed even when no figure changes: the new version still needs its own Golden Scenario.

If the user declines, nothing is written and the version cannot be accepted. Stop there.

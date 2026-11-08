# The Synthetic Check

Every workbook is verified before handover. `deliver` runs the check itself; you never run it separately or open any workbook.

- The engine copies the blank workbook to a disposable copy outside the package directory. It fills the copy with the profile's Golden Scenario: a small, obviously fake proposal whose expected figures the human signed off. The Golden Scenario is scaled to the build's Shape Parameters where they differ.
- Excel recalculates the copy. The Transfer Views and Check Summaries are read back and compared with figures from an independent reference model of the Funding Profile and Estimation Methods. The reference model reproduces the Golden Scenario's signed-off figures exactly. A build with the Golden Scenario's own Shape Parameters is also compared with those figures directly.
- The copy is deleted. The report records that it was.

## Reading the report

`synthetic-check-report.md` gives the result (PASS or FAIL), the scenario used, the number of figures compared, the Checks panel statuses and, on a failure, each differing figure: what it is, the cell, the expected and actual values and the difference.

The scenario line says which of three scenarios ran. Pass it on to the user as written.

- **human-owned Golden Scenario**: the build has the Golden Scenario's own Shape Parameters. The report also counts the figures pinned to the signed-off ones.
- **scaled from the human-owned Golden Scenario**: the usual case. Expected figures come from the reference model, which the signed-off figures pin.
- **PROVISIONAL, not human-owned**: the profile version has no Golden Scenario yet, so the expected figures are not pinned to signed-off ones.

## On a failure

A failure is a defect in the engine or the profile, not in the user's Shape Parameters. Tell the user so when you report it.

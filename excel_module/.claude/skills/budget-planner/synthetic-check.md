# The Synthetic Check

Every workbook is verified before handover. `deliver` runs the check itself; you never run it separately or open any workbook.

- The engine copies the blank workbook to a disposable copy outside the package directory and fills it with obviously fake inputs (BE1…BEn, round-number rates and effort), including rows added to its Tables after the build.
- Excel recalculates the copy. The Transfer Views and Check Summaries are read back and compared with figures from an independent reference model of the Funding Profile and Estimation Methods.
- The copy is deleted. The report records that it was.

## Reading the report

`synthetic-check-report.md` gives the result (PASS or FAIL), the scenario used, the number of figures compared, the Checks panel statuses and, on a failure, each differing figure: what it is, the cell, the expected and actual values and the difference.

The scenario line says whether the scenario is a **human-owned Golden Scenario** or **PROVISIONAL, not human-owned**. Pass this on to the user as written. A provisional scenario means the expected figures have not yet been pinned to hand-computed ones.

## On a failure

A failure is a defect in the engine or the profile, not in the user's Shape Parameters. Tell the user so when you report it.

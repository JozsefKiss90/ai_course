# 05 — Synthetic Check harness (seam 1)

**What to build:** The main verification seam. After a build, the engine:
1. makes a disposable copy of the blank Planning Workbook
2. fills its Human Input cells with an obviously fake scenario
3. recalculates the copy in real Excel via COM and reads back the Transfer View
4. compares the result with figures the reference model computes independently for the profile and the staff effort Estimation Method

On a mismatch it reports which figures differ, where and by how much. The copy is always deleted afterwards. A failed check stops delivery.

Until ticket 15 pins the HE Golden Scenario (ticket 03), the harness uses a **provisional scenario**. Its expected figures come from the reference model and are explicitly flagged as not human-owned.

**Blocked by:** 04 — Tracer bullet

**Status:** done

- [x] Disposable copy created outside the deliverable location; the deliverable itself is never opened by Excel or re-saved
- [x] Copy filled with the provisional scenario, scaled to the build's Shape Parameters
- [x] Recalculation and read-back through Excel COM; workbook closed without saving the deliverable
- [x] Reference model computes expected figures without reading any workbook formula
- [x] Each Estimation Method supplies its own reference-model function (staff effort first)
- [x] Synthetic Check report lists pass/fail and, on failure, every differing figure with location, expected, actual and difference
- [x] Copy deleted after the check, including on failure; deletion verified
- [x] Provisional scenario clearly marked as provisional and not human-owned
- [x] A deliberately broken formula in the generator makes the check fail with a useful report

## Notes (implementation)

- Entry points: `run_synthetic_check(build_result)` returns a `SyntheticCheckReport`; `build(..., synthetic_check=True)` runs it and, on failure, deletes the workbook and raises `SyntheticCheckFailed` (the report rides on the exception).
- The check is opt-in on `build()` so the fast structural tests can build many shapes without Excel. Delivery paths (tickets 13 and 14) must build with `synthetic_check=True`.
- The report exists in memory (`SyntheticCheckReport.to_markdown()`). Writing it to disk belongs to the Handover Package (ticket 13).
- Code: `budget_engine/verify/` — `scenario.py` (provisional scenario), `reference.py` (reference model), `excel.py` (COM: the copy is opened read-only, filled in memory, recalculated and closed without saving, so Excel calculates exactly the bytes the build wrote), `synthetic.py` (the harness and report).
- Figures match within 0.005 (half a cent) to absorb floating-point noise. This is not a rounding rule.
- The comparison covers the Transfer View only. Check Summaries arrive with ticket 11 and must be added to the comparison then.
- Tests: `budget_engine/tests/test_synthetic_check.py` (marked `excel`). The broken-generator test sabotages the Transfer View sum formula and asserts the reported location, expected, actual and difference.

# 05 — Synthetic Check harness (seam 1)

**What to build:** The main verification seam. After a build, the engine:
1. makes a disposable copy of the blank Planning Workbook
2. fills its Human Input cells with an obviously fake scenario
3. recalculates the copy in real Excel via COM and reads back the Transfer View
4. compares the result with figures the reference model computes independently for the profile and the staff effort Estimation Method

On a mismatch it reports which figures differ, where and by how much. The copy is always deleted afterwards. A failed check stops delivery.

Until ticket 15 pins the HE Golden Scenario (ticket 03), the harness uses a **provisional scenario**. Its expected figures come from the reference model and are explicitly flagged as not human-owned.

**Blocked by:** 04 — Tracer bullet

**Status:** ready-for-agent

- [ ] Disposable copy created outside the deliverable location; the deliverable itself is never opened by Excel or re-saved
- [ ] Copy filled with the provisional scenario, scaled to the build's Shape Parameters
- [ ] Recalculation and read-back through Excel COM; workbook closed without saving the deliverable
- [ ] Reference model computes expected figures without reading any workbook formula
- [ ] Each Estimation Method supplies its own reference-model function (staff effort first)
- [ ] Synthetic Check report lists pass/fail and, on failure, every differing figure with location, expected, actual and difference
- [ ] Copy deleted after the check, including on failure; deletion verified
- [ ] Provisional scenario clearly marked as provisional and not human-owned
- [ ] A deliberately broken formula in the generator makes the check fail with a useful report

# 13 — Handover Package

**What to build:** Every successful build delivers a Handover Package:
- the blank Planning Workbook
- the Synthetic Check report
- an English fill-in guide per sheet: what to enter, unit, source, and how to transfer the Transfer View into the Submission Budget

The workbook itself:
- carries a colour legend and the fill-in order on the Cover Sheet
- colours inputs light yellow and derived cells white, with guards conditionally coloured
- has document properties cleared of personal metadata, and no synthetic values left in it

Nothing is delivered unless the Synthetic Check passed.

**Blocked by:** 05 — Synthetic Check harness; 12 — Input Guards and the Checks panel

**Status:** ready-for-agent

- [ ] Styling applied consistently by cell role; colour legend on the Cover Sheet
- [ ] Fill-in order on the Cover Sheet follows formula dependencies
- [ ] Per-sheet English fill-in guide generated from the switched-on sheets and profile
- [ ] Author, last-modified-by and save-path metadata absent from the delivered file
- [ ] Structural checks confirm no synthetic values and no personal metadata in the deliverable
- [ ] A failing Synthetic Check produces no Handover Package, only the failure report

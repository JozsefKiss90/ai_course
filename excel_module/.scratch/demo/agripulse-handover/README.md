# AGRI-PULSE demo package

A live demonstration of the budget engine on a fictional six-beneficiary Horizon Europe lump sum project. AGRI-PULSE develops and validates a crop water-stress monitoring and irrigation decision-support system.

**Open this workbook for the live demo:** `agripulse-six-partner-budget.xlsx` in this folder.

## Package index

| File | What it is |
|---|---|
| `agripulse-six-partner-budget.xlsx` | The populated, recalculated demo workbook, and the starting point for the demo. It is a byte-for-byte copy of `..\agripulse-six-partner-budget.xlsx`, which stays as the original. |
| `presenter-guide.md` | The five-minute walkthrough, with sheet names, cell addresses and expected figures, plus the worksheet inventory. |
| `demo-verification.md` | Verification of the populated workbook: totals, person-months, hand checks, guard status and known limitations. |
| `template-handover/planning-workbook.xlsx` | The blank template with the same shape, from the standard handover (`budget_engine.handover.deliver()`). |
| `template-handover/fill-in-guide.md` | The generated sheet-by-sheet fill-in guide for the blank template. |
| `template-handover/synthetic-check-report.md` | Synthetic Check evidence for the blank template (PASS, 4,310 figures, 0 differences). |

The two halves are kept apart on purpose:

- **Demo workbook (populated):** checked by recalculating it in desktop Excel and comparing it with the reference model. See `demo-verification.md`.
- **Template (blank):** checked by the engine's Synthetic Check on a disposable filled copy. See `template-handover/synthetic-check-report.md`.

## Purpose

The populated workbook shows the engine end to end, with no typing during the demo:

- the consortium and its task structure;
- the four estimation methods (staff effort, travel, equipment depreciation and itemised costs);
- how each method feeds the per-beneficiary Transfer Views;
- the project-level check sheets and the guard panel.

All names and amounts are fictional. The 100% funding rate for every beneficiary is a demonstration assumption.

## Profile and shape

| Parameter | Value |
|---|---|
| Funding Profile | `he-lump-sum` version `1.0` (Official Budget Table v3.6, indirect costs at 25% of A+C) |
| Duration | 36 months |
| Beneficiaries | 6 (BE1–BE6), no affiliated entities, `headroom=0` (no spare blocks) |
| Work packages | 6 |
| Tasks per WP | `[2, 3, 3, 2, 2, 2]` (14 tasks) |
| Estimation Methods | `staff_effort`, `travel_planner`, `equipment_depreciation`, `itemised_list` |

| Code | Beneficiary | Acronym | Country | Leads |
|---|---|---|---|---|
| BE1 | Northbridge Institute of Technology | NIT | Netherlands | WP1 Project coordination and data governance |
| BE2 | Valewood Applied Research Centre | VARC | Finland | WP2 Field data and Earth observation |
| BE3 | Meridian Agricultural Systems Lab | MASL | Spain | WP3 Crop water-stress modelling |
| BE4 | Danube Digital Engineering Institute | DDEI | Hungary | WP4 Decision-support prototype |
| BE5 | Adriatic Field Innovation Centre | AFIC | Croatia | WP5 Field pilots and validation |
| BE6 | Alpine Knowledge Exchange Foundation | AKEF | Austria | WP6 Training, dissemination, and uptake |

## Build command

Run from `C:\elte_ai_course\excel_module\budget_engine` with `uv run python`.

The demo workbook was built blank with this command, then filled and saved in desktop Excel:

```python
from budget_engine.build import build
SHAPE = {"profile": {"id": "he-lump-sum", "version": "1.0"}, "duration_months": 36,
         "beneficiaries": 6, "work_packages": 6, "tasks": [2, 3, 3, 2, 2, 2],
         "methods": ["staff_effort", "travel_planner", "equipment_depreciation", "itemised_list"],
         "headroom": 0}
build(SHAPE, r"C:\elte_ai_course\excel_module\.scratch\demo\agripulse-six-partner-budget.xlsx")
```

The template handover was generated with the same shape:

```python
from budget_engine.handover import deliver
deliver(SHAPE, r"C:\elte_ai_course\excel_module\.scratch\demo\agripulse-handover\template-handover")
```

## Quick start for the presenter

1. Open `agripulse-six-partner-budget.xlsx` from this folder in desktop Excel (2021 or Microsoft 365). It opens on **Cover**, and the Checks panel (A17:B25) shows OK on every row.
2. Nothing needs typing or refreshing: every figure is already calculated. A full recalculation (Ctrl+Alt+F9) changes no cell.
3. Follow `presenter-guide.md`. The route goes from consortium and tasks, through the four methods, into Transfer Views BE4 and BE3, and ends at the project totals (EUR 1,605,016.25; 257 person-months).
4. To show a live change, edit a yellow input (for example `Rate Table` C8) and undo it afterwards. Don't save, so the demo file stays in its verified state. The original in `..\` can always restore it.
5. To show a fresh project starting from scratch, open `template-handover/planning-workbook.xlsx` next to `template-handover/fill-in-guide.md`.

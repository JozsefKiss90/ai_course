# Snapshot Template (demo only — not a gem task)

Save as `ops/snapshots/S<milestone>[.n] - <title>.md`. Attach `graph-S<…>.png` (Obsidian graph view, filter `path:wiki/aga`, colour groups by `node_type`) and `dashboard-S<…>.png`.

```markdown
# S4.2 — Leaf cluster: Art 6.2.A.1 daily rate

date: YYYY-MM-DD
milestone: M4
ticket(s): T-L3-6.2.A.1-01

## What was added
| Node | Type | Anchor(s) |
|---|---|---|
| RULE - Daily Rate Uses Last Closed Financial Year | rule | [[Daily Rate]] |
| … | | |

## Why it was needed
One paragraph: the gap this closes (e.g. "Anchors existed but no calculable rule; budget layer needs the formula and ceiling").

## How it was produced
NotebookLM queries Q1–Q5 → G6 → Smart Connections check (1 merge) → Copilot link check (0 broken) → G7 log/index.

## Dashboard metrics
| Metric | Before | After |
|---|---|---|
| total nodes | | |
| layer-3 nodes | | |
| orphans | | |
| unanchored leaves | | |
| unsourced factual | | |
| needs_review | | |

## Graph view
![[graph-S4.2.png]]

## Notes for the audience
One or two bullets: what to look at in the graph (new cluster attaching to hub X), what the gem got wrong and how lint caught it.
```

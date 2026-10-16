# AGA Wiki — Operations Manual

Human-operator runbook for building an Obsidian knowledge graph of the **AGA — Annotated Grant Agreement (V2.0, 01.04.2025)** with NotebookLM + Gemini gems, Copilot for Obsidian (where justified), Dataview and Smart Connections. Blueprint lineage: `llm_wiki.md` → Kierkegaard vault → `dev_graph/CLAUDE.md`.

Package contents: this manual · `gems/` (10 gem system instructions, G0–G9) · `templates/` (schema skeleton, dashboard, ticket, snapshot).

---

## 1. Architecture

| Layer | Location | Owner | Mutable by |
|---|---|---|---|
| Raw source | `raw/aga_en.pdf` — one file, never split | Human | Nobody |
| Grounding | NotebookLM notebook **"AGA v2.0"** (single source = the whole AGA; scope enforced by query, not by file) | Human | NotebookLM only |
| Wiki | `wiki/aga/**` markdown | Gems (via tickets) | Populator gems, Copilot (lint only) |
| Schema | `wiki/aga/WIKI_SCHEMA.md` | Schema Architect gem → human ratifies | Schema Architect only |
| Observability | `wiki/observability/Graph Health Dashboard.md` | Wiki Maintainer gem | Maintainer only |

Vault tree (type-to-directory binding, same rule as dev_graph):

```
wiki/aga/
  WIKI_SCHEMA.md  index.md  log.md
  sources/ structure/ actors/ concepts/ definitions/ rules/ procedures/
  cases/ examples/ best_practices/ references/ syntheses/ budget/ dashboards/ governance/
wiki/observability/Graph Health Dashboard.md
raw/aga_en.pdf
ops/passes/       (one note per extraction pass: lens × locator → saved NotebookLM Notes)
ops/tickets/     ops/snapshots/
```

## 2. Tool routing (who does what)

| Need | Tool | Why |
|---|---|---|
| Grounded extraction with citations | **NotebookLM** | Only tool that sees the full source; every answer cites page/passage. Output = saved Notes, one per pass. |
| Structured generation (schema, nodes, tickets) | **Gemini gem** (one per role, knowledge files = schema + index + anchors; NotebookLM notebook connected) | Role isolation + fixed knowledge = stable output shape. |
| In-vault operations (link repair, frontmatter migration, duplicate check against existing pages) | **Copilot for Obsidian** (Vault QA / agent mode) | Needs *vault state*, not source text. Not used for authoring. |
| Semantic near-duplicate detection, `related_nodes` suggestions | **Smart Connections** | Run on every new cluster before commit. |
| Lint, dashboards, budget tables | **Dataview** | Frontmatter is the contract; Dataview enforces it. |

Rule: **gems never see the whole AGA.** A gem sees only: `WIKI_SCHEMA.md` + `index.md` (titles) + the ticket + the ticket's canonical anchor nodes + the NotebookLM Notes for the ticket's pass (lens × locator).

## 3. Context-engineering strategy (the anchoring contract)

1. **Schema first, then anchors, then leaves.** Nothing is written until `WIKI_SCHEMA.md` is ratified; no leaf until its canonical anchor exists.
2. **One ticket = one extraction pass = one lens × one locator.** The document is parsed many times, never split. Lens = *what* to extract (structure, definitions, rules, cases/examples, cross-references, budget parameters); locator = *where* (an article, a sub-section, or — for cross-cutting lenses — the whole AGA). Scope ≤ 15 new nodes, explicit allowed `node_type` list, explicit anchor list. Every query names the locator and demands page cites; a cite outside the locator's page range (from the article map) is rejected. Order passes by value, not by page order. Anything outside scope → "Out-of-scope findings" section of the ticket result, never a node.
3. **Every factual node carries `source_refs`** (`Art. X | p. N | "≤30-word verbatim quote"`). No quote → `certainty: low` + `status: needs_review`. Syntheses are the only nodes allowed without quotes (`canonical_owner: agent`).
4. **Canonical nodes are read-only for leaf tickets.** A leaf ticket that needs a canonical change files a *Canonical Change Request* in the ticket result; the Maintainer applies it in a separate ticket.
5. **Gem knowledge refresh at every milestone.** After each milestone, re-upload `WIKI_SCHEMA.md` + `index.md` + anchor list to every gem. Stale knowledge = drift.
6. **Programme scoping.** AGA covers all programmes. Every node has `programme_scope` (`all` / `HE` / list). Budget layer filters `HE`.
7. **Output = files, not prose.** Gems emit one fenced block per file with the path in the fence info string; the operator (or Copilot) drops them in verbatim.

### Extraction lenses (the passes)

| Lens | Locator granularity | Feeds layer | Typical query shape |
|---|---|---|---|
| P1 Structure | whole AGA (TOC) | 1 | "List every heading under Article X with its page." |
| P2 Definitions & actors | Art 2 + whole AGA | 2 | "Where is <term> defined? Quote MGA text + page; list every article that uses it." |
| P3 Rules & ceilings | one (sub-)article | 3 | "Within 6.2.A.1 only: every condition, ceiling, formula, deadline — verbatim, page." |
| P4 Cases / examples / best practice | one (sub-)article | 3 | "Within 6.2.A.1 only: each Specific case, Example, Best practice, warning block by title, verbatim figures, page." |
| P5 Cross-references | whole AGA, filtered by anchor | 3/4 | "Every place the AGA refers to <anchor> outside its home article — locator + page." |
| P6 Budget parameters | whole AGA, HE filter | 4 | "Every numeric ceiling, rate, or percentage applicable to Horizon Europe — value, locator, page." |
| P7 Negative | one article | QA | "What does Article X explicitly NOT cover; where does it point instead?" |

Same document, seven lenses, any order. Re-run a lens on a locator whenever lint shows a gap (§14 of the dashboard).

## 4. Agents (Gemini gems)

| # | Gem | Layer | Input | Output |
|---|---|---|---|---|
| G0 | **Orchestrator / Ticket Generator** | all | article map, milestone | numbered tickets (`templates/Ticket Template.md`) |
| G1 | **Source Discovery** | 0 | AGA TOC (pasted), NotebookLM | article map (locator → page range), pass plan (lenses), query sets, source note (`SRC -`) |
| G2 | **Topic Analysis** | 1–2 | NotebookLM Notes for a chapter | topic clusters, candidate canonical list, priority |
| G3 | **Schema Architect** | 0 | blueprint files, G2 output | `WIKI_SCHEMA.md` (types, domains, naming, relations, lint) |
| G4 | **Frontmatter Specifier** | 0 | `WIKI_SCHEMA.md` draft | YAML contract + per-type extensions + Dataview compatibility check |
| G5 | **Node Author** | 1–2 | ticket + Notes + schema | meta & canonical nodes |
| G6 | **Graph Populator** | 3 | ticket + Notes + anchors | leaf cluster (≤15 nodes), link proposals, CCRs |
| G7 | **Wiki Maintainer** | all | dashboard output, lint queries | fixes, `log.md` entries, `index.md` updates, schema-evolution proposals |
| G8 | **Budget Assistant** | 4 | budget nodes + HE-scoped rules | `budget/` model nodes, cost-check answers (filed back as nodes) |
| G9 | **Meta-Prompter** | all | a gem file + failure sample, or a ticket scope | gem instruction patches, NotebookLM query sets, Copilot prompts, ticket execution headers |

Delegation: G0 generates tickets; G9 generates/repairs prompts. Neither touches wiki content. Use G9 whenever a gem's output fails lint twice for the same reason.

Gem setup (once per gem): paste `gems/G*.md` as the instruction; upload knowledge files listed at the top of that file; connect NotebookLM "AGA v2.0" where the file says so.

## 5. Workflow (phases = milestones)

Each phase ends with a **snapshot** (`templates/Snapshot Template.md`) — you take it, it is not a gem task.

### M0 — Bootstrap (½ day)
1. Create vault tree (§1). Install Dataview, Smart Connections, Copilot. Add `raw/aga_en.pdf`.
2. NotebookLM: notebook "AGA v2.0", upload `aga_en.pdf` as the single source. Verify a scoped citation query (e.g. "Within Article 6.2.A.1 only: the daily-rate formula, verbatim, with page") returns page-level cites inside pp. 62–75.
3. Paste the AGA table of contents (pp. 3–9) into `ops/article_map_raw.md` — this is the only "parsing" needed; G1 turns it into the locator → page-range map.
4. Copy `templates/*` into place. `Graph Health Dashboard.md` must render (empty tables are fine).
- Exit: dashboard renders; NotebookLM cites pages. Snapshot S0.

### M1 — Wiki Maintenance Schema (½ day)
1. G1: article map (locator → pages) + pass plan (lenses) + `SRC - AGA V2.0.md` + one query set per lens.
2. G2 on Intro + Art 1–6 Notes: topic clusters + candidate canonical list (~40).
3. G3: draft `WIKI_SCHEMA.md` from `templates/WIKI_SCHEMA (skeleton).md` + G2 output.
4. G4: finalize YAML contract; run Dataview compatibility check (every dashboard query must resolve).
5. **Human ratifies** schema → `ontology_version: "1.0"`. Upload to all gems.
- Exit: schema ratified, `log.md` entry `schema | v1.0`. Snapshot S1.

### M2 — Meta nodes / spine (1 day)
Ticket type L1. G5 creates: `SRC -`, `WORK - AGA`, `structure/` nodes for Intro, 6 chapters, 44 articles, Annex 5 sections (≈60 nodes, seed content: scope sentence, page range, MGA-vs-annotation note, child links). `index.md` sections created. `dashboards/` stubs.
- Exit: every article has a structure node; dashboard "Structure coverage" = 100 %. Snapshot S2.

### M3 — Canonical anchors (1–2 days)
Ticket type L2, one per topic cluster from G2. G5 writes canonical nodes (`status: canonical`, `canonical_owner: source`, ≥3 `source_refs`, Relations, Query Hooks). Typical anchors: Grant Agreement · Granting Authority · Coordinator · Beneficiary · Affiliated Entity · Associated Partner · Subcontractor · Action / DoA (Annex 1) · Estimated Budget (Annex 2) · Maximum Grant Amount · Funding Rate · Forms of Funding (actual / unit / flat-rate / lump-sum) · Eligible Cost (general conditions) · Cost Category A–F (one each) · Daily Rate · Day-equivalent · Indirect Costs · Pre-financing · Interim & Final Payment · Reporting Period · Financial Statement · CFS · Amendment · Audit · Rejection / Reduction / Suspension / Termination · Force Majeure.
Smart Connections dup-check before each commit.
- Exit: all anchors `canonical`, 0 orphans among anchors. Snapshot S3.

### M4 — Leaf clusters, iterative (main phase; ~2 tickets/day)
Ticket type L3. Order of clusters (value-first):
1. Art 6.1 general eligibility → 2. 6.2.A.1 personnel (daily rate, ceilings, specific cases) → 3. 6.2.A.2–A.6 → 4. 6.2.B subcontracting → 5. 6.2.C purchases → 6. 6.2.D–E → 7. 6.3–6.4 → 8. Art 5 grant/forms of funding → 9. Art 20–22 records, reporting, payments → 10. Art 7–10 participants → 11. Art 11–19 obligations → 12. Art 23–26 → 13. Art 27–35 → 14. Art 36–44 → 15. Annex 5.
Each cluster = P3 ticket then P4 ticket on the same locator; P5 (cross-references) runs per anchor across the whole AGA once its home cluster exists — this is what breaks the linear order. Per ticket loop (§6). After every 3 tickets: G7 lint pass.
- Exit per cluster: ≤15 nodes, every node linked to ≥1 anchor, 0 broken links, dashboard clean. Snapshot per cluster (S4.n) — the demo's core sequence.

### M5 — Budget layer (1 day)
G8 creates `budget/` nodes: `BUD - Cost Model HE` (categories × form of funding × ceilings), `BUD - Personnel Cost Calculator` (daily-rate procedure + worked example, mirrors Art 6.2.A.1), `BUD - Eligibility Checklist`, `dashboards/budget-planning.md` (Dataview over `budget_relevance`, `cost_category`, `programme_scope`). Budget answers are **filed back** as `BUD -` or `SYN -` nodes.
- Exit: budget dashboard lists every rule with `budget_relevance: high`. Snapshot S5.

### M6 — Syntheses & query filing (½ day)
G5 writes `SYN -` nodes for cross-article threads (e.g. "Cost lifecycle: eligibility → declaration → payment → audit → rejection"; "Amendment vs. flexibility"). Each SYN links ≥4 anchors.
- Exit: ≥5 SYN nodes. Snapshot S6.

### M7 — Full lint & close (½ day)
G7 full lint (all checks), dashboard review, `index.md` final, `log.md` summary, schema-evolution proposals parked.
- Exit: Graph Health Dashboard: 0 missing frontmatter, 0 invalid enums, 0 orphans, 0 broken links. Snapshot S7.

## 6. Per-ticket loop (L3 leaf cluster)

1. **G0** issues ticket `T-L3-<article>-<nn>` (scope, allowed types, anchors, max nodes, query set).
2. **NotebookLM**: run the ticket's query set (each query begins with the locator: "Within Article X only…"). Check every cite's page is inside the locator's range; re-ask with a tighter locator if not. Save answers as Notes titled `T-…/Q1…Qn`.
3. **G6** ← ticket + Notes + anchor nodes → fenced files + link proposals + CCRs + out-of-scope findings.
4. Operator drops files into vault (or Copilot agent mode writes them from the paste).
5. **Smart Connections** on each new file: flag ≥0.85 similarity with existing pages → merge or add to "Known Distinct Pairs" on the dashboard.
6. **Copilot** (Vault QA): "list broken wikilinks and missing inbound links for files created today" → apply fixes.
7. **G7** ← dashboard output → `log.md` entry `## [DATE] ingest | T-…`, `index.md` update, anchors' `child_nodes` updated (CCR-applied).
8. Snapshot (demo only).

Stop conditions (escalate to human): a node needs >1 anchor change · quote cannot be located inside the locator's page range · gem proposes a new enum value · cluster exceeds 15 nodes.

## 7. Governance rules carried over (non-negotiable)

- Canonical ownership: one concept, one node; link, never duplicate.
- Closed enums; append-only; every schema change is logged before applied (`schema |` entry).
- Flat YAML; no freeform keys.
- Structural files (`WIKI_SCHEMA.md`, `index.md`, `log.md`) have no frontmatter.
- Never delete: deprecate (`status: deprecated`, successor linked).
- Certainty lifecycle: `low → medium` (one quote), `medium → high` (two independent refs or MGA text + annotation); contradiction → `low` + logged.
- Batch limit 15 nodes; Dataview queries scoped `FROM "wiki/aga"`.

## 8. Log line formats

```
## [YYYY-MM-DD] schema    | v1.0 ratified
## [YYYY-MM-DD] ingest    | T-L2-anchors-03 — Cost categories A–F (6 nodes)
## [YYYY-MM-DD] lint      | pass 4 — 2 orphans fixed, 1 CCR applied
## [YYYY-MM-DD] query     | filed SYN - Cost Lifecycle
## [YYYY-MM-DD] snapshot  | S4.2
```

## 9. Milestone checklist (demo)

| Snapshot | Shows | Dashboard metric |
|---|---|---|
| S0 | empty vault, dashboard renders, NotebookLM cites | nodes = 0 |
| S1 | ratified schema, gems loaded | — |
| S2 | spine in graph view (articles as chain) | structure coverage 100 % |
| S3 | anchors as hubs | orphans = 0, canonical ≈ 40 |
| S4.n | one cluster per snapshot attaching to hubs | nodes +≤15, broken links 0 |
| S5 | budget dashboard | budget_relevance high listed |
| S6 | SYN nodes bridging clusters | SYN ≥ 5 |
| S7 | all lint green | all zero |

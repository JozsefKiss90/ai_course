# AGA Wiki — Wiki Maintenance Schema

ontology_version: "0.1-draft"   ← G3/G4 finalize; human ratifies → "1.0"

This file governs every gem session that writes to `wiki/aga/**`. Analogue of `wiki/CLAUDE.md` / `dev_graph/CLAUDE.md`. Read first, always. No frontmatter (structural file).

---

## 1. Vault structure (type → directory binding)

| Directory | node_type | Prefix |
|---|---|---|
| sources/ | source | `SRC -` |
| structure/ | work, chapter, article, section, annex | none (title = AGA heading, e.g. `Art 6.2.A.1 - Employees`) |
| actors/ | actor | none |
| concepts/ | concept | none |
| definitions/ | definition | `DEF -` |
| rules/ | rule | `RULE -` |
| procedures/ | procedure | `PROC -` |
| cases/ | specific_case | `CASE -` |
| examples/ | example | `EX -` |
| best_practices/ | best_practice | `BP -` |
| references/ | reference | `REF -` (Financial Regulation, other guides) |
| syntheses/ | synthesis | `SYN -` |
| budget/ | budget_model | `BUD -` |
| dashboards/ | dashboard | lowercase-kebab |
| governance/ | governance | none |
| ../observability/ | dashboard | `Graph Health Dashboard` |

## 2. Layers

| Layer | Content | Created by | Ticket type |
|---|---|---|---|
| 0 | this schema, dashboard, templates | G3/G4/human | — |
| 1 | meta nodes: source, work, chapters, articles, sections, annexes | G5 | L1 |
| 2 | canonical anchors (concepts, actors, key definitions) | G5 | L2 |
| 3 | leaf clusters: rules, cases, examples, best practices, procedures | G6 | L3 |
| 4 | syntheses, budget models | G5 / G8 | L4 |
| 5 | maintenance (lint, index, log) | G7 | L5 |

## 3. Frontmatter contract (universal — G4 finalizes)

```yaml
---
id: <kebab-slug>                # immutable
title: "<Title>"
aliases: []
node_type: <enum §4>
domain: <enum §5>
layer: 0|1|2|3|4
article: "6.2.A.1"              # AGA locator; "" for syntheses/dashboards
page_start: 62
page_end: 75
programme_scope: [all]          # all | HE | list of programme codes as printed in AGA
cost_category: ""               # A1|A2|A3|A4|A5|A6|B|C1|C2|C3|D|E|F or ""
budget_relevance: none          # none | low | high
status: seed                    # seed | draft | reviewed | canonical | needs_review | deprecated
certainty: medium               # low | medium | high
canonical_owner: source         # source | agent
source_refs: []                 # flat strings: 'Art 6.2.A.1 | p. 63 | "verbatim ≤30 words"'
parent_nodes: []                # [[wikilinks]]
child_nodes: []
related_nodes: []
anchors: []                     # canonical nodes this leaf hangs on (L3 only; ≥1)
tags: []
ticket_id: "T-L3-6.2.A.1-01"
created_by: G6
created: YYYY-MM-DD
updated: YYYY-MM-DD
ontology_version: "1.0"
---
```

Rules: flat YAML only · closed enums · no keys beyond this file · `id` and `created` never change · `updated` only on substantive edits.

## 4. node_type enum (closed, append-only)
`source, work, chapter, article, section, annex, actor, concept, definition, rule, procedure, specific_case, example, best_practice, warning, reference, synthesis, budget_model, dashboard, governance`

## 5. domain enum (closed, append-only)
`general, action_and_duration, grant_and_funding, eligibility_general, personnel_costs, subcontracting, purchases, other_cost_categories, indirect_costs, participants, implementation_obligations, ethics_data_security, ipr_dissemination, records_reporting, payments_recoveries, audits_certificates, non_compliance, final_provisions, annex5, budget_planning, query_dashboard, governance`

## 6. Node body template

```markdown
# {Title}

{One-sentence definition/claim, sourced.}

## MGA text
> {verbatim MGA clause if the node is a rule/definition; else omit}

## Annotation
{What the AGA annotation adds: conditions, ceilings, calculation, who it applies to.}

## Specific cases / Examples   (link to CASE - / EX - nodes; do not inline them)

## Budget implication          (only if budget_relevance != none)

## Relations
- governed_by: [[Art …]]
- anchored_to: [[<canonical>]]
- refines / exception_of / calculated_by / documented_by / audited_under / consequence: [[…]]

## Query Hooks
- {3–6 natural-language questions this node answers}
```

Relation predicates (closed): `governed_by, anchored_to, refines, exception_of, calculated_by, documented_by, reported_under, paid_under, audited_under, consequence, applies_to, defined_by, illustrated_by, see_also`.

## 7. Naming
Title Case; AGA locator in structure titles; leaf titles state the claim, not the topic (`RULE - Daily Rate Uses Last Closed Financial Year`, not `RULE - Daily rate`).

## 8. Canonical ownership
One concept, one node. Search `index.md` + Smart Connections before creating. Leaf tickets never edit canonical nodes → file a Canonical Change Request (CCR).

## 9. Lint checks (Dataview; see Graph Health Dashboard)
1 missing frontmatter · 2 invalid enum · 3 orphans (0 inlinks) · 4 leaf without `anchors` · 5 factual node with empty `source_refs` · 6 broken wikilinks (Copilot) · 7 `status: canonical` with `certainty != high` · 8 stale (>60 d, non-canonical) · 9 duplicate `id` · 10 programme_scope empty · 11 budget_relevance high without `cost_category`.

## 10. Certainty lifecycle
low → medium: one located quote · medium → high: MGA text + annotation, or two independent refs · any → low: contradiction (log it).

## 11. Automation boundaries
≤15 new nodes per ticket · gems never edit `index.md`/`log.md`/schema directly — they emit proposed lines, G7/human applies · canonical nodes edited only via CCR ticket · enum extension only via `schema |` log entry + this file updated first.

## 12. Schema evolution
Append-only enums · additive fields · governance-first (this file changes before any node) · migration runbook: update schema → ADR-style note in `governance/` → migrate → lint → bump `ontology_version` → log.

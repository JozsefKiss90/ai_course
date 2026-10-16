# Ticket Template

Issued by G0. One ticket = one lens × one locator. Saved to `ops/tickets/<ticket_id>.md`. The ticket text is pasted verbatim into the executing gem together with the NotebookLM Notes it names.

```markdown
# T-L<layer>-<article>-<nn>

ticket_id: T-L3-6.2.A.1-01
layer: 3
executing_gem: G6
milestone: M4
status: open | in_progress | done | blocked

## Scope
- AGA locator: Art 6.2.A.1 — Employees (or equivalent) — pp. 62–75
- Lens: P3 Rules & ceilings
- Valid cite range: pp. 62–75 (reject cites outside; re-query with tighter locator)
- Topic: daily-rate calculation and ceilings
- Explicitly OUT of scope: parental leave specific case (→ T-L3-6.2.A.1-02), project-based remuneration (→ -03)

## Anchors (read-only; link to these)
- [[Personnel Costs (Category A)]]
- [[Daily Rate]]
- [[Day-equivalent]]

## Allowed node types / max
- rule ≤ 6, procedure ≤ 2, specific_case ≤ 3, example ≤ 3, warning ≤ 1 — total ≤ 15

## NotebookLM query set (single source; every query starts with the locator; save each answer as Note "T-L3-6.2.A.1-01/Qn")
Q1 Within Article 6.2.A.1 only: what is the formula for the daily rate and which reference period must be used? Quote the MGA text and page.
Q2 Within Article 6.2.A.1 only: what is the horizontal ceiling on declared day-equivalents? Quote page.
Q3 Within Article 6.2.A.1 only: list every condition under which personnel costs of employees are ineligible. Quote pages.
Q4 Within Article 6.2.A.1 only: what examples does the AGA give for the daily-rate calculation? Reproduce figures verbatim with page.
Q5 Within Article 6.2.A.1 only: which best practices or warnings appear in this section? Quote page.

## Required output
1. Fenced files, one per node, path in fence info (e.g. ```md wiki/aga/rules/RULE - Daily Rate Uses Last Closed Financial Year.md)
2. Link proposals: lines to append to anchors' `child_nodes` (as CCR, not applied)
3. Proposed `index.md` lines and one `log.md` line
4. Out-of-scope findings (bullet list, no nodes)
5. Unresolved: quotes not found → node marked `certainty: low`, `status: needs_review`

## Exit criteria
- every node: ≥1 source_ref with page + quote, ≥1 anchor, valid enums, body template complete
- Smart Connections: no ≥0.85 match with existing page (else merged)
- 0 broken wikilinks after Copilot check
```

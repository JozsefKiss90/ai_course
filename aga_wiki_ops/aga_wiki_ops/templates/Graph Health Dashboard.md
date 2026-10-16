---
id: graph-health-dashboard
title: "Graph Health Dashboard"
aliases: []
node_type: dashboard
domain: query_dashboard
layer: 0
article: ""
page_start: 0
page_end: 0
programme_scope: [all]
cost_category: ""
budget_relevance: none
status: canonical
certainty: high
canonical_owner: agent
source_refs: []
parent_nodes: []
child_nodes: []
related_nodes: []
anchors: []
tags: [observability]
ticket_id: "T-L0-bootstrap-01"
created_by: human
created: 2026-09-25
updated: 2026-09-25
ontology_version: "1.0"
---

# Graph Health Dashboard

Observability for `wiki/aga`. Read at every lint pass and every snapshot. All queries scoped `FROM "wiki/aga"`, `WHERE node_type != null` (excludes structural files).

## 1. Node inventory
```dataview
TABLE node_type, layer, status, certainty, updated
FROM "wiki/aga"
WHERE node_type != null
SORT updated DESC
```

## 2. Missing frontmatter
```dataview
LIST
FROM "wiki/aga"
WHERE node_type = null
AND file.name != "index" AND file.name != "log" AND file.name != "WIKI_SCHEMA"
```

## 3. Type distribution
```dataview
TABLE length(rows) AS Count
FROM "wiki/aga"
WHERE node_type != null
GROUP BY node_type
SORT length(rows) DESC
```

## 4. Layer distribution (population progress)
```dataview
TABLE length(rows) AS Count
FROM "wiki/aga"
WHERE layer != null
GROUP BY layer
SORT layer ASC
```

## 5. Status distribution
```dataview
TABLE length(rows) AS Count
FROM "wiki/aga"
WHERE status != null
GROUP BY status
```

## 6. Certainty distribution
```dataview
TABLE length(rows) AS Count
FROM "wiki/aga"
WHERE certainty != null
GROUP BY certainty
```

## 7. Orphans (0 inbound links)
```dataview
TABLE node_type, layer
FROM "wiki/aga"
WHERE node_type != null AND length(file.inlinks) = 0
AND node_type != "dashboard"
SORT node_type ASC
```

## 8. Leaves without anchors (layer 3 must have ≥1)
```dataview
TABLE node_type, article
FROM "wiki/aga"
WHERE layer = 3 AND (anchors = null OR length(anchors) = 0)
```

## 9. Factual nodes without source_refs
```dataview
TABLE node_type, article, status
FROM "wiki/aga"
WHERE node_type != null AND canonical_owner = "source"
AND (source_refs = null OR length(source_refs) = 0)
```

## 10. Canonical with certainty != high
```dataview
TABLE certainty, article
FROM "wiki/aga"
WHERE status = "canonical" AND certainty != "high"
```

## 11. Needs review / low certainty
```dataview
TABLE node_type, certainty, ticket_id
FROM "wiki/aga"
WHERE status = "needs_review" OR certainty = "low"
SORT ticket_id ASC
```

## 12. Stale (>60 days, non-canonical)
```dataview
TABLE updated, status
FROM "wiki/aga"
WHERE node_type != null AND updated != null
AND date(updated) < date(today) - dur(60 days)
AND status != "canonical" AND status != "deprecated"
SORT updated ASC
```

## 13. Structure coverage (articles present)
```dataview
TABLE article, page_start, page_end
FROM "wiki/aga/structure"
WHERE node_type = "article"
SORT page_start ASC
```

## 14. Coverage by article (leaf count per article)
```dataview
TABLE length(rows) AS Leaves
FROM "wiki/aga"
WHERE layer = 3
GROUP BY article
SORT article ASC
```

## 15. Programme scope missing
```dataview
LIST
FROM "wiki/aga"
WHERE node_type != null AND (programme_scope = null OR length(programme_scope) = 0)
```

## 16. Budget: high relevance without cost_category
```dataview
TABLE article, node_type
FROM "wiki/aga"
WHERE budget_relevance = "high" AND (cost_category = null OR cost_category = "")
```

## 17. Budget rule inventory (HE)
```dataview
TABLE cost_category, article, certainty
FROM "wiki/aga"
WHERE budget_relevance = "high" AND (contains(programme_scope, "all") OR contains(programme_scope, "HE"))
SORT cost_category ASC, article ASC
```

## 18. Tickets ingested
```dataview
TABLE length(rows) AS Nodes, min(rows.created) AS Date
FROM "wiki/aga"
WHERE ticket_id != null
GROUP BY ticket_id
SORT ticket_id ASC
```

## 19. Deprecated nodes
```dataview
TABLE node_type, updated
FROM "wiki/aga"
WHERE status = "deprecated"
```

## 20. Syntheses and their anchor count
```dataview
TABLE length(related_nodes) AS Anchors, certainty
FROM "wiki/aga/syntheses"
WHERE node_type = "synthesis"
```

---

## Known Distinct Pairs
Pages flagged by Smart Connections as near-duplicates but confirmed distinct.
<!-- - [[Page A]] / [[Page B]] — reason -->

## Snapshot metrics (copy into each snapshot)
| Metric | Query |
|---|---|
| total nodes | §1 count |
| by layer | §4 |
| orphans | §7 |
| unanchored leaves | §8 |
| unsourced factual | §9 |
| needs_review | §11 |

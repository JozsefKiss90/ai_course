# The diff

`ENGINE profile-diff <id> <previous> <new>` prints a Markdown diff with one section per part of a profile, always in this order:

- **Source documents**: the `provenance` entries, named by document
- **Profile Constants**
- **Unit-cost tables**: read from the data files each version names, row by row (rows named by country or distance band), plus each table's title, source, annex and pages
- **Layout**: name, effort and rate units, cost categories, Staff Categories, the indirect cost rule, Reference Lists, Transfer View rows, Check Summaries and the handover text
- **Estimation Methods**: allowed, default and mandatory methods, method settings and default headroom
- **Rule checks**: the Input Guards, plausibility thresholds included
- **Lump Sum Tiers**
- **Other**: anything no section above covers

A section without changes says "No change." Each change is a row: the path of the value, its value in the previous version, and its value in the new one. "—" means the value does not exist in that version.

Show the diff to the user verbatim. Then point out anything that is not on the agreed list of changes, and any change with a wider effect, such as a layout change, which makes a rebuild's re-paste guide reach only within one version.

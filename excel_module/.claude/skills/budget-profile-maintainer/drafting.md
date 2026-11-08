# Drafting the version

`ENGINE profile-draft <id> --from <previous> --version <new>` copies the previous version to `profiles/data/<id>/<new>.json` with its `version` set. It refuses to overwrite an existing version. Edit only that new file, and any new data file you create for it.

## Making the changes

- **Profile Constants, layout, methods, rule checks, tiers:** edit the new version's JSON. Each constant keeps its `source` field: update it to the new document and page.
- **Unit-cost amounts:** never edit the existing data file (for example `he_travel_unit_costs_c2024_5405.json`): accepted versions read it. Copy it to a new file named after the new decision, such as `he_travel_unit_costs_c2025_1234.json`. Change the amounts and its `source` block (decision, date, version, URL) and keep the page references accurate. Then point the new version's `unit_cost_tables` entries at the new file.
- **Source documents:** the new version's `provenance` lists every document it rests on. Each entry needs a `document` and a `version`, the decision number, release or date. For an unchanged document, copy its version from the old document if the old entry has none, or ask the user. A new data file is listed with its `file` path too. Acceptance refuses a version whose source documents lack a version, or that reads a new data file its source documents do not list.

## Checks while drafting

- `ENGINE profile-diff <id> <previous> <new>` shows every change. Compare it with the agreed list: nothing missing, nothing extra.
- `uv run --project <engine> pytest tests/test_profile_maintainer.py::test_accepted_profile_versions_are_unchanged` passes as long as no accepted file was touched. If it fails, undo the edit to the accepted file (`git checkout -- <file>`) and make the change in the new version instead.

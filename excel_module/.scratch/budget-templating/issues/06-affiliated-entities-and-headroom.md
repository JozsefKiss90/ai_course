# 06 — Affiliated Entities and headroom capacity

**What to build:** Builds accept the number of Affiliated Entities per Beneficiary and a headroom.
- Each AE gets its own block, listed under its Beneficiary in the `BE list` and in every per-BE structure.
- Per-BE/AE column blocks are built up to count + headroom, so a late partner can join without a rebuild.
- Row-wise structures (Beneficiaries, AEs, WPs) grow through Excel Tables with structured references, so adding a row keeps every formula working.
- With no override, the profile's default headroom applies (HE +3).

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Shape Parameters contract extended with AEs per Beneficiary and headroom override
- [x] AE blocks appear under their Beneficiary, following the Official Budget Table's `BE list` convention
- [x] Spare blocks up to count + headroom exist and calculate correctly once filled
- [x] A Transfer View exists per Beneficiary and per AE
- [x] Structural checks verify block counts including headroom, across several combinations
- [x] Synthetic Check covers a scenario that fills a spare block and adds a Table row; both flow through to the Transfer View

## Notes (implementation)

- Contract: `affiliated_entities` is a list with one whole number per Beneficiary (e.g. `[1, 0, 2]`); it defaults to none. `headroom` defaults to the profile's (HE +3). The Cover records both.
- AE codes follow the Official Budget Table's VBA convention, `BEn-AEx`, listed directly under their Beneficiary with the role "Affiliated entity".
- Blocks: `ShapeParameters.slots` is every Beneficiary and AE in `BE list` order, then `SPARE1…SPAREh`. Each slot gets a Rate Table row, a staff effort row per WP and its own Transfer View (`Transfer View BE1-AE1`, `Transfer View spare 1`). Spare rows are outline-grouped, not hidden.
- A spare block's BE/AE nr is a Human Input in Rate Table column A. A late partner is added to the `BE list` and claims a spare block by typing its code there; the block's acronym and Transfer View name follow by lookup.
- `BE list` and `WP list` are Excel Tables (`BEList`, `WPList`). Every other sheet reaches them by code through structured references (`INDEX/MATCH` over `BEList[[BE/AE nr]]`), never by cell address. A structural check enforces this, because an inserted row moves cells.
- Per-WP structures are still built for the requested WP count. A WP row added to `WP list` breaks no formula, but it gets no Transfer View block until a rebuild.
- Synthetic Check: with headroom, the provisional scenario inserts a late AE of BE1 into `BEList` (via COM `ListRows.Add`, after the build's inputs are typed in) and fills the first spare block for it. The other spare blocks are filled with a blank code. The check now also compares each Transfer View's name (text) with the reference model.
- Follow-up for ticket 11 (full HE Transfer View): the AE Transfer View keeps the profile's "BE TOTAL COSTS" header, where the Official Budget Table's AE columns say "AE TOTAL COSTS". Changing it means a profile data edit. The `BE list` side of the AE convention is complete.
- Follow-up for ticket 12 (Input Guards): nothing yet stops two spare blocks claiming the same BE/AE nr, or a spare block claiming a code that already has a block.
- "Column blocks" in the spec are implemented as per-BE/AE rows (Rate Table, Staff effort) and one Transfer View sheet per block, because no current sheet lays BEs out as columns.

# 06 — Affiliated Entities and headroom capacity

**What to build:** Builds accept the number of Affiliated Entities per Beneficiary and a headroom.
- Each AE gets its own block, listed under its Beneficiary in the `BE list` and in every per-BE structure.
- Per-BE/AE column blocks are built up to count + headroom, so a late partner can join without a rebuild.
- Row-wise structures (Beneficiaries, AEs, WPs) grow through Excel Tables with structured references, so adding a row keeps every formula working.
- With no override, the profile's default headroom applies (HE +3).

**Blocked by:** 05 — Synthetic Check harness

**Status:** ready-for-agent

- [ ] Shape Parameters contract extended with AEs per Beneficiary and headroom override
- [ ] AE blocks appear under their Beneficiary, following the Official Budget Table's `BE list` convention
- [ ] Spare blocks up to count + headroom exist and calculate correctly once filled
- [ ] A Transfer View exists per Beneficiary and per AE
- [ ] Structural checks verify block counts including headroom, across several combinations
- [ ] Synthetic Check covers a scenario that fills a spare block and adds a Table row; both flow through to the Transfer View

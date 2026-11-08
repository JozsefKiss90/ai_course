# 10 — Itemised list Estimation Method

**What to build:** A generic itemised list sheet (items × cost per item), switched on via the method switches, where any other cost line can be entered per BE/AE × WP with the same structure. It outputs in the Estimation Method contract shape and supplies its reference-model function.

**Blocked by:** 05 — Synthetic Check harness

**Status:** done

- [x] Item rows grow through an Excel Table; cost line chosen from a validated list of the profile's cost categories
- [x] Number of items and cost per item are Human Inputs
- [x] Output feeds the matching Transfer View cost lines
- [x] Reference-model function added; Synthetic Check covers items spread across several cost lines

## Notes (implementation)

- Profile `he-lump-sum` 1.0: `itemised_list` is allowed and on by default (switch it off by leaving it out of `methods`). `method_settings.itemised_list.cost_lines` lists the lines no other method fills: `B`, the five C.3 lines and `D1`–`D5`. Profile 1.0 was edited in place, as in tickets 08–09: no Golden Scenario is pinned yet (ticket 15).
- `Itemised list` sheet: Excel Table `Items`, 15 blank rows. Human Inputs `("itemised", n, field)`: BE/AE nr, WP, Cost line, Item, Number of items, Cost per item. Total = number × cost per item, a calculated column.
- The cost lines a human can pick are listed by label in column I and the validation points at that range. An inline list would not work: labels hold commas ("Other (shipment, insurance, translation, etc.)") and together exceed Excel's 255-character limit. A line with no label of its own (HE's `B`) takes the label of the heading above it ("B. DIRECT SUBCONTRACTING COSTS").
- `Itemised list summary`: one row per BE/AE block × WP × cost line. Items = SUMIFS of the number of items; total = SUMIFS of the totals. The WP and cost line criteria point at the row's own C/D cells, not at quoted literals, so a label's quotes or commas cannot break the formula. Each row feeds its own Transfer View line. A spare block sums only once a code is typed for it.
- Synthetic Check: the provisional scenario enters 8 items over 7 cost lines and every BE/AE (the late AE included). It covers fractional numbers, a blank cost and a blank number, and two rows on the same BE/AE × WP × line. It then appends item 16 to the Table with inputs only. A sabotage test drops the number of items from the total and fails the check.
- Build time: the itemised list adds about 37k cells on the 25 BE × 15 WP shape. Two general speedups keep builds fast: `put_input`/`put_derived` copy a cached style per workbook instead of reassigning fill/border, and the bare-number check memoizes tokenizing on the formula with its cell references normalised. The extreme-shape time budget in `test_structural_checks_pass_across_shapes` was raised from 5 s to 10 s (agreed with the user). That shape builds in about 7 s.

### Known gaps / follow-ups

- Nothing stops a profile from listing, in `itemised_list.cost_lines`, a line another method also fills. The Transfer View would add both, which may be intended (e.g. extra C.1 costs) or a double count.
- A WP a human adds to `WP list` gets no summary rows until a rebuild (the same gap as in tickets 06–09).
- `cost_lines` refuses labels SUMIFS would not match exactly: those holding `*`, `?` or `~`, those starting with `<`, `>` or `=`, and duplicate labels. The reference model compares labels by equality, so it agrees with Excel only for such labels. All current HE labels pass.
- To confirm: D1–D5 are in the itemised list. The PRD's Out of Scope calls "topic-specific D-lines (D.2–D.5)" v2. This reads as dedicated D-line methods, not plain items × cost entry. If not, drop D2–D5 from `cost_lines`.
- Review follow-up: the itemised list, equipment depreciation and the travel planner repeat the same "item Table + SUMIFS summary + reference" shape (`_col`/`_this_row`, the BE/WP validations, the summary loop with its spare-block guard, the reference filter). Extract a shared helper before a fourth such method.

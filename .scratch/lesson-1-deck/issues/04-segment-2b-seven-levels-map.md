# 04 — Segment 2B slides: The 7 Levels map

**What to build:** The ~5-minute course-map segment plays as finished slides: the 7 Levels framework rendered as a presentable visual (a progression, not a dense wall-of-text table), each level with its name, its research-management translation, and where the course covers it; the one-sentence vibe-coding aside placed at the Level 4–5 rows; and the closing teaser — the KM System diagram (Wiki Sandbox → Markdown Generator → Personal Vault) with the "by Week 8, you will have built this" line. Terminology follows the ubiquitous language in `CONTEXT.md`.

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] The 7 Levels are legible from the back of a Teams call — visual progression, not a pasted markdown table
- [x] "You are (probably) here" marker on Level 1 and course-coverage mapping per level
- [x] Vibe-coding mentioned in exactly one sentence, positioned as out of scope
- [x] KM System teaser diagram slide uses CONTEXT.md terms (Wiki Sandbox, Markdown Generator, Personal Vault)
- [x] Speaker notes keep the pace instruction: one sentence per level, no dwelling

## Comments

**2026-08-31 (agent):** Implemented. Two slides in `deck/segments/seg2b_seven_levels.py`. The map slide renders the framework as an ascending stair — Level 1 at the bottom, each row indented further as the level rises — with a navy number badge, a bar carrying the level name plus a compressed research-management translation, and a coverage chip per row (orange "◀ You are (probably) here" on Level 1, blue chips for the course-covered Levels 2–5, muted chips for the Levels 6–7 outlook). The vibe-coding aside is one italic sentence inserted between the Level 5 and Level 4 rows; a test asserts "vibe coding" appears exactly once deck-wide. The teaser slide draws the KM System as three cards (Wiki Sandbox → Markdown Generator → Personal Vault, CONTEXT.md terms) with a Round-Trip return line and an orange "By Week 8, you will have built this." band. Speaker notes on both slides carry the pace instruction (one sentence per level, no dwelling) and the Level 1 → 4–5 close. Review fixes applied: unused imports dropped, chip bold folded into the treatment map, teaser sub-line aligned with the Anchor Project definition ("real or fictional"). The reviewer's duplicate-shape observations (in-row shape ritual, cards-with-arrows flow shared with seg2a) were left as-is — both match the house idiom at two occurrences; extract a `template.add_flow` if segment 3+ repeats the shape. Tests: 7 new segment-2B assertions (26 passing); slides visually verified via PowerPoint COM PNG export.

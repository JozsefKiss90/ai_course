# 08 — Integration pass: flow, timing, consistency

**What to build:** The assembled deck reviewed and polished end-to-end so it is ready to present: no placeholder slides remain, slide counts per segment are sane against the segment timings (a 10-minute segment shouldn't carry 15 slides), styling and terminology are consistent across all segments (ubiquitous language from `CONTEXT.md` throughout — Anchor Project, Sensitive Lane, Daily Driver, KM System, etc.), every slide has speaker notes, all live-demo cues are marked, and the regenerated `.pptx` opens cleanly as the final deliverable.

**Blocked by:** 02, 03, 04, 05, 06, 07.

**Status:** resolved

- [x] Zero placeholder slides; full deck regenerates from the build script in one run
- [x] Slide count per segment reviewed against the Timing Overview durations; overloaded segments trimmed
- [x] Terminology audit against CONTEXT.md passes (no forbidden synonyms like "homework week" or "team wiki")
- [x] Visual consistency check: fonts, colors, footer, divider style uniform across segments
- [x] Every content slide has speaker notes; every live-demo moment has a marked cue

## Comments

**2026-08-31 (agent):** Integration pass done; the deck is presentation-ready. The audits are encoded as a deck-wide integration-test section in `tests/test_deck.py` (6 new tests, 54 total passing): zero placeholders anywhere; per-segment slide counts pinned and density-guarded against the Timing Overview durations (densest is Segment 2 at 9 slides / 15 min, a deliberately fast tour — nothing needed trimming); terminology audit over all slide text + notes against the CONTEXT.md Avoid-lists (17 forbidden terms including "use case", which is safe to forbid since the canonical term is hyphenated); every non-divider slide has non-empty speaker notes; exactly three LIVE DEMO cues (the three demo switches — tiktokenizer, Demo 1, Demo 2; meta-prompting and the live pattern run inside Demo 2, cued in notes), each mirrored in notes; and every text run deck-wide uses an explicit Segoe UI font and size. Beyond the tests: full text+notes dump read end-to-end for flow (cross-references between segments all line up — Perplexity→L3, agent→L5, prompt library→L4, Practice Week 1→W3) and all 32 slides visually reviewed via exported PNGs (fonts, colors, footer, divider style uniform; no overflows). One inconsistency found and fixed: "neighbour" → "neighbor" (deck is otherwise American English). Deck rebuilt in one run and COM-verified to open cleanly in real PowerPoint. Two-axis review run; its real findings fixed: the vacuous timing assertion now derives durations from TIMING_OVERVIEW and acts as a guard on future pin bumps, "use case" added to the forbidden list (the prior exclusion rationale was wrong), the demo-cue test guards has_notes_slide before reading notes, and the font test renamed so it no longer overclaims the whole visual-consistency criterion. Known limits noted as judgement calls, not gaps: `_is_divider` is a text heuristic, and colors/footer/divider uniformity rest on the master/theme test plus the manual PNG pass.

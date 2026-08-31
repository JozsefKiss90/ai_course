# 01 — Deck skeleton and design template

**What to build:** Opening the generated PowerPoint file shows the entire shape of the Lesson 1 session at a glance: a title slide ("Lesson 1 — Why AI, How LLMs Work, and the Map Ahead", course name, Week 1), a section divider for each of the five segments with its duration and mode, and placeholder slides for the full slide inventory implied by `lesson_1.md`. A consistent visual template (fonts, colors, footer) applies to every slide. The deck is produced by running a python-pptx build script checked into the repo — every later ticket adds its slides through this script, so the deck is always regenerable from source.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] Running the build script produces a `.pptx` that opens cleanly in PowerPoint
- [x] Title slide + five section dividers present, each divider showing segment name, duration, and mode (per the Timing Overview table)
- [x] Master layout defines fonts, color scheme, and a footer used by all slides
- [x] Placeholder slides exist for each segment's content so the full slide count is visible
- [x] The build script has an obvious place for each segment's slides to be added independently (one function/module per segment)

## Comments

**2026-08-31 (agent):** Implemented. `python -m deck.build` writes `dist/lesson_1_deck.pptx` (32 slides: title + 5 dividers + 26 placeholders). Verified opening in real PowerPoint via COM, not just python-pptx round-trip — this caught a genuine corruption bug: the stock template's master carries shape ids near 2^31, so ids from `shapes._next_shape_id` exceed PowerPoint's signed 32-bit limit; fixed with `template.master_next_id()` (see the gotcha in `deck/README.md`). Theme fonts (Segoe UI) and the navy/blue color scheme are written into the master's theme part; the footer lives as master shapes inherited by every slide. One module per ticket under `deck/segments/` (segment 2 split into 2A/2B matching tickets 03/04); tickets 02–07 each edit exactly one module. Tests: `tests/test_deck.py` (7 passing) asserts structure against a saved-and-reopened file, with the Timing Overview table as independent oracle. Two-axis code review run: no standards violations; smell-level findings (private-member reach, unused default, duplicated styling block) fixed.

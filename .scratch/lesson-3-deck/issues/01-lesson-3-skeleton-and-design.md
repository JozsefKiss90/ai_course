# 01 — Lesson 3 skeleton with a third design template

**What to build:** `python -m deck.lesson3.build` writes `dist/lesson_3_deck.pptx` with a look clearly distinct from Lessons 1 (dark navy, Segoe) and 2 (warm paper, Cambria/Calibri, teal/violet): a title slide ("Lesson 3 — Knowledge Capture: NotebookLM and the Personal Vault", course name, Week 4, 90 minutes), a section divider per segment with name, duration and mode from the plan's Timing Overview, and a footer ("Lesson 3 · Week 4"). The template keeps the Lesson 1/2 builder call shapes (`add_title_slide`, `add_section_divider`, `add_content_slide`, `add_placeholder_slide`, `add_demo_cue`, `add_card`, `add_band`, `add_label`, `add_open_card`, `add_list_card`, `add_detail_card`, `add_lane_tag`) and colour-codes by lane: one accent for the Daily Driver (every cloud call), one for local (nothing leaves the machine); the template docstring is the contract. A new test file asserts the structure against a saved-and-reopened file with the plan's Timing Overview as the oracle.

**Blocked by:** —

**Status:** resolved

- [x] Lesson 3 builds with its own command to its own output file; Lessons 1 and 2 untouched
- [x] Title slide, five dividers in session order with duration and mode; master footer and theme fonts; palette and fonts differ from both earlier lessons
- [x] Builders exist with the Lesson 2 call shapes; the lane colour-coding is documented in the template docstring
- [x] `tests/test_lesson3_deck.py` passes its structure tests

## Comments

**2026-09-24 (agent):** Implemented. `python -m deck.lesson3.build` writes `dist/lesson_3_deck.pptx`. Design: a cool grey-blue canvas, Georgia over Arial, a vertical accent bar beside each title, numbered-disc dividers with an ink band across the top — neither Lesson 1's navy nor Lesson 2's warm paper. Two accents: amber = Daily Driver (every cloud call), green = local; the template docstring is the contract. All Lesson 2 call shapes kept, plus `add_table` for the plan's tables. Structure tests in `tests/test_lesson3_deck.py` against a saved-and-reopened file.

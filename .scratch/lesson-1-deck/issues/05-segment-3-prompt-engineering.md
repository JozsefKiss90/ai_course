# 05 — Segment 3 slides: Prompt engineering backdrop

**What to build:** The support slides behind the 25-minute live Gemini demo. The facilitator demos live; the slides anchor what participants should retain: the three-way escalation (Google-style → better → ICC) shown side by side, the full ICC demo prompt readable on screen (Instruction/Context/Constraints visually separated), the two shortcuts (ask-me-first, reverse prompt) with their exact append-phrases, the meta-prompting move with its example prompt, the four prompt patterns (persona, example-driven, step-by-step, critique-then-improve) each with its research-management example, and the two rules stated while demoing (nothing you couldn't publish; verify anything factual). Demo cues mark where the presenter switches to Gemini.

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] Three-way comparison slide makes the quality-scales-with-input point visually
- [x] The ICC prompt from the lesson plan appears verbatim, formatted so its three blocks are distinguishable on screen
- [x] The two shortcut phrases and the meta-prompting example prompt appear verbatim (participants copy these)
- [x] Four-patterns slide: one line + one example each, matching the lesson plan's research-management examples
- [x] The two safety rules get a slide; demo-switch cues marked in speaker notes with the rough 8/17-minute split

## Comments

**2026-08-31 (agent):** Implemented in `deck/segments/seg3_prompt_engineering.py` — six slides replacing the six placeholders (deck stays at 32 slides). Three-way escalation as cards with the "output quality scales with input quality" band; ICC prompt as three labeled block rows; shortcut phrases, meta-prompt, and all four pattern examples verified character-exact against `lesson_1.md` (whitespace reflow only). Demo cues: on-slide `add_demo_cue` bands mark the two Gemini switches (slide 1 → Demo 1, slide 3 → Demo 2), with the ≈8/≈17-minute split in the notes; slides 4–5 continue Demo 2 so they carry no new switch cue. TDD: nine seg3 tests added to `tests/test_deck.py` (red first), 34 passing against a saved-and-reopened file; deck also opened via PowerPoint COM and all six slides exported/visually checked. Two-axis code review run: spec axis found all five checkboxes met, nothing missing; standards axis found no hard violations — its two cheap findings (WHITE import inconsistency, `Inches(12.13)` literals where `CONTENT_WIDTH` exists) fixed.

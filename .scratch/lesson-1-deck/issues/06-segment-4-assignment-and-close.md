# 06 — Segment 4 slides: Assignment briefing + close

**What to build:** The 10-minute briefing plays as finished slides participants can screenshot: the five-part weekly assignment (pick the Anchor Project + 5-sentence description; three ICC prompts with at least one pattern; one ask-me-first; one meta-prompt; bring everything to Lesson 2), the expected effort (~1–2 hours across the week) and the debrief format (2–3 volunteers present), plus the close — next week's two-lane teaser (Sensitive Lane vs. Daily Driver, without teaching it yet).

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] Assignment slide(s) enumerate all five items exactly as in the lesson plan, screenshot-friendly
- [x] Anchor Project introduced with the anonymize-or-fictional rule and its role as the course-long thread
- [x] Effort expectation and Lesson 2 debrief format stated
- [x] Close slide teases the two-lane rule using CONTEXT.md terms without explaining it
- [x] Speaker notes on every slide

## Comments

**2026-08-31 (agent):** Implemented in `deck/segments/seg4_assignment_close.py` — four slides replacing the placeholders: Anchor Project (real-anonymized vs. fictional cards + course-long-thread band), the five-part assignment as numbered rows on one screenshot-friendly slide (all five items, with the four pattern names spelled out so the screenshot is self-contained), effort + debrief (~1–2 h, Lesson 2 debrief, 2–3 volunteers), and the close teasing Sensitive Lane / Daily Driver as an open question with the answer deferred to Lesson 2. Speaker notes on all four. Tests: 7 new assertions in `tests/test_deck.py` (40 total passing); deck rebuilt, COM-verified to open cleanly in real PowerPoint, and the four slides visually checked via exported PNGs. Two-axis code review run: no standards violations (a few noted judgement-call smells left as-is — the two-column geometry constants and the per-segment test-pair duplication are repo-wide idioms worth a later template/parametrization ticket); spec review's one real gap (pattern names missing from the assignment slide) fixed, plus two note-level fixes (canonical "Session Template" term; dropped the unbacked "deck is shared" promise).

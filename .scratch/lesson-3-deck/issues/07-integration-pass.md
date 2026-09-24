# 07 — Integration pass: flow, timing, lane colour, docs

**What to build:** The assembled Lesson 3 deck reviewed end-to-end: no placeholders; slide counts per segment pinned and held under one slide per minute; the dividers' durations plus the buffer add up to the 90 minutes the title slide promises; speaker notes on every content slide; every live-demo cue in Segment 2 or 3 and mirrored in its notes; no YouTube URL; one spelling of anonymise; terminology audit against the CONTEXT.md Avoid-lists (including bare "Copilot" for the plugin); explicit fonts everywhere; the look distinct from Lessons 1 and 2; the file opens in real PowerPoint and the exported slides reviewed for overflow. Docs: `deck/README.md` gains the Lesson 3 section and `com_check` opens all three decks.

**Blocked by:** 02, 03, 04, 05, 06

**Status:** resolved

- [x] Deck-wide tests in `tests/test_lesson3_deck.py`
- [x] COM check passes for all three decks; exported slides reviewed
- [x] README and com_check updated; Lessons 1 and 2 tests still pass

## Comments

**2026-09-24 (agent):** Integration pass done: 33 slides (title, five dividers, 3/9/8/3/4), zero placeholders, counts pinned and under one slide per minute, dividers plus the 2-minute buffer equal the 90 minutes promised, notes on every content slide, live-demo cues only in Segments 2–3 and mirrored in notes, no YouTube URL, one spelling of anonymise, terminology audit (each forbidden term asserted to be on a CONTEXT.md Avoid-list first), never bare "Copilot", lane colours only where the slide names that kind of tool, no Lesson 2 teal. All three decks open in real PowerPoint via `python -m deck.com_check`; all 33 slides exported as PNG and reviewed — no overflow; long titles now auto-shrink to one line. README gained the Lesson 3 section; `com_check` opens all three decks by default.

**2026-09-24 (agent, after code review):** Two-axis review run. Standards: the README's surrounding framing ("two lessons", the build block, the tests sentence, the pre-flight step) had not been updated with the new section — fixed; dead imports and an unused badge-size parameter removed; the badge and numbered-row helpers duplicated across Segments 2 and 3 moved into the template as `add_badge` / `add_numbered_rows`. Left as they are: the `Status: resolved` convention (every ticket in the repo uses it), and the per-lesson test helpers the README's convention endorses. Spec: live-demo cues now sit on every slide a demo step runs against (seven cues; Segment 2's step 6 is slide-only by the plan, and a test pins the count); the plugin table's Lane cell regained the "nothing from the never list is ever in the vault" clause; the fresh-install and key-flow prep item reached the setup notes; the Perplexity retention line, the Gems sentence that re-taught Lesson 2, and the invented fix wording came off the slides; the 50-a-day cap is said once, in the hands-on notes (test added). Judgement calls kept: the setup slide quotes Obsidian's menu path with the qualifier ("Settings → Copilot for Obsidian") because CONTEXT.md forbids the bare name; bare "wiki" as the retired thing's name is now a recorded decision in the spec.

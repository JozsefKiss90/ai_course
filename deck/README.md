# Deck build

One package, two lessons, one set of mechanics. Regenerate a deck any time with:

```
python -m deck.build            # Lesson 1 → dist/lesson_1_deck.pptx
python -m deck.lesson2.build    # Lesson 2 → dist/lesson_2_deck.pptx
```

Output goes to `dist/` (git-ignored — the source of truth is this package).
Requires Python 3.11+ and `python-pptx`. Tests: `python -m pytest` (`tests/test_core.py` for the shared core, `tests/test_deck.py` for Lesson 1, `tests/test_lesson2_deck.py` for Lesson 2). After a build, `python -m deck.com_check` opens the decks in real PowerPoint (Windows + pywin32) — the check that catches what a python-pptx round-trip does not.

## Core vs. per-lesson template

- `core.py` — **mechanics**, lesson-independent: presentation setup at 16:9, writing fonts and colours into the theme part, the master footer, `master_next_id()` (see the gotcha below), the `solid`/`outlined` shape styles, `style(run, ...)`, and the blank-slide, text-box and notes helpers. A lesson hands it a `core.Design` (fonts, theme colour scheme, canvas, footer text and colours) and gets a presentation back. Nothing here knows a palette or a layout.
- `template.py` (Lesson 1) and `lesson2/template.py` (Lesson 2) — **design**, one per lesson: the colour constants, the `Design` handed to the core, and the slide builders and in-slide blocks segment modules call. Both templates define the same slide builders and in-slide blocks with the same call shapes (`add_title_slide`, `add_section_divider`, `add_content_slide`, `add_placeholder_slide`, `add_demo_cue`, `add_card`, `add_band`, `add_label`), so segment authors work the same way in either lesson. Lesson 1's template re-exports the core helpers segment modules use (`solid`, `add_bar`, `set_notes`) so segment modules keep calling `template.solid(...)`.

Adding a lesson means adding a sub-package like `lesson2/` (its own `template.py`, `build.py`, `segments/`), never editing the core for a design reason.

## Lesson 1 — where slides come from

- `build.py` — session order: title slide, then per segment a divider + that segment's slides. Segment names/durations/modes mirror the Timing Overview in `lesson_1.md`.
- `template.py` — the single source of visual truth for Lesson 1: fonts, colors, footer, and the slide builders (`add_content_slide`, `add_section_divider`, `add_placeholder_slide`, `add_demo_cue`) and the in-slide building blocks (`add_card`, `add_label`, `add_band`). Segment modules style their custom shapes with `template.solid(shape, color)` and `template.style(run, ...)` plus the color constants. The content area for custom shapes is `CONTENT_LEFT/TOP/WIDTH/HEIGHT`.
- `segments/` — one module per segment, each exposing `add_slides(prs)`. Segment 1's two chart slides and Segment 2A's what-is-an-LLM slide embed images from `.scratch/` at build time, so those files are build inputs, not just reference material. Tickets 02–07 each replace the placeholders in exactly one module:

| Module | Ticket |
|---|---|
| `seg1_why_this_matters.py` | 02 |
| `seg2a_llm_fundamentals.py` | 03 |
| `seg2b_seven_levels.py` | 04 |
| `seg3_prompt_engineering.py` | 05 |
| `seg4_assignment_close.py` | 06 |
| `seg5_setup_block.py` | 07 |

Add real slides with `template.add_content_slide(...)` (returns the slide for custom shapes), set speaker notes via `template.set_notes(slide, ...)`, and mark live-demo cues in both the slide and its notes.

## Lesson 2 — where slides come from

- `lesson2/build.py` — session order per the Timing Overview in `lesson_2.md`: title slide, then per segment a divider + that segment's slides. Each `Segment` names the lane it lives in (Segment 3 → Sensitive Lane, Segment 4 → Daily Driver, the rest neutral) and the divider takes that lane's colour.
- `lesson2/template.py` — the single source of visual truth for Lesson 2: a light paper canvas, Cambria headings over Calibri body, and two lane colours (teal = Sensitive Lane / Copilot Chat (Basic), violet = Daily Driver / Google Gemini) that mean the lane wherever they appear — the module docstring is the colour-coding contract. Builders take an optional `lane=template.SENSITIVE_LANE` / `template.DAILY_DRIVER`; `add_lane_tag` puts the lane chip on a custom slide. Same call shapes as Lesson 1, plus `lane=`.
- `lesson2/segments/` — one module per segment, each exposing `add_slides(prs)`. Tickets 04–08 each replace the placeholders in exactly one module:

| Module | Segment | Ticket |
|---|---|---|
| `seg1_recap_debrief.py` | 1 — Recap + assignment debrief | 04 |
| `seg2_sensitive_data_rule.py` | 2 — The sensitive-data rule and data-protection principles | 05 |
| `seg3_copilot_in_practice.py` | 3 — Copilot Chat (Basic) in practice (Sensitive Lane) | 06 |
| `seg4_gemini_in_depth.py` | 4 — Gemini in depth (+ NotebookLM preview) (Daily Driver) | 07 |
| `seg5_assignment_close.py` | 5 — Assignment briefing + close | 08 |

Add real slides with `template.add_content_slide(..., lane=...)`, set speaker notes via `template.set_notes(slide, ...)`, mark live-demo cues with `template.add_demo_cue(..., lane=...)` on the slide and in its notes, and colour-code cards by lane with `fill=template.SENSITIVE_TINT` / `template.DAILY_TINT` (a lane's `.color` as fill gives a solid label block).

## Gotcha

Never add master shapes via `shapes._next_shape_id` — it scans every id in the master part, including the stock template's slide-layout ids (`p:sldLayoutId`, numbered from 2^31), and PowerPoint rejects files whose shape ids exceed the signed 32-bit range. Use `core.master_next_id()`, which looks at shape ids only — the core's own footer goes through it.

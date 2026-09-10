# Deck build

One package, two lessons, one set of mechanics. Regenerate a deck any time with:

```
python -m deck.build            # Lesson 1 → dist/lesson_1_deck.pptx
python -m deck.lesson2.build    # Lesson 2 → dist/lesson_2_deck.pptx
```

Output goes to `dist/` (git-ignored — the source of truth is this package).
Requires Python 3.11+ and `python-pptx`. Tests: `python -m pytest` (`tests/test_core.py` for the shared core, `tests/test_deck.py` for Lesson 1).

## Core vs. per-lesson template

- `core.py` — **mechanics**, lesson-independent: presentation setup at 16:9, writing fonts and colours into the theme part, the master footer, `master_next_id()` (see the gotcha below), the `solid`/`outlined` shape styles, `style(run, ...)`, and the blank-slide, text-box and notes helpers. A lesson hands it a `core.Design` (fonts, theme colour scheme, canvas, footer text and colours) and gets a presentation back. Nothing here knows a palette or a layout.
- `template.py` (Lesson 1) and `lesson2/template.py` (Lesson 2) — **design**, one per lesson: the colour constants, the `Design` handed to the core, and the slide builders and in-slide blocks segment modules call. Both templates keep the same call shapes (`add_content_slide`, `add_section_divider`, `add_placeholder_slide`, `add_demo_cue`, `add_card`, `add_band`, `add_label`) so segment authors work the same way in either lesson. Lesson 1's template re-exports the core helpers segment modules use (`solid`, `add_bar`, `set_notes`) so segment modules keep calling `template.solid(...)`.

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

- `lesson2/build.py` — session order per the Timing Overview in `lesson_2.md`; ticket 03 of the Lesson 2 effort adds the title slide, dividers and placeholders.
- `lesson2/template.py` — Lesson 2's design on top of the core; ticket 03 replaces the provisional stand-ins with the real palette and builders.
- `lesson2/segments/` — one module per segment, each exposing `add_slides(prs)`; tickets 04–08 each own one module (the table lands with ticket 03).

## Gotcha

Never add master shapes via `shapes._next_shape_id` — it scans every id in the master part, including the stock template's slide-layout ids (`p:sldLayoutId`, numbered from 2^31), and PowerPoint rejects files whose shape ids exceed the signed 32-bit range. Use `core.master_next_id()`, which looks at shape ids only — the core's own footer goes through it.

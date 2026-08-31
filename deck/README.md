# Lesson 1 deck build

Regenerate the deck any time with:

```
python -m deck.build
```

Output: `dist/lesson_1_deck.pptx` (git-ignored — the source of truth is this package).
Requires Python 3.11+ and `python-pptx`. Tests: `python -m pytest tests/test_deck.py`.

## Where slides come from

- `build.py` — session order: title slide, then per segment a divider + that segment's slides. Segment names/durations/modes mirror the Timing Overview in `lesson_1.md`.
- `template.py` — the single source of visual truth: fonts, colors, footer, and the slide builders (`add_content_slide`, `add_section_divider`, `add_placeholder_slide`). The content area for custom shapes is `CONTENT_LEFT/TOP/WIDTH/HEIGHT`.
- `segments/` — one module per segment, each exposing `add_slides(prs)`. Tickets 02–07 each replace the placeholders in exactly one module:

| Module | Ticket |
|---|---|
| `seg1_why_this_matters.py` | 02 |
| `seg2a_llm_fundamentals.py` | 03 |
| `seg2b_seven_levels.py` | 04 |
| `seg3_prompt_engineering.py` | 05 |
| `seg4_assignment_close.py` | 06 |
| `seg5_setup_block.py` | 07 |

Add real slides with `template.add_content_slide(...)` (returns the slide for custom shapes), set speaker notes via `template.set_notes(slide, ...)`, and mark live-demo cues in both the slide and its notes.

## Gotcha

Never add master shapes via `shapes._next_shape_id` — the stock template's master uses ids near 2^31 and PowerPoint rejects files whose shape ids exceed the signed 32-bit range. Use `template.master_next_id()`.

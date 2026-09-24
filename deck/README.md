# Deck build

One package, three lessons, one set of mechanics. Regenerate a deck any time with:

```
python -m deck.build            # Lesson 1 → dist/lesson_1_deck.pptx
python -m deck.lesson2.build    # Lesson 2 → dist/lesson_2_deck.pptx
python -m deck.lesson3.build    # Lesson 3 → dist/lesson_3_deck.pptx
```

Output goes to `dist/` (git-ignored — the source of truth is this package).
Requires Python 3.11+ and `python-pptx`. Tests: `python -m pytest` (`tests/test_core.py` for the shared core, `tests/test_deck.py` for Lesson 1, `tests/test_lesson2_deck.py` for Lesson 2, `tests/test_lesson3_deck.py` for Lesson 3). After a build, `python -m deck.com_check` opens the decks in real PowerPoint (Windows + pywin32) — the check that catches what a python-pptx round-trip does not.

## Core vs. per-lesson template

- `core.py` — **mechanics**, lesson-independent: presentation setup at 16:9, writing fonts and colours into the theme part, the master footer, `master_next_id()` (see the gotcha below), the `solid`/`outlined` shape styles, `style(run, ...)`, and the blank-slide, text-box and notes helpers. A lesson hands it a `core.Design` (fonts, theme colour scheme, canvas, footer text and colours) and gets a presentation back. Nothing here knows a palette or a layout.
- `template.py` (Lesson 1), `lesson2/template.py` (Lesson 2) and `lesson3/template.py` (Lesson 3) — **design**, one per lesson: the colour constants, the `Design` handed to the core, and the slide builders and in-slide blocks segment modules call. Both templates define the same slide builders and in-slide blocks with the same call shapes (`add_title_slide`, `add_section_divider`, `add_content_slide`, `add_placeholder_slide`, `add_demo_cue`, `add_card`, `add_band`, `add_label`), so segment authors work the same way in either lesson. Lesson 1's template re-exports the core helpers segment modules use (`solid`, `add_bar`, `set_notes`) so segment modules keep calling `template.solid(...)`.

Adding a lesson means adding a sub-package like `lesson2/` (its own `template.py`, `build.py`, `segments/`), never editing the core for a design reason.

## Lesson 1 — where slides come from

- `build.py` — session order: title slide, then per segment a divider + that segment's slides. Segment names/durations/modes mirror the Timing Overview in `lesson_1.md`.
- `template.py` — the single source of visual truth for Lesson 1: fonts, colors, footer, and the slide builders (`add_content_slide`, `add_section_divider`, `add_placeholder_slide`, `add_demo_cue`) and the in-slide building blocks (`add_card`, `add_label`, `add_band`). Segment modules style their custom shapes with `template.solid(shape, color)` and `template.style(run, ...)` plus the color constants. The content area for custom shapes is `CONTENT_LEFT/TOP/WIDTH/HEIGHT`.
- `segments/` — one module per segment, each exposing `add_slides(prs)`. Segment 1's two chart slides and Segment 2A's what-is-an-LLM slide embed images from `.scratch/` at build time, so those files are build inputs, not just reference material. The deck is complete: tickets 02–07 each replaced the placeholders in exactly one module, and ticket 08 was the integration pass.

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
- `lesson2/template.py` — the single source of visual truth for Lesson 2: a light paper canvas, Cambria headings over Calibri body, and two lane colours (teal = Sensitive Lane / Copilot Chat (Basic), violet = Daily Driver / Google Gemini) that mean the lane wherever they appear — the module docstring is the colour-coding contract. Builders take an optional `lane=template.SENSITIVE_LANE` / `template.DAILY_DRIVER`; `add_lane_tag` puts the lane chip on a custom slide. Same call shapes as Lesson 1, plus `lane=` and three additions: `add_open_card` — a card with an edge bar and an empty text frame, for rows whose text is several runs at their own sizes (`add_card` is the fixed heading/body version of the same block) — and the two blocks built on those, `add_list_card` (a heading over bulleted items) and `add_detail_card` (a bold lead over one or more lines of detail; several lines take bullets, one does not).
- `lesson2/segments/` — one module per segment, each exposing `add_slides(prs)`. The deck is complete: tickets 04–08 each replaced the placeholders in exactly one module, ticket 09 was the integration pass, ticket 10 reworked Segment 5 so that it renders the assignment's workflow orchestration — the roadmap and the blueprint the plan authors — instead of describing one, ticket 12 redefined that route as eight steps with only the anonymisation step required, every step naming where its input comes from and where its output goes, Adobe Acrobat and the justification boxes dropped, and ticket 11 replaced Segment 2's data-protection-principles and dean's-directive slides with the AI data safety and ethics framework: the four pillars of trustworthy AI, the four pillars of data safety, the four ethical principles, and the sources behind them, with the two institutional directives folded into the framework slide as a reference strip.

| Module | Segment | Ticket |
|---|---|---|
| `seg1_recap_debrief.py` | 1 — Recap + assignment debrief | 04 |
| `seg2_sensitive_data_rule.py` | 2 — The sensitive-data rule and data-protection principles | 05 |
| `seg3_copilot_in_practice.py` | 3 — Copilot Chat (Basic) in practice (Sensitive Lane) | 06 |
| `seg4_gemini_in_depth.py` | 4 — Gemini in depth (+ NotebookLM preview) (Daily Driver) | 07 |
| `seg5_assignment_close.py` | 5 — Assignment briefing + close | 08, 10, 12 |

Add real slides with `template.add_content_slide(..., lane=...)`, set speaker notes via `template.set_notes(slide, ...)`, mark live-demo cues with `template.add_demo_cue(..., lane=...)` on the slide and in its notes, and colour-code cards by lane with `fill=template.SENSITIVE_TINT` / `template.DAILY_TINT` — or `fill=lane.tint` when the code loops over lanes (a lane's `.color` as fill gives a solid label block). A lane colour is only ever right where the slide names that lane's tool as where work goes.

## Lesson 3 — where slides come from

- `lesson3/build.py` — session order per the Timing Overview in `lesson_3.md`: title slide, then per segment a divider + that segment's slides. Segment 2 declares the Daily Driver, Segment 3 the local non-lane; the divider takes that colour. `BUFFER_MINUTES` is the plan's 2-minute buffer row, which the dividers do not show but the 90-minute title slide includes.
- `lesson3/template.py` — the single source of visual truth for Lesson 3: a cool grey-blue canvas, Georgia headings over Arial body, a vertical accent bar beside each title, numbered-disc dividers. Two accent colours, and they mean the same thing wherever they appear: amber = Daily Driver (every tool that calls a cloud model: NotebookLM, Copilot for Obsidian, Perplexity), green = local (Obsidian, Smart Connections: nothing leaves the machine). The Sensitive Lane is not demonstrated in this lesson and has no colour. Same call shapes as Lesson 2 (`lane=template.DAILY_DRIVER` / `template.LOCAL`, `DAILY_TINT` / `LOCAL_TINT`), plus `add_table` — a grid of white row cards with a header line, one edge bar per row — for the plan's tables, `add_badge` / `add_numbered_rows` for step lists (a numbered badge beside a text card, with an optional trailing cell for a timing), and a long title shrinks itself to stay on one line.
- `lesson3/segments/` — one module per segment, each exposing `add_slides(prs)`. The deck is complete: tickets 02–06 each own one module, ticket 07 was the integration pass.

| Module | Segment | Ticket |
|---|---|---|
| `seg1_recap_debrief.py` | 1 — Recap + assignment debrief | 02 |
| `seg2_km_system_notebooklm.py` | 2 — The KM System redrawn + NotebookLM in depth (Daily Driver) | 03 |
| `seg3_obsidian_vault.py` | 3 — Obsidian: the Personal Vault and its two plugins (local) | 04 |
| `seg4_hands_on_block.py` | 4 — Hands-on block: notebook + vault | 05 |
| `seg5_assignment_close.py` | 5 — Assignment briefing + close | 06 |

Two Lesson 3 rules the tests hold deck-wide: a colour appears only on a slide that names a tool of that kind (amber needs a cloud tool named, green a local one), and the Obsidian plugin is always "Copilot for Obsidian", never bare "Copilot" — CONTEXT.md's Avoid-list for the vault plugins.

## The plan is the oracle

`lesson_1.md`, `lesson_2.md` and `lesson_3.md` are the session plans, and the tests read them the way the decks do: segment names, durations and modes come from each plan's Timing Overview, and the segment tests assert the plan's content — its scenarios, its demo script, its assignment wording. Changing what a deck says starts in its plan; a slide the plan does not call for has nothing to test it against.

Alongside the per-segment tests, each lesson's module carries tests that guard the deck as a whole. Some are grouped under the lesson's integration-pass heading (`tests/test_deck.py` ticket 08, `tests/test_lesson2_deck.py` ticket 09, `tests/test_lesson3_deck.py` ticket 07) — no placeholders left, per-segment slide counts pinned and held under one slide per minute of that segment's duration, the divider durations still adding up to the length the title slide promises, speaker notes on every content slide, every live-demo cue mirrored in its notes, one spelling of *anonymise* deck-wide — and the rest sit in the module's other deck-wide sections: the terminology audit against the Avoid-lists in `CONTEXT.md`, an explicit font and size on every run, and, for Lesson 2, no YouTube URL anywhere. Lesson 2's lane separation is stated once, in the integration section: a segment that names a lane in `lesson2/build.py` never names the other lane, the brand of its tool, or the words that give that lane away.

## Before you present

Three checks, in this order:

1. `python -m pytest` — the whole suite, both lessons.
2. `python -m deck.build && python -m deck.lesson2.build && python -m deck.lesson3.build`, then `python -m deck.com_check` — a python-pptx round-trip is not proof that PowerPoint opens the file.
3. A visual pass over exported slide images, which is the part no test covers — overflowing cards, a band running into the footer, a colour that says the wrong lane. Export them with PowerPoint's own renderer:

   ```python
   import win32com.client
   app = win32com.client.Dispatch("PowerPoint.Application")
   pres = app.Presentations.Open(r"C:\...\dist\lesson_2_deck.pptx", True, False, False)
   pres.Export(r"C:\...\png_out", "PNG", 1280, 720)
   pres.Close(); app.Quit()
   ```

Delivery-time content checks belong to the facilitator, not to the build: Lesson 2's Gemini free-tier capabilities and the dean's directive's version are re-verified the week before the session (see "Materials to Prepare" in `lesson_2.md`).

## Gotcha

Never add master shapes via `shapes._next_shape_id` — it scans every id in the master part, including the stock template's slide-layout ids (`p:sldLayoutId`, numbered from 2^31), and PowerPoint rejects files whose shape ids exceed the signed 32-bit range. Use `core.master_next_id()`, which looks at shape ids only — the core's own footer goes through it.

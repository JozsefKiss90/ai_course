# 07 — Segment 4 slides: Gemini in depth + NotebookLM preview

**What to build:** The 15-minute Gemini segment plays as finished slides with live-demo cues: one capability per slide for what the free tier adds beyond Copilot — file and image upload, long context, Gems as persistent context (framed as the Level 3 move: a workspace that already knows your Anchor Project, with the ICC prompts from Lesson 1 becoming Gem instructions), Deep Research, Canvas for structured outputs and drafts, Google Workspace hooks, and any further free capability the plan lists — each with a research-management use case on the Anchor Project; then NotebookLM at use-case level only, flagged as the Lesson 3 tool: a YouTube link turned into a textual source, several documents aggregated in one notebook, a notebook imported into Gemini and used as a project folder. A closing slide shows how these chain (upload → Gem → Canvas; NotebookLM → Gemini) as the seed of the assignment's workflow thinking. Notes carry the demo script and a reminder to re-verify feature availability the week before. Copilot is not named anywhere in this segment.

**Blocked by:** 03 — Lesson 2 skeleton with a new design template.

**Status:** resolved

- [x] Segment 4 placeholders replaced; slides in plan order; lane colour-coding applied
- [x] Every capability in the plan's Gemini list has a slide with a use case; Gems slide states the Level 3 link
- [x] NotebookLM slide(s) carry exactly the three use cases and mark it as the Lesson 3 tool, no deeper
- [x] Demo cues present on the slides the plan marks as live, mirrored in notes; the word "Copilot" appears nowhere in this segment's slides or notes (tested)
- [x] No YouTube URL as a reference (the YouTube-to-source use case is described, not linked); speaker notes on every slide; deck rebuilds and tests pass

## Resolution

Fifteen slides in `deck/lesson2/segments/seg4_gemini_in_depth.py`, in the plan's order: an opener carrying the availability flag, one slide per row of the plan's capability table, the three NotebookLM scenarios, and the chaining close. The deck is 39 slides; `python -m pytest` is green and `python -m deck.com_check` opens it in real PowerPoint.

**One slide per capability, including the ones the plan only mentions.** The ticket asks for a slide per capability; the plan's demo script gives five of them 1.5 minutes between them. Both are honoured: every row of the table has its own slide, and the slides in the script's batch say in their notes which batch they are in and how many seconds they get, so the facilitator can read them at the pace the plan budgets. "Gemini Live and mobile" is the one row the script gives no time of its own — its notes say so, and that it is the first thing to drop when the segment runs long.

**"Use case" could not be used.** It is on CONTEXT.md's Avoid-list for Anchor Project, and the deck's terminology audit enforces it on slide text and notes. The slides say "scenario", which is what Segment 3 called the same thing.

**NotebookLM is slate, not violet.** The template's rule is that a lane colour says "this is about that tool", and NotebookLM is a different product the course does not open until Lesson 3. Its three slides keep the lane chip and are slate throughout, the same line Segment 3 drew around Canva and genspark.ai, and a test holds it. The chaining slide's first chain (upload → Gem → Canvas) is the Daily Driver end to end and takes the lane's tint; the second runs through NotebookLM and stays neutral.

**Fixed in review.** The video scenario had lost the plan's subject: the constraint bans a YouTube *link*, not the word, so the slide now names YouTube and still carries no URL (tested). The plan's note that the product was renamed "Gemini Notebook" in mid-2026 is now on the slide and in the notes, because the facilitator's screen may not say NotebookLM. The upload slide called one document both "anonymised" and "public" — it now says what is cleared and how. Two free-tier figures no cited source gives ("a window measured in hundreds of pages", "sixty pages") are gone; the notes tell the facilitator to state the real length of their own document. The Deep Research notes named the wrong five slides as the demo script's prepared-result batch, and said nothing about sitting in table order ahead of a live demo; both are now correct, with the choice spelled out.

**Judgement calls left standing.** Guided Learning and Workspace hooks are "slide only" in the plan but carry what the facilitator would type or do — that is the convention Segment 3 established and tests (`test_slide_only_tools_show_what_to_type_or_do`), not new scope. The Workspace-hooks slide keeps its one-line workaround, because a boundary a participant has to plan a workflow around is only useful with the alternative beside it.

**Standards cleanups applied.** `_scenario_slide` is now the one band-and-title primitive, with `_notebook_slide` differing only by its fill and the Lesson 3 flag; `_block_row` replaced twelve copies of the column arithmetic; the chaining slide's hand-drawn card edge became a fill the template already edges; and `_seg3_corpus`/`_seg4_corpus` collapsed into one `_segment_corpus`.

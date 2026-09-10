# 08 — Segment 5 slides: Assignment briefing + close

**What to build:** The 8-minute briefing plays as finished slides participants can screenshot: the assignment on one slide — chain all tools and capabilities introduced in the course so far into a multi-step workflow orchestration; produce a blueprint of the tool chaining and the workflow steps with detailed guidelines and a justification for each step; the deliverable is a presentation on a hand-picked topic designed for educational purposes and intended to facilitate learning outcomes; sensitive steps routed to the Sensitive Lane — with a small worked example of a blueprint row (step, tool, lane, why) so the shape is unambiguous; an outcome slide stating "Level 3 achieved, foundation for Level 4 established" against the 7 Levels map; effort expectation and where the work is shown (Practice Week 1 drop-in in W3, Lesson 3 debrief); and the close pointing to Practice Week 1 and Lesson 3 (NotebookLM, Perplexity, Wiki Sandbox).

**Blocked by:** 03 — Lesson 2 skeleton with a new design template.

**Status:** resolved

- [x] Segment 5 placeholders replaced; slides in plan order
- [x] Assignment slide carries all assignment elements as in the plan, on one screenshot-friendly slide, with the blueprint example row
- [x] Outcome slide names Level 3 as achieved and Level 4 as the foundation laid
- [x] Close names Practice Week 1 (W3) and Lesson 3's tools using CONTEXT.md terms
- [x] Speaker notes on every slide; deck rebuilds and tests pass


## Resolution

Four slides in `deck/lesson2/segments/seg5_assignment_close.py`, in the plan's order: the assignment, the outcome on the 7 Levels map, the effort and its two venues, the close. The deck is 40 slides; `python -m pytest` is green and `python -m deck.com_check` opens it in real PowerPoint. Every slide was exported through PowerPoint and read back.

**The outcome is a slide, not a line.** The plan states it as a result — Level 3 achieved, foundation for Level 4 established — and a result only means something against the map it is measured on. So three rows of Lesson 1's 7 Levels appear: Level 2 as last week's work, Level 3 as this week's, Level 4 as what the blueprint founds. The level names are read out of `lesson_1.md`'s table at test time, so the two lessons cannot drift on what a level is called. That makes Segment 5 four slides where the skeleton had three placeholders.

**The worked blueprint row is the reason the assignment slide earns its density.** "Produce a blueprint of the tool chaining" is a sentence a participant can read twice and still not know what to write down. One filled row settles it: the step with its input and its output, the tool, the lane, and the justification. The plan asks a step for six fields and the ticket names four columns; the sixth — the guidelines for running the step — does not fit a table cell, so the label under the row says they go beneath it in the participant's own document, and the notes say what they should read like.

**Fixed in review.** The worked row originally showed four of the step's six fields and named its input inside the justification cell; the step's own cell now carries in and out. The tool list's third column was headed "Outside both lanes", which reads as a third lane where CONTEXT.md defines two — it is now "The rest of the chain", and the notes say why those tools are not a lane rather than claiming they sit outside the tenant (NotebookLM and Gemini both do). The Level 3 status line claimed the room already works in a Gem, off the back of a demo they watched: it now says Level 3 arrives as soon as the Gem they saw built is their own, and the notes tell the facilitator to be honest about the tense.

**Standards cleanups applied.** `_numbered_row` lost the `status`/`status_color` parameters and returns its card, so the outcome map adds its own second line and the assignment's items stay one line; the levels became a small frozen dataclass rather than six-wide tuples. The blueprint columns are sized in proportion and always fill the content width, instead of four hand-tuned inch figures that had to sum. The lane columns take their names and tints from `SENSITIVE_LANE`/`DAILY_DRIVER` rather than re-pairing a literal string with a tint constant. `_slide_title`/`_segment_slide` moved out of the Segment 4 test block into the shared helpers, with `_seg4_slide` delegating.

**Left for ticket 09.** `EXPECTED_PLACEHOLDERS` in the tests is now `(0, ...)` for all five segments, so its two placeholder assertions can no longer fail and its live role is the divider-name registry `_segment_ranges` iterates — the integration pass is where it gets renamed or retired.

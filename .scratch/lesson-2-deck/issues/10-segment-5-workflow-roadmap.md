# 10 — Segment 5 rework: the assignment roadmap, not a slide about the assignment

**What to build:** Segment 5 redesigned completely so that it *is* the multi-step workflow orchestration rather than a description of one. Ticket 08's slide told participants to "produce a blueprint of the tool chaining"; that sentence is not runnable, and what it produced was a slide about the instructions. Author the blueprint itself — every step with its tool, input, output, detailed guidelines for running it, and a justification for why that tool at that step — covering every tool the course has taught so far (Gemini with Guided Learning, Deep Research, Gems, file upload, long context, Canvas and image generation; Copilot Chat (Basic) with Prompt Coach, Study and Learn and Adobe Acrobat; NotebookLM; Canva for the prototype and the video excerpt; genspark.ai for the deck), aimed at the plan's deliverable: a presentation on a hand-picked topic designed for educational purposes and intended to facilitate learning outcomes. Visualise the chain as a flowchart / Mermaid diagram, and render the blueprint as the segment's slides. Segment 5 is the assignment roadmap.

**Blocked by:** 08 — Segment 5 slides: assignment briefing + close.

**Status:** resolved

- [x] `lesson_2.md` Segment 5 rewritten to author the blueprint in full, with a Mermaid diagram of the chain
- [x] Segment 5 slides render the blueprint: the assignment, the roadmap, the nine steps, the outcome, the effort, the close
- [x] Every step states its tool, input, output, how to run it and why that tool — the guidelines in full in the speaker notes
- [x] The chain names every tool the course has taught, in the step it is used in
- [x] Every step states its lane; the deck rebuilds, tests pass, and the slides were exported and read back


## Resolution

Eight slides in `deck/lesson2/segments/seg5_assignment_close.py`, replacing four: the assignment, the roadmap, the blueprint in three screenfuls, the outcome on the 7 Levels map, the effort and its two venues, the close. The deck is 44 slides; `python -m pytest` is green and `python -m deck.com_check` opens it in real PowerPoint. Every Segment 5 slide was exported through PowerPoint's own renderer and read back.

**The blueprint is authored in the plan, not in the module.** `lesson_2.md` Segment 5 now carries the nine-step table (step, tool, lane, in, out), a paragraph of guidelines and justification per step, and a Mermaid `flowchart LR` of the chain with the lanes as `classDef` colours. The module holds the same nine steps as `_Step` records and the tests read the plan's table and step paragraphs, so the deck and the plan cannot drift on what a step is, which tool runs it, or which lane it belongs to. The plan stays the oracle it was.

**Nine steps, one tool each, and the lane changes are the lesson.** Frame the topic (Gemini · Guided Learning) → write the prompt set (Prompt Coach) → clear the sources (Adobe Acrobat in Teams) → research the gaps (Deep Research) → aggregate into a grounded notebook (NotebookLM) → draft the outline (a Gem + Canvas) → generate the visuals (image generation) → make it teach (Study and Learn) → prototype, cut the excerpt and build (Canva → genspark.ai). Four of those are Daily Driver, three Sensitive Lane, one in neither. The roadmap draws the chain crossing lanes four times, which is the segment's routing argument made in colour rather than in a bullet: a chain does not inherit a lane from its first step.

**Checking is a gate, not a tenth step.** The directive's critical-checking and transparency points are per step, so they sit in a band under the roadmap — check every output before it becomes the next step's input, and log the tool, the date and the purpose. That log is the AI-use declaration on the participant's last slide, and it is one of the three things the effort slide counts as "done".

**Where the fifth field went.** A step's detailed guidelines are a paragraph and do not fit a card, so each blueprint row shows IN / OUT / HOW TO RUN IT / WHY THIS TOOL, HERE, with the slide-length HOW standing in for the full text — which goes, per step, into the slide's speaker notes and into the Teams chat after the session. A test reads the plan's per-step paragraphs and asserts all nine reach the notes, so "detailed guidelines" is not a promise the deck quietly drops.

**What the rework cost elsewhere.** The effort slide no longer lists the tools to chain from — the blueprint names each one in the step it is used in, which is a better answer to "all the tools so far" than a column of names — so it spends the room on the effort, the two venues and what "done" looks like instead. The screenshot cue moved from the assignment slide to the roadmap, because the roadmap and the three blueprint slides are what the room needs to keep.

**Timing.** Segment 5 is now eight slides against its eight minutes — at the density guard's limit, like Segment 4. The notes budget it explicitly: assignment 1 min, roadmap 2 min, the three blueprint slides 30 seconds each as reference slides that are handed out rather than read, outcome 45 s, effort 1 min, close and Q&A the rest. If a run-through says that is too tight, the minutes have to come from another segment — the 60-minute cap is why the hands-on block is absent from this lesson.

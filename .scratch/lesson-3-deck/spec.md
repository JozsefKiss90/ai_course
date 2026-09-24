# Lesson 3 deck — spec

Source plan: `lesson_3.md` (the single oracle for this deck and its tests, as `lesson_2.md` is for Lesson 2). This file records the decisions made when the plan was broken into tickets on 2026-09-24.

## The session

Lesson 3, "Knowledge Capture: NotebookLM and the Personal Vault" (W4), 90 minutes, online via Teams. The first session after Lesson 1 to run the full Session Template with a hands-on block; the former Lesson 4 (Obsidian) is merged in.

| Segment | Duration | Mode |
|---|---|---|
| 1. Recap + assignment debrief | 15 min | Participant demos, facilitated |
| 2. The KM System redrawn + NotebookLM in depth | 20 min | Presentation + live facilitator demo |
| 3. Obsidian: the Personal Vault and its two plugins | 20 min | Live facilitator demo |
| 4. Hands-on block: notebook + vault | 25 min | Hands-on, facilitated |
| 5. Assignment briefing + close | 8 min | Presentation + Q&A |
| Buffer | 2 min | — |

## Fixed constraints from the plan

- The recap map links Lesson 1 and 2 concepts to Lesson 3 topics; never re-teaches.
- Perfect Wiki is out; the Personal Vault is the single source of truth; NotebookLM is the distiller; the arrow into the vault is a person (read, check against the citation, paste with a source line).
- Only Part A rows of `.scratch/video_transcripts/vid_5_source_separation.md` are used, attributed where marked *speaker's claim*; the MIT EEG study is not on a slide. No YouTube URL anywhere in the deck.
- NotebookLM is named "NotebookLM (Gemini Notebook)" once, then "NotebookLM". Free-tier numbers are "at the time of writing (September 2026)" and re-verified the week before delivery.
- Copilot for Obsidian is never called bare "Copilot" (CONTEXT.md Avoid-list); it is not Microsoft Copilot and never the Sensitive Lane.
- Every tool that calls a cloud model (NotebookLM, Copilot for Obsidian, Perplexity) is Daily Driver; Obsidian and Smart Connections are local and call nothing.
- Assignment: notebook (5+ sources, one gap filled), vault (5 concepts, 2 processes, 1 guide, 1 project, `status: checked`), 10+ links and a Graph View screenshot, one link owed to Smart Connections, one judged Vault QA answer, an AI-use log. Outcome: Level 4 reached.
- A slide design distinct from Lessons 1 and 2.

## Decisions made at ticketing time

- Code layout follows Lesson 2: `deck/lesson3/` with its own `template.py`, `build.py` and `segments/`; the shared mechanics in `deck/core.py` are untouched. Output `dist/lesson_3_deck.pptx`; tests in `tests/test_lesson3_deck.py`.
- Colour-coding: Lesson 3 has one lane and one non-lane. The Daily Driver (every cloud call) keeps one accent; **local** (Obsidian, Smart Connections — nothing leaves the machine) gets a second. The Sensitive Lane is not demonstrated in this lesson and gets no colour. Segment 2 is Daily Driver throughout; Segment 3 is local, with the Copilot for Obsidian material colour-coded Daily Driver inside it.
- The plan's "knowledge base" wording (a notebook given to a Gem) is rendered as "the Gem's sources" on the slide, because CONTEXT.md avoids the phrase; the plan is not edited.
- The recap map is one slide of eleven rows, as the plan says; the rows are compressed to a line each and the test checks pairs and forward references against the plan's table.
- Tickets: 01 skeleton and design, 02–06 one segment each, 07 integration pass.
- Bare "wiki" is allowed on a slide only as the name of the retired thing ("the wiki is gone", "the loop the wiki was supposed to close"), as CONTEXT.md's own retired-term entry does; the KM System is never called a wiki. The terminology audit therefore bans "shared wiki" but not the bare word.

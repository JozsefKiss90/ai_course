# Lesson 2 deck — spec

Source prompt: `.scratch/lesson_2_prompt.md` (kept verbatim there). This file records the decisions made when the prompt was broken into tickets on 2026-09-10.

## The session

Lesson 2, "The Two-Lane Tool Landscape" (W2), at most 60 minutes, online via Teams. Opens with a 10–15 minute assignment debrief in which participants demo their Lesson 1 work (prompting techniques, Anchor Project). Follows the Session Template shape, compressed:

| Segment | Duration | Mode |
|---|---|---|
| 1. Recap + assignment debrief | 15 min | Participant demos, facilitated |
| 2. The sensitive-data rule and data-protection principles | 10 min | Presentation |
| 3. Copilot Chat (Basic) in practice | 12 min | Live facilitator demo |
| 4. Gemini in depth (+ NotebookLM preview) | 15 min | Live facilitator demo |
| 5. Assignment briefing + close | 8 min | Presentation + Q&A |

## Fixed constraints from the prompt

- Recap Lesson 1's main concepts and link each to a Lesson 2 topic or use-case; never re-teach — reference.
- The practical use of Copilot and Gemini is strictly separated (separate segments, no cross-demo).
- No YouTube links as references anywhere in the deck.
- The dean's directive 1/2026 (III.26.) on AI use (`.scratch/1_2026_sz_dekani_utasitas.pdf`) is a reference for Segment 2: key points briefly, not full slides.
- Institutional rule: uploaded documents must be anonymised if they contain personal or sensitive information.
- Segment 3 introduces every tool in `.scratch/copilot_free_to_use_tools.md` via a use case.
- Segment 4 covers everything the Gemini free tier offers beyond Copilot, and introduces NotebookLM (the Lesson 3 tool) at use-case level only: YouTube link → textual source; several documents aggregated in one notebook; notebooks imported into Gemini and used as project folders.
- Assignment: chain all tools and capabilities introduced so far into a multi-step workflow orchestration; deliver a blueprint of the tool chaining and workflow steps with guidelines and justification per step; the deliverable is an educational presentation on a hand-picked topic. Outcome: Level 3 reached, foundation for Level 4 laid.
- A different slide design from Lesson 1.

## Decisions made at ticketing time

- The referenced segment-1 template file is empty; Segment 2 is sourced from the dean's directive and CONTEXT.md. If the template is filled later, attach it as a comment on ticket 05.
- Canva (via the Teams app) and genspark.ai are included as taught in Segment 3 (presentation prototyping / actual presentations). CONTEXT.md and the roadmap currently say Canva is dropped; the integration ticket updates them.
- Code layout: lesson-independent PowerPoint mechanics are extracted to a shared core module; Lesson 1 stays in place with its design; Lesson 2 lives in its own sub-package with its own template, build entry point and segment modules. Output `dist/lesson_2_deck.pptx`.
- Lesson 2 gets its own session plan document at the repo root (the equivalent of `lesson_1.md`) before any slide is written; tests use it as the oracle the way Lesson 1's tests use the Timing Overview.
- The roadmap's older Lesson 2 assignment wording ("three real work tasks…") is superseded by the prompt's workflow-orchestration assignment.

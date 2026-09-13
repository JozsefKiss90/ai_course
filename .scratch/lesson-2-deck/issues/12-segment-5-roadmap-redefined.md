# 12 — Segment 5: the roadmap and blueprint redefined

**What to build:** Redefine the assignment roadmap and blueprint so they are intuitive and easy to use. The ticket-10 version was hard to follow: step 3 (Adobe Acrobat in Teams) cannot be used, because the Teams app needs system-administrator approval and there are no institutional PDFs in Teams; the purpose of Copilot Chat (Basic) in that step was unclear, and using any AI tool for sanitisation breaks the sensitive-data principle, since anonymisation has to happen before anything is uploaded and is manual work in Word or Excel; the prompts written in step 2 had no stated place of use; step 4's "coverage gap from step 3" referred to gaps nobody had defined; step 6's "three sources" were unexplained; and the flow of outputs into later steps was never stated. Requirements: clearer, more descriptive and simpler box text; every step's output feeds a named later step; a step that does not involve sensitive data is optional; the "Why this tool, here?" boxes go; clear and concise language.

**Blocked by:** 10 — Segment 5 rework: the assignment roadmap.

**Status:** resolved

- [x] `lesson_2.md` Segment 5 rewritten: eight steps, a Required column, in/out references between steps, a new Mermaid diagram, a paragraph on why Acrobat is out of the chain
- [x] Segment 5 slides render the new route: roadmap with Required / Optional tags and a Prompt Coach helper card, blueprint rows with IN / DO / OUT and no justification boxes
- [x] Only step 2 (manual anonymisation, no AI tool) is required, and only when the material contains sensitive data
- [x] Tests read the new table, assert the step-to-step references, the Required tags, and that Acrobat is gone; the deck rebuilds, `python -m pytest` is green, `python -m deck.com_check` opens it, and every Segment 5 slide was exported and read back

## Resolution

**Eight steps in three phases.** Prepare: 1 frame the topic (Guided Learning), 2 anonymise your own material (no AI tool; Word or Excel, by hand). Gather: 3 research the topic (Deep Research), 4 collect what the presentation must cover (NotebookLM). Produce: 5 draft the outline (a Gem with file upload, long context and Canvas), 6 add the learning material (Study and Learn), 7 make the visuals (image generation), 8 build the presentation (Canva → genspark.ai). Prompt Coach is no longer a step whose output had no stated destination; it is a helper card on the roadmap and a footer on the last blueprint slide: before you run a prompt in steps 3 to 6, improve it there first.

**What replaced the Acrobat step.** Step 2 is manual anonymisation with the Lesson 1 checklist, on a copy, in Word or Excel, and it names no AI tool on purpose: nothing may reach any AI tool before it is done. The plan's roadmap section says why Acrobat is out. Segment 3's Acrobat slide is untouched by this ticket and is a separate decision.

**Outputs feed named steps.** Every OUT card ends in "→ step N" and every IN card from step 4 on says which step its input comes from, so "the coverage gap from step 3" and "the three sources" are gone: step 3's question is "what your material does not cover, or the topic itself", and step 5's inputs are the outcomes from step 1, the coverage list from step 4 and the files from step 2. The old steps 3 and 4 were not merged, because one is manual work in no lane and the other is Daily Driver work, and a step's colour is its lane.

**Required versus optional.** Only step 2 is required, and only when the participant's material contains sensitive data; every other step is tagged Optional on its roadmap card and its blueprint head bar. Step 8 is tagged "Optional tools, required output", because the presentation is the deliverable even if the tools are not mandated. The assignment's blueprint item asks for one line per skipped or changed step, so skipping is a documented decision rather than an omission.

**Boxes.** Each blueprint row now has three fields, IN / DO / OUT, in plain imperative sentences; the WHY THIS TOOL, HERE column is gone from the slides and the plan. The full instruction per step still goes to the speaker notes and the Teams chat.

**Slide count.** Still eight slides for eight minutes: the blueprint fits in three screenfuls as 3 + 3 + 2 rows, the last with the Prompt Coach footer.

# Lesson 1 — Why AI, How LLMs Work, and the Map Ahead
## Detailed Session Plan (Week 1, 90 minutes, online via Teams)

**Character:** purely informational and educational — participants watch and discuss; their first hands-on moment is the 30-minute setup block at the end, and the real practice is the week's assignment.

**Sources for this lesson:**
- Tufts Digital Planet, *AI and the Emerging Geography of American Job Risk* — https://digitalplanet.tufts.edu/ai-and-the-emerging-geography-of-american-job-risk-page/ (opening excerpts)
- The 7 Levels of AI framework — transcript in `7levelsofai.txt` (the course's map)
- aihero.dev *LLM Fundamentals* — https://www.aihero.dev/llm-fundamentals (the fundamentals segment, adapted for a non-technical audience). Key sub-lessons:
  - https://www.aihero.dev/what-are-tokens
  - https://www.aihero.dev/what-is-the-context-window
  - https://www.aihero.dev/messages-system-prompts-and-reasoning-tokens
  - https://www.aihero.dev/what-are-tools
  - https://www.aihero.dev/what-is-an-agent
  - https://www.aihero.dev/what-are-llms-used-for

**Downstream use:** this plan is the input for a separate session that will convert it into a PowerPoint presentation implementation plan. Each segment below is written to map onto a slide sequence.

---

## Timing Overview

| Segment | Duration | Mode |
|---------|----------|------|
| 1. Opening: why this matters | 10 min | Presentation |
| 2. The map: LLM fundamentals + 7 Levels tour | 15 min | Presentation |
| 3. Prompt engineering: ICC, meta-prompting, patterns | 25 min | Live facilitator demo |
| 4. Assignment briefing + close | 10 min | Presentation + Q&A |
| 5. Guided setup block | 30 min | Hands-on, facilitated |

---

## Segment 1 — Opening: Why This Matters (10 min)

Open with the Tufts Digital Planet research on AI and job risk. The point is not fear — it is that *administrative and knowledge work is exactly where AI lands*, and the difference between at-risk and empowered is skill, not job title.

**Excerpts to present:**

- **9.3 million US jobs** are at risk under the median AI-adoption scenario (range 2.7–19.5 million), representing **$757 billion in annual income**.
- The risk is **concentrated in knowledge work**: Information (18% vulnerability), Finance/Insurance (16%), Professional Services (16%) — against a 6% industry average. High-skill, analytical, office-based occupations face the steepest exposure; the jobs historically "safe" from automation are now the most exposed.
- The research's counterintuitive core finding — the **augmentation–displacement pipeline**: occupations with the highest *augmentation potential* (where AI helps most) also show the highest *displacement risk*. In the researchers' framing: *"The more AI helps you do your job, the more expendable you become."*

**The turn (the course's thesis):** the same research implies the way through. Displacement risk attaches to people who let AI do their job *for* them at a shallow level. People who move up the skill curve — who direct AI, verify it, and build systems with it — become more valuable, not less. This course exists to move you up that curve.

**Charts:** two slides show the researchers' own graphics rather than a redrawn version. The sector chart (`.scratch/aijobloss.png`) follows the headline figures. The augmentation-vs-job-loss scatter (`.scratch/aijobloss2.png`) sits on the pipeline slide itself, beside the claim it evidences: claim on the left, chart on the right with a short reading guide, quote underneath — taught in that order.

**Framing for this audience:** research management is administrative, analytical knowledge work — squarely in the exposed zone. That is precisely why learning this well matters for you, now.

---

## Segment 2 — The Map: LLM Fundamentals + the 7 Levels (15 min)

### Part A: How LLMs actually work (≈10 min)

Practitioner-level mental model, no mathematics, adapted from the aihero.dev *LLM Fundamentals* lessons. Its framing sets the tone for the whole course: **AI is "powerful — but weird."** Once you understand the quirks and constraints, you can use it for what it is: a strange but powerful tool.

- **The four-layer AI engineering stack — the segment's map**: everything people call "AI engineering" is one of four layers, each wrapping the one below — *prompt* (the single message: instruction–context–constraints), *context* (what is in the window: sources, memory, and what you leave out), *harness* (the standing setup around the model: an agent's instructions, its tools, its output format), *loop* (the model running itself until a job is done). Coverage is printed on the slide: prompt = today + Lesson 2; context = Lessons 3–4; harness = Lesson 5's Agent Builder; loop = outlook only. Closes on the contrast between **vibe coding** (describe it, accept the output, judge the result) and **agentic engineering** (engineer all four layers, check every lap) — land the distinction, do not debate the terms.
- **Tokens — the model doesn't see words** (*what-are-tokens*): text is chopped into numbered fragments; common words are one token, rare words several (the lesson's example: "Frabjous Day" — 15 characters, 7 tokens). Tokens are what usage limits and context limits actually count. Live 1-minute demo: the tiktokenizer playground (tiktokenizer.vercel.app) — paste a sentence, watch it split.
- **The context window — a finite working memory** (*what-is-the-context-window*): everything you paste plus everything it answers must fit inside a hard limit. Worse, attention sags: models weigh the *beginning and end* of a long conversation and neglect the middle — the "lost in the middle" problem. Two practical rules: long chats degrade, so start fresh per task; and **more context is not better context** — fewer, relevant tokens beat a document dump. (This is why Lesson 3's source-grounded tools exist.)
- **System prompts — standing instructions** (*messages-system-prompts-and-reasoning-tokens*): every conversation is a stack of messages, and an invisible instruction at the top shapes everything the model does — when user and system instructions conflict, the system usually wins. Foreshadow: in Lesson 5 *you* write the system prompt; that's all a custom agent's "instructions" are. Reasoning models additionally "think out loud" in hidden tokens before answering — that's the pause before good answers.
- **Hallucination, sycophancy, and the cutoff** (*what-are-llms-used-for*): the model produces plausible text, not verified fact — confident, fluent, *wrong* answers, especially numbers, citations, names. It also tends to agree with you rather than push back, and its knowledge stops at a training-cutoff date (anything newer needs a searching tool — Perplexity, Lesson 3). Rule from day one: **verify anything you would sign your name to.**
- **Tools and agents — where this is heading** (*what-are-tools*, *what-is-an-agent*, 1 minute, foreshadowing only): an LLM given "tools" can act, not just write — and an *agent* is an LLM in a loop, choosing its own next step until the job is done. That's Level 5–6 territory; participants build their first agent in Lesson 5.

**Digestible principles from LLM Fundamentals** (say these out loud; they set the course's tone):
1. *Powerful but weird* — the quirks are not bugs to fear but constraints to work within.
2. *If it can be done deterministically, it should be* — use AI for messy, judgment-shaped work; use a template, a spreadsheet, or a checklist for work that must come out the same every time.
3. *Fewer, better tokens win* — curate what you give the model; relevance beats volume.

### Part B: The 7 Levels of AI — the course's map (≈5 min)

Present the framework from `7levelsofai.txt` as the arc of the whole course, at pace: one sentence per level from the table below — no dwelling; the levels get lived out in the coming weeks, not explained today.

| Level | Name | In research management terms | Course coverage |
|-------|------|------------------------------|-----------------|
| 1 | Question Asker | AI as a fancier search engine: one-off questions about calls, rules | You are (probably) here |
| 2 | Prompt Crafter | Structured prompts (instruction–context–constraints), examples, iteration | Today + Lesson 2 |
| 3 | Power User | Persistent context: dedicated workspaces that already know your domain | Lessons 2–3 |
| 4 | Tool Orchestrator | The right specialized tool per step: NotebookLM for documents, Perplexity for cited research | Lessons 3–4 |
| 5 | Builder | Building your own tools without code: custom agents, automated pipelines | Lesson 5 (Markdown Generator) |
| 6 | Systems Builder | Systems that run without you; agentic workflows | Outlook only (final session) |
| 7 | AI-Run Operation | Aspirational: an agent workforce running an operation | Mentioned for perspective |

**Vibe coding — mentioned in passing only (one sentence, at the Level 4–5 rows):** "vibe coding" is the practice of describing software in plain language and letting AI write it — it exists, it is reshaping who can build tools, but it is not part of this course. This is not an engineering course; the closest participants come to building is Lesson 5's Agent Builder, which needs no code at all.

**Close of segment:** this course takes you from Level 1 to Level 4–5. The destination artifact is your personal knowledge management system (show the wiki → agent → Obsidian diagram from the roadmap, 1 minute, as a teaser — "by Week 8, you will have built this").

---

## Segment 3 — Prompt Engineering: ICC, Meta-Prompting, and Patterns (25 min)

Live facilitator demo in Gemini (participants watch; they reproduce it in the setup block and assignment). Rough split: Demo 1 ≈8 min, Demo 2 ≈17 min.

**Demo 1 — the same question, three ways** (escalate quality live):
1. *Google-style:* "Horizon Europe budget"
2. *Better:* "Explain the budget structure of Horizon Europe collaborative projects"
3. *ICC:* full structured prompt —

```
[Instruction] Explain the eligible cost categories and overhead
calculation for a Horizon Europe collaborative project, and list
the 5 most common budgeting mistakes.

[Context] I am a research management administrator at a European
university. We are preparing a budget for a Cluster 4 project
with 8 partners, total budget EUR 3-4M. My audience is our PI,
who has never coordinated an EU project.

[Constraints] Maximum 600 words. Use a table for cost categories.
Plain language, no unexplained acronyms.
```

Show side by side how output quality scales with input quality.

**Demo 2 — shortcuts, meta-prompting, and prompt patterns** (these alone jump a participant from Level 1 to Level 2):

*The two shortcuts from the 7 Levels transcript:*
1. **Ask-me-first:** append *"Before answering, ask me the questions you need to give the best possible answer."* Show the model interviewing the facilitator.
2. **Reverse prompt:** after a good multi-turn result — *"Write the single prompt that would have gotten us to this result on the first try."* Save that prompt for reuse.

*Meta-prompting — let the AI write the prompt* (show live, ~2 min): describe the task and ask for the prompt instead of the answer — *"I need an AI assistant to help me draft the impact section of an EU project's periodic report. Write the optimal prompt I should use, including all the context and constraints that would produce the best result."* Then run the generated prompt (after filling in the specifics) and compare with a naive attempt. Message: the model knows what a good prompt looks like better than you do — use it as your prompt engineer.

*Prompt patterns — four reusable shapes* (present as a slide, demo one live; each shown with a research-management example):
1. **Persona:** *"Act as an experienced EU grants advisor reviewing a first-time applicant's budget…"* — the role sets vocabulary, priorities, and depth.
2. **Example-driven (few-shot):** paste one example of an output you liked — *"Here is a partner-search announcement in our house style. Write one for the following project in the same style: …"* — a good example beats a paragraph of description.
3. **Step-by-step:** *"Before giving the final assessment, first list the eligibility criteria, then check each against the project facts, then conclude."* — forcing intermediate steps improves reasoning on rule-checking tasks.
4. **Critique-then-improve:** *"Here is my draft. First list its three biggest weaknesses against the evaluation criteria, then rewrite it fixing only those."* — separates diagnosis from repair and keeps the model from rewriting what already works.

Close the segment by connecting shortcuts and patterns to the prompt library: every saved prompt is one of these shapes filled in — the library lives in your knowledge system from Lesson 4 on.

**Two rules stated while demoing:** never paste sensitive institutional data into Gemini (the full rule comes in Lesson 2 — for now: nothing you couldn't publish); verify anything factual before using it.

---

## Segment 4 — Assignment Briefing + Close (10 min)

**Assignment for the week** (due at Lesson 2's debrief; expect ~1–2 hours across the week):

1. **Pick your Anchor Project** — one real research project from your environment (anonymize it) or a fictional one. You will build your entire knowledge system around it during the course. Write 5 sentences describing it.
2. **Three ICC prompts in Gemini** about your Anchor Project's domain (e.g., its funding scheme's rules, its reporting duties, its stakeholder landscape) — at least one using a prompt pattern from the session (persona, example-driven, step-by-step, or critique-then-improve). For each, save: the prompt, the answer, one sentence on what you'd improve.
3. **One ask-me-first prompt:** let Gemini interview you about a task from your actual work, then complete the task with it.
4. **One meta-prompt:** describe a recurring task from your work and ask Gemini to write the optimal prompt for it; run the result and save the prompt.
5. Bring all of this to Lesson 2 — 2–3 volunteers will present at the debrief.

**Close (2 min):** next week — the two-lane rule: which AI is allowed to see sensitive institutional data (Copilot), which handles everything else (Gemini), and why.

---

## Segment 5 — Guided Setup Block (30 min, hands-on)

The only hands-on part of Lesson 1. Everyone leaves with working tools; the facilitator (plus any quick finishers) troubleshoots.

**Checklist per participant:**
1. **Google account** signed in; **Gemini** (gemini.google.com) opens and answers a test prompt
2. **Copilot Chat** opens in Teams / microsoft365.com with the institutional account (needed from Lesson 2)
3. **Perplexity** free account created (needed in Lesson 3; cheap to do now)
4. First experimental prompt sent in each tool

**Facilitation notes:**
- Screen-share a checklist slide; participants mark themselves done in the meeting chat ("✅ 1–4") so stragglers are visible
- Typical failure points: personal vs. institutional Microsoft account mixed up; Google account blocked by institutional policy in the default browser (fix: separate browser profile); Gemini region/consent prompts
- Anyone not finished by end of session: Practice Week 1's drop-in (W3) is the catch-up venue — but flag them now and offer a 10-minute slot during the week
- **Not installed today:** Obsidian (Lesson 4) and Perfect Wiki (Lesson 3) — deliberately deferred so tools arrive when they're needed

---

## Materials to Prepare (Facilitator)

- Slide deck per the segment structure above (the PPT implementation plan is produced in a separate planning session from this document)
- The three-way ICC demo prompts pre-typed and tested in Gemini the day before
- Setup checklist slide + chat template
- Anonymization one-pager: what makes a project description safe to use (no names, no unpublished amounts, no personnel data)

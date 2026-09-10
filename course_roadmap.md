# AI for Research Management
## 8-Week Online Course Roadmap

**Participants:** ~10 (max 15) research management administrators — no fixed teams; plenary teaching with individual or pair work
**Delivery:** Live online via Microsoft Teams, one 1.5-hour session per week, during office hours
**Central deliverable:** each participant leaves with a working, personal two-way knowledge management system (see below)
**Framework:** the 7 Levels of AI (source: `7levelsofai.txt`); the course takes participants from Level 1 to Level 4–5

---

## The Two-Lane Tool Rule

The course runs on a strict data-governance rule that participants learn in Week 2 and apply for the rest of their careers:

| Lane | Tool | Use for |
|------|------|---------|
| **Sensitive Lane** | Microsoft 365 Copilot Chat (Basic) | The *only* tool authorized for sensitive or IP-sensitive institutional data: internal administration, unsubmitted grant proposals, personnel information, strategic financial planning |
| **Daily Driver** | Google Gemini (free tier) | Everything else: drafting, prompting, long-document analysis, general research management work |

Copilot Chat (Basic) cannot ground in SharePoint/OneDrive and underperforms free-tier alternatives on general tasks — so it is reserved for the one thing only it is authorized to do: processing sensitive institutional data. Its second unique asset, the **Agent Store and Agent Builder**, carries the final third of the course.

## Core Tool Roster

Every tool taught contributes to the knowledge management architecture. Nothing else is taught.

| Tool | Role | Tier |
|------|------|------|
| **Microsoft 365 Copilot Chat (Basic)** | Sensitive Lane; Agent Store; Agent Builder (custom agents) | Institutional licence |
| **Google Gemini** | Daily Driver for all non-sensitive work | Free |
| **NotebookLM** | Distilling long documents into wiki-ready knowledge | Free |
| **Perplexity AI** | Cited research discovery feeding wiki concepts | Free |
| **Perfect Wiki** | Per-participant Wiki Sandbox — the single source of truth | Free tier (per-user; licence does not allow sharing) |
| **Obsidian** | Personal Vault — visual thinking space (Graph View, Canvas) | Free |

Taught but outside the roster, in one narrow role each: **Canva** (through its Teams app) to prototype a presentation's structure, and **genspark.ai** to build the deck itself — both introduced in Lesson 2 for that session's presentation deliverable. Neither feeds the KM System, and both sit outside the institutional tenant, so only anonymised, non-sensitive content goes into them.

Not in the course: ChatGPT (mentioned once as an alternative to Gemini), Horizon Dashboard (moved to the Optional Use-Case Phase).

---

## The Knowledge Management System

Each participant builds this architecture for themselves, around one **Anchor Project** — a real (anonymized) or fictional research project from their own environment, chosen in Week 1:

```
┌─────────────────────────────────────────────┐
│ PERFECT WIKI  (Wiki Sandbox)                │
│ Single source of truth. Entity types:       │
│ concepts · processes · guides · projects    │
└──────────────────┬──────────────────────────┘
                   │  Markdown Generator
                   │  (custom Copilot agent, built in Lesson 5)
                   ▼
┌─────────────────────────────────────────────┐
│ OBSIDIAN  (Personal Vault)                  │
│ Graph View · Canvas · local notes ·         │
│ visual navigation                           │
└──────────────────┬──────────────────────────┘
                   │  Manual export
                   ▼
        back into PERFECT WIKI
```

The round-trip is **human-mediated by design**: pulling wiki content into the vault and exporting vault content back are deliberate acts with a person deciding what enters the source of truth. No automated sync.

Because the "Workflows (Frontier)" agent is disabled, the custom-agent capability (Agent Builder) is used to achieve similar results — the Markdown Generator agent is the course's flagship example.

---

## Course Skeleton

Rhythm: teach, teach, practice, teach, teach, practice, teach, final.

| Week | Session | Content |
|------|---------|---------|
| **W1** | Lesson 1 | LLM fundamentals, 7 Levels framework, prompt engineering, guided tool setup — **detailed plan in [`lesson_1.md`](lesson_1.md)** |
| **W2** | Lesson 2 | The two-lane tool landscape: Copilot Chat and the sensitive-data rule; Gemini in depth, NotebookLM previewed — **detailed plan in [`lesson_2.md`](lesson_2.md)** |
| **W3** | Practice Week 1 | Optional facilitated drop-in; assignment work |
| **W4** | Lesson 3 | Knowledge capture: NotebookLM + Perplexity as knowledge distillers; Wiki Sandbox setup with the four entity types |
| **W5** | Lesson 4 | Obsidian: vault, linking, Graph View, Canvas; manual Markdown import from the wiki (feeling the pain the agent will remove) |
| **W6** | Practice Week 2 | Optional facilitated drop-in; assignment work |
| **W7** | Lesson 5 | Custom agents: Agent Store tour (Perfect Wiki app, Prompt Coach); Agent Builder — build the Markdown Generator; close the round-trip |
| **W8** | Final session | Participants demo their working KM System end to end; 7 Levels recap; Optional Use-Case Phase menu |

### Standard Session Template (Lessons 2–5)

Every teaching session after the first follows the same 90-minute shape:

1. **Recap & assignment debrief** (15 min) — 2–3 participants show their assignment work; common problems surfaced
2. **New concept + live demo** (25 min) — the week's tool/technique on a research management example
3. **Hands-on block** (30 min) — participants apply it to their own Anchor Project; facilitator troubleshoots
4. **Assignment briefing + Q&A** (15 min) — the week's assignment, always building the next piece of the KM System
5. **Buffer** (5 min)

Lesson 1 (informational, with a 30-minute setup finale) and the final session (demos) are the only deviations.

### Practice Weeks

The weekly slot stays in calendars as an **optional facilitated drop-in**: no agenda, no new content — participants work on their assignment with the facilitator present for troubleshooting (installation problems, agent quirks, wiki/vault confusion). The blanks exist because participants have no time outside office hours to practise.

---

## Session Outlines (Lessons 2–5 and Final)

Lessons 1 and 2 are planned in detail (`lesson_1.md`, `lesson_2.md`). These outlines fix each session's goal, topics, and assignment; detailed plans are written lesson by lesson as the course runs, and a detailed plan supersedes its outline here.

### Lesson 2 — The Two-Lane Tool Landscape (W2)
**Goal:** participants route every task to the correct lane and get consistently good results from both.
- Recap of Lesson 1 and the assignment debrief: 2–3 volunteers demo their Anchor Project and prompting work
- The sensitive-data rule: what *must* go to Copilot Chat, what must never; the data-protection principles behind it, the dean's directive 1/2026 (III.26.) as reference, and the anonymise-before-upload rule
- Copilot Chat (Basic) in practice: strengths, limits (no SharePoint/OneDrive grounding), enterprise guardrails, and one scenario per tool in the institutional licence — Adobe Acrobat, Prompt Coach, Study and Learn, Canva, genspark.ai
- Gemini in depth: file and image upload, long context, Gems, Deep Research, Canvas and the free tier's boundaries; NotebookLM previewed at scenario level for Lesson 3
- **Assignment:** chain every tool and capability introduced so far into one multi-step workflow orchestration — a blueprint giving the tool, input, output, guidelines and justification per step, with the lane stated per step, delivered as an educational presentation on a hand-picked topic. Outcome: Level 3 reached, the foundation for Level 4 laid.

### Lesson 3 — Knowledge Capture (W4)
**Goal:** turn raw documents and research into wiki-ready knowledge; stand up the Wiki Sandbox.
- NotebookLM: source-grounded analysis of Anchor Project documents; briefing notes as wiki fodder
- Perplexity: cited discovery; verifying claims before they enter the source of truth
- Perfect Wiki setup in Teams: the four entity types — concepts, processes, guides, projects
- **Assignment:** populate the Wiki Sandbox from the Anchor Project — at least 5 concepts, 2 processes, 1 guide, 1 project entry

### Lesson 4 — Obsidian: the Personal Vault (W5)
**Goal:** a working local vault, visually navigable, fed from the wiki.
- Vault setup; notes, `[[links]]`, tags; Graph View and Canvas
- Manual import: converting wiki content to Markdown by hand — deliberately tedious, motivating Lesson 5
- Linking discipline: the graph only pays off if entities reference each other
- **Assignment:** build the vault from your wiki content; link everything; bring a Graph View screenshot to Practice Week 2 / Lesson 5

### Lesson 5 — Custom Agents & Closing the Loop (W7)
**Goal:** the Markdown Generator exists and the round-trip works.
- Agent Store tour: Perfect Wiki app, Prompt Coach, Adobe Acrobat, Asana — what's worth installing
- Agent Builder: instructions-as-prompting (ICC applied to agent design)
- Build the **Markdown Generator**: an agent that converts Wiki Sandbox content into vault-ready Markdown with correct `[[links]]`
- Export back: getting vault changes into the wiki; the human gate on writes
- **Assignment:** run the full round-trip on your Anchor Project content; prepare a 5-minute demo for the final session

### Final Session — The Working KM System (W8)
- Participant demos: each shows their round-trip end to end (5 min each); group troubleshooting
- 7 Levels recap: where each participant started, where they are now, what Levels 5–7 look like from here
- **Optional Use-Case Phase menu** presented (see below)
- Course evaluation

---

## Optional Use-Case Phase

Offered *after* the 8 weeks, only to participants whose KM System exists. Format (follow-up sessions or self-study paths) to be designed later. Menu:

- **Detailed budget creation** — cost categories, overhead, partner allocations
- **Proposal writing** — call analysis to section drafting
- **Horizon Dashboard** — official EU funding statistics, success rates, CSV export for AI analysis
- Further use cases as demand emerges from participants' Anchor Projects

---

## Pre-Course Setup (Distributed 1 Week Before W1)

Participants:
1. Verify Microsoft 365 sign-in and that Copilot Chat opens in Teams
2. Create free accounts: Google (Gemini + NotebookLM), Perplexity
3. Think of a candidate Anchor Project (a real, anonymizable research project from your work) — chosen definitively in Lesson 1
4. Nothing else — Obsidian and Perfect Wiki installation happen in-course (Lessons 4 and 3)

Facilitator:
1. Teams meeting series for all 8 weeks (including Practice Week drop-ins)
2. Verify Agent Builder and Agent Store availability under the institutional licence
3. Prepare Lesson 1 materials per [`lesson_1.md`](lesson_1.md)
4. Sample documents for participants who cannot anonymize their own

---

## Risks

| Risk | Mitigation |
|------|-----------|
| Free-tier usage limits during live hands-on blocks | Stagger participants; facilitator demos on screen as fallback; hands-on continues as assignment |
| Sensitive data pasted into free-tier tools | The two-lane rule is taught in W2 and re-checked at every debrief; anonymization drilled in Lesson 1 assignment |
| Perfect Wiki free-tier limits change | Facilitator re-verifies limits before W4; fallback: plain Markdown files in Teams as interim source of truth |
| Agent Builder unavailable / degraded | Fallback for Lesson 5: a saved Copilot prompt template performing the same conversion, run manually |
| Participants skip assignments (office-hours time pressure) | Debrief-first session template creates accountability; Practice Week drop-ins lower the barrier |
| Tool UI changes | Facilitator check the week before each lesson |

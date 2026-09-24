# AI for Research Management
## 8-Week Online Course Roadmap

**Participants:** ~10 (max 15) research management administrators — no fixed teams; plenary teaching with individual or pair work
**Delivery:** Live online via Microsoft Teams, one 1.5-hour session per week, during office hours
**Central deliverable:** each participant leaves with a working, personal knowledge management system (see below)
**Framework:** the 7 Levels of AI (source: `7levelsofai.txt`); the course takes participants from Level 1 to Level 4–5

> **Redesign in progress (September 2026).** Perfect Wiki has been removed from the course: it is a paid service and therefore out of scope. Lesson 3 has been redesigned around NotebookLM and Obsidian and absorbs the former Lesson 4 (`lesson_3.md`). The sessions after Lesson 3 (W5 onwards) are being redesigned next; their outlines below are placeholders and any remaining reference to the wiki in them is obsolete. Delivered plans (`lesson_1.md`, `lesson_2.md`) keep their historical forward references to "the wiki" and "Lesson 4"; read them as "the Personal Vault" and "Lesson 3".

---

## The Two-Lane Tool Rule

The course runs on a strict data-governance rule that participants learn in Week 2 and apply for the rest of their careers:

| Lane | Tool | Use for |
|------|------|---------|
| **Sensitive Lane** | Microsoft 365 Copilot Chat (Basic) | The *only* tool authorized for sensitive or IP-sensitive institutional data: internal administration, unsubmitted grant proposals, personnel information, strategic financial planning |
| **Daily Driver** | Google Gemini (free tier) and the other free-tier cloud tools | Everything else: drafting, prompting, long-document analysis, general research management work |

Copilot Chat (Basic) cannot ground in SharePoint/OneDrive and underperforms free-tier alternatives on general tasks — so it is reserved for the one thing only it is authorized to do: processing sensitive institutional data. Its second unique asset, the **Agent Store and Agent Builder**, carries the final third of the course.

From Lesson 3 on, a third category exists beside the two lanes: **local-only** tools (Obsidian itself, and the Smart Connections plugin's on-device embeddings) that call no cloud model at all. They hold only Anchor Project content, which is anonymised or fictional by construction, so the lane question does not arise for them.

## Core Tool Roster

Every tool taught contributes to the knowledge management architecture. Nothing else is taught.

| Tool | Role | Tier |
|------|------|------|
| **Microsoft 365 Copilot Chat (Basic)** | Sensitive Lane; Agent Store; Agent Builder (custom agents) | Institutional licence |
| **Google Gemini** | Daily Driver for all non-sensitive work | Free |
| **NotebookLM** (renamed Gemini Notebook, July 2026) | The distiller: source-grounded, cited answers that become vault notes | Free |
| **Obsidian** | Personal Vault — the single source of truth; Graph View, Canvas, local Markdown | Free (personal use) |
| **Smart Connections** (Obsidian plugin) | Related-note discovery inside the vault, fully local | Free core |
| **Copilot for Obsidian** (Obsidian plugin, unrelated to Microsoft Copilot) | Asking the vault: Vault QA with cited notes, on the participant's own free Gemini API key | Free plugin + free API key |

Mentioned in passing only: **Perplexity** (cited web search on the free tier) is named once in Lesson 3 for what it offers research management and knowledge management: a fast, cited first answer on current questions, and claims that can enter the vault with their source line. It is not on the KM System's path and its paid Spaces are not used.

Taught but outside the roster, in one narrow role each: **Canva** (through its Teams app) to prototype a presentation's structure, and **genspark.ai** to build the deck itself — both introduced in Lesson 2 for that session's presentation deliverable. Neither feeds the KM System, and both sit outside the institutional tenant, so only anonymised, non-sensitive content goes into them.

Not in the course: **Perfect Wiki** (paid service, removed), ChatGPT (mentioned once as an alternative to Gemini), Horizon Dashboard (moved to the Optional Use-Case Phase).

---

## The Knowledge Management System

Each participant builds this architecture for themselves, around one **Anchor Project** — a real (anonymized) or fictional research project from their own environment, chosen in Week 1:

```
   SOURCES (anonymised or fictional Anchor Project material)
   call text · guidelines · FAQ · own notes · public pages · cited briefings
                          │
                          ▼
┌─────────────────────────────────────────────┐
│ NOTEBOOKLM  (the distiller)                 │
│ Source-grounded answers with citations;     │
│ reports, mind maps, audio overviews         │
└──────────────────┬──────────────────────────┘
                   │  human-mediated: read, check, paste
                   ▼
┌─────────────────────────────────────────────┐
│ OBSIDIAN  (Personal Vault — source of truth)│
│ Four note types: concepts · processes ·     │
│ guides · projects · [[links]] · Graph View  │
│  Smart Connections: related notes (local)   │
│  Copilot for Obsidian: ask the vault, cited │
└─────────────────────────────────────────────┘
```

The arrow into the vault is **human-mediated by design**: notebook output is read, checked against its citations and then pasted, with a source line, by a person deciding what enters the source of truth. No automated sync. The four entity types (concepts, processes, guides, projects) are the vault's four folders.

How the Copilot Agent Builder and the custom-agent capability (the "Markdown Generator" idea) fit this vault-centred architecture is decided in the redesign of the later lessons.

---

## Course Skeleton

Rhythm: teach, teach, practice, teach, teach, practice, teach, final.

| Week | Session | Content |
|------|---------|---------|
| **W1** | Lesson 1 | LLM fundamentals, 7 Levels framework, prompt engineering, guided tool setup — **detailed plan in [`lesson_1.md`](lesson_1.md)** |
| **W2** | Lesson 2 | The two-lane tool landscape: Copilot Chat and the sensitive-data rule; Gemini in depth, NotebookLM previewed — **detailed plan in [`lesson_2.md`](lesson_2.md)** |
| **W3** | Practice Week 1 | Optional facilitated drop-in; assignment work |
| **W4** | Lesson 3 | Knowledge capture: NotebookLM in depth, then Obsidian as the Personal Vault with Smart Connections and Copilot for Obsidian; Perplexity in passing; the former Lesson 4 merged in — **detailed plan in [`lesson_3.md`](lesson_3.md)** |
| **W5** | *To be redesigned* | Formerly Lesson 4 (Obsidian), now part of Lesson 3; content of this slot decided in the redesign of the later lessons |
| **W6** | Practice Week 2 | Optional facilitated drop-in; assignment work |
| **W7** | Lesson 5 *(redesign pending)* | Custom agents: Agent Store tour, Agent Builder; how a custom agent serves the vault-centred KM System |
| **W8** | Final session *(redesign pending)* | Participants demo their working KM System end to end; 7 Levels recap; Optional Use-Case Phase menu |

### Standard Session Template (Lessons 2–5)

Every teaching session after the first follows the same 90-minute shape:

1. **Recap & assignment debrief** (15 min) — 2–3 participants show their assignment work; common problems surfaced
2. **New concept + live demo** (25 min) — the week's tool/technique on a research management example
3. **Hands-on block** (30 min) — participants apply it to their own Anchor Project; facilitator troubleshoots
4. **Assignment briefing + Q&A** (15 min) — the week's assignment, always building the next piece of the KM System
5. **Buffer** (5 min)

Lesson 1 (informational, with a 30-minute setup finale) and the final session (demos) are the only deviations. Lesson 2 ran at a 60-minute cap without a hands-on block; Lesson 3 splits the concept slot across two tools and shortens the hands-on block to 25 minutes (see `lesson_3.md`).

### Practice Weeks

The weekly slot stays in calendars as an **optional facilitated drop-in**: no agenda, no new content — participants work on their assignment with the facilitator present for troubleshooting (installation problems, plugin quirks, notebook/vault confusion). The blanks exist because participants have no time outside office hours to practise.

---

## Session Outlines (Lessons 2–5 and Final)

Lessons 1, 2 and 3 are planned in detail (`lesson_1.md`, `lesson_2.md`, `lesson_3.md`). These outlines fix each session's goal, topics, and assignment; a detailed plan supersedes its outline here. Outlines marked *redesign pending* will be rewritten.

### Lesson 2 — The Two-Lane Tool Landscape (W2)
**Goal:** participants route every task to the correct lane and get consistently good results from both.
- Recap of Lesson 1 and the assignment debrief: 2–3 volunteers demo their Anchor Project and prompting work
- The sensitive-data rule: what *must* go to Copilot Chat, what must never; the data-protection principles behind it, the dean's directive 1/2026 (III.26.) as reference, and the anonymise-before-upload rule
- Copilot Chat (Basic) in practice: strengths, limits (no SharePoint/OneDrive grounding), enterprise guardrails, and one scenario per tool in the institutional licence — Adobe Acrobat, Prompt Coach, Study and Learn, Canva, genspark.ai
- Gemini in depth: file and image upload, long context, Gems, Deep Research, Canvas and the free tier's boundaries; NotebookLM previewed at scenario level for Lesson 3
- **Assignment:** chain every tool and capability introduced so far into one multi-step workflow orchestration — a blueprint giving the tool, input, output, guidelines and justification per step, with the lane stated per step, delivered as an educational presentation on a hand-picked topic. Outcome: Level 3 reached, the foundation for Level 4 laid.

### Lesson 3 — Knowledge Capture: NotebookLM and the Personal Vault (W4)
**Goal:** the first two floors of the KM System stand: a source-grounded notebook that distils Anchor Project material into cited answers, and a linked Obsidian vault that keeps them as the single source of truth, with its own AI for finding and asking.
- Recap and the Lesson 2 assignment debrief: 2–3 volunteers show blueprint, presentation and AI-use log
- The KM System redrawn without the wiki: notebook → vault; the four entity types become the vault's four folders; the human gate on every paste; the "four floors" map (grounding, frontier model, specialist, tools) with Obsidian on the fourth floor
- NotebookLM in depth: source grounding and citations; source types; free-tier limits; Studio outputs (reports, mind map, Audio and Video Overviews, flashcards, Deep Research inside the notebook); when a notebook beats a Gemini chat; the question shapes that turn a notebook into wiki-ready notes per entity type
- Perplexity in passing: cited web search for what the notebook does not yet hold; the benefit for research management (fast, cited first answers on current questions) and for knowledge management (claims enter the vault with their source line); find → ground → keep
- Obsidian: local Markdown vault, four folders, note template with `source` and `status`, `[[links]]`, tags, backlinks, Graph View, Canvas; linking discipline
- Two community plugins: **Smart Connections** (related notes from local embeddings, no API key, offline) and **Copilot for Obsidian** (Chat and Vault QA with cited notes, on a free Gemini API key from Google AI Studio; Daily Driver; not Microsoft Copilot)
- Hands-on block: notebook with three sources, vault with three linked notes, both plugins installed
- **Assignment:** notebook with at least 5 sources and one gap filled by Deep Research or Perplexity; vault with at least 5 concepts, 2 processes, 1 guide, 1 project note, each from a cited notebook answer with a source line; at least 10 links and a Graph View screenshot; one link owed to Smart Connections; one cited Vault QA answer judged against its notes; AI-use log. Outcome: Level 4 reached.

### W5 — *To be redesigned*
The former Lesson 4 (Obsidian: vault, linking, Graph View, Canvas, manual import from the wiki) is now inside Lesson 3. What this slot holds is decided with the redesign of Lessons 5 and the final session.

### Lesson 5 — Custom Agents *(redesign pending)* (W7)
**Goal (provisional):** a custom Copilot agent exists and serves the vault-centred KM System.
- Agent Store tour: Prompt Coach, Adobe Acrobat, Asana — what's worth installing
- Agent Builder: instructions-as-prompting (ICC applied to agent design)
- The agent's job against a vault that is already the source of truth is redefined in the redesign; the earlier "Markdown Generator" (wiki → vault conversion) no longer has a wiki to convert from
- **Assignment (provisional):** prepare a 5-minute demo for the final session

### Final Session — The Working KM System *(redesign pending)* (W8)
- Participant demos: each shows their KM System end to end (5 min each); group troubleshooting
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
4. Nothing else — Obsidian, its two plugins and the Gemini API key are set up in-course (Lesson 3)

Facilitator:
1. Teams meeting series for all 8 weeks (including Practice Week drop-ins)
2. Verify Agent Builder and Agent Store availability under the institutional licence
3. Prepare Lesson 1 materials per [`lesson_1.md`](lesson_1.md)
4. Sample documents for participants who cannot anonymize their own
5. Before W4: confirm Obsidian can be installed on institutionally managed machines (portable build as fallback)

---

## Risks

| Risk | Mitigation |
|------|-----------|
| Free-tier usage limits during live hands-on blocks | Stagger participants; facilitator demos on screen as fallback; hands-on continues as assignment |
| Sensitive data pasted into free-tier tools | The two-lane rule is taught in W2 and re-checked at every debrief; anonymization drilled in Lesson 1 assignment; the vault holds anonymised or fictional content only, so its cloud plugin inherits the rule |
| NotebookLM free-tier limits or Studio outputs change | Facilitator re-verifies limits and outputs the week before W4; any missing output is shown as a slide and marked |
| Obsidian cannot be installed on managed machines | Confirmed the week before W4; portable build or a personal device as fallback |
| Plugin settings or model lists change (Smart Connections, Copilot for Obsidian) | Fresh install on a clean vault the day before W4; the Google AI Studio key flow walked through once |
| Agent Builder unavailable / degraded | Fallback for Lesson 5: a saved Copilot prompt template performing the same job, run manually |
| Participants skip assignments (office-hours time pressure) | Debrief-first session template creates accountability; Practice Week drop-ins lower the barrier |
| Tool UI changes | Facilitator check the week before each lesson |

# AI Course for Research Management (ELTE)

The ubiquitous language for the redesigned online AI course for research management administrators. The course teaches AI-supported research management and culminates in a two-way knowledge management system.

## Language

### Course structure

**Teaching Session**:
A live 1.5-hour online lesson that introduces new material. One session per week.
_Avoid_: Module, day, class

**Practice Week**:
A week with no new material: the session slot runs as an optional, facilitated drop-in where participants work on their assignment with the facilitator available for troubleshooting. Needed because the course runs during office hours.
_Avoid_: Blank lesson, blank week, homework week, self-study week

**Course Skeleton**:
The 8-week rhythm of teaching and practice: teach, teach, practice, teach, teach, practice, teach, final. Six Teaching Sessions, two Practice Weeks.

**Session Template**:
The fixed five-part shape of Teaching Sessions 2–5: assignment debrief, concept + demo, hands-on block, assignment briefing, buffer. Lesson 1 (informational + setup finale) and the final session (demos) are the only deviations.

**Cohort**:
The participants of one course run — around 10, at most 15 people, working individually or in pairs. There are no fixed teams.
_Avoid_: Teams, breakout teams, domain teams

### Knowledge management system

**KM System**:
The two-way knowledge management architecture each participant builds for themselves: Wiki Sandbox → Markdown Generator → Personal Vault, and manual export back to the wiki. The course's central deliverable, built around the participant's Anchor Project.
_Avoid_: Knowledge base, shared wiki

**Anchor Project**:
The one real (anonymized) or fictional research project each participant picks at the start and builds their Wiki Sandbox around. All four entity types are populated from its lifecycle.
_Avoid_: Use case, case study, team project

**Wiki Sandbox**:
A participant's own Perfect Wiki instance, acting as their single source of truth. Holds four entity types: concepts, processes, guides, projects. Per-participant because the Perfect Wiki licence does not allow sharing.
_Avoid_: Shared wiki, team wiki

**Personal Vault**:
A participant's local Obsidian vault — their visual thinking space (Graph View, Canvas, local notes) fed from their Wiki Sandbox.

**Markdown Generator**:
The custom Copilot agent that converts Wiki Sandbox content into Markdown notes for the Personal Vault. Built late in the course, once basics are in place.

**Round-Trip**:
The human-mediated cycle wiki → vault → export → wiki. Pulling and exporting are deliberate acts by a person, never automated sync.

### Tool rules

**Sensitive Lane**:
Copilot Chat (Basic), the only tool authorized for sensitive or IP-sensitive institutional data: internal administration, unsubmitted grant proposals, personnel information, strategic financial planning. Never used for general tasks a free-tier tool does better.
_Avoid_: Home base, primary AI environment

**Daily Driver**:
Google Gemini (free tier), the primary tool for all non-sensitive work: fundamentals, prompting exercises, drafting, long-document analysis.
_Avoid_: Workhorse, main tool

**Core Roster**:
The five tool families taught in the course, each contributing to the KM System: the Copilot ecosystem (Chat, Agent Store, Agent Builder), Gemini, NotebookLM, Perplexity, Obsidian. ChatGPT is mentioned only as an alternative; the Horizon Dashboard belongs to the Optional Use-Case Phase. Canva (through its Teams app) and genspark.ai are taught in Teaching Session 2 in one narrow role each — prototyping a presentation's structure, and building the deck itself — but stay outside the roster: they serve that session's presentation deliverable, feed nothing into the KM System, and sit outside the institutional tenant, so only anonymised, non-sensitive content goes into either.
_Avoid_: Tool ecosystem, satellite tools

**Optional Use-Case Phase**:
Post-KM-System content covering specific research management tasks (detailed budgets, proposal writing, Horizon Dashboard statistics). Only offered after a participant's KM System exists.

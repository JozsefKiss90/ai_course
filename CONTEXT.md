# AI Course for Research Management (ELTE)

The ubiquitous language for the redesigned online AI course for research management administrators. The course teaches AI-supported research management and culminates in a personal, vault-centred knowledge management system.

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
The knowledge management architecture each participant builds for themselves: sources → NotebookLM (the distiller) → Personal Vault (the single source of truth), with the vault's two plugins for finding and asking. The arrow into the vault is a person: read, check against the citation, paste with a source line. The course's central deliverable, built around the participant's Anchor Project. How a custom Copilot agent serves it is decided in the redesign of the later lessons.
_Avoid_: Knowledge base, shared wiki, wiki

**Anchor Project**:
The one real (anonymized) or fictional research project each participant picks at the start and builds their Personal Vault around. All four entity types are populated from its lifecycle.
_Avoid_: Use case, case study, team project

**Wiki Sandbox** *(retired, September 2026)*:
Formerly a participant's own Perfect Wiki instance. Perfect Wiki is a paid service and is out of the course; the Personal Vault is the single source of truth. The four entity types survive as the vault's four folders. Delivered plans that say "wiki" mean the Personal Vault.

**Personal Vault**:
A participant's local Obsidian vault — the single source of truth of their KM System and their visual thinking space (Graph View, Canvas, local Markdown notes). Four folders for the four **entity types**: concepts, processes, guides, projects. Every note carries a `source` line and a `status` (draft or checked). Fed from the participant's notebook by hand.

**Entity types**:
The four kinds of note in the Personal Vault: concepts, processes, guides, projects. Populated from the Anchor Project's lifecycle.

**Distiller**:
NotebookLM (renamed Gemini Notebook, July 2026) in its KM System role: source-grounded, cited answers per entity type that become vault notes once a person has checked them.

**Vault plugins**:
The two Obsidian community plugins taught in Lesson 3. **Smart Connections** surfaces related notes from local embeddings (no API key, offline). **Copilot for Obsidian** answers questions over the vault (Vault QA) with cited notes, on the participant's own free Gemini API key; it is Daily Driver and unrelated to Microsoft Copilot.
_Avoid_: Calling Copilot for Obsidian "Copilot" without the qualifier

**Markdown Generator** *(redesign pending)*:
The custom Copilot agent idea from the original plan (wiki → vault conversion). With the wiki gone, its job is redefined in the redesign of the later lessons.

**Round-Trip** *(retired)*:
The former wiki → vault → export → wiki cycle. Replaced by the one human-mediated arrow notebook → vault; there is no second store to export to.

### Tool rules

**Sensitive Lane**:
Copilot Chat (Basic), the only tool authorized for sensitive or IP-sensitive institutional data: internal administration, unsubmitted grant proposals, personnel information, strategic financial planning. Never used for general tasks a free-tier tool does better.
_Avoid_: Home base, primary AI environment

**Daily Driver**:
Google Gemini (free tier), the primary tool for all non-sensitive work: fundamentals, prompting exercises, drafting, long-document analysis.
_Avoid_: Workhorse, main tool

**Core Roster**:
The tool families taught in the course, each contributing to the KM System: the Copilot ecosystem (Chat, Agent Store, Agent Builder), Gemini, NotebookLM, Obsidian with its two vault plugins. Perplexity is mentioned in passing in Lesson 3 (cited web search; not on the KM System's path); Perfect Wiki is out (paid); ChatGPT is mentioned only as an alternative; the Horizon Dashboard belongs to the Optional Use-Case Phase. Canva (through its Teams app) and genspark.ai are taught in Teaching Session 2 in one narrow role each — Canva for prototyping a presentation's structure and cutting a short video excerpt, genspark.ai for building the deck itself — but stay outside the roster: they serve that session's presentation deliverable, feed nothing into the KM System, and sit outside the institutional tenant, so only anonymised, non-sensitive content goes into either.
_Avoid_: Tool ecosystem, satellite tools

**Optional Use-Case Phase**:
Post-KM-System content covering specific research management tasks (detailed budgets, proposal writing, Horizon Dashboard statistics). Only offered after a participant's KM System exists.

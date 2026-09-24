# Lesson 3 — Knowledge Capture: NotebookLM and the Personal Vault
## Detailed Session Plan (Week 4, 90 minutes, online via Teams)

**Character:** debrief-first, then two tool segments and a hands-on block. Participants open by showing their Lesson 2 workflow blueprints; the facilitator then redraws the KM System without Perfect Wiki, teaches NotebookLM as the grounding floor, and teaches Obsidian as the Personal Vault, with two community plugins that give the vault its own AI. The former Lesson 4 (Obsidian) is merged into this session, so participants leave with the first two floors of their KM System standing: a source-grounded notebook and a linked vault. Nothing from Lessons 1–2 is re-taught; every earlier concept is referenced and pointed forward.

**What changed against the roadmap's original outline:** Perfect Wiki is out of the course (paid service, out of scope). The Wiki Sandbox no longer exists; the Personal Vault is the single source of truth, and NotebookLM is the distiller that feeds it. Perplexity is mentioned only in passing. The old Lesson 4 is folded in here. `course_roadmap.md` records the same changes; later lessons are being redesigned separately and are not referenced in detail.

**Sources for this lesson:**
- `CONTEXT.md` — course vocabulary (Anchor Project, Personal Vault, Daily Driver, Practice Week, Cohort)
- `course_roadmap.md` — the redrawn KM System and the Lesson 3 outline
- `lesson_1.md`, `lesson_2.md` — the concepts the recap map references
- `.scratch/video_transcripts/vid_5_source_separation.md` — the substantive content of a recorded talk on a "four-floor" Google-tools architecture, separated from the speaker's narrative; only Part A rows are used, each marked *verified* or *speaker's claim*. No YouTube link appears in the deck.
- NotebookLM (renamed **Gemini Notebook** on 16 July 2026; same tool, plans and limits) free-tier limits at the time of writing (September 2026): 50 sources per notebook, 100 notebooks, 50 chat questions a day, 500,000 words or 200 MB per source, daily generation caps on Audio and Video Overviews, 10 reports a day, 10 Deep Research sessions a month — https://elephas.app/blog/notebooklm-free-vs-plus and https://elephas.app/blog/notebooklm-source-limits ; re-verify in the facilitator's own account the week before delivery
- Obsidian — https://obsidian.md ; free for personal use, local Markdown files
- Smart Connections (Obsidian community plugin, Brian Petro) — README and docs: https://github.com/brianpetro/obsidian-smart-connections and https://smartconnections.app/ ; v4 core is free, ships a zero-setup local embedding model, needs no API key; Smart Chat has moved to a separate plugin and its API-based model integrations to a paid Pro tier (neither is used)
- Copilot for Obsidian (Obsidian community plugin, logancyang) — https://github.com/logancyang/obsidian-copilot and https://www.obsidiancopilot.com/docs/settings ; the free plugin runs on the participant's own API key; Copilot Plus is a paid tier and is not used. Not related to Microsoft Copilot.
- Google AI Studio (free Gemini API key) — https://aistudio.google.com ; the free API tier may use submitted content to improve Google's models, which is why the plugin is treated as Daily Driver
- Perplexity free tier at the time of writing: unlimited basic searches with citations, a handful of Pro searches a day, file upload with 30-day retention; Spaces are Pro-only — https://www.usecarly.com/blog/perplexity-pricing/ and https://fast.io/resources/perplexity-file-upload-limit/

**Downstream use:** this plan is the single oracle for the Lesson 3 deck tickets and their tests, exactly as `lesson_2.md` is for the Lesson 2 deck. Each segment below is written to map onto a slide sequence.

---

## Timing Overview

| Segment | Duration | Mode |
|---------|----------|------|
| 1. Recap + assignment debrief | 15 min | Participant demos, facilitated |
| 2. The KM System redrawn + NotebookLM in depth | 20 min | Presentation + live facilitator demo |
| 3. Obsidian: the Personal Vault and its two plugins | 20 min | Live facilitator demo |
| 4. Hands-on block: notebook + vault | 25 min | Hands-on, facilitated |
| 5. Assignment briefing + close | 8 min | Presentation + Q&A |
| Buffer | 2 min | — |

Total: 90 minutes. This is the first session after Lesson 1 to run the full Session Template with a hands-on block, because Obsidian has to be installed and a vault created during the session, and because the merged Lesson 4 material makes the assignment too large to start cold. The concept-and-demo slot is split across two segments (NotebookLM, then Obsidian); the hands-on block is 25 minutes instead of 30 to pay for it.

---

## Segment 1 — Recap + Assignment Debrief (15 min)

### Part A: The recap map (≈3 min)

One slide, read at pace. Each row names a Lesson 1 or Lesson 2 concept and the Lesson 3 topic it leads into: a link, never a definition. If anyone asks for the explanation, point to the earlier deck and move on.

| Earlier concept | Leads into (Lesson 3) |
|-----------------|-----------------------|
| The 7 Levels — Level 3 (Power User) reached in the Lesson 2 assignment, Level 4 (Tool Orchestrator) founded | Level 4 is today's target: the right specialised tool per step, NotebookLM for documents and Obsidian for the notes that outlive the chat (Segments 2–3, assignment) |
| The KM System teaser from Lesson 1 (wiki → agent → Obsidian) | Redrawn today without the wiki: notebook → vault, the vault as single source of truth (Segment 2) |
| "More context is not better context"; lost in the middle (Lesson 1) | Why a source-grounded notebook beats a document dump, and why answers carry citations (Segment 2) |
| Hallucination and "verify anything you would sign your name to" (Lesson 1) | NotebookLM's citations are the verification step built into the tool (Segment 2); nothing enters the vault without a source line (Segments 3, 5) |
| The two-lane rule and the anonymise-before-upload rule (Lesson 2) | Both new tools that call a cloud model (NotebookLM, the Copilot plugin) are Daily Driver; anonymised or fictional Anchor Project content only (Segments 2–3) |
| Gems — persistent context, "dedicated workspaces that already know your domain" (Lesson 2) | Notebooks are the evidence counterpart: a Gem organises behaviour, a notebook organises sources; a notebook can feed a Gem (Segment 2) |
| Deep Research in Gemini (Lesson 2) | Deep Research inside a notebook writes its findings straight into the sources (Segment 2); Perplexity as the cited-search alternative, in passing (Segment 2) |
| Gemini Canvas (Lesson 2) | A name clash: Obsidian also has a Canvas, and it is a different thing (Segment 3) |
| Microsoft Copilot Chat (Basic) (Lesson 2) | A second name clash: "Copilot for Obsidian" is an unrelated community plugin and sits in the Daily Driver, never in the Sensitive Lane (Segment 3) |
| The NotebookLM preview: three use cases at scenario level (Lesson 2 Segment 4) | Today the walkthrough: sources, citations, Studio outputs, limits (Segment 2) |
| The Lesson 2 blueprint: every step names its input and its output | Today's assignment chains two tools the same way: notebook output is vault input, and the vault's own AI answers from the vault (Segment 5) |

### Part B: Assignment debrief (≈12 min)

**Format:** 2–3 volunteers from the Cohort, 4 minutes each including questions, screen-shared. The facilitator keeps time visibly (a chat message at the 3-minute mark) and cuts at 4.

**What each volunteer shows** (the three items from the Lesson 2 assignment, in this order):
1. The blueprint: the redrawn roadmap diagram and the step table; the facilitator asks one question: "which steps did you skip, and why?"
2. The presentation: two or three slides, not the whole deck; the facilitator asks which learning outcome the shown slides serve
3. The AI-use log on the last slide: the facilitator asks whether any step's output was rejected at the check, and what happened then

**Capturing common problems:** the facilitator keeps a capture slide open (or a pinned Teams chat message) and writes problems down live as one line each, tagged by item (blueprint / presentation / log). After the last volunteer, read the list back (30 seconds) and say which ones today's session answers ("the notebook answered from the wrong document" → source grounding and citations, Segment 2; "I lost the good outputs after the chat ended" → the vault, Segment 3; "NotebookLM was not available on my account" → the free-tier check in Segment 2) and which go to Practice Week 2.

**Facilitation notes:**
- Ask for volunteers in the Teams chat before the session starts; one backup in case a screen-share fails
- Anyone who did not finish: no discussion now, Practice Week 2 is the venue
- The routing check is enforced from this debrief on: if a volunteer shows non-anonymised material in a Daily Driver tool, name it, in one sentence, as the anonymise-before-upload rule from Lesson 2, and move on

---

## Segment 2 — The KM System Redrawn + NotebookLM in Depth (20 min)

### The KM System, redrawn (≈3 min)

The Lesson 1 teaser showed wiki → agent → Obsidian. The wiki is gone: Perfect Wiki is a paid service, so it is out of scope for a free-tier course. What replaces it is not another wiki but a simpler architecture in which the **Personal Vault is the single source of truth**, and everything else either feeds it or reads from it.

```
   SOURCES (anonymised or fictional Anchor Project material)
   call text · guidelines · FAQ · own notes · public web pages · cited briefings
                          │
                          ▼
   ┌───────────────────────────────────────────────┐
   │ NOTEBOOKLM  (the distiller)                   │
   │ Source-grounded answers with citations;       │
   │ briefings, mind maps, audio overviews         │
   └──────────────────────┬────────────────────────┘
                          │  human-mediated: read, check, paste
                          ▼
   ┌───────────────────────────────────────────────┐
   │ OBSIDIAN  (the Personal Vault — source of truth) │
   │ Four note types: concepts · processes ·       │
   │ guides · projects  ·  [[links]] · Graph View  │
   │   Smart Connections — related notes, local    │
   │   Copilot for Obsidian — ask the vault, cited │
   └───────────────────────────────────────────────┘
```

Two rules travel with the diagram. First, the arrow into the vault is a person: NotebookLM output is read, checked against its citations and *then* pasted, with a source line. No automated sync. Second, the four entity types the wiki was going to hold (concepts, processes, guides, projects) survive as the vault's four folders, so nothing about the content model changes, only where it lives.

**The four-floor map (≈1 min, one slide).** A recorded talk consulted while drafting describes the Google tool family as four floors with four jobs: a *grounding* floor that answers only from your material (NotebookLM), a *frontier-model* floor for exploration with a large context (Gemini), a *specialist* floor of persistent roles (Gems), and a *tools* floor where the intelligence enters your documents and mail (Gemini in Google Workspace). Floors 2 and 3 were Lesson 2. Floor 1 is today. Floor 4 is a paid Workspace feature, so this course puts **Obsidian** on the fourth floor instead: the place where insight becomes durable, linked work. One line from the talk is worth keeping: *the edge is never the tool, it is the system you build.* (Source separation: rows E1, E2, T9.)

### NotebookLM: what it is (≈3 min)

- **Renamed:** Google renamed NotebookLM to **Gemini Notebook** on 16 July 2026. Same tool, same plans, same limits; the slides say "NotebookLM (Gemini Notebook)" once and "NotebookLM" afterwards.
- **What it does:** answers questions *only* from the sources you add, and every answer carries citations to the passage it came from. This is the tool-level answer to Lesson 1's hallucination rule: the receipt comes with the answer. (Rows T1, T2, E3, L1.)
- **What goes in:** PDFs, Google Docs, Slides and Sheets, .docx, plain text and Markdown, web page URLs, YouTube videos with captions, audio files, images (OCR), CSV. One source may be up to 500,000 words or 200 MB.
- **Free tier at the time of writing (September 2026), re-verified the week before delivery:**

| Limit | Free tier |
|-------|-----------|
| Sources per notebook | 50 |
| Notebooks | 100 |
| Chat questions per day | 50 |
| Audio / Video Overviews | Included; a daily generation cap (paid tiers raise it) |
| Reports | 10 a day |
| Deep Research (inside a notebook) | 10 sessions a month |

- **Routing:** NotebookLM runs on the personal Google account, so it is **Daily Driver**: anonymised or fictional material only, the Lesson 2 "what must never enter Gemini" list applies unchanged.

### Grounding versus exploration: when to use which (≈2 min)

The talk gives three situations for NotebookLM; they hold up (row A1 and the "action item" content, minus its wrapper):

1. **You are drowning in material** — more documents than you can hold in your head, let alone in one chat
2. **Precision matters and "close enough" is not good enough** — you will act on the answer, so you need the passage it came from
3. **The same knowledge has to move across formats** — a briefing for you, an audio overview for the commute, flashcards for a junior colleague

Everything else stays in Gemini: drafting, exploration, reasoning beyond the sources, anything where the answer is *not* in your documents. One line for the slide: **a notebook organises evidence; a Gem organises behaviour** (row E6); and a notebook can be given to a Gem as its knowledge base, a link that appeared on paid plans first, so the facilitator re-verifies whether the free tier has it before promising it (row T8, the Lesson 2 Segment 4 flag).

### Studio outputs: one notebook, many formats (≈2 min)

Presented as a table, one line each, with the participant-facing use:

| Output | Use for the Anchor Project |
|--------|----------------------------|
| **Chat with citations** | The core: ask, read the cited passage, decide |
| **Report** (briefing document, study guide, FAQ, timeline; custom report prompt) | The vault's raw material: a briefing per concept or process, sources attached |
| **Mind map** | The first sketch of which notes will link to which |
| **Audio Overview** (interactive: you can interrupt the hosts) | Listen to the call's rules on the commute; the "diffuse mode" use, see below |
| **Video Overview** | A short explainer for a colleague who will not read the call text |
| **Flashcards and quiz** | The learning-material step of the Lesson 2 blueprint, now grounded in your own sources |
| **Deep Research** (inside the notebook) | Fills a gap in the sources with a cited web report that lands in the notebook as a new source; 10 a month on the free tier, so write the question first |

The talk's learning-science point is used once, attributed: *the speaker argues that working memory is small, that learning happens when material moves into long-term memory, and that a notebook lets you alternate between focused investigation at the desk and a "diffuse" pass away from it, for instance by listening to the Audio Overview.* The talk also cites a small, preliminary MIT Media Lab EEG study on AI-assisted writing; the slide does not, because the study is not peer reviewed and the sample was 54 people. (Rows E4, E5, C1.)

### From notebook to note: the wiki-ready output (≈2 min)

The step that makes the notebook part of a system rather than a reading aid. For each of the four entity types, one question shape, asked in the notebook:

| Entity type | Question shape in the notebook |
|-------------|--------------------------------|
| **Concept** | "Define *[term]* as the sources use it. Give the definition, where it matters in the project, and the passages it rests on." |
| **Process** | "List the steps of *[process]* in order, who does each, and the deadline or rule attached to each, citing the source for every step." |
| **Guide** | "Write a how-to for a colleague doing *[task]* for the first time: prerequisites, steps, common mistakes, citing the source per step." |
| **Project** | "Summarise the project: aim, partners (as anonymised in the sources), funding scheme, timeline, key obligations; one line per item with its citation." |

Each answer becomes one note in the vault (Segment 3) with a **source line**: the notebook's name, the source document and, where it exists, the section. An answer without a citation does not become a note. That is the Lesson 1 rule ("verify anything you would sign your name to") operationalised: the notebook does the citing, the person does the checking.

### Perplexity, in passing (≈1 min, one slide)

Not a course tool and not on the KM System's path; named because participants have a free account from Lesson 1 and will meet the question "what if the source does not exist in my notebook yet?" Perplexity is a search engine that answers with inline citations to current web pages; the free tier gives unlimited basic cited searches and a few "Pro" searches a day. Its persistent workspaces (Spaces) are paid-only and are not used.

Two direct benefits, stated once:
- **For research management:** a fast, cited first answer on anything current that a static document cannot hold: a call's latest amendment, a portal change, a policy update. The citations are the point; the answer is not used without opening them.
- **For knowledge management:** because every answer arrives with its sources, the claim can enter the vault *with* its source line in one step, or better, the cited page becomes a new source in the notebook, so the notebook stays the distiller and the vault stays the source of truth.

Where it sits in the chain: Perplexity (or Deep Research in the notebook) finds the source; the notebook grounds it; the vault keeps it. Daily Driver; anonymised or public content only.

### Demo script (≈6 min of the 20, interleaved with the slides above)

Live in the facilitator's own Google account, on fictional Anchor Project material prepared beforehand.

1. Create a notebook "Anchor Project — [fictional name]"; add four sources: the anonymised call text (PDF), the guidelines (PDF), a public web page (the funding programme's FAQ), and the facilitator's own anonymised project notes (Markdown). Show the source count against the 50-source limit (1.5 min)
2. Ask one concept question from the table above; click through one citation to its passage; ask a follow-up that the sources do not answer and show the notebook say so instead of inventing (2 min)
3. Generate one report (briefing document) with the process question shape; leave it on screen: this text is the input to Segment 3's demo (1 min)
4. Mind map: open it, point at the three or four nodes that will become linked notes (30 s)
5. Audio Overview: show one prepared beforehand (generation takes minutes), play 20 seconds, show the interrupt button (1 min)
6. Deep Research and Perplexity: slide only, the routing line "find → ground → keep" (30 s)

**Rule stated while demoing:** everything on screen is fictional; the free-tier numbers are "at the time of writing"; if a Studio output is missing from the facilitator's account on the day, it is shown as a slide and marked as such.

---

## Segment 3 — Obsidian: the Personal Vault and Its Two Plugins (20 min)

Live facilitator demo in Obsidian on the facilitator's machine. This segment stays in the Daily Driver for anything that calls a cloud model, and states clearly which parts never leave the machine.

**Installation flag:** Obsidian is a desktop application (Windows, macOS, Linux; mobile apps exist). On institutionally managed machines the installer may need administrator rights; the facilitator confirms the week before whether participants can install it, and if not, arranges the portable build or a personal device for the hands-on block. Nothing in Obsidian requires an account.

### What Obsidian is (≈2 min)

- A note-taking application whose notes are **plain Markdown files in a folder on your disk**. No account, no cloud, no lock-in: the vault is a folder, and it can be opened with any text editor
- Free for personal use; the paid add-ons (Sync, Publish) are not used
- The vault is the fourth floor of the four-floor map: the place where the notebook's output becomes durable, linked, navigable work
- Talk row E7, one line: work scattered across four places has no connecting thread; the vault is the thread

### The vault: structure, notes, links, tags (≈5 min)

**Structure:** one vault per participant, named after the Anchor Project, with four folders that are the four entity types:

```
Anchor Project vault/
├── concepts/
├── processes/
├── guides/
├── projects/
└── _templates/      (one note template, below)
```

**The note template** (one Markdown file in `_templates/`, pasted into every new note; Obsidian's core Templates plugin can insert it):

```markdown
---
type: concept | process | guide | project
source: <notebook name> · <source document> · <section, if any>
captured: YYYY-MM-DD
status: draft | checked
---

# <Title>

<The checked text from the notebook, edited by you.>

## Related
- [[ ]]
```

The `source` and `status` fields are the human gate from Segment 2 made visible: a note is `draft` until its text has been checked against the citation, then `checked`. Graph View and the plugins do not care; the participant does.

**Links:** `[[Note title]]` creates a link; typing `[[` offers every note in the vault; a link to a note that does not exist yet creates it when clicked. **Backlinks** (the right-hand pane) show every note that points at the current one. **Tags** (`#eligible-cost`, `#deadline`) cut across the four folders.

**Linking discipline** (the slide's one rule): *a note with no links is a file, not knowledge.* Every concept links to the process it appears in; every process links to its concepts and to the guide that explains it; the project note links to everything. Graph View only pays off if entities reference each other.

**Graph View:** the whole vault as nodes and edges; filters by folder and tag; local graph for one note. **Canvas:** a freeform board where notes, cards and images are arranged spatially, for planning a proposal timeline or mapping stakeholders. Name clash with Gemini's Canvas from Lesson 2: Gemini Canvas is a drafting surface inside a chat, Obsidian Canvas is a whiteboard of your own notes.

### Two community plugins: the vault's own AI (≈8 min)

Enabling community plugins means switching off Obsidian's *Restricted mode* (Settings → Community plugins). The facilitator shows the switch and the warning, and states the rule: only the two plugins below, from the official community list, and read the plugin's data note before enabling.

| | **Smart Connections** | **Copilot for Obsidian** |
|---|---|---|
| **Author** | Brian Petro | logancyang |
| **What it does** | Shows notes semantically related to the one you are reading (Connections view); semantic **Lookup** across the vault | **Chat** with a model inside Obsidian; **Vault QA**: ask a question, get an answer assembled from your notes with the notes cited; Relevant Notes surfaced in the chat |
| **How it works** | Builds embeddings of your notes with a **local model that ships with the plugin**; no API key, no account, nothing leaves the machine | Indexes the vault locally, then sends the question and the relevant note chunks to the model you configure; you bring your own API key |
| **Cost** | Free core (v4). Paid "Pro" add-ons and the separate Smart Chat plugin exist and are **not used** | Free plugin with your own key. "Copilot Plus" is a paid tier and is **not used** |
| **Which model** | Local embedding model, no choice needed | A free **Gemini API key from Google AI Studio**; the plugin lists Gemini models to choose from |
| **Lane** | No cloud call: the only AI in the course that runs entirely on your device | **Daily Driver.** The free API tier may use submitted content to improve Google's models; the vault holds anonymised or fictional Anchor Project content only, so this is acceptable, and nothing from the Lesson 2 "never" list is ever in the vault |
| **Job in the KM System** | *Finding:* "what in my vault relates to this?" The link you forgot to make | *Asking:* "what does my vault say about X?" The vault's own grounding floor, with citations to notes instead of to sources |
| **Name clash** | — | Not Microsoft Copilot. Unrelated project, unrelated data path, never the Sensitive Lane |

**Why two plugins:** they answer different questions. Smart Connections surfaces relationships while you write, silently, offline, which is what makes the linking discipline sustainable past thirty notes. Copilot for Obsidian answers questions over the whole vault the way NotebookLM answers over sources, so once the vault is the source of truth it can be queried like one. Together they close the loop the wiki was supposed to close: capture in the notebook, keep in the vault, query the vault.

**Setup order for the hands-on block (on the slide):**
1. Settings → Community plugins → turn off Restricted mode → Browse
2. Install and enable **Smart Connections**; wait for the first embedding run (a progress notice), open the Connections view from the right sidebar
3. Get a Gemini API key at Google AI Studio (personal Google account, free tier)
4. Install and enable **Copilot for Obsidian**; Settings → Copilot → add the Gemini key, pick a Gemini chat model and, if offered, a Gemini embedding model; run "Refresh vault index"
5. Open the Copilot pane, switch to **Vault QA**, ask one question

### Demo script (≈8 min of the 20, interleaved)

1. Create a vault "Demo Anchor Project", the four folders, the template (1 min)
2. Paste the Segment 2 briefing into `processes/`, fill the frontmatter, set `status: draft`; check one sentence against the notebook's citation, set `checked` (1.5 min)
3. Create two concept notes from the same briefing, link them from the process note with `[[ ]]`, show backlinks; add one tag (1.5 min)
4. Graph View: three nodes; then open a prepared vault of ~25 linked notes and show the same view, with the folder filter (1 min)
5. Smart Connections on the prepared vault: open a note, read the Connections view, click one related note the facilitator "forgot" to link, add the link (1.5 min)
6. Copilot for Obsidian on the prepared vault, Vault QA: "Which deadlines apply to the periodic report, and which notes say so?" Read the cited notes; ask a question the vault cannot answer and show the answer say so (1.5 min)

**Rule stated while demoing:** the vault contains only anonymised or fictional content, so the Copilot plugin's cloud call is a Daily Driver call; Smart Connections never calls anything.

---

## Segment 4 — Hands-On Block: Notebook + Vault (25 min)

Everyone builds the smallest working version of their KM System on their own Anchor Project. The facilitator screen-shares a checklist slide; participants mark progress in the Teams chat ("✅ 1–4") so stragglers are visible; quick finishers help.

**Checklist per participant:**

| # | Step | Done when |
|---|------|-----------|
| 1 | Create a notebook for your Anchor Project; add at least **three anonymised or public sources** (the Lesson 2 blueprint's step 2 files qualify) | Sources listed, notebook answers a test question with a citation |
| 2 | Ask **one concept question** and **one process question** in the shapes from Segment 2; open one citation each | Two cited answers on screen |
| 3 | Install Obsidian; create a vault named after your Anchor Project; make the four folders and the template | Vault open, folders visible |
| 4 | Paste the two answers as two notes in the right folders; fill `type`, `source`, `captured`; leave `status: draft` | Two notes with frontmatter |
| 5 | Link them to each other with `[[ ]]`; create one more note by clicking a link to a title that does not exist yet | Graph View shows three connected nodes |
| 6 | Turn off Restricted mode; install and enable **Smart Connections**; open the Connections view on one note | Connections view lists the other notes |
| 7 | Get a Gemini API key at Google AI Studio; install **Copilot for Obsidian**; enter the key; refresh the index | Settings saved without an error |
| 8 | In Copilot's **Vault QA**, ask a question your three notes can answer | An answer citing at least one note |

Steps 1–5 are the minimum; anyone at step 5 by the 20-minute mark has a working system. Steps 6–8 finish in the assignment or at Practice Week 2 if time runs out.

**Facilitation notes:**
- Typical failure points: Obsidian install blocked on a managed machine (portable build or a personal device); Google account in the wrong browser profile (same fix as Lesson 1); API key pasted with a trailing space; Copilot's index refresh not run, so Vault QA answers "no relevant notes"; Smart Connections still embedding on a slow machine (wait, it is a one-off)
- Participants who bring no anonymised material use the facilitator's sample documents (prepared, fictional)
- The free-tier chat cap (50 a day) is far above what the block needs, but say it once so nobody burns questions on chit-chat
- Keep the "what must never enter Gemini" list from Lesson 2 on the second monitor; the vault inherits it

---

## Segment 5 — Assignment Briefing + Close (8 min)

### Assignment slide (as it will appear)

**Assignment: your KM System, first two floors**

Populate your Personal Vault from your Anchor Project, through your notebook, and put the vault's own AI to work.

1. **Notebook:** at least 5 sources, anonymised or public; one Deep Research run or Perplexity search that adds a source you did not have, with its citation.
2. **Vault:** at least **5 concepts, 2 processes, 1 guide, 1 project note**, each produced from a cited notebook answer, each with a filled `source` line and `status: checked` after you have compared the text with the citation.
3. **Links:** at least 10 `[[links]]`, every note linked at least once; the project note links to every process. Bring a **Graph View screenshot**.
4. **Smart Connections:** one relationship the Connections view surfaced that you had not linked; add the link and write one line on why you had missed it.
5. **Copilot for Obsidian:** one **Vault QA** question about your project, the cited answer, and one line on whether the cited notes actually support it.
6. **AI-use log:** tool, date and purpose per step, as in Lesson 2.

**Outcome:** Level 4 reached: the right specialised tool per step, chained, with the outputs kept somewhere they outlive the chat.

### How the chain reads (≈2 min)

The same discipline as the Lesson 2 blueprint: every step names its input and its output.

| # | Step | Tool | Lane | In | Out |
|---|------|------|------|----|-----|
| 1 | Gather and anonymise sources | No AI tool; Word or Excel, by hand | None (manual) | Your Anchor Project documents | Files that may be uploaded → step 2 |
| 2 | Fill the gap | Deep Research in the notebook, or Perplexity | Daily Driver | One question your sources do not answer | One cited source → step 3 |
| 3 | Ground | NotebookLM | Daily Driver | The files from 1 and the source from 2 | Cited answers per entity type → step 4 |
| 4 | Keep | Obsidian | Local | The cited answers | Notes with source lines and links → steps 5, 6 |
| 5 | Find | Smart Connections | Local, offline | The vault | Missed relationships → back into step 4 as links |
| 6 | Ask | Copilot for Obsidian, Vault QA | Daily Driver | The vault and one question | A cited answer, checked against the notes |

Only step 1 is required in the strict sense, and only when your material contains sensitive data; every other step is the assignment itself. The gate that is not a step, from Lesson 2, applies: check every output before it becomes the next step's input, and log it.

### Effort and where the work is shown (≈1 min)

- Expect 3–4 hours across the two weeks: the vault notes are the bulk, the plugin steps are minutes once installed
- Done looks like a vault whose Graph View has no isolated nodes, nine or more `checked` notes with source lines, one added link you owe to Smart Connections, one cited Vault QA answer you have judged, and a log
- Show the work at Practice Week 2's drop-in (W6) for troubleshooting, and at the next Teaching Session's debrief (W7): 2–3 volunteers walk through notebook → vault → Vault QA

### Close (≈1 min)

- **Practice Week 2 (W6):** optional facilitated drop-in, no new material; bring installation problems, plugin setup, linking questions and free-tier surprises
- **Next Teaching Session (W7):** builds on the vault as source of truth; the detailed plan follows the redesign of the remaining lessons and is announced in Teams before W6

---

## Materials to Prepare (Facilitator)

- Slide deck per the segment structure above, in a design distinct from Lessons 1 and 2; the redrawn KM System diagram and the four-floor map as two slides
- Volunteer list and one backup collected in Teams chat before the session; a capture slide or pinned chat message for the debrief
- Fictional Anchor Project material: anonymised call text (PDF), guidelines (PDF), a public FAQ page URL, and Markdown project notes; the same set offered to participants who bring nothing of their own
- A prepared notebook on that material with an Audio Overview already generated; a prepared Obsidian vault of ~25 linked notes with Smart Connections embedded and Copilot for Obsidian configured, for the two plugin demos
- The NotebookLM free-tier check the week before delivery: source, notebook and chat limits, which Studio outputs exist, Deep Research cap, and whether notebook-to-Gem linking is on the free tier; any missing feature shown as a slide and marked
- Obsidian installability on institutional machines confirmed the week before; portable build link ready as fallback
- Smart Connections and Copilot for Obsidian installed fresh on a clean vault the day before, to catch settings changes; the Google AI Studio key flow walked through once
- The Lesson 2 "what must never enter Gemini" list and the anonymisation one-pager reused unchanged
- Assignment slide text and the hands-on checklist ready to paste into Teams chat after the session

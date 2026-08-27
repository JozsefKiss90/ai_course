# AI for Research Management Administrators
# Participant Handbook

---

## Course Overview

| | Day 1: Foundations | Day 2: Depth & Context | Day 3: Integration |
|---|---|---|---|
| **Level** | 1-2 | 3 | 4 |
| **Theme** | Question Asker --> Prompt Crafter | Power User | Workflow Weaver |
| **Focus** | Prompt structure, meta-prompting, tool comparison | Persistent workspaces, document analysis, research intelligence | Multi-tool workflows, visual outputs, interactive tools, capstone |

**Your Team:** __________________ **Your Domain:** __________________

**Team Members:**
1. ________________________
2. ________________________
3. ________________________

---

## How This Course Runs (Microsoft Teams)

This is a live, online course delivered over three days via **Microsoft Teams**.

- **Plenary sessions** (demos, framing, share-outs) run in the main Teams meeting -- keep your camera on when you can.
- **Team exercises** run in your team's **breakout room**; the facilitator drops in to help.
- **Ask questions any time** in the meeting chat -- the facilitator watches it throughout.
- **Screen sharing:** you'll share your screen during share-outs and your capstone demo, so keep your tools pre-loaded.
- **Files and links** (vault template, scenario briefs, forms) are posted in the course Teams channel.

---

## Your Tool Ecosystem

| Tool | What It Does Best | URL | Login? |
|------|------------------|-----|--------|
| **Microsoft 365 Copilot** | Writing, analysis, Notebooks (persistent context), Agents (custom tools) | microsoft365.com | Work account |
| **ChatGPT Free** | Meta-prompting, Canvas, structured outputs | chatgpt.com | Yes |
| **Google Gemini** | Processing very long documents (100+ pages) | gemini.google.com | Google acct |
| **Perplexity AI** | Cited research, live web data, fact verification | perplexity.ai | Yes |
| **NotebookLM** | Source-grounded document analysis (only YOUR docs) | notebooklm.google.com | Google acct |
| **Horizon Dashboard** | Official EU funding statistics, success rates, CSV export | dashboard.tech.ec.europa.eu | No |
| **Canva AI** | Visual one-pagers, infographics, presentations | canva.com | Yes |
| **Obsidian** | Local knowledge management, linked notes, templates | obsidian.md (desktop app) | No |

### When to Use Which Tool

```
Need to WRITE or DRAFT something?          --> Microsoft 365 Copilot
Need to ANALYZE your own documents?        --> NotebookLM
Need to process a VERY LONG document?      --> Google Gemini
Need CURRENT facts with citations?         --> Perplexity AI
Need OFFICIAL EU funding statistics?       --> Horizon Dashboard
Need to VERIFY a number from an AI?        --> Horizon Dashboard
Need AI to WRITE a better PROMPT?          --> ChatGPT (meta-prompting)
Need a VISUAL deliverable?                 --> Canva AI
Need to BUILD an interactive tool?         --> Copilot Agent (Agent Builder)
Need to ORGANIZE and CONNECT everything?   --> Obsidian
```

---

## The ICC Prompt Framework

Every effective prompt has three components:

```
INSTRUCTION: What do you want the AI to do?
  - Be specific: "Draft a budget justification" not "help with budget"
  - One task per prompt works best

CONTEXT: What does the AI need to know?
  - Who you are (role, institution, programme)
  - What you're working on (project, call, document)
  - Background the AI wouldn't have

CONSTRAINTS: What are the rules?
  - Format (bullet points, table, narrative, email)
  - Length (word count, character limit, number of pages)
  - Tone (formal, accessible, technical)
  - Must-include items
  - What to avoid
```

### Example

```
[Instruction]
Write a partner search announcement for the Horizon Europe
Funding & Tenders portal.

[Context]
We are a mid-sized European university's research office.
Our PI specializes in sustainable urban mobility. We are
looking for 2-3 partners with expertise in IoT sensor
networks and urban planning policy. The target call is
HORIZON-CL5-2025-D6-01-02. Budget envelope is EUR 3-4M total.

[Constraints]
Maximum 2000 characters. Professional but engaging tone.
Must include: topic, expertise sought, role offered,
deadline, and contact method.
```

---

## Key Techniques

### 1. "Ask Me Questions First"
Instead of trying to include all context yourself, let the AI figure out what it needs:

```
I need to [task]. Before doing anything, ask me all the
questions you need to produce the best possible result.
```

### 2. Meta-Prompting (ChatGPT --> Copilot)
Use one AI to write optimized prompts for another:

```
I need to use an AI assistant to [task]. Write the optimal
prompt I should use, including all the context and constraints
that would produce the best result.
```

Then copy the generated prompt into Copilot.

### 3. Reverse Prompt
After a long conversation produces a great result:

```
This final output is exactly what I needed. Write the single
prompt that would have gotten us to this result on the first
try. Include all the context and constraints we discovered
during our conversation. Format it so I can copy-paste it
and reuse it next time.
```

Save the result in your prompt library.

### 4. Ground Truth Verification
Always verify quantitative claims from AI against official sources:
- EU funding statistics --> Horizon Dashboard (dashboard.tech.ec.europa.eu)
- Perplexity citations --> click through and verify
- NotebookLM citations --> click to see exact source passage

---

## Copilot Notebooks Quick Reference

### Setting Up a Notebook
1. Go to microsoft365.com --> Copilot --> Notebooks --> New notebook
2. Give it a clear, specific name (e.g., "Horizon Europe Grant Assistant")
3. Add a working brief as the first note (see template below)
4. Add reference sources (PDFs, Word/Excel files, Copilot Pages, meeting notes)
5. Every chat in the Notebook stays grounded in your brief and sources -- and your team can co-work in it in real time

### Working Brief Template

```
You are a [role] working with [institution type].
You specialize in [domain/programme].

When drafting text:
- [Tone and style rules]
- [Structure to follow]
- [Specific behaviors]

When reviewing text:
- [What to check]
- [How to give feedback]

Output formatting:
- [Format preferences]
- [Special markers, e.g., [ASSUMPTION] tags]
```

---

## Copilot Agents Quick Reference

A **custom agent** (built with Agent Builder) packages a task into a reusable, shareable tool -- described in plain language, no coding.

### Building an Agent
1. Go to microsoft365.com --> Copilot --> **Create agent** (Agent Builder)
2. Give it a clear name (e.g., "Ethics Screening Assistant")
3. Write its **instructions**: what it should ask the user, in what order, and what it should produce (your Notebook working brief is a great starting point)
4. Optional: add **knowledge** sources, and turn on **"Create documents, charts, and code"** for calculations or charts
5. Test it in the **"Try it"** pane, then **share** it with colleagues

### Notebook vs. Agent
- **Notebook** = a persistent workspace *you* work in, grounded in your sources.
- **Agent** = a reusable tool *others* can use, that interviews the user and produces a specific output.

---

## NotebookLM Quick Reference

### Key Differences from Copilot
- Only uses YOUR uploaded documents (no training data)
- Every claim has a clickable citation to the source passage
- Cannot make things up -- tells you when information isn't in your sources
- Best for: compliance checks, audit trails, document cross-referencing

### How to Use
1. Create a new notebook
2. Upload 2-5 source documents (PDF, Google Docs, text)
3. Review the auto-generated summary
4. Ask specific, actionable questions
5. Click citations to verify every claim

---

## Horizon Dashboard Quick Reference

### What It Provides
- Success rates by call topic, cluster, and country
- Funding distribution and participation statistics
- Country and organization profiles
- Project search and data
- CSV data export for AI analysis

### How to Use with AI Tools
1. Navigate to dashboard.tech.ec.europa.eu
2. Find the relevant statistics (e.g., success rates for your cluster)
3. Export as CSV
4. Upload the CSV to Copilot or Gemini
5. Ask for trend analysis, comparisons, or strategic insights

### Key Principle
The Dashboard provides **authoritative numbers**. AI tools provide **analysis and narrative**. When they disagree, trust the Dashboard.

---

## Workflow Design Framework

Use this framework when designing AI-assisted workflows:

```
1. TRIGGER:   What event initiates this workflow?
2. STEPS:     What needs to happen, in what order?
3. TOOLS:     Which AI tool for each step, and why?
4. HANDOFFS:  How does output move between tools?
5. GATES:     Where does a human review and decide?
6. OUTPUT:    What is the final deliverable?
7. STORAGE:   Where is everything saved for reuse?
```

### Handoff Mechanics
- **Text outputs:** Copy from Tool A, paste into Tool B with an instruction like: "Based on the following [analysis/findings]: [paste]"
- **CSV data (Dashboard):** Export CSV, upload directly to Copilot or Gemini
- **Document analysis (NotebookLM):** Copy the structured output, paste as context into Copilot
- **All outputs:** Save to Obsidian with links to related notes

---

## Obsidian Vault Structure

```
/AI-Research-Admin-Course
  /00-Prompts              Your prompt library
  /01-Templates            Reusable note templates
  /02-Tool-Notes           Notes on each AI tool
  /03-Workflows            Workflow documentation
  /04-Team-Project         Team deliverables
  /05-Daily-Reflections    Learning journal
```

### Essential Shortcuts
- `[[` -- Create a link to another note
- `Ctrl+G` / `Cmd+G` -- Open Graph View
- `Ctrl+T` / `Cmd+T` -- Insert template (if configured)
- `Ctrl+P` / `Cmd+P` -- Command palette (search any feature)

### Linking Best Practice
Ask yourself: "If I were reading this note and wanted more information about something mentioned here, what would I click on?" Create that link.

---

## Deliverables Checklist

By the end of the course, your team should have:

- [ ] **Prompt Library** -- 10+ refined prompts in Obsidian `/00-Prompts/`
- [ ] **Copilot Notebook** -- Configured workspace with a working brief and reference sources
- [ ] **NotebookLM Notebook** -- Source-grounded analysis of your domain documents
- [ ] **Intelligence Briefing** -- Citation-backed research briefing in Obsidian
- [ ] **Tool Comparison Matrix** -- Evaluation of tools for your task types
- [ ] **Horizon Dashboard Analysis** -- Official data exported and analyzed
- [ ] **Interactive Agent** -- Working custom agent built with Agent Builder
- [ ] **Visual Asset** -- Professional one-pager or infographic from Canva
- [ ] **Documented Workflow** -- Complete multi-tool workflow in Obsidian
- [ ] **Obsidian Knowledge Vault** -- Linked notes, session logs, Kanban board
- [ ] **Daily Reflections** -- 3 reflection notes capturing your learning

---

## Five Principles for AI-Assisted Research Management

```
1. Ask "What's the best tool for THIS step?"

2. Save every good prompt -- your prompt library
   is your most valuable AI asset.

3. Document workflows for reuse and sharing.

4. Keep the human in the loop. AI generates.
   You validate. Always.

5. Keep learning and experimenting.
   These tools change monthly. Stay curious.
```

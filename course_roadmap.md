# AI for Research Management Administrators
## 3-Day Course Roadmap | Levels 1-4

**Participants:** 15 (5 teams of 3)
**Primary AI Environment:** Claude Desktop / Claude Cowork
**Progression:** Level 1 (Question Asker) --> Level 2 (Prompt Crafter) --> Level 3 (Power User) --> Level 4 (Workflow Weaver)

---

## Tool Ecosystem Overview

| Tool | Role in Course | Tier |
|------|---------------|------|
| **Claude Desktop / Cowork** | Primary AI environment; Projects, Artifacts, collaborative work | Free / Pro |
| **ChatGPT Free** | Meta-prompting, comparison baseline, Canvas prototyping | Free |
| **NotebookLM** | Document analysis, source grounding, knowledge synthesis | Free |
| **Perplexity AI** | Research discovery, citation-backed exploration | Free |
| **Google Gemini** | Long-context experimentation (1M tokens), multimodal tasks | Free |
| **Canva AI** | Visual outputs, presentations, infographics | Free |
| **Horizon Dashboard** | Official EU funding statistics, success rates, country/organization data | Free |
| **Obsidian** | Personal/team knowledge management with plugins | Free |

---

## Pre-Course Setup (Distributed 1 Week Before)

### Participant Preparation
1. Create free accounts: Claude (claude.ai), ChatGPT, NotebookLM, Perplexity, Google Gemini, Canva
2. Bookmark the Horizon Dashboard (dashboard.tech.ec.europa.eu) and explore its main sections (projects, statistics, country profiles)
3. Install Obsidian desktop app
4. Bring 2-3 real work documents (anonymized if needed): a funding call text, a project report, a policy/regulation document, meeting minutes, or similar research management artifacts
5. Complete a 5-question self-assessment survey: current AI usage, biggest workflow pain points, expectations

### Instructor Preparation
- Pre-build an Obsidian vault template with folder structure for the course
- Prepare a shared Google Drive folder per team for document exchange
- Prepare a "Research Management Scenario Bank" with realistic tasks (grant writing, compliance checks, reporting, stakeholder communication, event planning, data management plans)

---

## Team Formation

Five teams of three, ideally mixed by:
- Role type (pre-award, post-award, compliance, strategy, coordination)
- Prior AI experience (pair novices with slightly more experienced users)
- Each team selects a research management domain to focus on throughout the course:
  - **Team A:** Grant Lifecycle Management (pre-award)
  - **Team B:** Research Compliance & Ethics
  - **Team C:** Research Reporting & Impact Assessment
  - **Team D:** Stakeholder Communication & Dissemination
  - **Team E:** Research Data Management & Open Science

---

# DAY 1: Foundations
## Level 1 "The Question Asker" + Level 2 "The Prompt Crafter"

**Goal:** Move participants from treating AI as a search engine to crafting effective, repeatable prompts for research management tasks.

---

### MODULE 1.1 | Opening & Orientation (09:00 - 10:00)

**Format:** Plenary, interactive

1. **Welcome & Course Arc** (15 min)
   - Present the 7 Levels framework (Levels 1-4 focus)
   - Show the "before and after" transformation: same research management task done at Level 1 vs. Level 4
   - Set expectations: by Day 3, each team will have a working AI-assisted workflow for their domain

2. **Live Diagnostic: Where Are You Now?** (20 min)
   - Each participant opens Claude Desktop and asks it a question they would normally Google related to their work
   - Examples: "What is Horizon Europe?", "How do I write a data management plan?", "What are the eligibility criteria for ERC grants?"
   - Collect and display the prompts anonymously -- observe patterns (short, no context, no constraints)

3. **The AI Landscape for Research Management** (25 min)
   - Quick tour of tools they will use (live demo of each, 3 min per tool)
   - Positioning: Claude Desktop as the "home base", other tools as specialized instruments
   - Key concept: AI is not one tool, it is an ecosystem

---

### MODULE 1.2 | Level 1 -- The Question Asker (10:00 - 11:00)

**Core Concept:** AI as a capable conversational partner, not a search engine.

**Demo (15 min): The Same Question, Three Ways**
Using Claude Desktop, demonstrate with a research management scenario:
- Version 1 (Google-style): "Horizon Europe budget"
- Version 2 (Better): "Explain the budget structure of Horizon Europe Pillar 2 collaborative projects"
- Version 3 (Good): "I'm preparing a budget for a Horizon Europe Cluster 4 collaborative project with 8 partners. Explain the eligible cost categories, overhead calculation method, and common budgeting mistakes."

Show how output quality scales with input quality.

**Team Exercise 1.1: "First Contact" (30 min)**
Each team member picks one real task from their daily work and asks Claude Desktop about it as they naturally would. Then they:
1. Screenshot the prompt and response
2. Rate the usefulness (1-5)
3. Identify what was missing from the response
4. Share within the team and discuss patterns

**Debrief (15 min)**
- Common patterns: prompts too vague, no role context, no format specification
- Key insight: the AI doesn't know you're a research manager at a university unless you tell it

---

### BREAK (11:00 - 11:15)

---

### MODULE 1.3 | Level 2 -- The Prompt Crafter, Part 1: Structure (11:15 - 12:30)

**Core Concept:** The Instruction-Context-Constraints (ICC) framework and the power of asking AI to ask you questions first.

**Demo (20 min): The ICC Framework in Research Management**
Live in Claude Desktop:

**Prompt anatomy for a real task -- drafting a partner search announcement:**
```
[Instruction] Write a partner search announcement for posting on the
Horizon Europe Funding & Tenders portal.

[Context] We are a mid-sized European university's research office.
Our PI specializes in sustainable urban mobility. We are looking for
2-3 partners with expertise in IoT sensor networks and urban planning
policy. The target call is HORIZON-CL5-2025-D6-01-02. Budget
envelope is EUR 3-4M total.

[Constraints] Maximum 2000 characters. Professional but engaging tone.
Must include: topic, expertise sought, role offered, deadline, and
contact method. Follow the standard Funding & Tenders template style.
```

Then show the shortcut: "Before answering, ask me the questions you need to write the best possible partner search announcement for the Horizon Europe portal."

**Team Exercise 1.2: "Prompt Makeover" (35 min)**
Each team takes their Level 1 prompts from Exercise 1.1 and rebuilds them using ICC structure. Then they try the "ask me questions first" approach for the same task.
- Compare the three outputs side-by-side (original, ICC, question-first)
- Document the best-performing prompt in a shared team note

**Plenary Share-Out (20 min)**
Each team presents their best before/after transformation (2 min each), followed by brief discussion.

---

### LUNCH (12:30 - 13:30)

---

### MODULE 1.4 | Level 2 -- The Prompt Crafter, Part 2: Meta-Prompting & Iteration (13:30 - 15:00)

**Core Concept:** Using AI to write better prompts (meta-prompting), and the "reverse prompt" technique.

**Demo (20 min): Meta-Prompting with ChatGPT + Claude**
1. In ChatGPT Free: "I need to use an AI assistant to help me draft the narrative impact section of an EU project's periodic report. Write the optimal prompt I should use, including all the context and constraints that would produce the best result."
2. Take ChatGPT's generated prompt --> paste it into Claude Desktop
3. Compare with a manually written prompt for the same task
4. Show the "reverse prompt" technique: after a long back-and-forth that produced a good result, ask Claude: "Write the single prompt that would have gotten us to this result on the first try."

**Team Exercise 1.3: "The Prompt Factory" (40 min)**
Each team works on TWO research management tasks from their domain:

| Team | Task 1 | Task 2 |
|------|--------|--------|
| A - Grants | Draft a call eligibility checklist | Write a go/no-go decision memo |
| B - Compliance | Summarize ethics requirements for a human-subjects project | Draft an informed consent template |
| C - Reporting | Write a publishable project summary from a technical report | Create a KPI tracking narrative |
| D - Communication | Draft a press release for a granted project | Write a stakeholder newsletter section |
| E - Data Mgmt | Draft a data management plan outline | Write a data sharing agreement summary |

Workflow per task:
1. Use ChatGPT Free to generate the meta-prompt
2. Refine the meta-prompt as a team
3. Execute in Claude Desktop
4. Iterate until satisfied
5. Use the "reverse prompt" technique to capture the final optimized prompt
6. Save the final prompt as a reusable template

**Debrief & Prompt Library Introduction (20 min)**
- Introduce the concept of a team "Prompt Library" (will live in Obsidian from Day 2)
- Each team saves their 2 refined prompts in a shared document
- Discussion: which tasks benefit most from structured prompting?

---

### BREAK (15:00 - 15:15)

---

### MODULE 1.5 | Comparison & Critical Evaluation (15:15 - 16:15)

**Core Concept:** Different AI tools produce different results. Learn to evaluate and cross-reference.

**Demo (15 min): The Same Prompt, Four Tools**
Take one research management prompt and run it simultaneously in:
- Claude Desktop
- ChatGPT Free
- Google Gemini
- Perplexity AI

Show differences in: depth, structure, citation behavior, tone, accuracy. Highlight that Perplexity cites sources, Gemini handles longer inputs, Claude excels at nuanced writing, ChatGPT is strong at structured outputs.

**Ground Truth Check with the Horizon Dashboard (5 min)**
Open the Horizon Dashboard (dashboard.tech.ec.europa.eu). Show how to pull real statistics -- e.g., success rates by call topic, funding by country, number of participants by organization type. Compare one specific claim from the AI outputs against the Dashboard's official data. Key message: the Dashboard provides the authoritative numbers that AI tools may approximate, hallucinate, or have outdated versions of. Always verify quantitative claims against official sources.

**Team Exercise 1.4: "AI Tool Comparison Matrix" (35 min)**
Each team runs one of their refined prompts across all four tools and fills in a comparison matrix:

| Criterion | Claude | ChatGPT | Gemini | Perplexity |
|-----------|--------|---------|--------|------------|
| Accuracy | | | | |
| Completeness | | | | |
| Tone/Style fit | | | | |
| Source citations | | | | |
| Actionability | | | | |
| Best for this task? | | | | |

**Plenary Discussion (10 min)**
- Teams share their "best tool for this task" verdict
- Build a collective "tool-task fit" reference

---

### MODULE 1.6 | Day 1 Wrap-Up & Obsidian Introduction (16:15 - 17:00)

**Obsidian Setup (30 min)**
- Install the pre-built vault template (instructor distributes via USB/download)
- Vault structure:
  ```
  /AI-Research-Admin-Course
    /00-Prompts          (prompt library)
    /01-Templates         (reusable document templates)
    /02-Tool-Notes        (notes on each AI tool)
    /03-Workflows         (workflow documentation, Day 2-3)
    /04-Team-Project      (team deliverables)
    /05-Daily-Reflections (learning journal)
  ```
- Quick tour: creating notes, linking with [[]], tags, and the Graph View
- Recommended plugins to pre-install: Templates, Dataview, Kanban

**Day 1 Reflection (15 min)**
- Each participant writes a short reflection note in Obsidian: `/05-Daily-Reflections/Day1.md`
  - What surprised you most?
  - What is your most useful prompt so far?
  - What research management task do you most want to tackle with AI?

---

### Day 1 Deliverables Checklist
- [ ] At least 4 refined prompts per team saved in shared docs
- [ ] AI tool comparison matrix completed
- [ ] Obsidian vault set up with initial prompt library entries
- [ ] Day 1 reflection note written

---
---

# DAY 2: Depth & Context
## Level 3 "The Power User"

**Goal:** Move from one-off prompts to persistent AI workspaces with deep context, and master document-heavy research management workflows using NotebookLM and long-context tools.

---

### MODULE 2.1 | Recap & Level 3 Introduction (09:00 - 09:30)

**Rapid Recap (10 min)**
- Quick quiz: ICC framework, meta-prompting, reverse prompt technique
- Each team shares their single best prompt from Day 1

**Level 3 Framing (20 min)**
- The key frustration at Level 2: rebuilding context from scratch every conversation
- The solution: Projects (Claude), Custom GPTs (ChatGPT), and persistent context
- Demo: show the difference between a bare Claude conversation and one inside a Project with custom instructions and uploaded files

---

### MODULE 2.2 | Claude Projects for Research Management (09:30 - 11:00)

**Core Concept:** Building dedicated AI workspaces with persistent context, custom instructions, and reference files.

**Demo (25 min): Building a "Grant Writing Assistant" Project in Claude**
Live setup of a Claude Project:
1. **Project name:** "Horizon Europe Grant Assistant"
2. **Custom instructions:**
   ```
   You are an experienced EU research management advisor working with
   university research offices. You specialize in Horizon Europe
   collaborative projects (RIAs and IAs).

   When drafting text:
   - Use formal but clear EU project language
   - Follow standard proposal section structures (Excellence,
     Impact, Implementation)
   - Flag common evaluation pitfalls
   - Reference current Horizon Europe rules (General MGA,
     HE Programme Guide)

   When reviewing text:
   - Check alignment with evaluation criteria
   - Identify vague claims that need quantification
   - Suggest concrete improvements, not generic advice

   Output formatting:
   - Use headers and bullet points for readability
   - Include word/character counts when relevant
   - Mark assumptions clearly with [ASSUMPTION] tags
   ```
3. **Upload reference files:** A call topic text (PDF), the team's CV/expertise summary, a template from a previous successful proposal
4. **First conversation:** "Based on the uploaded call topic, draft a 500-word excellence section outline identifying 3 key objectives and their alignment with the call expected outcomes."

Show how every new conversation in this Project inherits the instructions and files.

**Team Exercise 2.1: "Build Your Domain Project" (45 min)**
Each team builds a Claude Project tailored to their research management domain:

| Team | Project Name | Key Instructions | Reference Files to Upload |
|------|-------------|-----------------|--------------------------|
| A | Grant Lifecycle Hub | Grant writing style, call analysis, budget rules | Sample call text, budget template |
| B | Compliance Advisor | Ethics review language, regulatory frameworks | Ethics checklist, GDPR template |
| C | Reporting Workspace | EU reporting standards, impact metrics | Sample periodic report, KPI framework |
| D | Comms & Dissemination | Institutional voice, audience adaptation | Brand guidelines, press release template |
| E | Data Management Office | FAIR principles, DMP standards, repository knowledge | DMP template, funder data policies |

Each team:
1. Writes custom instructions (use ChatGPT meta-prompting to help draft them)
2. Uploads 2-3 real or sample reference files
3. Runs 3 test conversations to verify the Project works as intended
4. Iterates on the instructions based on output quality

**Share-Out (20 min)**
Each team demos their Project: shows the instructions, runs one query, and explains what they'd change.

---

### BREAK (11:00 - 11:15)

---

### MODULE 2.3 | NotebookLM -- Document Analysis & Knowledge Synthesis (11:15 - 12:30)

**Core Concept:** NotebookLM as a source-grounded research assistant for working through long, complex documents that are core to research management.

**Demo (20 min): Analyzing a Funding Call with NotebookLM**
1. Create a new NotebookLM notebook
2. Upload sources: a Horizon Europe call topic (PDF), the relevant work programme section, and the HE Programme Guide (relevant chapter)
3. Demonstrate:
   - Auto-generated summary and key topics
   - Asking questions grounded in the sources: "What are the mandatory deliverables mentioned across all sources?", "What are the TRL expectations?"
   - The citation pinning feature (click to see exactly where the answer comes from)
   - Generating an Audio Overview (podcast-style summary) for team review
   - Creating a structured briefing note from the sources

**Team Exercise 2.2: "Deep Document Dive" (40 min)**
Each team creates a NotebookLM notebook with documents relevant to their domain:

| Team | Sources to Upload | Key Analysis Tasks |
|------|------------------|--------------------|
| A | Call text + work programme + Programme Guide | Extract eligibility criteria, expected outcomes, evaluation weights |
| B | Ethics guidelines + institutional policy + GDPR regulation excerpt | Map compliance requirements, identify gaps between institutional and funder rules |
| C | 2 periodic reports + project description | Cross-reference achievements vs. planned deliverables, flag delays |
| D | 3 project summaries + dissemination plan template | Identify common impact narratives, extract reusable communication angles |
| E | Data policy (funder) + institutional DMP policy + FAIR guidelines | Compare requirements across sources, build a consolidated checklist |

Each team:
1. Uploads sources and reviews auto-generated summaries
2. Asks 5 targeted questions and evaluates source grounding
3. Generates one structured output (briefing note, checklist, or comparison table)
4. Generates an Audio Overview and listens to it during break (optional)

**Debrief (15 min)**
- When to use NotebookLM vs. Claude Projects vs. Perplexity
- Key insight: NotebookLM is grounded in YOUR sources (no hallucination from external data), Claude Projects are more flexible and creative, Perplexity searches the live web

---

### LUNCH (12:30 - 13:30)

---

### MODULE 2.4 | Long-Context Work with Google Gemini (13:30 - 14:30)

**Core Concept:** Using Gemini's large context window for tasks that require processing very long documents or multiple documents simultaneously.

**Demo (15 min): Processing a Full Grant Agreement**
1. Upload a complete Model Grant Agreement (100+ pages) to Google Gemini
2. Demonstrate queries that require understanding across the full document:
   - "Summarize all financial reporting obligations and their deadlines"
   - "List all articles that mention consortium obligations and create a responsibility matrix"
   - "Compare the reporting requirements in Article 20 with the deliverable schedule in Annex 1"
3. Show Gemini's strengths: handling very long inputs, structured extraction from large documents

**Team Exercise 2.3: "The Long Document Challenge" (30 min)**
Each team uploads their longest, most complex document to Gemini and performs:
1. A full-document summary with structured output
2. A cross-section extraction task (pulling related information from different parts)
3. A comparison with how Claude or NotebookLM handled similar queries

Document the strengths and limitations in their Obsidian tool notes.

**Discussion (15 min)**
- Practical limits: when is a document too long even for Gemini?
- Strategy: chunking vs. full upload vs. using NotebookLM for multi-source synthesis

---

### MODULE 2.5 | Research Discovery with Perplexity AI (14:30 - 15:15)

**Core Concept:** Using Perplexity for research-grounded, citation-backed information discovery relevant to research management.

**Demo (10 min): Research Management Intelligence Gathering**
Demonstrate Perplexity for tasks where you need verified, current information:
- "What are the success rates for ERC Starting Grants in 2024 and 2025 by domain?"
- "What changes were introduced in the Horizon Europe 2025 work programme for Cluster 6?"
- "Compare the open access policies of Horizon Europe, NSF, and NIH as of 2025"

Highlight: every claim is cited, sources can be verified, and follow-up questions refine the search.

**Cross-Reference with the Horizon Dashboard (5 min)**
Open the Horizon Dashboard and pull the same success rate data that Perplexity cited. Compare side by side:
- Does Perplexity's number match the official Dashboard data?
- Is the Dashboard more current, or does Perplexity find more recent analysis?
- Show how to export Dashboard CSV data for further analysis in AI tools

Key insight: the Horizon Dashboard is the authoritative source for EU funding statistics. Use Perplexity for narrative context, trends, and non-EU comparisons; use the Dashboard for official numbers. When they disagree, trust the Dashboard.

**Team Exercise 2.4: "Intelligence Briefing" (25 min)**
Each team uses Perplexity to research a current topic in their domain and produces a 1-page intelligence briefing with citations:

| Team | Research Question |
|------|------------------|
| A | What are the latest trends in EU funding success rates and common proposal weaknesses? (Cross-reference Perplexity findings with Horizon Dashboard statistics; export Dashboard CSV data and upload to Claude for trend analysis) |
| B | What are the newest EU regulations affecting research ethics and data protection in 2025-2026? |
| C | What frameworks are European universities using to measure research impact beyond publications? |
| D | What are the best practices for research communication and public engagement in EU projects? |
| E | What are the latest developments in FAIR data implementation and open science mandates? |

Output: a structured briefing note saved in Obsidian.

---

### BREAK (15:15 - 15:30)

---

### MODULE 2.6 | Obsidian as a Knowledge Management Hub (15:30 - 16:30)

**Core Concept:** Connecting all AI outputs into a structured, searchable, linked knowledge base using Obsidian.

**Demo (20 min): The Connected Knowledge Base**
Show a mature Obsidian vault for research management:
1. **Linking:** A note on "Horizon Europe Budget Rules" links to [[Grant Writing Prompts]], [[Budget Template]], and [[Compliance Checklist]]
2. **Templates plugin:** Create a template for "AI Session Log" with fields: Date, Tool Used, Task, Prompt, Output Quality (1-5), Key Learnings, Follow-up Actions
3. **Dataview plugin:** A dashboard note that auto-lists all prompts rated 4+ across the vault
4. **Kanban plugin:** A board tracking workflow development progress
5. **Graph View:** Visualize how knowledge connects across documents, tools, and workflows

**Team Exercise 2.5: "Vault Architecture" (30 min)**
Each team:
1. Transfers all Day 1 and Day 2 outputs into their Obsidian vault (prompts, briefings, comparison matrices)
2. Creates internal links between related notes
3. Sets up the "AI Session Log" template and retroactively logs 3 sessions from today
4. Creates a Kanban board for their Day 3 team project workflow
5. Explores Graph View to see connections emerging

**Share-Out (10 min)**
Quick screen-shares of each team's vault structure and graph view.

---

### MODULE 2.7 | Day 2 Wrap-Up & Day 3 Preview (16:30 - 17:00)

**Day 3 Team Project Briefing (20 min)**
Announce the Day 3 capstone project. Each team will build a complete, documented AI-assisted workflow for their domain that:
1. Chains at least 3 different AI tools in a defined sequence
2. Includes reusable prompts saved in their prompt library
3. Produces a tangible output artifact
4. Is documented as a repeatable workflow in Obsidian
5. Includes a visual summary created in Canva

Teams spend the remaining time planning their approach, assigning roles, and identifying which tools and prompts they will use.

**Day 2 Reflection (10 min)**
Each participant writes `/05-Daily-Reflections/Day2.md` in Obsidian.

---

### Day 2 Deliverables Checklist
- [ ] Claude Project built and tested for team domain
- [ ] NotebookLM notebook with analyzed documents and structured output
- [ ] Long-context analysis completed in Gemini
- [ ] Perplexity intelligence briefing with citations saved in Obsidian
- [ ] Obsidian vault populated with linked notes, session logs, and Kanban board
- [ ] Day 3 project plan drafted

---
---

# DAY 3: Integration & Workflow
## Level 4 "The Workflow Weaver"

**Goal:** Weave multiple AI tools into coherent, repeatable workflows for research management. Build and present a team capstone project. Leave with transferable workflow assets.

---

### MODULE 3.1 | Level 4 Introduction & Workflow Design (09:00 - 09:45)

**Level 4 Framing (15 min)**
- The shift: from "what can this tool do?" to "what's the best tool for THIS step?"
- Introduce the concept of an AI Workflow Chain: a sequence where the output of one tool becomes the input of the next
- Example workflow chain:

```
RESEARCH MANAGEMENT WORKFLOW: "New Call Assessment & Response"

Step 1: [Horizon Dashboard] Pull official success rates, funding
        statistics, and country participation data for the relevant
        cluster/call topic; export CSV for analysis
Step 2: [Perplexity] Research the call topic landscape, competing
        projects, and evaluator feedback trends
Step 3: [Claude Project] Upload Dashboard CSV export, ask Claude to
        analyze success patterns and identify strategic positioning
Step 4: [NotebookLM] Upload call text + work programme, extract
        requirements and evaluation criteria
Step 5: [Gemini] Upload full programme guide + call text, cross-reference
        eligibility and financial rules
Step 6: [Claude Project] Synthesize all previous outputs into a
        go/no-go assessment memo with data-backed justification
Step 7: [Canva AI] Create a visual one-pager summarizing the opportunity
        for internal stakeholders
Step 8: [Obsidian] Document the complete workflow, save all prompts,
        link all outputs
```

**Workflow Design Framework (15 min)**
Present a simple framework for designing AI workflows:
1. **Trigger:** What initiates this workflow? (e.g., "New Horizon Europe call published")
2. **Steps:** What needs to happen, in what order?
3. **Tool selection:** Which AI tool is best for each step and why?
4. **Handoff points:** How does output from one tool become input for the next?
5. **Quality gates:** Where does a human review before proceeding?
6. **Output:** What is the final deliverable?
7. **Storage:** Where is everything saved for reuse?

**Team Planning Session (15 min)**
Teams finalize their Day 3 project workflow design using this framework.

---

### MODULE 3.2 | Canva AI for Visual Outputs (09:45 - 10:30)

**Core Concept:** Creating professional visual deliverables that research managers actually need: one-pagers, infographics, presentation slides, and visual summaries.

**Demo (15 min): From AI Text to Visual Asset**
1. Take a Claude-generated project summary and paste it into Canva
2. Use Canva's Magic Design to generate a one-pager layout
3. Show Canva AI features: text-to-image for illustrations, Magic Write for copy refinement, bulk create for variations
4. Build a simple 3-slide presentation: project overview, timeline, team/budget

**Team Exercise 3.1: "Visual Communication" (30 min)**
Each team creates ONE visual asset relevant to their domain using Canva AI:

| Team | Visual Deliverable |
|------|-------------------|
| A | A one-page "Call Opportunity Brief" for internal circulation |
| B | An infographic mapping the ethics review process |
| C | A visual dashboard mockup showing project KPIs and status |
| D | A social media card set (3 cards) for a research project announcement |
| E | A visual checklist poster for FAIR data compliance |

Use AI-generated text from their Claude Project as the content source.

---

### BREAK (10:30 - 10:45)

---

### MODULE 3.3 | Claude Artifacts for Rapid Prototyping (10:45 - 11:45)

**Core Concept:** Using Claude's Artifacts feature to build interactive, functional tools with zero coding experience.

**Demo (20 min): Building a Research Management Tool**
Live in Claude Desktop, create an Artifact:
- "Build me an interactive grant proposal readiness checklist. It should have sections for: administrative requirements, consortium, scientific excellence, impact, and implementation. Each item should be checkable with a progress bar at the top. Include a section where I can add notes per item. Make it visually clean and professional."
- Show iterations: "Add a color-coded risk indicator per section", "Add an export-to-text button"
- Key message: you just described what you wanted in plain language and got a functional tool

**Team Exercise 3.2: "Build Your Tool" (40 min)**
Each team describes and builds ONE interactive Artifact in Claude:

| Team | Artifact to Build |
|------|------------------|
| A | A proposal budget calculator with cost categories, overhead rates, and partner allocation |
| B | An ethics screening questionnaire that recommends the type of review needed based on answers |
| C | A project milestone tracker with status indicators and deadline warnings |
| D | A dissemination activity planner with audience, channel, and timeline fields |
| E | A data management plan builder that asks questions and generates DMP sections |

Workflow:
1. Describe the tool to Claude (use ICC structure)
2. Test the first version
3. Request 2-3 iterations/improvements
4. Save the final Artifact
5. Document the creation process in Obsidian (prompts used, iterations needed)

---

### MODULE 3.4 | Capstone Project Work Session (11:45 - 12:30 + 13:30 - 15:00)

**The Capstone Brief**

Each team builds and documents a complete multi-tool AI workflow for a realistic research management scenario. The workflow must demonstrate Level 4 competency: weaving multiple specialized tools together into a coherent, repeatable process.

**Scenario Assignments:**

**Team A -- Grant Lifecycle Management:**
*"A new Horizon Europe call has been published in your cluster. Walk through the complete workflow from call discovery to internal go/no-go decision to proposal outline."*
- Horizon Dashboard: pull official success rates, country participation stats, and funding data for the relevant cluster; export CSV
- Perplexity: landscape research, competing projects, evaluator feedback trends
- Claude Project: upload Dashboard CSV export, analyze success patterns, draft go/no-go memo + proposal outline with data-backed justification
- NotebookLM: call document analysis
- Canva: visual opportunity brief for leadership (include Dashboard statistics)
- Artifact: interactive eligibility/readiness checklist
- Obsidian: full workflow documentation

**Team B -- Research Compliance & Ethics:**
*"A new project involving human participants, AI systems, and cross-border data transfer has been approved. Build the complete compliance assessment and documentation package."*
- Perplexity: current regulatory landscape research
- NotebookLM: policy document analysis (GDPR, AI Act, ethics guidelines)
- Claude Project: compliance assessment report + documentation templates
- Canva: ethics review process infographic
- Artifact: interactive ethics screening tool
- Obsidian: full workflow documentation

**Team C -- Research Reporting & Impact Assessment:**
*"An EU-funded project is approaching its 18-month periodic report deadline. Build the workflow for assembling, drafting, and quality-checking the report."*
- Perplexity: benchmarking against similar projects' reported impacts
- NotebookLM: analysis of project DoA and previous reports
- Gemini: cross-reference long MGA with reporting requirements
- Claude Project: draft report sections + quality review
- Canva: visual KPI dashboard
- Obsidian: full workflow documentation

**Team D -- Stakeholder Communication & Dissemination:**
*"A major research project has produced breakthrough results. Build the communication workflow from scientific output to public-facing content across multiple channels."*
- NotebookLM: analysis of the scientific publication/deliverable
- Claude Project: adapted content for different audiences (press, policy, public, social media)
- ChatGPT Canvas: draft a blog post with editorial refinement
- Canva: social media cards + one-page policy brief layout
- Perplexity: identify relevant media contacts and communication channels
- Obsidian: full workflow documentation

**Team E -- Research Data Management & Open Science:**
*"A new research consortium needs a comprehensive data management plan that satisfies funder requirements, FAIR principles, and institutional policy. Build the complete DMP workflow."*
- Perplexity: latest FAIR implementation standards and repository options
- NotebookLM: cross-analysis of funder data policy + institutional policy
- Claude Project: DMP section drafting with policy-aligned language
- Gemini: process the full funder data policy document for specific requirements
- Artifact: interactive DMP builder tool
- Obsidian: full workflow documentation

**Work Session Rules:**
- Each team member must lead on at least one tool
- Human quality gates must be explicitly marked in the workflow
- Every prompt used must be saved in the Obsidian prompt library
- The workflow must be documented well enough that a colleague NOT in the course could follow it

---

### LUNCH (12:30 - 13:30)
*(Teams continue capstone work 13:30 - 15:00)*

---

### BREAK (15:00 - 15:15)

---

### MODULE 3.5 | Capstone Presentations (15:15 - 16:30)

**Presentation Format: 12 min per team + 3 min Q&A**

Each team presents:
1. **The Scenario** (1 min): What research management challenge they addressed
2. **The Workflow** (3 min): Step-by-step walk-through of their multi-tool workflow, showing tool selection rationale and handoff points
3. **Live Demo** (5 min): Execute at least 2 steps of the workflow live, showing real outputs
4. **The Artifact** (2 min): Demo the interactive tool they built
5. **Lessons Learned** (1 min): What worked, what surprised them, what they would do differently

**Peer Evaluation:**
Other teams rate each presentation on:
- Workflow completeness and logic
- Tool selection appropriateness
- Output quality
- Reusability and documentation quality
- Creativity

---

### MODULE 3.6 | Course Wrap-Up & Forward Path (16:30 - 17:00)

**Synthesis (15 min)**
- Revisit the 7 Levels framework: where participants started vs. where they are now
- Preview of Levels 5-7 for self-directed exploration (automation with Zapier, building with Lovable/AI Studio, agentic systems)
- Key principles to carry forward:
  1. Always ask: "What is the best tool for THIS step?"
  2. Save every good prompt -- your prompt library is your most valuable AI asset
  3. Document workflows so they are repeatable and shareable
  4. Keep the human in the loop at quality gates
  5. Update your knowledge base continuously in Obsidian

**Resource Distribution (10 min)**
- Share a curated reading list and resource document
- Provide a "Level 5 Self-Study Path" for interested participants
- Share links to AI communities for research managers

**Final Reflection & Feedback (5 min)**
- Each participant writes `/05-Daily-Reflections/Day3-Final.md` in Obsidian
- Complete the course evaluation form

---

### Day 3 Deliverables Checklist
- [ ] Canva visual asset created for team domain
- [ ] Interactive Claude Artifact built and tested
- [ ] Complete multi-tool workflow executed and documented
- [ ] Capstone presentation delivered
- [ ] All prompts saved in Obsidian prompt library
- [ ] Workflow documented in Obsidian with linked notes

---
---

# Final Deliverables Summary (Per Team)

Each team leaves the course with the following transferable assets:

| Deliverable | Format | Location |
|------------|--------|----------|
| **Prompt Library** | 10+ refined, tested prompts for their domain | Obsidian `/00-Prompts/` |
| **Claude Project** | Configured workspace with custom instructions + reference files | Claude Desktop |
| **NotebookLM Notebook** | Source-grounded research workspace with analyzed documents | NotebookLM |
| **Intelligence Briefing** | Citation-backed research briefing for their domain | Obsidian `/04-Team-Project/` |
| **AI Tool Comparison Matrix** | Evaluation of tools for specific task types | Obsidian `/02-Tool-Notes/` |
| **Interactive Artifact** | Functional prototype tool for their domain | Claude Artifact (shareable link) |
| **Visual Asset** | Professional one-pager, infographic, or presentation | Canva (shareable/downloadable) |
| **Documented Workflow** | Complete multi-tool workflow with steps, tools, prompts, quality gates | Obsidian `/03-Workflows/` |
| **Obsidian Knowledge Vault** | Linked, searchable knowledge base with all course outputs | Local Obsidian vault |
| **Session Logs** | Documented AI interactions with quality ratings and learnings | Obsidian `/templates/` |
| **Reflections** | 3 daily reflection notes capturing learning progression | Obsidian `/05-Daily-Reflections/` |

---

# Appendix A: Timing Overview

| Block | Day 1 | Day 2 | Day 3 |
|-------|-------|-------|-------|
| 09:00-09:30 | Opening & Orientation | Recap & Level 3 Intro | Level 4 Intro & Workflow Design |
| 09:30-10:00 | Orientation (cont.) | Claude Projects Demo | Workflow Design (cont.) |
| 10:00-11:00 | Level 1: The Question Asker | Claude Projects Exercise | Canva AI Workshop |
| 11:15-12:30 | Level 2: Prompt Structure (ICC) | NotebookLM Workshop | Artifacts Workshop |
| 13:30-15:00 | Level 2: Meta-Prompting & Iteration | Gemini + Perplexity | Capstone Work Session |
| 15:15-16:15 | Tool Comparison Exercise | Obsidian Deep Dive | Capstone Presentations |
| 16:15-17:00 | Obsidian Setup + Day 1 Wrap | Day 2 Wrap + Day 3 Brief | Synthesis + Wrap-Up |

## Level Progression Arc

```
Day 1 AM   -->  Level 1: "I ask AI questions"
Day 1 PM   -->  Level 2: "I craft prompts that get consistently good results"
Day 2 AM   -->  Level 3: "I have AI workspaces with persistent context"
Day 2 PM   -->  Level 3: "I use specialized tools for specialized tasks"
Day 3 AM   -->  Level 4: "I chain tools into workflows"
Day 3 PM   -->  Level 4: "I build, document, and present complete AI workflows"
```

---

# Appendix B: Infrastructure Checklist

### Venue Requirements
- Stable Wi-Fi for 15+ simultaneous AI tool users
- Each participant needs a laptop with a modern browser
- Projector/screen for instructor demos and team presentations
- Power strips at every table (5 team tables)

### Account Setup (Pre-Course)
| Tool | Account Type | Setup Notes |
|------|-------------|-------------|
| Claude.ai | Free (or Pro if budget allows) | Cowork for team collaboration |
| ChatGPT | Free | Canvas feature available on free tier |
| NotebookLM | Free (Google account) | notebooklm.google.com |
| Perplexity AI | Free | perplexity.ai |
| Google Gemini | Free (Google account) | gemini.google.com |
| Canva | Free (education account preferred) | canva.com |
| Horizon Dashboard | Free (no account needed) | dashboard.tech.ec.europa.eu |
| Obsidian | Free | Download + install pre-course |

### Instructor Materials to Prepare
- Sample documents per team domain (call texts, reports, policies, templates)
- Obsidian vault template (ZIP file for distribution)
- Scenario Bank document with detailed capstone briefs
- Evaluation forms (daily + final)
- Resource and reading list document
- Certificate of completion template (optional)

---

# Appendix C: Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Free-tier rate limits during class | Stagger exercises; have backup prompts ready; teams work sequentially not simultaneously on same tool |
| Participant falls behind | Team-of-3 structure provides peer support; exercises have minimum + stretch goals |
| Wi-Fi instability | Have mobile hotspot as backup; some exercises can be done offline in Obsidian |
| Tool interface changes | Brief instructor check 1 week before course; prepare screenshots of current UI |
| Participants bring sensitive documents | Emphasize anonymization in pre-course instructions; provide sample documents as alternatives |
| Uneven team skill levels | Mix experienced and novice users; rotating team roles ensure everyone practices |
| Claude Cowork availability | Fall back to individual Claude Projects + screen sharing for collaboration |

# Facilitator Guide -- Day 3: Integration & Workflow
## Level 4 "The Workflow Weaver"

---

# Pre-Day Checklist

- [ ] Day 2 debrief notes reviewed -- know each team's readiness level
- [ ] Canva demo prepared: a Copilot-generated project summary text ready to paste into Canva, plus a pre-designed one-pager for the "after" comparison
- [ ] Copilot agent demo tested: the Grant Proposal Readiness Checker agent ready to build live
- [ ] Peer evaluation form set up in Microsoft Forms (link ready to share in Teams -- one submission per other team)
- [ ] Presentation timer ready (12 min presentation + 3 min Q&A)
- [ ] Order of team presentations decided (post in the Teams chat)
- [ ] "Level 5 Self-Study Path" handout link ready to share in Teams
- [ ] Final course evaluation form ready as a digital link (Microsoft Forms)
- [ ] Resource and reading list document finalized
- [ ] Celebration element ready if desired (certificates, team recognition, etc.)
- [ ] Extra sample documents available per team in case they need additional inputs for the capstone
- [ ] Ensure all teams' Kanban boards in Obsidian have tasks populated from yesterday's planning

---

# MODULE 3.1 | Level 4 Introduction & Workflow Design
**Time: 09:00 - 09:45 (45 min)**

## Learning Objectives
- Participants understand the Level 4 mindset shift: from tools to workflows
- Participants can apply the Workflow Design Framework (Trigger, Steps, Tools, Handoffs, Quality Gates, Output, Storage)
- Teams have a finalized, detailed plan for their capstone project

---

## Segment 1: Level 4 Framing (09:00 - 09:15, 15 min)

### Setup
- A shared whiteboard or screen share with the workflow chain visual
- Fresh energy -- this is the culmination day

### Facilitation Script

**Opening (3 min):**
> "Day 3. You've covered a lot of ground. Day 1, you went from asking AI random questions to crafting structured, reusable prompts. Day 2, you built persistent workspaces, analyzed documents with specialized tools, and connected everything in a knowledge base."

> "Today you become Level 4 -- the Workflow Weaver. Here's the mindset shift:"

Write on the shared whiteboard:
```
Level 3 thinks: "What can this tool do?"
Level 4 thinks: "What's the best tool for THIS step?"
```

> "At Level 3, you know the tools individually. At Level 4, you chain them together. The output of one tool becomes the input of the next. That's a workflow."

**Example workflow chain (7 min):**

Draw or display the workflow chain:
```
WORKFLOW: "New Call Assessment & Response"

Step 1: [Horizon Dashboard] Pull official success rates, funding
        data, and country participation stats for the relevant
        cluster; export CSV
        --> OUTPUT: Official statistics CSV + key numbers noted

Step 2: [Perplexity] Research competing projects, evaluator
        feedback trends, landscape analysis
        --> OUTPUT: Intelligence briefing with citations

Step 3: [Copilot Notebook] Upload Dashboard CSV, ask for trend
        analysis and strategic positioning insights
        --> OUTPUT: Data-backed competitive analysis

Step 4: [NotebookLM] Upload call text + work programme,
        extract requirements and evaluation criteria
        --> OUTPUT: Requirements checklist with source citations

Step 5: [Gemini] Upload full programme guide + call text,
        cross-reference eligibility and financial rules
        --> OUTPUT: Financial rules summary

Step 6: [Copilot Notebook] Synthesize all previous outputs into
        a go/no-go assessment memo with data-backed justification
        --> OUTPUT: Decision memo

    *** HUMAN QUALITY GATE: Research Director reviews memo ***

Step 7: [Copilot Notebook] Draft proposal outline aligned
        to evaluation criteria
        --> OUTPUT: Proposal skeleton

Step 8: [Canva AI] Create visual one-pager for stakeholders,
        including Dashboard statistics
        --> OUTPUT: Opportunity brief PDF

Step 9: [Obsidian] Document complete workflow, save prompts,
        link all outputs
        --> OUTPUT: Reusable workflow documentation
```

Walk through it step by step:
> "Step 1 uses the Horizon Dashboard -- not an AI tool, but an official EU data source. I pull real success rates, funding distribution, and participation statistics. This is the ground truth. I export it as CSV so I can feed it into AI tools in the next steps."

> "Step 2 uses Perplexity because I need narrative context that the Dashboard doesn't provide -- competing projects, evaluator feedback trends, landscape commentary. Perplexity cites its sources, so I can verify."

> "Step 3 uses my Copilot Notebook. I upload the Dashboard CSV and ask Copilot to analyze the trends -- which topics are most competitive, whether success rates are rising or falling, how our country compares. Copilot turns raw data into strategic insights."

> "Step 4 uses NotebookLM because I need to analyze specific call documents with traceable citations -- not general knowledge."

> "Step 5 uses Gemini because the Programme Guide is 200+ pages and I need to cross-reference it with the call text."

> "Step 6 uses my Copilot Notebook again to synthesize ALL of the previous outputs into a single go/no-go memo. Notice: it has official data from the Dashboard, narrative context from Perplexity, document analysis from NotebookLM, and financial rules from Gemini. That's four different sources feeding one decision document."

> "Between Step 6 and Step 7, there's a human quality gate. A person -- the Research Director -- reviews the memo before I proceed. The AI doesn't make the decision. The human does."

> "Step 8 uses Canva because I need a visual deliverable to share with leadership -- and I can embed the Dashboard statistics to make it data-driven."

> "Step 9 uses Obsidian because everything needs to be documented, linked, and reusable."

**Key point (2 min):**
> "Notice that I'm not using one tool for everything. Each tool does what it's best at. And the handoff points are explicit -- the output of Step 1 becomes input for Step 4. This is workflow thinking."

**The human quality gate principle (3 min):**
> "One more critical concept. In every workflow, there must be at least one human quality gate -- a point where a human reviews, evaluates, and decides before the workflow proceeds. AI generates. Humans validate. This is non-negotiable in research management, where accuracy and compliance matter."

> "In your capstone projects today, you must explicitly mark where the human quality gates are. Not as an afterthought -- as a designed feature of the workflow."

---

## Segment 2: Workflow Design Framework (09:15 - 09:30, 15 min)

### Facilitation Script

> "Here's the framework you'll use to design your capstone workflow."

Display or write:

```
WORKFLOW DESIGN FRAMEWORK

1. TRIGGER: What initiates this workflow?
   Example: "New Horizon Europe call published in our cluster"

2. STEPS: What needs to happen, in what order?
   List each step with its purpose

3. TOOL SELECTION: Which AI tool for each step, and why?
   Justify each choice based on the tool's strengths

4. HANDOFF POINTS: How does output move between tools?
   What gets copied, pasted, uploaded, or referenced?

5. QUALITY GATES: Where does a human review?
   What are they checking? Who is the reviewer?

6. OUTPUT: What is the final deliverable?
   Who receives it? In what format?

7. STORAGE: Where is everything saved for reuse?
   Obsidian locations, Copilot Notebook, file naming conventions
```

> "Let me show you how this works with a concrete example."

Fill in the framework quickly for a simple workflow (not the full example above -- something smaller):

```
TRIGGER: PI asks for help deciding whether to apply to a specific call

STEPS:
1. Pull official statistics from Horizon Dashboard
2. Research the call landscape and trends
3. Analyze the call document
4. Draft a go/no-go recommendation

TOOLS:
1. Horizon Dashboard (need authoritative success rates and participation data)
2. Perplexity (need narrative context, competing projects, evaluator insights)
3. NotebookLM (need source-grounded document analysis)
4. Copilot Notebook (need to synthesize and write)

HANDOFFS:
- Dashboard CSV export --> upload to Copilot Notebook for trend analysis
- Perplexity findings --> paste as context into Copilot Notebook
- NotebookLM requirements checklist --> paste as context into Copilot Notebook

QUALITY GATE:
- After Step 4: Research Manager reviews recommendation before
  sending to PI

OUTPUT: 1-page go/no-go memo with data-backed justification (Word/PDF)
STORAGE: Obsidian /03-Workflows/ + Copilot Notebook conversation
```

> "Simple, clear, repeatable. Anyone in your office could follow this."

---

## Segment 3: Team Planning Session (09:30 - 09:45, 15 min)

### Instructions to Give (3 min)

> "Take out your capstone scenario brief from yesterday. Using the Workflow Design Framework, fill in all 7 components for your specific scenario. Write this in your Obsidian vault at /03-Workflows/Capstone-Workflow-Design.md"

> "You have 12 minutes. By the end of this session, I want to see a completed workflow design from each team. I'll come around to check."

### During Planning (12 min)

**Drop into each breakout room. Check for:**

| Check | What to Look For | If Missing |
|-------|-----------------|------------|
| Trigger clearly defined? | Should be specific and realistic | "What event in real life would start this process?" |
| At least 3 tools in sequence? | Each tool should have a clear reason | "Can you justify why [tool X] and not [tool Y] for this step?" |
| Handoffs explicit? | Should say exactly what moves between tools | "When Step 2 ends, what exactly do you copy into Step 3?" |
| At least 1 human quality gate? | Must have a specific review point with a named reviewer role | "Where does a human decide whether to proceed?" |
| Final output defined? | Should be a concrete deliverable | "What does the person who triggered this workflow receive at the end?" |
| Obsidian storage planned? | Each output should have a vault location | "Where will you save the prompts, the outputs, the workflow documentation?" |

**Common issues:**

Teams trying to use too many tools:
> "You don't need to use every tool we learned. Use the ones that make sense for your scenario. Three tools, well-chained, is better than six tools loosely connected."

Teams not sure about handoff mechanics:
> "It's usually copy-paste. Take the key output from NotebookLM -- the requirements checklist -- select it, copy it, and paste it into your Copilot Notebook conversation as context. 'Based on the following requirements extracted from the call document: [paste]'. That's a handoff."

Teams skipping quality gates:
> "Where in this workflow would you normally want a senior colleague to check your work? That's your quality gate. Add it explicitly."

### Timing Checkpoint
At 09:45, check that all teams have at least a draft workflow design. If a team is behind, they can refine during the capstone work session.

---

# MODULE 3.2 | Canva AI for Visual Outputs
**Time: 09:45 - 10:30 (45 min)**

## Learning Objectives
- Participants can use Canva AI to transform AI-generated text into professional visual deliverables
- Participants experience the text-to-visual workflow (Copilot output --> Canva design)
- Each team creates one visual asset for their capstone project

---

## Segment 1: Demo -- From AI Text to Visual Asset (09:45 - 10:00, 15 min)

### Setup
- Canva open (canva.com), logged in
- A Copilot-generated project summary text ready to paste (prepare this: a well-written 200-word project summary)
- Know your way around Canva's current interface (test the day before -- Canva updates frequently)

### Facilitation Script

**Why visual outputs matter (2 min):**
> "Research managers constantly need to communicate complex information to non-specialists: university leadership, PIs, project partners, the public. A wall of text rarely works. A well-designed one-pager, infographic, or presentation slide set does."

> "Canva AI lets you take the text you've generated with Copilot and turn it into professional visuals in minutes. You don't need design skills."

**Demo: Building a one-pager (13 min)**

**Step 1 (3 min): Start with AI text**
Show the Copilot-generated project summary you prepared:
> "I drafted this project summary in my Copilot Notebook. It's good text, but it's just text. Let me turn it into something I'd actually share with my Vice-Rector."

**Step 2 (4 min): Canva Magic Design**
Open Canva. Click "Create a design" or "Magic Design."
> "I can describe what I want, or I can paste my text and let Canva suggest layouts."

Either:
- Use Magic Design: describe "Create a one-page project opportunity brief for internal stakeholders at a university" and let Canva generate options
- Or: choose a template (search "one pager" or "project brief") and customize

Select a layout. Paste sections of the Copilot text into the text boxes.

> "The key move here: don't paste a wall of text. Break it into sections -- headline, key facts, description, next steps. Canva works best with short, punchy text blocks."

**Step 3 (3 min): Canva AI features**
Demonstrate 2-3 AI features:
- **Magic Write:** Select a text box, use Magic Write to rephrase or shorten text for a visual format
- **Magic Design suggestions:** Show how Canva suggests alternative layouts
- **Image search or generation:** If the design needs a visual element, show how to search Canva's library or generate one

**Step 4 (3 min): Quick presentation slides**
> "Same principle for presentations."

Quickly show: create a presentation, add 3 slides (project overview, timeline, team), use Magic Design to style them.

> "Three slides, five minutes. From Copilot text to a presentable deck."

### Facilitator Notes
- Don't get bogged down in design details. The point is the WORKFLOW: Copilot generates content --> Canva makes it visual.
- Canva's interface changes frequently. If a feature has moved, acknowledge it: "The feature might be in a slightly different place on your screen."
- Free tier Canva has limitations (some templates are Pro-only). Focus on features available to free users.

---

## Segment 2: Team Exercise 3.1 -- "Visual Communication" (10:00 - 10:30, 30 min)

### Instructions to Give (3 min)

> "Each team: create ONE visual asset for your capstone project using Canva."

Display:

| Team | Visual Deliverable |
|------|-------------------|
| A | A one-page "Call Opportunity Brief" for internal circulation |
| B | An infographic mapping the ethics review process |
| C | A visual dashboard mockup showing project KPIs and status |
| D | A social media card set (3 cards) for a research project announcement |
| E | A visual checklist poster for FAIR data compliance |

> "Workflow:"
```
1. GENERATE the text content in your Copilot Notebook (5 min)
   - Ask Copilot to draft the text specifically formatted for a
     visual one-pager: short headlines, bullet points, key figures

2. DESIGN in Canva (20 min)
   - Start with a template or Magic Design
   - Paste Copilot's text into the template
   - Customize colors, layout, images
   - Use Magic Write to refine text for visual format

3. EXPORT as PDF and save the Canva link (2 min)
```

> "Assign one person to drive Canva, one to generate text in Copilot, and one to provide feedback and quality control."

### During the Exercise (27 min)

**Breakout-room visits -- first round (0-10 min):**

**Common issues:**

Teams spending too long choosing a template:
> "Pick any template that's roughly right and customize it. Don't browse for 15 minutes. Choose one, start editing, you can always switch."

Teams pasting long paragraphs:
> "Visual communication means short text. Take your Copilot output and ask Copilot: 'Rewrite this as a visual one-pager. Use a headline (max 8 words), 3 key bullet points (max 15 words each), and 3 key figures or statistics.' Then paste THAT into Canva."

Teams confused by Canva's interface:
Quick walkthrough: "Click on any text box to edit it. Drag elements to reposition. Use the left panel to add elements, images, or text boxes."

**Breakout-room visits -- second round (10-25 min):**

Look for quality:
- Is the visual actually communicating the key information?
- Is there a clear hierarchy (headline, supporting points, details)?
- Would this be useful in a real work context?

Coaching:
> "Imagine your Vice-Rector sees this for 30 seconds between meetings. Would they understand the key message? If not, simplify."

For **Team D** (social media cards): "Each card should have ONE message, ONE image or visual, and ONE call to action. Three cards, three messages."

For **Team C** (dashboard mockup): "Think about what a project coordinator needs to see at a glance: are deliverables on track? What's the budget status? Any risks? Make those the visual focal points."

### Timing
At 10:25, announce: "Five minutes. Export your visual as PDF if you can, and save the Canva link."

---

# BREAK (10:30 - 10:45)

During break:
- Test the agent demo in Microsoft 365 Copilot (Agent Builder)
- Make sure you can demonstrate iterating on an agent
- Have your screen ready with Copilot open

---

# MODULE 3.3 | Copilot Agents: Build Your Own AI Tools
**Time: 10:45 - 11:45 (60 min)**

## Learning Objectives
- Participants understand that they can build interactive tools with zero coding skills using Microsoft 365 Copilot's Agent Builder
- Participants experience the build-test-iterate cycle for custom agents
- Each team has a working interactive tool prototype for their domain

---

## Segment 1: Demo -- Building a Research Management Tool (10:45 - 11:05, 20 min)

### Setup
- Microsoft 365 Copilot open, Agent Builder ready (Copilot --> Create agent)
- Your screen shared in the Teams meeting

### Facilitation Script

**Concept introduction (3 min):**
> "This is going to be fun. Microsoft 365 Copilot has a feature called Agent Builder. When you describe an assistant you want -- a tool, a calculator, a checklist, a screening questionnaire -- Copilot turns your plain-language description into a working, interactive agent that asks people questions and produces results. You don't need to know any code. You don't need to install anything. You just describe what you want -- and then you can share it with your colleagues."

> "Let me show you."

**Build Step 1 -- Create the agent (5 min):**

In Agent Builder, give the agent a name -- "Grant Proposal Readiness Checker" -- and write its instructions:
```
You are a grant proposal readiness assistant. Walk the user through a
grant proposal readiness checklist, one section at a time, covering:
- Administrative requirements (institution registered, PIC number, etc.)
- Consortium (minimum partners, geographic spread, etc.)
- Scientific excellence (state of the art, objectives, methodology)
- Impact (exploitation plan, dissemination, societal impact)
- Implementation (work packages, milestones, deliverables, management)

For each section, ask about each item, track what is complete versus
outstanding, and let me add notes per item. Finish with a readiness
summary and an overall completion percentage. Keep the tone professional
and clear.
```

Turn on the **"Create documents, charts, and code"** capability so the agent can calculate the completion percentage and produce an export-ready summary.

Open the **"Try it"** pane and run through a section or two:
> "Look at this. I described what I wanted in plain English, and I have a working tool. Let me test it."

Answer a few of the agent's questions. Show it tracking progress and reporting the completion percentage.

> "This is functional. I could use this right now in a real proposal preparation meeting -- and I can share it with the whole office."

**Build Step 2 -- Iteration (5 min):**

> "But I want to improve it. Watch how easy this is."

Refine the instructions:
```
Add a color-coded risk rating for each section:
- Green if more than 75% of items are complete
- Yellow if 50-75% are complete
- Red if less than 50% are complete

At the end, produce an export-ready summary of the whole checklist --
status and notes -- as formatted text I can copy and paste into a report.
```

Test the updated agent in the "Try it" pane.

> "Two sentences. The agent now has risk ratings and an export-ready summary. Let me test it."

Show the export-ready summary it produces.

**Build Step 3 -- The key message (4 min):**

> "Think about what just happened. I described a tool in maybe 60 words total, across two short instructions. In under two minutes, I have a working, interactive agent with risk ratings and an export-ready summary."

> "This is what Level 4 looks like. You're not just asking AI to write text. You're asking it to build tools. And you're doing it in plain language."

> "Now, is this a production-ready enterprise application? No. But is it a fully functional prototype that solves a real problem? Absolutely. And you can keep iterating -- adding features, refining its behavior, fixing issues -- just by describing what you want."

**Quick tips (3 min):**
> "Three tips for building agents:"

Write on the shared whiteboard:
```
1. Be specific about structure: what the agent asks, in what order
2. Be specific about behavior: what it should track, calculate,
   and produce
3. Iterate in small steps: one change at a time, test each one in
   "Try it" before adding the next
```

> "Don't try to describe a 20-feature tool in one prompt. Start simple. Get it working. Then add features one by one."

---

## Segment 2: Team Exercise 3.2 -- "Build Your Tool" (11:05 - 11:45, 40 min)

### Instructions to Give (5 min)

> "Each team builds ONE interactive agent for their domain."

Display:

| Team | Agent to Build |
|------|------------------|
| A | A proposal budget assistant that collects cost categories (personnel, travel, equipment, subcontracting, other), an overhead rate (25% flat or actual indirect), and partner allocations, then calculates the totals automatically and returns a structured budget breakdown. Enable "create documents, charts, and code" for the calculations. |
| B | An ethics screening agent that asks a series of yes/no questions about the project (human participants? personal data? dual use? international partners?) and, based on the answers, recommends the type of ethics review needed (exempt, expedited, full board). |
| C | A project milestone assistant that takes a list of milestones with due dates and responsible partners, then reports status (on track/delayed/at risk/completed) and flags approaching deadlines. |
| D | A dissemination activity planner that gathers activity type, target audience, channel, responsible partner, timeline, and status, then returns a structured plan you can sort by date or audience. |
| E | A data management plan builder that interviews the user about the project's data (types, volume, formats, storage, sharing plans) and generates funder-ready DMP section text. |

> "Workflow:"
```
1. DESCRIBE the agent in Agent Builder using ICC structure (5 min)
   - Instruction: what the agent should do and produce
   - Context: what it's for, who uses it, in what context
   - Constraints: what it asks, in what order, and its output format

2. TEST the first version in the "Try it" pane (5 min)
   - Answer its questions. Does it work?
   - What's missing? What doesn't make sense?

3. ITERATE 2-3 times (15 min)
   - Refine the instructions one change at a time
   - Test each iteration before making the next change

4. DOCUMENT in Obsidian (5 min)
   - Save the instructions used (initial + iterations)
   - Note what worked and what didn't
   - Save and share the agent
```

> "One person drives Agent Builder, one person tests the agent in 'Try it' and identifies issues, one person documents the instructions and the process in Obsidian. Rotate if time allows."

### During the Exercise (35 min)

**Breakout-room visits -- this is a high-energy module. Expect excitement and some frustration.**

**Common issues and solutions:**

**The agent isn't behaving as intended:**
> "If the agent skips questions or answers too generally, tighten its instructions. Spell out the exact questions to ask and the order: 'Ask about each section one at a time and wait for my answer before moving on.' Then test again in 'Try it'."

**The agent is too simple:**
> "That's fine for v1. Now iterate: 'Also ask about [X]' or 'Add a summary at the end.' Build it up gradually."

**The agent's output is wrong (e.g., calculations off):**
> "Tell Agent Builder exactly what's wrong: 'The total is calculating incorrectly -- it's adding overhead twice. Fix the calculation,' and make sure the 'Create documents, charts, and code' capability is turned on. Be specific about the problem."

**The agent's replies are hard to read:**
> "Behavior first, polish second. But if you want cleaner output: 'Format the summary with clear headings and bullet points, and keep it concise.'"

**Team-specific coaching:**

**Team A (Budget assistant):**
> "Make sure the overhead calculation is correct. Test with real numbers. Add to the instructions: 'Flag if any partner's personnel costs exceed 60% of their total budget.'"

**Team B (Ethics screening):**
> "The branching logic is key. If someone answers 'Yes' to 'Does the project involve children?', it should immediately flag 'Full board review required' without needing further questions. Think about the decision tree."

**Team C (Milestone assistant):**
> "Tell the agent to report status automatically: green for on-track, yellow for approaching deadline (within 30 days), red for overdue. That's the kind of behavior that makes this immediately useful."

**Team D (Dissemination planner):**
> "Tell the agent it should let the user filter: 'Show only activities targeting policymakers' or 'Show only activities scheduled for Q1.' Filtering makes it practical for planning meetings."

**Team E (DMP builder):**
> "The generated DMP text is the key output. Make sure it produces actual usable paragraphs, not just bullet points. Add to the instructions: 'The generated DMP sections should be in formal, funder-ready language suitable for submission as part of a Horizon Europe proposal.'"

**If a team finishes early:**
> "Try adding an export step: have the agent produce a clean, copy-paste-ready summary of everything. That makes the tool actually usable beyond the demo."

### Timing
At 11:40, announce: "Five minutes. Make sure your agent is in a working state. Save and share it, and document your instructions in Obsidian."

---

# MODULE 3.4 | Capstone Project Work Session
**Time: 11:45 - 12:30 + 13:30 - 15:00 (135 min total)**

## Learning Objectives
- Teams execute their complete multi-tool workflow from start to finish
- Teams produce all required deliverables (workflow documentation, visual, agent, prompt library)
- Teams prepare their 12-minute presentation

---

## Session Structure

This is a working session, not a lecture. Your role shifts to coach and timekeeper.

### Pre-Work Session Setup

Share the capstone requirements on screen (keep them shared the entire session):
```
CAPSTONE REQUIREMENTS CHECKLIST

[ ] Multi-tool workflow executed (minimum 3 tools chained)
[ ] Reusable prompts saved in Obsidian /00-Prompts/
[ ] At least 1 tangible output artifact (document, memo, briefing)
[ ] Canva visual asset created
[ ] Copilot agent (interactive tool) working
[ ] Workflow documented in Obsidian /03-Workflows/
[ ] Human quality gates marked in workflow documentation
[ ] Presentation prepared (12 min)

PRESENTATION STRUCTURE:
1. The Scenario (1 min)
2. The Workflow (3 min) -- step-by-step, tools, rationale
3. Live Demo (5 min) -- execute at least 2 steps live
4. The Agent Demo (2 min)
5. Lessons Learned (1 min)
```

### Managing the Work Session

**Phase 1: Execution (11:45 - 12:30, pre-lunch, 45 min)**

Focus: teams should be executing their workflow steps, not still planning.

**11:45 - 11:55: Check-in with each team (2 min per team)**
> "Show me your workflow design from this morning. Which step are you on? What do you need from me?"

Verify each team has started executing, not still debating approach. If a team is stuck on planning:
> "Your plan is good enough. Start executing Step 1 now. You can refine the plan as you go."

**11:55 - 12:30: Roaming support**

Drop into breakout rooms in rotation. Priority issues:

| Issue | Response |
|-------|----------|
| "We can't get [tool] to work" | Help troubleshoot. If the tool is down, suggest an alternative or skip that step and note it. |
| "The Perplexity/Copilot output isn't good enough" | "Is it good enough to move forward? You can come back and refine it later. Don't get stuck on perfection at one step." |
| "We don't know what to do for the handoff" | "Copy the key output from [Tool A]. Open [Tool B]. Paste it with the instruction: 'Based on the following [analysis/findings/requirements]: [paste].' For Dashboard CSV data: download the CSV, then upload it directly to Copilot or Gemini." |
| "We're running behind" | Help them triage: "Which steps are essential? Which can be simplified? Focus on getting 3 tools chained with clear outputs, even if each output isn't perfect." |
| "We're ahead of schedule" | "Great. Use the extra time to polish your Canva visual, add an extra feature to your agent, or strengthen your Obsidian documentation." |

**At 12:25:**
> "Lunch in 5 minutes. Before you go: update your Kanban board. Mark what's done, what's in progress, and what's left for the afternoon."

---

### LUNCH (12:30 - 13:30)

During lunch:
- Review each team's progress. Which team needs the most support?
- Set up the presentation environment: everyone in the main meeting, a shared countdown timer, digital evaluation forms
- If any team is significantly behind, think about how to help them catch up without doing their work for them

---

**Phase 2: Completion & Presentation Prep (13:30 - 15:00, 90 min)**

**13:30 - 13:35: Afternoon kick-off**
> "You have 90 minutes. Here's how I'd suggest splitting it:"
```
13:30 - 14:15  Finish executing workflow steps (45 min)
14:15 - 14:30  Finalize Obsidian documentation (15 min)
14:30 - 15:00  Prepare presentation and rehearse (30 min)
```

> "At 14:30, I need everyone to stop building and start preparing their presentation. Even if your workflow isn't perfect, a well-presented 80% workflow is better than a poorly presented 100% workflow."

**13:35 - 14:15: Continue roaming support**

**Focus areas for this phase:**

**Documentation quality:**
Check that each team's Obsidian documentation is clear enough for a colleague to follow:
> "Imagine your colleague who wasn't at this course reads this workflow document. Could they actually follow it? Do they know which tool to open at each step? Do they have the prompts they'd need? Do they know what to look for at the quality gate?"

Look for these in the workflow documentation:
- [ ] Clear trigger description
- [ ] Step-by-step instructions (not just tool names -- actual instructions)
- [ ] Specific prompts written out (not "ask Copilot to help")
- [ ] Expected outputs described for each step
- [ ] Human quality gate(s) with clear criteria
- [ ] Links to related Obsidian notes (prompts, tool notes, outputs)

**Horizon Dashboard integration (especially Team A):**
If Team A hasn't started with the Dashboard:
> "Your workflow should start with official data. Go to dashboard.tech.ec.europa.eu, find the statistics for your cluster, export the CSV, and upload it to your Copilot Notebook. Ask Copilot to identify trends, compare success rates, and suggest strategic positioning. This is what makes your go/no-go memo data-driven rather than opinion-driven."

If other teams want to use the Dashboard:
> "Absolutely. Team C, look at project statistics and completion data for benchmarking. Team B, check for patterns in ethics-related issues across funded projects. The Dashboard has relevant data for everyone."

**Prompt library completeness:**
> "How many prompts are in your /00-Prompts/ folder? You should have at least 8-10 from the whole course. Make sure each one has: the prompt text, which tool it's for, what task it does, and a quality rating."

**Canva and agent status:**
If a team's Canva visual is unfinished: "Spend 10 minutes on this NOW. Choose a template, paste your key text, and get it to 'good enough.' Don't aim for perfection."

If a team's agent isn't working: help debug. Common fixes:
- Re-describe the agent from scratch in a new agent (sometimes faster than debugging the instructions)
- Simplify: remove the part that's broken and present what works

**14:15 - 14:30: Documentation wrap-up**

Announce at 14:15:
> "Documentation time. Spend the next 15 minutes finalizing your Obsidian vault. Make sure your workflow is fully documented, all prompts are saved, and your session logs are up to date."

Walk around and verify.

**14:30 - 15:00: Presentation preparation**

Announce at 14:30:
> "Stop building. Start presenting -- to each other first. Here's the structure again:"

```
1. The Scenario (1 min): What research management challenge did you address?
2. The Workflow (3 min): Step-by-step walk-through. Which tools, in what order,
   and why. Show the handoff points. Point out the quality gates.
3. Live Demo (5 min): Execute at least 2 steps of the workflow live.
   Pick your strongest steps. Have the tools open and ready.
4. The Agent Demo (2 min): Show the interactive agent. Run it.
   Show what it does.
5. Lessons Learned (1 min): What worked? What surprised you?
   What would you do differently?
```

> "Assign presentation roles: who presents which section? Who drives the demo? Who handles Q&A?"

> "Rehearse once. Time yourselves. You have 12 minutes for the presentation plus 3 minutes for Q&A from other teams."

**During rehearsals, visit each team briefly:**

Coaching points:
- "Your workflow explanation needs to show WHY you chose each tool. Don't just say 'then we used Gemini.' Say 'we used Gemini because the document was 150 pages and Copilot's context window couldn't handle it.'"
- "For the live demo, have everything pre-loaded and be ready to share your screen. Don't spend demo time logging into tools or searching for files."
- "The Lessons Learned section is the most important for the audience. Be honest about what was hard or what didn't work. That's where the real learning is."

---

# BREAK (15:00 - 15:15)

During break:
- Set up the presentation environment: everyone in the main meeting, a shared countdown timer
- Share the peer evaluation form link (Microsoft Forms) in Teams
- Post the presentation order in the Teams chat
- Confirm the first team can share their screen in the main meeting
- Share a visible countdown timer on screen

---

# MODULE 3.5 | Capstone Presentations
**Time: 15:15 - 16:30 (75 min)**

## Learning Objectives
- Teams demonstrate Level 4 competency: a complete, multi-tool AI workflow
- Participants learn from other teams' approaches and tool choices
- Peer evaluation reinforces critical evaluation skills

---

## Presentation Management

### Setup

**Announce the format (2 min):**
> "Five presentations. Each team gets 12 minutes to present, plus 3 minutes for Q&A. I'll keep strict time -- I'll give a 2-minute warning and cut you off at 12. This is good practice for real life too."

> "While each team presents, the other four teams fill in the peer evaluation form. Rate each team on:"
```
1. Workflow completeness and logic (/5)
2. Tool selection appropriateness (/5)
3. Output quality (/5)
4. Reusability and documentation quality (/5)
5. Creativity and presentation quality (/5)
```

**Presentation order:**
Announce the order. Recommended: start with the team you expect to be strongest -- it sets the bar and gives energy. Or alphabetical for fairness.

---

### Running Each Presentation (15 min per team)

**Your role during presentations:**

**Timekeeping:**
- Start a visible timer when the team begins
- At 10 minutes: post a "2 min" warning in the chat or give a verbal signal
- At 12 minutes: "Thank you -- let's go to Q&A"
- At 15 minutes total: "Thank you, let's move to the next team"

**During the presentation, note:**
- Did they clearly explain the trigger and context?
- Did they justify their tool choices?
- Did they show handoffs between tools?
- Did they explicitly identify quality gates?
- Did the live demo actually work?
- Did the agent function?
- Were lessons learned genuine and reflective?

**Q&A management (3 min per team):**
After each presentation:
> "Questions from the other teams?"

If no questions, ask one yourself. Suggested questions per team:

**For Team A (Grants):**
> "Your workflow starts with official Dashboard data, which gives your go/no-go memo real credibility. How would this workflow change if the call was from a different funder -- say NSF instead of Horizon Europe -- where there's no equivalent dashboard?"

**For Team B (Compliance):**
> "What happens when regulations conflict -- for example, if the funder requires data sharing but GDPR restricts it? Did your workflow help identify that tension?"

**For Team C (Reporting):**
> "How much time do you estimate this workflow saves compared to writing the periodic report from scratch?"

**For Team D (Communication):**
> "How do you ensure the AI-generated press release is factually accurate and approved by the PI before publication? Where's the quality gate?"

**For Team E (Data Management):**
> "Could this DMP workflow be adapted for a different funder with different requirements? How reusable is it?"

**Between presentations (1 min transition):**
> "Thank you, Team [X]. Next up, Team [Y]. Take a minute to set up."

### Facilitator Notes on Common Presentation Issues

| Issue | How to Handle |
|-------|--------------|
| Live demo fails (tool error, login issue) | "That's OK -- tell us what WOULD have happened. This is realistic -- tools sometimes fail." |
| Team goes over time | Be firm but kind: "I need to stop you here for fairness to other teams. We can discuss more during wrap-up." |
| Presentation is too shallow | Ask a follow-up question that pushes them deeper: "Walk me through the handoff between Step 2 and Step 3. What exactly did you paste, and how did it change the Copilot output?" |
| Presentation is excellent | Name specifically what was good: "Notice how they justified every tool choice with a specific reason. That's Level 4 thinking." |

### After All Presentations (5 min)

Collect the peer evaluation responses (Microsoft Forms). If time allows, quickly tabulate and announce:
- Highest-rated workflow
- Most creative use of tools
- Best documentation

Or save this for the wrap-up.

---

# MODULE 3.6 | Course Wrap-Up & Forward Path
**Time: 16:30 - 17:00 (30 min)**

## Learning Objectives
- Participants understand their progression from Level 1 to Level 4
- Participants know the path forward for continued learning (Levels 5-7)
- Participants provide course feedback

---

## Segment 1: Synthesis (16:30 - 16:45, 15 min)

### Facilitation Script

**The journey (5 min):**
> "Let's look at where you started and where you are now."

Draw or display:

```
Day 1 morning: "How do I write a data management plan?"
               (Level 1 -- one vague question, one generic answer)

Day 3 afternoon: A complete, documented, multi-tool workflow
                 that chains Perplexity, NotebookLM, Copilot Notebook,
                 Gemini, Canva, and an interactive agent --
                 with human quality gates, a prompt library, and
                 full documentation in Obsidian.
                 (Level 4 -- workflow weaving)
```

> "That's the same group of people, three days later. No coding skills required. No technical background needed. Just a structured approach to using AI tools for your actual work."

**Revisit the 7 Levels (3 min):**
> "You've covered Levels 1 through 4. Here's what's beyond, for your own exploration:"

```
Level 5 - The Builder: Automating workflows with tools like Zapier,
          building internal tools with Lovable or Google AI Studio
Level 6 - The Systems Architect: Building complex software with
          GitHub Copilot, orchestrating agents with n8n
Level 7 - The Visionary: AI workforce running entire operations
```

> "These are self-study territory, and each one is more technical than what we covered. But the foundation you built here -- prompt crafting, tool selection, workflow design, documentation -- that foundation carries through every level."

**Five principles to carry forward (5 min):**

> "Five principles for your AI-assisted research management work going forward:"

Write on the shared whiteboard:
```
1. Ask "What's the best tool for THIS step?"
   (not "How do I do everything in ChatGPT?")

2. Save every good prompt.
   Your prompt library is your most valuable AI asset.

3. Document workflows for reuse and sharing.
   If a colleague can't follow it, it's not documented enough.

4. Keep the human in the loop.
   AI generates. You validate. Always.

5. Keep learning and experimenting.
   These tools change monthly. Stay curious.
```

> "Principle 4 deserves emphasis. AI is extraordinarily capable, but it's not infallible. In research management, mistakes can cost grants, damage compliance, or harm your institution's reputation. Every AI output must pass through a knowledgeable human before it becomes real. That's not a limitation -- it's how professional AI use works."

**Peer evaluation results (2 min):**
If you tabulated them, announce results briefly. Keep it celebratory, not competitive.

---

## Segment 2: Resource Distribution (16:45 - 16:55, 10 min)

### Materials to Distribute

**1. Reading List & Resources (share link or handout):**
Prepare this in advance. Suggested contents:
```
AI FOR RESEARCH MANAGEMENT -- RESOURCE LIST

Getting started:
- Microsoft 365 Copilot: microsoft365.com
- NotebookLM: notebooklm.google.com
- Perplexity: perplexity.ai
- Canva: canva.com
- Horizon Dashboard: dashboard.tech.ec.europa.eu
- Obsidian: obsidian.md

Community & learning:
- [Your institution's AI community/channel if it exists]
- Prompt engineering guides: [curate 2-3 quality resources]
- Research management AI communities: [curate if any exist]

Level 5 self-study:
- Zapier (automation): zapier.com -- start with their AI copilot
- Google AI Studio: aistudio.google.com -- for building custom AI tools
- Lovable: lovable.dev -- for building web apps without code

Staying current:
- [2-3 newsletters or blogs on AI in research management]
- [Relevant institutional policy pages on AI use]
```

**2. Level 5 Self-Study Path (share link or handout):**
```
LEVEL 5 SELF-STUDY: YOUR FIRST AUTOMATION

Week 1: Identify a workflow you do repeatedly (e.g., "every time
a new call is published, I check eligibility and email the PI team")

Week 2: Open Zapier. Describe your workflow to the AI copilot.
See what it builds. Test it with a safe, non-critical scenario.

Week 3: Open Google AI Studio or Lovable. Describe an internal tool
you wish existed. See how far you get in 30 minutes.

Week 4: Share what you built with a colleague. Get feedback.
Iterate.
```

**3. Course materials package:**
> "Everything from this course -- all sample documents, the Obsidian vault template, the scenario briefs, and the resource list -- will be shared via [the course Teams channel / email] within 24 hours."

---

## Segment 3: Final Reflection & Feedback (16:55 - 17:00, 5 min)

### Facilitation Script

> "Two final things. First, your last reflection note: create /05-Daily-Reflections/Day3-Final.md in Obsidian."

Display:
```
1. What is the single most valuable thing you learned in this course?
2. What will you do differently in your work starting Monday?
3. What do you wish we had covered that we didn't?
```

> "Second, the course evaluation form. Please complete this before you leave -- it takes 2 minutes and helps me improve the course for future cohorts."

Share the form link in Teams.

**Closing (2 min):**
> "Thank you for three days of hard work and genuine engagement. You came in as AI question-askers. You're leaving as AI workflow weavers. You have a prompt library, documented workflows, interactive tools, and a connected knowledge base in Obsidian. These are real, working tools for your real work."

> "Use them starting Monday. And remember: the best way to get better with AI is simply to use it. Every day, for real tasks. The more you use it, the faster you climb the levels."

> "If you have questions after the course, [provide your contact information or support channel]."

> "Thank you, and good luck."

---

## End-of-Course Facilitator Tasks

### Immediate (within 24 hours)
- [ ] Share course materials package with all participants (Teams/OneDrive link or email)
- [ ] Send thank-you email with resource links
- [ ] Review course evaluation forms -- capture key feedback
- [ ] Tabulate and save peer evaluation results
- [ ] Save team presentation files/recordings if applicable

### Within 1 week
- [ ] Write course debrief notes: what worked, what to change, timing issues, content gaps
- [ ] Follow up with any participants who had technical issues
- [ ] Share best team outputs (with permission) as examples for future cohorts

### Within 1 month
- [ ] Send a 30-day follow-up survey: "Are you using AI tools in your work? Which ones? What workflows have you built?"
- [ ] Consider organizing a follow-up half-day session for Level 5 topics
- [ ] Update course materials based on feedback and tool changes

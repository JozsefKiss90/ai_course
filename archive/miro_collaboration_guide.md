# AI for Research Management Administrators
# Miro Collaboration Guide (Facilitator)

How to run the course agenda, team assignments, and progress tracking on a single
shared **Miro** board -- alongside Microsoft Teams -- across all three days.

---

## TL;DR -- What Miro is for in this course

Miro is the **shared visual workspace** the whole class points at and edits together, live.
You will use it for exactly three things:

1. **Agenda** -- one navigable 3-day plan everyone can see, with a live timer and a parking lot.
2. **Team assignments** -- five team zones (A-E) with ready-made task cards for every exercise and the capstone.
3. **Progress tracking** -- a deliverables dashboard and per-team Kanban you (and they) can read at a glance.

Miro **replaces** the ad-hoc "Microsoft Whiteboard / shared Google Doc / Mentimeter" touchpoints
referenced in the facilitator guides with one persistent surface that lasts all three days.

---

## 1. Where Miro fits in the course stack

The course already has four layers. Miro slots cleanly between "meeting" and "knowledge."

| Layer | Tool | Role |
|-------|------|------|
| **Meet & talk** | Microsoft Teams | Plenary meeting + 5 breakout rooms; voice, video, chat, screen share |
| **Collaborate visually (live)** | **Miro** | The board everyone edits together: agenda, assignments, progress |
| **Store knowledge (permanent)** | Obsidian | Each team's take-home vault: prompt library, workflows, reflections |
| **Do the work** | Copilot, NotebookLM, Gemini, Perplexity, Canva, Horizon Dashboard | Where the actual AI work happens |

**Keep the boundaries clean so nothing is duplicated:**

- Miro is **live and shared** -- it is the pane of glass for *running the course*. It is not a document store.
- Obsidian is **permanent and owned** -- the prompt library, workflows, and reflections live there, not in Miro.
- When a team produces a real artifact (a prompt, a briefing, a workflow), it lives in Obsidian or the AI tool; in Miro they drop a **link card** to it. Miro tracks *that it exists and its status*, not the content itself.

> Mental model: **Teams is the room, Miro is the whiteboard on the wall, Obsidian is each team's notebook, the AI tools are the workshop.** Miro shows where everyone is and what's done; it doesn't hold the deliverables.

---

## 2. Board architecture

**Recommendation: one master board for the whole course.** One board = one link = the simplest
possible onboarding for 15 participants, and it stays within the free plan's editable-board limit
with room to spare. Navigate it with **Frames** (Miro's named regions) and Presentation mode rather
than by splitting into multiple boards.

> Alternative: a **board per day** if one board feels crowded. Pros: less visual clutter, faster load.
> Cons: three links to distribute, progress split across boards, and you lose the single at-a-glance
> dashboard. For a 3-day / 15-person course, one board is the better trade. If you split, still keep
> **one** shared "Progress Dashboard" board so the overview lives in a single place.

### The board as six neighborhoods

Lay the board out left-to-right / top-to-bottom as labelled Frames. Cursors and zoom make a big
board easy; the structure is what keeps 16 people from colliding.

```
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 1: HOME / NAVIGATION                                                    |
|  [ START HERE ]   [ HOW TO USE THIS BOARD ]   [ PARKING LOT / QUESTIONS ]            |
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 2: AGENDA                                                               |
|  [ DAY 1 agenda ]        [ DAY 2 agenda ]        [ DAY 3 agenda ]                     |
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 3: PROGRESS DASHBOARD                                                   |
|  [ Deliverables grid: 5 teams x checklist ]   [ Level 1->4 progression ]             |
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 4: TEAM ZONES (each a tall frame; teams live here during breakouts)     |
|  [ TEAM A ]  [ TEAM B ]  [ TEAM C ]  [ TEAM D ]  [ TEAM E ]                           |
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 5: PLENARY CANVASES (used in the main room, everyone contributes)       |
|  [ Day1: "Our First Prompts" wall ]  [ Tool-Task Fit reference ]  [ Reflections ]    |
+--------------------------------------------------------------------------------------+
| NEIGHBORHOOD 6: CAPSTONE GALLERY + PEER VOTING (Day 3)                               |
|  [ Team A demo area ] ... [ Team E demo area ]   [ Peer voting rubric ]              |
+--------------------------------------------------------------------------------------+
```

- **Neighborhood 1-2** serve Use Case 1 (Agenda).
- **Neighborhood 4** serves Use Case 2 (Team assignments).
- **Neighborhood 3 + 6** serve Use Case 3 (Progress tracking), plus the mini-Kanban inside each team zone.
- **Neighborhood 5** absorbs the plenary "shared doc / whiteboard" moments from the facilitator guides.

---

## 3. Before the course -- setup

Do this the week before, in the same window as your other instructor prep.

### 3.1 Account & plan

- [ ] Create/confirm a Miro account that will **own** the board (yours, or a shared course account).
- [ ] Check your plan's limits **before** Day 1: number of editable boards, and whether **Timer**,
      **Voting**, and **anonymous-visitor editing** are available. These have changed over time and
      may be plan-gated -- every one has a low-tech fallback noted later, so it is not fatal if a
      feature is missing, but you want to know in advance.
- [ ] Decide sharing mode (see 3.4).

### 3.2 Build the board

- [ ] Create the master board, name it e.g. **"AI for Research Management -- Course Board"**.
- [ ] Lay out the six neighborhoods as Frames (titles in **Appendix A**).
- [ ] Paste the agenda, team cards, and trackers from **Appendix A**.
- [ ] Add the built-in **Timer** and **Voting** apps to the board (or note the fallback).
- [ ] **Lock** every scaffolding element -- frame borders, headings, table shells, instructions --
      so participants can add stickies and cards but cannot drag the structure apart. (Select ->
      right-click -> Lock.) This is the single most important step for a 16-cursor board.

### 3.3 Embed in Teams

- [ ] Add the **Miro app for Microsoft Teams** and pin the board as a **tab** in the course Team
      (and/or in each team's channel). One click from where participants already are beats a pasted link.
- [ ] Put the board link in the meeting invite and the Teams channel as a backup.

### 3.4 Sharing settings

- [ ] Set the board so **anyone with the link can edit**. For a live workshop you want zero friction.
- [ ] Decide on identity:
  - **Named** (default): each person's cursor and contributions show who they are -- best for team accountability and the progress board.
  - **Anonymous visitors**: if your plan allows visitor editing without an account, participants type a display name and don't need to sign up. Good for lowering the barrier, but see the note on the Day 1 anonymous diagnostic in 5.4.
- [ ] Test the link in a private/incognito window to confirm a first-timer can get in and edit.

### 3.5 Pre-course participant note (add to your existing pre-course email)

> "We'll use a Miro board for the agenda, your team's tasks, and progress. You don't need an account
> or any prep -- just click the **Miro tab** in our Team (or the link in the invite) when we start,
> and type your name when asked. Keep it open in a browser tab next to Teams throughout the course."

---

## 4. Onboarding participants (first 5 minutes of Day 1)

Fold this into Module 1.1's opening. Do it once; it pays off all three days.

1. **Everyone open the board** via the Teams tab. Confirm you can see a swarm of named cursors.
2. **Find your team zone** (Neighborhood 4) and **type your name** on your team's member stickies.
3. **Teach three controls only:**
   - Zoom / pan (scroll + drag) -- "if you're lost, press **F** or use the frames menu to jump."
   - Double-click empty space -> a **sticky note**.
   - Follow: "when I say *follow me*, click my avatar to be pulled to what I'm showing."
4. **One practice action:** everyone drops a sticky on the Parking Lot with one hope for the course.
   This proves everyone can edit before it matters.

> In Teams **breakout rooms** you cannot screen-share into a room you're not in, so participants must
> have Miro open **themselves**. That's the whole point of this onboarding: from now on, team work
> happens *in their Miro zone*, which you can see from anywhere without entering the room.

---

## 5. Use Case 1 -- The Agenda

### 5.1 What to build

Three **Day** frames (Neighborhood 2). Each day is a vertical stack of **module cards** with the
real times from the roadmap. Keep it lightweight -- title, time, one line, and a status dot.

```
DAY 1: FOUNDATIONS  (Level 1 -> 2)
  09:00  Opening & Orientation
  10:00  L1: The Question Asker
  11:15  L2: Prompt Structure (ICC)
  13:30  L2: Meta-Prompting & Iteration
  15:15  Tool Comparison
  16:15  Obsidian Setup + Wrap
```

Full text for all three days is in **Appendix A** -- paste it in.

### 5.2 Facilitate with it

- **Navigate by Presentation mode.** Add each Day frame (and, if you like, each module) to the frames
  order; step through them so "where we are" is always literally on screen. Or just click the frame
  in the frames panel to fly everyone's view there when you use Follow.
- **Mark the current module.** Move a bright "WE ARE HERE" marker (or flip the status dot to yellow)
  as you start each module. It orients latecomers and anyone who drifts.
- **The live Timer** (Neighborhood 1, floating): start it at the top of every exercise with the
  minutes from the roadmap (e.g., "First Contact -- 20:00"). Everyone sees the same countdown, which
  does the "5-minute warning" work for you.

### 5.3 Parking Lot / Questions

- A dedicated frame where anyone drops a sticky with a question at any time. This is the Miro version
  of "watch the meeting chat" -- but it persists and you can clear items as you answer them.
- Colour convention: **yellow = open question**, **green = answered**, **blue = idea for later**.

### 5.4 The Day 1 anonymous diagnostic ("Our First Prompts")

Module 1.1 asks you to collect everyone's first prompt *anonymously* to observe patterns.
Do it on a plenary wall (Neighborhood 5), **but note**: Miro attributes contributions to authors,
so it is not truly anonymous by default.

- If your plan supports it, turn on the board's **anonymous / hidden-author** setting for this activity.
- Otherwise, either (a) keep this one activity in a genuinely anonymous tool (a shared doc or Mentimeter,
  as the guide suggests) and use Miro for everything else, or (b) accept light attribution -- in a
  supportive room it's rarely a problem. Optionally use **Miro Assist** to auto-cluster the prompt
  stickies into themes ("too short", "no role", "no format") to power the debrief.

---

## 6. Use Case 2 -- Team-based assignments

### 6.1 Team zones

Neighborhood 4 has one tall frame per team, colour-coded. Each team zone contains:

```
+---------------------------------------------------+
| TEAM A -- Grant Lifecycle Management  (colour)     |
|---------------------------------------------------|
| MEMBERS:   [name] [name] [name]                    |
| DOMAIN:    Grant Lifecycle (pre-award)             |
|---------------------------------------------------|
| ROLES (rotate per exercise):                       |
|   Driver-1 (ChatGPT) | Driver-2 (Copilot) | Notes  |
|---------------------------------------------------|
| ASSIGNMENT CARDS  (Day 1 / Day 2 / Day 3)          |
|   [card] [card] [card] ...                         |
|---------------------------------------------------|
| MINI-KANBAN:  To do | Doing | Human review | Done  |
|---------------------------------------------------|
| OUTPUT LINKS:  [->Obsidian] [->Copilot] [->Canva]  |
+---------------------------------------------------+
```

This one zone is where a team spends every breakout. It carries their identity, their tasks, their
status, and links out to their real work -- all in the frame you can glance at from the main room.

### 6.2 Assignment cards

Every exercise becomes a **card** in the team's zone. Card face:

- **Title** (e.g., "Ex 1.3 -- Prompt Factory / Task 1")
- **What** (the concrete task, from the roadmap)
- **Tools** (which AI tools this step uses)
- **Owner** (which member leads -- the roadmap requires each member to lead at least one)
- **Status tag** (To do / Doing / Review / Done)
- **Link** (to the resulting prompt/output in Obsidian or the tool)

**Appendix A** contains the full, ready-to-paste card text for **all five teams across all three days**,
compiled from the roadmap -- so you build the zones once and the whole course is pre-loaded.

### 6.3 Role assignment (built into the cards)

The roadmap is explicit: "each team member must lead on at least one tool," and roles rotate between
tasks. Put a small **role strip** at the top of each zone and have teams drag their name stickies onto
the Driver/Notes slots at the start of each exercise. At a glance you can check nobody is coasting and
everyone has led at least once by the capstone.

### 6.4 How team zones + Teams breakout rooms work together

| In Teams... | In Miro... |
|-------------|------------|
| Facilitator sends teams to 5 breakout rooms | Each team works inside its own zone (Neighborhood 4) |
| You "drop in" to a breakout room to coach | You also watch all 5 zones from the board without entering |
| Team returns to main room for share-out | You use **Follow / Bring everyone to me** onto that team's zone |
| Plenary exercise (diagnostic, tool-fit, voting) | Everyone works on the shared canvases (Neighborhood 5/6) |

Because every team's status is visible on the board, you can spot the team that's stuck (empty
"Doing" column, no output links) and prioritise which breakout room to visit next.

### 6.5 The Day 3 capstone scenarios

Each team's zone gets its **capstone scenario card** (the full per-team briefs are in Appendix A).
For the capstone, expand the mini-Kanban into the team's **workflow chain** laid out as a row of cards
-- one per step (Dashboard -> Perplexity -> Copilot Notebook -> NotebookLM -> Gemini -> Canva -> Agent
-> Obsidian) -- with a **red diamond** dropped on each **human quality gate**. That single row *is* the
Level 4 deliverable, visible and reviewable, and it doubles as their presentation visual in Module 3.5.

---

## 7. Use Case 3 -- Progress tracking

Track progress at three zoom levels: the whole class, each team, and the capstone.

### 7.1 Class-level: the Deliverables Dashboard (Neighborhood 3)

A grid: **rows = deliverables, columns = Teams A-E.** Each cell is a status dot participants flip as
they finish. This is the live version of the Day 1 / Day 2 / Day 3 deliverable checklists.

```
DELIVERABLE                          | A | B | C | D | E |
-------------------------------------|---|---|---|---|---|
Day1: 4+ refined prompts             | O | O | O | O | O |
Day1: Tool comparison matrix         | O | O | O | O | O |
Day1: Obsidian vault set up          | O | O | O | O | O |
Day2: Copilot Notebook built         | O | O | O | O | O |
Day2: NotebookLM analysis            | O | O | O | O | O |
Day2: Gemini long-context task       | O | O | O | O | O |
Day2: Perplexity briefing            | O | O | O | O | O |
Day3: Canva visual asset             | O | O | O | O | O |
Day3: Copilot agent built            | O | O | O | O | O |
Day3: Workflow documented            | O | O | O | O | O |
Day3: Capstone presented             | O | O | O | O | O |
```

- **Colour key:** grey = not started, yellow = in progress, green = done, red = blocked/needs you.
- **The red dot is your radar.** Any red cell is a team asking for help without interrupting anyone.
- Full row text in **Appendix A**.

### 7.2 Team-level: the mini-Kanban (inside each zone)

Four columns: **To do | Doing | Human review | Done**. Assignment cards move left-to-right. The
**"Human review"** column is deliberate -- it makes the roadmap's "keep the human in the loop at
quality gates" principle visible: a card can't reach Done without passing through a human check.
This mirrors the Kanban board teams build in Obsidian on Day 2, but live and shared during sessions.

### 7.3 Level progression (optional, motivating)

A simple Level 1 -> 4 track (Neighborhood 3). Each team moves a token as the course advances:

```
L1 Question Asker --> L2 Prompt Crafter --> L3 Power User --> L4 Workflow Weaver
   (Day 1 AM)          (Day 1 PM)            (Day 2)           (Day 3)
```

It ties the daily work back to the course's spine (the 7 Levels framework) and gives a visible sense
of climbing.

### 7.4 End-of-day review ritual (5 min, plenary)

Close each day on the Deliverables Dashboard:

- Bring everyone to the dashboard with Follow.
- Each team flips its final dots and, in one sentence, names tomorrow's first move (a sticky in their zone).
- You scan for red/grey and note who needs a nudge or a follow-up email -- exactly the "end-of-day
  facilitator debrief" the guides already ask for, now with the data in front of you.

### 7.5 Capstone peer evaluation (Module 3.5) with Voting

Neighborhood 6 is the capstone gallery: one demo area per team plus a voting rubric. Use Miro's
**Voting** app for the peer evaluation the roadmap specifies.

- Give each participant a fixed number of votes per criterion (e.g., 3 dots each).
- Criteria (from the roadmap): **Workflow completeness & logic · Tool selection · Output quality ·
  Reusability & documentation · Creativity.**
- Voting is fast, visible, and hard to fudge; the dot pattern is your at-a-glance result.
- Fallback if Voting isn't on your plan: each person drags 3 coloured dots (emoji or stickies) onto
  the criteria -- same outcome, manual.

---

## 8. Day-by-day facilitation playbook

Compact map of Miro touchpoints to the existing modules. Nothing here changes your run-of-show; it
just says *which part of the board* is live when.

### Day 1 -- Foundations

| Module | Miro touchpoint |
|--------|-----------------|
| 1.1 Opening | 5-min onboarding; Agenda Day 1 frame; **"Our First Prompts"** diagnostic wall (see 5.4) |
| 1.2 First Contact | Teams work in their zones; drop Ex 1.1 stickies + usefulness scores |
| 1.3 Prompt Makeover | ICC card per member; best prompt -> a green "library candidate" sticky |
| 1.4 Prompt Factory | Ex 1.3 cards (Task 1 & 2) move across the mini-Kanban; output links to Obsidian |
| 1.5 Tool Comparison | Plenary **Tool-Task Fit** reference wall fills up as teams report verdicts |
| 1.6 Wrap | End-of-day ritual on the Deliverables Dashboard; flip Day 1 dots |

### Day 2 -- Depth & Context

| Module | Miro touchpoint |
|--------|-----------------|
| 2.1 Recap | Each team posts its single best Day 1 prompt on a "Best of Day 1" strip |
| 2.2 Copilot Notebooks | Notebook card per team; link-card to the actual Notebook; status -> Done when tested |
| 2.3 NotebookLM | NotebookLM card; drop the structured output link; tag "source-grounded" |
| 2.4 Gemini | Long-doc card; note strengths/limits sticky (feeds their Obsidian tool notes) |
| 2.5 Perplexity | Intelligence-briefing card; link to the briefing in Obsidian |
| 2.6 Obsidian | Confirm each team's output links on the board resolve to real vault notes |
| 2.7 Day 3 preview | Capstone scenario card appears in each zone; teams start the workflow-chain row |

### Day 3 -- Integration & Workflow

| Module | Miro touchpoint |
|--------|-----------------|
| 3.1 Workflow design | Build the capstone **workflow-chain row**; drop red diamonds on human gates |
| 3.2 Canva | Canva card; link to the visual asset |
| 3.3 Copilot Agents | Agent card; link to the shared agent; note instructions used |
| 3.4 Capstone work | The chain row fills in; mini-Kanban clears to Done; Deliverables dots go green |
| 3.5 Presentations | Capstone gallery + **Voting** peer evaluation (see 7.5) |
| 3.6 Wrap | Level progression tokens reach L4; final dashboard scan; export the board (see 10) |

---

## 9. Miro feature cheat-sheet

The short list of what you'll actually use. You don't need more than this.

| Feature | Use it for | Notes |
|---------|-----------|-------|
| **Frames** | The six neighborhoods; navigation | Name them; add to Presentation order |
| **Presentation mode** | Walking the agenda / share-outs | Step through frames in sequence |
| **Follow / Bring everyone to me** | Pull the class to what you're showing | Works across breakout rooms (they must have Miro open) |
| **Sticky notes** | Diagnostic prompts, questions, ideas | Colour = meaning (define once) |
| **Cards** | Assignment cards, Kanban items | Have title/owner/tag/status fields |
| **Tags** | Status (To do/Doing/Review/Done), tool labels | Colour-coded, filterable |
| **Timer** | Every timed exercise | Set the roadmap minutes; visible to all |
| **Voting** | Capstone peer evaluation | Fixed dots per criterion; manual fallback exists |
| **Comments** | Async feedback on a team's output | @mention; resolve when addressed |
| **Reactions/emoji** | Quick pulse checks, "done!", applause | Lightweight engagement |
| **Link/embed cards** | Point to Obsidian notes, Copilot, Canva, Dashboard | Keeps deliverables *out* of Miro |
| **Lock** | Freeze the scaffolding | Do this before Day 1 -- critical |
| **Miro Assist (AI)** | Cluster diagnostic stickies, summarise a wall | Optional flourish; on-theme for an AI course |

**Participant controls to teach (only these):** zoom/pan, double-click = sticky, click-avatar = follow, `F` = frames/fit.

---

## 10. Pitfalls, accessibility, privacy, contingency

**Pitfalls**
- *Structure gets dragged apart.* Lock everything that isn't meant to be edited (see 3.2). This is the #1 fix.
- *Cursor chaos.* Keep team work inside team zones; use the neighborhoods so 16 people aren't on top of each other.
- *Miro becomes a document dump.* It shouldn't. Real artifacts live in Obsidian/the tools; Miro holds status + links.
- *Big-board lag.* One well-organised board is fine for 16 people; if it slows, collapse/hide finished neighborhoods or split per-day (see 2).

**Accessibility**
- Don't rely on colour alone -- pair every status colour with a word or icon (the dashboard uses both).
- Keep font sizes readable at the default zoom; some participants join on laptops.
- Miro has keyboard shortcuts and screen-reader support, but for anyone who struggles, the team-of-3
  structure means a teammate can drive Miro while they contribute by voice -- consistent with the
  course's built-in peer-support design.

**Privacy** (consistent with the course's anonymisation rule)
- Miro is a shared, cloud, link-accessible surface. Treat it as **public to the class**.
- **No sensitive or non-anonymised documents on the board.** Miro holds *links and status*; the actual
  (possibly sensitive) documents stay in the AI tools and each team's own storage. Reinforce this when
  you teach the output-link pattern.

**Contingency** (mirrors the roadmap's risk table)
- *Miro is down / a participant can't get in:* fall back to a Microsoft Whiteboard for that session and
  the Teams channel for links; buddy the locked-out participant into a teammate's screen. The course
  runs fine without Miro for a session -- it's the coordination layer, not the work itself.
- *A feature (Timer/Voting) isn't on your plan:* use the manual fallbacks noted in 5.2 and 7.5.
- *Persist the work:* at the end of Day 3, **export the board** (PDF/image) and post it in the Teams
  channel so teams keep a record of their agenda, assignments, and final progress alongside their
  Obsidian vault.

---

## Appendix A -- Copy-paste board content

Build the board once from this. Text is compiled from the course roadmap so the whole course is
pre-loaded.

### A1. Home / Navigation frames

**START HERE**
> Welcome to the course board. 1) Find your **team zone** below and add your name. 2) Keep this open
> next to Teams all three days. 3) The **agenda** shows where we are; the **timer** shows time left;
> the **dashboard** shows what's done. Questions -> Parking Lot.

**HOW TO USE THIS BOARD**
> - Double-click empty space = sticky note.  - Click my avatar = follow me.  - `F` = jump between frames.
> - Move your task cards across your team's Kanban as you work.  - Drop a **link card** to anything you
>   make (Obsidian, Copilot, Canva) -- don't paste the content here.  - Don't move locked scaffolding.

**PARKING LOT / QUESTIONS**  (yellow = open, green = answered, blue = later)

### A2. Agenda frames

**DAY 1 -- FOUNDATIONS (Level 1 -> 2)**
```
09:00  Opening & Orientation
10:00  Level 1: The Question Asker
11:00  Break
11:15  Level 2: Prompt Structure (ICC)
12:30  Lunch
13:30  Level 2: Meta-Prompting & Iteration
15:00  Break
15:15  Tool Comparison & Critical Evaluation
16:15  Obsidian Setup + Day 1 Wrap
```

**DAY 2 -- DEPTH & CONTEXT (Level 3)**
```
09:00  Recap & Level 3 Intro
09:30  Copilot Notebooks
11:00  Break
11:15  NotebookLM -- Document Analysis
12:30  Lunch
13:30  Gemini -- Long-Context Work
14:30  Perplexity -- Research Discovery
15:15  Break
15:30  Obsidian Knowledge Hub
16:30  Day 2 Wrap + Day 3 Brief
```

**DAY 3 -- INTEGRATION & WORKFLOW (Level 4)**
```
09:00  Level 4 Intro & Workflow Design
09:45  Canva AI for Visual Outputs
10:30  Break
10:45  Copilot Agents -- Build Your Own
11:45  Capstone Work Session (+13:30)
15:15  Capstone Presentations + Peer Voting
16:30  Synthesis & Wrap-Up
```

### A3. Team zone assignment cards (all teams, all days)

Each block is one team's zone. Bracketed `[ ]` = status tag to flip.

**TEAM A -- Grant Lifecycle Management (pre-award)**
```
Members: ____  ____  ____
Day1 Ex1.3 Task 1  [ ]  Draft a call eligibility checklist            Tools: ChatGPT->Copilot
Day1 Ex1.3 Task 2  [ ]  Write a go/no-go decision memo                Tools: ChatGPT->Copilot
Day1 Ex1.4         [ ]  Tool comparison matrix (one prompt x4 tools)  Tools: all four + Dashboard
Day2 Notebook      [ ]  "Grant Lifecycle Hub" (call analysis, budget) Sources: call text, budget template
Day2 NotebookLM    [ ]  Call + work programme + Programme Guide -> eligibility, outcomes, weights
Day2 Perplexity    [ ]  EU funding success-rate trends + proposal weaknesses (cross-ref Dashboard CSV)
Day3 Canva         [ ]  One-page "Call Opportunity Brief" for leadership
Day3 Agent         [ ]  Proposal budget assistant (costs, overhead, partner allocations)
Day3 CAPSTONE      [ ]  New call published -> discovery to go/no-go to proposal outline
   Chain: Dashboard -> Perplexity -> Copilot Notebook -> NotebookLM -> Canva -> Agent -> Obsidian
```

**TEAM B -- Research Compliance & Ethics**
```
Members: ____  ____  ____
Day1 Ex1.3 Task 1  [ ]  Summarize ethics requirements (human-subjects) Tools: ChatGPT->Copilot
Day1 Ex1.3 Task 2  [ ]  Draft an informed consent template             Tools: ChatGPT->Copilot
Day1 Ex1.4         [ ]  Tool comparison matrix                         Tools: all four + Dashboard
Day2 Notebook      [ ]  "Compliance Advisor" (ethics language, frameworks) Sources: ethics checklist, GDPR template
Day2 NotebookLM    [ ]  Ethics guidelines + institutional policy + GDPR -> map reqs, find gaps
Day2 Perplexity    [ ]  Newest EU research-ethics & data-protection regs 2025-2026
Day3 Canva         [ ]  Infographic mapping the ethics review process
Day3 Agent         [ ]  Ethics screening agent (project Q&A -> review type)
Day3 CAPSTONE      [ ]  Human participants + AI + cross-border data -> compliance package
   Chain: Perplexity -> NotebookLM -> Copilot Notebook -> Canva -> Agent -> Obsidian
```

**TEAM C -- Research Reporting & Impact Assessment**
```
Members: ____  ____  ____
Day1 Ex1.3 Task 1  [ ]  Publishable project summary from a technical report  Tools: ChatGPT->Copilot
Day1 Ex1.3 Task 2  [ ]  KPI tracking narrative                               Tools: ChatGPT->Copilot
Day1 Ex1.4         [ ]  Tool comparison matrix                               Tools: all four + Dashboard
Day2 Notebook      [ ]  "Reporting Workspace" (EU reporting, impact metrics) Sources: periodic report, KPI framework
Day2 NotebookLM    [ ]  2 periodic reports + project desc -> achievements vs planned, flag delays
Day2 Perplexity    [ ]  Frameworks for research impact beyond publications
Day3 Canva         [ ]  Visual dashboard mockup (project KPIs & status)
Day3 Agent         [ ]  Milestone assistant (list -> status + deadline flags)
Day3 CAPSTONE      [ ]  18-month periodic report -> assemble, draft, quality-check
   Chain: Perplexity -> NotebookLM -> Gemini -> Copilot Notebook -> Canva -> Obsidian
```

**TEAM D -- Stakeholder Communication & Dissemination**
```
Members: ____  ____  ____
Day1 Ex1.3 Task 1  [ ]  Press release for a granted project           Tools: ChatGPT->Copilot
Day1 Ex1.3 Task 2  [ ]  Stakeholder newsletter section                Tools: ChatGPT->Copilot
Day1 Ex1.4         [ ]  Tool comparison matrix                        Tools: all four + Dashboard
Day2 Notebook      [ ]  "Comms & Dissemination" (institutional voice) Sources: brand guidelines, PR template
Day2 NotebookLM    [ ]  3 project summaries + dissemination template -> reusable angles
Day2 Perplexity    [ ]  Best practices for research comms & public engagement in EU projects
Day3 Canva         [ ]  Social media card set (3 cards) for an announcement
Day3 Agent         [ ]  Dissemination planner (audience, channel, timeline -> plan)
Day3 CAPSTONE      [ ]  Breakthrough results -> multi-channel communication workflow
   Chain: NotebookLM -> Copilot Notebook -> ChatGPT Canvas -> Canva -> Perplexity -> Obsidian
```

**TEAM E -- Research Data Management & Open Science**
```
Members: ____  ____  ____
Day1 Ex1.3 Task 1  [ ]  Data management plan outline                  Tools: ChatGPT->Copilot
Day1 Ex1.3 Task 2  [ ]  Data sharing agreement summary                Tools: ChatGPT->Copilot
Day1 Ex1.4         [ ]  Tool comparison matrix                        Tools: all four + Dashboard
Day2 Notebook      [ ]  "Data Management Office" (FAIR, DMP standards) Sources: DMP template, funder policies
Day2 NotebookLM    [ ]  Funder policy + institutional policy + FAIR -> consolidated checklist
Day2 Perplexity    [ ]  Latest FAIR implementation & open-science mandates
Day3 Canva         [ ]  Visual checklist poster for FAIR data compliance
Day3 Agent         [ ]  DMP builder (interviews user -> funder-ready DMP sections)
Day3 CAPSTONE      [ ]  New consortium DMP (funder + FAIR + institutional) workflow
   Chain: Perplexity -> NotebookLM -> Copilot Notebook -> Gemini -> Agent -> Obsidian
```

### A4. Deliverables Dashboard rows

```
DELIVERABLE                          | A | B | C | D | E |
Day1: 4+ refined prompts             | . | . | . | . | . |
Day1: Tool comparison matrix         | . | . | . | . | . |
Day1: Obsidian vault set up          | . | . | . | . | . |
Day2: Copilot Notebook built+tested  | . | . | . | . | . |
Day2: NotebookLM analysis + output   | . | . | . | . | . |
Day2: Gemini long-context task       | . | . | . | . | . |
Day2: Perplexity briefing (cited)    | . | . | . | . | . |
Day2: Day 3 project plan drafted     | . | . | . | . | . |
Day3: Canva visual asset             | . | . | . | . | . |
Day3: Copilot agent built+tested     | . | . | . | . | . |
Day3: Workflow documented (Obsidian) | . | . | . | . | . |
Day3: Capstone presented             | . | . | . | . | . |
Legend:  . grey=not started  Y yellow=in progress  G green=done  R red=blocked/needs facilitator
```

### A5. Capstone peer-voting rubric (Neighborhood 6)

```
Vote (3 dots each) on every team, per criterion:
  [ ] Workflow completeness & logic
  [ ] Tool selection appropriateness
  [ ] Output quality
  [ ] Reusability & documentation quality
  [ ] Creativity
```

---

## Appendix B -- Pre-course build checklist

- [ ] Board created and named; owner account confirmed; plan limits checked (boards, Timer, Voting, visitor edit)
- [ ] Six neighborhoods laid out as Frames (A1-A5 pasted in)
- [ ] Three Agenda day-frames with real times (A2)
- [ ] Five team zones with members/roles/cards/mini-Kanban/output-links (A3)
- [ ] Deliverables Dashboard grid (A4) and Level 1->4 track
- [ ] Plenary canvases: "Our First Prompts" wall, Tool-Task Fit reference, Reflections
- [ ] Capstone gallery + voting rubric (A5)
- [ ] Timer + Voting apps added (or fallbacks noted)
- [ ] **All scaffolding locked**
- [ ] Miro app added to Teams; board pinned as a tab; link in invite + channel
- [ ] Sharing = anyone-with-link-can-edit; identity mode decided; tested in an incognito window
- [ ] Frames added to Presentation order for smooth navigation

---

## Appendix C -- Participant quick-start (share this)

> **Our course board (Miro)**
> - Open it from the **Miro tab** in our Team (or the link in the invite). No account needed -- type your name when asked.
> - **Keep it open next to Teams** for all three days.
> - **Find your team zone**, add your name, and use it as your team's home base during breakouts.
> - **Move your task cards** across your team's Kanban (To do -> Doing -> Human review -> Done) as you work.
> - Made something (a prompt, a briefing, a workflow)? Drop a **link** to it on your card -- keep the
>   actual content in Obsidian or the tool, not on the board.
> - **When I say "follow me,"** click my avatar to be pulled to what I'm showing.
> - Questions any time -> **Parking Lot** (yellow sticky).
> - Only rule: don't drag the board's structure around -- add your own stickies and cards freely.

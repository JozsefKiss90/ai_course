# Facilitator Guide -- Day 1: Foundations
## Level 1 "The Question Asker" + Level 2 "The Prompt Crafter"

---

# Pre-Day Checklist

Complete these before participants join the Teams meeting:

- [ ] Teams meeting set up with 5 team breakout rooms (3 per room), each named for its team (A-E) and domain
- [ ] Screen sharing tested in Teams; your camera and microphone working
- [ ] Test your internet connection and screen share with 3+ AI tools open at once
- [ ] Open on your facilitator machine: Microsoft 365 Copilot, ChatGPT, Gemini, Perplexity (all logged in)
- [ ] Load the "before and after" demo prompts (see Module 1.1 script below)
- [ ] Prepare team domain / task-assignment cards to share in Teams for Exercises 1.3 and 1.4
- [ ] Download link ready (to post in Teams) for the Obsidian vault template
- [ ] Shared Teams channel with a Files folder created (one per team) with sample documents
- [ ] Anonymous prompt collection method ready (shared Google Doc, Mentimeter, or the Teams meeting chat)
- [ ] A shared digital whiteboard (Microsoft Whiteboard) available for collective notes
- [ ] Have backup sample prompts prepared in case participants struggle to generate their own
- [ ] Pre-course survey results reviewed -- note any participants with zero AI experience

---

# MODULE 1.1 | Opening & Orientation
**Time: 09:00 - 10:00 (60 min)**

## Learning Objectives
- Participants understand the 7 Levels framework and where the course will take them
- Participants experience their current AI usage level firsthand
- Participants can name all tools they will use and understand the role of each

---

## Segment 1: Welcome & Course Arc (09:00 - 09:15, 15 min)

### Setup
- Have slide 1 ready: course title, your name, the 3-day arc visual
- Share your screen; camera on

### Facilitation Script

**Opening (2 min):**
> "Welcome. Over the next three days, you're going to go from using AI the way most people do -- as a slightly fancier Google -- to building complete AI-powered workflows for your research management work. By Friday afternoon, each team will walk out with a documented, repeatable workflow, a library of tested prompts, and at least one interactive tool you built yourselves -- with zero coding."

**The 7 Levels Framework (8 min):**
> "This course follows a framework called the 7 Levels of AI User. Let me walk you through all seven, and then I'll tell you where we're going."

Present each level briefly (use a single slide or shared list):
1. The Question Asker -- using AI like Google
2. The Prompt Crafter -- how you ask changes what you get
3. The Power User -- persistent context, workspaces, multiple tools
4. The Workflow Weaver -- chaining tools, building prototypes, multi-tool workflows
5. The Builder -- automations that run without you
6. The Systems Architect -- building complex software and agent systems
7. The Visionary -- AI workforce running a business

> "We're going from Level 1 to Level 4 in three days. That's ambitious, but it's absolutely realistic because the jumps between levels are about mindset shifts, not technical skills. Every one of you can get there."

**Before and After Demo (5 min):**
Show a concrete example -- the same research management task at Level 1 vs. Level 4.

Open Microsoft 365 Copilot. Type this Level 1 prompt live:
```
How do I respond to a Horizon Europe call?
```
Show the generic, high-level response.

Then say:
> "Now let me show you what this looks like at Level 4."

Switch to a pre-prepared screenshot or second browser tab showing a Level 4 workflow output: a go/no-go memo produced by a Copilot Notebook fed with a call document analyzed in NotebookLM, with a Canva one-pager and an interactive readiness checklist agent. Don't explain the tools yet -- just show the quality and specificity of the output.

> "Same task. Same person. The difference is knowing how to use the tools. That's what this course teaches."

### Timing Checkpoint
You should be at 09:15. If you ran over, compress the next segment slightly.

---

## Segment 2: Live Diagnostic -- Where Are You Now? (09:15 - 09:35, 20 min)

### Setup
- Open a shared Google Doc or Mentimeter board titled "Our First Prompts"
- Ensure all participants have Microsoft 365 Copilot open in their browsers

### Facilitation Script

**Instructions (3 min):**
> "Here's your first task. Open Microsoft 365 Copilot -- microsoft365.com in your browser. Think of a question you would normally Google that's related to your research management work. Something you've actually wondered about or needed to look up recently. Type it into Copilot exactly the way you'd ask it. Don't overthink it -- I want your natural instinct."

> "Once you get a response, I want you to do two things: copy your exact prompt into our shared document [show link/Mentimeter], and give the response a usefulness score from 1 to 5."

**Individual Work (7 min):**
Keep an eye on the meeting and the chat. Common issues to watch for:
- Participants not knowing what to ask: suggest "Think about what you Googled last week for work"
- Sign-in problems: help with Microsoft 365 / Copilot sign-in (should be done pre-course, but stragglers happen)
- Very short prompts are GOOD at this stage -- that's the point

**Collective Review (10 min):**
Share the shared document/Mentimeter on your screen. Read through prompts aloud (or display them). Likely patterns you'll see:

- Very short: "ERC grant deadlines", "data management plan"
- Question-style: "What is open access?"
- Slightly better: "How do I write an ethics section for my proposal?"

Point out the patterns WITHOUT judgment:
> "Look at these. What do they have in common? [Take 2-3 answers from the group.] Most of them are short. Most don't tell Copilot anything about who you are, what you're working on, or what format you need. That's completely normal -- it's how all of us start. The AI gave you a response, and it was probably... fine. Generic. The kind of thing you could have found on a website."

> "Now here's the key insight that changes everything: the AI doesn't know you're a research manager at a European university working on Horizon Europe projects -- unless you tell it. And that one fact transforms what you get back."

> "We're going to come back to these exact prompts later today and rebuild them. You'll see the difference yourselves."

### Facilitator Notes
- Save this shared document -- you'll reference it in Module 1.3
- If anyone scored their response 4 or 5, flag their prompt as a good example to analyze later
- Don't fix anyone's prompts yet -- the learning happens when THEY see the gap

---

## Segment 3: The AI Landscape for Research Management (09:35 - 10:00, 25 min)

### Setup
- Have each tool open in separate browser tabs, ready to switch quickly
- Prepare one simple query to demonstrate in each tool: "What are the key components of a data management plan for an EU-funded project?"

### Facilitation Script

**Framing (2 min):**
> "Before we dive deeper into prompting, let me show you the tools you'll be using over these three days. Think of this as your toolkit -- each tool does something different, and part of becoming a Level 4 user is knowing which tool to reach for."

**Tool Tour -- 3 minutes each, 18 min total:**

For each tool, do the same thing: briefly describe what it's for, show the interface, and run one quick action.

**1. Microsoft 365 Copilot (3 min) -- "Home Base"**
> "This is Microsoft 365 Copilot. It's our primary tool -- it works across your Microsoft 365 apps and can ground its answers in your own files and work data. It has a feature called Notebooks, where you can give it persistent context -- we'll set this up tomorrow. And you can build your own Agents -- custom AI tools -- with no coding; we'll do that on Day 3."
- Show: the chat interface, Notebooks, and where you create Agents

**2. ChatGPT Free (3 min) -- "The Meta-Prompter"**
> "ChatGPT by OpenAI. You probably know this one. We'll mainly use it for meta-prompting -- using AI to write better prompts for other AI tools. It also has Canvas, which is useful for collaborative document editing."
- Show: the chat interface, mention Canvas

**3. Google Gemini (3 min) -- "The Long Reader"**
> "Gemini by Google. Its superpower is context window -- it can process very long documents, up to a million tokens. That means you can upload an entire grant agreement and ask questions across the whole thing. We'll use this tomorrow."
- Show: the chat interface, the file upload button

**4. Perplexity AI (3 min) -- "The Research Engine"**
> "Perplexity is different from the others. Every answer comes with source citations that you can click and verify. When you need current, factual information -- success rates, policy changes, regulation updates -- this is where you go."
- Show: run the DMP query, point out the citation numbers and source panel

**5. NotebookLM (3 min) -- "The Document Analyst"**
> "NotebookLM by Google. You upload your own documents and it only answers based on those documents. No external information, no hallucination from training data. It shows you exactly which passage each answer comes from. For analyzing call texts, policies, and reports -- this is essential. We'll go deep on this tomorrow."
- Show: a pre-loaded notebook with a sample document, ask one question, show the citation pinning

**6. Horizon Dashboard (2 min) -- "The Ground Truth"**
> "This is the EU's official Horizon Dashboard, hosted on the Funding & Tenders Portal. It's not an AI tool -- it's a data source. It gives you authoritative statistics on success rates, funding distribution, country participation, and project data for Horizon Europe and Horizon 2020. When an AI tool tells you 'the success rate for this call type is 15%,' the Dashboard is where you verify that number."
- Show: the main dashboard page, click into a statistics view (e.g., success rates by cluster), show the CSV export button
- Key message: "AI tools are powerful, but they can get numbers wrong. The Dashboard is your ground truth for EU funding data."

**7. Canva AI (2 min) -- "The Visual Designer"**
> "Canva for creating professional visuals -- one-pagers, infographics, presentation slides. We'll use it on Day 3 to turn AI-generated text into things you can actually share with stakeholders."
- Show: Magic Design, briefly

**8. Obsidian (1 min) -- "The Knowledge Vault"**
> "And Obsidian -- this is where everything comes together. It's a knowledge management tool where you'll save your prompts, document your workflows, and build a connected knowledge base. We'll set this up at the end of today."
- Show: a screenshot or quick flash of the vault -- don't demo fully yet

**Closing (3 min):**
> "Here's the key mental model: Microsoft 365 Copilot is your home base -- it's where you do most of your thinking and writing. The other tools are specialists you bring in when you need something specific. Over three days, you'll learn when to reach for which tool. Any questions about the tools before we move on?"

Take 2-3 questions. Common ones:
- "Do I need paid versions?" -- Mostly no: the supporting tools all work on free tiers, and Microsoft 365 Copilot Chat is included with your Microsoft 365 account. A paid Copilot licence adds grounding in your organisation's work data, but it isn't required for this course.
- "Is my data safe?" -- Good question. Don't upload truly sensitive data to any of these. We'll discuss anonymization practices.
- "Which one is best?" -- That's exactly what we'll figure out today in Module 1.5.

### Timing Checkpoint
You should be at 10:00. If running late, cut the Q&A short -- you can address tool questions as they come up.

---

# MODULE 1.2 | Level 1 -- The Question Asker
**Time: 10:00 - 11:00 (60 min)**

## Learning Objectives
- Participants see firsthand how input quality determines output quality
- Participants experience the gap between a vague prompt and a specific one
- Teams begin collaborative AI work

---

## Segment 1: Demo -- The Same Question, Three Ways (10:00 - 10:15, 15 min)

### Setup
- Microsoft 365 Copilot open, new conversation
- Screen sharing on in Teams

### Facilitation Script

> "Let me show you something. I'm going to ask Copilot the same question three different ways, and I want you to watch what happens to the answer."

**Version 1 -- Google-style (type live):**
```
Horizon Europe budget
```
Read the response aloud briefly. It will be generic: here's what Horizon Europe is, here's the total budget, etc.

> "Useful? Sort of. It's like a Wikipedia summary. Is this what a research manager actually needs when they're working on a budget? No."

**Version 2 -- Better (type live):**
```
Explain the budget structure of Horizon Europe Pillar 2 collaborative projects
```
Scan the response. It will be more specific -- pillars, clusters, cost categories.

> "Better. It's getting closer. But it still doesn't know what I'm actually trying to do."

**Version 3 -- Good (type live):**
```
I'm preparing a budget for a Horizon Europe Cluster 4 collaborative project
with 8 partners. Explain the eligible cost categories, overhead calculation
method, and common budgeting mistakes.
```
Let the response generate. It will be substantially more useful -- specific cost categories, the 25% flat rate overhead, practical warnings.

> "Now THAT is useful. Same topic, same tool, wildly different results. What changed? [Take answers.] I told it who I am, what I'm doing, how many partners, and exactly what I need. The AI didn't get smarter between these three attempts -- I got more specific."

> "This is the fundamental insight of Level 1: the AI is only as good as what you give it. Let's practice that."

### Facilitator Notes
- Keep the three conversations open side-by-side if your screen allows it
- If a participant points out that Version 3 might also have errors -- great! Acknowledge that AI can be wrong and we'll address critical evaluation later

---

## Segment 2: Team Exercise 1.1 -- "First Contact" (10:15 - 10:45, 30 min)

### Setup
- Ensure all participants are in their team breakout rooms
- Each person has Microsoft 365 Copilot open

### Instructions to Give (3 min)

> "Now it's your turn. Each of you, individually: think of a real task from your daily work. Not a question you'd Google -- a task you actually need to do. Maybe you need to draft an email to a PI about a budget revision. Maybe you need to summarize a policy document. Maybe you need to explain a compliance requirement to a colleague. Whatever it is, ask Copilot to help you, using whatever words feel natural."

> "After you get a response, do four things:"
Post in the meeting chat:
1. Screenshot your prompt and response
2. Rate the usefulness: 1 = useless, 5 = I could use this as-is
3. Write down what's missing or wrong in the response
4. Share with your team and look for patterns

> "You have 20 minutes for this. About 10 minutes individual, 10 minutes team discussion."

### During the Exercise (20 min)
Drop into the team breakout rooms. What to watch for:

**Common struggles:**
- "I don't know what to ask" -- suggest: "What did you work on yesterday? What task took the longest?"
- Participants writing very long, perfect prompts -- that's actually fine, but note it for the debrief as an outlier
- Participants writing extremely short prompts -- don't intervene, this is the learning moment

**Coaching moves (if needed):**
- If a team finishes early: "Now try asking the same question but add one sentence about who you are and what you're trying to accomplish. See if the answer changes."
- If someone gets a great response on their first try: "Interesting -- what did you include in your prompt that might have helped?"

**What to listen for during team discussions:**
- Teams noticing that vague prompts got vague answers
- Teams noticing that format wasn't specified (got paragraphs when they needed bullet points)
- Teams realizing they didn't say what role they're in

### Timing Check
At 10:40, give a 5-minute warning: "Start wrapping up your team discussions."

---

## Segment 3: Debrief (10:45 - 11:00, 15 min)

### Facilitation Script

> "Let's hear what you noticed. I don't need every prompt -- just the patterns. What did your team observe?"

Call on 2-3 teams. Guide the discussion toward these key takeaways:

**Takeaway 1: No context = generic output**
> "Most of us didn't tell Copilot who we are, what institution we're at, what programme we're working with, or what we've already tried. So it gave us the answer it would give anyone."

**Takeaway 2: No format specification = AI chooses for you**
> "If you don't say 'give me bullet points' or 'write this as an email' or 'format this as a checklist,' the AI picks whatever format it wants. Usually long paragraphs."

**Takeaway 3: The AI doesn't know your job**
> "Here's the big one: Copilot doesn't know you're a research manager at a university. It doesn't know you deal with Horizon Europe, or ethics reviews, or that you report to a Vice-Rector for Research. Unless you tell it. And when you tell it, the outputs transform."

> "That's Level 1. You're using AI, and it's helpful. But you're leaving 80% of the value on the table. Level 2 is about getting that other 80%. Let's take a break and come back ready to learn the structure."

### Facilitator Notes
- Post the three takeaways in the meeting chat (or a shared Microsoft Whiteboard) -- keep them visible all day
- Don't spend time on individual prompts here -- the deep work happens in Module 1.3

---

# BREAK (11:00 - 11:15)

During break:
- Check that the shared Google Doc has everyone's prompts from the diagnostic
- Prepare the ICC framework slide or shared whiteboard layout
- Have the partner search announcement demo prompt ready to type

---

# MODULE 1.3 | Level 2 -- The Prompt Crafter, Part 1: Structure
**Time: 11:15 - 12:30 (75 min)**

## Learning Objectives
- Participants can apply the Instruction-Context-Constraints (ICC) framework to any research management task
- Participants experience the "ask me questions first" technique
- Participants see measurable improvement in AI output quality by comparing before/after prompts

---

## Segment 1: Demo -- The ICC Framework in Research Management (11:15 - 11:35, 20 min)

### Setup
- Microsoft 365 Copilot open, new conversation
- Microsoft Whiteboard or a slide with the ICC framework:
  ```
  I = Instruction (What do you want?)
  C = Context (Who are you? What's the situation?)
  C = Constraints (Format, length, tone, what to include/exclude)
  ```

### Facilitation Script

**Introduce the framework (5 min):**
> "The first technique at Level 2 is called ICC: Instruction, Context, Constraints. It's dead simple. Every prompt you write should have three parts."

Write or display:
> "**Instruction:** What do you want the AI to do? Be specific. Not 'help me with a budget' but 'draft a budget justification narrative for personnel costs.'"

> "**Context:** Who are you, what's the situation, what background does the AI need? This is where you tell it you're a research manager, you're working on Horizon Europe, your PI's expertise is X, the project has Y partners."

> "**Constraints:** What are the rules? Word limits, tone, format, what must be included, what to avoid. 'Maximum 500 words, formal tone, must include cost breakdown by partner.'"

**Live Demo (10 min):**
> "Let me show you this in action. Let's say I need to write a partner search announcement for the Funding & Tenders portal."

Type in Microsoft 365 Copilot -- deliberately, so participants can follow:

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

Let the response generate. Read through it briefly with the group.

> "Look at this. It has the right length, the right tone, it includes everything I specified. Could I use this as a starting point? Absolutely. Now let me show you a shortcut that's even more powerful."

**The "Ask Me Questions" technique (5 min):**
Open a new conversation. Type:

```
I need to write a partner search announcement for the Horizon Europe
Funding & Tenders portal. Before writing anything, ask me all the
questions you need to produce the best possible announcement.
```

Show the questions Copilot asks. Answer 3-4 of them briefly (type short answers). Then show the output.

> "See what happened? Instead of me trying to think of all the context and constraints upfront, I let the AI figure out what it needs. It asked about things I wouldn't have thought to include -- like whether we have a project acronym yet, or whether there's a specific TRL range. This technique is especially powerful when you're not sure what context matters."

### Facilitator Notes
- Keep both conversations open -- you'll reference them during the debrief
- The [Instruction], [Context], [Constraints] labels are optional in real use -- they're training wheels. Mention this: "You don't have to literally write [Instruction] -- it's just a way to organize your thinking while you're learning."

---

## Segment 2: Team Exercise 1.2 -- "Prompt Makeover" (11:35 - 12:10, 35 min)

### Instructions to Give (5 min)

> "Go back to the prompts you wrote in Exercise 1.1 -- the ones where you asked Copilot something the natural way. Each team member is going to rebuild their prompt using ICC structure, and then try the 'ask me questions first' approach for the same task."

> "So for each person's task, you'll have three versions:"
Post in the meeting chat:
```
Version A: Original prompt (from Exercise 1.1)
Version B: Rebuilt with ICC structure
Version C: "Ask me questions first" approach
```

> "Compare the three outputs. Which one is best? Why? Document the winning prompt."

> "Work individually on the rewriting, but help each other. If your teammate is struggling with what context to include, brainstorm together. You have 25 minutes."

### During the Exercise (25 min)

**Breakout-room visits -- spend ~4-5 min per team:**

**What to look for and coach:**

*Instruction issues:*
- Too vague: "Help me with reporting" --> coach to "Draft the executive summary section of an 18-month periodic report for a Horizon Europe project"
- Multiple instructions crammed together --> coach to split into separate prompts or prioritize

*Context issues:*
- Missing role/institution: "Add a sentence about who you are and what programme you're working with"
- Missing specifics: "What's the project about? How many partners? What's the budget?"
- Too much irrelevant context: "Focus on what the AI needs to know to do THIS specific task"

*Constraint issues:*
- No format specified: "Do you want bullet points, a narrative, a table? Tell it."
- No length: "How long should this be? A paragraph? A full page? Specify."
- Missing must-include items: "What does a good version of this always contain?"

**Common coaching conversations:**

If a team is stuck on context:
> "Think about it this way: if you were handing this task to a brand-new colleague who just started today, what would you need to tell them before they could do it?"

If a team is debating ICC vs. "ask me questions":
> "They're not competing techniques. ICC is for when you know what you need. 'Ask me questions' is for when you're not sure. Use both -- start with 'ask me questions' to discover what context matters, then build that into an ICC prompt you can reuse."

If a team member's original prompt was already quite good:
> "Great -- now help your teammates. What made yours work well? Can you help them identify what context to add?"

### Timing
- At 12:05, announce: "Five minutes left. Make sure you've documented your best prompt for the share-out."

---

## Segment 3: Plenary Share-Out (12:10 - 12:30, 20 min)

### Facilitation Script

> "Each team, show us your best before-and-after. I want to see the original prompt and the improved version, and hear what changed. Two minutes per team."

**For each team (2-3 min each):**
1. Team reads their original prompt
2. Team reads their ICC or question-first version
3. Team briefly describes what improved in the output
4. You add one coaching comment

**Coaching comments to prepare (use the one most relevant per team):**

- "Notice how adding your role -- research manager vs. general public -- completely changed the vocabulary and specificity of the output."
- "The constraint about format was the game-changer here. Same content, but now it's in a format you can actually use."
- "Great use of 'ask me questions first.' You discovered context you wouldn't have thought to provide."
- "This is a prompt you could reuse every time this task comes up. That's the beginning of a prompt library."
- "The word/character count constraint is small but powerful -- it forces the AI to prioritize and be concise."

**Closing:**
> "Save these prompts. After lunch, we'll learn how to use AI itself to make them even better. And we'll start building a library of these so you never have to start from scratch again."

---

# LUNCH (12:30 - 13:30)

During lunch:
- Review team prompts from the shared docs -- identify the strongest examples for afternoon reference
- Prepare the meta-prompting demo (have ChatGPT and Copilot open side by side)
- Set up the Exercise 1.3 task assignments (post or share the team-specific tasks table)

---

# MODULE 1.4 | Level 2 -- The Prompt Crafter, Part 2: Meta-Prompting & Iteration
**Time: 13:30 - 15:00 (90 min)**

## Learning Objectives
- Participants can use one AI tool to generate optimized prompts for another (meta-prompting)
- Participants can use the "reverse prompt" technique to extract reusable prompts from successful conversations
- Each team has at least 2 refined, reusable prompt templates for their domain

---

## Segment 1: Demo -- Meta-Prompting with ChatGPT + Copilot (13:30 - 13:50, 20 min)

### Setup
- ChatGPT Free open in one browser window
- Microsoft 365 Copilot open in another
- Arrange side-by-side on your screen if possible

### Facilitation Script

**Introduce meta-prompting (3 min):**
> "Here's a mind-bending idea: you can use AI to write better prompts for AI. This is called meta-prompting. You describe the task you need done, and one AI writes the optimal prompt for another AI to execute."

> "Why would you do this? Because the AI knows what information it needs better than you do. It will include context and constraints you wouldn't think of."

**Live Demo Part 1 -- Meta-prompting (8 min):**

Switch to ChatGPT. Type:
```
I need to use an AI assistant to help me draft the narrative impact
section of an EU project's periodic report. The project is a Horizon
Europe RIA in Cluster 4 (Digital, Industry, Space), focused on
AI-assisted manufacturing. We are at the 18-month mark.

Write the optimal prompt I should use with the AI assistant, including
all the context and constraints that would produce the best result.
The prompt should instruct the AI to write a draft that aligns with
EU reporting requirements and evaluation criteria.
```

Let ChatGPT generate the meta-prompt. Read through it with the group.

> "Look at what it included. [Point out specific elements.] It added things like 'reference the Description of Action,' 'align with expected impacts listed in the work programme,' 'use quantitative indicators where possible.' These are things an experienced grant writer would know to include, and the AI just gave them to us for free."

Now copy the generated prompt. Switch to Microsoft 365 Copilot. Paste it in. Let Copilot generate the response.

> "So ChatGPT wrote the prompt, Copilot executed it. We used one AI's strength -- ChatGPT is excellent at structured prompt generation -- to get the best out of another AI's strength -- Copilot is excellent at grounded, contextual writing and can draw on your Microsoft 365 content."

**Live Demo Part 2 -- The Reverse Prompt (7 min):**

> "Now let me show you the second technique. Sometimes you have a long conversation with Copilot -- back and forth, refining, adding details -- and you finally get a great result. But it took 15 messages to get there. You don't want to repeat that process next time."

If you have a pre-prepared long conversation, open it. If not, simulate briefly:

Open a new Copilot conversation. Have a brief exchange (3-4 messages) about drafting a project summary, where you iteratively add context. Then type:

```
This final output is exactly what I needed. Write the single prompt
that would have gotten us to this result on the first try. Include
all the context and constraints we discovered during our conversation.
Format it so I can copy-paste it and reuse it next time.
```

Show the result.

> "This is gold. You just turned a 15-minute iterative conversation into a one-shot prompt you can reuse forever. Save it. This is how you build a prompt library."

**Handling questions (2 min):**

Common questions:
- "Can I use Copilot for meta-prompting too?" -- Yes, but using a different AI helps because it won't have the same biases or blind spots. It's also a good practice run with multiple tools.
- "What if the meta-prompt is too long?" -- You can ask it to be more concise. But longer, more specific prompts usually produce better results.

---

## Segment 2: Team Exercise 1.3 -- "The Prompt Factory" (13:50 - 14:30, 40 min)

### Setup
- Share the task assignment table on your screen
- Each team should have both ChatGPT and Copilot open

### Instructions to Give (5 min)

> "Each team has two tasks assigned from your domain."

Display or read:

| Team | Task 1 | Task 2 |
|------|--------|--------|
| A - Grants | Draft a call eligibility checklist | Write a go/no-go decision memo |
| B - Compliance | Summarize ethics requirements for a human-subjects project | Draft an informed consent template |
| C - Reporting | Write a publishable project summary from a technical report | Create a KPI tracking narrative |
| D - Communication | Draft a press release for a granted project | Write a stakeholder newsletter section |
| E - Data Mgmt | Draft a data management plan outline | Write a data sharing agreement summary |

> "For EACH task, follow this workflow:"
Post in the meeting chat:
```
1. Go to ChatGPT --> ask it to write the optimal prompt for this task
2. Review the meta-prompt as a team --> refine it (add missing context)
3. Paste the refined prompt into Copilot --> execute it
4. Read the output --> iterate if needed (ask Copilot to adjust)
5. When satisfied, use the reverse prompt technique to capture the final prompt
6. Save the final prompt -- this goes in your prompt library
```

> "Each team member should lead on different steps. One person drives ChatGPT, another drives Copilot, the third reviews and takes notes. Switch roles for Task 2."

> "You have 35 minutes. Try to complete both tasks."

### During the Exercise (35 min)

**Breakout-room visit priorities:**

**Minutes 0-10: Ensure teams get started correctly**
- Check that teams are using ChatGPT for the meta-prompt, not writing the prompt themselves
- If a team skips straight to Copilot: "Pause -- let's try the meta-prompting approach first. Go to ChatGPT and describe the task you need done."

**Minutes 10-20: Coach on refinement**
- Look at the meta-prompts ChatGPT generated. Are teams just blindly copying them?
- Coach: "Read through the meta-prompt before pasting it into Copilot. Is anything missing? Does it know what kind of institution you're at? Does it know the specific programme or funder?"
- If a team's Copilot output is mediocre: "What context could you add? Look at the output -- what's wrong with it? Tell Copilot specifically what to fix."

**Minutes 20-30: Ensure reverse prompt technique is being used**
- Check that teams are asking Copilot to write the reusable prompt
- Common mistake: teams just save the output, not the prompt. Remind them: "The output is for today. The prompt is forever."

**Minutes 30-35: Wrap up**
- Teams should have 2 saved prompts
- If a team only completed one task: that's fine. Quality over quantity.

**Troubleshooting:**

| Problem | Solution |
|---------|----------|
| ChatGPT is slow or rate-limited | Have another team member try on their account; or use Copilot itself for meta-prompting this time |
| Team can't think of context for their task | Ask: "If you were training a new colleague on this task, what would you tell them? What documents would you show them?" |
| Copilot's output is too generic despite good prompt | Add an example: "Here's an example of a good [output type]..." or add the constraint "Do not be generic. Be specific to [their context]." |
| Team finishes both tasks early | Challenge: "Now try running your best prompt in Gemini or Perplexity. How does the output compare?" |

---

## Segment 3: Debrief & Prompt Library Introduction (14:30 - 14:50, 20 min)

### Facilitation Script

**Quick share (10 min):**
> "Let's hear one highlight from each team. What was the most useful prompt you created? And did the meta-prompting approach add anything you wouldn't have included yourself?"

Call on each team briefly (2 min each). Listen for:
- Teams that were surprised by what ChatGPT included in the meta-prompt
- Teams that found the reverse prompt technique particularly useful
- Teams that noticed different output quality between ChatGPT and Copilot

**Prompt Library concept (5 min):**
> "You now have at least 4 refined prompts -- 2 from this exercise, and 2 from the ICC exercise this morning. Tomorrow, these go into Obsidian as your team's Prompt Library. A prompt library is exactly what it sounds like: a collection of tested, refined prompts organized by task type."

> "Think about it: how many times do you draft a go/no-go memo in a year? How many partner search announcements? How many budget justifications? Every one of those tasks can have a ready-made prompt that gets you 80% of the way there in one shot."

> "By the end of this course, each team will have 10+ prompts in their library. That's a genuine work tool you take home."

**Discussion question (5 min):**
> "Quick discussion: which tasks benefit MOST from a saved prompt? What makes a task a good candidate for prompt-ification?"

Guide toward:
- Tasks you do repeatedly (monthly reports, call assessments)
- Tasks with consistent structure (emails to PIs, compliance summaries)
- Tasks where you always forget something (checklists, review criteria)
- Tasks you delegate to junior staff (prompt becomes a training tool)

---

# BREAK (15:00 - 15:15)

During break:
- Prepare the 4-tool comparison demo (have Copilot, ChatGPT, Gemini, Perplexity ready)
- Select one prompt from the afternoon exercises that will work well across all tools
- Share the comparison matrix template on your screen

---

# MODULE 1.5 | Comparison & Critical Evaluation
**Time: 15:15 - 16:15 (60 min)**

## Learning Objectives
- Participants understand that different AI tools have different strengths
- Participants can critically evaluate AI outputs for accuracy, completeness, and fitness for purpose
- Teams have a reference for which tool to use for which task type

---

## Segment 1: Demo -- The Same Prompt, Four Tools (15:15 - 15:30, 15 min)

### Setup
- Four browser tabs open: Copilot, ChatGPT, Gemini, Perplexity
- Select a mid-complexity research management prompt. Recommended:
```
What are the key differences between Research and Innovation Actions
(RIA) and Innovation Actions (IA) in Horizon Europe? Include funding
rates, TRL expectations, consortium requirements, and evaluation
criteria differences. Format as a comparison table.
```

### Facilitation Script

> "We've been primarily using Copilot today, with ChatGPT as our meta-prompter. But here's a Level 4 insight coming early: different AI tools give you different results for the same prompt. Let me show you."

Paste the same prompt into all four tools simultaneously (or as fast as you can). While they generate:

> "Watch the differences. Same prompt, same words, four tools."

Once all four have responded, walk through the comparison:

**Copilot:**
> "Look at Copilot's response. [Point out specifics.] Typically strong on grounded, careful drafting -- it can weave in your Microsoft 365 content and flags caveats. The table is well-structured and thorough."

**ChatGPT:**
> "ChatGPT's version. [Point out specifics.] Often gives a clean, well-formatted table quickly. May include a helpful summary paragraph. Sometimes more concise."

**Gemini:**
> "Gemini. [Point out specifics.] May include additional detail from its training data. Good at structured extraction. Sometimes adds context you didn't ask for -- which can be useful or distracting."

**Perplexity:**
> "And Perplexity. [Point out specifics.] Look at the bottom -- citations. Every claim has a source you can click and verify. This is the only tool here that shows you WHERE it got its information. For factual questions about regulations and policies, this is invaluable."

> "None of these is 'the best.' They're different. The skill is knowing which to reach for. We'll build a reference for this."

**Ground truth check with the Horizon Dashboard (3 min):**

> "One more thing. Let me show you something critical."

Open the Horizon Dashboard (dashboard.tech.ec.europa.eu). Navigate to the statistics section that shows success rates or funding rates for the topic area in your prompt.

> "Look at this number. This is from the EU's official Horizon Dashboard -- the authoritative source. Now let's compare: did any of our four AI tools get this number right? [Check each tool's response.] Did Perplexity cite this source? Did Copilot or ChatGPT give the right figure, or an approximation?"

If any tool got the number wrong:
> "This is exactly why we verify. An AI told you a number with total confidence, and it was [wrong / outdated / approximated]. The Horizon Dashboard is your ground truth for EU funding statistics. Always check."

If all tools got it right:
> "Good -- they all agree, and they match the official source. But that's not always the case. Make a habit of spot-checking quantitative claims."

### Facilitator Notes
- Don't be dogmatic about which tool is best for what -- let participants form their own views
- If any tool gives a clearly wrong answer, point it out: "This is why we cross-reference. No AI is 100% reliable."
- The Horizon Dashboard moment is designed to create a lasting impression about verification -- make it concrete by showing an actual number comparison

---

## Segment 2: Team Exercise 1.4 -- "AI Tool Comparison Matrix" (15:30 - 16:05, 35 min)

### Instructions to Give (5 min)

> "Each team: pick one of your refined prompts from this afternoon -- ideally one that's representative of your domain. You're going to run it across all four tools and fill in a comparison matrix."

Display the matrix template:

| Criterion | Copilot | ChatGPT | Gemini | Perplexity |
|-----------|--------|---------|--------|------------|
| Accuracy (factually correct?) | /5 | /5 | /5 | /5 |
| Completeness (all aspects covered?) | /5 | /5 | /5 | /5 |
| Tone/Style (appropriate for your use?) | /5 | /5 | /5 | /5 |
| Source citations (can you verify claims?) | /5 | /5 | /5 | /5 |
| Actionability (can you use this output directly?) | /5 | /5 | /5 | /5 |
| **Best for this specific task?** | Y/N | Y/N | Y/N | Y/N |
| **Notes** | | | | |

> "One extra step: if your prompt involves any quantitative claims -- success rates, funding amounts, participation numbers -- open the Horizon Dashboard and verify at least one number from each tool. Add a row to your matrix:"

| Verified against Dashboard? | Y/N | Y/N | Y/N | Y/N |

> "Divide the work: one person runs Copilot and ChatGPT, another runs Gemini and Perplexity, the third reviews all four outputs, checks the Dashboard, and fills in the matrix. You have 25 minutes."

### During the Exercise (25 min)

**Breakout-room visits:**

**What to watch for:**
- Teams just filling in numbers without actually reading the outputs: "Tell me WHY you gave this a 3 for accuracy. What specifically was wrong or missing?"
- Teams assuming longer output = better output: "Is the extra length actually useful, or is it padding?"
- Teams ignoring Perplexity's citations: "Click one of those source links. Does the source actually say what Perplexity claims? This is how you verify AI claims."

**Key coaching moments:**

On accuracy:
> "If Copilot says the overhead rate is 25% and Perplexity cites a source saying it's 25%, that's corroboration. If they disagree, that's a red flag -- check the source."

On actionability:
> "Could you paste this output into an email or document and send it with minor edits? Or would you need to rewrite it significantly?"

On critical evaluation:
> "None of these tools is an authority. They're assistants. The research manager is still the expert. Your job is to evaluate, not just accept."

**If teams finish early:**
> "Now try a second prompt -- something very different from the first. Does the tool ranking change? For example, Perplexity might win for factual queries but lose for creative writing tasks."

---

## Segment 3: Plenary Discussion (16:05 - 16:15, 10 min)

### Facilitation Script

> "Let's build a collective reference. Each team: which tool won for your task, and why?"

Go around the teams in the main meeting. After each team shares, jot the result on the shared whiteboard:

```
Task Type                    | Best Tool  | Why
-----------------------------|------------|----
[Team A's task]              | [tool]     | [reason]
[Team B's task]              | [tool]     | [reason]
...
```

After all teams have shared:

> "See the pattern? [Identify any patterns -- e.g., Perplexity tends to win for factual/regulatory questions, Copilot tends to win for drafting, etc.] This is a living reference. As you use these tools more, you'll refine your own sense of which tool to grab for which job."

> "One more thing: you can also combine tools. Use Perplexity to get the facts with citations, then feed those facts into Copilot to draft the document. That's the workflow approach we'll build on Day 3."

**Save the shared whiteboard or the collective reference -- it will be useful on Day 3.**

---

# MODULE 1.6 | Day 1 Wrap-Up & Obsidian Introduction
**Time: 16:15 - 17:00 (45 min)**

## Learning Objectives
- Every participant has Obsidian installed with the course vault template
- Participants can create notes, use basic linking, and navigate the vault
- Participants complete their Day 1 reflection

---

## Segment 1: Obsidian Setup (16:15 - 16:45, 30 min)

### Setup
- The vault template ZIP at a download link posted in Teams
- Your own Obsidian open with the template vault loaded
- Step-by-step setup slides or checklist to share on screen

### Facilitation Script

**Distribution (5 min):**
> "Last activity for today: setting up your knowledge management tool. This is Obsidian -- it's a free app that stores your notes locally as simple text files. Unlike Google Docs or Notion, your data stays on YOUR computer. And it has a powerful feature: you can link notes to each other, creating a web of connected knowledge."

> "Grab the vault template from the download link in Teams. If you haven't installed Obsidian yet, do that first -- obsidian.md, download, install."

Walk them through:
1. Download/copy the ZIP file
2. Extract it to a folder they'll remember (e.g., Documents/AI-Research-Admin-Course)
3. Open Obsidian --> "Open folder as vault" --> select the extracted folder

**Guided Tour (15 min):**

Once everyone has the vault open (help stragglers -- this is where the team-of-3 structure helps, as faster members assist slower ones):

> "Let me walk you through the structure."

Share your screen, have them follow along:

```
/00-Prompts          -- your prompt library lives here
/01-Templates        -- reusable document templates
/02-Tool-Notes       -- your notes on each AI tool
/03-Workflows        -- workflow documentation (Day 2-3)
/04-Team-Project     -- team deliverables
/05-Daily-Reflections -- your learning journal
```

**Demo 1: Creating a note (3 min)**
> "Let's create your first prompt note. Click into the /00-Prompts folder. Click 'New note.' Title it something like 'Grant Call Eligibility Checklist Prompt' -- or whatever your best prompt from today was."

> "Paste your best prompt from today into the note. Below it, add a line: 'Output quality: 4/5' and a brief note about when to use this prompt."

**Demo 2: Linking (3 min)**
> "Now, the magic of Obsidian. In your prompt note, type two square brackets: [[ -- see the dropdown? You can link to any other note. Link to your tool notes or to related prompts."

Show how to create a link: [[Copilot]] or [[Tool Comparison Matrix]]

> "These links build a web of knowledge. The more you link, the more useful it becomes."

**Demo 3: Graph View (2 min)**
> "Press Ctrl+G (or Cmd+G on Mac) to see Graph View. Right now it's sparse, but by Day 3, you'll see a connected web of all your prompts, workflows, and tools."

Show the graph view briefly.

**Plugin check (2 min):**
> "The vault template comes with three plugins pre-installed: Templates, Dataview, and Kanban. We'll use these tomorrow. For now, just confirm they're enabled: go to Settings --> Community Plugins --> check that all three are turned on."

Check in with each team and verify. Common issues:
- "Community plugins aren't enabled" --> Settings --> Community Plugins --> Turn on community plugins --> Enable each plugin
- "I can't find the plugins" --> They may need to be installed if the vault template didn't include them. Show the Community Plugins browse/search feature.

**Quick practice (5 min):**
> "Take 5 minutes now. Transfer at least one prompt from your shared team document into your Obsidian vault. Create a note in /00-Prompts. If you finish quickly, start a note in /02-Tool-Notes for one of the AI tools you used today."

Drop into breakout rooms and help. This is just about getting comfortable with the basic mechanics.

---

## Segment 2: Day 1 Reflection (16:45 - 17:00, 15 min)

### Facilitation Script

> "Final task for Day 1. Create a new note in /05-Daily-Reflections/ called 'Day1'. Answer three questions -- just a few sentences each:"

Share on your screen:
```
1. What surprised you most today about AI?
2. What is your most useful prompt so far? (link to it!)
3. What research management task do you most want to tackle with AI
   during this course?
```

> "This is for you, not for me. But it's important: writing down what you learned helps it stick, and question 3 will guide your focus for the rest of the course."

Let them write quietly for 10 minutes.

**Closing (5 min):**
> "Great first day. You started at Level 1 -- asking AI questions like Google. You're now solidly at Level 2 -- you understand prompt structure, you've used meta-prompting, you've compared tools, and you've started building a prompt library."

> "Tomorrow, we go to Level 3: you'll build persistent AI workspaces as Copilot Notebooks, learn to analyze complex documents with NotebookLM and Gemini, do research intelligence gathering with Perplexity, and connect everything in Obsidian. See you at 9 AM."

---

## End-of-Day Facilitator Debrief (do this after participants log off)

- [ ] Review all teams' shared documents -- note quality of prompts, any teams that struggled
- [ ] Identify 1-2 prompts per team that could be highlighted tomorrow
- [ ] Check that all participants have Obsidian working (follow up via email with anyone who had issues)
- [ ] Review the collective tool-task fit reference from the whiteboard -- you'll build on this Day 3
- [ ] Pre-load your Copilot Notebook demo for Module 2.2 (working brief, sample sources added)
- [ ] Pre-load your NotebookLM demo notebook for Module 2.3 (3 sample documents uploaded, some questions already asked)
- [ ] Prepare the Day 2 quiz questions:
  - What does ICC stand for?
  - What is meta-prompting?
  - What does the "reverse prompt" technique give you?
  - Name two situations where you'd use the "ask me questions first" approach.

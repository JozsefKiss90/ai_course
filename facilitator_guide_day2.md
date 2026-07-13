# Facilitator Guide -- Day 2: Depth & Context
## Level 3 "The Power User"

---

# Pre-Day Checklist

- [ ] Day 1 debrief notes reviewed -- know which teams need extra support
- [ ] Claude Project demo pre-loaded: "Horizon Europe Grant Assistant" with custom instructions and 2-3 uploaded files (call topic PDF, budget template)
- [ ] NotebookLM demo notebook pre-loaded: 3 source documents uploaded (Horizon Europe call topic PDF, work programme section, Programme Guide chapter), some questions already asked
- [ ] Google Gemini: full Model Grant Agreement PDF ready for upload (100+ pages)
- [ ] Perplexity AI: test your three demo queries to ensure they return current, cited results
- [ ] Horizon Dashboard: pre-load the statistics page for your demo cluster/call topic; test CSV export; have a specific success rate number ready to cross-reference with Perplexity results
- [ ] Obsidian demo vault updated: mature version with links, Dataview queries, Kanban board, and session log template pre-configured
- [ ] Sample documents prepared for each team (in case they didn't bring their own or documents are insufficient):
  - Team A: Horizon Europe call topic text, sample budget spreadsheet
  - Team B: Ethics review guidelines PDF, GDPR excerpt, AI Act summary
  - Team C: Sample periodic report, Description of Action excerpt, KPI framework
  - Team D: Institutional brand guidelines, sample press release, project summary
  - Team E: Funder data policy, institutional DMP template, FAIR principles overview
- [ ] Quiz questions for Day 1 recap printed or on slide
- [ ] Day 3 capstone scenario briefs printed (one per team) for Module 2.7

---

# MODULE 2.1 | Recap & Level 3 Introduction
**Time: 09:00 - 09:30 (30 min)**

## Learning Objectives
- Participants recall and can apply Day 1 concepts (ICC, meta-prompting, reverse prompt)
- Participants understand the Level 2 --> Level 3 transition: from one-off prompts to persistent workspaces

---

## Segment 1: Rapid Recap (09:00 - 09:10, 10 min)

### Facilitation Script

**Interactive quiz (5 min):**
> "Quick warm-up. I'll ask four questions -- shout out the answers."

1. "What does ICC stand for?" --> Instruction, Context, Constraints
2. "What is meta-prompting?" --> Using one AI to write prompts for another AI
3. "What does the reverse prompt technique give you?" --> A reusable single prompt that captures everything from a long conversation
4. "When would you use the 'ask me questions first' approach?" --> When you're unsure what context matters, or for complex tasks

If the room is quiet, call on specific teams.

**Team prompt showcase (5 min):**
> "Each team: hold up or read your single best prompt from yesterday. The one you're most proud of. No explanation needed -- just the prompt."

Let each team read theirs quickly. Brief applause or acknowledgment. This reinforces Day 1 learning and creates continuity.

---

## Segment 2: Level 3 Framing (09:10 - 09:30, 20 min)

### Facilitation Script

**The Level 2 wall (5 min):**
> "Yesterday you learned to write great prompts. Here's the problem: every time you open a new conversation with Claude, you start from zero. It doesn't remember that you're a research manager. It doesn't remember your institution's rules. It doesn't remember the prompts you refined yesterday."

> "Imagine if every time you walked into your office, your colleagues had complete amnesia. You'd have to re-introduce yourself, re-explain your projects, re-describe your role. Every. Single. Day. That's what using AI at Level 2 feels like."

**The Level 3 solution (5 min):**
> "Level 3 solves this. The key concept is persistent context -- giving the AI a workspace that remembers who you are, what you're working on, and how you want it to behave. In Claude, this is called Projects. In ChatGPT, it's Custom GPTs. The AI retains instructions and reference files across every new conversation."

> "Today is about building these workspaces and learning to use specialized tools for specialized jobs. By the end of today, you'll have:"
Write on whiteboard:
```
1. A Claude Project configured for your team's domain
2. A NotebookLM notebook analyzing your core documents
3. A long-context analysis from Gemini
4. A citation-backed intelligence briefing from Perplexity
5. An Obsidian vault connecting everything together
```

**Live contrast demo (10 min):**

Open Claude Desktop. Start a new conversation (NOT in a Project). Type:
```
Draft a 200-word summary of our project's progress for the mid-term review.
```
Show the response -- it's generic, asks for details, can't be specific.

> "See? It doesn't know anything about 'our project.'"

Now switch to your pre-loaded Claude Project ("Horizon Europe Grant Assistant"). Start a new conversation within the Project. Type the same thing:
```
Draft a 200-word summary of our project's progress for the mid-term review.
```
Show the response -- it references the uploaded documents, uses the right terminology, follows the custom instructions.

> "Same prompt. Completely different result. The Project already knows the context. That's the difference between Level 2 and Level 3."

> "Now let's build yours."

---

# MODULE 2.2 | Claude Projects for Research Management
**Time: 09:30 - 11:00 (90 min)**

## Learning Objectives
- Participants can create a Claude Project with custom instructions and reference files
- Participants understand how to write effective custom instructions for their domain
- Teams have a working, tested Claude Project for their research management area

---

## Segment 1: Demo -- Building a "Grant Writing Assistant" Project (09:30 - 09:55, 25 min)

### Setup
- Claude Desktop open, logged in
- If you have a pre-built Project, delete it or start fresh so you can build live
- Have your custom instructions text ready to type (or paste in segments)
- Have 2-3 sample files ready to upload

### Facilitation Script

> "I'm going to build a Claude Project from scratch, step by step. Follow along on your screens -- you'll be building your own version in a few minutes."

**Step 1: Create the Project (3 min)**

Navigate to the Projects section in Claude. Click "New Project."
> "Name it something clear and specific. I'm calling mine 'Horizon Europe Grant Assistant.' Not just 'Work' or 'AI stuff' -- you want to know exactly what this workspace is for."

Set the name. Show where the description field is.

**Step 2: Write Custom Instructions (10 min)**

> "This is the most important part. Custom instructions tell Claude how to behave EVERY TIME you start a new conversation in this Project. Think of it as briefing a new team member on their first day."

Type the instructions, explaining each section as you go:

```
You are an experienced EU research management advisor working with
university research offices. You specialize in Horizon Europe
collaborative projects (RIAs and IAs).
```
> "First: who is Claude in this context? An EU research management advisor. This sets the vocabulary, the level of expertise, and the frame of reference."

```
When drafting text:
- Use formal but clear EU project language
- Follow standard proposal section structures (Excellence,
  Impact, Implementation)
- Flag common evaluation pitfalls
- Reference current Horizon Europe rules (General MGA,
  HE Programme Guide)
```
> "Second: how should it draft text? I'm specific about tone, structure, and behavior. 'Flag common evaluation pitfalls' means it will proactively warn me about things evaluators look for."

```
When reviewing text:
- Check alignment with evaluation criteria
- Identify vague claims that need quantification
- Suggest concrete improvements, not generic advice
```
> "Third: how should it review my text? I don't want 'this is good, maybe add more detail.' I want it to find vague claims and tell me to quantify them."

```
Output formatting:
- Use headers and bullet points for readability
- Include word/character counts when relevant
- Mark assumptions clearly with [ASSUMPTION] tags
```
> "Fourth: formatting rules. The [ASSUMPTION] tag is particularly useful -- when Claude isn't sure about something, I want it to mark it clearly rather than just making something up."

> "A tip: you can use ChatGPT to help draft these instructions. Describe your role and what you need, and ask it to write Claude Project custom instructions for you. Meta-prompting strikes again."

**Step 3: Upload Reference Files (5 min)**

> "Now we add reference files. These are documents that Claude can access in every conversation within this Project."

Upload your sample files:
1. A Horizon Europe call topic (PDF)
2. A budget template (Excel or PDF)
3. Optionally: a sample proposal section or institutional guidelines

> "A few rules about files: Claude can read PDFs, text files, and code files. There are size limits on the free tier. For very large documents -- like a full 200-page Programme Guide -- you might want to upload just the relevant chapter, or use Gemini for the full document."

> "What makes good reference files? Things you reference repeatedly: call texts, templates, institutional SOPs, style guides, policy documents."

**Step 4: Test It (7 min)**

Start a new conversation in the Project. Type:
```
Based on the uploaded call topic, draft a 500-word excellence
section outline identifying 3 key objectives and their alignment
with the call expected outcomes.
```

Let the response generate. Point out:
> "Look -- it references the call topic I uploaded. It uses the terminology from the document. It follows the formatting rules from my instructions. And it flagged an [ASSUMPTION] about TRL levels because the call wasn't specific."

Start ANOTHER new conversation in the same Project. Type:
```
What are the three biggest risks in our budget approach for this call?
```

> "New conversation, but it still knows the call, still follows my instructions. I didn't have to re-explain anything. That's persistent context."

---

## Segment 2: Team Exercise 2.1 -- "Build Your Domain Project" (09:55 - 10:40, 45 min)

### Instructions to Give (5 min)

> "Now it's your turn. Each team is going to build a Claude Project for your domain. Here are your assignments."

Display:

| Team | Project Name | Key Focus |
|------|-------------|-----------|
| A | Grant Lifecycle Hub | Grant writing, call analysis, budget rules |
| B | Compliance Advisor | Ethics review, regulatory frameworks, documentation |
| C | Reporting Workspace | EU reporting standards, impact metrics, periodic reports |
| D | Comms & Dissemination | Institutional voice, audience adaptation, messaging |
| E | Data Management Office | FAIR principles, DMP standards, repository selection |

> "Here's your workflow for the next 40 minutes:"
```
1. DRAFT custom instructions (10 min)
   - Use ChatGPT meta-prompting: describe your domain and role,
     ask it to write Claude Project instructions
   - Review and refine as a team

2. BUILD the Project in Claude (5 min)
   - Create the Project, paste in your instructions
   - Upload 2-3 reference files (your own documents or the samples
     in the shared drive)

3. TEST with 3 different conversations (15 min)
   - Conversation 1: Ask it to draft something (test writing quality)
   - Conversation 2: Ask it to analyze/review something (test analytical quality)
   - Conversation 3: Ask it a domain-specific question (test knowledge application)

4. ITERATE (10 min)
   - What didn't work? Refine the instructions.
   - What context was missing? Add it.
   - Run the test that failed again.
```

> "Important: only ONE team member creates the Project, since you're sharing an account or working on one person's account. The other two team members should be helping draft instructions and evaluating outputs. Take turns driving."

### During the Exercise (40 min)

**Priority table visits:**

**Minutes 0-10 (Instruction drafting phase):**

Common issue: teams go straight to Claude without meta-prompting.
> "Start in ChatGPT. Tell it: 'I'm a [role] at a [type of institution]. I need Claude Project custom instructions that make Claude behave as my [domain] assistant. Here's what I need it to do well: [list tasks].' Then refine what it gives you."

Common issue: instructions too vague.
> "I see 'Be helpful with compliance.' That's too broad. WHAT compliance? Which regulations? What types of projects? What does 'helpful' look like -- drafting documents? Reviewing documents? Answering questions?"

Coaching prompts per team:

**Team A (Grants):**
> "What specific grant tasks do you do most? Call analysis, proposal writing, budget preparation, consortium building? Pick the top 3 and write instructions for each."

**Team B (Compliance):**
> "Which regulations matter most? GDPR, ethics guidelines (Declaration of Helsinki?), AI Act, institutional review board procedures? Be specific about the regulatory framework."

**Team C (Reporting):**
> "What kind of reports? Periodic reports, final reports, financial reports? What sections do you struggle with most? Excellence achievements? Impact narrative?"

**Team D (Communication):**
> "Who are your audiences? Think about this: press, policymakers, general public, academic community, funders. Each needs different tone, vocabulary, and framing."

**Team E (Data Management):**
> "Which funder requirements do you deal with? Horizon Europe? National funders? Multiple? What repositories does your institution use? Be specific about FAIR implementation standards."

**Minutes 10-25 (Building and testing phase):**

Common issue: teams upload only one file.
> "Upload at least 2-3 files. The more context the Project has, the better it performs. What documents do you reference constantly in your work? Those are your reference files."

Common issue: first test conversation gives underwhelming results.
> "Don't abandon the Project -- iterate the instructions. What was wrong with the output? Was it the wrong tone? Too generic? Missing domain knowledge? Add a specific instruction to fix that."

Watch for instructions that are too restrictive:
> "If you tell it 'only answer based on uploaded files,' you're limiting it to a NotebookLM-style tool. You want Claude to combine its general knowledge WITH your specific documents. Say 'reference the uploaded files when relevant, but also draw on your knowledge of [domain].'"

**Minutes 25-40 (Iteration phase):**

Check that each team has:
- [ ] Custom instructions written and pasted
- [ ] At least 2 reference files uploaded
- [ ] At least 2 test conversations completed
- [ ] At least 1 instruction refinement made based on test results

If a team finishes early:
> "Try this: open a conversation and ask it to do something you've never prompted an AI for before. Something complex, something you thought AI couldn't handle. See what happens."

### Timing
At 10:35, give a 5-minute warning: "Start wrapping up. Pick the one query you want to show in the share-out."

---

## Segment 3: Share-Out (10:40 - 11:00, 20 min)

### Facilitation Script

> "Each team: 3 minutes. Show us your Project. I want to see three things:"
```
1. Your custom instructions (read the key parts)
2. One live query -- run it now and show the output
3. One thing you'd change or add based on testing
```

**For each team presentation, prepare one coaching comment:**

Possible comments:
- "Notice how [Team X] included specific document section references in their instructions -- that's why Claude's output follows the right structure."
- "I love that [Team X] added the instruction about flagging assumptions. That builds trust -- you know when the AI is guessing."
- "The instruction about audience adaptation is clever -- [Team D] can use the same Project for press releases and policy briefs by just specifying the audience in the conversation."
- "Great iteration -- the first version was too generic, and adding [specific instruction] fixed it. That's exactly the process: test, evaluate, refine."
- "For [Team X], I'd suggest adding an instruction about what NOT to do. For example: 'Do not use jargon that a non-specialist reviewer wouldn't understand' or 'Do not make claims without evidence from the uploaded sources.'"

**Closing:**
> "You now have a persistent AI workspace for your domain. Every new conversation inherits your instructions and files. You'll keep refining this throughout the course. Let's take a break, and then we'll learn a fundamentally different tool -- one that's grounded entirely in your documents."

---

# BREAK (11:00 - 11:15)

During break:
- Open your pre-loaded NotebookLM demo notebook
- Ensure the 3 demo documents are uploaded and the auto-summary has been generated
- Test the demo queries to make sure they work with your specific documents
- Have the Audio Overview feature ready to demonstrate (or pre-generate one if it takes time)

---

# MODULE 2.3 | NotebookLM -- Document Analysis & Knowledge Synthesis
**Time: 11:15 - 12:30 (75 min)**

## Learning Objectives
- Participants can create a NotebookLM notebook, upload sources, and ask source-grounded questions
- Participants understand the difference between NotebookLM (source-grounded) and Claude/ChatGPT (general knowledge + context)
- Teams have a working NotebookLM notebook for their domain with structured outputs

---

## Segment 1: Demo -- Analyzing a Funding Call with NotebookLM (11:15 - 11:35, 20 min)

### Setup
- NotebookLM open (notebooklm.google.com)
- Pre-loaded notebook with 3 sources:
  1. A Horizon Europe call topic (PDF)
  2. The relevant work programme section (PDF)
  3. A relevant chapter from the HE Programme Guide (PDF)

### Facilitation Script

**Introduction (3 min):**
> "NotebookLM is fundamentally different from Claude or ChatGPT. Those tools combine their training data -- everything they've ever been trained on -- with whatever you give them. NotebookLM does the opposite: it ONLY uses the documents you upload. Nothing else."

> "Why does this matter? Because when Claude says 'the overhead rate is 25%,' you don't know if that's from its training data, from a document you uploaded, or something it hallucinated. When NotebookLM says 'the overhead rate is 25%,' it shows you the exact sentence in the exact document where it found that. Click the citation, and you're looking at the source."

> "For research management -- where accuracy and traceability matter enormously -- this is a critical tool."

**Demo Step 1: Sources and auto-summary (3 min)**

Show your pre-loaded notebook. Point to the source panel:
> "I've uploaded three documents: the call topic text, the work programme section for this cluster, and the relevant chapter from the Programme Guide. NotebookLM automatically generated a summary and identified key topics. Let me show you."

Click on the auto-generated summary/overview. Read a few bullet points:
> "It's already identified the key themes across all three documents. This took seconds -- doing this manually would take an hour."

**Demo Step 2: Source-grounded questions (7 min)**

Ask the first question:
```
What are the mandatory deliverables mentioned across all sources?
```
Show the response. Point to the citation numbers:
> "See these numbers? Each one links to a specific passage in a specific document."

Click one citation. Show where it opens the source document and highlights the exact passage:
> "I can verify every claim. If I'm preparing a proposal, I know exactly which document requires which deliverable."

Ask the second question:
```
What are the TRL expectations for this call?
```
Show the response and citations.

> "Now watch what happens when I ask something that ISN'T in the documents:"
```
What is the success rate for this type of call?
```
Show how NotebookLM either says it can't find this in the sources, or provides only what the sources mention:
> "It won't make something up. It tells you when the information isn't in your documents. That's the safety net."

**Demo Step 3: Audio Overview (3 min)**

> "One more feature that's surprisingly useful. NotebookLM can generate a podcast-style audio summary of your sources. Two AI voices discuss the key points from your documents."

If pre-generated, play 30-60 seconds of the Audio Overview.
> "This is useful for getting a quick overview, sharing with colleagues who don't want to read documents, or reviewing while commuting. You can even customize the discussion focus."

**Demo Step 4: Structured output (4 min)**

Ask:
```
Create a structured briefing note from these sources. Include:
sections for eligibility criteria, expected outcomes, evaluation
weights, mandatory deliverables, and budget constraints. Use bullet
points and cite the source document for each item.
```
Show the structured output with citations throughout.
> "This is a document you could share with a PI or a project team. Every claim is sourced, every requirement is traceable."

---

## Segment 2: Team Exercise 2.2 -- "Deep Document Dive" (11:35 - 12:15, 40 min)

### Instructions to Give (5 min)

> "Each team: create a NotebookLM notebook for your domain. Upload the documents relevant to your work."

Display the assignment table:

| Team | Sources to Upload | Analysis Tasks |
|------|------------------|----------------|
| A | Call text + work programme + Programme Guide | 1. Extract eligibility criteria 2. List expected outcomes 3. Identify evaluation weights 4. Create a go/no-go checklist from the documents |
| B | Ethics guidelines + institutional policy + GDPR excerpt | 1. Map compliance requirements by category 2. Find gaps between institutional and funder rules 3. Create a compliance cross-reference table |
| C | 2 periodic reports + project Description of Action | 1. Cross-reference achievements vs. planned deliverables 2. Flag delays or deviations 3. Draft a gap analysis summary |
| D | 3 project summaries + dissemination plan template | 1. Identify common impact narratives across projects 2. Extract reusable communication angles 3. Create a messaging framework |
| E | Data policy (funder) + institutional DMP policy + FAIR guidelines | 1. Compare requirements across all three sources 2. Identify conflicts or gaps 3. Build a consolidated compliance checklist |

> "Workflow:"
```
1. Upload sources (5 min) -- use your own documents or the samples
   in the shared drive
2. Review auto-generated summary (3 min)
3. Ask 5 targeted questions -- evaluate the citations for each (15 min)
4. Generate ONE structured output: a briefing note, checklist,
   or comparison table (10 min)
5. Optional: generate an Audio Overview
```

> "Divide roles: one person uploads and navigates, one formulates questions, one evaluates citation accuracy. Rotate."

### During the Exercise (35 min)

**Table visit priorities:**

**Minutes 0-8 (Upload phase):**

Common issue: "We don't have documents to upload."
> "Use the sample documents in your team's shared Google Drive folder. Or upload something from your real work -- even a policy document from your institution's website."

Common issue: uploading too many documents at once.
> "Start with 2-3 focused documents. You can always add more. Too many sources can dilute the answers."

Common issue: documents won't upload.
> "Check the file format -- NotebookLM accepts PDFs, Google Docs, and text files. If your document is in Word, convert it to PDF first. There's also a size limit -- very large PDFs may need to be split."

**Minutes 8-25 (Questioning phase):**

Coach on question quality:
> "Don't ask vague questions like 'What is this document about?' Ask specific, actionable questions: 'What are the mandatory deliverables listed in section 5.2?' or 'Compare the data retention requirements across the GDPR excerpt and the funder policy.'"

Key coaching moments:

For **Team A**: "Ask NotebookLM to compare the call topic's expected outcomes with the evaluation criteria in the work programme. Are they aligned? Any gaps?"

For **Team B**: "Ask it to find all instances where the institutional policy is MORE restrictive than the funder's requirements. These are the ones that trip people up."

For **Team C**: "Ask it to list every deliverable from the Description of Action and then check whether the periodic reports mention the status of each one. That's a gap analysis."

For **Team D**: "Ask it to extract the strongest impact claims from each project summary and identify what makes them effective. Look for quantified outcomes."

For **Team E**: "Ask it to create a side-by-side comparison of data handling requirements from each source. Where do they agree? Where do they differ?"

**Watch for citation verification:**
> "Don't just accept the answer -- click at least two citations. Does the source passage actually say what NotebookLM claims? This is critical for building trust in the tool."

**Minutes 25-35 (Structured output phase):**

Ensure each team generates at least one structured deliverable. If they're stuck:
> "Ask NotebookLM: 'Create a [briefing note / checklist / comparison table] based on all uploaded sources. Include [specific sections]. Cite the source document for each item.'"

### Timing
At 12:10, give a 5-minute warning.

---

## Segment 3: Debrief (12:15 - 12:30, 15 min)

### Facilitation Script

**Quick observations (5 min):**
> "What did you discover? Any surprises?"

Take 2-3 observations from the room. Likely themes:
- "The citations are really useful -- I can trace every claim"
- "It found something in the document I hadn't noticed"
- "It couldn't answer questions about things not in the documents"

**Tool positioning (10 min):**

Draw a simple comparison on the whiteboard:

```
NotebookLM                  Claude Projects              Perplexity
- Only YOUR sources         - Your files + general       - Live web search
- Every claim cited           knowledge                  - Every claim cited
- No hallucination risk     - More creative/flexible     - Current information
- Can't go beyond docs      - Can hallucinate            - Can't use YOUR docs
- Best for: document        - Best for: drafting,        - Best for: research,
  analysis, compliance,       creative writing,            fact-checking,
  audit trails                brainstorming                discovery
```

> "These three tools complement each other perfectly. NotebookLM tells you what's IN your documents. Claude helps you WRITE and CREATE based on that knowledge. Perplexity tells you what's happening IN THE WORLD right now. Level 3 means knowing when to use which one."

> "After lunch, we'll work with Gemini for long documents and Perplexity for research intelligence. Then we'll connect everything in Obsidian."

---

# LUNCH (12:30 - 13:30)

During lunch:
- Prepare the Gemini demo: have your 100+ page document ready to upload
- Test the Gemini demo queries with your specific document
- Prepare the Perplexity demo queries -- test them for current, relevant results
- Review each team's NotebookLM notebooks if accessible -- note any issues for afternoon coaching

---

# MODULE 2.4 | Long-Context Work with Google Gemini
**Time: 13:30 - 14:30 (60 min)**

## Learning Objectives
- Participants understand Gemini's advantage for processing very long documents
- Participants can perform cross-section extraction and structured analysis on long documents
- Participants can articulate when to use Gemini vs. NotebookLM vs. Claude for document work

---

## Segment 1: Demo -- Processing a Full Grant Agreement (13:30 - 13:45, 15 min)

### Setup
- Google Gemini open (gemini.google.com)
- Full Model Grant Agreement PDF ready (100+ pages) -- use the Horizon Europe Annotated Model Grant Agreement if possible
- Alternative: any long policy/regulatory document

### Facilitation Script

**Context setting (2 min):**
> "Gemini's superpower is its context window -- how much text it can process at once. While Claude and ChatGPT can handle moderate-length documents, Gemini can process up to a million tokens. That's roughly 750,000 words, or a 1,500-page book."

> "For research management, this matters when you're working with: full grant agreements, complete programme guides, multi-hundred-page regulatory documents, or multiple documents at once."

**Upload and demonstrate (13 min):**

Upload the full MGA PDF to Gemini.
> "I'm uploading the full Annotated Model Grant Agreement -- over 100 pages. Let's see what Gemini can do with it."

Wait for processing, then run three queries in sequence:

**Query 1 -- Structured extraction:**
```
Summarize all financial reporting obligations and their deadlines
in a table format with columns: Obligation, Article Reference,
Deadline/Timing, and Key Requirements.
```
Show the result:
> "It pulled information from across the entire document and organized it into one table. Doing this manually would take hours."

**Query 2 -- Cross-section analysis:**
```
List all articles that mention consortium obligations. For each,
create a row with: Article number, obligation type, who is
responsible (coordinator vs. all beneficiaries), and consequences
of non-compliance.
```
Show the result:
> "This is cross-referencing across dozens of articles. It's finding connections between sections that even experienced research managers might miss."

**Query 3 -- Comparative analysis within the document:**
```
Compare the reporting requirements in Article 20 with the
deliverable schedule obligations. Identify any potential
conflicts or timing issues.
```
Show the result:
> "It's analyzing relationships between different parts of a 100-page legal document. This is where long-context processing really shines."

### Facilitator Notes
- If Gemini gives incomplete results, show this as a learning moment: "Even with a large context window, very complex queries sometimes need to be broken down. Let's try asking about just Article 20 first."
- If upload fails due to file size: have a shorter version ready, or split the document

---

## Segment 2: Team Exercise 2.3 -- "The Long Document Challenge" (13:45 - 14:15, 30 min)

### Instructions to Give (3 min)

> "Each team: find your longest, most complex document. If you have a grant agreement, programme guide, or thick policy document -- that's ideal. If not, use a combination of your team's documents uploaded together."

> "Three tasks:"
```
1. Full-document summary: Upload the document to Gemini and ask
   for a structured summary with sections and key points (10 min)

2. Cross-section extraction: Ask a question that requires pulling
   information from multiple parts of the document (10 min)
   Examples: "List all deadlines mentioned anywhere in the document"
             "Find all sections that discuss financial rules"

3. Tool comparison: Take the SAME question and ask it in Claude
   (or NotebookLM if you uploaded the same doc there). Compare
   the results. (10 min)
```

> "Document your findings in your Obsidian tool notes -- /02-Tool-Notes/Gemini.md"

### During the Exercise (27 min)

**Table visits -- key coaching:**

**If Gemini gives a very general summary:**
> "Be more specific in your request. Instead of 'summarize this document,' try 'create a section-by-section summary with key obligations, deadlines, and defined terms for each section.'"

**If teams don't have long documents:**
> "Upload multiple shorter documents at once. Ask Gemini to cross-reference them -- 'compare the requirements in Document A with the requirements in Document B.'"

**For the tool comparison task:**

Coach teams to notice:
- Does Gemini find information Claude missed (or vice versa)?
- Are there factual discrepancies between the tools' answers?
- Which tool's format/structure is more useful?
- Which tool is faster?

> "The point isn't which tool is 'better' -- it's understanding what each is best at. If you need to quickly scan a 200-page document, Gemini is your tool. If you need to deeply analyze 3 specific documents with citations, NotebookLM is better. If you need to write something based on a document, Claude Projects wins."

---

## Segment 3: Discussion (14:15 - 14:30, 15 min)

### Facilitation Script

> "What did you discover? Where did Gemini excel, and where did it struggle?"

Guide the discussion toward practical decision-making:

**Draw a decision tree on the whiteboard:**
```
How long is the document?
|
+-- Short (< 20 pages) --> Claude Project (upload as reference file)
|
+-- Medium (20-100 pages) --> Claude OR Gemini (either works)
|
+-- Long (100+ pages) --> Gemini for exploration, then extract
                          key sections for Claude/NotebookLM
|
Multiple documents to cross-reference?
|
+-- Yes, need citations --> NotebookLM
+-- Yes, need creative synthesis --> Claude Project
+-- Yes, very long docs --> Gemini
```

> "This decision tree goes in your Obsidian vault. By Day 3, you'll instinctively know which tool to reach for."

---

# MODULE 2.5 | Research Discovery with Perplexity AI
**Time: 14:30 - 15:15 (45 min)**

## Learning Objectives
- Participants can use Perplexity for verified, citation-backed research management intelligence
- Participants understand Perplexity's unique value: live web search with source attribution
- Teams produce a structured intelligence briefing with citations

---

## Segment 1: Demo -- Research Management Intelligence Gathering (14:30 - 14:40, 10 min)

### Setup
- Perplexity AI open (perplexity.ai)
- Three demo queries ready

### Facilitation Script

**Positioning (2 min):**
> "Perplexity is the tool for when you need CURRENT, VERIFIABLE information. Unlike Claude, which draws on training data that might be months old, Perplexity searches the live web and cites every source."

> "For research management, this is invaluable for: tracking policy changes, monitoring success rates, benchmarking against other institutions, and staying current on regulatory developments."

**Demo queries (8 min):**

Run three queries in sequence, spending ~2.5 min on each:

**Query 1:**
```
What are the success rates for ERC Starting Grants in 2024 and 2025
by domain?
```
Show the response. Point out:
> "Every number has a citation. I can click through to the ERC's own statistics pages. I don't have to trust the AI -- I can verify."

**Query 2:**
```
What changes were introduced in the Horizon Europe 2025 work
programme for Cluster 6?
```
Show the response:
> "This is current information -- within the last few months. No LLM training data would have this."

**Query 3:**
```
Compare the open access policies of Horizon Europe, NSF, and NIH
as of 2025. Format as a comparison table.
```
Show the response:
> "Cross-referencing multiple funder policies with live source verification. This would take you an afternoon of searching funder websites. Perplexity does it in seconds."

> "A critical note: always click at least one or two citations and verify. Perplexity is very good, but occasionally a source may not say exactly what the AI claims. Trust but verify."

**Cross-reference with the Horizon Dashboard (5 min):**

Open the Horizon Dashboard (dashboard.tech.ec.europa.eu).

> "Remember the Horizon Dashboard from our Day 1 tool tour? Let me show you how it works alongside Perplexity."

Navigate to the statistics section for the same topic as Query 1 (ERC success rates). Pull the official numbers.

> "Perplexity told us [X]% success rate. The Dashboard says [Y]%. [If they match:] Good -- they agree. [If they differ:] See that? Perplexity's number might be from a slightly different calculation or a secondary source. The Dashboard is the official EU data."

Show the CSV export feature:
> "You can also export Dashboard data as CSV. Watch this."

Export a CSV. Then switch to Claude Desktop and upload it:
```
I'm uploading a CSV export from the Horizon Dashboard showing success
rates by call topic for Cluster 4 over the past 3 years. Analyze
the trends: which topics have the highest and lowest success rates?
Are rates increasing or decreasing? Which topics are most competitive?
Format as a briefing with a summary table.
```

Show the response:
> "This is powerful: official EU data, analyzed by AI, in seconds. The Dashboard gives you the raw truth. AI tools give you the analysis and narrative. Together, they're a research management intelligence system."

> "Team A, take note -- you'll be using this exact approach in your capstone workflow tomorrow."

---

## Segment 2: Team Exercise 2.4 -- "Intelligence Briefing" (14:40 - 15:05, 25 min)

### Instructions to Give (3 min)

> "Each team: you're going to produce a 1-page intelligence briefing on a current topic in your domain. Use Perplexity as your primary research tool."

Display:

| Team | Research Question |
|------|------------------|
| A | What are the latest trends in EU funding success rates and common proposal weaknesses identified by evaluators? (Also: download success rate data from Horizon Dashboard, upload CSV to Claude for trend analysis, and cross-reference with Perplexity findings) |
| B | What are the newest EU regulations affecting research ethics and data protection in 2025-2026? |
| C | What frameworks are European universities using to measure research impact beyond publications? |
| D | What are the best practices for research communication and public engagement in EU projects? |
| E | What are the latest developments in FAIR data implementation and open science mandates? |

> "Your briefing should include:"
```
- Executive summary (3-4 sentences)
- Key findings (5-7 bullet points)
- Implications for your institution (3-4 bullet points)
- Sources (at least 5 verified citations)
```

> "Workflow: use Perplexity to research, then structure the briefing in Claude (paste the Perplexity findings as context), and save the final version in Obsidian at /04-Team-Project/Intelligence-Briefing.md"

### During the Exercise (22 min)

**Table visits:**

**Key coaching:**

On query refinement:
> "If the first result is too general, use follow-up queries to drill down. Perplexity maintains context within a thread. Ask: 'Focus specifically on [sub-topic]. What does [specific institution or source] say about this?'"

On citation verification:
> "Have one team member click through the top 3 citations while another works on follow-up queries. Verify that the sources actually say what Perplexity claims."

On structuring the briefing:
> "Once you have enough Perplexity results, copy the key findings and paste them into Claude with the instruction: 'Organize these research findings into a structured intelligence briefing for research management administrators at a European university. Include an executive summary, key findings, and implications for our institution.'"

On using the Horizon Dashboard (especially Team A):
> "Go to dashboard.tech.ec.europa.eu. Find the statistics for your cluster or call topic. Export the data as CSV. Upload it to Claude and ask for a trend analysis. Then compare those official numbers with what Perplexity told you. Which source is more current? More detailed? Do they agree?"

If other teams want to use the Dashboard:
> "Any team can use it. Team C, look at project completion rates and deliverable statistics. Team E, check open access compliance rates. The Dashboard has data relevant to every domain."

On the combined workflow:
> "This is your first multi-tool workflow! Horizon Dashboard for official data --> Perplexity for research context --> Claude for analysis and writing --> Obsidian for storage. Notice how each tool does what it's best at."

**If teams finish early:**
> "Try a second, more specific query. Or try asking Perplexity to compare your institution's practices with the best practices it found."

### Timing
At 15:00, announce: "5 minutes. Make sure your briefing is at least in draft form in Obsidian."

---

## Segment 3: Brief Share (15:05 - 15:15, 10 min)

> "Quick round: each team, read your executive summary -- the 3-4 sentence version. And tell us: what was the most surprising finding?"

One minute per team. No deep discussion -- just awareness of what each team found.

---

# BREAK (15:15 - 15:30)

During break:
- Open your mature demo Obsidian vault with Dataview queries, Kanban, and session logs
- Have the session log template ready to show
- Prepare the Dataview query example

---

# MODULE 2.6 | Obsidian as a Knowledge Management Hub
**Time: 15:30 - 16:30 (60 min)**

## Learning Objectives
- Participants can create internal links, use templates, and view the knowledge graph
- Participants set up an AI Session Log template and Kanban project board
- Participants experience the "connected knowledge" insight -- how linking creates emergent value

---

## Segment 1: Demo -- The Connected Knowledge Base (15:30 - 15:50, 20 min)

### Setup
- Your mature demo vault open in Obsidian (not the participants' starter vault -- this is a "what it looks like when it's built out" demo)
- Pre-configured examples of each feature you'll demo

### Facilitation Script

**The knowledge connection concept (3 min):**
> "You've been creating great content all day -- prompts, briefings, tool comparison matrices, project instructions. Right now, these are isolated notes. The real power of Obsidian is turning isolated notes into connected knowledge."

> "Let me show you what a well-developed vault looks like."

**Demo 1: Internal linking in context (4 min)**

Open a note called "Horizon Europe Budget Rules." Show how it contains links:
> "See these blue links? [[Grant Writing Prompts]] takes me to my prompt library entry for budget-related prompts. [[Budget Template]] takes me to the actual template file. [[Compliance Checklist]] links to the list of financial compliance items."

> "Every note is connected to the notes it relates to. When I'm working on a budget and I need my prompts, one click. When I need the compliance checklist, one click."

Click through a few links to show the navigation.

> "To create a link, type [[ and start typing the name of any note in your vault. Obsidian autocompletes it."

Create a new link live: type [[Perplexity Intelligence Briefing]] in a note.

**Demo 2: Templates plugin (5 min)**

> "Templates save you from creating the same note structure repeatedly."

Open Settings --> Templates. Show the template folder.

Open your "AI Session Log" template:
```
---
date: {{date}}
tool:
task:
prompt:
output_quality: /5
---

## Key Learnings

## Follow-up Actions

## Links
- Related prompts:
- Related workflows:
```

> "Every time I have an AI session, I create a new note from this template. It pre-fills the date and gives me the structure. Let me show you."

Create a new note, apply the template. Fill in a few fields quickly.

> "Over time, these session logs become a searchable record of everything you've tried, what worked, and what didn't."

**Demo 3: Dataview plugin (4 min)**

> "Dataview lets you automatically query your vault. Watch this."

Open a note called "Dashboard" that contains:
````
```dataview
TABLE tool, output_quality, task
FROM "session-logs"
WHERE output_quality >= 4
SORT output_quality DESC
```
````

Show the auto-generated table:
> "This automatically finds every session log where I rated the output 4 or higher, and displays them in a table. It updates in real time as I add new logs."

> "You don't need to learn any programming for this. I'll give you the query to copy-paste."

**Demo 4: Kanban plugin (2 min)**

Open a Kanban board:
```
| To Do | In Progress | Done |
|-------|-------------|------|
| Build Claude Project | Test NotebookLM | Complete tool comparison |
| Create Canva visual | | Write prompt library |
```

> "This is your project management board for the capstone project tomorrow. You'll set this up in the exercise."

**Demo 5: Graph View (2 min)**

Press Ctrl+G. Show the graph:
> "This is every note in my vault and every connection between them. The clusters show related topics. The orphan dots are notes that aren't linked to anything yet -- which tells me I should connect them."

> "Your graph will look sparse right now, but by tomorrow evening it will start showing real structure."

---

## Segment 2: Team Exercise 2.5 -- "Vault Architecture" (15:50 - 16:20, 30 min)

### Instructions to Give (5 min)

> "Time to build out your vaults. Five tasks in 25 minutes:"

Write on whiteboard:
```
1. TRANSFER all outputs into Obsidian (10 min)
   - Prompts from Day 1 --> /00-Prompts/
   - Intelligence briefing --> /04-Team-Project/
   - Tool comparison matrix --> /02-Tool-Notes/
   - Any other notes or outputs

2. LINK related notes (5 min)
   - In each prompt note, add links to the tools used
   - In the intelligence briefing, link to the prompts that produced it
   - In tool notes, link to relevant prompts and outputs

3. SET UP the AI Session Log template (3 min)
   - Create a template note in /01-Templates/
   - Use the structure I showed you (copy from the projector)
   - Log 3 sessions from today retroactively

4. CREATE a Kanban board for Day 3 (5 min)
   - Create a new note in /04-Team-Project/ called "Capstone Board"
   - Add columns: To Do, In Progress, Done
   - Add your Day 3 capstone tasks as cards

5. EXPLORE Graph View (2 min)
   - Open Graph View and see the connections emerging
```

### During the Exercise (25 min)

**Table visits:**

**Common issues and solutions:**

| Issue | Solution |
|-------|----------|
| "I can't remember how to create a link" | Type [[ and start typing the note name |
| "How do I create a note from a template?" | New note --> click the template icon (or Ctrl+T if configured) --> select template |
| "The Dataview query doesn't work" | Check that the plugin is enabled. The query syntax must be in a code block with "dataview" as the language |
| "Kanban board doesn't appear" | Create a new note, then in the three-dot menu choose "Toggle Kanban board" |
| "I don't know what to link" | "Think about it this way: if you were reading this note and wanted more information about something mentioned in it, what would you click on?" |

**Quality checks per table:**
- [ ] At least 5 notes in the vault
- [ ] At least 3 internal links created
- [ ] Session log template created
- [ ] At least 1 session log filled in
- [ ] Kanban board started

**If teams struggle with Kanban:**
Walk them through: Create new note --> type the title "Capstone Project Board" --> go to the note menu (three dots) --> select "Add Kanban Board" or similar option depending on the plugin version. Add lists: "To Do", "In Progress", "Done". Add cards to "To Do" based on their capstone scenario.

---

## Segment 3: Share-Out (16:20 - 16:30, 10 min)

> "Quick screen-shares. Each team, show us your Graph View for 30 seconds. Then one thing that surprised you about connecting your notes."

Call on each team. Celebrate the graphs, even if they're sparse:
> "That's 2 days of knowledge, already showing structure. Imagine what this looks like after a month of use."

---

# MODULE 2.7 | Day 2 Wrap-Up & Day 3 Preview
**Time: 16:30 - 17:00 (30 min)**

## Learning Objectives
- Teams understand the Day 3 capstone project requirements
- Teams have a plan for Day 3 with assigned roles
- Participants capture Day 2 reflections

---

## Segment 1: Day 3 Team Project Briefing (16:30 - 16:50, 20 min)

### Facilitation Script

> "Tomorrow is Day 3 -- and it's where everything comes together. Let me tell you what you're building."

**The capstone concept (5 min):**
> "Each team will build a complete, documented, multi-tool AI workflow for a realistic scenario in your domain. By 'complete,' I mean:"

Write on whiteboard:
```
YOUR WORKFLOW MUST:
1. Chain at least 3 different AI tools in a defined sequence
2. Include reusable prompts saved in your prompt library
3. Produce a tangible output artifact (document, visual, tool)
4. Be documented in Obsidian well enough for a colleague to follow
5. Include a visual summary created in Canva
6. Include an interactive tool built as a Claude Artifact
7. Mark all human quality gates explicitly
```

**Distribute scenario briefs (5 min):**
Hand out or display each team's scenario. Read the scenarios briefly:

> "Team A: A new Horizon Europe call has been published. You'll build the complete workflow from call discovery to go/no-go decision to proposal outline."

> "Team B: A new project involving human participants, AI systems, and cross-border data transfer. Build the complete compliance assessment and documentation package."

> "Team C: An EU-funded project is approaching its 18-month periodic report deadline. Build the workflow for assembling, drafting, and quality-checking the report."

> "Team D: A major research project has produced breakthrough results. Build the communication workflow from scientific output to public-facing content across channels."

> "Team E: A new consortium needs a comprehensive data management plan. Build the complete DMP workflow."

**Day 3 schedule (3 min):**
```
09:00 - 09:45  Level 4 intro & workflow design framework
09:45 - 10:30  Canva AI workshop (visual outputs)
10:45 - 11:45  Claude Artifacts workshop (interactive tools)
11:45 - 12:30  Capstone work session (Part 1)
13:30 - 15:00  Capstone work session (Part 2)
15:15 - 16:30  Presentations (12+3 min per team)
16:30 - 17:00  Synthesis & wrap-up
```

**Team planning time (7 min):**
> "Use the remaining time to plan. Assign roles within your team:"
```
Role 1: TOOL LEAD -- responsible for the AI tool execution
         (who runs which tools when)
Role 2: DOCUMENTATION LEAD -- responsible for Obsidian documentation,
         prompt saving, workflow capture
Role 3: PRESENTATION LEAD -- responsible for the Canva visual,
         the demo, and the team presentation
```

> "Also, update your Kanban board in Obsidian with your Day 3 tasks. What needs to happen, in what order?"

### During Planning
Walk around and verify:
- Each team understands their scenario
- Roles are assigned
- Teams are thinking about the tool sequence (which tool first, second, third)
- Kanban boards are being updated

**Common concern:** "We can't build all of this in one day."
> "You don't have to build everything from scratch. You already have a Claude Project, a NotebookLM notebook, refined prompts, and an intelligence briefing. Reuse everything from Days 1 and 2. Day 3 is about connecting what you've already built into a workflow and adding the new pieces: Canva visual and Claude Artifact."

---

## Segment 2: Day 2 Reflection (16:50 - 17:00, 10 min)

> "Last task: create /05-Daily-Reflections/Day2.md in Obsidian. Three questions:"

Display:
```
1. Which tool felt most valuable for YOUR work today? Why?
2. What was the most surprising thing you discovered in your
   documents using NotebookLM, Gemini, or Perplexity?
3. How has your view of AI tools changed since yesterday morning?
```

> "See you tomorrow at 9 AM. Come ready to build."

---

## End-of-Day Facilitator Debrief

- [ ] Review each team's Claude Project instructions -- note any that need significant improvement
- [ ] Check Obsidian vaults if possible -- are teams set up correctly for Day 3?
- [ ] Review the capstone scenario briefs -- do any teams need additional sample documents?
- [ ] Prepare the Canva demo for Module 3.2 (have a Claude-generated text ready to design)
- [ ] Prepare the Artifact demo for Module 3.3 (test the readiness checklist Artifact)
- [ ] Set up the presentation order for Module 3.5 (alphabetical by team, or reverse, or draw)
- [ ] Prepare peer evaluation forms for the presentations
- [ ] Check the timing: 5 teams x 15 min = 75 min exactly for the presentation block
- [ ] Prepare the "Level 5 Self-Study Path" handout for Module 3.6
- [ ] Prepare the final course evaluation form

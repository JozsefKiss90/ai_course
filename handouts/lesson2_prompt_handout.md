# From unfamiliar videos to a lesson

## Example prompts for the Lesson 2 assignment

Sample material: four transcribed videos from Sandeep Swadia's channel. Lane: Daily Driver (Gemini), because the material is public. Nothing here is required. Every prompt is an example you may run, adapt or discard.

---

## 1. What this handout is for

The Lesson 2 assignment asks you to chain the course's tools into one workflow and deliver an educational presentation on a topic of your choice. This handout covers one specific case of that assignment: the material you start from is unfamiliar. Nobody in the cohort has watched these videos, and the facilitator has watched one.

That is the point of the exercise. A research manager receives unfamiliar material all the time: a new call text, a partner's report, a recorded webinar. The skill is turning it into something a colleague can learn from, without reading every word twice and without trusting the model's summary blindly.

The prompts below apply the Lesson 1 techniques to that job. Each prompt carries a tag naming its technique, the blueprint step it serves, and the pitfall it protects against. The assignment's eight-step roadmap stays the route. These prompts only fill in the "how" for steps 1, 3, 4, 5, 6 and 7 when the input is a stack of transcripts.

**Technique tags used in this handout**

| Tag | Lesson 1 technique | One line |
|---|---|---|
| ASK | Ask-me-first | The model interviews you before it answers |
| META | Meta-prompting | The model writes the prompt, you run it |
| PERSONA | Persona pattern | A role sets vocabulary, priorities and depth |
| EXAMPLE | Example-driven pattern | One good example beats a paragraph of description |
| STEPS | Step-by-step pattern | Forced intermediate steps improve reasoning |
| CRITIQUE | Critique-then-improve | Diagnose first, then repair only what is broken |
| REVERSE | Reverse prompt | Turn a good conversation into one reusable prompt |

---

## 2. The material and the lane

The folder holds four transcripts, between 2,600 and 3,100 words each, about 11,300 words in total. A fifth video from the same channel, the 7 Levels of AI, was the course map in Lesson 1 and is not part of this stack.

The transcripts are auto-captions. They have no punctuation, they mishear product names, and each one contains a sponsor segment, a newsletter plug and a sign-off. Every prompt below assumes that noise and tells the model what to do with it.

**Routing.** Public YouTube content goes to the Daily Driver. If you add your own notes, meeting minutes or institutional examples, they pass through step 2 of the blueprint first. Prompt Coach may see any prompt below, but only the prompt, never the transcript.

**Context.** All four transcripts fit in one Gemini chat. Do not paste them together for extraction. Process one transcript per chat, save the output as a file, then open a fresh chat for the synthesis. Lesson 1's rule applies: fewer, better tokens win, and the middle of a long chat gets lost.

**NotebookLM option.** If your free tier supports it, add the four videos as YouTube sources instead of the transcript files. The notebook then cites the video and the timestamp. The prompts below work unchanged.

---

## 3. The sorting tray

Every extraction prompt in this handout sorts the material into the same seven categories. Naming the categories once, and reusing them in every prompt, is what makes the outputs of different chats fit together at the synthesis step.

| Category | What it is | What to do with it |
|---|---|---|
| Core idea | The claim the whole video rests on | Keep. One sentence, in your words |
| Framework | A named model or acronym the speaker teaches | Keep. Expand the acronym, list its parts |
| Technique | Something a learner can execute, often a prompt | Keep. Rewrite as an instruction |
| Evidence claim | A study, a number, a named person or company | Keep, flag for verification |
| Illustration | A story, anecdote or metaphor | Keep at most one per core idea |
| Opinion | The speaker's stance or motivation | Keep only if it changes what a learner should do |
| Noise | Sponsor, newsletter, channel promotion, sign-off | Drop |

A rule of thumb from the material itself: one of the videos describes a book as a trunk, branches and leaves. The core idea is the trunk, the frameworks and techniques are the branches, the stories are the leaves. Collect the trunk first. Leaves without a branch are the most common failure in a summary.

---

## 4. The loop every prompt runs in

None of these prompts is meant to be run once and accepted. Each one sits inside a short loop that chains the Lesson 1 techniques. Run the loop at every blueprint step where a prompt is involved.

```
   1. META      Describe the job. Ask the model to write the prompt.
        |
   2. ASK       Run that prompt with "ask me first" appended. Answer.
        |
   3. RUN       Take the answer. Check it against the sorting tray.
        |
   4. CRITIQUE  "List the three biggest weaknesses, then fix only those."
        |
   5. REVERSE   "Write the one prompt that would have got us here."
        |
   6. SAVE      The reverse prompt goes into your Gem or prompt library.
        |
        +------> The output becomes the next step's input. Repeat.
```

The loop is a prompt chain. The output of one turn is the input of the next. The reverse prompt at the end is what makes the next run shorter. Prompt Coach can replace stage 4 for any prompt you are unsure about.

You do not need all six stages every time. A first-pass sort of a transcript may need only stages 2 and 3. The synthesis and the ranking deserve the whole loop, because those are the outputs the presentation is built on.

---

## 5. The prompts

Each prompt has the same shape. It states what it is for, its tags, the blueprint step that consumes its output, and the pitfall it avoids. Then comes the prompt text and what to check before the output moves on.

### Phase A. Orient before you read anything

#### A1. The triage interview

Tags: ASK, PERSONA. Serves blueprint step 1. Pitfall: starting to extract before you know what the lesson is for.

```
Act as an instructional designer who builds short lessons for
administrative professionals in a university.

I have four transcripts of talks about using AI well. I have not
watched the videos. I want to turn them into one standalone lesson
of at most 60 minutes for research management staff who have
completed an introductory session on prompting.

Before you do anything else, ask me the questions you need in order
to plan this well: about the audience, what they already know, what
the lesson must enable them to do, and what I want to leave out.
Ask one question at a time. Stop after five.
```

Check: write the answers down. They become the context block of every later prompt, and the "what they already know" answer is the Lesson 1 syllabus.

#### A2. Let the model write the extraction prompt

Tags: META. Serves steps 4 and 5. Pitfall: an extraction prompt that reads like "summarise this".

```
I need a prompt that I will run once per transcript, in a fresh chat.
The transcript is an auto-caption of a spoken talk: no punctuation,
misheard product names, a sponsor segment and a sign-off.

The prompt must make the model sort the content into these seven
categories: core idea, framework, technique, evidence claim,
illustration, opinion, noise. It must extract only domain knowledge
and drop the speaker's framing. It must return the result in a fixed
format I can paste into a table later.

Write the optimal prompt, including the context and constraints that
will produce the best result. Do not run it. Ask me first if any
detail is missing.
```

Check: read the generated prompt before running it. If it does not mention the seven categories by name, add them by hand.

#### A3. Three questions to carry in

Tags: ASK. Serves step 1. Pitfall: reading without a purpose, so the material decides what matters.

```
I am about to read four transcripts about working with AI in order
to teach research administrators how to use it well. Give me three
questions I should carry into the reading so that I read with a
purpose. Then ask me which of the three matters most, and why.
```

Check: keep the question you chose visible while you read. It is the mission sentence for the whole chain.

### Phase B. Categorise and extract, one transcript at a time

#### B1. The step-by-step sort

Tags: STEPS. Serves step 4. Pitfall: a summary that keeps every story and loses the frameworks.

```
Here is one transcript of a spoken talk. Work through it in this
order and show each step before moving to the next.

Step 1. List every named framework, acronym or model the speaker
teaches. Expand each acronym.
Step 2. List every technique a learner could execute, in the
speaker's words.
Step 3. List every evidence claim: a study, a number, a named person
or company. Quote it exactly.
Step 4. List the stories and metaphors, one line each.
Step 5. Mark which passages are sponsor content, newsletter promotion
or sign-off.
Step 6. Only now: state the one core idea the talk rests on, in one
sentence, in neutral language.

Do not skip a step. Do not merge steps.

[paste one transcript]
```

Check: compare step 1 against a keyword search of the transcript for capital-letter acronyms. The model sometimes invents a framework name or misses one buried in the middle.

#### B2. The knowledge card

Tags: EXAMPLE. Serves step 4. Pitfall: four transcripts extracted in four different formats that will not merge.

```
Below is one knowledge card in the exact format I want. Produce one
card like it for every framework and every technique in the
transcript that follows. Keep the field names. Leave a field empty
rather than inventing content for it.

--- EXAMPLE CARD ---
Name: AIM
Category: Framework
Parts: Actor (who the model acts as), Input (the context and data),
Mission (what it must do)
Learner can: write a three-part prompt instead of a one-line request
Overlaps with: the ICC structure from Lesson 1 (instruction, context,
constraints)
Evidence offered: none, speaker's experience
Best illustration: a résumé rewrite, one persona line, one input line,
one mission line
Verify: nothing to verify
--- END EXAMPLE ---

[paste one transcript]
```

Check: the "Overlaps with" field is where the work happens. A card that overlaps with a Lesson 1 concept is a reference back, not a new slide.

#### B3. Strip the channel voice

Tags: PERSONA, CRITIQUE. Serves step 5. Pitfall: a lesson that sounds like a YouTube pitch.

```
Act as an editor for a university training unit. The extracted notes
below use the speaker's rhetoric: "the top 1%", "dangerously smart",
"most people are doing it wrong".

First, list every phrase that is motivation or marketing rather than
content. Then rewrite the notes in neutral, plain language that a
staff-training handbook would use. Keep every framework, technique
and evidence claim intact. Change nothing else.

[paste the extracted notes]
```

Check: the rewrite must be shorter than the original. If it is longer, the model has added content.

#### B4. Check your own reading of the trunk

Tags: CRITIQUE. Serves step 4. Pitfall: the model confirming whatever interpretation you offer.

```
I think the load-bearing idea of this transcript is:
[your one-sentence interpretation]

Check my interpretation against the transcript. What did I miss?
What did I overstate? Where does the speaker say something different
from what I wrote? Do not agree with me unless the text supports it.
Quote the passages you rely on.

[paste the transcript]
```

Check: if the model agrees with you in every case, rerun with a deliberately wrong interpretation. If it agrees again, its agreement is worth nothing and you need a stricter prompt.

### Phase C. Rank and structure across the whole stack

Open a fresh chat for this phase. The inputs are the cards and notes from Phase B, not the transcripts.

#### C1. Merge and map to what the audience knows

Tags: STEPS, EXAMPLE. Serves step 5. Pitfall: teaching the same idea twice under two names.

```
Here are the knowledge cards from four talks, plus the syllabus of
the introductory session my audience has already attended.

Step 1. Group the cards that describe the same idea under different
names. For each group, name the idea once.
Step 2. Mark every group that the audience already knows from the
syllabus. Those become one-line references, not teaching content.
Step 3. List what remains: the ideas that are genuinely new to this
audience.
Step 4. For each new idea, state in one sentence why a research
administrator would use it.

Show every step.

[paste the cards]
[paste the Lesson 1 syllabus: ICC, the four patterns, ask-me-first,
reverse prompt, meta-prompting, tokens, context window, hallucination,
the 7 Levels]
```

Check: expect large overlaps. Several talks teach a three-part prompt, a few-shot example, a chain-of-thought instruction and an "ask me questions first" move. Those are Lesson 1 material and should surface in step 2.

#### C2. Rank by relevance, with criteria you chose

Tags: ASK, STEPS. Serves step 5. Pitfall: a ranking the model produced by its own unstated criteria.

```
I want to rank the new ideas by relevance for a 60-minute lesson.
Before you rank anything, ask me to weight these three criteria from
1 to 5: how new the idea is to the audience, how directly a research
administrator can apply it this week, and how strong the evidence
behind it is. Suggest a fourth criterion if you think one is missing.

Then rank the ideas, show the score per criterion, and mark the cut
line: which ideas fit in 60 minutes and which are left for a handout.
```

Check: the cut line is a decision you own. Move it if you disagree, and record why in the blueprint.

#### C3. Attack the ranking

Tags: CRITIQUE. Serves step 5. Pitfall: accepting the first ordering because it looks tidy.

```
Here is my ranked list and cut line. List the three biggest
weaknesses of this ranking against the learning outcomes below.
Consider: an idea that depends on one below the cut line, an idea
ranked high on novelty but with no evidence, and any two ideas that
should be taught as one.

Then propose the smallest change to the ranking that fixes those
three weaknesses. Do not rewrite the whole list.

[paste the ranking]
[paste the three learning outcomes]
```

Check: the fix must be small. If the model reorders everything, ask it again for the minimal change.

#### C4. Order into a standalone lesson

Tags: STEPS, PERSONA. Serves step 5. Pitfall: the video's order becoming the lesson's order.

```
Act as a curriculum designer. Take the ideas above the cut line and
order them so that a learner never meets an idea before its
prerequisite. Show the prerequisite dependencies first, as a list of
"A before B" pairs with the reason. Then give the lesson order as a
table: segment, idea, minutes, the outcome it serves, the one activity
the learner does, and how you would check they got it.

Total time at most 60 minutes. Cut anything that serves no outcome.
```

Check: every segment row must name an outcome. A row without one is a leaf without a branch. Cut it or merge it.

#### C5. Observable learning outcomes

Tags: CRITIQUE. Serves steps 1 and 6. Pitfall: outcomes that cannot be tested, such as "understand prompting better".

```
Here are my draft learning outcomes. For each one, say whether an
observer could tell that a learner has achieved it, and if not,
rewrite it so they could. Use a verb that names a visible action:
sort, write, choose, check, explain to a colleague. Stop at three.

[paste the draft outcomes]
```

Check: step 6 will build a quiz per outcome. An outcome you cannot quiz is not an outcome.

### Phase D. Turn structure into teaching material

#### D1. Draft one section at a time in Canvas

Tags: EXAMPLE, PERSONA. Serves step 5 and step 8. Pitfall: regenerating the whole outline every time one section changes.

```
Here is one finished section of my lesson in the style I want: one
core idea in plain language, one worked example from research
administration, one thing the learner does, one check.

Write the next section in the same style for the idea below. Keep the
same length. Use an example from grant administration, reporting or
partner coordination, not from the original talk.

[paste your finished section]
[paste the next idea from the lesson order]
```

Check: replace the example if it is generic. The talks use résumés, LinkedIn posts and start-ups. Your lesson should use calls, budgets and consortia.

#### D2. Learning material per outcome

Tags: STEPS. Serves step 6, in Study and Learn (Copilot Chat, Sensitive Lane tool; the content is public, so either lane is fine). Pitfall: quiz questions answerable without the lesson.

```
Explain this concept to a junior colleague in research
administration in under 200 words. Then produce five flashcards on
its key terms. Then write a five-question quiz. Every question must
require something taught in the explanation, not general knowledge.

[paste one idea and its section]
```

Check: try each question yourself without reading the explanation. Drop any you could answer.

#### D3. A harder quiz, borrowed from the material

Tags: STEPS. Serves step 6. Pitfall: a quiz with one difficulty level.

One of the talks proposes four levels of questioning, from a school test to a hostile interview. It makes a good closing exercise, and it demonstrates a technique from the material inside the lesson itself.

```
Quiz me on the concept below in four rounds. Round 1: as if I were a
school student. Round 2: as if I were a university student. Round 3:
as an interviewer for a senior administrative post. Round 4: as a
sceptical manager who thinks I am unprepared. One question per round,
wait for my answer, then tell me what I missed.

[paste one idea]
```

Check: keep round 3 or 4 for the presentation only if your learning outcome is at that level.

#### D4. Describe the visual, not the picture

Tags: EXAMPLE. Serves step 7. Pitfall: generated images with wrong or unreadable labels.

```
I need a diagram for a slide. Describe the relationship, not the
picture: [for example: a tray with seven labelled compartments, the
first three highlighted, arrows from a document into the tray].
Produce the image with no text inside it. I will add labels on the
slide.
```

Check: text inside generated images is often wrong. Ask for none, and label the image in the presentation tool.

### Phase E. Verify and close the loop

#### E1. Audit the evidence claims

Tags: STEPS. Serves the gate between every step. Pitfall: a slide that repeats a number the speaker got wrong.

```
Here are the evidence claims extracted from four talks. For each one:
1. State whether it is a checkable fact, a paraphrase of research,
or the speaker's opinion.
2. For a checkable fact, name the most likely primary source and
what to search for.
3. Rank your confidence that the claim is accurate, high, medium or
low, and say why.
4. List any assumption the speaker made that the claim depends on.

Do not confirm a claim you cannot trace.

[paste the evidence claims]
```

Check: open at least three sources yourself. A claim you could not trace goes on the slide as "the speaker reports", or not at all.

#### E2. Cross-model check

Tags: CRITIQUE. Serves the gate. Pitfall: one model's confident error going unchallenged.

```
Below is a lesson outline another AI produced from four transcripts I
will also paste. Find every place where the outline states something
the transcripts do not support, or leaves out a framework the
transcripts teach. Quote the transcript for each finding.

[paste the outline]
[paste the transcripts]
```

Check: run this in Copilot Chat if the outline contains nothing sensitive, or in a second Gemini chat. Different chats disagree more usefully than one chat asked twice.

#### E3. The reverse prompt for your Gem

Tags: REVERSE. Serves step 5 and your prompt library. Pitfall: doing the whole conversation again for the next set of videos.

```
We have reached a lesson outline I am satisfied with. Write the
single prompt that would have taken us from four raw transcripts to
this outline on the first attempt. Include the seven categories, the
audience, the exclusion of the audience's prior knowledge, the
ranking criteria I chose, and the 60-minute limit. Write it as
standing instructions for an assistant that will do this again.
```

Check: paste the result into a Gem as its instructions. Test it on one transcript you have already processed and compare the two outputs.

#### E4. The AI-use log

Tags: none. Serves the last slide of the presentation.

One line per step, written as you go, not afterwards:

```
Step | Tool | Lane | Date | Input | Prompt used (name from this
handout or your own) | What I checked before using the output
```

The log is the AI-use declaration the dean's directive asks for. It also tells the Lesson 3 debrief audience what you did.

---

## 6. Common pitfalls with this kind of material

- **Leaf collection.** The summary keeps the Beatles, the Formula 1 team and the boatman, and loses the five roles they illustrate. Sort the tray before you summarise.
- **Teaching Lesson 1 twice.** Three of the four talks teach a structured prompt under their own acronym. Map it to ICC in one line and move on.
- **Trusting the attributions.** "A Stanford study", "a Yale study", "a Harvard Business Review finding" appear without citations. Extract them, audit them, and label what you could not trace.
- **Pasting everything at once.** Four transcripts in one chat produce a merged summary that quietly drops the middle one, so keep one chat per transcript.
- **Letting the video order become the lesson order.** The talks are ordered for retention on YouTube, while your lesson is ordered by prerequisite.
- **Keeping the rhetoric.** "Dangerously smart" is a hook. A training handbook says "more capable". Run prompt B3.
- **Accepting a ranking with hidden criteria.** If you did not choose the weights, the model did, so run prompt C2 before C4.
- **Outcomes that cannot be tested.** If step 6 cannot write a quiz question for it, it is not an outcome.
- **Sponsor content as teaching content.** One talk spends several minutes on a sponsor's automation product, which is noise unless your topic is automation.

---

## 7. What the chain might look like

One possible route through the blueprint using these prompts. It is illustrative. Your blueprint records your own route and the steps you skipped.

| Blueprint step | Tool | Prompts used | Output passed on |
|---|---|---|---|
| 1. Frame the topic | Gemini, Guided Learning | A1, A3, C5 | Topic sentence, three outcomes |
| 2. Anonymise own material | None, by hand | none | Skipped if only the transcripts are used; say so |
| 3. Research the topic | Gemini, Deep Research | E1 sources | One cited briefing on the untraced claims |
| 4. Collect what to cover | NotebookLM or Gemini | B1, B2, B3, B4, one per transcript | Knowledge cards per video |
| 5. Draft the outline | Gemini Gem + Canvas | C1, C2, C3, C4, D1 | Lesson order with outcomes |
| 6. Learning material | Study and Learn | D2, D3 | Explanation, flashcards, quiz per outcome |
| 7. Visuals | Gemini image generation | D4 | One image per section that needs one |
| 8. Build | Canva, genspark.ai | none | The presentation, with E4 on the last slide |
| Any step | Prompt Coach | any prompt above | An improved prompt, if you can say what changed |

Close every phase with E3. The reverse prompt from the synthesis chat is the most valuable artefact of this assignment. It is the one you will run again.

---

## Appendix. The material at a glance

The inventory below is a starting point for prompt B1, not a substitute for it. It lists what each transcript names, not what it argues.

| Transcript | Length | Named frameworks and techniques |
|---|---|---|
| vid_1 | ~2,700 words | Machine English; AIM; MAP; chain-of-thought, verifier and refinement patterns; steering to experts; five verification checks; OCEAN |
| vid_2 | ~2,900 words | Intelligent laziness and two payoff curves; satisficing; DRAG; the intelligent hill from zero-shot to agents; the intelligent gym and progressive overload; the intelligent fool |
| vid_3 | ~3,100 words | University in a box; ALTER: advisor, librarian, tutor, editor, roommate; five advisor decisions; NotebookLM as librarian; a sponsored automation segment |
| vid_4 | ~2,600 words | Three myths of reading; three reading traps; ACTOR: aim, compress, test, own, run; trunk, branches and leaves |

Expect the merge in prompt C1 to find that the four talks share more than their acronyms suggest. Deciding what that shared core is, and how to teach it once, is the assignment.

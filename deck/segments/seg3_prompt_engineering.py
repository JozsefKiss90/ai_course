"""Segment 3 — Prompt engineering backdrop (25 min, live facilitator demo).

Nine slides supporting the live Gemini demo, per lesson_1.md Segment 3,
in session order: the problem space (the Horizon Europe worked example),
the three-way escalation (Demo 1), the ICC prompt verbatim, the
prompt-as-contract generalization, the two shortcut append-phrases, the
meta-prompting move, the four prompt patterns with their
research-management examples, the working-scale patterns & meta-prompting
case, and the two rules stated while demoing.

Three slides (The Problem Space, Prompting LLMs, Prompt Patterns &
Meta-Prompting) are ported from dist/ai_proposal_writing_horizon_europe.pptx
and redrawn in the deck's visual language; their notes weave them into the
Demo 1 / Demo 2 arc. The facilitator demos live; these slides anchor what
participants retain and copy. Demo-switch cues use template.add_demo_cue,
and the Two shortcuts notes carry the full minute-by-minute script for the
≈17-minute Demo 2 (Demo 1 gets ≈8 min).
"""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    AMBER, CONTENT_WIDTH, HIGHLIGHT, PALE, PALE_WARM, PRIMARY, SKY, TEXT, WHITE,
)


def _add_quote(card, text, color=PRIMARY):
    """Append the copy-this phrase to a card as its own quoted paragraph.

    Legacy heading colors remap for the dark canvas: navy quotes render
    light azure, orange quotes render amber."""
    if color == PRIMARY:
        color = SKY
    elif color == HIGHLIGHT:
        color = AMBER
    para = card.text_frame.add_paragraph()
    para.space_before = Pt(8)
    run = para.add_run()
    run.text = f"“{text}”"
    template.style(run, size=14, color=color, italic=True)
    return para


# --- Slide 1: the problem space (ported from the proposal deck) --------------

_PROBLEM_CARDS = [
    ("Structural complexity",
     "A multi-part, strict template; Excellence / Impact / Implementation "
     "criteria; call-specific constraints; a joint effort across partners."),
    ("Fragmented inputs",
     "Call documents and annexes, templates and compliance rules, internal "
     "drafts and partner materials, separate budget tables."),
    ("Consistency & compliance risks",
     "A long, manual process across versions and hands — errors and "
     "inconsistencies quietly accumulate."),
]


def _problem_space_slide(prs):
    slide = template.add_content_slide(
        prs,
        "The Problem Space",
        ["Why Horizon Europe proposals are hard — the worked example for "
         "the next 25 minutes."],
    )
    for i, (heading, body) in enumerate(_PROBLEM_CARDS):
        template.add_card(
            slide, Inches(template.CONTENT_LEFT.inches + i * 4.11),
            Inches(2.3), Inches(3.91), Inches(2.6), PALE, heading, PRIMARY,
            body,
        )
    template.add_band(
        slide, Inches(5.25), Inches(0.9),
        "Key insight: most failures are structural, not conceptual.",
        fill=HIGHLIGHT,
    )
    template.set_notes(slide, (
        "≈1 min, spoken before switching to Gemini — this slide grounds "
        "the whole segment. Bridge from the 7 Levels map: 'Levels 2–3 are "
        "where this course takes you; here is terrain where those skills "
        "pay off.' Horizon Europe proposals are the running example "
        "because they are the hardest thing this audience touches: a "
        "strict multi-part template scored on Excellence / Impact / "
        "Implementation, inputs scattered across call documents, drafts, "
        "partner materials, and budget tables, and a long manual pipeline "
        "where errors accumulate.\n\n"
        "Land the orange band and let it reframe the segment: most "
        "failures are structural, not conceptual — and structure is "
        "exactly what a well-built prompt supplies. Prompting is not "
        "magic words; it is imposing structure on the model's work. With "
        "that lens set, switch to Gemini for Demo 1: the same question, "
        "three ways."
    ))


# --- Slide 2: the same question, three ways (Demo 1) -------------------------

_THREE_WAYS = [
    ("1 · Google-style", "Horizon Europe budget",
     "A keyword, not a question. You get a generic encyclopedia answer.",
     PALE, PRIMARY),
    ("2 · Better", "Explain the budget structure of Horizon Europe "
     "collaborative projects",
     "A real question. Better — but the model still guesses who is asking "
     "and why.",
     PALE, PRIMARY),
    ("3 · ICC", "Instruction + Context + Constraints",
     "The full structured prompt — next slide. The answer arrives shaped "
     "for your PI.",
     PALE_WARM, HIGHLIGHT),
]


def _three_ways_slide(prs):
    slide = template.add_content_slide(prs, "The same question, three ways")

    card_width = 3.71
    arrow_gap = 0.5
    x = template.CONTENT_LEFT.inches
    for i, (heading, prompt, gloss, fill, heading_color) in enumerate(_THREE_WAYS):
        card = template.add_card(
            slide, Inches(x), Inches(1.6), Inches(card_width), Inches(2.55),
            fill, heading, heading_color, gloss,
        )
        _add_quote(card, prompt, color=heading_color)
        x += card_width
        if i < len(_THREE_WAYS) - 1:
            template.add_label(slide, Inches(x), Inches(2.6), Inches(arrow_gap),
                               "→", size=24, color=AMBER, align=PP_ALIGN.CENTER)
            x += arrow_gap

    template.add_band(
        slide, Inches(4.45), Inches(0.85),
        "Output quality scales with input quality.",
        sub="Same model, same question — three very different answers.",
    )
    template.add_demo_cue(
        slide,
        "Gemini, Demo 1 (≈8 min): run all three prompts live, compare the "
        "answers side by side",
        top=Inches(5.65),
    )
    template.set_notes(slide, (
        "SWITCH TO GEMINI — Demo 1, ≈8 min of the 25 including the ICC "
        "readout and the Prompting LLMs generalization (Demo 2 gets the "
        "other ≈17 min; its full script is in the Two shortcuts notes). "
        "The budget question continues the problem space just set up: "
        "this is a structurally hard domain, so watch structure win. Run "
        "the three prompts in escalating order, in separate "
        "conversations, and leave all three answers visible for comparison. "
        "1: 'Horizon Europe budget' — a Google habit carried into a chatbot; "
        "generic result. 2: the real question — visibly better, still "
        "unanchored. 3: the full ICC prompt (pre-typed and tested the day "
        "before; shown verbatim on the next slide) — the answer comes out "
        "scoped, structured, and pitched at the PI.\n\n"
        "The one sentence to land while the outputs sit side by side: output "
        "quality scales with input quality. Participants only watch here — "
        "they reproduce this in the setup block and the assignment."
    ))


# --- Slide 3: the ICC prompt, verbatim ---------------------------------------

# The Demo 1 ICC prompt from lesson_1.md, verbatim (reflowed, not reworded).
_ICC_BLOCKS = [
    ("Instruction",
     "Explain the eligible cost categories and overhead calculation for a "
     "Horizon Europe collaborative project, and list the 5 most common "
     "budgeting mistakes.",
     1.05),
    ("Context",
     "I am a research management administrator at a European university. "
     "We are preparing a budget for a Cluster 4 project with 8 partners, "
     "total budget EUR 3-4M. My audience is our PI, who has never "
     "coordinated an EU project.",
     1.35),
    ("Constraints",
     "Maximum 600 words. Use a table for cost categories. Plain language, "
     "no unexplained acronyms.",
     1.05),
]


def _icc_slide(prs):
    slide = template.add_content_slide(prs, "The ICC prompt")

    top = 1.6
    for label, text, height in _ICC_BLOCKS:
        template.add_card(slide, template.CONTENT_LEFT, Inches(top),
                          Inches(2.0), Inches(height), PRIMARY, label, WHITE)
        card = template.add_card(
            slide, Inches(2.85), Inches(top), Inches(9.88), Inches(height),
            PALE, "", PRIMARY,
        )
        para = card.text_frame.paragraphs[0]
        para.alignment = PP_ALIGN.LEFT
        run = para.add_run()
        run.text = text
        template.style(run, size=14, color=TEXT)
        top += height + 0.25

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(top + 0.1), CONTENT_WIDTH,
        "One prompt, three labeled blocks: what to do, who is asking and "
        "why, and what shape the answer must take.",
        italic=True, align=PP_ALIGN.CENTER,
    )
    template.set_notes(slide, (
        "Still in Demo 1 — this slide is the readable record of the prompt "
        "just run in Gemini, so nobody has to transcribe from the demo "
        "window. Walk the three blocks: Instruction — the task itself, with "
        "a deliverable ('list the 5 most common mistakes'). Context — who "
        "is asking, what for, and for whom; this is what stages 1 and 2 "
        "were missing. Constraints — length, format, language; this is "
        "what makes the answer usable without editing.\n\n"
        "Tell participants: you'll write three of these yourselves this "
        "week, about your own Anchor Project's domain — the exact prompt "
        "text is in the deck to copy the shape from.\n\n"
        "Then the next slide generalizes: ICC is the starter form of a "
        "bigger idea — the prompt as a contract."
    ))


# --- Slide 4: prompting LLMs — the contract (ported from the proposal deck) --

_CONTRACT_EXAMPLE = (
    "Role:  Gantt designer\n"
    "Task:  create a Gantt chart for the work packages\n"
    "Constraints:  measurable KPIs · align with Expected Outcomes · "
    "include milestones · no WP-level detail\n"
    "Input:  the documents in the WP folder\n"
    "Output:  structured text, max 600 words"
)


def _prompting_llms_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Prompting LLMs",
        ["From one-line requests to structured contracts."],
    )
    card = template.add_card(
        slide, template.CONTENT_LEFT, Inches(2.15), Inches(5.9), Inches(3.35),
        PALE, "Garbage in, garbage out", PRIMARY,
        "Output quality is set by input quality. “Write section X” leaves "
        "the model guessing about goals, audience, and format — so it "
        "guesses. A working prompt defines all five:",
    )
    for line in ("Role — who the AI is to be",
                 "Task — the goal and its boundaries",
                 "Inputs — the documents that ground it",
                 "Constraints — limits, criteria, exclusions",
                 "Output — structure, length, format"):
        para = card.text_frame.add_paragraph()
        para.space_before = Pt(4)
        run = para.add_run()
        run.text = f"•  {line}"
        template.style(run, size=13, color=SKY)
    example = template.add_card(
        slide, Inches(6.77), Inches(2.15), Inches(5.96), Inches(3.35),
        PALE_WARM, "A structured prompt, in full", HIGHLIGHT,
    )
    para = example.text_frame.add_paragraph()
    para.space_before = Pt(6)
    run = para.add_run()
    run.text = _CONTRACT_EXAMPLE
    template.style(run, size=13, color=TEXT)
    template.add_band(
        slide, Inches(5.75), Inches(0.85),
        "A prompt is a contract, not just an instruction.",
    )
    template.set_notes(slide, (
        "≈1–2 min, still inside Demo 1's ≈8-minute window, while the three "
        "Gemini answers are on screen. The move is generalization: the ICC "
        "prompt everyone just saw is the starter form of this contract — "
        "Instruction, Context, Constraints, plus two blocks working "
        "prompts add: an explicit Role and explicit Inputs.\n\n"
        "Walk the right-hand example from proposal practice (a Gantt "
        "chart for the work packages): every block removes a guess the "
        "model would otherwise make — GIGO in reverse. The model does "
        "exactly as much guessing as your prompt leaves it.\n\n"
        "Land the band — a prompt is a contract, not just an instruction — "
        "then bridge to Demo 2: 'now, two shortcut phrases that get you "
        "most of this contract for free.'"
    ))


# --- Slide 5: the two shortcuts (Demo 2 starts) ------------------------------

_SHORTCUTS = [
    ("Shortcut 1 — Ask-me-first",
     "Append this to any task and let the model interview you before it "
     "answers:",
     "Before answering, ask me the questions you need to give the best "
     "possible answer."),
    ("Shortcut 2 — Reverse prompt",
     "After a good multi-turn result, ask for the reusable prompt — and "
     "save it:",
     "Write the single prompt that would have gotten us to this result on "
     "the first try."),
]


def _shortcuts_slide(prs):
    slide = template.add_content_slide(prs, "Two shortcuts")

    for i, (heading, gloss, phrase) in enumerate(_SHORTCUTS):
        card = template.add_card(
            slide, Inches(template.CONTENT_LEFT.inches + i * 6.17), Inches(1.6),
            Inches(5.96), Inches(2.6), PALE, heading, PRIMARY, gloss,
        )
        _add_quote(card, phrase)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(4.45), CONTENT_WIDTH,
        "Copy these two phrases word for word — they alone jump you from "
        "Level 1 to Level 2.",
        color=AMBER, align=PP_ALIGN.CENTER,
    )
    template.add_demo_cue(
        slide,
        "Gemini, Demo 2 (≈17 min) starts here: ask-me-first live — watch "
        "the model interview the facilitator",
        top=Inches(5.05),
    )
    template.set_notes(slide, (
        "SWITCH TO GEMINI — Demo 2 begins here and runs ≈17 min, spanning "
        "this slide through the rules recap. Both shortcut phrases come "
        "from the 7 Levels transcript, and these alone jump a participant "
        "from Level 1 to Level 2. The assignment uses both. Full "
        "minute-by-minute script:\n\n"
        "0:00–1:00 — Set up. Open a NEW Gemini conversation (fresh window "
        "— practice the context-window rule out loud). Frame the block: "
        "'Demo 1 was about writing a better prompt yourself; the next "
        "quarter hour is about making the model do that work for you.'\n\n"
        "1:00–3:00 — Shortcut 1, the setup. Type a deliberately ordinary "
        "task: 'Draft an agenda for the kick-off meeting of our 8-partner "
        "Horizon Europe project.' Before sending, append the ask-me-first "
        "phrase verbatim from the slide. Send.\n\n"
        "3:00–6:00 — Shortcut 1, the interview. Gemini returns questions "
        "— typically 4–8 (date and duration? online or in person? who "
        "attends? what must be decided?). Read them aloud: the model is "
        "surfacing exactly the context Demo 1 had to hand-write into the "
        "ICC prompt. Answer two or three briefly, tell it to make "
        "sensible assumptions for the rest, and let it produce the "
        "agenda. Land one sentence: 'It asked better questions than most "
        "of us would have.'\n\n"
        "6:00–8:00 — Shortcut 2, reverse prompt. In the same "
        "conversation, type the second phrase verbatim. Show the single "
        "consolidated prompt it returns — point out that your interview "
        "answers are now written into it as context.\n\n"
        "8:00–10:00 — Save it, prove it. Copy the generated prompt into a "
        "visibly open document titled 'Prompt library — kick-off agenda'. "
        "Say: this saved prompt is the seed of the prompt library that "
        "moves into your knowledge system from Lesson 4 on. If on time: "
        "open a new conversation, paste it, and show the first-try result "
        "matching the interviewed one.\n\n"
        "10:00–13:00 — Meta-prompting (advance to the next slide). Run "
        "the periodic-report meta-prompt exactly as printed; scroll the "
        "generated prompt and point at the context and constraints nobody "
        "asked for; fill one or two specifics and run it. If tight on "
        "time, describe the naive 'draft the impact section' comparison "
        "instead of running it.\n\n"
        "13:00–15:00 — One pattern live (advance to Four prompt "
        "patterns). Persona is the quickest win: run the "
        "EU-grants-advisor example; point at the other three patterns as "
        "read-later.\n\n"
        "15:00–16:00 — Working scale (advance to Prompt Patterns & "
        "Meta-Prompting). No typing: point at the pattern families and "
        "the reusable-template meta-example from proposal practice; land "
        "'you design standards, not just prompts.'\n\n"
        "16:00–17:00 — Rules recap (advance to Two rules while we demo). "
        "State both rules over the last screen of outputs, then hand to "
        "Segment 4.\n\n"
        "Contingencies: keep yesterday's rehearsal transcript open in a "
        "second tab in case Gemini stalls or the interview comes back "
        "thin. If running long, drop the fresh-chat rerun (8:00–10:00) "
        "first, then compress the persona run to a read-through."
    ))


# --- Slide 6: meta-prompting -------------------------------------------------

_META_PROMPT = (
    "I need an AI assistant to help me draft the impact section of an EU "
    "project's periodic report. Write the optimal prompt I should use, "
    "including all the context and constraints that would produce the best "
    "result."
)


def _meta_prompting_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Meta-prompting — let the AI write the prompt",
        [
            "Describe the task and ask for the prompt — not the answer.",
            "Then fill in your specifics, run the generated prompt, and "
            "compare with a naive attempt.",
        ],
    )
    card = template.add_card(
        slide, template.CONTENT_LEFT, Inches(3.0), CONTENT_WIDTH, Inches(1.7),
        PALE_WARM, "The move, in one prompt:", HIGHLIGHT,
    )
    _add_quote(card, _META_PROMPT, color=TEXT)
    template.add_band(
        slide, Inches(5.05), Inches(1.1),
        "The model knows what a good prompt looks like better than you do —\n"
        "use it as your prompt engineer.",
        size=18,
    )
    template.set_notes(slide, (
        "Still in Gemini — minutes 10–13 of the Demo 2 script (see the "
        "Two shortcuts notes). Run the periodic-report "
        "meta-prompt exactly as printed; scroll the generated prompt — "
        "point out that the model added context and constraints nobody "
        "asked it for. Fill in one or two specifics, run it, and compare "
        "with a naive 'draft the impact section' attempt.\n\n"
        "The message is the band: the model knows what a good prompt looks "
        "like better than you do — use it as your prompt engineer. The "
        "assignment's item 4 is exactly this move on a recurring task from "
        "the participant's own work."
    ))


# --- Slide 7: the four prompt patterns ---------------------------------------

# (name, one line, research-management example) — examples verbatim from
# lesson_1.md; the one-liners compress its dash-glosses.
_PATTERNS = [
    ("Persona",
     "The role sets vocabulary, priorities, and depth.",
     "Act as an experienced EU grants advisor reviewing a first-time "
     "applicant's budget…"),
    ("Example-driven (few-shot)",
     "A good example beats a paragraph of description.",
     "Here is a partner-search announcement in our house style. Write one "
     "for the following project in the same style: …"),
    ("Step-by-step",
     "Forcing intermediate steps improves reasoning on rule-checking tasks.",
     "Before giving the final assessment, first list the eligibility "
     "criteria, then check each against the project facts, then conclude."),
    ("Critique-then-improve",
     "Separates diagnosis from repair — the model stops rewriting what "
     "already works.",
     "Here is my draft. First list its three biggest weaknesses against "
     "the evaluation criteria, then rewrite it fixing only those."),
]


def _patterns_slide(prs):
    slide = template.add_content_slide(prs, "Four prompt patterns")

    for i, (name, one_liner, example) in enumerate(_PATTERNS):
        left = template.CONTENT_LEFT.inches + (i % 2) * 6.17
        top = 1.55 + (i // 2) * 2.15
        card = template.add_card(
            slide, Inches(left), Inches(top), Inches(5.96), Inches(1.95),
            PALE, name, PRIMARY, one_liner,
        )
        _add_quote(card, example)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.0), CONTENT_WIDTH,
        "Every saved prompt is one of these shapes filled in — your prompt "
        "library lives in your knowledge system from Lesson 4 on.",
        italic=True, align=PP_ALIGN.CENTER,
    )
    template.set_notes(slide, (
        "Minutes 13–15 of the Demo 2 script. Present from the slide; demo "
        "exactly ONE pattern live in Gemini "
        "(persona is the quickest win), then point at the other three — "
        "each example is a research-management task, readable later. "
        "Persona: the role sets vocabulary, priorities, depth. "
        "Example-driven: one pasted example of a liked output beats a "
        "paragraph of description. Step-by-step: forcing intermediate "
        "steps improves rule-checking (eligibility is the natural demo). "
        "Critique-then-improve: diagnose first, then repair only the "
        "diagnosed — keeps good passages intact.\n\n"
        "Close the segment with the caption line: every saved prompt is one "
        "of these shapes filled in; the library lives in the knowledge "
        "system from Lesson 4 on. The assignment requires at least one "
        "pattern in the three ICC prompts."
    ))


# --- Slide 8: patterns & meta-prompting at working scale (ported) ------------

_FAMILIES = [
    ("Role-based", "“Act as a Horizon Europe evaluator.”"),
    ("Verifier", "Generate probing questions about X, then combine the "
     "answers into Y."),
    ("Constraint-driven", "Page limits, structure rules, forbidden content "
     "(no WP detail in section X)."),
    ("Input-grounded", "Concept note + work packages in, template "
     "followed."),
    ("Refinement", "“Suggest a better version of this question to use "
     "instead.”"),
]

_META_TEMPLATE_EXAMPLE = (
    "Task:  generate a reusable prompt template for Horizon Europe "
    "proposal writing.\n"
    "Requirements:  evaluator alignment (Excellence / Impact / "
    "Implementation) · measurable KPIs · no WP-level detail leakage · "
    "explicit input structure · defined output format.\n"
    "Output:  a reusable template with placeholders for the concept, "
    "WPs, and call requirements."
)


def _patterns_meta_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Prompt Patterns & Meta-Prompting",
        ["The same moves, at working scale — from proposal-writing "
         "practice."],
    )
    card = template.add_card(
        slide, template.CONTENT_LEFT, Inches(2.15), Inches(5.9), Inches(3.5),
        PALE, "Pattern families in daily use", PRIMARY,
    )
    for name, gloss in _FAMILIES:
        para = card.text_frame.add_paragraph()
        para.space_before = Pt(5)
        run = para.add_run()
        run.text = f"{name} — "
        template.style(run, size=13, color=SKY, bold=True)
        run = para.add_run()
        run.text = gloss
        template.style(run, size=13, color=TEXT)
    example = template.add_card(
        slide, Inches(6.77), Inches(2.15), Inches(5.96), Inches(3.5),
        PALE_WARM, "Meta-prompting, one level up", HIGHLIGHT,
    )
    para = example.text_frame.add_paragraph()
    para.space_before = Pt(6)
    run = para.add_run()
    run.text = _META_TEMPLATE_EXAMPLE
    template.style(run, size=13, color=TEXT)
    template.add_band(
        slide, Inches(5.9), Inches(0.85),
        "You design standards, not just prompts.",
        fill=HIGHLIGHT,
    )
    template.set_notes(slide, (
        "Minutes 15–16 of the Demo 2 script — no typing, point and talk. "
        "The four patterns just shown are the entry palette; this slide "
        "is what they grow into in working practice, back in the problem "
        "space that opened the segment. Left: the pattern families a "
        "proposal-support team reaches for daily — the four patterns "
        "reappear under working names, plus the verifier family "
        "(generate probing questions, then combine the answers), which "
        "previews the checking habits of Lesson 3.\n\n"
        "Right: meta-prompting promoted from a trick to a habit — you "
        "ask the model for a reusable TEMPLATE, not an answer, and the "
        "template joins your prompt library with placeholders for the "
        "next proposal. This is the Level 2 → Level 3 shift on the map, "
        "and the seed of the standards that live in your knowledge "
        "system from Lesson 4 on.\n\n"
        "Land the band — you design standards, not just prompts — then "
        "advance to the rules recap."
    ))


# --- Slide 9: the two rules --------------------------------------------------


def _rules_slide(prs):
    slide = template.add_content_slide(prs, "Two rules while we demo")

    template.add_card(
        slide, template.CONTENT_LEFT, Inches(1.7), CONTENT_WIDTH, Inches(1.6),
        PALE, "1 — Nothing you couldn't publish", PRIMARY,
        "Never paste sensitive institutional data into Gemini. The full "
        "rule comes in Lesson 2 — until then: if you couldn't publish it, "
        "don't paste it.",
    )
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(3.55), CONTENT_WIDTH, Inches(1.6),
        PALE, "2 — Verify anything factual before using it", PRIMARY,
        "Cost rules, percentages, deadlines, citations — confident and "
        "fluent is not the same as correct. Check against the source "
        "before it goes into your work.",
    )
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.5), CONTENT_WIDTH,
        "Both rules apply to everything you just watched — and to "
        "everything you build this week.",
        italic=True, align=PP_ALIGN.CENTER,
    )
    template.set_notes(slide, (
        "State both rules while demoing — this slide is the recap that "
        "stays on screen at the end of Demo 2, not a new topic. Rule 1: "
        "nothing you couldn't publish goes into Gemini; the full "
        "sensitive-data rule (the Copilot Sensitive Lane) comes in "
        "Lesson 2. Rule 2: verify anything factual before using it — the "
        "'sign your name to it' rule from the fundamentals segment, now "
        "applied to the demo outputs everyone just admired.\n\n"
        "Then hand over to Segment 4: the assignment turns everything from "
        "these 25 minutes into this week's practice."
    ))


def add_slides(prs):
    _problem_space_slide(prs)
    _three_ways_slide(prs)
    _icc_slide(prs)
    _prompting_llms_slide(prs)
    _shortcuts_slide(prs)
    _meta_prompting_slide(prs)
    _patterns_slide(prs)
    _patterns_meta_slide(prs)
    _rules_slide(prs)

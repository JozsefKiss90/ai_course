"""Segment 3 — Prompt engineering backdrop (25 min, live facilitator demo).

Six slides supporting the live Gemini demo, per lesson_1.md Segment 3: the
three-way escalation (Demo 1), the ICC prompt verbatim, the two shortcut
append-phrases, the meta-prompting move, the four prompt patterns with their
research-management examples, and the two rules stated while demoing. The
facilitator demos live; these slides anchor what participants retain and
copy. Demo-switch cues use template.add_demo_cue and are repeated in the
notes with the rough 8/17-minute split.
"""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    ACCENT, CONTENT_WIDTH, HIGHLIGHT, PALE, PALE_WARM, PRIMARY, TEXT, WHITE,
)


def _add_quote(card, text, color=PRIMARY):
    """Append the copy-this phrase to a card as its own quoted paragraph."""
    para = card.text_frame.add_paragraph()
    para.space_before = Pt(8)
    run = para.add_run()
    run.text = f"“{text}”"
    template.style(run, size=14, color=color, italic=True)
    return para


# --- Slide 1: the same question, three ways (Demo 1) -------------------------

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
                               "→", size=24, color=ACCENT, align=PP_ALIGN.CENTER)
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
        "SWITCH TO GEMINI — Demo 1, ≈8 min of the 25 (Demo 2 gets the other "
        "≈17 min). Run the three prompts in escalating order, in separate "
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


# --- Slide 2: the ICC prompt, verbatim ---------------------------------------

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
        "text is in the deck to copy the shape from."
    ))


# --- Slide 3: the two shortcuts (Demo 2 starts) ------------------------------

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
        color=HIGHLIGHT, align=PP_ALIGN.CENTER,
    )
    template.add_demo_cue(
        slide,
        "Gemini, Demo 2 (≈17 min) starts here: ask-me-first live — watch "
        "the model interview the facilitator",
        top=Inches(5.05),
    )
    template.set_notes(slide, (
        "SWITCH TO GEMINI — Demo 2 begins, ≈17 min (shortcuts, then "
        "meta-prompting, then one prompt pattern live). Both shortcuts come "
        "from the 7 Levels transcript, and these alone jump a participant "
        "from Level 1 to Level 2.\n\n"
        "Ask-me-first: give Gemini a real task, append the phrase, and let "
        "it interview you on screen — answer two or three of its questions, "
        "then let it complete the task. Reverse prompt: after the multi-turn "
        "result, ask for the single prompt that would have gotten there on "
        "the first try, and show yourself saving it — that saved prompt is "
        "the seed of the prompt library that moves into the knowledge "
        "system from Lesson 4 on. The assignment uses both."
    ))


# --- Slide 4: meta-prompting -------------------------------------------------

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
        "Still in Gemini (Demo 2), ~2 min live. Run the periodic-report "
        "meta-prompt exactly as printed; scroll the generated prompt — "
        "point out that the model added context and constraints nobody "
        "asked it for. Fill in one or two specifics, run it, and compare "
        "with a naive 'draft the impact section' attempt.\n\n"
        "The message is the band: the model knows what a good prompt looks "
        "like better than you do — use it as your prompt engineer. The "
        "assignment's item 4 is exactly this move on a recurring task from "
        "the participant's own work."
    ))


# --- Slide 5: the four prompt patterns ---------------------------------------

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
        "Present from the slide; demo exactly ONE pattern live in Gemini "
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


# --- Slide 6: the two rules --------------------------------------------------


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
    _three_ways_slide(prs)
    _icc_slide(prs)
    _shortcuts_slide(prs)
    _meta_prompting_slide(prs)
    _patterns_slide(prs)
    _rules_slide(prs)

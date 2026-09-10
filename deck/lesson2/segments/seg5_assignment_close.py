"""Segment 5 — Assignment briefing + close (8 min, Presentation + Q&A).

Four slides, per lesson_2.md Segment 5 and in its order: the assignment on
one screenshot-friendly slide, the outcome read off the 7 Levels map from
Lesson 1, the effort expectation with the two places the work is shown,
and the close pointing at Practice Week 1 and Lesson 3.

The assignment slide carries the plan's three numbered items whole —
blueprint, deliverable, routing — and then one row of the blueprint filled
in, in the four columns a step has to carry: the step, the tool, the lane,
and why that tool belongs there. The worked row is the reason the slide is
worth its density. "Produce a blueprint of the tool chaining" is a
sentence a participant can read twice and still not know what to write in
their document; one filled row settles the shape, and a test holds both
the plan's wording and the four columns.

The outcome is a slide of its own rather than a line at the foot of the
assignment. The plan states it as a result — Level 3 achieved, foundation
for Level 4 established — and a result is only meaningful against the map
it is measured on, which is Lesson 1's 7 Levels. So three rows of that map
appear: Level 2 as last week's work, Level 3 as this week's, Level 4 as
what the blueprint is the foundation of. The names come from lesson_1.md's
table and a test reads them out of it, so the two lessons cannot drift
apart on what a level is called.

The segment is about both lanes — the assignment chains across them — so
its slides sit on the neutral ink/slate accents, and a lane colour appears
only where a slide says work goes to that lane: the blueprint row's LANE
cell, and the two lane-tinted columns of the tool list. That is the
template's rule, the same line Segment 2 drew. This is also the one
segment that names both tools, which a test checks from the positive side,
where Segments 3 and 4 are checked from the negative.
"""

from dataclasses import dataclass

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

from deck.lesson2 import template
from deck.lesson2.template import (
    DAILY_DRIVER, INK, MUTED, PANEL, SENSITIVE_LANE, SLATE, TEXT, WHITE,
)

# The content area, in inches, as the geometry every slide here is laid out
# on — the same grid the demo segments use, so the deck reads as one.
_LEFT = template.CONTENT_LEFT.inches
_WIDTH = template.CONTENT_WIDTH.inches
_GAP = 0.23
_COL_WIDTH = (_WIDTH - _GAP) / 2
_RIGHT_COL = _LEFT + _COL_WIDTH + _GAP
_COL3_WIDTH = (_WIDTH - 2 * _GAP) / 3

# A numbered row: a solid chip carrying the number, then the row's card.
_CHIP_WIDTH = 0.62
_CHIP_GAP = 0.18
_ROW_LEFT = _LEFT + _CHIP_WIDTH + _CHIP_GAP
_ROW_WIDTH = _WIDTH - _CHIP_WIDTH - _CHIP_GAP


def _numbered_row(slide, number, top, height, heading, detail, accent=SLATE):
    """One numbered row: the number in a solid chip, then a card whose lead
    is bold and whose detail continues on the same line. Returns the card,
    so a caller that needs more than one line — the outcome map's levels do,
    the assignment's items do not — can add its own paragraphs."""
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(top), Inches(_CHIP_WIDTH),
        Inches(height), accent, str(number), WHITE)

    card = template.add_open_card(
        slide, Inches(_ROW_LEFT), Inches(top), Inches(_ROW_WIDTH),
        Inches(height), accent)
    para = card.text_frame.paragraphs[0]
    run = para.add_run()
    run.text = heading
    template.style(run, size=15, color=INK, font=template.HEADING_FONT,
                   bold=True)
    run = para.add_run()
    run.text = f"  —  {detail}"
    template.style(run, size=13, color=TEXT)
    return card


# --- The assignment, on one slide -------------------------------------------

# The plan's three numbered items, verbatim in substance: what to produce,
# what to hand in, and how every step is routed. Kept on one slide because
# the slide is the assignment — the room screenshots it and works from the
# picture for two weeks.
_ASSIGNMENT_ITEMS = [
    ("Blueprint",
     "For every step: the tool, the input, the output, detailed guidelines "
     "for running it, and a justification for why that tool at that step."),
    ("Deliverable",
     "A presentation on a hand-picked topic, designed for educational "
     "purposes and intended to facilitate learning outcomes."),
    ("Routing",
     "Every step that touches sensitive data goes to the Sensitive Lane, "
     "documents are anonymised before upload, and the blueprint states the "
     "lane per step."),
]

_ITEM_TOP = 2.24
_ITEM_HEIGHT = 0.80
_ITEM_PITCH = 0.90

# One row of the blueprint, filled in: the four columns a step carries, and
# a step a participant could actually have written. The LANE cell takes the
# lane's colour, because that cell is exactly the claim "this work goes to
# that tool"; the other three stay neutral.
# The last field of each column is its share of the row: the columns are
# sized in proportion so the four of them always fill the content width,
# rather than as four inch figures that have to be re-tuned together.
_BLUEPRINT_ROW = [
    ("STEP",
     "Step 3 — in: step 2's cleared PDF. Out: the outline the presentation "
     "must cover.",
     5, SLATE),
    ("TOOL", "Gemini — file upload, then Canvas", 4, SLATE),
    ("LANE", DAILY_DRIVER.name, 3, DAILY_DRIVER.color),
    ("WHY THIS TOOL, HERE",
     "The topic is public, so this is not Sensitive Lane work. Upload reads "
     "the whole PDF at once; Canvas turns it into an outline you can "
     "iterate section by section.",
     7, SLATE),
]

_ROW_TOP = 5.22
_ROW_HEIGHT = 1.06
_ROW_GAP = 0.12


def _assignment_slide(prs):
    slide = template.add_content_slide(
        prs, "Assignment: your first workflow orchestration")

    template.add_band(
        slide, Inches(1.30), Inches(0.80),
        "One multi-step workflow orchestration", size=21,
        sub="Chain all the tools and capabilities the course has introduced "
            "so far into one run of steps — and write down why each step is "
            "where it is.",
    )

    top = _ITEM_TOP
    for number, (heading, detail) in enumerate(_ASSIGNMENT_ITEMS, start=1):
        _numbered_row(slide, number, top, _ITEM_HEIGHT, heading, detail)
        top += _ITEM_PITCH

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(4.96), template.CONTENT_WIDTH,
        "One row of that blueprint, filled in — every step is written like "
        "this, with the guidelines for running it underneath",
        size=11, color=MUTED,
    )

    span = _WIDTH - (len(_BLUEPRINT_ROW) - 1) * _ROW_GAP
    shares = sum(share for _, _, share, _ in _BLUEPRINT_ROW)
    left = _LEFT
    for column, value, share, edge in _BLUEPRINT_ROW:
        width = span * share / shares
        template.add_detail_card(
            slide, Inches(left), Inches(_ROW_TOP), Inches(width),
            Inches(_ROW_HEIGHT), edge, column, [value],
            heading_size=10.5, line_size=11.5)
        left += width + _ROW_GAP

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.38), template.CONTENT_WIDTH,
        "Screenshot this slide — it is the whole assignment.",
        size=13, color=MUTED, italic=True, align=PP_ALIGN.CENTER,
    )

    template.set_notes(slide, (
        "~4 minutes on this slide, and it is the one they leave with. Read "
        "the three items aloud, slowly, then say the caption out loud: "
        "screenshot this slide, it is the whole assignment.\n\n"
        "Nothing on it is new. Item 1 is the chaining slide that closed the "
        "last segment, written down. Item 2 is the presentation Study and "
        "Learn and Canvas were demonstrated on. Item 3 is Segment 2's "
        "routing question, asked once per step instead of once per task.\n\n"
        "The worked row is the part worth slowing down for. “Produce a "
        "blueprint” means nothing until they see one line of it: the step "
        "with its input and its output, the tool, the lane, and the reason. "
        "Read the reason column aloud in full — the justification is the "
        "assignment, the rest is bookkeeping. The guidelines for running the "
        "step are the sixth field and they do not fit a table cell: they go "
        "under the row in the participant's own document, as the how-to a "
        "colleague could follow without asking. Say that a blueprint of six to ten rows like this one "
        "is the right size; nobody needs thirty steps.\n\n"
        "The deliverable is a presentation on a topic they pick, for "
        "teaching someone something. Say the topic is theirs — it does not "
        "have to be the Anchor Project, and a topic they already know well "
        "makes the learning-outcome part easier to judge.\n\n"
        "Routing is where this assignment can go wrong quietly. A chain "
        "does not inherit a lane from its first step: each step is routed "
        "on its own, and Canva and genspark.ai sit outside the tenant, so "
        "only cleared content goes into them. If a step cannot be cleared, "
        "the step changes — not the lane.\n\n"
        "Paste this slide's text into the Teams chat straight after the "
        "session, so nobody is working from a screenshot alone.\n\n"
        "Then take questions here. This slide and the next are the Q&A "
        "anchor; the close is one minute at the end."
    ))
    return slide


# --- The outcome, on the 7 Levels map ---------------------------------------

# Three rows of the 7 Levels map from lesson_1.md: the level just left, the
# level reached this week, and the level the blueprint is the foundation
# of. The names and the one-line descriptions are Lesson 1's, so the room
# recognises the map rather than meeting a new one.
@dataclass(frozen=True)
class _Level:
    """One row of the 7 Levels map as this slide shows it: the level as
    Lesson 1 named and described it, plus where the course stands on it.
    `chip` is the number chip's fill and the card's edge; `status_color`
    is the weight the standing line carries — the level reached this week
    is the darkest of the three, the level already behind them the
    lightest."""

    number: int
    name: str
    description: str
    status: str
    chip: object
    status_color: object


_LEVELS = [
    _Level(2, "Prompt Crafter",
           "Structured prompts, examples, iteration.",
           "Done — that was last week's assignment.", SLATE, MUTED),
    _Level(3, "Power User",
           "Persistent context: dedicated workspaces that already know your "
           "domain.",
           "Reached this week — as soon as the Gem you saw built is your "
           "own.", INK, INK),
    _Level(4, "Tool Orchestrator",
           "The right specialised tool per step: NotebookLM for documents, "
           "Perplexity for cited research.",
           "Founded, not yet reached — the blueprint is the orchestration "
           "written down; Lessons 3 and 4 hand you the specialised tools to "
           "put in it.", SLATE, SLATE),
]

_LEVEL_TOP = 1.78
_LEVEL_HEIGHT = 1.06
_LEVEL_PITCH = 1.18


def _outcome_slide(prs):
    slide = template.add_content_slide(
        prs, "The outcome, on the 7 Levels map")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "Three rows of the map from Lesson 1 — where last week left you, "
        "where this week puts you, and what the blueprint is the foundation "
        "of",
        size=13, color=MUTED,
    )

    top = _LEVEL_TOP
    for level in _LEVELS:
        card = _numbered_row(
            slide, level.number, top, _LEVEL_HEIGHT,
            f"Level {level.number} · {level.name}", level.description,
            accent=level.chip)
        para = card.text_frame.add_paragraph()
        run = para.add_run()
        run.text = level.status
        template.style(run, size=12, color=level.status_color, bold=True)
        top += _LEVEL_PITCH

    template.add_band(
        slide, Inches(5.42), Inches(0.94),
        "Level 3 achieved · foundation for Level 4 established", size=20,
        sub="A persistent, domain-aware workspace — and the right tool per "
            "step, chained.",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.46), template.CONTENT_WIDTH,
        "Nobody reaches a level by owning a tool. Level 3 is a workspace you "
        "work inside; Level 4 is a chain you can justify.",
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~1 minute. This is the answer to “what did this week get me?”, and "
        "it is worth stating because the answer is not “two more tools”.\n\n"
        "Point at the map, not at the slide's wording: they saw these rows "
        "in Lesson 1 and have not seen them since. Level 2 was last week — "
        "structured prompts, iteration, done. Level 3 is today, and the "
        "thing that earns it is the Gem, not the number of tools they now "
        "have accounts for. Be honest about the tense: they watched one "
        "built, and they are on Level 3 once they have their own — which is "
        "the first thing the assignment has them do.\n\n"
        "Be precise about Level 4: the assignment does not reach it, it "
        "founds it. Orchestration is the right specialised tool per step, "
        "and the specialised tools arrive in Lessons 3 and 4 — NotebookLM, "
        "Perplexity. What the blueprint gives them is the habit of "
        "justifying the step, which is the part that does not come with a "
        "tool.\n\n"
        "Say the closing line as written if the room looks pleased with "
        "itself: nobody reaches a level by owning a tool.\n\n"
        "If someone asks where Levels 5–7 are, one sentence: Level 5 is "
        "Lesson 5's Agent Builder, and 6 and 7 are the final session's "
        "outlook. Do not open the map here."
    ))
    return slide


# --- Effort and where the work is shown (≈2 min) -----------------------------

# The plan's tool list, grouped by the lane each tool is used in — the
# grouping is the point, because the assignment's third item is routing.
# The lane tints say "work goes here"; the third column is neither lane's,
# so it stays on the neutral card.
_TOOL_COLUMNS = [
    (SENSITIVE_LANE.name,
     ["Copilot Chat (Basic), institutional account",
      "Prompt Coach — for the prompts in the chain",
      "Study and Learn — flashcards and a quiz from your topic",
      "Adobe Acrobat for the PDF sources"],
     SENSITIVE_LANE.tint),
    (DAILY_DRIVER.name,
     ["Gemini — file and image upload",
      "Gems — the workspace the chain runs in",
      "Deep Research — the researched briefing",
      "Canvas — the outline and its iterations"],
     DAILY_DRIVER.tint),
    ("The rest of the chain",
     ["Canva for the prototype",
      "genspark.ai for the deck",
      "NotebookLM at scenario level, if the free tier supports it"],
     PANEL),
]

_WHERE_SHOWN = [
    "Practice Week 1's drop-in (W3) — troubleshooting a half-built chain",
    "The Lesson 3 debrief (W4) — 2–3 volunteers present blueprint and "
    "presentation",
]


def _effort_slide(prs):
    slide = template.add_content_slide(
        prs, "Effort and where the work is shown")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "Two weeks, the blueprint first — and two places where the work gets "
        "looked at",
        size=13, color=MUTED,
    )

    template.add_card(
        slide, template.CONTENT_LEFT, Inches(1.72), Inches(_COL_WIDTH),
        Inches(1.60), PANEL, "3–4 hours across the two weeks", INK,
        "The blueprint first, then the presentation. The blueprint is the "
        "assignment; the presentation is what proves the chain runs. Twenty "
        "minutes at a time beats one long Sunday.",
    )
    template.add_list_card(
        slide, Inches(_RIGHT_COL), Inches(1.72), Inches(_COL_WIDTH),
        Inches(1.60), PANEL, "Where the work is shown", _WHERE_SHOWN, size=12.5)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(3.44), template.CONTENT_WIDTH,
        "Tools to chain from — everything the course has introduced, in the "
        "lane it is used in",
        size=11, color=MUTED,
    )

    for index, (heading, items, fill) in enumerate(_TOOL_COLUMNS):
        template.add_list_card(
            slide, Inches(_LEFT + index * (_COL3_WIDTH + _GAP)), Inches(3.78),
            Inches(_COL3_WIDTH), Inches(2.22), fill, heading, items,
            size=12.5)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.10), template.CONTENT_WIDTH,
        "A chain does not inherit a lane from its first step — every step is "
        "routed on its own, and nothing uncleared goes into the last two "
        "columns",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~2 minutes. Set the effort expectation out loud: 3–4 hours across "
        "the two weeks, spread out, blueprint first. Anyone past four hours "
        "is polishing the presentation instead of writing the blueprint, "
        "and the blueprint is the assignment.\n\n"
        "Say what “all the tools so far” means, because otherwise it reads "
        "as a memory test. The three columns are the answer, and they are "
        "grouped by lane on purpose: the Sensitive Lane column is what the "
        "institutional account gives them, the Daily Driver column is what "
        "the free tier gives them. The last column is not a third lane — "
        "Canva, genspark.ai and NotebookLM are tools the chain passes "
        "through rather than assistants a task is routed to, and none of "
        "them is the Sensitive Lane, so only cleared content goes into any "
        "of them.\n\n"
        "NotebookLM is on the list with a condition attached. It was shown "
        "at scenario level only and the free tier moves; if it is not "
        "available to them this fortnight, the chain works without it and "
        "Lesson 3 is where it gets its own treatment.\n\n"
        "Both venues, plainly. Practice Week 1's drop-in in W3 is optional "
        "and is the place for a half-built chain — bring the blueprint even "
        "if nothing runs yet. The Lesson 3 debrief in W4 is where 2–3 "
        "volunteers present blueprint and presentation. Ask for tentative "
        "volunteers now, in the chat; a named volunteer arrives prepared.\n\n"
        "Anyone who did not finish: the drop-in, not an apology in the "
        "chat. Say it once, lightly."
    ))
    return slide


# --- Close (≈1 min) ----------------------------------------------------------

_NEXT_SESSIONS = [
    ("Practice Week 1 · W3",
     ["An optional, facilitated drop-in — no new material, and no "
      "obligation to come",
      "Bring the blueprint and the lane questions it raised",
      "Bring any Gemini free-tier surprise you hit — that is what the hour "
      "is for"]),
    ("Lesson 3 · W4",
     ["NotebookLM properly, not at scenario level",
      "Perplexity for cited research you can trace back to a source",
      "The Wiki Sandbox — the first piece of your KM System, and what the "
      "rest of the course is built on"]),
]


def _close_slide(prs):
    slide = template.add_content_slide(
        prs, "Next: Practice Week 1 and Lesson 3")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "No new material next week. The week after, the first piece of the "
        "system this course is building",
        size=13, color=MUTED,
    )

    for index, (heading, items) in enumerate(_NEXT_SESSIONS):
        card = template.add_list_card(
            slide, Inches(_LEFT if index == 0 else _RIGHT_COL), Inches(1.86),
            Inches(_COL_WIDTH), Inches(2.00), PANEL, heading, items,
            size=13)
        card.text_frame.margin_top = Inches(0.18)

    template.add_band(
        slide, Inches(4.45), Inches(1.06),
        "A workflow you can justify, step by step", size=21,
        sub="Bring the blueprint to the drop-in, and the whole chain to the "
            "Lesson 3 debrief.",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.80), template.CONTENT_WIDTH,
        "Questions now — this slide and the assignment stay up.",
        size=13, color=MUTED, italic=True, align=PP_ALIGN.CENTER,
    )

    template.set_notes(slide, (
        "~1 minute, no new teaching, and then Q&A on whatever is left.\n\n"
        "Practice Week 1 is next week and it is exactly what its name says: "
        "no new material, the session slot runs as an optional facilitated "
        "drop-in, and the reason it exists is that this course runs during "
        "office hours. Say that anyone stuck on a lane question or a "
        "half-built chain should come; anyone whose chain already runs does "
        "not have to.\n\n"
        "Lesson 3 in W4 is the payoff for the NotebookLM scenarios they "
        "just watched — the tool properly this time, Perplexity beside it "
        "for cited research, and the Wiki Sandbox, which is the first piece "
        "of the KM System they will still be building in Week 8.\n\n"
        "Leave the assignment slide up while you take questions, and post "
        "its text in the chat before you close the meeting."
    ))
    return slide


# --- Segment assembly --------------------------------------------------------

# Slide order per lesson_2.md Segment 5: the assignment, the outcome it
# produces, the effort it costs and where it is shown, then the close.
_BUILDERS = [
    _assignment_slide,
    _outcome_slide,
    _effort_slide,
    _close_slide,
]


def add_slides(prs):
    for builder in _BUILDERS:
        builder(prs)

"""Segment 1 — Recap + assignment debrief (15 min, Participant demos,
facilitated).

Three slides, per lesson_3.md Segment 1: the recap map (Part A) as a
two-column table — every Lesson 1 or Lesson 2 concept on the left, the
Lesson 3 topic it leads into on the right, with the forward reference to
the segment that picks it up; the debrief format (Part B) as the three
things each volunteer shows, in the Lesson 2 assignment's order; and the
capture slide the facilitator fills live, tagged by assignment item, with
the routing of the captured problems.

The recap map links and never re-teaches: no cell explains a concept, it
only names it and points forward. The segment is about neither lane, so
its slides carry no lane colour.
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck.lesson3 import template
from deck.lesson3.template import (
    HEADING_FONT, INK, LINE, MUTED, PANEL, SLATE, TEXT, WHITE,
)

# --- Part A: the recap map ---------------------------------------------------

# One row per row of the Part A table in lesson_3.md: the earlier concept,
# the Lesson 3 topic it leads into, and the forward reference. Compressed
# to a line each — the plan's cells are the source; the tests check the
# pairs and the forward references against the plan itself.
_RECAP_ROWS = [
    ("The 7 Levels — Level 3 (Power User) reached, Level 4 (Tool Orchestrator) "
     "founded (Lesson 2 assignment)",
     "Level 4 is today's target: the right specialised tool per step, "
     "NotebookLM for documents, Obsidian for the notes that outlive the chat",
     "Segments 2–3 · assignment"),
    ("The KM System teaser (Lesson 1): wiki → agent → Obsidian",
     "Redrawn today without the wiki: notebook → vault, the vault as "
     "single source of truth",
     "Segment 2"),
    ("“More context is not better context”; lost in the middle (Lesson 1)",
     "Why a source-grounded notebook beats a document dump, and why "
     "answers carry citations",
     "Segment 2"),
    ("Hallucination; “verify anything you would sign your name to” (Lesson 1)",
     "NotebookLM's citations: the verification step built into the tool; "
     "nothing enters the vault without a source line",
     "Segments 2 · 3 · 5"),
    ("The two-lane rule; anonymise-before-upload (Lesson 2)",
     "Both new tools that call a cloud model (NotebookLM, the Copilot for "
     "Obsidian plugin) run as Daily Driver: anonymised or fictional Anchor "
     "Project content only",
     "Segments 2–3"),
    ("Gems — persistent context, workspaces that already know your domain "
     "(Lesson 2)",
     "Notebooks as the evidence counterpart: a Gem organises behaviour, a "
     "notebook organises sources; a notebook can feed a Gem",
     "Segment 2"),
    ("Deep Research in Gemini (Lesson 2)",
     "Deep Research inside a notebook writes its findings straight into the "
     "sources; Perplexity as the cited-search alternative, in passing",
     "Segment 2"),
    ("Gemini Canvas (Lesson 2)",
     "A name clash: Obsidian also has a Canvas, a different thing entirely",
     "Segment 3"),
    ("Microsoft Copilot Chat (Basic) (Lesson 2)",
     "A second name clash: “Copilot for Obsidian”, an unrelated community "
     "plugin, sits in the Daily Driver, never in the Sensitive Lane",
     "Segment 3"),
    ("The NotebookLM preview: three scenarios (Lesson 2 Segment 4)",
     "Today the walkthrough: sources, citations, Studio outputs, limits",
     "Segment 2"),
    ("The Lesson 2 blueprint: every step names its input and its output",
     "Today's assignment chains two tools the same way: notebook output is "
     "vault input, and the vault's own AI answers from the vault",
     "Segment 5"),
]

_LEFT = template.CONTENT_LEFT.inches

_ROW_TOP = 1.22
_ROW_PITCH = 0.485
_ROW_HEIGHT = 0.44

_CONCEPT_WIDTH = 4.35
_ARROW_LEFT = 5.05
_LINK_LEFT = 5.4
_LINK_WIDTH = 7.33


def _solid_label(slide, left, top, width, height, text, size):
    """A solid slate block with centred white heading type — the debrief's
    number badges and the capture slide's item tags are the same block."""
    block = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width),
        Inches(height),
    )
    template.solid(block, SLATE)
    tf = block.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = text
    template.style(run, size=size, color=WHITE, font=HEADING_FONT, bold=True)
    return block


def _recap_row(slide, concept, link, forward, top):
    card = template.add_open_card(
        slide, Inches(_LEFT), Inches(top), Inches(_CONCEPT_WIDTH),
        Inches(_ROW_HEIGHT), SLATE)
    card.text_frame.margin_top = 0
    card.text_frame.margin_bottom = 0
    run = card.text_frame.paragraphs[0].add_run()
    run.text = concept
    template.style(run, size=9.5, color=INK, bold=True)

    template.add_label(
        slide, Inches(_ARROW_LEFT), Inches(top + 0.03), Inches(0.3), "→",
        size=13, color=MUTED, align=PP_ALIGN.CENTER,
    )

    card = template.add_open_card(
        slide, Inches(_LINK_LEFT), Inches(top), Inches(_LINK_WIDTH),
        Inches(_ROW_HEIGHT), INK)
    card.text_frame.margin_top = 0
    card.text_frame.margin_bottom = 0
    para = card.text_frame.paragraphs[0]
    run = para.add_run()
    run.text = link
    template.style(run, size=9.5, color=TEXT)
    run = para.add_run()
    run.text = f"  ·  {forward}"
    template.style(run, size=9.5, color=SLATE, bold=True)


def _recap_map_slide(prs):
    slide = template.add_content_slide(
        prs, "Lessons 1–2 → Lesson 3: the recap map", compact=True)

    template.add_label(slide, Inches(_LEFT), Inches(0.88),
                       Inches(_CONCEPT_WIDTH), "FROM LESSONS 1 AND 2", size=10,
                       color=MUTED)
    template.add_label(slide, Inches(_LINK_LEFT), Inches(0.88),
                       Inches(_LINK_WIDTH), "LEADS INTO TODAY", size=10,
                       color=MUTED)

    top = _ROW_TOP
    for concept, link, forward in _RECAP_ROWS:
        _recap_row(slide, concept, link, forward, top)
        top += _ROW_PITCH

    template.add_label(
        slide, Inches(_LEFT), Inches(6.62), template.CONTENT_WIDTH,
        "Reference only — the Lesson 1 and Lesson 2 decks carry the explanations",
        size=10.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~3 min. Read the map at pace, one line per row, left then right — "
        "a link, never a definition. Nothing from Lessons 1–2 gets explained "
        "again: if someone asks for the explanation, point at the earlier "
        "deck and move on.\n\n"
        "Two rows to land with a beat: the 7 Levels row — Level 3 is behind "
        "you as of the Lesson 2 assignment, Level 4 is what today buys you — "
        "and the KM System row, because the diagram you saw teased in Lesson "
        "1 gets redrawn in ten minutes without the wiki.\n\n"
        "The two name-clash rows (Canvas, Copilot for Obsidian) are there so the words do "
        "not trip anyone in Segment 3; say them once here.\n\n"
        "Then straight into the debrief; do not let the map eat into the "
        "volunteers' time."
    ))
    return slide


# --- Part B: the assignment debrief ------------------------------------------

# The three Lesson 2 assignment items each volunteer shows, in the plan's
# order, with the facilitator's one question per item.
_DEBRIEF_ITEMS = [
    ("1", "The blueprint", "the redrawn roadmap diagram and the step table",
     "“Which steps did you skip, and why?”"),
    ("2", "The presentation", "two or three slides, not the whole deck",
     "“Which learning outcome do these slides serve?”"),
    ("3", "The AI-use log", "on the last slide",
     "“Was any step's output rejected at the check — and then what?”"),
]

_BADGE_TOP = 2.62
_BADGE_SIZE = 0.5
_ITEM_TOP = 3.24
_ITEM_HEIGHT = 2.2
_ITEM_WIDTH = 3.85
_ITEM_PITCH = 4.14


def _debrief_item(slide, left, badge, heading, detail, question):
    _solid_label(slide, left, _BADGE_TOP, _BADGE_SIZE, _BADGE_SIZE, badge, 18)

    card = template.add_card(
        slide, Inches(left), Inches(_ITEM_TOP), Inches(_ITEM_WIDTH),
        Inches(_ITEM_HEIGHT), PANEL, heading, INK, detail,
    )
    card.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    card.text_frame.margin_top = Inches(0.26)
    para = card.text_frame.add_paragraph()
    para.space_before = Pt(10)
    run = para.add_run()
    run.text = question
    template.style(run, size=12, color=SLATE, italic=True)
    return card


def _debrief_slide(prs):
    slide = template.add_content_slide(
        prs, "Assignment debrief — the next 12 minutes")

    template.add_band(
        slide, Inches(1.48), Inches(0.68),
        "2–3 volunteers  ·  4 minutes each, questions included  ·  "
        "screen-shared",
        size=18,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(2.22), template.CONTENT_WIDTH,
        "Shown in this order — the three items of the Lesson 2 assignment, "
        "one facilitator question each",
        size=13, color=MUTED,
    )

    left = _LEFT
    for badge, heading, detail, question in _DEBRIEF_ITEMS:
        _debrief_item(slide, left, badge, heading, detail, question)
        left += _ITEM_PITCH

    template.add_band(
        slide, Inches(5.75), Inches(0.65),
        "Time check in the chat at 3 minutes  ·  we cut at 4  ·  "
        "didn't finish? Practice Week 2 is the venue",
        size=15, fill=SLATE,
    )

    template.set_notes(slide, (
        "~12 min, and it is the segment's whole point — protect it.\n\n"
        "Setup done before the session: volunteers asked for in the Teams "
        "chat, plus one backup in case a screen-share fails. Say the format "
        "once, then hand over: 2–3 volunteers, 4 minutes each including "
        "questions.\n\n"
        "Keeping time: post a visible time check in the chat at the "
        "3-minute mark and cut at 4. Three volunteers at four minutes each "
        "is exactly the twelve minutes; if the first two overrun, stop at "
        "two so the read-back still fits.\n\n"
        "Ask exactly one question per item, the ones printed on the cards. "
        "Problems go on the capture slide, not into a discussion here.\n\n"
        "Anyone who did not finish: no discussion now, Practice Week 2 is "
        "the venue.\n\n"
        "The routing check is enforced from this debrief on: if a volunteer "
        "shows non-anonymised material in a Daily Driver tool, name it in "
        "one sentence as the anonymise-before-upload rule from Lesson 2, "
        "and move on."
    ))
    return slide


# --- Capturing the common problems -------------------------------------------

_CAPTURE_TAGS = ["Blueprint", "Presentation", "Log"]

_CAPTURE_TOP = 1.95
_CAPTURE_PITCH = 1.05
_CAPTURE_HEIGHT = 0.85
_TAG_WIDTH = 2.1
_WRITE_LEFT = 2.85
_WRITE_WIDTH = 9.88
_READ_BACK_TOP = 5.3
_READ_BACK_HEIGHT = 1.45

_ROUTING_READ_BACK = (
    "“the notebook answered from the wrong document” → source grounding and "
    "citations, Segment 2  ·  “I lost the good outputs after the chat ended” "
    "→ the vault, Segment 3  ·  “NotebookLM was not available on my account” "
    "→ the free-tier check, Segment 2  ·  everything else → Practice Week 2"
)


def _capture_row(slide, tag, top):
    _solid_label(slide, _LEFT, top, _TAG_WIDTH, _CAPTURE_HEIGHT, tag, 14)
    # Deliberately empty: the facilitator types into this box during the
    # demos, one line per problem.
    writing = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(_WRITE_LEFT), Inches(top),
        Inches(_WRITE_WIDTH), Inches(_CAPTURE_HEIGHT),
    )
    template.outlined(writing, PANEL, LINE)
    writing.text_frame.word_wrap = True
    writing.text_frame.margin_left = Inches(0.2)
    writing.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    return writing


def _capture_slide(prs):
    slide = template.add_content_slide(prs, "Common problems — captured live")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        "One line per problem, typed in as it comes up, filed under the item "
        "it belongs to",
        size=13, color=MUTED,
    )

    top = _CAPTURE_TOP
    for tag in _CAPTURE_TAGS:
        _capture_row(slide, tag, top)
        top += _CAPTURE_PITCH

    card = template.add_open_card(
        slide, Inches(_LEFT), Inches(_READ_BACK_TOP), template.CONTENT_WIDTH,
        Inches(_READ_BACK_HEIGHT), INK)
    tf = card.text_frame
    run = tf.paragraphs[0].add_run()
    run.text = "After the last volunteer — read the list back, 30 seconds:"
    template.style(run, size=14, color=INK, font=HEADING_FONT, bold=True)
    para = tf.add_paragraph()
    para.space_before = Pt(4)
    run = para.add_run()
    run.text = _ROUTING_READ_BACK
    template.style(run, size=12.5, color=TEXT)

    template.set_notes(slide, (
        "Runs alongside the demos — keep this slide up while the volunteers "
        "share, or keep a pinned Teams chat message if screen real estate is "
        "tight. One line per problem, no names, filed under the item it came "
        "from.\n\n"
        "~30 sec at the end: read the list back and say which ones today's "
        "session answers — the wrong-document answer in Segment 2's source "
        "grounding and citations, the lost outputs in Segment 3's vault, "
        "the missing NotebookLM in Segment 2's free-tier check — and which "
        "go to Practice Week 2. Say so explicitly so nobody leaves with an "
        "unanswered problem.\n\n"
        "This list is the facilitator's own carry-forward: it says what "
        "Practice Week 2 has to cover. Keep it after the session."
    ))
    return slide


def add_slides(prs):
    _recap_map_slide(prs)
    _debrief_slide(prs)
    _capture_slide(prs)

"""Segment 1 — Recap + assignment debrief (15 min, Participant demos,
facilitated).

Three slides, per lesson_2.md Segment 1: the recap map (Part A) as a
two-column table — every Lesson 1 concept on the left, the Lesson 2 topic
it leads into on the right, with the forward reference to the segment that
picks it up; the debrief format (Part B) as the four things each volunteer
shows, in the assignment's order; and the capture slide the facilitator
fills live, tagged by assignment item, with the routing of the captured
problems.

The recap map links and never re-teaches: no cell explains a Lesson 1
concept, it only names it and points forward. Anyone who wants the
explanation gets pointed at the Lesson 1 deck — that instruction lives in
the speaker notes.

The segment is about neither lane, so its slides carry no lane colour;
Gemini is named on the debrief slide only as where the volunteers'
screen-shares come from.
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck.lesson2 import template
from deck.lesson2.template import (
    HEADING_FONT, INK, LINE, MUTED, PANEL, SLATE, TEXT, WHITE,
)

# --- Part A: the recap map ---------------------------------------------------

# One row per row of the Part A table in lesson_2.md: the Lesson 1 concept,
# the Lesson 2 topic or work it leads into, and the forward reference to
# the segment that picks it up. Compressed to fit a row each — the plan's
# cells are the source; tests/test_lesson2_deck.py checks the pairs and the
# forward references against the plan itself.
_RECAP_ROWS = [
    ("The 7 Levels — Level 2 (Prompt Crafter), done in the Lesson 1 assignment",
     "Level 3 (Power User) is today's target — persistent context via Gems; "
     "the assignment lays the foundation for Level 4 (Tool Orchestrator)",
     "Segment 4"),
    ("ICC prompting and the four patterns (persona, example-driven, "
     "step-by-step, critique-then-improve)",
     "The same prompts run in both lanes — the lane decides where a prompt "
     "goes, not how it is written; Prompt Coach checks them",
     "Segments 3 · 4"),
    ("Ask-me-first and reverse prompt",
     "Reverse prompts become a Gem's standing instructions",
     "Segment 4"),
    ("Meta-prompting",
     "Prompt Coach — meta-prompting as a packaged agent",
     "Segment 3"),
    ("The two rules from the Lesson 1 demo — the publish test for Gemini; "
     "verify before use",
     "The first becomes the full two-lane rule; the second, the directive's "
     "“critical checking of every output”",
     "Segment 2"),
    ("The anonymize-or-fictional Anchor Project rule",
     "The institutional anonymise-before-upload rule for documents; the "
     "routing test in the assignment",
     "Segments 2 · 5"),
    ("Context window and “more context is not better context”",
     "Why file upload and long context need curation; why NotebookLM's "
     "source grounding exists",
     "Segment 4 · Lesson 3 preview"),
]

_LEFT = template.CONTENT_LEFT.inches  # the content area's left edge

_ROW_TOP = 1.68
_ROW_PITCH = 0.70
_ROW_HEIGHT = 0.62

_CONCEPT_WIDTH = 4.55
_ARROW_LEFT = 5.28
_LINK_LEFT = 5.65
_LINK_WIDTH = 7.08


# The template's white card carries a fixed heading run, so a cell whose
# text is several runs at its own sizes builds the same shape here — same
# fill, hairline and edge-bar width as template.add_card — and leaves the
# text to the caller.
_EDGE_BAR = 0.09


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


def _edged_card(slide, left, top, width, height, edge):
    """A white card with a coloured edge bar; its text frame is empty and
    left-aligned, vertically centred, for the caller to fill."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width),
        Inches(height),
    )
    template.panel(card)
    template.add_bar(slide, Inches(left), Inches(top), Inches(_EDGE_BAR),
                     Inches(height), edge)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.26)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT
    return card


def _recap_row(slide, concept, link, forward, top):
    card = _edged_card(slide, _LEFT, top, _CONCEPT_WIDTH, _ROW_HEIGHT, SLATE)
    run = card.text_frame.paragraphs[0].add_run()
    run.text = concept
    template.style(run, size=12, color=INK, bold=True)

    template.add_label(
        slide, Inches(_ARROW_LEFT), Inches(top + 0.12), Inches(0.3), "→",
        size=15, color=MUTED, align=PP_ALIGN.CENTER,
    )

    card = _edged_card(slide, _LINK_LEFT, top, _LINK_WIDTH, _ROW_HEIGHT, INK)
    para = card.text_frame.paragraphs[0]
    run = para.add_run()
    run.text = link
    template.style(run, size=11, color=TEXT)
    run = para.add_run()
    run.text = f"  ·  {forward}"
    template.style(run, size=11, color=SLATE, bold=True)


def _recap_map_slide(prs):
    slide = template.add_content_slide(prs, "Lesson 1 → Lesson 2: the recap map")

    template.add_label(slide, Inches(_LEFT), Inches(1.3),
                       Inches(_CONCEPT_WIDTH), "FROM LESSON 1", size=11,
                       color=MUTED)
    template.add_label(slide, Inches(_LINK_LEFT), Inches(1.3),
                       Inches(_LINK_WIDTH), "LEADS INTO TODAY", size=11,
                       color=MUTED)

    top = _ROW_TOP
    for concept, link, forward in _RECAP_ROWS:
        _recap_row(slide, concept, link, forward, top)
        top += _ROW_PITCH

    template.add_label(
        slide, Inches(_LEFT), Inches(6.52), template.CONTENT_WIDTH,
        "Reference only — the Lesson 1 deck carries the explanations",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~3 min. Read the map at pace, one line per row, left then right — "
        "this is a map, not a lesson. Nothing here gets explained again: if "
        "someone asks for the explanation, point at the Lesson 1 deck and "
        "move on; the recap exists so today's session can lean on Lesson 1 "
        "without repeating it.\n\n"
        "The two rows to land with a beat: the 7 Levels row — Level 2 is "
        "behind you as of the Lesson 1 assignment, Level 3 is what today "
        "buys you, and this week's assignment is the run-up to Level 4 — "
        "and the Anchor Project row, because the anonymise rule you already "
        "applied to your own project turns into the institutional rule in "
        "ten minutes' time.\n\n"
        "Then straight into the debrief; do not let the map eat into the "
        "volunteers' time."
    ))
    return slide


# --- Part B: the assignment debrief ------------------------------------------

# The four assignment items each volunteer shows, in the plan's order, with
# the facilitator's one question per item.
_DEBRIEF_ITEMS = [
    ("1", "Anchor Project description", "five sentences",
     "“What did you anonymise or invent?”"),
    ("2", "One of the three ICC prompts",
     "with the one-sentence “what I'd improve”",
     "“Which pattern did it use, if any?”"),
    ("3", "Ask-me-first result", "what the model asked back",
     "“Were the questions useful?”"),
    ("4", "The meta-prompt", "the generated prompt",
     "“Did it beat the naive attempt?”"),
]

_BADGE_TOP = 2.62
_BADGE_SIZE = 0.5
_ITEM_TOP = 3.24
_ITEM_HEIGHT = 2.2
_ITEM_WIDTH = 2.85
_ITEM_PITCH = 3.09


def _debrief_item(slide, left, badge, heading, detail, question):
    _solid_label(slide, left, _BADGE_TOP, _BADGE_SIZE, _BADGE_SIZE, badge, 18)

    card = template.add_card(
        slide, Inches(left), Inches(_ITEM_TOP), Inches(_ITEM_WIDTH),
        Inches(_ITEM_HEIGHT), PANEL, heading, INK, detail,
    )
    # Top-anchored so the four headings all start at the same height
    # instead of floating with how much text their card carries.
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
        "screen-shared from your own Gemini",
        size=18,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(2.22), template.CONTENT_WIDTH,
        "Shown in this order — the four items of the Lesson 1 assignment, "
        "one facilitator question each",
        size=13, color=MUTED,
    )

    left = _LEFT
    for badge, heading, detail, question in _DEBRIEF_ITEMS:
        _debrief_item(slide, left, badge, heading, detail, question)
        left += _ITEM_PITCH

    template.add_band(
        slide, Inches(5.75), Inches(0.65),
        "You get a time check in the chat at 3 minutes  ·  we cut at 4  ·  "
        "didn't finish the assignment? Practice Week 1 is the venue",
        size=15, fill=SLATE,
    )

    template.set_notes(slide, (
        "~12 min, and it is the segment's whole point — protect it.\n\n"
        "Setup done before the session: volunteers asked for in the Teams "
        "chat, plus one backup in case a screen-share fails. Say the format "
        "once, then hand over: 2–3 volunteers, 4 minutes each including "
        "questions, sharing from their own Gemini.\n\n"
        "Keeping time: post a visible time check in the chat at the "
        "3-minute mark and cut at 4 — cut mid-item if you must, the "
        "remaining items are the same for everyone and you have seen them "
        "already. Three volunteers at four minutes each is exactly the "
        "twelve minutes; if the first two overrun, stop at two so the "
        "read-back still fits.\n\n"
        "Ask exactly one question per item, the ones printed on the cards. "
        "Do not turn a demo into coaching — problems go on the capture "
        "slide, not into a discussion here.\n\n"
        "Anyone who did not finish the assignment: no discussion now, "
        "Practice Week 1 is the venue.\n\n"
        "The two-lane rule is not in force yet — it gets stated in Segment "
        "2 — so do not correct anyone mid-demo. If a volunteer shows "
        "sensitive content in Gemini, note it without comment and use it, "
        "anonymised, as the opening example of Segment 2."
    ))
    return slide


# --- Capturing the common problems -------------------------------------------

# The four tags the captured problems are filed under — the assignment's
# own items, so a problem lands in one glance.
_CAPTURE_TAGS = ["Anchor Project", "ICC", "Ask-me-first", "Meta-prompt"]

_CAPTURE_TOP = 1.95
_CAPTURE_PITCH = 0.92
_CAPTURE_HEIGHT = 0.72
_TAG_WIDTH = 2.1
_WRITE_LEFT = 2.85
_WRITE_WIDTH = 9.88
_READ_BACK_TOP = 5.72
_READ_BACK_HEIGHT = 1.05

_ROUTING_READ_BACK = (
    "Routing questions → Segment 2  ·  “the answer was wrong” → verification "
    "in Segment 2 and Prompt Coach in Segment 3  ·  “the chat lost track” → "
    "Gems in Segment 4  ·  everything else → Practice Week 1"
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

    card = _edged_card(slide, _LEFT, _READ_BACK_TOP,
                       template.CONTENT_WIDTH.inches, _READ_BACK_HEIGHT, INK)
    tf = card.text_frame
    run = tf.paragraphs[0].add_run()
    run.text = "After the last volunteer — read the list back, 30 seconds:"
    template.style(run, size=14, color=INK, font=HEADING_FONT, bold=True)
    para = tf.add_paragraph()
    para.space_before = Pt(4)
    run = para.add_run()
    run.text = _ROUTING_READ_BACK
    template.style(run, size=13, color=TEXT)

    template.set_notes(slide, (
        "Runs alongside the demos — keep this slide up while the volunteers "
        "share, or keep a pinned Teams chat message if screen real estate is "
        "tight. One line per problem, no names, filed under the item it came "
        "from.\n\n"
        "~30 sec at the end: read the list back and say where each one gets "
        "answered — routing questions in Segment 2, “the answer was wrong” "
        "in Segment 2's verification point and Prompt Coach in Segment 3, "
        "“the chat lost track” in Segment 4's Gems. Everything else goes to "
        "Practice Week 1; say so explicitly so nobody leaves with an "
        "unanswered problem.\n\n"
        "This list is the facilitator's own carry-forward: it says what "
        "Practice Week 1 has to cover. Keep it after the session."
    ))
    return slide


def add_slides(prs):
    _recap_map_slide(prs)
    _debrief_slide(prs)
    _capture_slide(prs)

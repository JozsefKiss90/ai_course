"""Design template for the Lesson 2 deck — the single source of visual truth
for Lesson 2, on top of the shared mechanics in deck/core.py.

Every Lesson 2 slide is created through the builders here, so fonts,
colours and the footer stay uniform across segment modules. The builders
and in-slide blocks keep the call shapes of deck/template.py (Lesson 1) —
add_title_slide, add_section_divider, add_content_slide,
add_placeholder_slide, add_demo_cue, add_card, add_band, add_label — so a
segment author works the same way in either lesson.

Visual language — deliberately not Lesson 1's dark navy: a light, warm
paper canvas with near-black ink type, a serif heading face (Cambria) over
a sans body face (Calibri), thin hairlines instead of panels, and white
cards. Title and divider slides stay on the paper canvas with a single
bold colour stripe rather than a full-bleed dark ground.

Lane colour-coding: the deck's two accent colours are the two lanes from
CONTEXT.md, and they mean the lane wherever they appear.

- Sensitive Lane (Copilot Chat (Basic), institutional account) — teal
  SENSITIVE_LANE.color, tint SENSITIVE_LANE.tint.
- Daily Driver (Google Gemini, free tier) — violet DAILY_DRIVER.color,
  tint DAILY_DRIVER.tint.

Builders take an optional `lane=` (SENSITIVE_LANE or DAILY_DRIVER): a
divider, content slide or demo cue given a lane carries that lane's colour
in its stripe, rule and tag chip, and cards filled with a lane tint get the
lane's edge bar. Slides about both lanes or neither (recap, rules,
assignment) use the neutral ink/slate accents, so a lane colour on a slide
always says "this is about that tool". Never use teal for Gemini or violet
for Copilot content.
"""

from dataclasses import dataclass

from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import core
# The lesson-independent mechanics live in deck.core; these names are
# re-exported so segment modules call template.solid(...) etc. exactly as
# they do for Lesson 1.
from deck.core import (  # noqa: F401
    SLIDE_HEIGHT, SLIDE_WIDTH, Design, add_bar, add_text as _add_text,
    blank_slide as _blank_slide, set_notes, solid,
)

# --- Design constants -------------------------------------------------------

HEADING_FONT = "Cambria"
BODY_FONT = "Calibri"

CANVAS = RGBColor(0xF7, 0xF4, 0xEE)  # warm paper — every slide's ground
PANEL = RGBColor(0xFF, 0xFF, 0xFF)  # white card surface
LINE = RGBColor(0xD8, 0xD2, 0xC6)  # hairlines, card borders
INK = RGBColor(0x1C, 0x24, 0x2B)  # near-black type, neutral fills
SLATE = RGBColor(0x3E, 0x4C, 0x59)  # neutral accent — rules, chips
TEXT = RGBColor(0x2A, 0x33, 0x3B)  # body text
MUTED = RGBColor(0x6B, 0x74, 0x7D)  # captions, footer, secondary lines
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PRIMARY = INK  # neutral fill for bands and label blocks


@dataclass(frozen=True)
class Lane:
    """One of the two lanes from CONTEXT.md and the colours that mean it."""

    name: str
    tool: str
    color: RGBColor
    tint: RGBColor


SENSITIVE_LANE = Lane(
    "Sensitive Lane", "Copilot Chat (Basic)",
    RGBColor(0x0E, 0x7C, 0x7B), RGBColor(0xDF, 0xF1, 0xEF),
)
DAILY_DRIVER = Lane(
    "Daily Driver", "Google Gemini",
    RGBColor(0x6A, 0x4C, 0xBC), RGBColor(0xEB, 0xE6, 0xF7),
)
LANES = (SENSITIVE_LANE, DAILY_DRIVER)

# Legacy-style fill keys, so the Lesson 1 add_card call shape carries over:
# fill=SENSITIVE_TINT / DAILY_TINT colour-codes a card by lane.
SENSITIVE_TINT = SENSITIVE_LANE.tint
DAILY_TINT = DAILY_DRIVER.tint

FOOTER_TEXT = "AI for Research Management · Lesson 2 · Week 2"

# Content area shared by all content slides (below the title block).
CONTENT_LEFT = Inches(0.6)
CONTENT_TOP = Inches(1.5)
CONTENT_WIDTH = Inches(12.13)
CONTENT_HEIGHT = Inches(5.3)

# --- Presentation setup -----------------------------------------------------

DESIGN = Design(
    heading_font=HEADING_FONT,
    body_font=BODY_FONT,
    scheme={
        "dk2": INK,
        "accent1": SENSITIVE_LANE.color,
        "accent2": DAILY_DRIVER.color,
    },
    canvas=CANVAS,
    footer_text=FOOTER_TEXT,
    footer_rule=LINE,
    footer_color=MUTED,
)


def new_presentation():
    """A 16:9 presentation with the Lesson 2 theme, paper canvas and footer."""
    return core.new_presentation(DESIGN)


def outlined(shape, fill=PANEL, border=LINE, weight=1.0):
    """Card style: white fill with a thin hairline border, no shadow."""
    core.outlined(shape, fill, border, weight)


def panel(shape):
    """The standard white card surface."""
    outlined(shape, PANEL, LINE)


def style(run, size, color, font=BODY_FONT, bold=False, italic=False):
    core.style(run, size, color, font, bold=bold, italic=italic)


def _accent(lane):
    """The colour that marks a slide: the lane's, or the neutral slate."""
    return lane.color if lane else SLATE


def _lane_of_fill(fill):
    for lane in LANES:
        if fill in (lane.tint, lane.color):
            return lane
    return None


# --- Slide builders ---------------------------------------------------------


def add_title_slide(prs, title, course_name, session_line):
    """Paper cover: two-lane stripe down the left edge, serif title, ink
    course line, session line in the muted caption colour."""
    slide = _blank_slide(prs)

    # The two lanes as one vertical stripe: teal above, violet below.
    add_bar(slide, 0, 0, Inches(0.35), Inches(3.75), SENSITIVE_LANE.color)
    add_bar(slide, 0, Inches(3.75), Inches(0.35), Inches(3.75), DAILY_DRIVER.color)

    tf = _add_text(slide, Inches(1.1), Inches(1.6), Inches(11.3), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = course_name.upper()
    style(run, size=14, color=SLATE, bold=True)

    add_bar(slide, Inches(1.1), Inches(2.15), Inches(1.2), Pt(2), INK)

    tf = _add_text(slide, Inches(1.1), Inches(2.4), Inches(11.3), Inches(2.2))
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=44, color=INK, font=HEADING_FONT, bold=True)

    tf = _add_text(slide, Inches(1.1), Inches(4.8), Inches(11.3), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = session_line
    style(run, size=16, color=MUTED)

    # Lane legend along the bottom — the colour key for the whole deck.
    x = 1.1
    for lane in LANES:
        add_bar(slide, Inches(x), Inches(5.7), Inches(0.18), Inches(0.18), lane.color)
        tf = _add_text(slide, Inches(x + 0.3), Inches(5.6), Inches(5.0), Inches(0.4))
        run = tf.paragraphs[0].add_run()
        run.text = f"{lane.name} · {lane.tool}"
        style(run, size=12, color=TEXT)
        x += 5.6
    return slide


def add_section_divider(prs, number, total, title, duration, mode, lane=None):
    """Paper divider: a colour block at the left carrying the segment
    number, serif title, duration · mode line, and progress ticks. The
    block is the lane's colour when the segment belongs to a lane, slate
    otherwise."""
    slide = _blank_slide(prs)
    accent = _accent(lane)

    # The block stops above the master footer strip so the footer stays
    # readable on dividers too.
    block = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(3.2), Inches(6.95)
    )
    solid(block, accent)
    tf = block.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = str(number)
    style(run, size=120, color=WHITE, font=HEADING_FONT, bold=True)

    tf = _add_text(
        slide, Inches(3.8), Inches(2.1), Inches(8.9), Inches(1.5),
        anchor=MSO_ANCHOR.BOTTOM,
    )
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=34, color=INK, font=HEADING_FONT, bold=True)

    add_bar(slide, Inches(3.8), Inches(3.72), Inches(1.2), Pt(2.5), accent)

    tf = _add_text(slide, Inches(3.8), Inches(3.9), Inches(8.9), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = f"{duration} · {mode}"
    style(run, size=18, color=accent, bold=True)

    tf = _add_text(slide, Inches(3.8), Inches(4.4), Inches(8.9), Inches(0.4))
    run = tf.paragraphs[0].add_run()
    run.text = f"Segment {number} of {total}"
    if lane:
        run.text += f" · {lane.name} · {lane.tool}"
    style(run, size=12, color=MUTED)

    # Progress ticks: one per segment, the current one in the accent.
    tick_w, tick_h, gap = 0.55, 0.08, 0.2
    x = 3.8
    for i in range(1, total + 1):
        add_bar(slide, Inches(x), Inches(6.55), Inches(tick_w), Inches(tick_h),
                accent if i == number else LINE)
        x += tick_w + gap
    return slide


# How far the header block rides up on a compact slide, in inches, so an
# image-dominant slide can start its content at COMPACT_CONTENT_TOP — the
# same knob as Lesson 1's template.
COMPACT_HEADER_RISE = 0.44
COMPACT_CONTENT_TOP = Inches(0.9)


def add_content_slide(prs, title, body_lines=None, notes=None, compact=False,
                      lane=None):
    """Standard content slide on the paper canvas: serif ink title over a
    hairline with a short accent lead, and — when the slide belongs to a
    lane — a lane tag chip at the top right.

    body_lines is a list of strings, or (indent_level, string) tuples.
    Returns the slide so callers can add custom shapes in the content area
    (CONTENT_LEFT/TOP/WIDTH/HEIGHT).

    compact=True raises the whole header block by COMPACT_HEADER_RISE so an
    image-dominant slide can start its content at COMPACT_CONTENT_TOP.
    """
    slide = _blank_slide(prs)
    accent = _accent(lane)
    rise = COMPACT_HEADER_RISE if compact else 0.0

    tf = _add_text(slide, CONTENT_LEFT, Inches(0.45 - rise), Inches(8.8),
                   Inches(0.7), anchor=MSO_ANCHOR.BOTTOM)
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=28, color=INK, font=HEADING_FONT, bold=True)

    if lane:
        add_lane_tag(slide, lane, Inches(9.53), Inches(0.5 - rise))

    add_bar(slide, CONTENT_LEFT, Inches(1.21 - rise), CONTENT_WIDTH, Pt(1), LINE)
    add_bar(slide, CONTENT_LEFT, Inches(1.19 - rise), Inches(1.2), Pt(3), accent)

    if body_lines:
        tf = _add_text(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, CONTENT_HEIGHT)
        first = True
        for entry in body_lines:
            level, text = entry if isinstance(entry, tuple) else (0, entry)
            para = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            para.level = level
            run = para.add_run()
            run.text = text
            style(run, size=18 if level == 0 else 15, color=TEXT if level == 0 else MUTED)
            para.space_after = Pt(8)

    if notes:
        set_notes(slide, notes)
    return slide


def add_lane_tag(slide, lane, left, top, width=Inches(3.2)):
    """Small solid chip naming the lane and its tool in the lane's colour."""
    chip = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.36)
    )
    solid(chip, lane.color)
    tf = chip.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = f"{lane.name.upper()} · {lane.tool.upper()}"
    style(run, size=10, color=WHITE, bold=True)
    return chip


def add_demo_cue(slide, text, top, left=CONTENT_LEFT, width=CONTENT_WIDTH,
                 lane=None):
    """Live-demo marker: the facilitator switches to a live tool here.

    Renders as a filled band reading "▶ LIVE DEMO — <text>" in the lane's
    colour (ink when no lane is given). Callers must also mention the demo
    in the slide's speaker notes.
    """
    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.55)
    )
    solid(band, lane.color if lane else INK)
    add_bar(slide, left, top, Inches(0.1), Inches(0.55), WHITE)
    add_bar(slide, left, top, Inches(0.05), Inches(0.55), lane.color if lane else INK)
    tf = band.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.25)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run = tf.paragraphs[0].add_run()
    run.text = f"▶ LIVE DEMO — {text}"
    style(run, size=16, color=WHITE, font=HEADING_FONT, bold=True)
    return band


def add_band(slide, top, height, text, size=20, fill=PRIMARY, sub=None):
    """Full-width emphasis band: centred bold white text on a solid
    rectangle; optional sub-line. Pass a lane's colour as fill to
    colour-code the band."""
    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, CONTENT_LEFT, top, CONTENT_WIDTH, height
    )
    solid(band, fill)
    tf = band.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = text
    style(run, size=size, color=WHITE, font=HEADING_FONT, bold=True)
    if sub:
        para = tf.add_paragraph()
        para.alignment = PP_ALIGN.CENTER
        para.space_before = Pt(6)
        run = para.add_run()
        run.text = sub
        style(run, size=13, color=WHITE)
    return band


def add_card(slide, left, top, width, height, fill, heading, heading_color,
             body=None):
    """Card on the paper canvas. A lane colour as fill gives a solid label
    block (centred white heading). A lane tint or PANEL gives a white or
    tinted card with a hairline border and an edge bar — the lane's colour
    for a tinted card, slate for a neutral one."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    lane = _lane_of_fill(fill)
    dark = fill in (PRIMARY, INK, SLATE) or (lane is not None and fill == lane.color)
    if dark:
        solid(card, fill)
        heading_color = WHITE
    else:
        outlined(card, fill, LINE)
        add_bar(slide, left, top, Inches(0.09), height,
                lane.color if lane else SLATE)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.25)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER if dark else PP_ALIGN.LEFT
    run = para.add_run()
    run.text = heading
    style(run, size=18, color=heading_color, font=HEADING_FONT, bold=True)
    if body:
        para = tf.add_paragraph()
        para.alignment = PP_ALIGN.LEFT
        para.space_before = Pt(4)
        run = para.add_run()
        run.text = body
        style(run, size=14, color=WHITE if dark else TEXT)
    return card


def add_label(slide, left, top, width, text, size=14, color=MUTED, italic=False,
              align=PP_ALIGN.LEFT):
    """Small free-standing caption/label text."""
    box = slide.shapes.add_textbox(left, top, width, Inches(0.4))
    tf = box.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = align
    run = tf.paragraphs[0].add_run()
    style(run, size=size, color=color, italic=italic)
    run.text = text
    return box


def add_placeholder_slide(prs, segment_label, planned_title, gist, ticket,
                          lane=None):
    """A visibly-unfinished slide standing in for one planned content
    slide: a dashed-outline card, the [PLACEHOLDER] tag, the gist, and the
    ticket that replaces it — on the slide and in the notes."""
    slide = add_content_slide(prs, planned_title, lane=lane)

    card = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(2.3), Inches(10.1), Inches(2.9)
    )
    outlined(card, CANVAS, MUTED, weight=1.5)
    card.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = f"[PLACEHOLDER] {segment_label}"
    style(run, size=20, color=MUTED, font=HEADING_FONT, bold=True)
    para = tf.add_paragraph()
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = gist
    style(run, size=14, color=MUTED)
    para = tf.add_paragraph()
    para.alignment = PP_ALIGN.CENTER
    para.space_before = Pt(10)
    run = para.add_run()
    run.text = f"Replaced by ticket {ticket}"
    style(run, size=12, color=MUTED, italic=True)

    set_notes(
        slide,
        f"Placeholder — replaced by ticket {ticket} ({segment_label}). "
        f"Planned content: {gist}",
    )
    return slide

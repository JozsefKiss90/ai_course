"""Design template for the Lesson 3 deck — the single source of visual truth
for Lesson 3, on top of the shared mechanics in deck/core.py.

Every Lesson 3 slide is created through the builders here, so fonts,
colours and the footer stay uniform across segment modules. The builders
and in-slide blocks keep the call shapes of deck/lesson2/template.py —
add_title_slide, add_section_divider, add_content_slide,
add_placeholder_slide, add_demo_cue, add_card, add_band, add_label,
add_lane_tag, add_open_card, add_list_card, add_detail_card — so a segment
author works the same way in any of the three lessons.

Visual language — deliberately neither Lesson 1's dark navy nor Lesson 2's
warm paper: a cool, light grey-blue canvas with deep blue-black type,
Georgia headings over Arial body, a vertical accent bar beside each title
instead of a rule under it, and section dividers built around a numbered
disc. Title and divider slides stay on the canvas with an ink band across
the top.

Lane colour-coding: Lesson 3 has one lane and one non-lane, and the deck's
two accent colours mean them wherever they appear.

- Daily Driver (every tool that calls a cloud model: NotebookLM, Copilot for
  Obsidian, Perplexity; anonymised or fictional content only) — amber
  DAILY_DRIVER.color, tint DAILY_DRIVER.tint.
- Local (Obsidian itself and Smart Connections: nothing leaves the machine)
  — green LOCAL.color, tint LOCAL.tint.

The Sensitive Lane is not demonstrated in this lesson and has no colour
here. Builders take an optional `lane=` (DAILY_DRIVER or LOCAL): a divider,
content slide or demo cue given a lane carries that lane's colour in its
disc, bar and tag chip, and cards filled with a lane tint get the lane's
edge bar. Slides about neither (recap, hands-on checklist, assignment) use
the neutral ink/slate accents. Never colour a cloud call green or a local
step amber.
"""

from dataclasses import dataclass

from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

from deck import core
# Re-exported so segment modules call template.solid(...) etc. exactly as
# they do for Lessons 1 and 2.
from deck.core import (  # noqa: F401
    SLIDE_HEIGHT, SLIDE_WIDTH, Design, add_bar, add_text as _add_text,
    blank_slide as _blank_slide, set_notes, solid,
)

# --- Design constants -------------------------------------------------------

HEADING_FONT = "Georgia"
BODY_FONT = "Arial"

CANVAS = RGBColor(0xED, 0xF1, 0xF5)  # cool grey-blue — every slide's ground
PANEL = RGBColor(0xFF, 0xFF, 0xFF)  # white card surface
LINE = RGBColor(0xC9, 0xD2, 0xDC)  # hairlines, card borders
INK = RGBColor(0x12, 0x21, 0x3A)  # deep blue-black type, neutral fills
SLATE = RGBColor(0x4A, 0x5A, 0x6E)  # neutral accent — rules, chips
TEXT = RGBColor(0x26, 0x31, 0x3F)  # body text
MUTED = RGBColor(0x6E, 0x7A, 0x88)  # captions, footer, secondary lines
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PRIMARY = INK  # neutral fill for bands and label blocks


@dataclass(frozen=True)
class Lane:
    """A lane (or the local non-lane) and the colours that mean it."""

    name: str
    tool: str
    color: RGBColor
    tint: RGBColor


DAILY_DRIVER = Lane(
    "Daily Driver", "Cloud model",
    RGBColor(0xB3, 0x54, 0x1E), RGBColor(0xFB, 0xE9, 0xDC),
)
LOCAL = Lane(
    "Local", "Nothing leaves the machine",
    RGBColor(0x2E, 0x7D, 0x5B), RGBColor(0xDD, 0xF0, 0xE6),
)
LANES = (DAILY_DRIVER, LOCAL)

# Fill keys so the Lesson 1/2 add_card call shape carries over:
# fill=DAILY_TINT / LOCAL_TINT colour-codes a card by lane.
DAILY_TINT = DAILY_DRIVER.tint
LOCAL_TINT = LOCAL.tint

FOOTER_TEXT = "AI for Research Management · Lesson 3 · Week 4"

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
        "accent1": DAILY_DRIVER.color,
        "accent2": LOCAL.color,
        "hlink": SLATE,
        "folHlink": SLATE,
    },
    canvas=CANVAS,
    footer_text=FOOTER_TEXT,
    footer_rule=LINE,
    footer_color=MUTED,
)


def new_presentation():
    """A 16:9 presentation with the Lesson 3 theme, canvas and footer."""
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

_TOP_BAND_HEIGHT = Inches(1.35)


def _top_band(slide, text):
    """The ink band across the top of title and divider slides."""
    band = add_bar(slide, 0, 0, SLIDE_WIDTH, _TOP_BAND_HEIGHT, INK)
    tf = band.text_frame
    tf.margin_left = Inches(0.9)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run = tf.paragraphs[0].add_run()
    run.text = text
    style(run, size=13, color=WHITE, bold=True)
    return band


def add_title_slide(prs, title, course_name, session_line):
    """Cover: ink band across the top with the course name, serif title on
    the canvas, session line, and the two-colour legend that is the colour
    key for the whole deck."""
    slide = _blank_slide(prs)
    _top_band(slide, course_name.upper())

    tf = _add_text(slide, Inches(0.9), Inches(2.0), Inches(11.5), Inches(2.4),
                   anchor=MSO_ANCHOR.BOTTOM)
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=40, color=INK, font=HEADING_FONT, bold=True)

    add_bar(slide, Inches(0.9), Inches(4.55), Inches(1.6), Pt(3), DAILY_DRIVER.color)
    add_bar(slide, Inches(2.5), Inches(4.55), Inches(1.6), Pt(3), LOCAL.color)

    tf = _add_text(slide, Inches(0.9), Inches(4.75), Inches(11.5), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = session_line
    style(run, size=16, color=MUTED)

    # Colour legend along the bottom.
    x = 0.9
    for lane in LANES:
        disc = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x), Inches(5.75), Inches(0.2), Inches(0.2))
        solid(disc, lane.color)
        tf = _add_text(slide, Inches(x + 0.3), Inches(5.63), Inches(5.4), Inches(0.4))
        run = tf.paragraphs[0].add_run()
        run.text = f"{lane.name} · {lane.tool}"
        style(run, size=12, color=TEXT)
        x += 5.8
    return slide


def add_section_divider(prs, number, total, title, duration, mode, lane=None):
    """Divider: ink band across the top with the segment count, a large
    numbered disc in the accent colour, serif title, duration · mode line,
    and progress ticks. The disc is the lane's colour when the segment
    belongs to a lane, slate otherwise."""
    slide = _blank_slide(prs)
    accent = _accent(lane)
    count = f"SEGMENT {number} OF {total}"
    if lane:
        count += f"   ·   {lane.name.upper()} · {lane.tool.upper()}"
    _top_band(slide, count)

    disc = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(0.9), Inches(2.1), Inches(2.4), Inches(2.4))
    solid(disc, accent)
    tf = disc.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = str(number)
    style(run, size=88, color=WHITE, font=HEADING_FONT, bold=True)

    tf = _add_text(slide, Inches(3.9), Inches(2.0), Inches(8.8), Inches(1.7),
                   anchor=MSO_ANCHOR.BOTTOM)
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=32, color=INK, font=HEADING_FONT, bold=True)

    add_bar(slide, Inches(3.9), Inches(3.85), Inches(1.2), Pt(3), accent)

    tf = _add_text(slide, Inches(3.9), Inches(4.0), Inches(8.8), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = f"{duration} · {mode}"
    style(run, size=18, color=accent, bold=True)

    tf = _add_text(slide, Inches(3.9), Inches(4.5), Inches(8.8), Inches(0.4))
    run = tf.paragraphs[0].add_run()
    run.text = f"Segment {number} of {total}"
    style(run, size=12, color=MUTED)

    tick_w, tick_h, gap = 0.55, 0.08, 0.2
    x = 3.9
    for i in range(1, total + 1):
        add_bar(slide, Inches(x), Inches(6.55), Inches(tick_w), Inches(tick_h),
                accent if i == number else LINE)
        x += tick_w + gap
    return slide


COMPACT_HEADER_RISE = 0.44
COMPACT_CONTENT_TOP = Inches(0.9)

TITLE_SIZE = 27
TITLE_MIN_SIZE = 21
# Average advance of bold Georgia, in inches per point of font size; a
# title wider than its box at TITLE_SIZE is shrunk so it stays on one line.
_TITLE_INCH_PER_CHAR_PT = 0.0075


def _title_size(title, width):
    """The largest title size, from TITLE_SIZE down to TITLE_MIN_SIZE, at
    which the title fits its box on one line — a two-line title crowds
    the header and the lane chip."""
    fits = Emu(width).inches / (len(title) * _TITLE_INCH_PER_CHAR_PT)
    return max(TITLE_MIN_SIZE, min(TITLE_SIZE, int(fits)))

# A lane slide's title stops short of the lane chip at the top right.
TITLE_WIDTH_WITH_CHIP = Inches(8.6)
_TITLE_BAR_WIDTH = Inches(0.12)


def add_content_slide(prs, title, body_lines=None, notes=None, compact=False,
                      lane=None):
    """Standard content slide: a vertical accent bar beside a serif ink
    title, a hairline under the header, and — when the slide belongs to a
    lane — a lane tag chip at the top right.

    body_lines is a list of strings, or (indent_level, string) tuples.
    Returns the slide so callers can add custom shapes in the content area
    (CONTENT_LEFT/TOP/WIDTH/HEIGHT). compact=True raises the header block
    by COMPACT_HEADER_RISE so content can start at COMPACT_CONTENT_TOP.
    """
    slide = _blank_slide(prs)
    accent = _accent(lane)
    rise = COMPACT_HEADER_RISE if compact else 0.0

    title_width = TITLE_WIDTH_WITH_CHIP if lane else CONTENT_WIDTH - Inches(0.3)
    tf = _add_text(slide, CONTENT_LEFT + Inches(0.3), Inches(0.45 - rise),
                   title_width, Inches(0.7), anchor=MSO_ANCHOR.BOTTOM)
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=_title_size(title, title_width), color=INK,
          font=HEADING_FONT, bold=True)

    add_bar(slide, CONTENT_LEFT, Inches(0.5 - rise), _TITLE_BAR_WIDTH, Inches(0.65), accent)

    if lane:
        add_lane_tag(slide, lane, Inches(9.33), Inches(0.5 - rise))

    add_bar(slide, CONTENT_LEFT, Inches(1.24 - rise), CONTENT_WIDTH, Pt(1), LINE)

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


def add_lane_tag(slide, lane, left, top, width=Inches(3.4)):
    """Small solid chip naming the lane in the lane's colour."""
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
    style(run, size=9.5, color=WHITE, bold=True)
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


EDGE_BAR = Inches(0.09)


def add_open_card(slide, left, top, width, height, edge):
    """A white card with a coloured edge bar and an *empty*, vertically
    centred text frame, for callers whose text is several runs at their own
    sizes."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    outlined(card, PANEL, LINE)
    add_bar(slide, left, top, EDGE_BAR, height, edge)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.26)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT
    return card


def add_card(slide, left, top, width, height, fill, heading, heading_color,
             body=None):
    """Card on the canvas. A lane colour (or INK/SLATE) as fill gives a
    solid label block with a centred white heading. A lane tint or PANEL
    gives a white or tinted card with a hairline border and an edge bar —
    the lane's colour for a tinted card, slate for a neutral one."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    lane = _lane_of_fill(fill)
    dark = fill in (PRIMARY, INK, SLATE) or (lane is not None and fill == lane.color)
    if dark:
        solid(card, fill)
        heading_color = WHITE
    else:
        outlined(card, fill, LINE)
        add_bar(slide, left, top, EDGE_BAR, height,
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


def add_list_card(slide, left, top, width, height, fill, heading, items,
                  size=13):
    """add_card's heading over bulleted items, top-anchored."""
    card = add_card(slide, left, top, width, height, fill, heading, INK)
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.16)
    for item in items:
        para = tf.add_paragraph()
        para.space_before = Pt(5)
        run = para.add_run()
        run.text = f"·  {item}"
        style(run, size=size, color=TEXT)
    return card


def add_detail_card(slide, left, top, width, height, edge, heading, lines,
                    heading_size=13, line_size=11.5):
    """A bold lead over one or more lines of detail, on add_open_card,
    top-anchored. One line reads as a sentence; several take bullets."""
    card = add_open_card(slide, left, top, width, height, edge)
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.14)
    run = tf.paragraphs[0].add_run()
    run.text = heading
    style(run, size=heading_size, color=INK, font=HEADING_FONT, bold=True)
    marker = "·  " if len(lines) > 1 else ""
    for line in lines:
        para = tf.add_paragraph()
        para.space_before = Pt(3)
        run = para.add_run()
        run.text = f"{marker}{line}"
        style(run, size=line_size, color=TEXT)
    return card


def add_label(slide, left, top, width, text, size=14, color=MUTED, italic=False,
              align=PP_ALIGN.LEFT, bold=False):
    """Small free-standing caption/label text."""
    box = slide.shapes.add_textbox(left, top, width, Inches(0.4))
    tf = box.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = align
    run = tf.paragraphs[0].add_run()
    style(run, size=size, color=color, italic=italic, bold=bold)
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


def add_table(slide, top, columns, rows, row_height, size=11, header_size=10,
              left=CONTENT_LEFT, edge=SLATE, row_edges=None, first_bold=True,
              row_gap=Inches(0.07)):
    """A grid of white row cards with a header line above: one card per row,
    a coloured edge bar at its left (edge, or row_edges[i] per row), and one
    text box per column inside it. columns is a list of (width, header)
    pairs; rows a list of lists of cell strings, the first cell bold when
    first_bold. Returns the row cards, so a caller can restyle one."""
    x = left
    for width, header in columns:
        if header:
            add_label(slide, x, top, width, header.upper(), size=header_size,
                      color=MUTED, bold=True)
        x += width
    y = top + (Inches(0.34) if any(h for _, h in columns) else 0)
    cards = []
    total = sum(w for w, _ in columns)
    for i, row in enumerate(rows):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, y, total, row_height)
        outlined(card, PANEL, LINE)
        add_bar(slide, left, y, EDGE_BAR, row_height,
                row_edges[i] if row_edges else edge)
        x = left + EDGE_BAR
        for j, ((width, _), cell) in enumerate(zip(columns, row)):
            cell_width = width - EDGE_BAR if j == 0 else width
            tf = _add_text(slide, x, y, cell_width, row_height, anchor=MSO_ANCHOR.MIDDLE)
            tf.margin_left = Inches(0.14)
            tf.margin_right = Inches(0.1)
            tf.margin_top = Inches(0.02)
            tf.margin_bottom = Inches(0.02)
            run = tf.paragraphs[0].add_run()
            run.text = cell
            bold = first_bold and j == 0
            style(run, size=size, color=INK if bold else TEXT, bold=bold)
            x += cell_width
        cards.append(card)
        y += row_height + row_gap
    return cards


def add_badge(slide, left, top, size, text):
    """A solid slate square with a centred white number — the step badge
    the numbered blocks below and the segment modules share."""
    return add_card(slide, left, top, size, size, SLATE, text, WHITE)


def add_numbered_rows(slide, rows, top, pitch, height, edge, size=11.5,
                      trailing_width=None, left=CONTENT_LEFT, width=CONTENT_WIDTH):
    """Rows of badge + white text card, optionally with a short trailing
    cell (a timing, say). rows are (number, text) or (number, text, tail)
    tuples; top, pitch, height and trailing_width are in inches."""
    badge = Inches(0.5)
    for i, row in enumerate(rows):
        number, text, *rest = row
        y = Inches(top + i * pitch)
        add_badge(slide, left, y + (Inches(height) - badge) // 2, badge, number)
        text_left = left + badge + Inches(0.15)
        text_width = width - badge - Inches(0.15)
        if trailing_width:
            text_width -= Inches(trailing_width + 0.1)
        card = add_open_card(slide, text_left, y, text_width, Inches(height), edge)
        run = card.text_frame.paragraphs[0].add_run()
        run.text = text
        style(run, size=size, color=TEXT)
        if rest and trailing_width:
            tail = add_open_card(slide, text_left + text_width + Inches(0.1), y,
                                 Inches(trailing_width), Inches(height), edge)
            tail.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            run = tail.text_frame.paragraphs[0].add_run()
            run.text = rest[0]
            style(run, size=size, color=INK, bold=True)

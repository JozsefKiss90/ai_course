"""Design template for the Lesson 1 deck — the single source of visual truth.

Every slide in the deck is created through the helpers here, so fonts,
colors, and the footer stay uniform no matter which segment module adds
the slide. The theme (fonts + color scheme) is written into the slide
master's theme part, and the footer is a master shape, so both apply to
all slides.
"""

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.util import Emu, Inches, Pt

# --- Design constants -------------------------------------------------------

HEADING_FONT = "Segoe UI Semibold"
BODY_FONT = "Segoe UI"

PRIMARY = RGBColor(0x1F, 0x38, 0x64)  # navy — headings, divider band
ACCENT = RGBColor(0x2E, 0x75, 0xB6)  # mid blue — rules, secondary text
HIGHLIGHT = RGBColor(0xC5, 0x5A, 0x11)  # warm orange — demo cues, emphasis
TEXT = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x59, 0x59, 0x59)
PALE = RGBColor(0xDE, 0xEB, 0xF7)  # pale blue — placeholder cards, fills
PALE_WARM = RGBColor(0xFB, 0xE5, 0xD6)  # pale orange — alternating chips, soft emphasis
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FOOTER_TEXT = "AI for Research Management · Lesson 1 · Week 1"

SLIDE_WIDTH = Emu(12192000)  # 13.333 in — 16:9 for Teams
SLIDE_HEIGHT = Emu(6858000)  # 7.5 in

# Content area shared by all content slides (below the title block).
CONTENT_LEFT = Inches(0.6)
CONTENT_TOP = Inches(1.5)
CONTENT_WIDTH = Inches(12.13)
CONTENT_HEIGHT = Inches(5.3)

_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
_P = "http://schemas.openxmlformats.org/presentationml/2006/main"


# --- Presentation setup -----------------------------------------------------


def new_presentation():
    """A 16:9 presentation with theme fonts/colors and footer on the master."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    _apply_theme(prs)
    _add_master_footer(prs)
    return prs


def _apply_theme(prs):
    """Write our fonts and color scheme into the master's theme part."""
    theme_part = prs.slide_master.part.part_related_by(RT.THEME)
    root = etree.fromstring(theme_part.blob)
    for tag, font in (("majorFont", HEADING_FONT), ("minorFont", BODY_FONT)):
        latin = root.find(f".//{{{_A}}}{tag}/{{{_A}}}latin")
        latin.set("typeface", font)
    scheme = root.find(f".//{{{_A}}}clrScheme")
    for name, color in (("dk2", PRIMARY), ("accent1", ACCENT), ("accent2", HIGHLIGHT)):
        srgb = scheme.find(f"{{{_A}}}{name}/{{{_A}}}srgbClr")
        if srgb is not None:
            srgb.set("val", str(color))
    theme_part._blob = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    )


def solid(shape, color):
    """Flat fill with no outline or shadow — the deck's shape style."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False


def master_next_id(master):
    """Next free shape id on the master, ignoring the near-2^31 ids the
    stock template uses for its footer placeholders — ids above the signed
    32-bit limit make PowerPoint report the file as corrupt."""
    ids = [
        int(el.get("id"))
        for el in master.shapes._spTree.iter(f"{{{_P}}}cNvPr")
    ]
    return max((i for i in ids if i < 0x7F000000), default=1) + 1


def _master_add_shape(master, sp):
    """Append a shape element to the master's shape tree (python-pptx's
    MasterShapes collection has no add_shape/add_textbox of its own)."""
    from pptx.shapes.autoshape import Shape

    master.shapes._spTree.append(sp)
    return Shape(sp, master.shapes)


def _add_master_footer(prs):
    """Footer rule + text on the slide master, inherited by every slide."""
    from pptx.oxml.shapes.autoshape import CT_Shape

    master = prs.slide_master

    sp = CT_Shape.new_autoshape_sp(
        master_next_id(master), "Footer Rule", "rect",
        Inches(0.6), Inches(7.08), Inches(12.13), Pt(1.2),
    )
    line = _master_add_shape(master, sp)
    solid(line, ACCENT)

    sp = CT_Shape.new_textbox_sp(
        master_next_id(master), "Footer Text",
        Inches(0.6), Inches(7.13), Inches(12.13), Inches(0.3),
    )
    box = _master_add_shape(master, sp)
    tf = box.text_frame
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    para = tf.paragraphs[0]
    run = para.add_run()
    run.text = FOOTER_TEXT
    style(run, size=10, color=MUTED)


def style(run, size, color, font=BODY_FONT, bold=False, italic=False):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic


def _blank_slide(prs):
    return prs.slides.add_slide(prs.slide_master.slide_layouts[6])


def _add_text(slide, left, top, width, height, align=PP_ALIGN.LEFT, anchor=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    if anchor is not None:
        tf.vertical_anchor = anchor
    tf.paragraphs[0].alignment = align
    return tf


def set_notes(slide, notes):
    slide.notes_slide.notes_text_frame.text = notes


# --- Slide builders ---------------------------------------------------------


def add_title_slide(prs, title, course_name, session_line):
    """Full-width navy band with the lesson title; course name above."""
    slide = _blank_slide(prs)

    tf = _add_text(slide, Inches(0.9), Inches(1.55), Inches(11.5), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = course_name.upper()
    style(run, size=16, color=ACCENT, font=HEADING_FONT)

    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, Inches(2.2), SLIDE_WIDTH, Inches(2.3)
    )
    solid(band, PRIMARY)
    tf = band.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.9)
    tf.margin_right = Inches(0.9)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=36, color=WHITE, font=HEADING_FONT, bold=True)

    tf = _add_text(slide, Inches(0.9), Inches(4.8), Inches(11.5), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = session_line
    style(run, size=16, color=MUTED)
    return slide


def add_section_divider(prs, number, total, title, duration, mode):
    """Navy left column with the big segment number; title and timing right."""
    slide = _blank_slide(prs)

    # Stops at the footer rule (y=7.08") so the master footer stays legible.
    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(2.6), Inches(7.08)
    )
    solid(band, PRIMARY)
    tf = band.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = str(number)
    style(run, size=96, color=WHITE, font=HEADING_FONT, bold=True)

    tf = _add_text(
        slide, Inches(3.1), Inches(2.35), Inches(9.4), Inches(1.6),
        anchor=MSO_ANCHOR.BOTTOM,
    )
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=32, color=PRIMARY, font=HEADING_FONT, bold=True)

    tf = _add_text(slide, Inches(3.1), Inches(4.1), Inches(9.4), Inches(0.5))
    run = tf.paragraphs[0].add_run()
    run.text = f"{duration} · {mode}"
    style(run, size=18, color=ACCENT)

    tf = _add_text(slide, Inches(3.1), Inches(4.65), Inches(9.4), Inches(0.4))
    run = tf.paragraphs[0].add_run()
    run.text = f"Segment {number} of {total}"
    style(run, size=12, color=MUTED)
    return slide


def add_content_slide(prs, title, body_lines=None, notes=None):
    """Standard content slide: navy title, accent underline, optional bullets.

    body_lines is a list of strings, or (indent_level, string) tuples.
    Returns the slide so callers can add custom shapes in the content area
    (CONTENT_LEFT/TOP/WIDTH/HEIGHT).
    """
    slide = _blank_slide(prs)

    tf = _add_text(slide, Inches(0.6), Inches(0.45), Inches(12.13), Inches(0.7))
    run = tf.paragraphs[0].add_run()
    run.text = title
    style(run, size=28, color=PRIMARY, font=HEADING_FONT, bold=True)

    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.2), Inches(1.6), Pt(3)
    )
    solid(rule, ACCENT)

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


def add_demo_cue(slide, text, top, left=CONTENT_LEFT, width=CONTENT_WIDTH):
    """Orange live-demo marker: the facilitator switches to a live tool here.

    Renders as a filled band reading "▶ LIVE DEMO — <text>". Callers must
    also mention the demo in the slide's speaker notes.
    """
    band = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.55)
    )
    solid(band, HIGHLIGHT)
    tf = band.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run = tf.paragraphs[0].add_run()
    run.text = f"▶ LIVE DEMO — {text}"
    style(run, size=16, color=WHITE, font=HEADING_FONT, bold=True)
    return band


def add_placeholder_slide(prs, segment_label, planned_title, gist, ticket):
    """A visibly-unfinished slide standing in for one planned content slide."""
    slide = add_content_slide(prs, planned_title)

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.6), Inches(2.3), Inches(10.1), Inches(2.9)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = PALE
    card.line.color.rgb = ACCENT
    card.shadow.inherit = False
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = f"[PLACEHOLDER] {segment_label}"
    style(run, size=20, color=PRIMARY, font=HEADING_FONT, bold=True)
    para = tf.add_paragraph()
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = gist
    style(run, size=14, color=MUTED)

    set_notes(
        slide,
        f"Placeholder — replaced by ticket {ticket} ({segment_label}). "
        f"Planned content: {gist}",
    )
    return slide

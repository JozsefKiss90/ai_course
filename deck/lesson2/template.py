"""Design template for the Lesson 2 deck — the single source of visual truth
for Lesson 2, on top of the shared mechanics in deck/core.py.

Ticket 03 of the Lesson 2 effort fills this in: its own fonts and palette
(distinct from Lesson 1's dark navy), the lane colour-coding, and the
title/divider/content/placeholder/demo-cue builders plus the in-slide
blocks (card, band, label) with the same call shapes as deck/template.py.
Until then the module carries only the footer and the presentation setup,
so the build entry point already produces a valid (empty) Lesson 2 file.
"""

from pptx.dml.color import RGBColor

from deck import core

FOOTER_TEXT = "AI for Research Management · Lesson 2 · Week 2"

# Provisional stand-ins until ticket 03 chooses the Lesson 2 design.
HEADING_FONT = "Segoe UI Semibold"
BODY_FONT = "Segoe UI"
CANVAS = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xC8, 0xCF, 0xD9)
MUTED = RGBColor(0x5F, 0x6B, 0x7A)

DESIGN = core.Design(
    heading_font=HEADING_FONT,
    body_font=BODY_FONT,
    canvas=CANVAS,
    footer_text=FOOTER_TEXT,
    footer_rule=LINE,
    footer_color=MUTED,
)


def new_presentation():
    """A 16:9 presentation carrying the Lesson 2 footer and theme."""
    return core.new_presentation(DESIGN)

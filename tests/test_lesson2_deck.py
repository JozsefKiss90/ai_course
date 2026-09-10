"""Structural tests for the Lesson 2 deck skeleton (ticket 03 of the
Lesson 2 effort).

Every assertion runs against a saved-and-reopened .pptx, so it checks what
PowerPoint will load. The Timing Overview in lesson_2.md is the oracle for
segment names, durations and modes, as lesson_1.md is for the Lesson 1
deck.
"""

import os
import tempfile

import pytest
from pptx import Presentation

from deck.lesson2.build import build_presentation


def _slide_text(slide):
    """All visible text on a slide, joined."""
    return "\n".join(
        shape.text_frame.text for shape in slide.shapes if shape.has_text_frame
    )


@pytest.fixture(scope="module")
def reopened():
    """Build the deck, save it, and reopen it the way PowerPoint would."""
    prs = build_presentation()
    fd, path = tempfile.mkstemp(suffix=".pptx")
    os.close(fd)
    try:
        prs.save(path)
        yield Presentation(path)
    finally:
        os.unlink(path)


# --- Title slide ------------------------------------------------------------


def test_title_slide_names_the_lesson_course_week_and_length(reopened):
    text = _slide_text(reopened.slides[0])
    assert "Lesson 2 — The Two-Lane Tool Landscape" in text
    assert "ai for research management" in text.lower()
    assert "Week 2" in text
    assert "60 minutes" in text


# --- Section dividers ---------------------------------------------------------

# The Timing Overview table from lesson_2.md — the independent source of truth.
TIMING_OVERVIEW = [
    ("Recap + assignment debrief", "15 min", "Participant demos, facilitated"),
    ("The sensitive-data rule and data-protection principles", "10 min", "Presentation"),
    ("Copilot Chat (Basic) in practice", "12 min", "Live facilitator demo"),
    ("Gemini in depth (+ NotebookLM preview)", "15 min", "Live facilitator demo"),
    ("Assignment briefing + close", "8 min", "Presentation + Q&A"),
]


def test_each_segment_has_a_divider_with_duration_and_mode(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    for number, (name, duration, mode) in enumerate(TIMING_OVERVIEW, start=1):
        dividers = [t for t in all_slides if name in t and f"{duration} · {mode}" in t]
        assert dividers, f"no divider found for segment {number} ({name})"
        assert any(f"Segment {number} of 5" in t for t in dividers)


def test_dividers_appear_in_session_order_after_the_title(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = [
        next(i for i, t in enumerate(all_slides) if name in t)
        for name, _, _ in TIMING_OVERVIEW
    ]
    assert positions == sorted(positions)
    assert positions[0] > 0


# --- Placeholders per segment -----------------------------------------------

# Placeholder slides each segment carries until tickets 04–08 land, sized
# from the slide inventory implied by lesson_2.md's segment plans, and the
# ticket that replaces them.
EXPECTED_PLACEHOLDERS = {
    "Recap + assignment debrief": (3, "04"),
    "The sensitive-data rule and data-protection principles": (5, "05"),
    "Copilot Chat (Basic) in practice": (7, "06"),
    "Gemini in depth (+ NotebookLM preview)": (11, "07"),
    "Assignment briefing + close": (3, "08"),
}


def _segment_ranges(reopened):
    """Map divider name -> the slides between that divider and the next."""
    all_slides = [_slide_text(s) for s in reopened.slides]
    starts = {
        name: next(i for i, t in enumerate(all_slides) if name in t)
        for name in EXPECTED_PLACEHOLDERS
    }
    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    ranges = {}
    for (name, start), nxt in zip(ordered, [s for _, s in ordered[1:]] + [len(all_slides)]):
        ranges[name] = list(reopened.slides)[start + 1 : nxt]
    return ranges


def test_each_segment_has_its_placeholder_slides(reopened):
    for name, slides in _segment_ranges(reopened).items():
        count = sum(1 for s in slides if "[PLACEHOLDER]" in _slide_text(s))
        expected, _ = EXPECTED_PLACEHOLDERS[name]
        assert count == expected, f"{name}: {count} placeholders, expected {expected}"


def test_placeholder_slides_name_their_ticket_on_the_slide_and_in_notes(reopened):
    for name, slides in _segment_ranges(reopened).items():
        _, ticket = EXPECTED_PLACEHOLDERS[name]
        for slide in slides:
            if "[PLACEHOLDER]" not in _slide_text(slide):
                continue
            assert f"ticket {ticket}" in _slide_text(slide), name
            notes = slide.notes_slide.notes_text_frame.text
            assert f"ticket {ticket}" in notes, name


def test_total_slide_count(reopened):
    # 1 title + 5 dividers + 29 placeholders
    assert len(reopened.slides) == 35


# --- Master, theme and the Lesson 2 look ------------------------------------


def _theme_xml(reopened):
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    return reopened.slide_masters[0].part.part_related_by(RT.THEME).blob.decode("utf-8")


def test_master_defines_the_lesson_2_footer_and_theme_fonts(reopened):
    master = reopened.slide_masters[0]
    master_text = "\n".join(
        s.text_frame.text for s in master.shapes if s.has_text_frame
    )
    assert "Lesson 2 · Week 2" in master_text
    assert "Lesson 1" not in master_text
    theme_xml = _theme_xml(reopened)
    assert 'typeface="Cambria"' in theme_xml
    assert 'typeface="Calibri"' in theme_xml


def test_look_is_not_lesson_1s(reopened):
    """A light canvas, non-Segoe fonts, and none of Lesson 1's theme colours."""
    from deck import template as lesson1

    theme_xml = _theme_xml(reopened)
    assert "Segoe" not in theme_xml
    for color in (lesson1.PRIMARY, lesson1.ACCENT, lesson1.HIGHLIGHT):
        assert str(color) not in theme_xml
    canvas = reopened.slide_masters[0].background.fill.fore_color.rgb
    assert canvas != lesson1.CANVAS
    r, g, b = canvas[0], canvas[1], canvas[2]
    assert min(r, g, b) > 0xE0, "Lesson 2 canvas is light, not navy"


def test_fonts_and_sizes_are_explicit_everywhere(reopened):
    for i, slide in enumerate(reopened.slides):
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    assert run.font.name in ("Cambria", "Calibri"), (
                        f"slide {i + 1}: font {run.font.name!r} in {run.text!r}"
                    )
                    assert run.font.size is not None, (
                        f"slide {i + 1}: inherited size in {run.text!r}"
                    )


# --- Lane colour-coding ------------------------------------------------------


def _fills(slide):
    fills = set()
    for shape in slide.shapes:
        try:
            if shape.fill.type is not None and shape.fill.fore_color.rgb:
                fills.add(str(shape.fill.fore_color.rgb))
        except (AttributeError, TypeError):
            continue
    return fills


def test_lane_segments_are_colour_coded_by_lane(reopened):
    """Segment 3 (Copilot) carries the Sensitive Lane colour and never the
    Daily Driver's; Segment 4 (Gemini) the reverse — divider and every
    slide. Segments about both lanes (2, 5) or neither (1) may use either
    colour where they name a tool, so they are not constrained here."""
    from deck.lesson2 import template

    teal, violet = str(template.SENSITIVE_LANE.color), str(template.DAILY_DRIVER.color)
    all_slides = list(reopened.slides)
    ranges = _segment_ranges(reopened)
    expected = {
        "Copilot Chat (Basic) in practice": (teal, violet),
        "Gemini in depth (+ NotebookLM preview)": (violet, teal),
    }
    for name, (own, other) in expected.items():
        slides = ranges[name]
        divider = all_slides[all_slides.index(slides[0]) - 1]
        for slide in [divider, *slides]:
            fills = _fills(slide)
            assert own in fills, f"{name}: slide without its lane colour"
            assert other not in fills, f"{name}: other lane's colour present"


# --- Terminology ------------------------------------------------------------

# Forbidden synonyms from the CONTEXT.md Avoid-lists, the same list the
# Lesson 1 deck is audited against (see tests/test_deck.py for why the
# generic words are left out).
FORBIDDEN_TERMS = [
    "homework week", "self-study week", "blank week", "blank lesson",
    "breakout team", "domain team",
    "knowledge base", "shared wiki", "team wiki",
    "use case", "case study", "team project",
    "home base", "primary AI environment",
    "workhorse", "main tool",
    "tool ecosystem", "satellite tool",
]


def test_terminology_audit_no_forbidden_synonyms(reopened):
    for i, slide in enumerate(reopened.slides):
        corpus = _slide_text(slide)
        if slide.has_notes_slide:
            corpus += "\n" + slide.notes_slide.notes_text_frame.text
        corpus = corpus.lower()
        for term in FORBIDDEN_TERMS:
            assert term.lower() not in corpus, f"{term!r} on slide {i + 1}"


# --- Builders keep the Lesson 1 call shapes ----------------------------------


def test_builders_accept_the_lesson_1_call_shapes_and_survive_a_roundtrip():
    """A segment author calls the Lesson 2 template exactly as a Lesson 1
    segment module calls deck/template.py; the result opens after a
    save-and-reopen."""
    from pptx.util import Inches

    from deck.lesson2 import template

    prs = template.new_presentation()
    slide = template.add_content_slide(
        prs, "Sample", ["one", (1, "two")], notes="n", lane=template.DAILY_DRIVER,
    )
    template.add_demo_cue(slide, "open Gemini", Inches(1.6), lane=template.DAILY_DRIVER)
    template.add_band(slide, Inches(2.4), Inches(0.8), "Band", sub="sub")
    template.add_card(slide, Inches(0.6), Inches(3.5), Inches(4.0), Inches(1.5),
                      template.DAILY_TINT, "Card", template.INK, "body")
    template.add_card(slide, Inches(4.8), Inches(3.5), Inches(4.0), Inches(1.5),
                      template.SENSITIVE_LANE.color, "Label block", template.WHITE)
    template.add_label(slide, Inches(0.6), Inches(5.3), Inches(4.0), "caption")

    fd, path = tempfile.mkstemp(suffix=".pptx")
    os.close(fd)
    try:
        prs.save(path)
        reopened = Presentation(path)
    finally:
        os.unlink(path)
    text = _slide_text(reopened.slides[0])
    for expected in ("Sample", "one", "two", "LIVE DEMO — open Gemini", "Band",
                     "sub", "Card", "body", "Label block", "caption",
                     "DAILY DRIVER"):
        assert expected in text, expected
    assert reopened.slides[0].notes_slide.notes_text_frame.text == "n"

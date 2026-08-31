"""Structural tests for the Lesson 1 deck build script (ticket 01).

All assertions run against a saved-and-reopened .pptx, so they verify what
PowerPoint will actually load, not just the in-memory object.
"""

import pytest
from pptx import Presentation

from deck.build import build_presentation


def _slide_text(slide):
    """All visible text on a slide, joined."""
    chunks = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            chunks.append(shape.text_frame.text)
    return "\n".join(chunks)


@pytest.fixture(scope="module")
def reopened():
    """Build the deck, save it, and reopen it the way PowerPoint would."""
    prs = build_presentation()
    import tempfile, os

    fd, path = tempfile.mkstemp(suffix=".pptx")
    os.close(fd)
    try:
        prs.save(path)
        yield Presentation(path)
    finally:
        os.unlink(path)


def test_title_slide_names_the_lesson(reopened):
    first = reopened.slides[0]
    text = _slide_text(first)
    assert "Lesson 1 — Why AI, How LLMs Work, and the Map Ahead" in text
    assert "ai for research management" in text.lower()


# The Timing Overview table from lesson_1.md — the independent source of truth.
TIMING_OVERVIEW = [
    ("Opening: why this matters", "10 min", "Presentation"),
    ("The map: LLM fundamentals + 7 Levels tour", "15 min", "Presentation"),
    ("Prompt engineering: ICC, meta-prompting, patterns", "25 min", "Live facilitator demo"),
    ("Assignment briefing + close", "10 min", "Presentation + Q&A"),
    ("Guided setup block", "30 min", "Hands-on, facilitated"),
]


def test_each_segment_has_a_divider_with_duration_and_mode(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    for number, (name, duration, mode) in enumerate(TIMING_OVERVIEW, start=1):
        dividers = [t for t in all_slides if name in t and f"{duration} · {mode}" in t]
        assert dividers, f"no divider found for segment {number} ({name})"
        assert any(str(number) in t for t in dividers)


def test_dividers_appear_in_session_order(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for name, _, _ in TIMING_OVERVIEW:
        positions.append(next(i for i, t in enumerate(all_slides) if name in t))
    assert positions == sorted(positions)
    assert positions[0] > 0  # title slide comes first


# Placeholder slides each segment carries until tickets 02–07 land, sized
# from the slide inventory implied by lesson_1.md's segment plans.
EXPECTED_PLACEHOLDERS = {
    "Opening: why this matters": 4,
    "The map: LLM fundamentals + 7 Levels tour": 9,  # 2A (7) + 2B (2)
    "Prompt engineering: ICC, meta-prompting, patterns": 6,
    "Assignment briefing + close": 4,
    "Guided setup block": 3,
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
        assert count == EXPECTED_PLACEHOLDERS[name], (
            f"{name}: {count} placeholders, expected {EXPECTED_PLACEHOLDERS[name]}"
        )


def test_total_slide_count(reopened):
    # 1 title + 5 dividers + 26 placeholders
    assert len(reopened.slides) == 32


def test_placeholder_slides_carry_notes_naming_their_ticket(reopened):
    for slide in reopened.slides:
        if "[PLACEHOLDER]" in _slide_text(slide):
            notes = slide.notes_slide.notes_text_frame.text
            assert "ticket" in notes.lower()


def test_master_defines_footer_and_theme_fonts(reopened):
    master = reopened.slide_masters[0]
    master_text = "\n".join(
        s.text_frame.text for s in master.shapes if s.has_text_frame
    )
    assert "AI for Research Management · Lesson 1" in master_text

    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    theme_xml = master.part.part_related_by(RT.THEME).blob.decode("utf-8")
    assert "Segoe UI" in theme_xml
    assert "1F3864" in theme_xml  # navy in the color scheme

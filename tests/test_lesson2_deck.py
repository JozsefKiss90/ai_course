"""Structural tests for the Lesson 2 deck skeleton (ticket 03 of the
Lesson 2 effort).

Every assertion runs against a saved-and-reopened .pptx, so it checks what
PowerPoint will load. The Timing Overview in lesson_2.md is the oracle for
segment names, durations and modes, as lesson_1.md is for the Lesson 1
deck.
"""

import os
import re
import tempfile
from pathlib import Path

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
    "Recap + assignment debrief": (0, "04"),  # ticket 04 landed
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
    # 1 title + 5 dividers + 3 Segment 1 slides + 26 placeholders
    assert len(reopened.slides) == 35


# --- Segment 1: Recap + assignment debrief (ticket 04) -----------------------

# The plan is the oracle. Unlike TIMING_OVERVIEW above (transcribed from
# lesson_2.md, so the copy is independent), the recap rows are read out of
# the plan's Part A table at test time: the ticket asks for a test that
# checks the pairs "against the plan", and the table's seven rows are too
# long to transcribe without the copy itself becoming the thing that
# drifts. A row added to or dropped from the plan fails the deck here.
PLAN_PATH = Path(__file__).resolve().parents[1] / "lesson_2.md"

RECAP_TITLE = "Lesson 1 → Lesson 2: the recap map"
DEBRIEF_TITLE = "Assignment debrief — the next 12 minutes"
CAPTURE_TITLE = "Common problems — captured live"
SEG1_TITLES = [RECAP_TITLE, DEBRIEF_TITLE, CAPTURE_TITLE]

# One (concept token, link token) pair per row of the plan's recap table,
# in the plan's order. Each token is asserted to appear in its plan cell
# first, so the pairs cannot drift from the plan; matching is
# case-sensitive, which is what keeps "Meta-prompting" (the concept) from
# matching "meta-prompting" inside its own link cell.
RECAP_TOKENS = [
    ("7 Levels", "Level 3"),
    ("ICC", "lane decides"),
    ("Ask-me-first", "standing instructions"),
    ("Meta-prompting", "packaged agent"),
    ("two rules", "two-lane rule"),
    ("Anchor Project", "anonymise-before-upload"),
    ("Context window", "curation"),
]


def _slide_by_title(reopened, title):
    """The slide whose text contains `title`; exactly one must."""
    matches = [s for s in reopened.slides if title in _slide_text(s)]
    assert len(matches) == 1, f"{title!r}: {len(matches)} slides matched"
    return matches[0]


def _shape_containing(slide, token):
    """The single shape whose text contains `token` (case-sensitive)."""
    matches = [
        sh for sh in slide.shapes
        if sh.has_text_frame and token in sh.text_frame.text
    ]
    assert len(matches) == 1, f"{token!r}: {len(matches)} shapes matched"
    return matches[0]


def _recap_rows_from_plan():
    """The (concept, leads-into) rows of the Part A table in lesson_2.md."""
    text = PLAN_PATH.read_text(encoding="utf-8")
    part_a = text[text.index("### Part A: The recap map"):text.index("### Part B")]
    rows = []
    for line in part_a.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0].startswith("Lesson 1 concept"):
            continue
        rows.append((cells[0], cells[1]))
    return rows


def _segment_refs(text):
    """The segment numbers a piece of text points forward to — "Segment 4",
    "Segments 3 · 4", "Segments 3 and 4"."""
    refs = set()
    for chunk in re.findall(r"Segments?\s+(\d+(?:\s*(?:·|,|and)\s*\d+)*)", text):
        refs.update(int(d) for d in re.findall(r"\d+", chunk))
    return refs


def test_seg1_slides_present_in_order_and_not_placeholders(reopened):
    """All three slides live between Segment 1's divider and Segment 2's,
    in the plan's order, with no placeholder left."""
    segment = _segment_ranges(reopened)["Recap + assignment debrief"]
    texts = [_slide_text(s) for s in segment]
    positions = []
    for title in SEG1_TITLES:
        matches = [i for i, t in enumerate(texts) if title in t]
        assert matches, f"{title!r} is not in Segment 1"
        assert "[PLACEHOLDER]" not in texts[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_recap_map_pairs_every_plan_concept_with_its_lesson_2_link(reopened):
    """Every row of the plan's Part A table is on the slide as a concept
    sitting to the left of the Lesson 2 topic it leads into, and the link
    keeps the plan's forward references."""
    slide = _slide_by_title(reopened, RECAP_TITLE)
    plan_rows = _recap_rows_from_plan()
    assert len(plan_rows) == len(RECAP_TOKENS), (
        f"plan has {len(plan_rows)} recap rows, tokens cover {len(RECAP_TOKENS)}"
    )

    tops = []
    for (concept_cell, link_cell), (concept, link) in zip(plan_rows, RECAP_TOKENS):
        assert concept in concept_cell, f"{concept!r} not in the plan's concept cell"
        assert link in link_cell, f"{link!r} not in the plan's leads-into cell"

        concept_shape = _shape_containing(slide, concept)
        link_shape = _shape_containing(slide, link)
        assert concept_shape.top == link_shape.top, f"{concept!r}: link not alongside"
        assert concept_shape.left < link_shape.left, f"{concept!r}: link not to its right"

        planned = _segment_refs(concept_cell) | _segment_refs(link_cell)
        assert planned <= _segment_refs(link_shape.text_frame.text), (
            f"{concept!r}: slide points to "
            f"{_segment_refs(link_shape.text_frame.text)}, plan to {planned}"
        )
        tops.append(concept_shape.top)

    assert tops == sorted(tops), "recap rows are not in the plan's order"


# Wording that would mean a Lesson 1 concept is being explained again
# rather than referenced — the recap map links, it never re-teaches.
DEFINITION_MARKERS = [
    " is a ", " is an ", " is the ", " are the ", " means ", " refers to ",
    " stands for ", "in other words", "that is, ", "which is ",
]


def test_recap_map_restates_no_lesson_1_definition(reopened):
    """No cell on the recap slide explains a concept: no definition
    wording and no multi-sentence prose — each cell is a link, not a
    lesson."""
    slide = _slide_by_title(reopened, RECAP_TITLE)
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if RECAP_TITLE in text:
            continue
        lowered = text.lower()
        for marker in DEFINITION_MARKERS:
            assert marker not in lowered, f"{marker!r} in {text!r}"
        assert not re.search(r"\.\s+[A-Z“]", text), f"explanation prose in {text!r}"


def test_debrief_slide_states_the_format_and_the_four_items(reopened):
    text = _slide_text(_slide_by_title(reopened, DEBRIEF_TITLE))
    assert "2–3 volunteers" in text
    assert "4 minutes" in text          # the per-volunteer time box
    assert "12 minutes" in text         # the segment's time box
    assert "Gemini" in text             # screen-shared from their own account

    # The four assignment items, in the plan's order.
    items = ["Anchor Project", "ICC prompt", "Ask-me-first", "meta-prompt"]
    positions = []
    for item in items:
        assert item.lower() in text.lower(), f"{item!r} missing from the debrief slide"
        positions.append(text.lower().index(item.lower()))
    assert positions == sorted(positions), "the four items are out of plan order"


def test_debrief_slide_carries_the_facilitator_questions(reopened):
    text = _slide_text(_slide_by_title(reopened, DEBRIEF_TITLE)).lower()
    assert "anonymise or invent" in text
    assert "five sentences" in text


def test_capture_slide_tags_the_four_items_and_routes_the_problems(reopened):
    """The capture slide is empty space the facilitator fills live, tagged
    by assignment item, with the routing the plan gives."""
    slide = _slide_by_title(reopened, CAPTURE_TITLE)
    text = _slide_text(slide)
    for tag in ("Anchor Project", "ICC", "Ask-me-first", "Meta-prompt"):
        assert tag in text, f"capture lane {tag!r} missing"
    assert _segment_refs(text) >= {2, 3, 4}, "the routing loses a segment"
    assert "Practice Week 1" in text

    # Blank lanes to write in: cards with no text of their own.
    blank = [
        sh for sh in slide.shapes
        if sh.has_text_frame and not sh.text_frame.text.strip()
    ]
    assert len(blank) >= 4, "no blank capture lanes to write in"


def test_every_seg1_slide_has_speaker_notes(reopened):
    for title in SEG1_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


def test_seg1_notes_carry_the_time_keeping_script(reopened):
    """The facilitation script that keeps the demos on time lives in the
    notes: the 3-minute chat warning, the cut at 4, and where an
    unfinished assignment goes."""
    notes = " ".join(
        _slide_by_title(reopened, t).notes_slide.notes_text_frame.text
        for t in SEG1_TITLES
    ).lower()
    assert "3-minute" in notes or "three-minute" in notes
    assert "cut at 4" in notes
    assert "practice week 1" in notes
    assert "backup" in notes  # the spare volunteer if a screen-share fails


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

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
    "Opening: why this matters": 0,  # ticket 02 landed
    "The map: LLM fundamentals + 7 Levels tour": 0,  # tickets 03 + 04 landed
    "Prompt engineering: ICC, meta-prompting, patterns": 0,  # ticket 05 landed
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


# --- Segment 1: Why this matters (ticket 02) --------------------------------

SEG1_TITLES = [
    "AI and the geography of job risk",
    "The risk is concentrated in knowledge work",
    "The augmentation–displacement pipeline",
    "The turn: skill, not job title",
]


def test_seg1_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG1_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_headline_figures_slide_shows_stats_and_credits_tufts(reopened):
    text = _slide_text(_slide_by_title(reopened, "AI and the geography of job risk"))
    assert "9.3" in text
    assert "757" in text
    assert "2.7" in text and "19.5" in text
    assert "Tufts Digital Planet" in text


def test_concentration_slide_shows_the_vulnerability_figures(reopened):
    text = _slide_text(
        _slide_by_title(reopened, "The risk is concentrated in knowledge work")
    )
    for figure in ("18%", "16%", "6%"):
        assert figure in text, f"{figure} missing"


def test_pipeline_slide_carries_the_verbatim_quote(reopened):
    text = _slide_text(
        _slide_by_title(reopened, "The augmentation–displacement pipeline")
    )
    assert "The more AI helps you do your job, the more expendable you become." in text


def test_turn_slide_lands_the_not_fear_skill_framing(reopened):
    text = _slide_text(_slide_by_title(reopened, "The turn: skill, not job title"))
    assert "not fear" in text.lower()
    assert "research management" in text.lower()


def test_every_seg1_slide_has_speaker_notes(reopened):
    for title in SEG1_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


# --- Segment 2A: How LLMs actually work (ticket 03) -------------------------

# One slide per concept, in teaching order, per lesson_1.md Segment 2 Part A.
SEG2A_TITLES = [
    "Powerful — but weird",
    "Tokens — the model doesn't see words",
    "The context window — a finite working memory",
    "System prompts — standing instructions",
    "Hallucination, sycophancy, and the cutoff",
    "Tools and agents — where this is heading",
    "Three principles to keep",
]


def _slide_by_title(reopened, title):
    for slide in reopened.slides:
        if title in _slide_text(slide):
            return slide
    raise AssertionError(f"no slide titled {title!r}")


def test_seg2a_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG2A_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_tokens_slide_carries_frabjous_example_and_demo_cue(reopened):
    slide = _slide_by_title(reopened, "Tokens — the model doesn't see words")
    text = _slide_text(slide)
    assert "O Frabjous Day!" in text
    assert "15 characters" in text
    assert "7 tokens" in text
    # The live-demo cue is visibly marked on the slide AND in the notes.
    assert "LIVE DEMO" in text
    assert "tiktokenizer.vercel.app" in text
    assert "tiktokenizer.vercel.app" in slide.notes_slide.notes_text_frame.text


def test_context_window_slide_states_the_two_practical_rules(reopened):
    text = _slide_text(
        _slide_by_title(reopened, "The context window — a finite working memory")
    )
    assert "lost in the middle" in text.lower()
    assert "start fresh" in text.lower()
    assert "more context is not better context" in text.lower()


def test_failure_modes_slide_states_the_verify_rule(reopened):
    text = _slide_text(
        _slide_by_title(reopened, "Hallucination, sycophancy, and the cutoff")
    )
    assert "verify anything you would sign your name to" in text.lower()


def test_principles_slide_carries_the_three_principles_verbatim(reopened):
    text = _slide_text(_slide_by_title(reopened, "Three principles to keep"))
    assert "Powerful but weird" in text
    assert "If it can be done deterministically, it should be" in text
    assert "Fewer, better tokens win" in text


def test_every_seg2a_slide_has_speaker_notes(reopened):
    for title in SEG2A_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


def test_seg2a_notes_carry_the_forward_references(reopened):
    all_notes = "\n".join(
        _slide_by_title(reopened, title).notes_slide.notes_text_frame.text
        for title in SEG2A_TITLES
    )
    assert "Lesson 3" in all_notes
    assert "Lesson 5" in all_notes


# --- Segment 2B: The 7 Levels map (ticket 04) --------------------------------

SEG2B_TITLES = [
    "The 7 Levels of AI — the course's map",
    "The destination: your KM System",
]

# Level names from the lesson_1.md Part B table — the framework itself.
SEVEN_LEVEL_NAMES = [
    "Question Asker",
    "Prompt Crafter",
    "Power User",
    "Tool Orchestrator",
    "Builder",
    "Systems Builder",
    "AI-Run Operation",
]


def test_seg2b_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG2B_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_map_slide_names_all_seven_levels_with_coverage(reopened):
    text = _slide_text(_slide_by_title(reopened, SEG2B_TITLES[0]))
    for name in SEVEN_LEVEL_NAMES:
        assert name in text, f"level name {name!r} missing"
    # Course-coverage mapping, per the lesson table.
    assert "You are (probably) here" in text  # the Level 1 marker
    assert "Today + Lesson 2" in text
    assert "Lessons 2–3" in text
    assert "Lessons 3–4" in text
    assert "Lesson 5" in text


def test_vibe_coding_appears_in_exactly_one_sentence_deck_wide(reopened):
    full_deck = "\n".join(_slide_text(s) for s in reopened.slides).lower()
    assert full_deck.count("vibe coding") == 1
    # And it lives on the 7 Levels map slide, positioned as out of scope.
    map_text = _slide_text(_slide_by_title(reopened, SEG2B_TITLES[0])).lower()
    assert "vibe coding" in map_text
    assert "not part of this course" in map_text


def test_km_teaser_slide_uses_context_terms_and_the_week8_line(reopened):
    text = _slide_text(_slide_by_title(reopened, SEG2B_TITLES[1]))
    for term in ("Wiki Sandbox", "Markdown Generator", "Personal Vault"):
        assert term in text, f"CONTEXT.md term {term!r} missing"
    assert "By Week 8, you will have built this" in text


def test_seg2b_notes_keep_the_pace_instruction(reopened):
    map_notes = _slide_by_title(
        reopened, SEG2B_TITLES[0]
    ).notes_slide.notes_text_frame.text
    assert "one sentence per level" in map_notes.lower()
    assert "no dwelling" in map_notes.lower()


def test_every_seg2b_slide_has_speaker_notes(reopened):
    for title in SEG2B_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


# --- Segment 3: Prompt engineering backdrop (ticket 05) ----------------------

SEG3_TITLES = [
    "The same question, three ways",
    "The ICC prompt",
    "Two shortcuts",
    "Meta-prompting — let the AI write the prompt",
    "Four prompt patterns",
    "Two rules while we demo",
]


def test_seg3_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG3_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_three_ways_slide_shows_the_escalation_and_cues_demo1(reopened):
    slide = _slide_by_title(reopened, "The same question, three ways")
    text = _slide_text(slide)
    # The three escalation stages from lesson_1.md Demo 1, verbatim prompts.
    assert "Horizon Europe budget" in text
    assert "Explain the budget structure of Horizon Europe collaborative projects" in text
    assert "ICC" in text
    # The retention point the side-by-side makes.
    assert "quality" in text.lower() and "input" in text.lower()
    # Demo-switch cue on the slide AND in the notes, with the ≈8 min share.
    assert "LIVE DEMO" in text
    notes = slide.notes_slide.notes_text_frame.text
    assert "gemini" in notes.lower()
    assert "8 min" in notes


def test_icc_slide_carries_the_demo_prompt_verbatim_in_three_blocks(reopened):
    text = _slide_text(_slide_by_title(reopened, "The ICC prompt"))
    # The three block labels are each visible.
    for label in ("Instruction", "Context", "Constraints"):
        assert label in text, f"block label {label!r} missing"
    # Spot-check each block's verbatim wording from lesson_1.md.
    assert (
        "Explain the eligible cost categories and overhead calculation "
        "for a Horizon Europe collaborative project" in text
    )
    assert "the 5 most common budgeting mistakes" in text
    assert "I am a research management administrator at a European university" in text
    assert "Cluster 4 project" in text and "EUR 3-4M" in text
    assert "who has never coordinated an EU project" in text
    assert "Maximum 600 words" in text
    assert "Use a table for cost categories" in text
    assert "Plain language, no unexplained acronyms" in text


def test_shortcuts_slide_carries_both_append_phrases_verbatim(reopened):
    slide = _slide_by_title(reopened, "Two shortcuts")
    text = _slide_text(slide)
    assert (
        "Before answering, ask me the questions you need to give "
        "the best possible answer." in text
    )
    assert (
        "Write the single prompt that would have gotten us to this result "
        "on the first try." in text
    )
    # Demo 2 starts here: cue on the slide, ≈17 min share in the notes.
    assert "LIVE DEMO" in text
    notes = slide.notes_slide.notes_text_frame.text
    assert "gemini" in notes.lower()
    assert "17 min" in notes


def test_meta_prompting_slide_carries_the_example_prompt_verbatim(reopened):
    text = _slide_text(
        _slide_by_title(reopened, "Meta-prompting — let the AI write the prompt")
    )
    assert (
        "I need an AI assistant to help me draft the impact section of an "
        "EU project's periodic report. Write the optimal prompt I should "
        "use, including all the context and constraints that would produce "
        "the best result." in text
    )
    assert "prompt engineer" in text


def test_patterns_slide_shows_all_four_with_their_examples(reopened):
    text = _slide_text(_slide_by_title(reopened, "Four prompt patterns"))
    for pattern in ("Persona", "Example-driven", "Step-by-step", "Critique-then-improve"):
        assert pattern in text, f"pattern {pattern!r} missing"
    # The research-management example of each pattern, per lesson_1.md.
    assert "Act as an experienced EU grants advisor" in text
    assert "partner-search announcement in our house style" in text
    assert "first list the eligibility criteria" in text
    assert "three biggest weaknesses against the evaluation criteria" in text


def test_rules_slide_states_both_safety_rules(reopened):
    text = _slide_text(_slide_by_title(reopened, "Two rules while we demo"))
    assert "nothing you couldn't publish" in text.lower()
    assert "verify" in text.lower() and "factual" in text.lower()


def test_every_seg3_slide_has_speaker_notes(reopened):
    for title in SEG3_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


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

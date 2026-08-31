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
    "Assignment briefing + close": 0,  # ticket 06 landed
    "Guided setup block": 0,  # ticket 07 landed
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
    # 1 title + 5 dividers + 26 content slides
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


# --- Segment 4: Assignment briefing + close (ticket 06) ----------------------

SEG4_TITLES = [
    "Your Anchor Project",
    "This week's assignment",
    "Effort and debrief",
    "Next week: the two-lane rule",
]


def test_seg4_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG4_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_anchor_project_slide_states_the_anonymize_or_fictional_rule(reopened):
    text = _slide_text(_slide_by_title(reopened, "Your Anchor Project"))
    assert "anonymize" in text.lower()
    assert "fictional" in text.lower()
    # Its role as the course-long thread, and the 5-sentence description.
    assert "entire knowledge system around it" in text
    assert "5 sentences" in text


def test_assignment_slide_enumerates_all_five_items(reopened):
    text = _slide_text(_slide_by_title(reopened, "This week's assignment"))
    # Item 1 — pick the Anchor Project, 5-sentence description.
    assert "Pick your Anchor Project" in text
    assert "5 sentences" in text
    # Item 2 — three ICC prompts, at least one pattern (all four named so
    # the screenshot is self-contained), what to save.
    assert "Three ICC prompts" in text
    assert "at least one" in text.lower() and "pattern" in text.lower()
    for pattern in ("persona", "example-driven", "step-by-step", "critique-then-improve"):
        assert pattern in text, f"pattern name {pattern!r} missing"
    assert "what you'd improve" in text
    # Item 3 — one ask-me-first.
    assert "ask-me-first" in text
    assert "interview you" in text
    # Item 4 — one meta-prompt.
    assert "meta-prompt" in text
    assert "optimal prompt" in text
    # Item 5 — bring everything to Lesson 2.
    assert "Lesson 2" in text


def test_effort_slide_states_expectation_and_debrief_format(reopened):
    text = _slide_text(_slide_by_title(reopened, "Effort and debrief"))
    assert "1–2 hours" in text
    assert "Lesson 2" in text and "debrief" in text.lower()
    assert "2–3 volunteers" in text


def test_close_slide_teases_the_two_lanes_without_explaining(reopened):
    text = _slide_text(_slide_by_title(reopened, "Next week: the two-lane rule"))
    # CONTEXT.md terms, with their tools, per the lesson plan's close.
    assert "Sensitive Lane" in text
    assert "Copilot" in text
    assert "Daily Driver" in text
    assert "Gemini" in text
    # A teaser, not a lesson: the explanation is deferred to Lesson 2.
    assert "Lesson 2" in text


def test_every_seg4_slide_has_speaker_notes(reopened):
    for title in SEG4_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


# --- Segment 5: Guided setup block (ticket 07) --------------------------------

SEG5_TITLES = [
    "Setup checklist",
    "Troubleshooting",
    "Not finished? Catch-up path",
]


def test_seg5_slides_present_in_order_and_not_placeholders(reopened):
    all_slides = [_slide_text(s) for s in reopened.slides]
    positions = []
    for title in SEG5_TITLES:
        matches = [i for i, t in enumerate(all_slides) if title in t]
        assert matches, f"no slide titled {title!r}"
        assert "[PLACEHOLDER]" not in all_slides[matches[0]]
        positions.append(matches[0])
    assert positions == sorted(positions)


def test_checklist_slide_lists_the_four_setup_items(reopened):
    text = _slide_text(_slide_by_title(reopened, "Setup checklist"))
    # Item 1 — Google account signed in, Gemini answers a test prompt.
    assert "gemini.google.com" in text
    assert "test prompt" in text.lower()
    # Item 2 — Copilot Chat with the institutional account.
    assert "Copilot Chat" in text
    assert "institutional" in text.lower()
    # Item 3 — Perplexity free account.
    assert "Perplexity" in text
    # Item 4 — first experimental prompt in each tool.
    assert "first" in text.lower() and "prompt in each" in text.lower()
    # The four items are numbered.
    for number in ("1", "2", "3", "4"):
        assert number in text


def test_checklist_slide_shows_the_chat_template(reopened):
    text = _slide_text(_slide_by_title(reopened, "Setup checklist"))
    assert "✅ 1–4" in text
    assert "meeting chat" in text.lower()


def test_checklist_is_large_type(reopened):
    """Readable while screen-shared for 30 minutes: every run in all four
    checklist item rows — number chips and item cards — is at least 14 pt."""
    from pptx.util import Pt

    item_markers = [
        "gemini.google.com", "Copilot Chat", "perplexity.ai", "prompt in each",
    ]
    slide = _slide_by_title(reopened, "Setup checklist")
    item_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and (
            s.text_frame.text.strip() in ("1", "2", "3", "4")  # number chips
            or any(m in s.text_frame.text for m in item_markers)  # item cards
        )
    ]
    assert len(item_shapes) == 8, [s.text_frame.text[:30] for s in item_shapes]
    for shape in item_shapes:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                assert run.font.size is not None, f"inherited size: {run.text!r}"
                assert run.font.size >= Pt(14), run.text


def test_troubleshooting_slide_lists_the_three_failure_points_with_fixes(reopened):
    text = _slide_text(_slide_by_title(reopened, "Troubleshooting"))
    # Personal vs. institutional Microsoft account mixed up.
    assert "personal" in text.lower() and "institutional" in text.lower()
    # Blocked Google account → separate browser profile.
    assert "browser profile" in text.lower()
    # Gemini region/consent prompts.
    assert "consent" in text.lower()


def test_catchup_slide_names_the_venue_and_the_not_installed_note(reopened):
    text = _slide_text(_slide_by_title(reopened, "Not finished? Catch-up path"))
    # Practice Week 1 drop-in plus the offered 10-minute slot.
    assert "Practice Week 1" in text
    assert "drop-in" in text.lower()
    assert "10-minute" in text
    # Obsidian and Perfect Wiki deliberately not installed today.
    assert "Obsidian" in text
    assert "Perfect Wiki" in text
    assert "not installed today" in text.lower()


def test_every_seg5_slide_has_speaker_notes(reopened):
    for title in SEG5_TITLES:
        slide = _slide_by_title(reopened, title)
        assert slide.has_notes_slide, f"{title!r} has no notes slide"
        assert slide.notes_slide.notes_text_frame.text.strip(), (
            f"{title!r} has empty speaker notes"
        )


def test_seg5_notes_carry_the_facilitation_guidance(reopened):
    """The lesson plan's Segment 5 facilitation notes live in the deck's
    speaker notes: chat-marking makes stragglers visible, and unfinished
    participants are flagged now, not discovered in Week 3."""
    checklist_notes = _slide_by_title(
        reopened, "Setup checklist"
    ).notes_slide.notes_text_frame.text
    assert "stragglers" in checklist_notes.lower()
    catchup_notes = _slide_by_title(
        reopened, "Not finished? Catch-up path"
    ).notes_slide.notes_text_frame.text
    assert "flag" in catchup_notes.lower()


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

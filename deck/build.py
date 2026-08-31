"""Entry point for the Lesson 1 deck: `python -m deck.build`.

Assembles the deck in session order: title slide, then for each segment a
section divider followed by that segment's slides. Each segment's slides
come from its own module in deck/segments/ — later tickets edit only
their segment module.
"""

from dataclasses import dataclass
from pathlib import Path

from deck import template
from deck.segments import (
    seg1_why_this_matters,
    seg2a_llm_fundamentals,
    seg2b_seven_levels,
    seg3_prompt_engineering,
    seg4_assignment_close,
    seg5_setup_block,
)

LESSON_TITLE = "Lesson 1 — Why AI, How LLMs Work, and the Map Ahead"
COURSE_NAME = "AI for Research Management"
SESSION_LINE = "Week 1 · Teaching Session · 90 minutes · Online via Teams"

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "dist" / "lesson_1_deck.pptx"


@dataclass
class Segment:
    number: int
    title: str
    duration: str
    mode: str
    # Modules whose add_slides(prs) fills this segment; tickets 02–07 each
    # own exactly one module in deck/segments/.
    modules: list


# Names, durations, and modes per the Timing Overview in lesson_1.md.
SEGMENTS = [
    Segment(1, "Opening: why this matters", "10 min", "Presentation",
            [seg1_why_this_matters]),
    Segment(2, "The map: LLM fundamentals + 7 Levels tour", "15 min", "Presentation",
            [seg2a_llm_fundamentals, seg2b_seven_levels]),
    Segment(3, "Prompt engineering: ICC, meta-prompting, patterns", "25 min",
            "Live facilitator demo", [seg3_prompt_engineering]),
    Segment(4, "Assignment briefing + close", "10 min", "Presentation + Q&A",
            [seg4_assignment_close]),
    Segment(5, "Guided setup block", "30 min", "Hands-on, facilitated",
            [seg5_setup_block]),
]


def build_presentation():
    """Build the full Lesson 1 deck and return it (unsaved)."""
    prs = template.new_presentation()
    template.add_title_slide(prs, LESSON_TITLE, COURSE_NAME, SESSION_LINE)
    for segment in SEGMENTS:
        template.add_section_divider(
            prs, segment.number, len(SEGMENTS),
            segment.title, segment.duration, segment.mode,
        )
        for module in segment.modules:
            module.add_slides(prs)
    return prs


def main():
    prs = build_presentation()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()

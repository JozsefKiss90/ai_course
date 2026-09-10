"""Entry point for the Lesson 2 deck: `python -m deck.lesson2.build`.

Assembles the deck in session order per the Timing Overview in
lesson_2.md: title slide, then per segment a section divider followed by
that segment's slides from its module in deck/lesson2/segments/. Tickets
04–08 of the Lesson 2 effort each own one segment module and replace its
placeholders; the divider is added here and colour-coded by lane.
"""

from dataclasses import dataclass
from pathlib import Path

from deck.lesson2 import template
from deck.lesson2.segments import (
    seg1_recap_debrief,
    seg2_sensitive_data_rule,
    seg3_copilot_in_practice,
    seg4_gemini_in_depth,
    seg5_assignment_close,
)

LESSON_TITLE = "Lesson 2 — The Two-Lane Tool Landscape"
COURSE_NAME = "AI for Research Management"
SESSION_LINE = "Week 2 · Teaching Session · 60 minutes · Online via Teams"

OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "dist" / "lesson_2_deck.pptx"


@dataclass
class Segment:
    number: int
    title: str
    duration: str
    mode: str
    # Modules whose add_slides(prs) fill this segment; tickets 04–08 each
    # own exactly one module in deck/lesson2/segments/.
    modules: list
    # The lane the whole segment lives in, or None for segments about both
    # lanes or neither; the divider takes the lane's colour.
    lane: template.Lane | None = None


# Names, durations, and modes per the Timing Overview in lesson_2.md.
SEGMENTS = [
    Segment(1, "Recap + assignment debrief", "15 min",
            "Participant demos, facilitated", [seg1_recap_debrief]),
    Segment(2, "The sensitive-data rule and data-protection principles", "10 min",
            "Presentation", [seg2_sensitive_data_rule]),
    Segment(3, "Copilot Chat (Basic) in practice", "12 min",
            "Live facilitator demo", [seg3_copilot_in_practice],
            lane=template.SENSITIVE_LANE),
    Segment(4, "Gemini in depth (+ NotebookLM preview)", "15 min",
            "Live facilitator demo", [seg4_gemini_in_depth],
            lane=template.DAILY_DRIVER),
    Segment(5, "Assignment briefing + close", "8 min",
            "Presentation + Q&A", [seg5_assignment_close]),
]


def build_presentation():
    """Build the full Lesson 2 deck and return it (unsaved)."""
    prs = template.new_presentation()
    template.add_title_slide(prs, LESSON_TITLE, COURSE_NAME, SESSION_LINE)
    for segment in SEGMENTS:
        template.add_section_divider(
            prs, segment.number, len(SEGMENTS),
            segment.title, segment.duration, segment.mode, lane=segment.lane,
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

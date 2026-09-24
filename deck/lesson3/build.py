"""Entry point for the Lesson 3 deck: `python -m deck.lesson3.build`.

Assembles the deck in session order per the Timing Overview in
lesson_3.md: title slide, then per segment a section divider followed by
that segment's slides from its module in deck/lesson3/segments/. Tickets
02–06 of the Lesson 3 effort each own one segment module; the divider is
added here and colour-coded by lane.
"""

from dataclasses import dataclass
from pathlib import Path

from deck.lesson3 import template
from deck.lesson3.segments import (
    seg1_recap_debrief,
    seg2_km_system_notebooklm,
    seg3_obsidian_vault,
    seg4_hands_on_block,
    seg5_assignment_close,
)

LESSON_TITLE = "Lesson 3 — Knowledge Capture: NotebookLM and the Personal Vault"
COURSE_NAME = "AI for Research Management"
SESSION_LINE = "Week 4 · Teaching Session · 90 minutes · Online via Teams"
# The Timing Overview's buffer row: minutes the dividers do not show.
BUFFER_MINUTES = 2

OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "dist" / "lesson_3_deck.pptx"


@dataclass
class Segment:
    number: int
    title: str
    duration: str
    mode: str
    modules: list
    # The lane (or the local non-lane) the whole segment lives in, or None
    # for segments about both or neither; the divider takes its colour.
    lane: template.Lane | None = None


# Names, durations, and modes per the Timing Overview in lesson_3.md.
SEGMENTS = [
    Segment(1, "Recap + assignment debrief", "15 min",
            "Participant demos, facilitated", [seg1_recap_debrief]),
    Segment(2, "The KM System redrawn + NotebookLM in depth", "20 min",
            "Presentation + live facilitator demo", [seg2_km_system_notebooklm],
            lane=template.DAILY_DRIVER),
    Segment(3, "Obsidian: the Personal Vault and its two plugins", "20 min",
            "Live facilitator demo", [seg3_obsidian_vault],
            lane=template.LOCAL),
    Segment(4, "Hands-on block: notebook + vault", "25 min",
            "Hands-on, facilitated", [seg4_hands_on_block]),
    Segment(5, "Assignment briefing + close", "8 min",
            "Presentation + Q&A", [seg5_assignment_close]),
]


def build_presentation():
    """Build the full Lesson 3 deck and return it (unsaved)."""
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

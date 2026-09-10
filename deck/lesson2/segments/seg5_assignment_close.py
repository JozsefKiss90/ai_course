"""Segment 5 — Assignment briefing + close (8 min, Presentation + Q&A).

Ticket 08 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/lesson2/build.py. The
assignment chains both lanes, so its slides stay neutral and mark the
lane per step with the lane colours where they name a tool.
"""

from deck.lesson2 import template

SEGMENT_LABEL = "Segment 5"
TICKET = "08"

# Slide inventory implied by lesson_2.md Segment 5: the assignment as it
# will appear, effort and where the work is shown, and the close.
PLANNED_SLIDES = [
    ("Assignment: your first workflow orchestration",
     "Chain all tools and capabilities so far into a multi-step workflow: "
     "blueprint (tool, input, output, guidelines, justification per step), "
     "an educational presentation as deliverable, routing per step; "
     "outcome Level 3 achieved, foundation for Level 4"),
    ("Effort and where the work is shown",
     "3–4 hours across two weeks, blueprint first; the tools to chain "
     "from; shown at Practice Week 1's drop-in (W3) and the Lesson 3 "
     "debrief (W4)"),
    ("Next: Practice Week 1 and Lesson 3",
     "Practice Week 1 (W3) optional drop-in; Lesson 3 (W4): NotebookLM, "
     "Perplexity, the Wiki Sandbox as the first piece of the KM System"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

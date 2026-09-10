"""Segment 1 — Recap + assignment debrief (15 min, Participant demos,
facilitated).

Ticket 04 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/lesson2/build.py. The segment
is about neither lane, so its slides carry no lane colour.
"""

from deck.lesson2 import template

SEGMENT_LABEL = "Segment 1"
TICKET = "04"

# Slide inventory implied by lesson_2.md Segment 1: the recap map, the
# debrief format, and the live capture slide.
PLANNED_SLIDES = [
    ("The recap map: Lesson 1 → Lesson 2",
     "Seven Lesson 1 concepts, each paired with the Lesson 2 topic it leads "
     "into — links by reference, no definitions"),
    ("Assignment debrief",
     "2–3 volunteers, 4 minutes each, screen-shared from Gemini; the four "
     "things to show in order (Anchor Project, ICC prompt, ask-me-first, "
     "meta-prompt)"),
    ("Common problems — captured live",
     "Empty capture slide the facilitator fills during the demos, one line "
     "per problem tagged by item; read back and routed to today's segments "
     "or Practice Week 1"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

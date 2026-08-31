"""Segment 2, Part B — The 7 Levels of AI, the course's map (~5 min).

Ticket 04 replaces these placeholders with the real slides. Edit only
this module; the segment 2 divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 2B"
TICKET = "04"

PLANNED_SLIDES = [
    ("The 7 Levels of AI — the course's map",
     "Visual progression (not a table): each level's name, research-management "
     "translation, and course coverage; 'You are (probably) here' on Level 1; "
     "one-sentence vibe-coding aside at Levels 4–5"),
    ("By Week 8, you will have built this",
     "KM System teaser diagram: Wiki Sandbox → Markdown Generator → Personal "
     "Vault (terms per CONTEXT.md)"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

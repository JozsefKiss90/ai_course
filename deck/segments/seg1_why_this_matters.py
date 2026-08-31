"""Segment 1 — Opening: why this matters (10 min, Presentation).

Ticket 02 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 1"
TICKET = "02"

PLANNED_SLIDES = [
    ("AI and the geography of job risk",
     "Tufts headline figures: 9.3M US jobs at risk (range 2.7–19.5M), "
     "$757B in annual income — numbers large, Tufts Digital Planet credited"),
    ("The risk is concentrated in knowledge work",
     "Information 18%, Finance/Insurance 16%, Professional Services 16% "
     "vs. 6% industry average; 'safe' analytical office jobs most exposed"),
    ("The augmentation–displacement pipeline",
     "Highest augmentation potential = highest displacement risk, with the "
     "verbatim quote: 'The more AI helps you do your job, the more expendable you become.'"),
    ("The turn: skill, not job title",
     "The course thesis — direct AI, verify it, build systems with it — "
     "framed for research management administrators (not fear, skill)"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

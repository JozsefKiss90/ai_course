"""Segment 4 — Assignment briefing + close (10 min, Presentation + Q&A).

Ticket 06 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 4"
TICKET = "06"

PLANNED_SLIDES = [
    ("Your Anchor Project",
     "Pick one real (anonymized) or fictional research project; the "
     "course-long thread; 5-sentence description"),
    ("This week's assignment",
     "All five items verbatim, screenshot-friendly: Anchor Project; three "
     "ICC prompts (≥1 pattern); one ask-me-first; one meta-prompt; bring to Lesson 2"),
    ("Effort and debrief",
     "~1–2 hours across the week; due at Lesson 2's debrief; 2–3 volunteers present"),
    ("Next week: the two-lane rule",
     "Teaser only — Sensitive Lane vs. Daily Driver, which AI may see "
     "institutional data and why (not taught yet)"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

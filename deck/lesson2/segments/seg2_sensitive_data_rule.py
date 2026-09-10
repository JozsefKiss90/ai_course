"""Segment 2 — The sensitive-data rule and data-protection principles
(10 min, Presentation).

Ticket 05 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/lesson2/build.py. The segment
is about both lanes: the routing slide colour-codes each lane with its
own colour, the rest stays neutral.
"""

from deck.lesson2 import template

SEGMENT_LABEL = "Segment 2"
TICKET = "05"

# Slide inventory implied by lesson_2.md Segment 2, one slide per
# sub-section.
PLANNED_SLIDES = [
    ("The two-lane rule: one routing question",
     "Does the task involve sensitive or IP-sensitive institutional data? "
     "Yes → Sensitive Lane, No → Daily Driver; three worked routing examples"),
    ("Data-protection principles",
     "Personal data, confidential institutional data, purpose and "
     "minimisation, human responsibility — the reasons behind the rule"),
    ("Institutional rules: the dean's directive as reference",
     "Rector's directive 4/2025. (X. 28.) as the umbrella rule; dean's "
     "directive 1/2026 (III.26.) with its six key points as one-liners, "
     "section references in the notes"),
    ("Anonymise before upload",
     "Documents with personal or sensitive content are anonymised before "
     "upload to any AI tool, in either lane; the Anchor Project rule was "
     "this rule in miniature"),
    ("What must never enter Gemini",
     "The seven-item list; anything on it goes to the Sensitive Lane, "
     "anonymised first if it is a document"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

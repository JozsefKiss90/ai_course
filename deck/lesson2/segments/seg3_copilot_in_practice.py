"""Segment 3 — Copilot Chat (Basic) in practice (12 min, Live facilitator
demo).

Ticket 06 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/lesson2/build.py. The whole
segment lives in the Sensitive Lane, so every slide carries the
Sensitive Lane colour (template.SENSITIVE_LANE) and the Daily Driver is
not mentioned.
"""

from deck.lesson2 import template

SEGMENT_LABEL = "Segment 3"
TICKET = "06"
LANE = template.SENSITIVE_LANE

# Slide inventory implied by lesson_2.md Segment 3: the four scenarios, the
# guardrails, then one slide per tool in the compiled tool list.
PLANNED_SLIDES = [
    ("Sensitive Lane scenarios",
     "Four scenarios with a one-line routing example and the ICC prompt "
     "shape each: internal administration (run live), unsubmitted "
     "proposals, personnel matters, strategic financial planning"),
    ("Limits and guardrails",
     "Enterprise behaviour, no SharePoint/OneDrive grounding, "
     "underperforms free-tier tools on general tasks, anonymise anyway"),
    ("Adobe Acrobat",
     "Free-to-use features only; premium features and the AI Assistant "
     "flagged as not available under the institutional licence"),
    ("Prompt Coach",
     "Run live on a participant's ICC prompt — Lesson 1's meta-prompting "
     "as a packaged agent"),
    ("Study and Learn",
     "Run live: concept explanation, flashcards, five-question quiz — "
     "learning outcomes for the assignment's educational presentation"),
    ("Canva via the Teams app",
     "Presentation prototyping: multi-page design previewed and commented "
     "on inside Teams"),
    ("genspark.ai",
     "The tool for the actual presentation; outside the tenant, so only "
     "anonymised, non-sensitive content goes in"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(
            prs, SEGMENT_LABEL, title, gist, TICKET, lane=LANE,
        )

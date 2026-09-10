"""Segment 4 — Gemini in depth (+ NotebookLM preview) (15 min, Live
facilitator demo).

Ticket 07 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/lesson2/build.py. The whole
segment lives in the Daily Driver, so every slide carries the Daily
Driver colour (template.DAILY_DRIVER) and the Sensitive Lane tool is not
mentioned.
"""

from deck.lesson2 import template

SEGMENT_LABEL = "Segment 4"
TICKET = "07"
LANE = template.DAILY_DRIVER

# Slide inventory implied by lesson_2.md Segment 4: an overview carrying
# the availability flag, one slide per capability that is demoed live or
# shown with a prepared result, one round-up for the capabilities only
# mentioned or shown as the paid-plan boundary, then the three NotebookLM
# scenarios.
PLANNED_SLIDES = [
    ("The free tier beyond the Sensitive Lane tool",
     "The capability list with live / prepared / slide-only marking and "
     "the 'free tier at the time of writing (September 2026)' flag"),
    ("File and image upload",
     "Live: anonymised call PDF plus a budget-table screenshot; "
     "eligibility checklist and a reading of the table"),
    ("Long context",
     "Live, short: one long guideline document summarised; the free "
     "tier's window limit and Lesson 1's curation rule"),
    ("Gems — persistent context",
     "Live, the Level 3 move: an 'Anchor Project assistant' Gem with "
     "standing instructions and reference files"),
    ("Canvas",
     "Live: outline of an educational presentation, iterated section by "
     "section, exported as a structured draft"),
    ("Deep Research",
     "Prepared result: a researched briefing with sources and the prompt "
     "that produced it; the monthly report cap"),
    ("Image generation and editing",
     "Prepared result: a diagram-style illustration for the presentation "
     "from a text description"),
    ("Workspace hooks, Guided Learning, Live and saved info",
     "Slide-only and mentioned capabilities: the paid-plan boundary, the "
     "tutoring mode, voice rehearsal, standing personal facts"),
    ("NotebookLM preview: a video becomes a textual source",
     "Scenario only — a public captioned video turned into a citable "
     "text source; no video link in the deck"),
    ("NotebookLM preview: several documents in one notebook",
     "Scenario only — call document, guidelines, FAQ and own notes in one "
     "source-grounded notebook; the answer to 'more context is not better "
     "context'"),
    ("NotebookLM preview: notebooks as project folders in Gemini",
     "Scenario only — a notebook linked into a chat as the Anchor "
     "Project's context; paid-plan steps marked after re-verification"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(
            prs, SEGMENT_LABEL, title, gist, TICKET, lane=LANE,
        )

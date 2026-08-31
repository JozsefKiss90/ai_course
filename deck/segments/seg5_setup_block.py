"""Segment 5 — Guided setup block (30 min, hands-on, facilitated).

Ticket 07 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 5"
TICKET = "07"

PLANNED_SLIDES = [
    ("Setup checklist",
     "Four numbered items in large type (Google/Gemini, Copilot Chat "
     "institutional, Perplexity, first prompt in each) + the '✅ 1–4' chat template"),
    ("Troubleshooting",
     "Personal vs. institutional Microsoft account; blocked Google account → "
     "separate browser profile; Gemini region/consent prompts"),
    ("Not finished? Catch-up path",
     "Practice Week 1 drop-in + offered 10-minute slot; note: Obsidian and "
     "Perfect Wiki deliberately not installed today"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

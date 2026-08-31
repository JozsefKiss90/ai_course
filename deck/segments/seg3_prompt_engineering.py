"""Segment 3 — Prompt engineering backdrop (25 min, live facilitator demo).

Ticket 05 replaces these placeholders with the real slides. Edit only
this module; the divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 3"
TICKET = "05"

PLANNED_SLIDES = [
    ("The same question, three ways",
     "Google-style → better → ICC side by side; quality scales with input "
     "quality; demo cue: switch to Gemini (Demo 1, ≈8 min)"),
    ("The ICC prompt",
     "The Horizon Europe demo prompt verbatim, Instruction/Context/"
     "Constraints blocks visually separated"),
    ("Two shortcuts",
     "Ask-me-first and reverse prompt, each with its exact append-phrase "
     "(participants copy these)"),
    ("Meta-prompting — let the AI write the prompt",
     "The periodic-report example prompt verbatim; run the generated prompt "
     "and compare; the model is your prompt engineer"),
    ("Four prompt patterns",
     "Persona, example-driven (few-shot), step-by-step, critique-then-improve "
     "— one line + one research-management example each"),
    ("Two rules while we demo",
     "Nothing you couldn't publish goes into Gemini; verify anything factual "
     "before using it"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

"""Segment 2, Part A — How LLMs actually work (~10 min, Presentation).

Ticket 03 replaces these placeholders with the real slides. Edit only
this module; the segment 2 divider is added by deck/build.py.
"""

from deck import template

SEGMENT_LABEL = "Segment 2A"
TICKET = "03"

PLANNED_SLIDES = [
    ("Powerful — but weird",
     "Framing slide: quirks are constraints to work within, not bugs to fear"),
    ("Tokens — the model doesn't see words",
     "Text chopped into numbered fragments; 'Frabjous Day' = 15 characters, "
     "7 tokens; live demo cue: tiktokenizer.vercel.app"),
    ("The context window — finite working memory",
     "Hard limit on paste + answer; lost-in-the-middle; two rules: start "
     "fresh per task, more context is not better context"),
    ("System prompts — standing instructions",
     "Message stack with an invisible instruction on top; system usually "
     "wins; Lesson 5 foreshadow (you write the system prompt); reasoning tokens"),
    ("Hallucination, sycophancy, and the cutoff",
     "Plausible text, not verified fact; agrees rather than pushes back; "
     "knowledge stops at the cutoff; rule: verify anything you would sign your name to"),
    ("Tools and agents — where this is heading",
     "One-minute foreshadow: tools let an LLM act; an agent is an LLM in a "
     "loop; Level 5–6 territory, built in Lesson 5"),
    ("Three principles to keep",
     "Verbatim: powerful but weird; if it can be done deterministically, it "
     "should be; fewer, better tokens win"),
]


def add_slides(prs):
    for title, gist in PLANNED_SLIDES:
        template.add_placeholder_slide(prs, SEGMENT_LABEL, title, gist, TICKET)

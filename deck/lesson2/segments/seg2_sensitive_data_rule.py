"""Segment 2 — The sensitive-data rule and data-protection principles
(10 min, Presentation).

Five slides, per lesson_2.md Segment 2 and in its order: the two-lane rule
as a routing decision; the data-protection principles as the reasons
behind it; the dean's directive and its rector-level parent as reference
points; the anonymise-before-upload rule; and the "what must never enter
Gemini" list that completes the interim rule Lesson 1 left open.

The segment is about both lanes, so its slides stay on the neutral
ink/slate accents. A lane colour appears only where a slide names that
lane's tool as where work goes: the routing slide's two columns and its
worked examples, the two lane chips on the anonymise slide, and the teal
exit band that routes the closing list to the Sensitive Lane. In
particular the "never enter Gemini" list is neutral, not violet — violet
means "Gemini is the right tool", which is the opposite of what the list
says. This narrows the "the rest stays neutral" instruction ticket 03 left
in this module: the rule that survives is the template's, that a lane
colour always says "this is about that tool".

The directive is cited, never reproduced. The slide carries six key points
as one-liners and the section references live in the speaker notes. So
does the tie-back to Lesson 1: this segment *completes* the interim
"nothing you couldn't publish" rule by saying what it meant, and the notes
say so in one sentence rather than teaching the old rule again.
"""

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck.lesson2 import template
from deck.lesson2.template import (
    DAILY_DRIVER, HEADING_FONT, INK, MUTED, PANEL, SENSITIVE_LANE, SLATE, TEXT,
    WHITE,
)

# The content area, in inches, as the two-column geometry every slide here
# is laid out on.
_LEFT = template.CONTENT_LEFT.inches
_WIDTH = template.CONTENT_WIDTH.inches
_COL_WIDTH = 5.95
_RIGHT_COL = _LEFT + _COL_WIDTH + 0.23


def _list_card(slide, left, top, width, height, fill, heading, items, size=13):
    """A card whose body is a short list rather than one line of prose."""
    card = template.add_card(
        slide, Inches(left), Inches(top), Inches(width), Inches(height),
        fill, heading, INK,
    )
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.16)
    for item in items:
        para = tf.add_paragraph()
        para.space_before = Pt(5)
        run = para.add_run()
        run.text = f"·  {item}"
        template.style(run, size=size, color=TEXT)
    return card


def _run_row(slide, top, height, edge, runs, size=13):
    """A full-width open card carrying one line built from several runs.
    The routed examples and the "never enter Gemini" list are the same
    block, read in opposite directions: plain text then a bold tail, or a
    bold lead then plain detail."""
    card = template.add_open_card(
        slide, Inches(_LEFT), Inches(top), Inches(_WIDTH), Inches(height),
        edge)
    para = card.text_frame.paragraphs[0]
    for text, color, bold in runs:
        run = para.add_run()
        run.text = text
        template.style(run, size=size, color=color, bold=bold)
    return card


def _line_card(slide, left, top, width, height, edge, heading, line,
               heading_size=13, line_size=11.5):
    """A reference row: a bold lead over one line of detail, on the
    template's open card. Top-anchored, so the leads line up across a row
    of cards whose detail lines wrap differently."""
    card = template.add_open_card(
        slide, Inches(left), Inches(top), Inches(width), Inches(height), edge)
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.14)
    run = tf.paragraphs[0].add_run()
    run.text = heading
    template.style(run, size=heading_size, color=INK, font=HEADING_FONT,
                   bold=True)
    para = tf.add_paragraph()
    para.space_before = Pt(2)
    run = para.add_run()
    run.text = line
    template.style(run, size=line_size, color=TEXT)
    return card


# --- The two-lane rule as a routing decision (≈3 min) ------------------------

ROUTING_QUESTION = (
    "Does the task involve sensitive or IP-sensitive institutional data?"
)

# The two columns of the plan's routing table. The "covers" lists are the
# plan's Covers column; the Sensitive Lane's four are the categories
# CONTEXT.md names, and tests/test_lesson2_deck.py checks them against
# CONTEXT.md itself.
_LANE_COLUMNS = [
    (SENSITIVE_LANE, "YES", "Copilot Chat (Basic), institutional account",
     ["Internal administration",
      "Unsubmitted grant proposals",
      "Personnel information",
      "Strategic financial planning"]),
    (DAILY_DRIVER, "NO", "Google Gemini (free tier)",
     ["Drafting",
      "Prompting exercises",
      "Long-document analysis",
      "General research management work"]),
]

# The plan's three worked examples: the task as it would be typed, the lane
# it routes to, and the one word that decides it.
_ROUTING_EXAMPLES = [
    ("“Summarise the partner feedback on our unsubmitted Cluster 4 proposal”",
     SENSITIVE_LANE, "unsubmitted proposal"),
    ("“Explain the eligible cost categories in Horizon Europe”",
     DAILY_DRIVER, "public knowledge"),
    ("“Draft a workload plan for the three administrators in my unit”",
     SENSITIVE_LANE, "personnel information"),
]

_HEADER_TOP = 2.18
_HEADER_HEIGHT = 0.74
_COVERS_TOP = 3.02
_COVERS_HEIGHT = 1.72
_EXAMPLE_TOP = 5.02
_EXAMPLE_PITCH = 0.53
_EXAMPLE_HEIGHT = 0.48


def _lane_column(slide, left, lane, answer, tool, covers):
    header = template.add_card(
        slide, Inches(left), Inches(_HEADER_TOP), Inches(_COL_WIDTH),
        Inches(_HEADER_HEIGHT), lane.color, f"{answer}  →  {lane.name}",
        WHITE, tool,
    )
    # add_card left-aligns a body under its centred heading; on a two-line
    # label block both lines want the same axis.
    header.text_frame.paragraphs[1].alignment = PP_ALIGN.CENTER

    _list_card(slide, left, _COVERS_TOP, _COL_WIDTH, _COVERS_HEIGHT,
               lane.tint, "What goes here", covers)


def _routing_example(slide, top, task, lane, reason):
    _run_row(slide, top, _EXAMPLE_HEIGHT, lane.color, [
        (task, TEXT, False),
        (f"   →  {lane.name} ({reason})", lane.color, True),
    ])


def _routing_slide(prs):
    slide = template.add_content_slide(
        prs, "The two-lane rule: one routing question")

    template.add_band(
        slide, Inches(1.32), Inches(0.78), ROUTING_QUESTION, size=20,
        sub="Answered before any prompt is written — per task, not per "
            "person and not per day",
    )

    for left, (lane, answer, tool, covers) in zip(
            (_LEFT, _RIGHT_COL), _LANE_COLUMNS):
        _lane_column(slide, left, lane, answer, tool, covers)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(4.78), template.CONTENT_WIDTH,
        "Three tasks, routed", size=11, color=MUTED,
    )

    top = _EXAMPLE_TOP
    for task, lane, reason in _ROUTING_EXAMPLES:
        _routing_example(slide, top, task, lane, reason)
        top += _EXAMPLE_PITCH

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.62), template.CONTENT_WIDTH,
        "The Sensitive Lane is the only place authorised for sensitive data — "
        "and never the place for general work the free tier does better",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~3 min, and it is the spine of the session — Segments 3, 4 and the "
        "assignment all assume it.\n\n"
        "Lead with the question, not with the tools: the lane is decided "
        "before a prompt is written, and it is decided per task. The same "
        "person routes a proposal one way in the morning and a public FAQ "
        "the other way in the afternoon.\n\n"
        "Lesson 1 left an interim rule for Gemini — nothing you couldn't "
        "publish. Say in one sentence that the two-lane rule is that rule "
        "completed, and move on; do not re-teach it, they applied it all "
        "week. The closing slide of this segment spells out what it "
        "meant.\n\n"
        "If a volunteer showed sensitive content in Gemini during the "
        "debrief, this is where it comes back: state it anonymised, without "
        "naming anyone, and route it aloud.\n\n"
        "The asymmetry is what people get wrong. The Sensitive Lane is the "
        "only authorised place for sensitive data — and it is not the better "
        "tool for everything else; sending general work there gives up the "
        "capabilities Segment 4 demos.\n\n"
        "Read the three examples at pace. Questions about a specific "
        "document go on the capture list, not into a discussion here."
    ))
    return slide


# --- Data-protection principles (≈2 min) -------------------------------------

# The plan's four principles, in the terms they take in research
# management: the reason behind the rule, not the legal text.
_PRINCIPLES = [
    ("Personal data",
     "Names, a role tied to a unit, contact details, evaluations, CVs. GDPR "
     "protects it, and putting it into an external AI tool is a data "
     "transfer — a transfer needs a legal basis."),
    ("Confidential institutional data",
     "Unsubmitted proposals, internal financial planning, unpublished "
     "results and raw data are institutional assets. A public AI platform "
     "may keep what you type and may train on it."),
    ("Purpose and minimisation",
     "Only the data the task needs, only for the task's purpose. “More "
     "context is not better context” and data minimisation point the same "
     "way."),
    ("Human responsibility",
     "The tool assists; the person signs. What leaves your desk carries "
     "your name on it, never the model's."),
]

_PRINCIPLE_TOP = 1.72
_PRINCIPLE_PITCH = 1.90
_PRINCIPLE_HEIGHT = 1.80


def _principles_slide(prs):
    slide = template.add_content_slide(
        prs, "Data-protection principles — why the rule exists")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        "Four reasons, in the form they take in research management",
        size=13, color=MUTED,
    )

    for index, (heading, body) in enumerate(_PRINCIPLES):
        left = _LEFT if index % 2 == 0 else _RIGHT_COL
        top = _PRINCIPLE_TOP + (index // 2) * _PRINCIPLE_PITCH
        card = template.add_card(
            slide, Inches(left), Inches(top), Inches(_COL_WIDTH),
            Inches(_PRINCIPLE_HEIGHT), PANEL, heading, INK, body,
        )
        card.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        card.text_frame.margin_top = Inches(0.22)

    template.add_band(
        slide, Inches(5.66), Inches(0.72),
        "The rule exists so the judgement is made once, at routing time — "
        "not again at every prompt",
        size=17,
    )

    template.set_notes(slide, (
        "~2 min. Four cards, one beat each — these are the reasons behind "
        "the rule, not a data-protection lecture. Nobody has to reason from "
        "first principles in the moment; that is the whole point of routing "
        "once, up front.\n\n"
        "Personal data: the trap is the combination. A name alone may be "
        "public, a name plus a unit plus a performance remark is not.\n\n"
        "Confidential institutional data: the risk is retention, not "
        "malice. A free-tier consumer platform may keep inputs and may train "
        "on them; that is enough to make an unsubmitted proposal the wrong "
        "thing to paste.\n\n"
        "Purpose and minimisation: tie it to Lesson 1 — the context-window "
        "point and data minimisation want the same behaviour, so this costs "
        "nothing in quality.\n\n"
        "Human responsibility is the one to close on: the tool assists, the "
        "person signs. It is also the first key point of the directive on "
        "the next slide, so hand over on it."
    ))
    return slide


# --- Institutional rules: the directive as reference (≈3 min) ----------------

# The two documents, named and cited, never reproduced.
_UMBRELLA = (
    "Umbrella — Rector's directive 4/2025. (X. 28.)",
    "On the use of artificial intelligence in education at ELTE",
)
_FACULTY = (
    "Faculty — Dean's directive 1/2026 (III.26.)",
    "ELTE Faculty of Informatics · Use of artificial intelligence in "
    "education, research and administration · supplements the rector's "
    "directive and the EU AI Act (Regulation (EU) 2024/1689)",
)

# The directive's six key points as one-liners. Where each lives in the
# document goes in the speaker notes, not on the slide.
_KEY_POINTS = [
    ("Human oversight and final responsibility",
     "AI assists; the person carries the responsibility for content, "
     "correctness and compliance."),
    ("Transparency and documentation of AI use",
     "Record where AI was used: which tool, when, for what, in which part "
     "of the work."),
    ("No sensitive data into external AI without permission",
     "Personal, sensitive or unpublished data, raw data and industrial "
     "results — explicit permission required."),
    ("AI in institutional administration is allowed",
     "Scheduling, reports, data analysis, documentation — inside the "
     "data-protection rules."),
    ("Critical checking of every output",
     "Every AI-generated material is checked before use; the author owns "
     "the content."),
    ("Consequences of breaches",
     "Disciplinary and ethical rules; embargoed or personal data can carry "
     "legal liability."),
]

_DOC_TOP = 1.30
_DOC_HEIGHT = 1.06
_POINT_TOP = 2.86
_POINT_PITCH = 0.98
_POINT_HEIGHT = 0.84


def _directive_slide(prs):
    slide = template.add_content_slide(
        prs, "Institutional rules: the dean's directive as reference")

    for left, (heading, body) in zip((_LEFT, _RIGHT_COL), (_UMBRELLA, _FACULTY)):
        _line_card(slide, left, _DOC_TOP, _COL_WIDTH, _DOC_HEIGHT, SLATE,
                   heading, body, heading_size=15)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(2.50), template.CONTENT_WIDTH,
        "Key points of the dean's directive — one line each, as reference "
        "points",
        size=13, color=MUTED,
    )

    for index, (heading, line) in enumerate(_KEY_POINTS):
        left = _LEFT if index % 2 == 0 else _RIGHT_COL
        top = _POINT_TOP + (index // 2) * _POINT_PITCH
        _line_card(slide, left, top, _COL_WIDTH, _POINT_HEIGHT, INK,
                   heading, line)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.88), template.CONTENT_WIDTH,
        "Cited, not reproduced — read the directive itself before you rely "
        "on it. Version 1.0, effective 26 March 2026, review expected "
        "1 July 2026.",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~3 min. Two documents, six pointers — this is a reference slide, "
        "not a reading. Say the titles, say the six points at pace, and tell "
        "the room the directive itself is the text; the slide only says "
        "where to look.\n\n"
        "Where each point lives, if anyone asks: human oversight and final "
        "responsibility — section 2; transparency and documentation — "
        "sections 2, 4, 5; no personal, sensitive or unpublished data into "
        "external AI tools without explicit permission — sections 2, 4; "
        "administration allowed within the data-protection and "
        "data-security rules — section 6; critical checking of every output "
        "— sections 4, 6; consequences of breaches — section 7.\n\n"
        "Point 4 is the one that reassures rather than restricts: "
        "administrative AI use is explicitly allowed, which is what this "
        "whole course is built on. Do not let the segment land as a list of "
        "prohibitions.\n\n"
        "Point 5 is the “verify before use” rule from the Lesson 1 demo, now "
        "with an institutional source behind it — name that link, do not "
        "re-teach it.\n\n"
        "Housekeeping before delivery: the directive is version 1.0 with a "
        "review expected 1 July 2026. Check for a newer version the week "
        "before the session and correct this slide if it moved."
    ))
    return slide


# --- The anonymise-before-upload rule (≈1 min) -------------------------------

_ANONYMISE_RULE = (
    "A document that contains personal or sensitive information is "
    "anonymised before it is uploaded to any AI tool"
)

# What anonymising actually removes, per the plan and the Lesson 1
# one-pager it points at.
_ANONYMISE_ITEMS = [
    "Names and any personal identifier — people, roles tied to a unit, "
    "contact details",
    "Unpublished amounts — budgets, salaries, internal financial figures",
    "Partner identities and consortium composition on anything unsubmitted",
    "Anything that still links the document back to a person or to an "
    "unsubmitted proposal",
]


def _anonymise_slide(prs):
    slide = template.add_content_slide(prs, "Anonymise before upload")

    template.add_band(
        slide, Inches(1.32), Inches(0.92), _ANONYMISE_RULE, size=19,
        sub="In either lane — the rule does not change with the tool",
    )

    for left, lane in zip((_LEFT, _RIGHT_COL), (SENSITIVE_LANE, DAILY_DRIVER)):
        template.add_card(
            slide, Inches(left), Inches(2.48), Inches(_COL_WIDTH),
            Inches(0.54), lane.color, f"{lane.name} — anonymise first", WHITE,
        )

    _list_card(slide, _LEFT, 3.22, _WIDTH, 1.70, PANEL,
               "What anonymising removes or replaces", _ANONYMISE_ITEMS)

    template.add_card(
        slide, Inches(_LEFT), Inches(5.02), Inches(_WIDTH), Inches(1.02),
        PANEL, "You did this in Lesson 1", INK,
        "The Anchor Project rule — real-but-anonymised, or fictional — was "
        "this rule in miniature. The anonymisation one-pager from Lesson 1's "
        "materials is the checklist.",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.20), template.CONTENT_WIDTH,
        "The check happens before the upload, not after the answer comes back",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~1 min. One institutional rule, stated once: a document carrying "
        "personal or sensitive information is anonymised before it goes into "
        "any AI tool — either lane, no exception for the institutional "
        "account.\n\n"
        "The lane chips are there because this is the point people expect an "
        "exception. The Sensitive Lane is authorised for sensitive data, and "
        "the anonymisation rule still applies to the files you upload into "
        "it.\n\n"
        "Tie it back in one sentence: they already did this when they wrote "
        "their Anchor Project description last week, and the anonymisation "
        "one-pager from Lesson 1's materials is the checklist. Do not walk "
        "the one-pager again — point at it.\n\n"
        "If someone asks about a document they cannot anonymise, the answer "
        "is on the next slide: it does not go into an AI tool at all."
    ))
    return slide


# --- What must never enter Gemini (≈1 min) -----------------------------------

# The plan's list, in the plan's order: the lead phrase in bold and the
# detail that follows it, or nothing where the lead says it all.
_NEVER_ITEMS = [
    ("Personal data of any kind",
     " — names with roles, contact details, evaluations, CVs, personnel "
     "matters"),
    ("Unsubmitted grant proposals", " — and their drafts, budgets, partner "
     "lists"),
    ("Internal financial planning", " — and strategic documents"),
    ("Unpublished research results", " — and raw data"),
    ("Results of industrial or contract research", ""),
    ("Any document under a confidentiality or data-processing agreement", ""),
    ("Anything not anonymised that would need to be", ""),
]

_NEVER_TOP = 1.72
_NEVER_PITCH = 0.53
_NEVER_HEIGHT = 0.46


def _never_slide(prs):
    slide = template.add_content_slide(prs, "What must never enter Gemini")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        "The rule Lesson 1 left open, now complete", size=13, color=MUTED,
    )

    top = _NEVER_TOP
    for lead, detail in _NEVER_ITEMS:
        runs = [(lead, INK, True)]
        if detail:
            runs.append((detail, TEXT, False))
        _run_row(slide, top, _NEVER_HEIGHT, SLATE, runs)
        top += _NEVER_PITCH

    template.add_band(
        slide, Inches(5.52), Inches(0.62),
        "Anything on this list  →  Sensitive Lane · Copilot Chat (Basic), "
        "anonymised first if it is a document",
        size=16, fill=SENSITIVE_LANE.color,
    )
    template.add_band(
        slide, Inches(6.24), Inches(0.55),
        "Fails the anonymisation test even there? Then it does not go into "
        "an AI tool at all",
        size=14, fill=SLATE,
    )

    template.set_notes(slide, (
        "~1 min. Read the list, do not discuss it. It is the closing slide "
        "of the segment and the one people photograph.\n\n"
        "This completes the interim rule from Lesson 1 — nothing you "
        "couldn't publish — by saying exactly what that meant. Say that in "
        "one sentence; the rule itself does not need re-teaching.\n\n"
        "Two exits, and both matter. Anything on the list goes to the "
        "Sensitive Lane, anonymised first if it is a document. And if it "
        "fails the anonymisation test even there, it does not go into an AI "
        "tool at all — say that line out loud, it is the floor under the "
        "whole rule.\n\n"
        "Then move straight into Segment 3: the Sensitive Lane has been "
        "named four times by now and nobody has seen it work yet."
    ))
    return slide


def add_slides(prs):
    _routing_slide(prs)
    _principles_slide(prs)
    _directive_slide(prs)
    _anonymise_slide(prs)
    _never_slide(prs)

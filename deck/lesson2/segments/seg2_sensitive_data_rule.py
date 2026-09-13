"""Segment 2 — The sensitive-data rule and data-protection principles
(10 min, Presentation).

Seven slides, per lesson_2.md Segment 2 and in its order: the two-lane
rule as a routing decision; the AI data safety and ethics framework — the
four pillars of trustworthy AI — with the institutional directives as its
reference strip; the four pillars of data safety; the four ethical AI
principles; the sources behind those three slides; the
anonymise-before-upload rule; and the "what must never enter Gemini" list
that completes the interim rule Lesson 1 left open.

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

The directives are cited, never reproduced: they ride as a two-card
reference strip under the pillars, carrying their titles and the
directive's own headline rules, while the section references live in the
speaker notes. So does the tie-back to Lesson 1: this segment *completes*
the interim "nothing you couldn't publish" rule by saying what it meant,
and the notes say so in one sentence rather than teaching the old rule
again.

The bracketed numbers on the framework, data-safety and ethics slides are
the sources slide that closes the block, and they match the plan's own
numbering — a claim on a slide can always be traced to the source it came
from.
"""

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from deck.lesson2 import template
from deck.lesson2.template import (
    DAILY_DRIVER, INK, MUTED, PANEL, SENSITIVE_LANE, SLATE, TEXT, WHITE,
)

# The content area, in inches, as the two-column geometry every slide here
# is laid out on.
_LEFT = template.CONTENT_LEFT.inches
_WIDTH = template.CONTENT_WIDTH.inches
_COL_WIDTH = 5.95
_RIGHT_COL = _LEFT + _COL_WIDTH + 0.23


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

    template.add_list_card(
        slide, Inches(left), Inches(_COVERS_TOP), Inches(_COL_WIDTH),
        Inches(_COVERS_HEIGHT), lane.tint, "What goes here", covers)


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


# --- AI data safety and ethical use: the framework (≈1.5 min) ----------------

_FRAMEWORK_LEAD = (
    "Protecting sensitive information, preventing algorithmic bias, and "
    "keeping human control over automated systems. As AI scales, balancing "
    "rapid innovation against robust risk management stops being an "
    "aspiration and becomes an operational requirement.  [1–3]"
)

_PILLARS_HEADING = "PILLARS OF TRUSTWORTHY AI"

# The four pillars of the plan's framework table, drawn as the one block
# the plan asks for: the heading band over four equal columns.
_PILLARS = [
    ("Data governance",
     "What may be collected, where it is allowed to travel, and who is "
     "accountable for it"),
    ("Algorithmic fairness",
     "Training and outputs actively filtered for systemic bias"),
    ("Transparency & explainability",
     "What data was used, and how a given automated decision was reached"),
    ("Human control",
     "Automated systems supplement human judgement; they never take over "
     "the responsibility"),
]

# The two institutional documents, named and cited, never reproduced. The
# faculty card carries the directive's own headline rules; where each of
# them lives in the document stays in the speaker notes.
_UMBRELLA = (
    "Umbrella — Rector's directive 4/2025. (X. 28.)",
    "On the use of artificial intelligence in education at ELTE",
)
_FACULTY = (
    "Faculty — Dean's directive 1/2026 (III.26.)",
    "ELTE Faculty of Informatics · supplements the rector's directive and "
    "the EU AI Act (Regulation (EU) 2024/1689) · human oversight and final "
    "responsibility, documented AI use, no sensitive data into external AI "
    "tools without explicit permission, critical checking of every output",
)

_PILLAR_HEADER_TOP = 1.88
_PILLAR_HEADER_HEIGHT = 0.46
_PILLAR_TOP = 2.42
_PILLAR_HEIGHT = 1.24
_PILLAR_WIDTH = 2.9275
_PILLAR_PITCH = 3.0675

_DOC_TOP = 4.18
_DOC_HEIGHT = 1.30


def _framework_slide(prs):
    slide = template.add_content_slide(
        prs, "AI data safety and ethical use — the framework")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.28), template.CONTENT_WIDTH,
        _FRAMEWORK_LEAD, size=13, color=TEXT,
    )

    template.add_band(
        slide, Inches(_PILLAR_HEADER_TOP), Inches(_PILLAR_HEADER_HEIGHT),
        _PILLARS_HEADING, size=15,
    )

    left = _LEFT
    for heading, gloss in _PILLARS:
        template.add_detail_card(
            slide, Inches(left), Inches(_PILLAR_TOP), Inches(_PILLAR_WIDTH),
            Inches(_PILLAR_HEIGHT), INK, heading, [gloss], heading_size=13,
            line_size=11)
        left += _PILLAR_PITCH

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(3.86), template.CONTENT_WIDTH,
        "Where this is written down for us", size=11, color=MUTED,
    )

    for left, (heading, body) in zip((_LEFT, _RIGHT_COL), (_UMBRELLA, _FACULTY)):
        template.add_detail_card(
            slide, Inches(left), Inches(_DOC_TOP), Inches(_COL_WIDTH),
            Inches(_DOC_HEIGHT), SLATE, heading, [body], heading_size=14,
            line_size=11)

    template.add_band(
        slide, Inches(5.74), Inches(0.62),
        "The rule exists so the judgement is made once, at routing time — "
        "not again at every prompt",
        size=16,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.46), template.CONTENT_WIDTH,
        "Cited, not reproduced — read the directives themselves before you "
        "rely on them. Dean's directive version 1.0, effective 26 March "
        "2026, review expected 1 July 2026.",
        size=10.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~1.5 min. This is the reason behind the rule, not a "
        "data-protection lecture. Say the lead sentence once, then walk the "
        "four pillars left to right, a beat each — data governance, "
        "algorithmic fairness, transparency and explainability, human "
        "control. Nobody has to reason from first principles in the moment; "
        "that is the whole point of routing once, up front.\n\n"
        "The reference strip is the institutional anchor: the rector's "
        "directive 4/2025. (X. 28.) is the umbrella, the dean's directive "
        "1/2026 (III.26.) is the faculty supplement, and the four rules on "
        "the faculty card are the directive's own headline points. Say the "
        "titles; do not read the document.\n\n"
        "Where each point lives, if anyone asks: human oversight and final "
        "responsibility — section 2; transparency and documentation — "
        "sections 2, 4, 5; no personal, sensitive or unpublished data into "
        "external AI tools without explicit permission — sections 2, 4; "
        "administration allowed within the data-protection and "
        "data-security rules — section 6; critical checking of every output "
        "— sections 4, 6; consequences of breaches — section 7.\n\n"
        "The point that reassures rather than restricts: administrative AI "
        "use is explicitly allowed by section 6, which is what this whole "
        "course is built on. Do not let the segment land as a list of "
        "prohibitions.\n\n"
        "Critical checking of every output is the “verify before use” rule "
        "from the Lesson 1 demo, now with an institutional source behind it "
        "— name that link, do not re-teach it.\n\n"
        "Housekeeping before delivery: the directive is version 1.0 with a "
        "review expected 1 July 2026. Check for a newer version the week "
        "before the session and correct this slide if it moved."
    ))
    return slide


# --- Key pillars of data safety (≈1.5 min) -----------------------------------

# The plan's four practices. The bracketed numbers are the sources slide
# that closes this block, and they match the plan's own numbering.
_DATA_SAFETY = [
    ("Data minimisation",
     "Collect and process only the information a clear, designated purpose "
     "actually needs. “More context is not better context” and data "
     "minimisation point the same way.  [4]"),
    ("Privacy by design",
     "Data protection built into the design of a system from the start, "
     "rather than bolted on afterwards.  [4]"),
    ("Anonymisation",
     "Masking or removing personally identifiable information (PII) "
     "safeguards people against breaches and unapproved tracking.  "
     "[2, 4, 5]"),
    ("Regulatory compliance",
     "The GDPR and the EU AI Act in Europe, equivalents such as the CCPA "
     "elsewhere — what you deploy has to align with them.  [1]"),
]

# --- Ethical AI principles (≈1.5 min) ----------------------------------------

_ETHICAL_PRINCIPLES = [
    ("Fairness and non-discrimination",
     "Training and prompting actively filter out systemic bias, or the "
     "model replicates historical inequalities as if they were findings.  "
     "[6, 7]"),
    ("Transparency",
     "Anyone affected by an automated outcome is owed clear insight into "
     "what data was tracked and how the decision was reached.  [7, 8]"),
    ("Accountability",
     "Responsibility for a system's behaviour, its audits and its "
     "performance tracking is assigned before the tool is launched.  "
     "[7, 9]"),
    ("Human oversight",
     "The model supplements human judgement rather than displacing human "
     "responsibility. The tool assists; the person signs.  [1, 9]"),
]

_QUAD_TOP = 1.72
_QUAD_PITCH = 1.90
_QUAD_HEIGHT = 1.80


def _quad_slide(prs, title, caption, cards, band, band_size=17):
    """Four cards in a 2×2 grid under a caption, closed by a band — the
    shape both the data-safety slide and the ethics slide take."""
    slide = template.add_content_slide(prs, title)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        caption, size=13, color=MUTED,
    )

    for index, (heading, body) in enumerate(cards):
        left = _LEFT if index % 2 == 0 else _RIGHT_COL
        top = _QUAD_TOP + (index // 2) * _QUAD_PITCH
        card = template.add_card(
            slide, Inches(left), Inches(top), Inches(_COL_WIDTH),
            Inches(_QUAD_HEIGHT), PANEL, heading, INK, body,
        )
        card.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        card.text_frame.margin_top = Inches(0.22)

    template.add_band(slide, Inches(5.66), Inches(0.72), band, size=band_size)
    return slide


def _data_safety_slide(prs):
    slide = _quad_slide(
        prs, "Key pillars of data safety",
        "The four practices the pillars come down to in daily work",
        _DATA_SAFETY,
        "The same discipline Lesson 1 already asked for — minimise the data, "
        "curate the context; none of this costs you answer quality",
    )
    template.set_notes(slide, (
        "~1.5 min. Four cards, one beat each.\n\n"
        "Data minimisation is the one to tie back: the context-window point "
        "from Lesson 1 and data minimisation ask for exactly the same "
        "discipline, so nobody is being asked to trade quality for "
        "compliance.\n\n"
        "Privacy by design is why the routing question comes before the "
        "prompt rather than after the answer — the protection is in the "
        "design of the workflow, not in a review at the end.\n\n"
        "Anonymisation gets one sentence here; the rule itself is two "
        "slides away and that is where it is stated. Do not pre-empt it.\n\n"
        "Regulatory compliance: name the GDPR and the EU AI Act and move "
        "on. The bracketed numbers point at the sources slide that closes "
        "this block — say so once, so nobody copies a claim without its "
        "source."
    ))
    return slide


def _ethics_slide(prs):
    slide = _quad_slide(
        prs, "Ethical AI principles",
        "Four principles — and the one the institution puts first",
        _ETHICAL_PRINCIPLES,
        "Critical checking of every output before use — the directive's "
        "rule, and the floor under the other three",
    )
    template.set_notes(slide, (
        "~1.5 min. Read the four, then close on human oversight — it is the "
        "one the dean's directive puts first and the one this course keeps "
        "returning to.\n\n"
        "Fairness: the risk in research management is not an exotic one. A "
        "model trained on past funding decisions reproduces the pattern of "
        "past funding decisions; that is a finding about history, not about "
        "the proposal in front of you.\n\n"
        "Transparency and accountability are what the directive's "
        "documentation rule is for — recording which tool was used, when "
        "and for what is how an automated step stays answerable afterwards. "
        "The assignment in Segment 5 asks for exactly that log.\n\n"
        "“The tool assists; the person signs” is the sentence to leave the "
        "room with. Everything from here — both lanes, every capability in "
        "Segments 3 and 4 — sits under it."
    ))
    return slide


# --- Sources (≈30 s) ---------------------------------------------------------

# The reading list behind the previous three slides, numbered as the
# bracketed markers on them. The link text is the domain; the full address
# rides on the run as a hyperlink, so the list stays readable at 10.5pt.
# Two video sources from the same research are absent by the deck-wide
# rule against YouTube links; the plan's Sources subsection says so.
_SOURCES = [
    ("European Commission — Ethics guidelines for trustworthy AI",
     "digital-strategy.ec.europa.eu",
     "https://digital-strategy.ec.europa.eu/en/library/"
     "ethics-guidelines-trustworthy-ai"),
    ("Harvard DCE — Ethics in AI: why it matters",
     "professional.dce.harvard.edu",
     "https://professional.dce.harvard.edu/blog/ethics-in-ai-why-it-matters/"),
    ("Salesforce Trailhead — Data ethics and privacy in practice",
     "trailhead.salesforce.com",
     "https://trailhead.salesforce.com/content/learn/modules/"
     "data-fundamentals-for-ai/"
     "know-data-ethics-privacy-and-practical-implementation"),
    ("TrustCloud — Ethical AI and data privacy practices",
     "trustcloud.ai",
     "https://www.trustcloud.ai/ai/"
     "boost-trust-with-powerful-ethical-ai-and-data-privacy-practices/"),
    ("Alation — Data ethics in AI: 6 key principles",
     "alation.com",
     "https://www.alation.com/blog/"
     "data-ethics-in-ai-6-key-principles-for-responsible-machine-learning/"),
    ("SDAIA — AI principles",
     "sdaia.gov.sa",
     "https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf"),
    ("Transcend — AI ethics",
     "transcend.io",
     "https://transcend.io/blog/ai-ethics"),
    ("ADP — AI and data ethics: five principles to consider",
     "adp.ca",
     "https://www.adp.ca/en/resources/articles-and-insights/articles/a/"
     "ai-and-data-ethics-5-principles-to-consider.aspx"),
    ("UNESCO — Recommendation on the ethics of artificial intelligence",
     "unesco.org",
     "https://www.unesco.org/en/artificial-intelligence/"
     "recommendation-ethics"),
]

_SOURCE_TOP = 1.76
_SOURCE_PITCH = 0.70
_SOURCE_HEIGHT = 0.62
_SOURCE_SPLIT = 5  # rows in the left column; the rest go to the right


def _source_row(slide, left, top, number, name, domain, url):
    card = template.add_open_card(
        slide, Inches(left), Inches(top), Inches(_COL_WIDTH),
        Inches(_SOURCE_HEIGHT), SLATE)
    para = card.text_frame.paragraphs[0]
    run = para.add_run()
    run.text = f"[{number}]  "
    template.style(run, size=10.5, color=INK, bold=True)
    run = para.add_run()
    run.text = f"{name}  ·  "
    template.style(run, size=10.5, color=TEXT)
    run = para.add_run()
    run.text = domain
    template.style(run, size=10.5, color=SLATE, bold=True)
    run.hyperlink.address = url
    return card


def _sources_slide(prs):
    slide = template.add_content_slide(prs, "Sources")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        "The reading list behind the previous three slides — the bracketed "
        "numbers on those slides point here. Photograph it; it is not read "
        "out.",
        size=13, color=MUTED,
    )

    for index, (name, domain, url) in enumerate(_SOURCES):
        column, row = divmod(index, _SOURCE_SPLIT)
        _source_row(
            slide, _LEFT if column == 0 else _RIGHT_COL,
            _SOURCE_TOP + row * _SOURCE_PITCH,
            index + 1, name, domain, url,
        )

    template.add_band(
        slide, Inches(5.50), Inches(0.62),
        "Institutional sources — Rector's directive 4/2025. (X. 28.) and "
        "Dean's directive 1/2026 (III.26.)",
        size=15, fill=SLATE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.26), template.CONTENT_WIDTH,
        "Every link is live on the slide — the deck goes into the Teams "
        "channel after the session, so the list travels with it.",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~30 sec, and it is a reference slide — do not read it out. Say "
        "that the numbers in brackets on the previous three slides point "
        "here, that every link is live in the deck, and that the deck goes "
        "into the Teams channel after the session.\n\n"
        "Two of the eleven are videos rather than written sources and are "
        "marked as such, so nobody cites a video as a standard. The two "
        "institutional documents sit on the band at the bottom, because "
        "they are the ones that actually bind us — the eleven explain why "
        "the rules read the way they do.\n\n"
        "If the segment is running behind, this is the slide to skip on the "
        "day: it loses nothing, because it travels with the deck."
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

    template.add_list_card(
        slide, Inches(_LEFT), Inches(3.22), Inches(_WIDTH), Inches(1.70),
        PANEL, "What anonymising removes or replaces", _ANONYMISE_ITEMS)

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
    _framework_slide(prs)
    _data_safety_slide(prs)
    _ethics_slide(prs)
    _sources_slide(prs)
    _anonymise_slide(prs)
    _never_slide(prs)

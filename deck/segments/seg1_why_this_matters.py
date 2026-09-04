"""Segment 1 — Opening: why this matters (10 min, Presentation).

Four slides per lesson_1.md Segment 1: the Tufts Digital Planet headline
figures, the concentration of risk in knowledge work, the augmentation–
displacement pipeline with its verbatim quote, and the turn — the course
thesis, framed for research management administrators. Not fear — skill.
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    ACCENT, AMBER, HEADING_FONT, HIGHLIGHT, MUTED, PALE, PALE_WARM, PANEL_EDGE,
    PRIMARY, SKY, SLATE, TEXT, WHITE,
)

TUFTS_CREDIT = (
    "Source: Tufts Digital Planet — AI and the Emerging Geography of "
    "American Job Risk"
)


def _stat_tile(slide, left, width, number, caption, detail=None):
    """Big-number tile: the figure dominates, the caption explains it."""
    tile = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, Inches(1.95), width, Inches(1.62)
    )
    template.panel(tile)
    template.add_bar(slide, left, Inches(1.95), width, Inches(0.09), AMBER)
    tf = tile.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = number
    template.style(run, size=38, color=AMBER, font=HEADING_FONT, bold=True)
    para = tf.add_paragraph()
    para.alignment = PP_ALIGN.CENTER
    para.space_before = Pt(6)
    run = para.add_run()
    run.text = caption
    template.style(run, size=14, color=WHITE)
    if detail:
        para = tf.add_paragraph()
        para.alignment = PP_ALIGN.CENTER
        para.space_before = Pt(4)
        run = para.add_run()
        run.text = detail
        template.style(run, size=12, color=SKY, italic=True)
    return tile


# The two ends of the Tufts "AI Job Risk Index" occupation ranking: the
# three most vulnerable of 784 occupations analyzed, and the three least.
# Percentages are predicted job loss; the whole tail of the ranking sits
# at 0%, so the bottom three are the ranking's own final three.
_MOST_VULNERABLE = [
    (1, "Writers and Authors", "57%"),
    (2, "Computer Programmers", "55%"),
    (3, "Web and Digital Interface Designers", "55%"),
]

_LEAST_VULNERABLE = [
    (782, "Foundry Mold and Coremakers", "0%"),
    (783, "Cleaners of Vehicles and Equipment", "0%"),
    (784, "Dishwashers", "0%"),
]


def _rank_panel(slide, left, width, heading, rows, edge, value_color):
    """Ranked-occupation card: heading, rule, then rank / name / percent."""
    top = 3.75
    height = 2.45
    card = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, Inches(top), width, Inches(height)
    )
    template.panel(card)
    template.add_bar(slide, left, Inches(top), Inches(0.09), Inches(height), edge)

    inner = Inches(left.inches + 0.34)
    template.add_label(slide, inner, Inches(top + 0.16), width, heading,
                       size=15, color=WHITE)
    template.add_bar(slide, inner, Inches(top + 0.62),
                     Inches(width.inches - 0.68), Pt(1), PANEL_EDGE)

    name_left = Inches(left.inches + 0.86)
    name_width = Inches(width.inches - 0.86 - 1.25)
    value_left = Inches(left.inches + width.inches - 1.3)
    row_top = top + 0.76
    for rank, name, value in rows:
        template.add_label(slide, inner, Inches(row_top), Inches(0.5),
                           str(rank), size=13, color=MUTED)
        template.add_label(slide, name_left, Inches(row_top - 0.02), name_width,
                           name, size=14, color=TEXT)
        template.add_label(slide, value_left, Inches(row_top - 0.03),
                           Inches(0.95), value, size=17, color=value_color,
                           align=PP_ALIGN.RIGHT)
        row_top += 0.52
    return card


def _headline_figures_slide(prs):
    slide = template.add_content_slide(
        prs,
        "AI and the geography of job risk",
        ["What new research says about where AI lands in the labor market:"],
    )
    _stat_tile(
        slide, template.CONTENT_LEFT, Inches(5.96),
        "9.3 million",
        "US jobs at risk under the median AI-adoption scenario",
        "range across scenarios: 2.7–19.5 million",
    )
    _stat_tile(
        slide, Inches(6.77), Inches(5.96),
        "$757 billion",
        "in annual income attached to those jobs",
    )
    _rank_panel(
        slide, template.CONTENT_LEFT, Inches(5.96),
        "Most vulnerable occupations", _MOST_VULNERABLE,
        HIGHLIGHT, AMBER,
    )
    _rank_panel(
        slide, Inches(6.77), Inches(5.96),
        "Least vulnerable occupations", _LEAST_VULNERABLE,
        ACCENT, SKY,
    )
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.35), template.CONTENT_WIDTH,
        TUFTS_CREDIT + " · AI Job Risk Index, share of jobs lost, "
        "ranked across 784 occupations",
        size=11,
    )
    template.set_notes(slide, (
        "~2.5 min. Open the session here — but set the tone in the first "
        "sentence: the point of these numbers is not fear. The Tufts Digital "
        "Planet research maps where AI lands in the US labor market, and it "
        "lands exactly on administrative and knowledge work — our kind of "
        "work. 9.3 million US jobs at risk under the median AI-adoption "
        "scenario (the honest range across scenarios is 2.7 to 19.5 "
        "million), representing 757 billion dollars in annual income.\n\n"
        "Then drop to the two panels — this is the part that lands. The "
        "three most vulnerable occupations of the 784 analyzed are Writers "
        "and Authors at 57%, Computer Programmers at 55%, and Web and "
        "Digital Interface Designers at 55%. Writing, coding, design: all "
        "desk work, all of it work we would have called creative or highly "
        "skilled.\n\n"
        "The other end of the ranking is the punchline. Foundry mould "
        "makers, vehicle cleaners, dishwashers — 0% predicted job loss. "
        "The whole tail sits at zero: 311 of the 784 occupations come out "
        "at 0%. If the work is physical, this wave does not touch it. If "
        "the work arrives as text on a screen, it does.\n\n"
        "Do not let anyone read this as 'programmers are doomed'. Read it "
        "as: exposure follows the task, not the job title. Hold that "
        "thought — it is the argument of the next three slides."
    ))


# Vulnerability by sector, per the Tufts research: three knowledge-work
# sectors against the all-industry average.
_VULNERABILITY_ROWS = [
    ("Information", 18, ACCENT),
    ("Finance / Insurance", 16, ACCENT),
    ("Professional Services", 16, ACCENT),
    ("All-industry average", 6, SLATE),
]

_BAR_SCALE = 0.42  # inches per percentage point


def _concentration_slide(prs):
    slide = template.add_content_slide(
        prs,
        "The risk is concentrated in knowledge work",
        ["Share of jobs vulnerable to AI, by sector:"],
    )
    top = 2.15
    for sector, pct, fill in _VULNERABILITY_ROWS:
        template.add_label(slide, template.CONTENT_LEFT, Inches(top + 0.06),
                           Inches(3.0), sector, size=14, color=TEXT)
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(3.7), Inches(top),
            Inches(pct * _BAR_SCALE), Inches(0.5),
        )
        template.solid(bar, fill)
        template.add_label(slide, Inches(3.7 + pct * _BAR_SCALE + 0.15),
                           Inches(top + 0.04), Inches(1.0), f"{pct}%",
                           size=16, color=AMBER)
        top += 0.75
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.35), template.CONTENT_WIDTH,
        "High-skill, analytical, office-based occupations face the steepest "
        "exposure. The jobs historically “safe” from automation are now the "
        "most exposed.",
        size=16, color=TEXT,
    )
    template.add_label(slide, template.CONTENT_LEFT, Inches(6.35),
                       template.CONTENT_WIDTH, TUFTS_CREDIT, size=11)
    template.set_notes(slide, (
        "~2 min. Walk the bars top-down: Information 18%, Finance and "
        "Insurance 16%, Professional Services 16% — against a 6% "
        "all-industry average. Three times the average, and all three are "
        "knowledge-work sectors.\n\n"
        "Land the reversal: for decades, automation threatened manual and "
        "routine work while analytical office jobs were the 'safe' ones. "
        "This research says the opposite is now true — high-skill, "
        "analytical, office-based occupations face the steepest exposure. "
        "Research management sits in exactly this category; say so, but "
        "save the full framing for the thesis slide in a minute."
    ))


def _pipeline_slide(prs):
    slide = template.add_content_slide(
        prs,
        "The augmentation–displacement pipeline",
        ["The research's counterintuitive core finding: help and risk are "
         "the same list."],
    )
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(2.3), Inches(5.5), Inches(1.7),
        PALE, "Highest augmentation potential", PRIMARY,
        "The occupations where AI helps the most with everyday tasks…",
    )
    template.add_label(slide, Inches(6.2), Inches(2.85), Inches(0.8), "→",
                       size=32, color=AMBER, align=PP_ALIGN.CENTER)
    template.add_card(
        slide, Inches(7.23), Inches(2.3), Inches(5.5), Inches(1.7),
        PALE_WARM, "Highest displacement risk", PRIMARY,
        "…are the same occupations AI can most readily replace.",
    )
    template.add_band(
        slide, Inches(4.5), Inches(1.55),
        "“The more AI helps you do your job, the more expendable you become.”",
        size=22, sub="— the researchers' own framing",
    )
    template.set_notes(slide, (
        "~2 min. This is the slide the whole opening builds to. The naive "
        "expectation is that AI-helps and AI-replaces are different lists "
        "of jobs. The research found they are the same list: the "
        "occupations with the highest augmentation potential also show the "
        "highest displacement risk.\n\n"
        "Read the quote out loud, then pause. Then plant the question the "
        "next slide answers: if being helped by AI makes you expendable, "
        "what makes the difference between at-risk and empowered? Hold "
        "there — that turn is the whole point of the course."
    ))


def _turn_slide(prs):
    slide = template.add_content_slide(
        prs,
        "The turn: skill, not job title",
        ["The point is not fear. The same research implies the way through — "
         "what matters is how you work with AI, not what your job is called."],
    )
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(2.5), Inches(5.96), Inches(1.9),
        PALE_WARM, "Displacement attaches to shallow use", PRIMARY,
        "Letting AI do the job for you — unchecked, unexamined, at a "
        "shallow level.",
    )
    template.add_card(
        slide, Inches(6.77), Inches(2.5), Inches(5.96), Inches(1.9),
        PALE, "Value attaches to moving up the skill curve", PRIMARY,
        "Directing AI, verifying it, and building systems with it. This "
        "course exists to move you up that curve.",
    )
    template.add_band(
        slide, Inches(4.85), Inches(1.35),
        "Research management is administrative, analytical knowledge work — "
        "squarely in the exposed zone.\nThat is precisely why learning this "
        "well matters for you, now.",
        size=18,
    )
    template.set_notes(slide, (
        "~3 min, including a beat for questions. Answer the question the "
        "quote raised: displacement risk attaches to people who let AI do "
        "their job for them at a shallow level. People who move up the "
        "skill curve — who direct AI, verify it, and build systems with it "
        "— become more valuable, not less. That is the course thesis, and "
        "the reason this course exists.\n\n"
        "Then make it personal for this audience: research management is "
        "administrative, analytical knowledge work — squarely in the "
        "exposed zone, which is precisely why learning this well matters "
        "now. Keep the register matter-of-fact, not alarmist: the numbers "
        "were the diagnosis, the course is the response.\n\n"
        "Bridge to Segment 2: 'so let's start by understanding the tool "
        "itself — what these models actually are, and why they behave so "
        "strangely.'"
    ))


def add_slides(prs):
    _headline_figures_slide(prs)
    _concentration_slide(prs)
    _pipeline_slide(prs)
    _turn_slide(prs)

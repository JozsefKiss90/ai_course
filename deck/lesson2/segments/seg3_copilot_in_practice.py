"""Segment 3 — Copilot Chat (Basic) in practice (12 min, Live facilitator
demo).

Seven slides, per lesson_2.md Segment 3 and in its order: the four
Sensitive Lane scenarios, the limits and guardrails, then one slide per
tool in `.scratch/copilot_free_to_use_tools.md` — Adobe Acrobat, Prompt
Coach, Study and Learn, Canva in Teams, genspark.ai — each opened by the
piece of research-management work it is for rather than by a feature list,
and each showing what the facilitator actually types or does.

The segment lives in the Sensitive Lane, so every slide carries the lane
chip, and the other lane is not named anywhere on a slide or in a note: the
two lanes are demonstrated separately, and a participant watching this
segment should have nothing to compare against yet. A test enforces that.

Where the teal goes is narrower than "the whole segment is teal". The
template's rule is that a lane colour says "this is about that tool", so
only the three tools that run inside the institutional tenant — Acrobat,
Prompt Coach, Study and Learn — take it in their content blocks. Canva and
genspark.ai sit outside the tenant and their own slides say so; teal on
those blocks would assert the opposite of the caution beside it, so they
are slate throughout and the lane chip is their only teal. A test holds
that line.

Three of the seven run on screen — the first scenario, Prompt Coach, and
Study and Learn — and each carries a `template.add_demo_cue` band mirrored
by the step-by-step script in its speaker notes. The remaining four say so
in the notes ("slide only"), so the facilitator never has to guess which
tab to open.

Acrobat is the one tool whose slide has to subtract as well as add: the
compiled list mixes free-to-use features with a premium tier and an AI
Assistant add-on the institutional licence does not include. Both paid
blocks are headed "Not available", and a test asserts every paid
capability sits inside one of them.
"""

from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches, Pt

from deck.lesson2 import template
from deck.lesson2.template import (
    HEADING_FONT, INK, MUTED, PANEL, SENSITIVE_LANE, SLATE, TEXT,
)

LANE = SENSITIVE_LANE

# The content area, in inches, as the column geometry every slide here is
# laid out on — two columns for a pair of blocks, three for a row of them.
_LEFT = template.CONTENT_LEFT.inches
_WIDTH = template.CONTENT_WIDTH.inches
_GAP = 0.23
_COL_WIDTH = (_WIDTH - _GAP) / 2
_RIGHT_COL = _LEFT + _COL_WIDTH + _GAP
_COL3_WIDTH = (_WIDTH - 2 * _GAP) / 3


def _tool_slide(prs, title, scenario, accent, band_height=0.80, band_size=17):
    """A tool slide: the lane's content slide, opened by the piece of work
    the tool is for. Every tool in the compiled list is introduced this way,
    so the room hears the task before it hears the product name.

    `accent` is the colour the slide's own blocks carry — the lane's for a
    tool that runs inside the institutional tenant, slate for one outside
    it, because a lane colour says "this is about that tool".
    """
    slide = template.add_content_slide(prs, title, lane=LANE)
    template.add_band(slide, Inches(1.30), Inches(band_height), scenario,
                      size=band_size, fill=accent)
    return slide


# --- Sensitive Lane scenarios (≈2 min) ---------------------------------------

# The plan's four scenarios, in its order: the category from CONTEXT.md's
# Sensitive Lane entry, the one-line prompt, and what is prepared before
# anything is pasted.
_SCENARIOS = [
    ("Internal administration",
     "“Turn these meeting notes into a decision log and action list”",
     "Notes pasted in, names replaced by roles"),
    ("Unsubmitted proposals",
     "“Check this draft work-package description against the call's "
     "evaluation criteria and list gaps”",
     "The call text and the draft, both pasted in"),
    ("Personnel matters",
     "“Draft a neutral workload-distribution note for a three-person unit "
     "from these constraints”",
     "Constraints as roles and hours — no names, no evaluations"),
    ("Strategic financial planning",
     "“Build a three-scenario cost projection table from these assumptions”",
     "Assumptions in; the figures never leave the institutional tenant"),
]

_SCENARIO_TOP = 1.66
_SCENARIO_PITCH = 0.90
_SCENARIO_HEIGHT = 0.82


def _scenario_row(slide, top, category, prompt, prep):
    """The category and its prompt on one line, over what is prepared before
    the paste. Not add_detail_card: the lead and the prompt share a line
    here, because the pairing is the point of the slide."""
    card = template.add_open_card(
        slide, Inches(_LEFT), Inches(top), Inches(_WIDTH),
        Inches(_SCENARIO_HEIGHT), LANE.color)
    tf = card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.12)
    para = tf.paragraphs[0]
    run = para.add_run()
    run.text = category
    template.style(run, size=13, color=INK, font=HEADING_FONT, bold=True)
    run = para.add_run()
    run.text = f"   {prompt}"
    template.style(run, size=13, color=TEXT)
    para = tf.add_paragraph()
    para.space_before = Pt(3)
    run = para.add_run()
    run.text = prep
    template.style(run, size=11, color=MUTED)
    return card


def _scenarios_slide(prs):
    slide = template.add_content_slide(
        prs, "Four scenarios in the Sensitive Lane", lane=LANE)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "Same prompt shape as last week — ICC: Instruction · Context · "
        "Constraints (Lesson 1). The lane decides where a prompt goes, "
        "never how it is written.",
        size=13, color=MUTED,
    )

    top = _SCENARIO_TOP
    for category, prompt, prep in _SCENARIOS:
        _scenario_row(slide, top, category, prompt, prep)
        top += _SCENARIO_PITCH

    template.add_demo_cue(
        slide,
        "Scenario 1 in Copilot Chat — anonymised meeting notes in, decision "
        "log and action list out",
        Inches(5.42), lane=LANE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.14), template.CONTENT_WIDTH,
        "You reproduce the other three in the assignment and at Practice "
        "Week 1 — watch the shape of the prompt, not the wording",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~2 min, and the segment opens on it. Before the first slide, open "
        "Copilot Chat in Teams and show the enterprise notice — 30 seconds, "
        "no commentary. It is the visible proof of the boundary the last "
        "segment argued for.\n\n"
        "Four categories, four prompts, read at pace. These are the same "
        "four categories the routing slide named, now as work. The point to "
        "make: nothing about the prompt changes between the lanes, only "
        "where it goes.\n\n"
        "Say the ICC line once and move on — they wrote three ICC prompts "
        "last week, this is a reference, not a lesson.\n\n"
        "LIVE, about 2 minutes: scenario 1. Paste the anonymised meeting "
        "notes prepared for today, type the ICC prompt, read the decision "
        "log and the action list out loud. Point at the names as you paste: "
        "roles, not people — the anonymisation happened before the paste, "
        "not after the answer.\n\n"
        "Run one scenario only. The other three are described, not "
        "demonstrated; the room reproduces them in the assignment. If the "
        "demo drifts past 2 minutes, cut it and go to the guardrails.\n\n"
        "State the rule while the answer is on screen: the output is still "
        "checked before it is used. The tenant boundary buys "
        "confidentiality, not correctness."
    ))
    return slide


# --- Limits and guardrails (≈2 min) ------------------------------------------

# The plan's four guardrails: what the enterprise boundary does buy, the
# one limit people trip over, why general work stays out, and the rule the
# boundary does not lift.
_GUARDRAILS = [
    ("Enterprise behaviour",
     "Prompts and answers stay inside the institutional Microsoft 365 "
     "tenant, are not used to train the models, and are covered by the same "
     "terms as the institution's other tenant data. This is what makes it "
     "the Sensitive Lane."),
    ("No SharePoint or OneDrive grounding",
     "It does not read the institution's files by itself. What it knows "
     "about a task is what you paste or attach — the relevant content has "
     "to be brought to it, and curated on the way in (context window, "
     "Lesson 1)."),
    ("Weaker on general work",
     "Shorter effective context and fewer capabilities than a free-tier "
     "tool. Sending ordinary drafting or research work here costs you "
     "quality and buys you nothing."),
    ("Anonymise anyway",
     "The tenant boundary does not lift the anonymise-before-upload rule. A "
     "document carrying personal or sensitive information is anonymised "
     "before it is attached here too."),
]

_GUARDRAIL_TOP = 1.72
_GUARDRAIL_PITCH = 1.90
_GUARDRAIL_HEIGHT = 1.80


def _limits_slide(prs):
    slide = template.add_content_slide(prs, "Limits and guardrails", lane=LANE)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.32), template.CONTENT_WIDTH,
        "What the institutional account buys you, and what it does not",
        size=13, color=MUTED,
    )

    for index, (heading, body) in enumerate(_GUARDRAILS):
        left = _LEFT if index % 2 == 0 else _RIGHT_COL
        top = _GUARDRAIL_TOP + (index // 2) * _GUARDRAIL_PITCH
        card = template.add_card(
            slide, Inches(left), Inches(top), Inches(_COL_WIDTH),
            Inches(_GUARDRAIL_HEIGHT), PANEL, heading, INK, body,
        )
        card.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        card.text_frame.margin_top = Inches(0.22)

    template.add_band(
        slide, Inches(5.66), Inches(0.78),
        "Reserve it for the sensitive work",
        size=19, fill=LANE.color,
        sub="The boundary is the whole reason this lane exists — and the "
            "reason everything else belongs somewhere else",
    )

    template.set_notes(slide, (
        "~2 min. Four cards, and the second one is the one that saves "
        "support time later.\n\n"
        "Enterprise behaviour: this is the answer to “is it safe to paste "
        "this?”. Inside the tenant, not training data, same terms as the "
        "institution's other Microsoft 365 content.\n\n"
        "No grounding is the surprise. People expect an institutional tool "
        "to know the institution's files; it does not open SharePoint or "
        "OneDrive by itself. If it has not been pasted or attached, it is "
        "not in the conversation. Tie it to Lesson 1: what you bring is "
        "curated, because more context is not better context.\n\n"
        "Weaker on general work — say it plainly, and do not name the "
        "alternative yet; the next segment shows what it can do instead of "
        "arguing about it now.\n\n"
        "Anonymise anyway: the expected exception, refused. The rule is "
        "about the document, not about the destination.\n\n"
        "Close on the band and go straight into the tool slides: reserve "
        "the lane for the sensitive work."
    ))
    return slide


# --- Adobe Acrobat (slide only) ----------------------------------------------

# The compiled list's five free-to-use features, in its own words, so the
# slide and the licence say the same thing.
_ACROBAT_FREE = [
    "High-quality viewing — high-fidelity PDFs opened inside Teams, Outlook "
    "and Microsoft 365",
    "Central access to PDFs — channel and chat files, OneDrive and your own "
    "machine, in one place",
    "Streamline PDF review — the unit's feedback collected in a single PDF "
    "inside Teams (not on mobile)",
    "Keep reviewers informed — a reviewer is notified when someone replies "
    "to their comment",
    "Collaborate with confidence — versions retained in SharePoint or "
    "OneDrive",
]

# The two paid blocks. Both headings start "Not available"; a test asserts
# every capability named here sits inside a block that says so.
_ACROBAT_PAID = [
    ("Not available — Premium (needs an Acrobat subscription)",
     ["Convert PDFs to Word, Excel and PowerPoint, or to an image · combine "
      "multiple documents into one PDF · delete, rotate, extract, insert or "
      "reorder pages · reduce the size of a PDF · add a password"]),
    ("Not available — AI Assistant (needs the add-on)",
     ["Answers about a document with attributions back to the source · "
      "drafting from your own documents · meeting transcript summaries"]),
]

_ACROBAT_STEPS = (
    "Open the PDF from the channel → Comment → share the review back to the "
    "channel, so every reply lands on the same file"
)


def _acrobat_slide(prs):
    slide = _tool_slide(
        prs, "Adobe Acrobat in Teams and Copilot",
        "A call document lands as a PDF in a Teams channel: read it in high "
        "fidelity, and collect the unit's comments in that one file instead "
        "of reconciling four separate attachments",
        LANE.color, band_height=0.86, band_size=16,
    )

    template.add_list_card(
        slide, Inches(_LEFT), Inches(2.30), Inches(_COL_WIDTH), Inches(2.62),
        PANEL, "Free to use", _ACROBAT_FREE, size=11.5)

    top = 2.30
    for heading, lines in _ACROBAT_PAID:
        template.add_detail_card(
            slide, Inches(_RIGHT_COL), Inches(top), Inches(_COL_WIDTH),
            Inches(1.26), SLATE, heading, lines, line_size=11)
        top += 1.36

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(5.04), Inches(_WIDTH), Inches(0.74),
        LANE.color, "What you do", [_ACROBAT_STEPS], line_size=12)

    template.add_band(
        slide, Inches(5.90), Inches(0.64),
        "Plan the workflow around the free features — the paid tiers are "
        "not part of the institutional licence",
        size=15, fill=SLATE,
    )

    template.set_notes(slide, (
        "Slide only — no demo here; the plan gives the three slide-only "
        "tools 1.5 minutes between them, so this one gets about 30 "
        "seconds.\n\n"
        "Lead with the work, not the product: a call document arrives as a "
        "PDF in a channel and four people comment on four separate "
        "attachments. Acrobat's free tier is the answer to that one problem "
        "— one file, one set of comments, everyone notified.\n\n"
        "The free/paid boundary is the point of the slide, and it is the "
        "thing to get right before delivery: convert, combine, reorganise, "
        "compress and password-protect need an Acrobat subscription, and "
        "the AI Assistant needs its own add-on. Neither is in what you "
        "have. Check both blocks in your own account the day before — Adobe "
        "moves features between tiers. Two the compiled list names in its "
        "blurb but places in no tier are redact and export; find out where "
        "those sit before you promise them.\n\n"
        "If someone asks why Acrobat is not simply the default PDF viewer "
        "in Teams: a tenant admin can set that policy centrally. That is an "
        "IT request, not something a participant configures.\n\n"
        "The PDF is still a document: if it carries personal or sensitive "
        "information it is anonymised before it goes anywhere near a chat."
    ))
    return slide


# --- Prompt Coach (live) -----------------------------------------------------

_COACH_PROMPT = (
    "“Here is a prompt I wrote and the goal it was meant to serve. Critique "
    "it against that goal, then give me an improved version and explain each "
    "change.”"
)

_COACH_BLOCKS = [
    ("What comes back",
     ["A critique of your prompt against the goal you stated",
      "An improved version, ready to paste",
      "The reasoning behind each change — so the next prompt is better "
      "before it is critiqued"]),
    ("The Lesson 1 link",
     ["Meta-prompting, packaged as an agent: the model as your prompt "
      "engineer, with the coach persona already built in",
      "Keep the improved prompt — it is the first entry in your prompt "
      "library"]),
]


def _coach_slide(prs):
    slide = _tool_slide(
        prs, "Prompt Coach — your own prompt, critiqued",
        "Take one of the three ICC prompts from your Lesson 1 assignment, "
        "paste it in, and ask for a critique and a rewrite",
        LANE.color,
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.28), Inches(_WIDTH), Inches(0.94),
        LANE.color, "What you type", [_COACH_PROMPT], line_size=12.5)

    for left, (heading, lines) in zip((_LEFT, _RIGHT_COL), _COACH_BLOCKS):
        template.add_detail_card(
            slide, Inches(left), Inches(3.38), Inches(_COL_WIDTH),
            Inches(1.40), SLATE, heading, lines)

    template.add_demo_cue(
        slide,
        "Prompt Coach on an ICC prompt from the debrief — with the author's "
        "permission",
        Inches(4.96), lane=LANE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.68), template.CONTENT_WIDTH,
        "A prompt is worth improving once and reusing twenty times — that "
        "is what a prompt library is for",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Prompt Coach runs LIVE, about 2 minutes. Ask in the Teams chat "
        "during the debrief whether one volunteer will let you use their "
        "prompt here, and get their permission before the segment — never "
        "lift a prompt off someone's screen without it. If nobody offers, "
        "use your own; have it ready either way.\n\n"
        "Run it once: paste the prompt, state the goal it was meant to "
        "serve, ask for a critique and a rewrite. Read the critique aloud "
        "and stop at the first concrete change — one improvement the room "
        "can see is worth more than a full list they cannot follow.\n\n"
        "The tie-back is one sentence: this is last week's meta-prompting, "
        "packaged as an agent. Do not re-teach meta-prompting; they used it "
        "in the assignment.\n\n"
        "Say what happens to the output: the improved prompt gets saved. "
        "That is the beginning of the prompt library, and the prompts in it "
        "are what the assignment's workflow steps are built out of.\n\n"
        "If the coach's rewrite is worse than the original — it happens — "
        "keep it on screen and say so. Every output is checked, including "
        "this one."
    ))
    return slide


# --- Study and Learn (live) --------------------------------------------------

# The three learning outcomes the agent supports, as the compiled list
# describes them.
_STUDY_OUTCOMES = [
    ("Understand",
     ["A concept explained conversationally, at the depth you ask for"]),
    ("Practise",
     ["Flashcards generated from the explanation, for spaced repetition"]),
    ("Check",
     ["A study guide and a quiz — what the learner can actually do"]),
]


def _study_slide(prs):
    slide = _tool_slide(
        prs, "Study and Learn — concepts, flashcards, quizzes",
        "Explain a concept from your Anchor Project's domain — eligible "
        "costs, say — then turn the explanation into flashcards and a "
        "five-question quiz for a junior colleague",
        LANE.color, band_height=0.86, band_size=16,
    )

    for index, (heading, lines) in enumerate(_STUDY_OUTCOMES):
        left = _LEFT + index * (_COL3_WIDTH + _GAP)
        template.add_detail_card(
            slide, Inches(left), Inches(2.36), Inches(_COL3_WIDTH),
            Inches(1.08), LANE.color, heading, lines, heading_size=15)

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(3.62), Inches(_WIDTH), Inches(0.80),
        SLATE, "What it needs",
        ["A Microsoft 365 Education account (Entra ID). No Copilot licence "
         "required."])

    template.add_demo_cue(
        slide,
        "The concept explained, then flashcards and a five-question quiz "
        "built from it",
        Inches(4.60), lane=LANE,
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(5.32), Inches(_WIDTH), Inches(0.92),
        SLATE, "Why it matters for the assignment",
        ["Your deliverable is a presentation designed to facilitate learning "
         "outcomes. This is where you find out whether they land — build the "
         "quiz, and the gaps in the presentation show up as questions "
         "nobody can answer."])

    template.set_notes(slide, (
        "LIVE, about 2 minutes, and it is the demo that pays off in "
        "Segment 5.\n\n"
        "Pick a concept the room shares — eligible costs works, so does "
        "reporting periods. Ask for the explanation first, at a stated "
        "depth: “for a colleague who joined the office last month”.\n\n"
        "Then the two moves that matter: turn that explanation into "
        "flashcards, and turn it into a five-question quiz. Read two "
        "flashcards and one quiz question aloud. Do not read the whole "
        "set.\n\n"
        "The access line saves a support ticket: it needs a Microsoft 365 "
        "Education account, not a Copilot licence. Confirm it in your own "
        "account the day before, and if a participant's account does not "
        "show the agent, that goes on the capture list for Practice "
        "Week 1.\n\n"
        "Name the link to the assignment out loud: the quiz is how a "
        "presentation gets tested. A question nobody can answer is a slide "
        "that did not teach.\n\n"
        "The explanation is generated, so it is checked before it is taught "
        "to anyone — the flashcards inherit whatever the explanation got "
        "wrong."
    ))
    return slide


# --- Canva in Teams (slide only) ---------------------------------------------

_CANVA_BLOCKS = [
    ("What the Teams app gives you",
     ["Design notifications and updates in one place, without leaving Teams",
      "Colleagues invited to preview or collaborate on a design",
      "Multi-page designs viewed inside Teams"]),
    ("Prototyping only",
     ["The structure and the look of the presentation — the order of the "
      "sections, what goes on a page, where the examples sit",
      "Not the finished deck: that is the next slide"]),
]

_CANVA_STEPS = (
    "New multi-page design → one page per section of the presentation → "
    "share it to the channel and let the comments come back in Teams"
)


def _canva_slide(prs):
    slide = _tool_slide(
        prs, "Canva in Teams — prototype the presentation",
        "Prototype the structure of your assignment presentation as a "
        "multi-page design, previewed and commented on without leaving Teams",
        SLATE,
    )

    for top, height, (heading, lines) in zip(
            (2.22, 3.54), (1.20, 1.00), _CANVA_BLOCKS):
        template.add_detail_card(
            slide, Inches(_LEFT), Inches(top), Inches(_WIDTH), Inches(height),
            SLATE, heading, lines, heading_size=14, line_size=12)

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(4.66), Inches(_WIDTH), Inches(0.74),
        SLATE, "What you do", [_CANVA_STEPS], line_size=12)

    template.add_band(
        slide, Inches(5.52), Inches(0.78),
        "A third-party design platform surfaced inside Teams",
        size=15, fill=SLATE,
        sub="The design leaves the institutional tenant, so the routing rule "
            "applies to it: anonymised, non-sensitive content only",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.40), template.CONTENT_WIDTH,
        "Prototype first, build second — a structure is cheap to change, a "
        "finished deck is not",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Slide only — about 30 seconds. Do not open Canva; there is no time "
        "and the app adds nothing to watch.\n\n"
        "One idea: prototype before you build. The Teams app is the reason "
        "it is worth doing here rather than in a separate browser tab — "
        "notifications, previews and comments land where the Cohort already "
        "works.\n\n"
        "Be precise about the scope. This is the structure of the "
        "presentation, not the presentation. The next slide is where the "
        "deck itself gets made.\n\n"
        "The caution is not decoration: Canva sits outside the "
        "institutional tenant, which is also why nothing on this slide "
        "carries the lane's colour. Whatever goes into a design is subject "
        "to the routing rule and anonymised first, exactly as in the last "
        "segment.\n\n"
        "If anyone asks about the Canva they already use privately: same "
        "app, and the same rule about what goes into it."
    ))
    return slide


# --- genspark.ai (slide only) ------------------------------------------------

_CHAIN = [
    ("1 · Prototype",
     ["Canva in Teams — the structure, agreed before anything is built"]),
    ("2 · Content",
     ["Drafted in whichever lane the topic routes to, and checked"]),
    ("3 · Deck",
     ["genspark.ai — the presentation itself, from the prototype and the "
      "approved content"]),
]

_GENSPARK_PROMPT = (
    "“Build a 12-slide educational presentation on <topic> from this "
    "outline. Audience: research management administrators. One idea per "
    "slide, a worked example every third slide, and a five-question quiz at "
    "the end.”"
)


def _genspark_slide(prs):
    slide = _tool_slide(
        prs, "genspark.ai — build the actual presentation",
        "Hand the approved prototype and the drafted content to genspark.ai "
        "and get the presentation itself back",
        SLATE,
    )

    for index, (heading, lines) in enumerate(_CHAIN):
        left = _LEFT + index * (_COL3_WIDTH + _GAP)
        template.add_detail_card(
            slide, Inches(left), Inches(2.28), Inches(_COL3_WIDTH),
            Inches(1.10), SLATE, heading, lines, heading_size=15)

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(3.52), Inches(_WIDTH), Inches(0.92),
        SLATE, "What you type", [_GENSPARK_PROMPT], line_size=12)

    template.add_band(
        slide, Inches(4.58), Inches(0.86),
        "Outside the institutional tenant — anonymised, non-sensitive "
        "content only",
        size=17, fill=SLATE,
        sub="The routing rule applies to every step of a chain, not only to "
            "the first one",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.62), template.CONTENT_WIDTH,
        "The presentation itself is next week's deliverable — Segment 5 "
        "gives you the rest of the assignment",
        size=12, color=MUTED,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.06), template.CONTENT_WIDTH,
        "Every step names its tool, its input, its output — and its lane",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Slide only — about 30 seconds, and it closes the segment.\n\n"
        "Three boxes, read left to right: the prototype, the content, the "
        "deck. That is the first chain the room has seen end to end, and "
        "the assignment asks them to write one down.\n\n"
        "The caution carries the weight of the whole segment: genspark.ai "
        "sits outside the tenant, which is why this slide carries none of "
        "the lane's colour either. The routing rule is not a gate at the "
        "front of a workflow — it is applied at every step, and a chain is "
        "only as safe as the least protected tool in it.\n\n"
        "Do not brief the assignment here. One sentence pointing at "
        "Segment 5 is the whole handover; the deliverable slide comes after "
        "the next segment.\n\n"
        "Practical note for the week before: try genspark.ai yourself on a "
        "fictional topic first. It is the least familiar of the five, and "
        "whatever it produces still gets checked before it is shown to "
        "anyone."
    ))
    return slide


def add_slides(prs):
    _scenarios_slide(prs)
    _limits_slide(prs)
    _acrobat_slide(prs)
    _coach_slide(prs)
    _study_slide(prs)
    _canva_slide(prs)
    _genspark_slide(prs)

"""Segment 4 — Gemini in depth (+ NotebookLM preview) (15 min, Live
facilitator demo).

Fifteen slides, per lesson_2.md Segment 4 and in its order: an opener
carrying the availability flag, then one slide per row of the plan's
capability table — file and image upload, long context, Gems, Deep
Research, Canvas, Google Workspace hooks, image generation, Gemini Live
and mobile, Guided Learning, saved info — then the three NotebookLM
scenarios, then one closing slide that chains what the room has just seen
into the shape of the assignment.

Every capability slide opens on the piece of research-management work it
is for, on the participant's own Anchor Project material, rather than on a
feature list. Four of them run on screen — upload, long context, Gems,
Canvas, exactly the four the plan's table marks **Live** — and each
carries a `template.add_demo_cue` band mirrored by the step-by-step script
in its notes. The rest say in their notes whether they are a prepared
result or a slide, with the seconds the plan's demo script gives them, so
the facilitator never has to guess which tab to open. A test holds the
cues to the plan's four.

The segment lives in the Daily Driver, so every slide carries the lane
chip and the Sensitive Lane's tool is named nowhere on a slide or in a
note: the two lanes are demonstrated separately, and this segment is about
what one tool does, not about a comparison. A test enforces that.

Where the violet goes is narrower than "the whole segment is violet". The
template's rule is that a lane colour says "this is about that tool", so
only the capability slides — which are about the Daily Driver itself —
take it in their content blocks. The three NotebookLM slides are about a
different product, one the course does not open until Lesson 3, so they
are slate throughout and the lane chip is their only violet. A test holds
that line, and the same rule puts the Workspace-hooks slide's "not on the
free tier" block in slate while its workaround stays violet.

The availability flag is the one thing on this segment that cannot be
finished in code: Google moves capabilities between plans month to month,
so the opener says "free tier at the time of writing (September 2026)" on
the slide and every set of notes that promises a capability repeats the
re-verification reminder.
"""

from pptx.util import Inches

from deck.lesson2 import template
from deck.lesson2.template import (
    DAILY_DRIVER, DAILY_TINT, MUTED, PANEL, SLATE,
)

LANE = DAILY_DRIVER

# The content area, in inches, as the column geometry every slide here is
# laid out on — the same grid Segment 3 uses, so the two demo segments
# read as one deck.
_LEFT = template.CONTENT_LEFT.inches
_WIDTH = template.CONTENT_WIDTH.inches
_GAP = 0.23
_COL_WIDTH = (_WIDTH - _GAP) / 2
_RIGHT_COL = _LEFT + _COL_WIDTH + _GAP
_COL3_WIDTH = (_WIDTH - 2 * _GAP) / 3

# The sentence the facilitator says while demoing (plan, "Rule stated
# while demoing"), on the opener and repeated in the live slides' notes.
_ANONYMISATION_RULE = (
    "Everything on screen is anonymised or fictional — the "
    "“what must never enter Gemini” list from Segment 2 stays on "
    "the second monitor"
)

_REVERIFY = (
    "Re-verify in your own account the week before delivery: the free tier "
    "moves month to month, and anything that has moved behind a paid plan "
    "is shown as a slide and marked as such."
)


def _scenario_slide(prs, title, scenario, band_height=0.84,
                    fill=None):
    """The segment's content slide, opened by the piece of research-
    management work the capability is for. Every row of the plan's table
    is introduced this way, so the room hears the task before it hears
    the feature name.

    `fill` is the scenario band's colour: the lane's for the Daily
    Driver's own capabilities, slate for the NotebookLM slides, which are
    about a different product (see _notebook_slide).
    """
    slide = template.add_content_slide(prs, title, lane=LANE)
    template.add_band(slide, Inches(1.30), Inches(band_height), scenario,
                      size=16, fill=LANE.color if fill is None else fill)
    return slide


# One row of blocks across the content width, in as many equal columns as
# there are blocks — the shape almost every slide in this segment ends in.
def _block_row(slide, blocks, top, height, edge=None, **card):
    width = (_WIDTH - (len(blocks) - 1) * _GAP) / len(blocks)
    for index, (heading, lines) in enumerate(blocks):
        template.add_detail_card(
            slide, Inches(_LEFT + index * (width + _GAP)), Inches(top),
            Inches(width), Inches(height),
            LANE.color if edge is None else edge, heading, lines, **card)


# --- Opener: the capability list and the availability flag (≈30 s) -----------

# The plan's ten capabilities, grouped by what the room will actually see
# of each — the plan's Demo column, in its three values. Every capability
# in the table appears here, and again on a slide of its own.
_INVENTORY = [
    ("Live on screen",
     ["File and image upload", "Long context", "Gems — persistent context",
      "Canvas"],
     DAILY_TINT),
    ("Prepared result",
     ["Deep Research", "Image generation and editing"],
     PANEL),
    ("Named, not demonstrated",
     ["Google Workspace hooks", "Gemini Live and mobile",
      "Guided Learning mode", "Saved info"],
     PANEL),
]


def _opener_slide(prs):
    slide = template.add_content_slide(
        prs, "What the Daily Driver adds", lane=LANE)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "Ten free-tier capabilities, one research-management scenario each, "
        "all of them on your own Anchor Project material",
        size=13, color=MUTED,
    )

    for index, (heading, items, fill) in enumerate(_INVENTORY):
        left = _LEFT + index * (_COL3_WIDTH + _GAP)
        template.add_list_card(
            slide, Inches(left), Inches(1.86), Inches(_COL3_WIDTH),
            Inches(2.34), fill, heading, items, size=12.5)

    template.add_band(
        slide, Inches(4.44), Inches(1.00),
        "Free tier at the time of writing — September 2026",
        size=19, fill=LANE.color,
        sub="Google moves capabilities between plans month to month. What is "
            "demonstrated today was checked in this account last week; check "
            "yours before you build a workflow on any one of them.",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.62), template.CONTENT_WIDTH,
        _ANONYMISATION_RULE,
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~30 seconds, and then straight into the first demo — this slide is "
        "a map, not a lesson.\n\n"
        "Say what the next fifteen minutes are: one tool, ten capabilities, "
        "a scenario each, and four of them on screen live. The room does "
        "not need to remember the list; they need to know it exists and "
        "that the slides are the reference afterwards.\n\n"
        "The availability flag is the important line. Say it once, plainly: "
        "this is the free tier as of September 2026, and it changes. "
        + _REVERIFY + " If a capability moved this month, say so here "
        "rather than discovering it on screen.\n\n"
        "State the rule before the first upload and leave it stated: "
        "everything demonstrated today is anonymised or fictional. Have the "
        "Segment 2 “what must never enter Gemini” list open on the second "
        "monitor for the rest of the segment — if a participant suggests a "
        "document in the chat, that list is the answer.\n\n"
        "Have ready before the session: the anonymised call PDF, the "
        "budget-table screenshot, the long guideline document, the Gem "
        "half-built, the Deep Research report from last night, and the "
        "generated diagram. Six tabs, in that order."
    ))
    return slide


# --- File and image upload (LIVE, 2.5 min) -----------------------------------

_UPLOAD_PROMPT = (
    "“You are advising a research management office. From the attached call "
    "document, give me the eligibility criteria as a checklist we can tick "
    "off. From the attached table image, tell me which cost lines sit above "
    "the call's caps. Ask me before assuming anything the documents do not "
    "state.”"
)

_UPLOAD_BLOCKS = [
    ("What comes back",
     ["A checklist you can paste into the project's guide page",
      "A reading of a table that only ever existed as a photograph",
      "Its own questions, where the documents are silent — the "
      "ask-me-first pattern from Lesson 1"]),
    ("Before anything is uploaded",
     ["Both files are cleared first: the call document anonymised where "
      "your copy carries internal notes, the budget table fictional — "
      "names, sums and partners changed before the screenshot",
      "A document with personal or sensitive information does not come "
      "here at all (Segment 2)"]),
]


def _upload_slide(prs):
    slide = _scenario_slide(
        prs, "File and image upload",
        "An anonymised call document as a PDF and a photographed budget "
        "table as an image, in the same question — the checklist out of one, "
        "a reading of the numbers out of the other",
        band_height=0.88,
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.32), Inches(_WIDTH), Inches(1.06),
        LANE.color, "What you type", [_UPLOAD_PROMPT], line_size=12.5)

    _block_row(slide, _UPLOAD_BLOCKS, 3.54, 1.52)

    template.add_demo_cue(
        slide,
        "PDF and screenshot attached to one prompt — eligibility checklist "
        "and the table read back",
        Inches(5.24), lane=LANE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.96), template.CONTENT_WIDTH,
        "A photograph of a table is a document too — and it is anonymised "
        "the same way",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "LIVE, 2.5 minutes — the plan's first demo step, and the one that "
        "earns the segment its time. Two files, one prompt.\n\n"
        "Attach both before you type: the anonymised call PDF and the "
        "budget-table screenshot. Say out loud what you did to them — the "
        "sums and the partner names are invented, and that happened before "
        "the upload, not after the answer.\n\n"
        "Type the ICC prompt as written on the slide: instruction, context, "
        "constraints, and the ask-me-first clause at the end. They wrote "
        "three of these last week; this is the same shape with files "
        "attached, not a new technique.\n\n"
        "Read two lines of the checklist aloud, then jump to the table "
        "reading. The image is the part people do not expect — point at it: "
        "nobody typed those numbers in.\n\n"
        "If it asks you a question back, answer it on screen. That is the "
        "ask-me-first pattern working, and it is worth ten seconds.\n\n"
        + _ANONYMISATION_RULE + ".\n\n"
        "The answer is still checked before it is used. An eligibility "
        "checklist that missed a criterion is worse than no checklist.\n\n"
        "If the upload fails or the file is rejected, do not debug it live "
        "— say what should have happened, move to long context, and put it "
        "on the capture list for Practice Week 1.\n\n"
        + _REVERIFY + " Upload limits and accepted file types are the "
        "part of this that moves quietly."
    ))
    return slide


# --- Long context (LIVE, short, 1.5 min) -------------------------------------

_CONTEXT_PROMPT = (
    "“Here is the funder's guideline document. Summarise it as the ten "
    "things our office has to do differently from last year's call, each "
    "with the section it comes from.”"
)

_CONTEXT_BLOCKS = [
    ("Why it holds",
     ["The whole guideline goes in at once instead of in extracts, and the "
      "answer can cite across all of it",
      "The free tier's window is smaller than the paid plans'; a very long "
      "document may still have to be split"]),
    ("It does not lift Lesson 1's rule",
     ["More context is not better context. A guideline plus four unrelated "
      "documents gives you a worse summary, not a fuller one",
      "Curate on the way in: one document, one question, one job"]),
]


def _long_context_slide(prs):
    slide = _scenario_slide(
        prs, "Long context",
        "A funder's guidelines pasted in whole rather than in extracts, "
        "and the answer that matters: what changed since last year's call, "
        "section by section",
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.28), Inches(_WIDTH), Inches(0.94),
        LANE.color, "What you type", [_CONTEXT_PROMPT], line_size=12.5)

    _block_row(slide, _CONTEXT_BLOCKS, 3.38, 1.52)

    template.add_demo_cue(
        slide, "One long guideline document in, a structured summary out",
        Inches(5.08), lane=LANE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.80), template.CONTENT_WIDTH,
        "The window is what you may bring, not what you should bring",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "LIVE and short — 1.5 minutes, one document, one summary. Do not "
        "let this one run: the Gem is the demo that matters and it is next.\n\n"
        "Paste the long guideline document you prepared. Say its length out "
        "loud while it loads — however many pages yours runs to, one paste. "
        "That number is the whole point of the slide, so use the real one "
        "rather than a figure off a slide.\n\n"
        "Ask for the structured summary with the section references, read "
        "three items, stop. Point at one section reference and say why it "
        "is there: an answer you can check is worth more than an answer you "
        "have to trust.\n\n"
        "Then the counterweight, in one sentence, because it is the Lesson 1 "
        "link: the window is what you may bring, not what you should bring. "
        "More context is not better context — the curation rule survives "
        "the bigger window.\n\n"
        "Free-tier limit: the window is smaller than the paid plans'. "
        + _REVERIFY + "\n\n"
        + _ANONYMISATION_RULE + " — the guideline document is public, which "
        "is why it is the one being pasted."
    ))
    return slide


# --- Gems — persistent context (LIVE, 3 min, the Level 3 move) ---------------

_GEM_BLOCKS = [
    ("Name and purpose",
     ["“Anchor Project assistant” — one Gem per project, not one per task"]),
    ("Standing instructions",
     ["Your Lesson 1 ICC prompt, promoted: what it should do, who it is "
      "advising, the constraints it always works under — written once, "
      "applied to every future chat",
      "The reverse prompt becomes its opening move: ask me what you need "
      "before you answer"]),
    ("Reference files",
     ["The project description, the call text, your own notes — up to the "
      "free tier's reference-file limit"]),
]


def _gems_slide(prs):
    slide = _scenario_slide(
        prs, "Gems — persistent context",
        "Build one Gem for your Anchor Project, and every chat you open "
        "afterwards already knows the project, the funder and the rules you "
        "work under",
    )

    _block_row(slide, _GEM_BLOCKS, 2.26, 1.66, heading_size=14)

    template.add_demo_cue(
        slide,
        "A Gem built from scratch — name, instructions, reference files, "
        "then the first chat that already knows the project",
        Inches(4.08), lane=LANE,
    )

    template.add_band(
        slide, Inches(4.84), Inches(1.00),
        "This is the Level 3 move",
        size=20, fill=LANE.color,
        sub="Level 2 was writing a good prompt every time. Level 3 is "
            "building the workspace that no longer needs you to — persistent "
            "context, ready before the question. The assignment lays the "
            "foundation for Level 4.",
    )

    template.set_notes(slide, (
        "LIVE, 3 minutes — the longest demo in the segment, and the one the "
        "whole course structure points at. Do not shorten this one; shorten "
        "Canvas instead.\n\n"
        "Build the Gem in front of them, in the plan's four steps: name, "
        "instructions, reference files, first chat. Have it half-built in a "
        "second tab in case the creation flow has moved.\n\n"
        "Name: “Anchor Project assistant”. Say the rule while you type it — "
        "one Gem per project, not one per task. A Gem per task is a prompt "
        "with extra steps.\n\n"
        "Instructions: paste one of your own ICC prompts from last week and "
        "edit it into standing instructions as they watch. This is the "
        "sentence to say out loud: the prompt you wrote once is now the "
        "brief it always works under. Add the reverse prompt — ask me what "
        "you need before you answer — as its opening move.\n\n"
        "Reference files: attach the project description and the call text. "
        "Name the free tier's file limit as you hit it. " + _REVERIFY + "\n\n"
        "First chat: ask it something you would otherwise have to explain "
        "the project for — “draft the risk section for this project's "
        "next report”. The point lands when nobody had to paste the "
        "project description.\n\n"
        "Then the Level 3 line, and connect it to the recap map from "
        "Segment 1: Level 2 was the Prompt Crafter, done in last week's "
        "assignment. This is the Power User — dedicated workspaces that "
        "already know your domain. The assignment chains them, which is "
        "Level 4.\n\n"
        + _ANONYMISATION_RULE + " — the Gem's reference files included; "
        "whatever goes in a Gem stays in it."
    ))
    return slide


# --- Deep Research (prepared result) -----------------------------------------

_RESEARCH_PROMPT = (
    "“Which national and European funders opened calls in the last twelve "
    "months for work in my Anchor Project's field? For each: the funder, "
    "what it funds, the deadline pattern, and the source you found it in.”"
)

_RESEARCH_BLOCKS = [
    ("What comes back",
     ["A briefing rather than a chat answer: sections, a source list, and a "
      "statement of what it could not find"]),
    ("The cap",
     ["The free tier allows a small number of reports a month, and a run "
      "takes minutes rather than seconds — this one was started last night"]),
    ("Check it anyway",
     ["It lists its sources so you can open them. A deadline that is not in "
      "the source is not a deadline"]),
]


def _deep_research_slide(prs):
    slide = _scenario_slide(
        prs, "Deep Research",
        "One question about the funding landscape, answered as a briefing "
        "with its sources — the work that used to be an afternoon of "
        "opening funder pages",
    )

    _block_row(slide, _RESEARCH_BLOCKS, 2.24, 1.44, heading_size=14)

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(3.84), Inches(_WIDTH), Inches(0.98),
        LANE.color, "What you type", [_RESEARCH_PROMPT], line_size=12.5)

    template.add_band(
        slide, Inches(4.98), Inches(0.72),
        "On screen today: a report run last night, and the prompt that "
        "produced it",
        size=15, fill=SLATE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.84), template.CONTENT_WIDTH,
        "A monthly cap is a planning constraint: decide what the question "
        "is before you spend one",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Prepared result, not a live run, and about 20 seconds. The plan's "
        "demo script runs it in one batch with Workspace hooks, image "
        "generation, Guided Learning and saved info — five slides sharing "
        "1.5 minutes. Have the report open in a tab.\n\n"
        "It sits here because the slides follow the plan's capability "
        "table, which puts it before Canvas. The script runs Canvas live "
        "first: either take the 20 seconds here, or skip forward to Canvas "
        "and come back to this slide with the rest of the batch. Decide "
        "before the session, not on the day.\n\n"
        "Show the shape, not the content: sections, sources, and the line "
        "where it says what it could not find. Scroll once. Do not read it.\n\n"
        "Say why it is not live: a run takes minutes, and the free tier caps "
        "how many you get a month. That cap is the reason to write the "
        "question properly before spending one — which is the same "
        "discipline as last week's ICC prompt, at a higher price.\n\n"
        + _REVERIFY + " The cap in particular moves.\n\n"
        "Every source is a link you can open. Say the verification rule "
        "once more here — a briefing that looks finished is exactly the "
        "kind of output people forget to check."
    ))
    return slide


# --- Canvas (LIVE, 2 min) ----------------------------------------------------

_CANVAS_PROMPT = (
    "“Draft the outline of a 20-minute presentation that teaches a junior "
    "colleague how our office handles reporting periods. Sections, one "
    "learning outcome each, and where an example goes.”"
)

_CANVAS_BLOCKS = [
    ("What Canvas is",
     ["A document beside the chat, edited in place — not a wall of chat "
      "text you have to copy out",
      "Rewrite one section and the rest stays where it was"]),
    ("What you take away",
     ["A structured draft you can export and keep working on",
      "This is the assignment's deliverable, started: an educational "
      "presentation on a topic you pick"]),
]


def _canvas_slide(prs):
    slide = _scenario_slide(
        prs, "Canvas",
        "Draft the outline of your assignment presentation, then rewrite "
        "one section at a time without losing the rest",
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.28), Inches(_WIDTH), Inches(0.98),
        LANE.color, "What you type", [_CANVAS_PROMPT], line_size=12.5)

    _block_row(slide, _CANVAS_BLOCKS, 3.42, 1.44)

    template.add_demo_cue(
        slide,
        "The outline drafted in Canvas, then one section rewritten in place",
        Inches(5.04), lane=LANE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.76), template.CONTENT_WIDTH,
        "Structured outputs are what the next step in a workflow can "
        "actually use",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "LIVE, 2 minutes: the outline, then exactly one iteration. This is "
        "the demo to cut short if the Gem ran long.\n\n"
        "Open Canvas from the chat and give it the prompt on the slide. "
        "While it drafts, say what is different: the answer arrives as a "
        "document beside the conversation, not as chat text to copy out.\n\n"
        "Then the one iteration that makes the point — pick a section and "
        "ask for it to be rewritten shorter, or for the learning outcome to "
        "be sharpened. Show that the other sections did not move. That is "
        "the difference between a draft and a transcript.\n\n"
        "Name the export once: it comes out as a structured draft you can "
        "keep. Do not demonstrate the export — say it and move on.\n\n"
        "Point forward without teaching it: this is where the assignment's "
        "presentation starts, and a structured output is the thing the next "
        "step in a chain can use. The closing slide picks that up.\n\n"
        + _REVERIFY + "\n\n"
        + _ANONYMISATION_RULE + " — draft on the fictional project, not on "
        "a real colleague's."
    ))
    return slide


# --- Google Workspace hooks (slide only, the paid-plan boundary) -------------

def _workspace_slide(prs):
    slide = _scenario_slide(
        prs, "Google Workspace hooks",
        "“Summarise the three call documents in this Drive folder, and draft "
        "the reply to the funder's email” — the chat reaching into Drive, "
        "Docs and Gmail on its own",
        band_height=0.88,
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.34), Inches(_COL_WIDTH), Inches(1.68),
        SLATE, "Not on the free tier at the time of writing",
        ["The Drive, Docs and Gmail connections are limited or absent on the "
         "free tier — this is the clearest place the paid plans start",
         "Shown here so you recognise it in a comparison table, not because "
         "you are expected to have it"],
        line_size=12)

    template.add_detail_card(
        slide, Inches(_RIGHT_COL), Inches(2.34), Inches(_COL_WIDTH),
        Inches(1.68), LANE.color, "What you do instead",
        ["Upload the three documents to the chat, or attach them to the "
         "project's Gem once and stop attaching them",
         "The manual step is the upload; everything after it is the same"],
        line_size=12)

    template.add_band(
        slide, Inches(4.24), Inches(0.84),
        "A capability you do not have is still a capability you have to "
        "plan around",
        size=17, fill=SLATE,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.28), template.CONTENT_WIDTH,
        "Check this one before your workflow blueprint depends on it — the "
        "boundary moves",
        size=11, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Slide only, about 20 seconds — one of the demo script's batch of "
        "five (Deep Research, this, image generation, Guided Learning, "
        "saved info) that share 1.5 minutes.\n\n"
        "Show the boundary, do not mourn it. The connections are where the "
        "paid plans begin, and the workaround is the capability from four "
        "slides ago: upload the documents, or put them in the Gem once.\n\n"
        + _REVERIFY + " This is the row most likely to have changed, in "
        "either direction — if the free tier has gained a connection, "
        "say so and move the slide's framing.\n\n"
        "If someone asks whether to pay for it: not for this course. "
        "Nothing in the assignment needs it.\n\n"
        "Note for the blueprint they write this week: a manual upload step "
        "is a legitimate workflow step. It just has to be written down as "
        "one."
    ))
    return slide


# --- Image generation and editing (prepared result) --------------------------

_IMAGE_PROMPT = (
    "“A simple flow diagram for a slide: proposal → evaluation → grant "
    "agreement → reporting. Four boxes, one arrow each, no decoration, "
    "labels in English.”"
)

_IMAGE_BLOCKS = [
    ("What it is good for",
     ["The diagram a presentation needs and nobody has time to draw",
      "Editing what came back — “make the third box the widest” — instead "
      "of starting again"]),
    ("What it is not for",
     ["Anything that has to be true: it draws what a chart looks like, not "
      "your figures",
      "Faces, logos, institutional identity — none of that comes out of a "
      "generator and into an official document"]),
]


def _image_slide(prs):
    slide = _scenario_slide(
        prs, "Image generation and editing",
        "The one diagram your presentation needs — described in a sentence, "
        "adjusted in another, and dropped onto the slide",
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.28), Inches(_WIDTH), Inches(0.94),
        LANE.color, "What you type", [_IMAGE_PROMPT], line_size=12.5)

    _block_row(slide, _IMAGE_BLOCKS, 3.38, 1.52)

    template.add_band(
        slide, Inches(5.08), Inches(0.72),
        "On screen today: the diagram this prompt produced, before and "
        "after one edit",
        size=15, fill=SLATE,
    )

    template.set_notes(slide, (
        "Prepared result, about 20 seconds, still inside the script's "
        "batch of five. Have the two images side by side — the first "
        "attempt and the one after the edit.\n\n"
        "The point is the second image, not the first: you describe a "
        "change instead of redrawing. Say the edit you asked for.\n\n"
        "Then the limit, and do not soften it: it draws what a chart looks "
        "like, not your numbers. A generated illustration never carries "
        "data, and never carries the institution's identity.\n\n"
        + _REVERIFY + " Free-tier image quotas move often.\n\n"
        "If asked about attribution: the directive from Segment 2 wants AI "
        "use recorded — which tool, for what, in which part of the work. "
        "A generated illustration is part of the work."
    ))
    return slide


# --- Gemini Live and mobile (mentioned) --------------------------------------

_LIVE_BLOCKS = [
    ("Voice, both ways",
     ["Talk through your section on the way to work and get questioned on "
      "it — the rehearsal that finds the slide you cannot explain"]),
    ("Same account, same Gems",
     ["The mobile app is the same workspace: the Anchor Project Gem you "
      "built ten minutes ago is already there"]),
]


def _live_slide(prs):
    slide = _scenario_slide(
        prs, "Gemini Live and mobile",
        "Rehearse the presentation out loud, in the car or on the tram, and "
        "let it ask you the questions your audience will",
    )

    _block_row(slide, _LIVE_BLOCKS, 2.34, 1.86, line_size=12)

    template.add_band(
        slide, Inches(4.48), Inches(0.90),
        "The one capability you use with your hands full",
        size=17, fill=LANE.color,
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.58), template.CONTENT_WIDTH,
        "Voice is still an upload: what you say out loud goes to the same "
        "place a pasted document would",
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Mentioned in passing — the one capability the plan's demo script "
        "gives no time of its own, so it comes out of the segment's slack "
        "and is the first thing to drop if you are behind. Say it, do not "
        "show it: a voice demo over Teams audio is a lottery.\n\n"
        "The scenario is rehearsal: you talk, it asks. It is the cheapest "
        "way to find the section of your presentation you cannot actually "
        "explain, and the assignment ends in a presentation.\n\n"
        "Mobile parity is the second half of the sentence: same account, "
        "same Gems, so what was built on the laptop is on the phone.\n\n"
        "The caution belongs on this slide more than most: talking is "
        "uploading. The Segment 2 list applies to what you say as much as "
        "to what you paste — rehearse the presentation, not the personnel "
        "case.\n\n"
        + _REVERIFY
    ))
    return slide


# --- Guided Learning mode (slide only) ---------------------------------------

_GUIDED_PROMPT = (
    "“Teach me how indirect costs work in this funder's scheme. Do not give "
    "me the answer — take me through it, and check whether I followed.”"
)

_GUIDED_BLOCKS = [
    ("What changes",
     ["It asks you questions instead of answering yours, and stops when "
      "you have got there rather than when it has finished"]),
    ("Why it is on this list",
     ["Your deliverable is a presentation that has to produce learning "
      "outcomes. This is a worked example of the shape you are being asked "
      "to build — watch what it does with a concept, then do that"]),
]


def _guided_learning_slide(prs):
    slide = _scenario_slide(
        prs, "Guided Learning mode",
        "Learn a concept from your Anchor Project's domain the way you will "
        "have to teach it — step by step, questions first",
    )

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(2.28), Inches(_WIDTH), Inches(0.94),
        LANE.color, "What you type", [_GUIDED_PROMPT], line_size=12.5)

    _block_row(slide, _GUIDED_BLOCKS, 3.38, 1.92, line_size=12)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.52), template.CONTENT_WIDTH,
        "A concept explained to you badly is a concept you are about to "
        "explain badly",
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Slide only, about 20 seconds, and the fourth of the script's "
        "batch of five.\n\n"
        "One sentence on what the mode does — questions instead of answers "
        "— and one on why it is in a research management course: the "
        "assignment's deliverable is a presentation designed around learning "
        "outcomes, and this is that shape, modelled.\n\n"
        "Suggest it as the thing to try this week on whichever concept in "
        "their Anchor Project they understand least.\n\n"
        + _REVERIFY + " The mode has moved between a toggle and a setting "
        "more than once.\n\n"
        "The explanation is generated like any other output: check it "
        "before you teach it to anyone."
    ))
    return slide


# --- Saved info / personalisation (mentioned) --------------------------------

_SAVED_BLOCKS = [
    ("Three facts, once",
     ["Your role, your institution, the field your Anchor Project sits in — "
      "and every new chat starts from them instead of from nothing"]),
    ("The lightweight version of a Gem",
     ["Saved info follows you everywhere; a Gem is one project's workspace. "
      "Standing facts here, project context there"]),
]


def _saved_info_slide(prs):
    slide = _scenario_slide(
        prs, "Saved info — the lightweight Gem",
        "Stop opening every conversation by explaining who you are and what "
        "your office does",
    )

    _block_row(slide, _SAVED_BLOCKS, 2.34, 1.8, line_size=12)

    template.add_detail_card(
        slide, Inches(_LEFT), Inches(4.40), Inches(_WIDTH), Inches(1.06),
        SLATE, "What does not go in here",
        ["Nothing from the Segment 2 list. Saved info is stored on your "
         "personal Google account and read by every chat you open — it is "
         "the last place a colleague's name or an unsubmitted figure "
         "belongs."],
        line_size=12)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.66), template.CONTENT_WIDTH,
        "Standing context is a convenience; it is not a place to keep "
        "anything",
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "The last of the script's batch of five, about 10 seconds, and the "
        "last capability before NotebookLM.\n\n"
        "Frame it against the Gem you just built: saved info is the "
        "lightweight version — facts about you that every chat sees, rather "
        "than a workspace for one project.\n\n"
        "Spend the caution rather than the feature: it is stored on a "
        "personal account and read everywhere, so the Segment 2 list "
        "applies to it without exception.\n\n"
        + _REVERIFY + "\n\n"
        "Then close the capability half of the segment and move to "
        "NotebookLM — four minutes left, three slides."
    ))
    return slide


# --- NotebookLM: three scenarios, no walkthrough (≈4 min) -------------------

# The Lesson 3 flag, on all three NotebookLM slides in the same place, so
# nobody leaves thinking today was the NotebookLM lesson.
_LESSON_3_FLAG = (
    "The Lesson 3 tool — what it is for today, the walkthrough next week"
)


# Every NotebookLM scenario runs to two lines in the band, so the three
# slides share one band depth and one place for the Lesson 3 flag.
_NOTEBOOK_BAND_HEIGHT = 0.88


def _notebook_slide(prs, title, scenario):
    """A NotebookLM slide: the segment's scenario slide in slate rather
    than the lane's violet, under the Lesson 3 flag. The lane colour says
    "this is about the Daily Driver", and these three slides are about a
    different product the course does not open until Lesson 3, so the lane
    chip add_content_slide paints is the only violet on them. A test holds
    that."""
    slide = _scenario_slide(prs, title, scenario,
                            band_height=_NOTEBOOK_BAND_HEIGHT, fill=SLATE)
    template.add_label(
        slide, template.CONTENT_LEFT,
        Inches(1.30 + _NOTEBOOK_BAND_HEIGHT + 0.10),
        template.CONTENT_WIDTH, _LESSON_3_FLAG,
        size=11.5, color=MUTED, italic=True,
    )
    return slide


_VIDEO_BLOCKS = [
    ("What you get",
     ["The spoken hour as a text source the notebook can quote, with the "
      "point in the recording each answer came from",
      "Searchable: “what did they say about co-financing?” instead of "
      "scrubbing a timeline"]),
    ("What it needs",
     ["A public YouTube video with captions — the captions are what the "
      "notebook actually reads, so a recording without them is not a "
      "source",
      "No link goes in this deck: the scenario is described, and the "
      "recording you use on the day is your own"]),
]


def _notebook_video_slide(prs):
    slide = _notebook_slide(
        prs, "NotebookLM: a YouTube link becomes a source",
        "A funder's recorded information session on YouTube — an hour of "
        "video nobody will rewatch — turned into a text source you can "
        "question and quote",
    )

    _block_row(slide, _VIDEO_BLOCKS, 2.72, 2.26, SLATE, line_size=12)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.24), template.CONTENT_WIDTH,
        "The hour of video you could not cite becomes a source you can",
        size=12, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Scenario only, about 80 seconds. NotebookLM is next week's tool — "
        "say that first, and do not open a walkthrough today.\n\n"
        "The scenario is the recorded information session everybody saves "
        "and nobody rewatches. Added as a source, it becomes something you "
        "can ask a question of, and the answer points back at where in the "
        "recording it came from.\n\n"
        "The catch is captions: what the notebook reads is the transcript. "
        "A recording without captions is not a source.\n\n"
        "No YouTube link appears in this deck, by the course's own rule — "
        "describe the scenario, and if you want to show one, open a "
        "recording you brought yourself.\n\n"
        + _REVERIFY + " In 2026 Google folded NotebookLM into the Gemini "
        "product family, so check which of these three scenarios the free "
        "tier still covers and mark any paid-only step on the slide."
    ))
    return slide


_AGGREGATE_BLOCKS = [
    ("Four sources, one question",
     ["The call document, the funder's guidelines, the FAQ and your own "
      "notes in one notebook",
      "Ask it once — “what does eligibility actually require?” — and the "
      "answer says which of the four it came from"]),
    ("The answer to “more context is not better context”",
     ["It answers from the sources you gave it and says so, rather than "
      "from everything it has ever read",
      "Curation stops being a discipline you have to remember and becomes "
      "the shape of the tool"]),
]


def _notebook_aggregate_slide(prs):
    slide = _notebook_slide(
        prs, "NotebookLM: several documents, one notebook",
        "Everything the office holds on one call — the document, the "
        "guidelines, the FAQ and your own notes — answering as one source, "
        "with citations",
    )

    _block_row(slide, _AGGREGATE_BLOCKS, 2.72, 2.26, SLATE, line_size=12)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.22), template.CONTENT_WIDTH,
        "Source-grounded: every claim carries the document it came from, so "
        "checking it takes one click rather than one afternoon",
        size=12, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "Scenario only, about 80 seconds — the one with the strongest link "
        "back to Lesson 1.\n\n"
        "Describe the pile: four documents about one call, all of them "
        "true, none of them complete. In a notebook they answer together, "
        "and every sentence of the answer says which document it came "
        "from.\n\n"
        "Then make the Lesson 1 connection explicitly, because it closes a "
        "loop the room opened last week: “more context is not better "
        "context” was a rule they had to remember. Source grounding is that "
        "rule built into a tool — it answers from what you gave it.\n\n"
        "Do not walk through building one. Next week.\n\n"
        "The sources are documents like any other: anonymised before they "
        "go in, if they carry personal or sensitive information.\n\n"
        + _REVERIFY
    ))
    return slide


_FOLDER_BLOCKS = [
    ("What it changes",
     ["The notebook becomes the project's folder inside a conversation: "
      "the Anchor Project's sources travel with the chat",
      "Persistent context again, one level up — a Gem knows how you work, "
      "a notebook knows what you are working from"]),
    ("Check before you promise it",
     ["Google folded NotebookLM into the Gemini family in 2026 — the "
      "product itself was renamed “Gemini Notebook” in mid-2026, and the "
      "notebook-to-chat link arrived on paid plans first",
      "Any step of this that is paid-only on the day is marked on the "
      "slide before delivery"]),
]


def _notebook_folder_slide(prs):
    slide = _notebook_slide(
        prs, "NotebookLM: a notebook as the project folder",
        "Link the Anchor Project's notebook into a conversation, and stop "
        "re-uploading the same four documents every time you open one",
    )

    _block_row(slide, _FOLDER_BLOCKS, 2.72, 2.26, SLATE, line_size=12)

    template.add_band(
        slide, Inches(5.22), Inches(0.82),
        "Next week: the notebook itself. Today: what it is for",
        size=16, fill=SLATE,
    )

    template.set_notes(slide, (
        "Scenario only, about 80 seconds, and it is the bridge to Lesson 3.\n\n"
        "The scenario: the four documents you just put in a notebook, "
        "linked into a chat as the project's folder. Nothing is re-uploaded, "
        "and the conversation has the project's sources in it from the "
        "first message.\n\n"
        "Connect it back to the Gem without re-teaching either: a Gem holds "
        "how you work, a notebook holds what you work from. Both are "
        "persistent context, which is the Level 3 idea from the middle of "
        "this segment.\n\n"
        "Say the caution plainly rather than burying it: this integration "
        "appeared on paid plans first, and the product carries two names — "
        "the course says NotebookLM, the screen may say “Gemini Notebook” "
        "since the mid-2026 rename. Say which you are looking at. " + _REVERIFY + " If the link is "
        "paid-only in your account on the day, mark it on the slide and "
        "present it as where this is going, not as something they can do "
        "this week.\n\n"
        "Close the NotebookLM block here: three scenarios, no walkthrough, "
        "the tool itself is Lesson 3."
    ))
    return slide


# --- Closing: how these chain (≈30 s) ---------------------------------------

# The two chains the ticket names, each as the steps a participant would
# actually write in the assignment's blueprint. The first is the Daily
# Driver's own capabilities end to end, so it takes the lane's tint; the
# second runs through NotebookLM and stays neutral.
_CHAINS = [
    ("Upload → Gem → Canvas",
     ["Upload the anonymised call document and read the eligibility "
      "criteria out of it",
      "Put the project's standing context in a Gem, so the next chat starts "
      "where this one ended",
      "Draft the presentation in Canvas, from a workspace that already "
      "knows the project"],
     DAILY_TINT),
    ("Notebook → chat → draft",
     ["Aggregate the call's four documents in one notebook, source-grounded",
      "Link the notebook into a chat as the project's folder",
      "Draft from sources you can cite, instead of from a conversation you "
      "have to trust"],
     PANEL),
]


def _chaining_slide(prs):
    slide = template.add_content_slide(
        prs, "Chaining what you have just seen", lane=LANE)

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.30), template.CONTENT_WIDTH,
        "No single capability on its own is the interesting part. Two of "
        "them in a row, with a reason for the order, is a workflow.",
        size=13, color=MUTED,
    )

    for index, (heading, steps, fill) in enumerate(_CHAINS):
        left = _LEFT if index == 0 else _RIGHT_COL
        card = template.add_list_card(
            slide, Inches(left), Inches(1.86), Inches(_COL_WIDTH),
            Inches(2.60), fill, heading, steps, size=12.5)
        card.text_frame.margin_top = Inches(0.18)

    template.add_band(
        slide, Inches(4.70), Inches(1.02),
        "This is the assignment",
        size=21, fill=LANE.color,
        sub="Next segment: chain the tools and capabilities from both weeks "
            "into one workflow, and justify every step — which tool, why "
            "that one, and what the step before it had to produce.",
    )

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(5.94), template.CONTENT_WIDTH,
        "Level 3 was persistent context. Level 4 is orchestration — and the "
        "blueprint you write this week is its foundation.",
        size=11.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~30 seconds, and it is the handover into Segment 5. Do not add "
        "material here — this slide only names what they already watched.\n\n"
        "Walk the first chain in one breath, pointing at the three slides "
        "it came from: the upload, the Gem, Canvas. Then the second: the "
        "notebook, the chat, the draft.\n\n"
        "The sentence that matters is the one under the cards: a capability "
        "is not interesting on its own. Two in a row, with a reason for the "
        "order, is a workflow — and a reason for the order is exactly what "
        "the assignment asks them to write down.\n\n"
        "Say the level once: Level 3 was the persistent workspace, which "
        "they saw built in this segment. Level 4 is orchestration, and the "
        "blueprint is its foundation. Then hand over — the next segment has "
        "the assignment slide.\n\n"
        "If you are over time here, cut the second chain and keep the "
        "sentence."
    ))
    return slide


# --- Segment assembly --------------------------------------------------------

# Slide order: the opener, the plan's capability table row by row, the
# three NotebookLM scenarios, then the chaining close.
_BUILDERS = [
    _opener_slide,
    _upload_slide,
    _long_context_slide,
    _gems_slide,
    _deep_research_slide,
    _canvas_slide,
    _workspace_slide,
    _image_slide,
    _live_slide,
    _guided_learning_slide,
    _saved_info_slide,
    _notebook_video_slide,
    _notebook_aggregate_slide,
    _notebook_folder_slide,
    _chaining_slide,
]


def add_slides(prs):
    for builder in _BUILDERS:
        builder(prs)

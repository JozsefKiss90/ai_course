"""Segment 2 — The KM System redrawn + NotebookLM in depth (20 min,
Presentation + live facilitator demo). Daily Driver segment.

Nine slides, per lesson_3.md Segment 2: the KM System redrawn without the
wiki (sources → NotebookLM the distiller → Obsidian the source of truth,
with a person on the arrow); the four-floor map with Obsidian on the
fourth floor; what NotebookLM is (the rename said once), the free-tier
limits dated "at the time of writing"; grounding versus exploration; the
Studio outputs; the four question shapes that make a notebook answer
wiki-ready; Perplexity in passing; and the six-step demo script.

Every tool this segment demonstrates calls a cloud model on the personal
Google account, so every slide carries the Daily Driver colour; the one
green block is the vault on the KM System diagram, because Obsidian is
local. Source-separation rows used: E1, E2, E3, E4, E5, E6, T1, T2, T8,
T9, L1, A1 — attributed where the plan marks them as the speaker's.
"""

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from deck.lesson3 import template
from deck.lesson3.template import (
    DAILY_DRIVER, DAILY_TINT, HEADING_FONT, INK, LOCAL, LOCAL_TINT, MUTED,
    PANEL, SLATE, TEXT,
)

LANE = DAILY_DRIVER
_LEFT = template.CONTENT_LEFT
_WIDTH = template.CONTENT_WIDTH


# --- 1. The KM System, redrawn ---------------------------------------------


def _km_system_slide(prs):
    slide = template.add_content_slide(
        prs, "The KM System, redrawn", lane=LANE)

    template.add_band(
        slide, Inches(1.42), Inches(0.62),
        "SOURCES — anonymised or fictional Anchor Project material",
        size=14, fill=SLATE,
        sub="call text · guidelines · FAQ · own notes · public web pages · cited briefings",
    )
    template.add_label(slide, _LEFT, Inches(2.05), _WIDTH, "▼", size=13,
                       color=MUTED, align=PP_ALIGN.CENTER)

    template.add_card(
        slide, _LEFT, Inches(2.38), _WIDTH, Inches(0.9), DAILY_TINT,
        "NOTEBOOKLM — the distiller", INK,
        "Source-grounded answers with citations; briefings, mind maps, audio "
        "overviews  ·  Daily Driver",
    )

    gate = template.add_label(
        slide, _LEFT, Inches(3.32), _WIDTH,
        "▼   human-mediated: read, check against the citation, then paste — "
        "with a source line.  No automated sync.",
        size=12, color=INK, bold=True, align=PP_ALIGN.CENTER,
    )
    gate.text_frame.paragraphs[0].runs[0].font.name = HEADING_FONT

    template.add_card(
        slide, _LEFT, Inches(3.8), _WIDTH, Inches(1.25), LOCAL_TINT,
        "OBSIDIAN — the Personal Vault, the single source of truth", INK,
        "Four note types: concepts · processes · guides · projects  ·  "
        "[[links]]  ·  Graph View\n"
        "Smart Connections — related notes, local   ·   "
        "Copilot for Obsidian — ask the vault, cited answers",
    )

    template.add_detail_card(
        slide, _LEFT, Inches(5.25), Inches(5.95), Inches(1.15), SLATE,
        "Rule 1 — the arrow into the vault is a person",
        ["NotebookLM output is read, checked against its citations and then "
         "pasted, with a source line. Nothing syncs on its own."],
    )
    template.add_detail_card(
        slide, _LEFT + Inches(6.18), Inches(5.25), Inches(5.95), Inches(1.15), SLATE,
        "Rule 2 — the four entity types become the vault's four folders",
        ["What the wiki was going to hold survives unchanged; only where it "
         "lives changes."],
    )
    template.add_label(
        slide, _LEFT, Inches(6.5), _WIDTH,
        "The Lesson 1 teaser said wiki → agent → Obsidian. Perfect Wiki is a "
        "paid service, so it is out of scope for a free-tier course — and what "
        "replaces it is not another wiki but a simpler architecture.",
        size=10.5, color=MUTED, italic=True,
    )

    template.set_notes(slide, (
        "~3 min. The Lesson 1 teaser showed wiki → agent → Obsidian. The wiki "
        "is gone: Perfect Wiki is a paid service, out of scope for a free-tier "
        "course. What replaces it is not another wiki but a simpler "
        "architecture: the Personal Vault is the single source of truth, and "
        "everything else either feeds it or reads from it.\n\n"
        "Two rules travel with the diagram. First, the arrow into the vault "
        "is a person: NotebookLM output is read, checked against its "
        "citations and then pasted, with a source line. No automated sync. "
        "Second, the four entity types the wiki was going to hold — concepts, "
        "processes, guides, projects — survive as the vault's four folders, "
        "so nothing about the content model changes, only where it lives.\n\n"
        "Colour: amber is a cloud call (Daily Driver), green is local. The "
        "vault box is green because Obsidian never calls anything; the "
        "Copilot for Obsidian line inside it is the one cloud call from the "
        "vault, and it comes up in Segment 3."
    ))
    return slide


# --- 2. The four-floor map ---------------------------------------------------

# Floor 4 at the top, floor 1 at the bottom: (number, floor, job, who, tag, tint).
_FLOORS = [
    ("4", "Tools floor",
     "where the intelligence enters your documents and mail (Gemini in Google "
     "Workspace) — a paid Workspace feature, so this course puts Obsidian here: "
     "where insight becomes durable, linked work",
     "TODAY · Segment 3", LOCAL_TINT),
    ("3", "Specialist floor", "persistent roles — Gems", "Lesson 2", PANEL),
    ("2", "Frontier-model floor",
     "exploration with a large context — Gemini", "Lesson 2", PANEL),
    ("1", "Grounding floor",
     "answers only from your material — NotebookLM", "TODAY · Segment 2",
     DAILY_TINT),
]


def _four_floor_slide(prs):
    slide = template.add_content_slide(prs, "The four-floor map", lane=LANE)
    template.add_label(
        slide, _LEFT, Inches(1.3), _WIDTH,
        "A recorded talk consulted while drafting describes the Google tool "
        "family as four floors with four jobs",
        size=12, color=MUTED,
    )
    top = 1.75
    for number, floor, job, tag, tint in _FLOORS:
        template.add_badge(slide, _LEFT, Inches(top + 0.17), Inches(0.55), number)
        card = template.add_card(
            slide, _LEFT + Inches(0.7), Inches(top), Inches(9.2), Inches(0.9),
            tint, floor, INK, job,
        )
        card.text_frame.paragraphs[1].runs[0].font.size = Pt(12)
        tag_card = template.add_open_card(
            slide, _LEFT + Inches(10.05), Inches(top), Inches(2.08), Inches(0.9),
            LOCAL.color if tint == LOCAL_TINT else
            DAILY_DRIVER.color if tint == DAILY_TINT else SLATE)
        tag_card.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tag_card.text_frame.paragraphs[0].add_run()
        run.text = tag
        template.style(run, size=11, color=INK, bold=True)
        top += 1.0

    template.add_band(
        slide, Inches(5.85), Inches(0.75),
        "“The edge is never the tool, it is the system you build.”",
        size=17, sub="the one line from the talk worth keeping",
    )
    template.set_notes(slide, (
        "~1 min, one slide. Floors 2 and 3 were Lesson 2. Floor 1 is today's "
        "first half. Floor 4 is a paid Workspace feature, so this course puts "
        "Obsidian on the fourth floor instead — the second half of today.\n\n"
        "Source separation rows E1, E2, T9: the map and the closing line are "
        "the talk's framing; the plan keeps them as framing, not as facts. No "
        "link to the talk appears anywhere in the deck."
    ))
    return slide


# --- 3. NotebookLM: what it is -----------------------------------------------


def _what_it_is_slide(prs):
    slide = template.add_content_slide(
        prs, "NotebookLM (Gemini Notebook): what it is", lane=LANE)

    template.add_detail_card(
        slide, _LEFT, Inches(1.42), Inches(5.9), Inches(1.0), LANE.color,
        "Renamed, 16 July 2026",
        ["Same tool, same plans, same limits — the deck says NotebookLM from "
         "here on."],
    )
    template.add_detail_card(
        slide, _LEFT, Inches(2.55), Inches(5.9), Inches(1.45), LANE.color,
        "What it does",
        ["Answers questions only from the sources you add, and every answer "
         "carries citations to the passage it came from. The receipt comes "
         "with the answer: Lesson 1's hallucination rule, answered at tool "
         "level."],
    )
    template.add_detail_card(
        slide, _LEFT, Inches(4.13), Inches(5.9), Inches(1.2), LANE.color,
        "Routing — Daily Driver",
        ["Runs on the personal Google account: anonymised or fictional "
         "material only. The Lesson 2 “what must never enter Gemini” list "
         "applies unchanged."],
    )
    template.add_list_card(
        slide, _LEFT + Inches(6.13), Inches(1.42), Inches(6.0), Inches(3.91),
        DAILY_TINT, "What goes in",
        ["PDFs; Google Docs, Slides and Sheets; .docx",
         "Plain text and Markdown",
         "Web page URLs",
         "YouTube videos with captions",
         "Audio files; images (OCR); CSV",
         "One source: up to 500,000 words or 200 MB"],
        size=12.5,
    )
    template.add_demo_cue(
        slide,
        "steps 1–2: create the notebook, add the four sources, ask one "
        "concept question, click a citation",
        Inches(5.55), lane=LANE,
    )
    template.set_notes(slide, (
        "~3 min, with the live demo's first two steps interleaved: switch to "
        "NotebookLM in your own Google account on the fictional Anchor "
        "Project material. Create the notebook, add the four sources (call "
        "text PDF, guidelines PDF, the public FAQ page, your anonymised "
        "Markdown notes), show the source count against the 50-source limit. "
        "Then ask one concept question from the question-shape table, click "
        "through one citation to its passage, and ask a follow-up the sources "
        "do not answer — show the notebook say so instead of inventing.\n\n"
        "Say the rename once — Google renamed NotebookLM to Gemini Notebook "
        "on 16 July 2026, same tool, same plans, same limits — and then call "
        "it NotebookLM.\n\n"
        "Rows T1, T2, E3, L1: grounding is the tool-level answer to Lesson 1's "
        "hallucination point. Routing: personal Google account, so Daily "
        "Driver; anonymised or fictional material only."
    ))
    return slide


# --- 4. Free tier ------------------------------------------------------------

# The plan's free-tier table, one row each.
_LIMITS = [
    ("Sources per notebook", "50"),
    ("Notebooks", "100"),
    ("Chat questions per day", "50"),
    ("Audio / Video Overviews",
     "Included; a daily generation cap (paid tiers raise it)"),
    ("Reports", "10 a day"),
    ("Deep Research (inside a notebook)", "10 sessions a month"),
]


def _free_tier_slide(prs):
    slide = template.add_content_slide(
        prs, "Free tier at the time of writing (September 2026)", lane=LANE)
    template.add_table(
        slide, Inches(1.42), [(Inches(5.0), "Limit"), (Inches(7.13), "Free tier")],
        [[a, b] for a, b in _LIMITS], Inches(0.5), size=13, edge=LANE.color,
    )
    template.add_detail_card(
        slide, _LEFT, Inches(5.35), _WIDTH, Inches(1.2), SLATE,
        "Re-verified in the facilitator's own account the week before delivery",
        ["Source, notebook and chat limits; which Studio outputs exist; the "
         "Deep Research cap; whether notebook-to-Gem linking is on the free tier",
         "Any Studio output missing on the day is shown as a slide and marked "
         "as such"],
    )
    template.set_notes(slide, (
        "~1 min. Read the numbers as “at the time of writing”; they move. "
        "The free-tier check the week before delivery is in Materials to "
        "Prepare: re-verify every row here in your own account, and if a "
        "Studio output is missing on the day, show it as a slide and say so."
    ))
    return slide


# --- 5. Grounding versus exploration ----------------------------------------

_SITUATIONS = [
    ("1", "You are drowning in material",
     "more documents than you can hold in your head, let alone in one chat"),
    ("2", "Precision matters and “close enough” is not good enough",
     "you will act on the answer, so you need the passage it came from"),
    ("3", "The same knowledge has to move across formats",
     "a briefing for you, an audio overview for the commute, flashcards for "
     "a junior colleague"),
]


def _grounding_slide(prs):
    slide = template.add_content_slide(
        prs, "Grounding versus exploration: when to use which", lane=LANE)
    template.add_label(slide, _LEFT, Inches(1.3), _WIDTH,
                       "THREE SITUATIONS FOR THE NOTEBOOK", size=10, color=MUTED,
                       bold=True)
    left = _LEFT
    for number, lead, detail in _SITUATIONS:
        template.add_badge(slide, left, Inches(1.68), Inches(0.5), number)
        template.add_detail_card(
            slide, left + Inches(0.62), Inches(1.68), Inches(3.3), Inches(1.75),
            LANE.color, lead, [detail], heading_size=13.5, line_size=12,
        )
        left += Inches(4.07)

    template.add_band(
        slide, Inches(3.68), Inches(0.95),
        "Everything else stays in Gemini",
        size=17,
        sub="drafting, exploration, reasoning beyond the sources — anything "
            "where the answer is not in your documents",
    )
    template.add_card(
        slide, _LEFT, Inches(4.85), Inches(5.95), Inches(1.65), DAILY_TINT,
        "a notebook organises evidence; a Gem organises behaviour", INK,
        "Notebooks are the evidence counterpart to Lesson 2's Gems.",
    )
    template.add_detail_card(
        slide, _LEFT + Inches(6.18), Inches(4.85), Inches(5.95), Inches(1.65), SLATE,
        "A notebook can be handed to a Gem as its sources",
        ["This link appeared on paid plans first — re-verify whether the free "
         "tier has it before promising it (the Lesson 2 Segment 4 flag)."],
    )
    template.set_notes(slide, (
        "~2 min. The three situations come from the talk (row A1, the “action "
        "item” content minus its wrapper) and they hold up. Everything else "
        "stays in Gemini.\n\n"
        "One line for the slide: a notebook organises evidence; a Gem "
        "organises behaviour (row E6). A notebook can be given to a Gem as "
        "its sources — a link that appeared on paid plans first (row T8), so "
        "check your own free-tier account before promising it."
    ))
    return slide


# --- 6. Studio outputs -------------------------------------------------------

_STUDIO = [
    ("Chat with citations", "The core: ask, read the cited passage, decide"),
    ("Report (briefing document, study guide, FAQ, timeline; custom prompt)",
     "The vault's raw material: a briefing per concept or process, sources attached"),
    ("Mind map", "The first sketch of which notes will link to which"),
    ("Audio Overview (interactive: you can interrupt the hosts)",
     "Listen to the call's rules on the commute — the “diffuse mode” use"),
    ("Video Overview",
     "A short explainer for a colleague who will not read the call text"),
    ("Flashcards and quiz",
     "The learning-material step of the Lesson 2 blueprint, grounded in your own sources"),
    ("Deep Research (inside the notebook)",
     "Fills a gap with a cited web report that lands as a new source; 10 a "
     "month on the free tier, so write the question first"),
]


def _studio_slide(prs):
    slide = template.add_content_slide(
        prs, "Studio outputs: one notebook, many formats", lane=LANE)
    template.add_table(
        slide, Inches(1.32),
        [(Inches(4.3), "Output"), (Inches(7.83), "Use for the Anchor Project")],
        [[a, b] for a, b in _STUDIO], Inches(0.5), size=11.5, edge=LANE.color,
        row_gap=Inches(0.06),
    )
    template.add_label(
        slide, _LEFT, Inches(5.72), _WIDTH,
        "The speaker of the talk consulted argues that working memory is "
        "small, that learning happens when material moves into long-term "
        "memory, and that a notebook lets you alternate focused investigation "
        "at the desk with a “diffuse” pass away from it — the Audio Overview "
        "on the commute.",
        size=11, color=TEXT, italic=True,
    )
    template.add_demo_cue(
        slide, "steps 3–5: generate one briefing report, open the mind map, "
        "play 20 seconds of the Audio Overview", Inches(6.4), lane=LANE)
    template.set_notes(slide, (
        "~2 min, one line per row, then the attributed learning-science "
        "sentence (rows E4, E5). The talk also cites a small, preliminary MIT "
        "Media Lab EEG study on AI-assisted writing (row C1); the slide does "
        "not, because the study is not peer reviewed and the sample was 54 "
        "people. If asked, say exactly that.\n\n"
        "Live demo steps 3–5 run against this slide: generate one report "
        "(briefing document) with the process question shape and leave it on "
        "screen — it is the input to Segment 3's demo; open the mind map and "
        "point at the three or four nodes that will become linked notes; play "
        "20 seconds of the Audio Overview prepared beforehand and show the "
        "interrupt button. The demo-script slide at the end of the segment "
        "carries the timings."
    ))
    return slide


# --- 7. From notebook to note ------------------------------------------------

_SHAPES = [
    ("Concept",
     "“Define [term] as the sources use it. Give the definition, where it "
     "matters in the project, and the passages it rests on.”"),
    ("Process",
     "“List the steps of [process] in order, who does each, and the deadline "
     "or rule attached to each, citing the source for every step.”"),
    ("Guide",
     "“Write a how-to for a colleague doing [task] for the first time: "
     "prerequisites, steps, common mistakes, citing the source per step.”"),
    ("Project",
     "“Summarise the project: aim, partners (as anonymised in the sources), "
     "funding scheme, timeline, key obligations; one line per item with its "
     "citation.”"),
]


def _question_shapes_slide(prs):
    slide = template.add_content_slide(
        prs, "From notebook to note: the four question shapes",
        lane=LANE)
    template.add_table(
        slide, Inches(1.32),
        [(Inches(2.1), "Entity type"), (Inches(10.03), "Question shape, asked in the notebook")],
        [[a, b] for a, b in _SHAPES], Inches(0.74), size=12, edge=LANE.color,
    )
    template.add_band(
        slide, Inches(5.0), Inches(0.72),
        "Each answer becomes one note in the vault, with a source line: "
        "notebook name · source document · section",
        size=14,
    )
    template.add_label(
        slide, _LEFT, Inches(5.85), _WIDTH,
        "An answer without a citation does not become a note. That is Lesson "
        "1's rule — verify anything you would sign your name to — "
        "operationalised: the notebook does the citing, the person does the "
        "checking.",
        size=12, color=INK, bold=True,
    )
    template.set_notes(slide, (
        "~2 min. This is the step that makes the notebook part of a system "
        "rather than a reading aid: one question shape per entity type, and "
        "each answer becomes one note in the vault (Segment 3) with a source "
        "line — the notebook's name, the source document and, where it "
        "exists, the section.\n\n"
        "An answer without a citation does not become a note. The notebook "
        "does the citing, the person does the checking."
    ))
    return slide


# --- 8. Perplexity, in passing -----------------------------------------------


def _perplexity_slide(prs):
    slide = template.add_content_slide(prs, "Perplexity, in passing", lane=LANE)
    template.add_label(
        slide, _LEFT, Inches(1.3), _WIDTH,
        "Not a course tool and not on the KM System's path — named because "
        "you have a free account from Lesson 1 and will ask: “what if the "
        "source does not exist in my notebook yet?”",
        size=12, color=MUTED,
    )
    template.add_detail_card(
        slide, _LEFT, Inches(2.05), _WIDTH, Inches(1.05), LANE.color,
        "A search engine that answers with inline citations to current web pages",
        ["Free tier: unlimited basic cited searches, a few “Pro” searches a "
         "day. Its persistent workspaces (Spaces) are paid-only and are not "
         "used."],
    )
    template.add_detail_card(
        slide, _LEFT, Inches(3.25), Inches(5.95), Inches(1.75), SLATE,
        "For research management",
        ["A fast, cited first answer on anything current that a static "
         "document cannot hold: a call's latest amendment, a portal change, a "
         "policy update. The citations are the point; the answer is not used "
         "without opening them."],
    )
    template.add_detail_card(
        slide, _LEFT + Inches(6.18), Inches(3.25), Inches(5.95), Inches(1.75), SLATE,
        "For knowledge management",
        ["Every answer arrives with its sources, so a claim can enter the "
         "vault with its source line in one step — or better, the cited page "
         "becomes a new source in the notebook, so the notebook stays the "
         "distiller and the vault the source of truth."],
    )
    template.add_band(
        slide, Inches(5.2), Inches(1.0),
        "find → ground → keep",
        size=20, fill=LANE.color,
        sub="Perplexity (or Deep Research in the notebook) finds the source; "
            "the notebook grounds it; the vault keeps it  ·  Daily Driver  ·  "
            "anonymised or public content only",
    )
    template.set_notes(slide, (
        "~1 min, one slide, and the live demo's step 6 is this slide only — "
        "no switch to Perplexity. Two direct benefits, stated once; then "
        "where it sits in the chain: find → ground → keep. Daily Driver; "
        "anonymised or public content only."
    ))
    return slide


# --- 9. Demo script ----------------------------------------------------------

_DEMO_STEPS = [
    ("1", "Create a notebook “Anchor Project — [fictional name]”; add four "
          "sources: call text (PDF), guidelines (PDF), the programme's public "
          "FAQ page, own anonymised notes (Markdown); show the count against "
          "the 50-source limit", "1.5 min"),
    ("2", "Ask one concept question from the question-shape table; click "
          "through one citation to its passage; ask a follow-up the sources "
          "do not answer and show the notebook say so", "2 min"),
    ("3", "Generate one report (briefing document) with the process "
          "question shape; leave it on screen — the input to Segment 3's "
          "demo", "1 min"),
    ("4", "Mind map: open it, point at the three or four nodes that will "
          "become linked notes", "30 s"),
    ("5", "Audio Overview: play 20 seconds of one prepared beforehand; show "
          "the interrupt button", "1 min"),
    ("6", "Deep Research and Perplexity: slide only, the routing line "
          "find → ground → keep", "30 s"),
]


def _demo_script_slide(prs):
    slide = template.add_content_slide(
        prs, "Demo script — six steps, fictional material", lane=LANE)
    template.add_demo_cue(
        slide, "NotebookLM in the facilitator's own Google account, ≈6 of the "
        "20 minutes, interleaved with the slides", Inches(1.4), lane=LANE)
    template.add_numbered_rows(slide, _DEMO_STEPS, 2.1, 0.66, 0.58, LANE.color,
                               size=11, trailing_width=1.0)
    template.add_band(
        slide, Inches(6.12), Inches(0.62),
        "Everything on screen is fictional  ·  numbers are “at the time of "
        "writing”  ·  a missing Studio output is shown as a slide and marked",
        size=12.5, fill=SLATE,
    )
    template.set_notes(slide, (
        "The six live demo steps in one place, ≈6 minutes of the 20. They "
        "are interleaved with the slides before this one (steps 1–2 on the "
        "what-it-is slide, 3–5 on the Studio outputs slide, 6 on the "
        "Perplexity slide); this slide is the checklist if the interleaving "
        "slips.\n\n"
        "Rule stated while demoing: everything on screen is fictional; the "
        "free-tier numbers are “at the time of writing”; if a Studio output "
        "is missing from your account on the day, it is shown as a slide and "
        "marked as such."
    ))
    return slide


def add_slides(prs):
    _km_system_slide(prs)
    _four_floor_slide(prs)
    _what_it_is_slide(prs)
    _free_tier_slide(prs)
    _grounding_slide(prs)
    _studio_slide(prs)
    _question_shapes_slide(prs)
    _perplexity_slide(prs)
    _demo_script_slide(prs)

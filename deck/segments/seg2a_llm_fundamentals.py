"""Segment 2, Part A — How LLMs actually work (~10 min, Presentation).

Seven slides, one per concept, per lesson_1.md Segment 2 Part A: framing,
tokens (with live tiktokenizer demo cue), context window, system prompts,
failure modes, tools/agents foreshadow, and the three closing principles.
Wording stays at the practitioner mental-model level — no mathematics, no
engineering jargon.
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    ACCENT, HEADING_FONT, HIGHLIGHT, MUTED, PALE, PALE_WARM, PRIMARY, TEXT, WHITE,
)


def _card(slide, left, top, width, height, fill, heading, heading_color, body=None):
    """Rounded card with a bold heading and an optional body paragraph."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    template.solid(card, fill)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run = tf.paragraphs[0].add_run()
    run.text = heading
    template.style(run, size=18, color=heading_color, font=HEADING_FONT, bold=True)
    if body:
        para = tf.add_paragraph()
        para.space_before = Pt(4)
        run = para.add_run()
        run.text = body
        template.style(run, size=14, color=TEXT)
    return card


def _label(slide, left, top, width, text, size=14, color=MUTED, italic=False,
           align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, Inches(0.4))
    tf = box.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = align
    run = tf.paragraphs[0].add_run()
    template.style(run, size=size, color=color, italic=italic)
    run.text = text
    return box


def _framing_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Powerful — but weird",
        [
            "The next ten minutes: a working picture of what actually happens "
            "when you type into Gemini or Copilot — no mathematics, no engineering.",
            "These tools write like experts, yet trip over things a child finds "
            "easy. That is not a defect — it is how they are built.",
            "The quirks are not bugs to fear. They are constraints to work within.",
        ],
    )
    band = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        template.CONTENT_LEFT, Inches(4.6), template.CONTENT_WIDTH, Inches(1.4),
    )
    template.solid(band, PRIMARY)
    tf = band.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = "Once you know the quirks, you can use it for what it is:\n" \
               "a strange but powerful tool."
    template.style(run, size=20, color=WHITE, font=HEADING_FONT, bold=True)
    template.set_notes(slide, (
        "~1 min. Framing for the whole course: AI is powerful — but weird. "
        "Everyone's first weeks with these tools produce both amazement and "
        "bafflement; this segment explains the bafflement. Promise the group: "
        "no mathematics, no engineering — just the mental model practitioners "
        "actually use. The five ideas coming up: tokens, the context window, "
        "system prompts, the failure modes, and a one-minute look at where "
        "tools and agents fit. Everything here gets lived out in later "
        "lessons; today is the map, not the training."
    ))


# "O Frabjous Day!" (Jabberwocky) — 15 characters, 7 tokens. Split verified
# against both GPT tokenizers (cl100k_base and o200k_base) via tiktoken.
_FRABJOUS_CHIPS = ["O", "Fr", "ab", "j", "ous", "Day", "!"]


def _tokens_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Tokens — the model doesn't see words",
        [
            "The model never sees your words. Text is chopped into numbered "
            "fragments called tokens.",
            "Common words are a single token; rare words get split into several.",
            "Tokens are the model's real currency: usage limits and context "
            "limits count tokens, not words or pages.",
        ],
    )
    _label(slide, template.CONTENT_LEFT, Inches(3.45), Inches(5.0),
           "What the model sees:")
    x = template.CONTENT_LEFT
    top = Inches(3.9)
    for i, chip_text in enumerate(_FRABJOUS_CHIPS):
        width = Inches(0.55 + 0.16 * len(chip_text))
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top, width,
                                      Inches(0.6))
        template.solid(chip, PALE if i % 2 == 0 else PALE_WARM)
        tf = chip.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = chip_text
        template.style(run, size=18, color=PRIMARY, font=HEADING_FONT, bold=True)
        x = Inches(x.inches + width.inches + 0.12)
    _label(slide, template.CONTENT_LEFT, Inches(4.75), Inches(9.0),
           "“O Frabjous Day!” — 15 characters, but 7 tokens.", italic=True)
    template.add_demo_cue(
        slide,
        "tiktokenizer.vercel.app (1 min): paste a sentence, watch it split "
        "into tokens live",
        top=Inches(5.7),
    )
    template.set_notes(slide, (
        "~2 min. Key move: replace 'it reads my words' with 'it reads numbered "
        "fragments'. 'Frabjous' is from Lewis Carroll's Jabberwocky — a rare "
        "word, so it shatters into pieces; 'Day' stays whole. The chip split "
        "matches the real GPT tokenizer output (leading spaces omitted for "
        "display).\n\n"
        "LIVE DEMO (1 min): switch to tiktokenizer.vercel.app. Paste a plain "
        "sentence first (mostly one token per word), then 'O Frabjous Day!', "
        "then something with a long Hungarian compound word — watch it "
        "shatter. Point at the token count. Takeaway: this count is what "
        "you pay in usage limits and what fills the context window — which "
        "is the next slide."
    ))


def _context_window_slide(prs):
    slide = template.add_content_slide(
        prs,
        "The context window — a finite working memory",
        [
            "Everything you paste and everything the model answers must fit "
            "inside one hard limit: the context window.",
            "And attention sags: in a long conversation the model weighs the "
            "beginning and the end, and neglects the middle — the "
            "“lost in the middle” problem.",
        ],
    )
    _label(slide, template.CONTENT_LEFT, Inches(3.1), Inches(9.0),
           "A long conversation, as the model weighs it:")
    bar_top = Inches(3.55)
    segments = [
        ("beginning — remembered", 3.4, PRIMARY, WHITE),
        ("middle — often lost", 5.33, PALE, MUTED),
        ("end — remembered", 3.4, PRIMARY, WHITE),
    ]
    x = template.CONTENT_LEFT
    for text, width_in, fill, color in segments:
        seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, bar_top,
                                     Inches(width_in), Inches(0.55))
        template.solid(seg, fill)
        tf = seg.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = text
        template.style(run, size=13, color=color)
        x = Inches(x.inches + width_in)
    _card(
        slide, template.CONTENT_LEFT, Inches(4.5), Inches(5.96), Inches(1.75),
        PALE, "Rule 1 — Start fresh per task", PRIMARY,
        "Long chats degrade. Open a new conversation for each new task "
        "instead of continuing yesterday's thread.",
    )
    _card(
        slide, Inches(6.77), Inches(4.5), Inches(5.96), Inches(1.75),
        PALE, "Rule 2 — More context is not better context", PRIMARY,
        "Fewer, relevant tokens beat a document dump. Curate what you paste; "
        "relevance beats volume.",
    )
    template.set_notes(slide, (
        "~2 min. The working-memory analogy carries the slide: the window is "
        "finite, and even inside it, attention is uneven. If you have ever "
        "had a chatbot 'forget' an instruction from twenty messages ago — "
        "this is why, not a malfunction.\n\n"
        "Land the two rules; they are the practical payoff. Forward "
        "reference: this limit is exactly why Lesson 3's source-grounded "
        "tools (NotebookLM) exist — instead of dumping documents into a "
        "chat, you give a tool a fixed set of sources and it answers only "
        "from those."
    ))


def _system_prompts_slide(prs):
    slide = template.add_content_slide(
        prs,
        "System prompts — standing instructions",
        [
            "A conversation is really a stack of messages — with an invisible "
            "instruction sitting on top of the stack.",
            "That system prompt shapes everything the model does. When it "
            "conflicts with your request, the system usually wins.",
            "Reasoning models also “think out loud” in hidden tokens before "
            "answering — that is the pause before good answers.",
        ],
    )
    # (text, is_system) — the system message gets the navy heading treatment.
    stack = [
        ("SYSTEM PROMPT — standing instructions (you never see this)", True),
        ("You:  “Draft a partner letter for our project…”", False),
        ("AI:  (the draft)", False),
        ("You:  “Make it shorter.”", False),
    ]
    top = 3.35
    for text, is_system in stack:
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            template.CONTENT_LEFT, Inches(top), Inches(5.9), Inches(0.62),
        )
        template.solid(box, PRIMARY if is_system else PALE)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        run = tf.paragraphs[0].add_run()
        run.text = text
        template.style(run, size=13, color=WHITE if is_system else TEXT,
                       bold=is_system,
                       font=HEADING_FONT if is_system else template.BODY_FONT)
        top += 0.78
    _card(
        slide, Inches(6.9), Inches(3.7), Inches(5.83), Inches(1.9),
        PALE_WARM, "Coming in Lesson 5", HIGHLIGHT,
        "You will write a system prompt yourself. That is all a custom "
        "agent's “instructions” are — standing instructions you put on top "
        "of the stack.",
    )
    template.set_notes(slide, (
        "~2 min. Walk the stack visual top-down: the system prompt was "
        "written by the tool's maker and sits above everything you type — "
        "that is why the same question behaves differently in Gemini vs. "
        "Copilot. When your instruction fights the system's, the system "
        "usually wins.\n\n"
        "Forward reference (say it explicitly): in Lesson 5 you write the "
        "system prompt yourself — a custom agent's 'instructions' box is "
        "nothing more than this. Demystify it now, harvest it later.\n\n"
        "Reasoning models: one sentence only — some models spend hidden "
        "'thinking' tokens before answering; that is the pause, and those "
        "tokens count against limits too."
    ))


def _failure_modes_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Hallucination, sycophancy, and the cutoff",
        ["The model produces plausible text — not verified fact. "
         "Three habits to know about:"],
    )
    cards = [
        ("Hallucination",
         "Confident, fluent — and wrong. Watch numbers, citations, and "
         "names especially."),
        ("Sycophancy",
         "It would rather agree with you than push back. Ask it to "
         "challenge your draft, not to admire it."),
        ("Knowledge cutoff",
         "Its knowledge stops at a training date. Anything newer needs a "
         "searching tool — Perplexity, in Lesson 3."),
    ]
    for i, (heading, body) in enumerate(cards):
        _card(slide, Inches(template.CONTENT_LEFT.inches + i * 4.11), Inches(2.35),
              Inches(3.91), Inches(2.5), PALE, heading, PRIMARY, body)
    band = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        template.CONTENT_LEFT, Inches(5.3), template.CONTENT_WIDTH, Inches(0.9),
    )
    template.solid(band, HIGHLIGHT)
    tf = band.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = "Rule from day one: verify anything you would sign your name to."
    template.style(run, size=20, color=WHITE, font=HEADING_FONT, bold=True)
    template.set_notes(slide, (
        "~2 min. The three failure modes, briskly — each will bite someone "
        "in the cohort within weeks, so name them now. Hallucination: the "
        "model optimizes for plausible, not true; fabricated regulation "
        "numbers and citations look exactly like real ones. Sycophancy: it "
        "mirrors your framing — if you sound sure, it agrees; make it argue "
        "against you. Cutoff: this year's work programme may simply not "
        "exist for the model; Lesson 3 brings Perplexity for anything that "
        "needs current, cited sources.\n\n"
        "Close on the rule and let it land: verify anything you would sign "
        "your name to. This rule returns in every later lesson."
    ))


def _tools_agents_slide(prs):
    slide = template.add_content_slide(
        prs,
        "Tools and agents — where this is heading",
        [
            "So far, a model that only writes. Give it tools and it can act: "
            "search the web, read documents, file the result somewhere.",
            "An agent is an LLM in a loop: it chooses its own next step, uses "
            "its tools, and keeps going until the job is done.",
            "That is Level 5–6 territory on the map you are about to see — "
            "and in Lesson 5 you build your first agent, no code involved.",
        ],
    )
    _label(slide, template.CONTENT_LEFT, Inches(3.85), Inches(9.0),
           "An agent, one lap of the loop:")
    steps = ["decide the next step", "use a tool", "look at the result"]
    x = template.CONTENT_LEFT.inches
    for i, step in enumerate(steps):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(4.35), Inches(3.4),
            Inches(0.75),
        )
        template.solid(box, PALE)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        run = tf.paragraphs[0].add_run()
        run.text = step
        template.style(run, size=16, color=PRIMARY, font=HEADING_FONT, bold=True)
        x += 3.4
        if i < len(steps) - 1:
            _label(slide, Inches(x), Inches(4.5), Inches(0.7), "→", size=24,
                   color=ACCENT, align=PP_ALIGN.CENTER)
            x += 0.7
    _label(slide, template.CONTENT_LEFT, Inches(5.35), Inches(11.0),
           "⟲  …and around again, until the job is done.", italic=True)
    template.set_notes(
        slide,
        (
            "~1 min, foreshadowing only — do not dwell or demo. The point is "
            "that 'chatbot' is not the ceiling: tools let the model act, and "
            "an agent is just a model in a loop with tools. Plant the flag "
            "for Lesson 5 (participants build their first agent there — the "
            "custom agent that feeds their knowledge system) and move "
            "straight into the 7 Levels map, where levels 5–6 put this on "
            "the course arc."
        ),
    )


_PRINCIPLES = [
    ("1", "Powerful but weird",
     "The quirks are not bugs to fear but constraints to work within."),
    ("2", "If it can be done deterministically, it should be",
     "Use AI for messy, judgment-shaped work. Use a template, a spreadsheet, "
     "or a checklist for work that must come out the same every time."),
    ("3", "Fewer, better tokens win",
     "Curate what you give the model — relevance beats volume."),
]


def _principles_slide(prs):
    slide = template.add_content_slide(prs, "Three principles to keep")
    top = 1.65
    for number, principle, gloss in _PRINCIPLES:
        badge = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, template.CONTENT_LEFT, Inches(top + 0.35),
            Inches(0.85), Inches(0.85),
        )
        template.solid(badge, PRIMARY)
        tf = badge.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = number
        template.style(run, size=28, color=WHITE, font=HEADING_FONT, bold=True)
        _card(slide, Inches(1.75), Inches(top), Inches(10.98), Inches(1.55),
              PALE, principle, PRIMARY, gloss)
        top += 1.72
    template.set_notes(slide, (
        "~1 min. Say the three principles out loud — they set the tone for "
        "the whole course and get quoted back in later lessons. 1: powerful "
        "but weird — everything from the last ten minutes compressed into "
        "four words. 2: if it can be done deterministically, it should be — "
        "AI is for judgment-shaped work; identical-every-time work belongs "
        "in templates, spreadsheets, checklists. 3: fewer, better tokens "
        "win — the context-window rule as a habit; it returns in Lesson 3 "
        "with source-grounded tools and in Lesson 5 when writing agent "
        "instructions.\n\n"
        "Then bridge to Part B: 'so where is all this taking you? Here is "
        "the map' — the 7 Levels."
    ))


def add_slides(prs):
    _framing_slide(prs)
    _tokens_slide(prs)
    _context_window_slide(prs)
    _system_prompts_slide(prs)
    _failure_modes_slide(prs)
    _tools_agents_slide(prs)
    _principles_slide(prs)

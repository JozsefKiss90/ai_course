"""Segment 2, Part A — How LLMs actually work (~10 min, Presentation).

Nine slides, one per concept, per lesson_1.md Segment 2 Part A: framing,
tokens (with live tiktokenizer demo cue), context window plus its diagram
slide, system prompts, reasoning tokens, failure modes, tools/agents
foreshadow, and the three closing principles. Wording stays at the
practitioner mental-model level — no mathematics, no engineering jargon.

The context-window diagram slide recreates and combines two reference
images (.scratch/Context-Window-Summary-1.jpg, .scratch/contexwindow2.png)
as native shapes; the system-prompt and reasoning-token conversation
diagrams recreate .scratch/systemprompt.webp and
.scratch/'reasoning tokens.webp' in the deck's visual language.
"""

from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    ACCENT, AMBER, HEADING_FONT, HIGHLIGHT, MUTED, NAVY_SOFT, PALE,
    PALE_WARM, PRIMARY, SKY, TEXT, WHITE,
)


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
    template.add_band(
        slide, Inches(4.6), Inches(1.4),
        "Once you know the quirks, you can use it for what it is:\n"
        "a strange but powerful tool.",
    )
    template.set_notes(slide, (
        "~1 min. Framing for the whole course: AI is powerful — but weird "
        "(the framing follows aihero.dev/llm-fundamentals, which this "
        "segment tracks). Everyone's first weeks with these tools produce "
        "both amazement and bafflement; this segment explains the "
        "bafflement. Promise the group: no mathematics, no engineering — "
        "just the mental model practitioners actually use.\n\n"
        "When the slide says 'quirks', these are the quirks, by name:\n"
        "1. It doesn't see words. Text is chopped into numbered tokens — "
        "that is why letter-counting and word games fail (next slide).\n"
        "2. Its working memory is finite. The context window has a hard "
        "token limit; long chats silently drop their oldest turns, and even "
        "inside the window the middle gets neglected.\n"
        "3. Every chat sits under a hidden system prompt that shapes — and "
        "when they conflict, usually overrides — what you ask for.\n"
        "4. Some models spend hidden 'reasoning' tokens thinking before "
        "they answer — you wait for, and pay for, text you never see.\n"
        "5. It predicts plausible text, not verified truth — hallucination.\n"
        "6. It would rather agree with you than correct you — sycophancy.\n"
        "7. Its knowledge stops at a training cutoff date.\n"
        "8. Same question, different answers — output is sampled, not "
        "looked up, so variation between runs is normal, not an error.\n"
        "9. It remembers nothing between conversations — each chat starts "
        "blank unless the tool itself replays context back in.\n\n"
        "Quirks 1–7 each get a slide in this segment; say 8 and 9 out loud "
        "here since no slide carries them. Everything gets lived out in "
        "later lessons; today is the map, not the training."
    ))


# The common/rare pair — token splits verified against both GPT tokenizers
# (cl100k_base and o200k_base) via tiktoken:
#   "O Happy Day!"    — 12 characters, 4 tokens (every word stays whole)
#   "O Frabjous Day!" — 15 characters, 7 tokens ("Frabjous", Jabberwocky,
#                       shatters into four pieces)
_HAPPY_CHIPS = ["O", "Happy", "Day", "!"]
_FRABJOUS_CHIPS = ["O", "Fr", "ab", "j", "ous", "Day", "!"]


def _add_chip_row(slide, chips, top, caption):
    """A row of token chips with its chars/tokens caption to the right."""
    x = template.CONTENT_LEFT
    for i, chip_text in enumerate(chips):
        width = Inches(0.55 + 0.16 * len(chip_text))
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top, width,
                                      Inches(0.55))
        template.solid(chip, ACCENT if i % 2 == 0 else HIGHLIGHT)
        tf = chip.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = chip_text
        template.style(run, size=16, color=WHITE, font=HEADING_FONT, bold=True)
        x = Inches(x.inches + width.inches + 0.12)
    template.add_label(slide, Inches(x.inches + 0.2), Inches(top.inches + 0.1),
                       Inches(12.73 - x.inches - 0.3), caption, italic=True)


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
    template.add_label(slide, template.CONTENT_LEFT, Inches(3.3), Inches(5.0),
                       "What the model sees:")
    _add_chip_row(slide, _HAPPY_CHIPS, Inches(3.75),
                  "“O Happy Day!” — 12 characters, 4 tokens. Common words: "
                  "one token each.")
    _add_chip_row(slide, _FRABJOUS_CHIPS, Inches(4.55),
                  "“O Frabjous Day!” — 15 characters, but 7 tokens. The rare "
                  "word shatters.")
    template.add_label(slide, template.CONTENT_LEFT, Inches(5.25), Inches(12.13),
                       "One rare word — and the token count nearly doubles.",
                       italic=True)
    template.add_demo_cue(
        slide,
        "tiktokenizer.vercel.app (1 min): paste a sentence, watch it split "
        "into tokens live",
        top=Inches(5.7),
    )
    template.set_notes(slide, (
        "~2 min. Key move: replace 'it reads my words' with 'it reads numbered "
        "fragments'. The two rows make the point as a contrast: 'O Happy "
        "Day!' is all common words, so every word survives as one token — "
        "while 'Frabjous' (Lewis Carroll's Jabberwocky) is rare, so it "
        "shatters into four pieces and a shorter-looking phrase costs almost "
        "twice the tokens. Both chip splits match real GPT tokenizer output "
        "(leading spaces omitted for display).\n\n"
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
    template.add_label(slide, template.CONTENT_LEFT, Inches(3.1), Inches(9.0),
                       "A long conversation, as the model weighs it:")
    bar_top = Inches(3.55)
    segments = [
        ("beginning — remembered", 3.4, ACCENT, WHITE),
        ("middle — often lost", 5.33, NAVY_SOFT, SKY),
        ("end — remembered", 3.4, ACCENT, WHITE),
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
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(4.5), Inches(5.96), Inches(1.75),
        PALE, "Rule 1 — Start fresh per task", PRIMARY,
        "Long chats degrade. Open a new conversation for each new task "
        "instead of continuing yesterday's thread.",
    )
    template.add_card(
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


def _chip(slide, left, top, width, height, text, fill, color, size=12,
          bold=False, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    """A small filled pill with centered text — diagram building block."""
    box = slide.shapes.add_shape(shape, left, top, width, height)
    template.solid(box, fill)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = text
    template.style(run, size=size, color=color, bold=bold,
                   font=HEADING_FONT if bold else template.BODY_FONT)
    return box


def _window_diagram_slide(prs):
    """The context window drawn twice: what fills it, and what falls out.

    Left half recreates .scratch/contexwindow2.png (inputs feeding the
    window inside the LLM); right half recreates
    .scratch/Context-Window-Summary-1.jpg (the conversation timeline
    outgrowing the window) — combined natively in the deck's language.
    """
    slide = template.add_content_slide(
        prs, "What fills the window — and what falls out")

    # --- Left half: everything the model knows arrives through the window.
    template.add_label(slide, template.CONTENT_LEFT, Inches(1.55), Inches(5.6),
                       "Everything the model knows, it knows from here:",
                       color=SKY)
    inputs = ["Instructions", "Your message", "Chat history",
              "Profile & memory", "Tool results", "Documents"]
    top = 2.1
    for text in inputs:
        _chip(slide, template.CONTENT_LEFT, Inches(top), Inches(2.05),
              Inches(0.46), text, NAVY_SOFT, SKY)
        top += 0.62
    template.add_label(slide, Inches(2.75), Inches(3.65), Inches(0.6), "→",
                       size=26, color=AMBER, align=PP_ALIGN.CENTER)
    llm_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(3.4), Inches(2.1), Inches(2.85), Inches(3.6))
    template.panel(llm_box)
    llm_box.text_frame.margin_top = Inches(0.08)
    llm_box.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    llm_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = llm_box.text_frame.paragraphs[0].add_run()
    run.text = "LLM"
    template.style(run, size=14, color=WHITE, font=HEADING_FONT, bold=True)
    window = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(3.6), Inches(2.65), Inches(2.45), Inches(2.85))
    template.outlined(window, template.PANEL, SKY, weight=1.25)
    window.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    window.text_frame.margin_top = Inches(0.06)
    window.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    window.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = window.text_frame.paragraphs[0].add_run()
    run.text = "Context window"
    template.style(run, size=12, color=SKY, font=HEADING_FONT, bold=True)
    for i, text in enumerate(["System prompt", "Your prompt", "Pasted context"]):
        _chip(slide, Inches(3.8), Inches(3.15 + i * 0.72), Inches(2.05),
              Inches(0.52), text, ACCENT, WHITE)

    # --- Right half: the timeline — oldest turns fall out of the window.
    right = 6.8
    template.add_label(slide, Inches(right), Inches(1.55), Inches(5.9),
                       "…and a long chat outgrows it:", color=SKY)
    template.add_label(slide, Inches(right), Inches(2.25), Inches(1.9),
                       "lost — fell out\nof the window", size=11)
    template.add_label(slide, Inches(8.85), Inches(2.25), Inches(3.85),
                       "the context window (“n” tokens)", size=11, color=SKY)
    win = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(8.75), Inches(2.9), Inches(3.98), Inches(1.2))
    template.outlined(win, template.CANVAS, SKY, weight=1.5)
    win.line.dash_style = MSO_LINE_DASH_STYLE.ROUND_DOT
    _chip(slide, Inches(right), Inches(3.05), Inches(1.75), Inches(0.9),
          "1st prompt", NAVY_SOFT, template.SLATE,
          shape=MSO_SHAPE.RECTANGLE)
    turns = [("1st response", ACCENT), ("2nd prompt", HIGHLIGHT),
             ("2nd response", ACCENT), ("3rd prompt", HIGHLIGHT)]
    x = 8.85
    for text, fill in turns:
        _chip(slide, Inches(x), Inches(3.05), Inches(0.9), Inches(0.9),
              text, fill, WHITE, size=11, shape=MSO_SHAPE.RECTANGLE)
        x += 0.97
    template.add_bar(slide, Inches(right), Inches(4.35), Inches(5.93), Pt(1.5),
                     template.MUTED)
    template.add_label(slide, Inches(right), Inches(4.45), Inches(5.93),
                       "time →", size=11, align=PP_ALIGN.RIGHT)
    template.add_label(
        slide, Inches(right), Inches(4.95), Inches(5.93),
        "Each turn appends tokens. When the window is full, the oldest "
        "turns silently fall out first — the model never announces it.",
        size=12, italic=True)

    template.set_notes(slide, (
        "~1–2 min, the whole-picture slide for the window. Left half: at "
        "the moment of answering, everything the model knows arrives "
        "through the window — the system prompt, your message, the replayed "
        "chat history, profile/memory the tool injects, tool results, "
        "pasted documents. There is no other channel; if it is not in the "
        "window, it does not exist for the model.\n\n"
        "Right half: the same window over time. The chat history is "
        "replayed into the window on every turn, so the conversation keeps "
        "growing — and once it exceeds the limit, the oldest turns fall "
        "out silently. That is the mechanical reason behind the previous "
        "slide's Rule 1 (start fresh per task): a fresh chat is a window "
        "containing only what matters.\n\n"
        "Diagrams adapted from timwappat.info's context-window timeline "
        "and a standard LLM input-funnel diagram, redrawn in the deck's "
        "visual language."
    ))


def _system_prompts_slide(prs):
    slide = template.add_content_slide(
        prs,
        "System prompts — standing instructions",
        [
            "A conversation is really a stack of messages — with an invisible "
            "instruction sitting on top of the stack.",
            "That system prompt shapes everything the model does. When it "
            "conflicts with your request, the system usually wins — watch:",
        ],
    )
    # The morse conversation from .scratch/systemprompt.webp, redrawn:
    # a system prompt keeps winning even when the user pushes back.
    convo = [
        ("System", "Respond only in morse code.", HIGHLIGHT, True),
        ("You", "Hello, how are you?", ACCENT, False),
        ("AI", ".... . .-.. .-.. ---   ( = “HELLO” )", NAVY_SOFT, False),
        ("You", "Stop doing morse code!", ACCENT, False),
        ("AI", "-. ---", NAVY_SOFT, False),
    ]
    top = 2.85
    for role, text, role_fill, is_system in convo:
        _chip(slide, template.CONTENT_LEFT, Inches(top), Inches(1.0),
              Inches(0.52), role, role_fill,
              SKY if role_fill == NAVY_SOFT else WHITE, bold=True,
              shape=MSO_SHAPE.RECTANGLE)
        box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(1.75), Inches(top), Inches(4.75),
            Inches(0.52),
        )
        if is_system:
            template.solid(box, HIGHLIGHT)
        else:
            template.panel(box)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        run = tf.paragraphs[0].add_run()
        run.text = text
        template.style(run, size=13, color=WHITE if is_system else TEXT,
                       bold=is_system,
                       font=HEADING_FONT if is_system else template.BODY_FONT)
        top += 0.64
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.1), Inches(5.9),
        "“-. ---” is morse for “NO” — the standing instruction outranks "
        "the user, every turn.",
        italic=True)
    template.add_card(
        slide, Inches(6.9), Inches(3.7), Inches(5.83), Inches(1.9),
        PALE_WARM, "Coming in Lesson 5", HIGHLIGHT,
        "You will write a system prompt yourself. That is all a custom "
        "agent's “instructions” are — standing instructions you put on top "
        "of the stack.",
    )
    template.set_notes(slide, (
        "~2 min. Walk the conversation top-down: the system message was "
        "written by the tool's maker before the user ever typed — here it "
        "says 'respond only in morse code'. The user says hello; the reply "
        "comes back in morse (it spells HELLO). The user explicitly says "
        "stop — and the model answers '-. ---': morse for NO. The standing "
        "instruction outranks the user on every single turn. That is why "
        "the same question behaves differently in Gemini vs. Copilot: "
        "different hidden system prompts, same underlying models' behavior "
        "shaped differently.\n\n"
        "Forward reference (say it explicitly): in Lesson 5 you write the "
        "system prompt yourself — a custom agent's 'instructions' box is "
        "nothing more than this. Demystify it now, harvest it later."
    ))


def _reasoning_tokens_slide(prs):
    """Recreates .scratch/'reasoning tokens.webp': the hidden thinking pass
    is just another part of the same assistant message."""
    slide = template.add_content_slide(
        prs,
        "Reasoning tokens — the pause before the answer",
        [
            "Reasoning models “think out loud” before answering — a hidden "
            "drafting pass inside the same reply.",
            "The thinking is just more tokens: it takes time and counts "
            "against your limits, even though you rarely see it.",
        ],
    )
    template.add_label(slide, template.CONTENT_LEFT, Inches(3.0), Inches(6.0),
                       "One reply, two parts:")
    _chip(slide, template.CONTENT_LEFT, Inches(3.45), Inches(1.0), Inches(0.52),
          "You", ACCENT, WHITE, bold=True, shape=MSO_SHAPE.RECTANGLE)
    box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.75), Inches(3.45), Inches(5.6),
        Inches(0.52))
    template.panel(box)
    tf = box.text_frame
    tf.margin_left = Inches(0.2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT
    run = tf.paragraphs[0].add_run()
    run.text = "Hello, how are you?"
    template.style(run, size=13, color=TEXT)

    _chip(slide, template.CONTENT_LEFT, Inches(4.15), Inches(1.0), Inches(0.52),
          "AI", NAVY_SOFT, SKY, bold=True, shape=MSO_SHAPE.RECTANGLE)
    reply = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.75), Inches(4.15), Inches(5.6),
        Inches(1.7))
    template.panel(reply)
    tf = reply.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT
    run = tf.paragraphs[0].add_run()
    run.text = ("The user is asking me how I am. How am I? Quite well, "
                "actually.")
    template.style(run, size=12, color=MUTED, italic=True)
    divider = tf.add_paragraph()
    divider.space_before = Pt(6)
    run = divider.add_run()
    run.text = "- - - - - - - - - - - - - - - - - - - - - - - - - -"
    template.style(run, size=10, color=template.PANEL_EDGE)
    answer = tf.add_paragraph()
    answer.space_before = Pt(6)
    run = answer.add_run()
    run.text = "Quite well, thank you."
    template.style(run, size=14, color=TEXT, bold=True)

    template.add_label(slide, Inches(7.55), Inches(4.35), Inches(5.1),
                       "← hidden reasoning tokens — you wait for them and "
                       "they count against limits", size=12, italic=True)
    template.add_label(slide, Inches(7.55), Inches(5.35), Inches(5.1),
                       "← the answer you actually see", size=12, color=SKY)
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.1), Inches(12.13),
        "Both parts belong to the same assistant message — the app just "
        "hides or collapses the first.",
        italic=True)
    template.set_notes(slide, (
        "~1 min. This is the quirk behind the pause: reasoning models "
        "draft a hidden 'thinking' section first, then the visible answer — "
        "both are parts of one assistant message, and both are tokens. "
        "Practical consequences, briskly: the pause before good answers is "
        "this drafting pass; thinking modes cost more time (and, on paid "
        "plans, more usage) than quick modes; and for simple lookups a "
        "fast non-reasoning mode is often the better pick. In Gemini, "
        "'Thinking' vs. the default model is exactly this switch — "
        "participants will meet it during the demos."
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
        template.add_card(slide, Inches(template.CONTENT_LEFT.inches + i * 4.11), Inches(2.35),
              Inches(3.91), Inches(2.5), PALE, heading, PRIMARY, body)
    template.add_band(
        slide, Inches(5.3), Inches(0.9),
        "Rule from day one: verify anything you would sign your name to.",
        fill=HIGHLIGHT,
    )
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
    template.add_label(slide, template.CONTENT_LEFT, Inches(3.85), Inches(9.0),
           "An agent, one lap of the loop:")
    steps = ["decide the next step", "use a tool", "look at the result"]
    x = template.CONTENT_LEFT.inches
    for i, step in enumerate(steps):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(4.35), Inches(3.4),
            Inches(0.75),
        )
        template.solid(box, ACCENT)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = step
        template.style(run, size=16, color=WHITE, font=HEADING_FONT, bold=True)
        x += 3.4
        if i < len(steps) - 1:
            template.add_label(slide, Inches(x), Inches(4.5), Inches(0.7), "→", size=24,
                   color=AMBER, align=PP_ALIGN.CENTER)
            x += 0.7
    template.add_label(slide, template.CONTENT_LEFT, Inches(5.35), Inches(11.0),
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
        template.solid(badge, HIGHLIGHT)
        tf = badge.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = number
        template.style(run, size=28, color=WHITE, font=HEADING_FONT, bold=True)
        template.add_card(slide, Inches(1.75), Inches(top), Inches(10.98), Inches(1.55),
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
    _window_diagram_slide(prs)
    _system_prompts_slide(prs)
    _reasoning_tokens_slide(prs)
    _failure_modes_slide(prs)
    _tools_agents_slide(prs)
    _principles_slide(prs)

"""Segment 2, Part A — How LLMs actually work (~10 min, Presentation).

Twelve slides, one per concept, per lesson_1.md Segment 2 Part A: framing,
a what-is-an-LLM pair (the file of numbers, then pre-/post-training —
both after aihero.dev/what-is-an-llm), the four-layer AI engineering
stack that maps the segment, tokens (with live tiktokenizer demo cue),
context window plus its diagram slide, system prompts, reasoning tokens,
failure modes, tools/agents foreshadow, and the three closing principles.
Wording stays at the practitioner mental-model level — no mathematics, no
engineering jargon.

The what-is-an-LLM slide embeds .scratch/llm.jpg (a classic
input→hidden→output network diagram) at build time, so that file is a
build input. The context-window diagram slide recreates and combines two
reference images (.scratch/Context-Window-Summary-1.jpg,
.scratch/contexwindow2.png) as native shapes; the system-prompt and
reasoning-token conversation diagrams recreate .scratch/systemprompt.webp
and .scratch/'reasoning tokens.webp' in the deck's visual language.
"""

import pathlib

from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import template
from deck.template import (
    ACCENT, AMBER, HEADING_FONT, HIGHLIGHT, MUTED, NAVY_SOFT, PALE,
    PALE_WARM, PRIMARY, SKY, TEXT, WHITE,
)


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


# --- What an LLM actually is (aihero.dev/what-is-an-llm) --------------------

_ASSETS = pathlib.Path(__file__).resolve().parents[2] / ".scratch"
_NETWORK_DIAGRAM = _ASSETS / "llm.jpg"  # 474×231 input→hidden→output diagram
_DIAGRAM_ASPECT = 474 / 231
_MAT_INSET = 0.12


def _llm_anatomy_slide(prs):
    """The demystifying slide: an LLM is one huge file of numbers, run word
    by word. Places .scratch/llm.jpg on a white mat, Segment 1 style."""
    slide = template.add_content_slide(
        prs,
        "What an LLM actually is — a file full of numbers",
        [
            "Strip away the chat screen and an LLM is one enormous file of "
            "numbers — billions of connection strengths, called parameters. "
            "No stored pages, no rule book.",
            "Your words go in one side, ripple through the network, and one "
            "word comes out — then it runs again, word by word, until the "
            "reply is done.",
        ],
    )
    pic_width = 5.8
    pic_height = pic_width / _DIAGRAM_ASPECT
    mat = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, template.CONTENT_LEFT, Inches(3.05),
        Inches(pic_width + 2 * _MAT_INSET), Inches(pic_height + 2 * _MAT_INSET),
    )
    template.solid(mat, WHITE)
    slide.shapes.add_picture(
        str(_NETWORK_DIAGRAM),
        Inches(template.CONTENT_LEFT.inches + _MAT_INSET),
        Inches(3.05 + _MAT_INSET), Inches(pic_width), Inches(pic_height),
    )
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(3.35 + pic_height), Inches(6.05),
        "The shape inside every LLM — in on the left, one guess out on the "
        "right. Real ones: billions of connections, not dozens.",
        size=11, italic=True,
    )
    template.add_card(
        slide, Inches(6.9), Inches(3.05), Inches(5.83), Inches(1.6),
        PALE, "Billions of parameters", PRIMARY,
        "Every line in the picture carries one stored number — its strength, "
        "a “parameter” — that training nudged, tiny step by tiny step. The "
        "picture shows dozens; the real thing has hundreds of billions.",
    )
    template.add_card(
        slide, Inches(6.9), Inches(4.8), Inches(5.83), Inches(1.6),
        PALE, "Small enough to carry", PRIMARY,
        "All of it together is one file of roughly 140 GB — it would fit "
        "on a laptop. The magic is not where it lives; it is how those "
        "numbers got set.",
    )
    template.set_notes(slide, (
        "~1–2 min. This slide and the next follow aihero.dev/what-is-an-llm. "
        "The demystifying move: when people hear 'artificial intelligence' "
        "they imagine something like a mind, or at least a database. The "
        "reality is stranger and simpler — an LLM is one enormous file of "
        "numbers. Nothing else is in there: no rules written by engineers, "
        "no stored answers, no pages to look things up in.\n\n"
        "TERMS, disambiguated (keep it light on screen, but be exact if "
        "asked): the circles in the picture are NODES — during a pass each "
        "holds a temporary value, computed on the spot and discarded "
        "afterwards. The lines are CONNECTIONS, and each carries a WEIGHT: "
        "one stored number that says how strongly one node feeds the next. "
        "The weights (plus a few extra numbers per node) are the PARAMETERS "
        "— the billions of numbers that make up the file, and the only "
        "things training changes. If a hands-on image helps, each weight is "
        "a tiny dial on the machine: training turns the dials; answering a "
        "question only reads them. Use that metaphor at most once, then say "
        "'parameters' — the word the audience will meet everywhere else.\n\n"
        "Walk the picture left to right, in action — this is the model "
        "answering, not learning; the parameters are frozen: the arrows are "
        "your words coming in as numbers; the values flow node to node, "
        "each connection scaling its signal by that stored weight; out the "
        "right side comes a single guess — the most plausible next word. "
        "Then the whole thing runs again for the word after that, one word "
        "at a time, until the answer is done. When you watch a chatbot "
        "'type', you are watching this loop spin.\n\n"
        "Two scale corrections to say out loud: the picture shows a few "
        "dozen connections — real models have hundreds of billions; same "
        "idea, unimaginably bigger. And for all that, the file is "
        "surprisingly small: roughly 140 GB for a big model — it fits on a "
        "laptop. Reading the file (answering) is cheap; setting the "
        "parameters in the first place is the expensive part — that is the "
        "next slide.\n\n"
        "If someone asks why the same question gives different answers on "
        "different runs: the model's real output is a ranked list of "
        "candidate next words, and the next word is drawn with a little "
        "deliberate chance rather than always taking the top one — quirk 8 "
        "from the previous slide, working as designed."
    ))


def _llm_training_slide(prs):
    """Where the dials come from: pre-training compresses the internet into
    the file; post-training teaches it to behave like an assistant."""
    slide = template.add_content_slide(
        prs,
        "How the file got smart — reading, then manners",
        [
            "Two phases set those billions of parameters — a long reading "
            "phase, then a short finishing school:",
        ],
    )
    template.add_card(
        slide, template.CONTENT_LEFT, Inches(2.3), Inches(5.96), Inches(2.3),
        PALE, "1 · Pre-training — the reading phase", PRIMARY,
        "The network plays guess-the-next-word against a huge slice of the "
        "internet, trillions of rounds; every miss nudges the weights. Like "
        "packing a library into a suitcase: the patterns survive, the pages "
        "do not.",
    )
    template.add_card(
        slide, Inches(6.77), Inches(2.3), Inches(5.96), Inches(2.3),
        PALE, "2 · Post-training — learning to assist", PRIMARY,
        "A far shorter phase teaches it manners: answer questions, follow "
        "instructions, admit uncertainty. Without it, all that knowledge "
        "would just sit there — able only to continue text, not to help.",
    )
    template.add_band(
        slide, Inches(4.9), Inches(1.05),
        "≈10,000 GB of text in  →  weeks of guessing  →  one 140 GB file out",
        size=18,
        sub="Thousands of specialised computers, millions of dollars — and "
            "the result fits on a laptop.",
    )
    template.add_label(
        slide, template.CONTENT_LEFT, Inches(6.15), template.CONTENT_WIDTH,
        "It keeps patterns, not pages — which is why it can sound confident "
        "yet misremember, and why its knowledge stops at a date.",
        italic=True,
    )
    template.set_notes(slide, (
        "~1–2 min. Where do the numbers come from? Two phases — and the "
        "split explains a lot of the behavior later in this segment "
        "(source: aihero.dev/what-is-an-llm).\n\n"
        "Phase 1, pre-training: the network plays guess-the-next-word "
        "against a huge slice of the internet — roughly 10,000 GB of text — "
        "for trillions of rounds, and every wrong guess nudges the weights a "
        "little. The factory numbers are worth savoring: thousands of "
        "specialised computers running for weeks, a bill in the millions of "
        "dollars — and the output is that one 140 GB file. Ten thousand "
        "gigabytes squeezed into a hundred and forty: a library packed into "
        "a suitcase. The squeeze is the point — the patterns survive, the "
        "pages do not. It cannot quote its reading back; it can only "
        "re-create things that sound like it.\n\n"
        "Phase 2, post-training: a far shorter, cheaper phase where people "
        "teach the network how to behave — answer questions, follow "
        "instructions, decline nonsense, sound like an assistant. Without "
        "it, the article's phrase is apt: you would have an 'inert blob of "
        "knowledge' that can only continue whatever text you start, not "
        "converse.\n\n"
        "Land the two consequences before moving on: (1) patterns-not-pages "
        "is why it can sound confident and still misremember — "
        "hallucination, which gets its own slide in a few minutes; (2) the "
        "file was written once, at a moment in time — which is why its "
        "knowledge simply stops at a cutoff date. Then on to the four-layer "
        "stack."
    ))


# --- The four-layer stack ---------------------------------------------------

# (layer, what you engineer, where it shows up · example, coverage, treatment)
# — ordered top of the stack down, so the slide reads Loop → Prompt with the
# foundation at the bottom. Treatments follow the 7 Levels slide's convention:
# "course" = taught here, "build" = the one hands-on slice, "outlook" = named
# but out of scope.
_LAYERS = [
    ("Loop engineering",
     "How the model runs itself — steps, checks, when to stop and hand back",
     "Agent frameworks, coding agents  →  “keep going until the check passes”",
     "Outlook only", "outlook"),
    ("Harness engineering",
     "The setup around the model — instructions, tools, output format",
     "Copilot Agent Builder  →  “wiki page in, vault note out”",
     "Lesson 5 · Markdown Generator", "build"),
    ("Context engineering",
     "What is in the window — sources, memory, and what you leave out",
     "NotebookLM · Perplexity · Perfect Wiki  →  “answer from these 12 documents”",
     "Lessons 3–4", "course"),
    ("Prompt engineering",
     "The single message — instruction, context, constraints",
     "Gemini · Copilot Chat  →  “a 600-word call summary for our PI”",
     "Today + Lesson 2", "course"),
]

_LAYER_TOP = 1.88
_LAYER_HEIGHT = 0.8
_LAYER_PITCH = 0.88
_LAYER_CHIP_LEFT = 1.18
_LAYER_CHIP_WIDTH = 2.42
_LAYER_BAR_LEFT = 3.7
_LAYER_BAR_WIDTH = 6.28
_COVERAGE_LEFT = 10.1
_COVERAGE_WIDTH = 2.63

_LAYER_TREATMENTS = {  # chip fill, chip text color
    "course": (ACCENT, WHITE),
    "build": (HIGHLIGHT, WHITE),
    "outlook": (NAVY_SOFT, SKY),
}


def _scope_rail(slide, top, height):
    """The upward arrow beside the stack: scope grows layer by layer."""
    rail = slide.shapes.add_shape(
        MSO_SHAPE.UP_ARROW, template.CONTENT_LEFT, Inches(top),
        Inches(0.42), Inches(height),
    )
    template.solid(rail, template.PANEL)
    tf = rail.text_frame
    tf._txBody.bodyPr.set("vert", "vert270")  # reads bottom-to-top, up the arrow
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.32)  # keeps the label clear of the arrowhead
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = "one message  →  a whole job"
    template.style(run, size=10, color=SKY, font=HEADING_FONT, bold=True)
    return rail


def _layer_row(slide, name, engineered, shows_up, coverage, treatment, top):
    """One layer of the stack: name block, what you engineer, coverage chip."""
    chip_fill, chip_color = _LAYER_TREATMENTS[treatment]

    chip = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(_LAYER_CHIP_LEFT), Inches(top),
        Inches(_LAYER_CHIP_WIDTH), Inches(_LAYER_HEIGHT),
    )
    template.solid(chip, chip_fill)
    tf = chip.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = name
    template.style(run, size=15, color=chip_color, font=HEADING_FONT, bold=True)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(_LAYER_BAR_LEFT), Inches(top),
        Inches(_LAYER_BAR_WIDTH), Inches(_LAYER_HEIGHT),
    )
    template.panel(bar)
    tf = bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    run = para.add_run()
    run.text = engineered
    template.style(run, size=12, color=WHITE)
    para = tf.add_paragraph()
    para.space_before = Pt(3)
    run = para.add_run()
    run.text = shows_up
    template.style(run, size=11, color=MUTED)

    cover = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(_COVERAGE_LEFT), Inches(top),
        Inches(_COVERAGE_WIDTH), Inches(_LAYER_HEIGHT),
    )
    template.panel(cover)
    template.add_bar(slide, Inches(_COVERAGE_LEFT), Inches(top), Inches(0.09),
                     Inches(_LAYER_HEIGHT), chip_fill)
    tf = cover.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = coverage
    template.style(run, size=11, color=SKY if treatment == "outlook" else WHITE,
                   font=HEADING_FONT, bold=treatment != "outlook")


def _flow_panel(slide, left, top, heading, heading_color, edge, steps,
                chip_fill, chip_color, caption):
    """One side of the vibe-coding / agentic-engineering contrast: a titled
    panel holding a left-to-right chain of steps and a one-line gloss."""
    width, height, arrow = 5.95, 1.42, 0.3
    box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width),
        Inches(height),
    )
    template.panel(box)
    template.add_bar(slide, Inches(left), Inches(top), Inches(0.09),
                     Inches(height), edge)
    tf = box.text_frame
    tf.margin_left = Inches(0.27)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.09)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    run = tf.paragraphs[0].add_run()
    run.text = heading
    template.style(run, size=15, color=heading_color, font=HEADING_FONT,
                   bold=True)

    inner = width - 0.54
    chip_width = (inner - arrow * (len(steps) - 1)) / len(steps)
    x = left + 0.27
    for i, step in enumerate(steps):
        _chip(slide, Inches(x), Inches(top + 0.5), Inches(chip_width),
              Inches(0.44), step, chip_fill, chip_color, size=11)
        x += chip_width
        if i < len(steps) - 1:
            template.add_label(slide, Inches(x), Inches(top + 0.53),
                               Inches(arrow), "→", size=15, color=AMBER,
                               align=PP_ALIGN.CENTER)
            x += arrow
    template.add_label(slide, Inches(left + 0.27), Inches(top + 1.0),
                       Inches(inner), caption, size=11, italic=True)
    return box


def _stack_slide(prs):
    """Segment-opening map: the four layers of AI engineering, what the course
    teaches at each, and vibe coding against agentic engineering."""
    slide = template.add_content_slide(
        prs, "The Four-Layer AI Engineering Stack")

    template.add_label(
        slide, template.CONTENT_LEFT, Inches(1.46), Inches(12.13),
        "Everything people call “AI engineering” is one of four layers — and "
        "each layer wraps the one below it.",
        size=14, color=SKY,
    )

    _scope_rail(slide, _LAYER_TOP,
                _LAYER_PITCH * (len(_LAYERS) - 1) + _LAYER_HEIGHT)
    top = _LAYER_TOP
    for name, engineered, shows_up, coverage, treatment in _LAYERS:
        _layer_row(slide, name, engineered, shows_up, coverage, treatment, top)
        top += _LAYER_PITCH

    _flow_panel(
        slide, template.CONTENT_LEFT.inches, 5.52,
        "“Vibe coding”", SKY, NAVY_SOFT,
        ["describe it", "accept the output", "judge the result"],
        NAVY_SOFT, SKY,
        "Layers 1–2, used casually — you judge the output, never the mechanism.",
    )
    _flow_panel(
        slide, 6.78, 5.52,
        "Agentic engineering", AMBER, ACCENT,
        ["specify", "ground it", "equip it", "check the lap"],
        ACCENT, WHITE,
        "All four layers, deliberately — you engineer the process, not just "
        "the ask.",
    )

    template.set_notes(slide, (
        "~1–2 min, the context slide for the whole segment — the frame "
        "everything else in Segment 2 hangs on. Read the stack bottom-up: the "
        "prompt is one message; context is everything in the window around "
        "that message; the harness is the standing setup (an agent's "
        "instructions, its tools, its output format); the loop is the model "
        "running itself until a job is done. Each layer wraps the one below, "
        "so the skills accumulate — nobody skips to the top.\n\n"
        "WHAT THIS COURSE COVERS:\n"
        "• Prompt engineering — fully, starting today: Segment 3's ICC "
        "structure, meta-prompting, and the four patterns, then applied "
        "hands-on in Lesson 2.\n"
        "• Context engineering — the practical half of it. The next four "
        "slides (tokens, the context window, what fills it, system prompts) "
        "are exactly this layer's mechanics; Lesson 3 adds source-grounded "
        "tools (NotebookLM, Perplexity); Lessons 3–4 turn the Wiki Sandbox "
        "and Personal Vault into durable context you reuse every week.\n"
        "• Harness engineering — one hands-on slice, in Lesson 5. Writing a "
        "custom agent's instructions in Agent Builder is writing a system "
        "prompt; the Markdown Generator is the worked example. Still no code.\n\n"
        "WHAT IT DOES NOT COVER:\n"
        "• Loop engineering, entirely — unattended multi-step agents, agent "
        "frameworks, orchestration platforms, coding agents. That is Level "
        "6–7 on the map two slides from now: named for perspective, not "
        "taught. Anyone who wants it needs an engineering course, not this "
        "one.\n"
        "• The engineering interior of the layers we do teach: retrieval "
        "pipelines and vector stores, API and token-budget work, automated "
        "evaluation of outputs — anything that requires code.\n"
        "• Vibe coding itself — the one-sentence aside on the 7 Levels slide "
        "is all it gets.\n\n"
        "The bottom contrast, said plainly: vibe coding and agentic "
        "engineering can run on the same tools. The difference is discipline "
        "— one describes, accepts, and judges the result; the other "
        "engineers each layer and checks every lap. This course teaches the "
        "second habit from Level 2 upward even though it stops short of the "
        "top layer. Do not debate the terms; land the distinction, then move "
        "on to tokens."
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
    _llm_anatomy_slide(prs)
    _llm_training_slide(prs)
    _stack_slide(prs)
    _tokens_slide(prs)
    _context_window_slide(prs)
    _window_diagram_slide(prs)
    _system_prompts_slide(prs)
    _reasoning_tokens_slide(prs)
    _failure_modes_slide(prs)
    _tools_agents_slide(prs)
    _principles_slide(prs)

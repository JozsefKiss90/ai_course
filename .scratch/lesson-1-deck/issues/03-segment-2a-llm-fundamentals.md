# 03 — Segment 2A slides: How LLMs actually work

**What to build:** The ~10-minute LLM fundamentals sequence plays as finished slides for a non-technical audience, carrying the "powerful — but weird" framing: tokens (with the "Frabjous Day" example and a marked cue for the live tiktokenizer demo), the context window as finite working memory with the lost-in-the-middle problem and its two practical rules, system prompts as standing instructions (with the Lesson 5 foreshadow), hallucination/sycophancy/knowledge-cutoff with the "verify anything you would sign your name to" rule, a one-minute tools-and-agents foreshadow, and a closing slide with the three digestible principles.

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] One slide (or tight slide pair) per concept: tokens, context window, system prompts, failure modes, tools/agents
- [x] Live-demo cue for tiktokenizer.vercel.app visibly marked on the tokens slide and in its speaker notes
- [x] The three principles (powerful but weird; deterministic → don't use AI; fewer, better tokens) appear verbatim on a closing slide
- [x] No mathematics or engineering jargon; wording stays at the practitioner mental-model level of the lesson plan
- [x] Speaker notes on every slide, including the forward references to Lessons 3 and 5

## Comments

**2026-08-31 (agent):** Implemented. Seven real slides replace the 2A placeholders in `deck/segments/seg2a_llm_fundamentals.py`: framing ("powerful — but weird"), tokens (chip visual of "O Frabjous Day!" = 15 characters / 7 tokens — split verified against both GPT tokenizers via tiktoken, leading spaces omitted for display — plus an orange ▶ LIVE DEMO band for tiktokenizer.vercel.app), context window (attention bar visual + the two rules as cards), system prompts (message-stack visual + "Coming in Lesson 5" card), failure modes (three cards + the verify-rule band), tools/agents (one-lap-of-the-loop visual), and the three principles verbatim on numbered cards. Template gains `add_demo_cue` (reusable by ticket 05), `PALE_WARM`/`WHITE`, and public `solid`/`style` so segment modules stop reaching into privates. Facilitator notes on every slide carry timing, the live-demo script, and the Lesson 3 (NotebookLM, Perplexity) and Lesson 5 (agent/system prompt) forward references. Tests: 7 new segment-2A assertions in `tests/test_deck.py` (14 passing) — demo cue on slide AND notes, principles verbatim, notes present, order preserved. Verified visually via PowerPoint COM PNG export of all seven slides and a clean reopen of the final file. Two-axis code review run: spec axis fully met; standards findings fixed (content-area constants, stale README, white literals, fill-identity coupling).

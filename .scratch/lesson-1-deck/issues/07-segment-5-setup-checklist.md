# 07 — Segment 5 slides: Guided setup checklist

**What to build:** The screen-shareable material for the 30-minute hands-on setup block: a checklist slide with the four setup items (Google account + Gemini test prompt; Copilot Chat with the institutional account; Perplexity free account; first experimental prompt in each), the "✅ 1–4" meeting-chat template participants use to mark themselves done, a troubleshooting slide covering the typical failure points (personal vs. institutional Microsoft account, blocked Google account → separate browser profile, Gemini region/consent), and the catch-up path (Practice Week 1 drop-in, plus the offer of a 10-minute slot). A note makes clear Obsidian and Perfect Wiki are deliberately not installed today.

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] Checklist slide readable while screen-shared for 30 minutes: four numbered items, large type
- [x] Chat template ("✅ 1–4") shown on the slide so participants can copy the convention
- [x] Troubleshooting slide lists the three typical failure points with their fixes
- [x] Catch-up venue (Practice Week 1 drop-in) and the not-installed-today note present
- [x] Speaker notes carry the facilitation guidance from Segment 5 of the lesson plan

## Comments

**2026-08-31 (agent):** Implemented in `deck/segments/seg5_setup_block.py` — three slides replacing the placeholders: the setup checklist (four numbered rows in larger type than the deck's other lists, 19/15 pt on 0.92" rows, plus an orange band showing the ✅-in-meeting-chat convention ending in "✅ 1–4"), troubleshooting (the three failure points as symptom-heading/fix-body cards), and the catch-up path (Practice Week 1 drop-in card + 10-minute-slot card + "Not installed today — on purpose: Obsidian and Perfect Wiki" band). Speaker notes on all three carry the plan's facilitation guidance: checklist stays on screen-share, chat marks make stragglers visible, quick finishers co-troubleshoot, unfinished participants flagged by name before the call ends. Tests: 8 new tests in `tests/test_deck.py` (48 total passing, including a large-type check over all four rows); deck rebuilt, COM-verified to open cleanly in real PowerPoint, and the three slides visually checked via exported PNGs. Two-axis review run: standards clean (the numbered-row duplication with seg4 noted again as a candidate for a later template building-block ticket); spec review's real findings fixed — the Gemini troubleshooting card no longer invents a personal-vs-institutional Google account fact (the plan gives no fix beyond the consent prompts), the blocked-Google speaker note was trimmed to what the plan states, and the large-type test was broadened from row 1 to all eight row shapes. Judgement call kept: the slide renders "✅ 1–4" as a per-item convention (post ✅ + number as you finish) — that reading is what makes stragglers visible mid-block, which is the note's stated purpose.

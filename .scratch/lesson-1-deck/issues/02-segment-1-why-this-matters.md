# 02 — Segment 1 slides: Why this matters

**What to build:** The 10-minute opening plays as finished slides. A presenter can deliver Segment 1 from the deck alone: the Tufts Digital Planet job-risk figures (9.3M jobs, $757B, the 2.7–19.5M range), the concentration of risk in knowledge work (Information 18%, Finance/Insurance 16%, Professional Services 16% vs. 6% average), the augmentation–displacement pipeline with its "the more AI helps you do your job, the more expendable you become" quote, and the turn — the course thesis that moving up the skill curve is the way through, framed for research management administrators. Each slide carries speaker notes drawn from the lesson plan.

**Blocked by:** 01 — Deck skeleton and design template.

**Status:** resolved

- [x] Segment 1 placeholders replaced by real slides; the segment is presentable start to finish
- [x] Statistics are presented visually (numbers large, not paragraphs), with the Tufts source credited
- [x] The augmentation–displacement pipeline gets its own slide with the verbatim quote
- [x] The thesis/turn slide lands the "not fear — skill" framing for this audience
- [x] Speaker notes on every slide, sourced from Segment 1 of `lesson_1.md`

## Comments

**2026-08-31 (agent):** Implemented. Four slides in `deck/segments/seg1_why_this_matters.py`: headline figures as two 54-pt stat tiles (9.3 million jobs with the 2.7–19.5M range as a detail line; $757 billion) with the Tufts Digital Planet source line; the concentration slide as a proportional bar chart (Information 18%, Finance/Insurance 16%, Professional Services 16%, all-industry average 6% in a contrasting color) with the "historically safe jobs are now the most exposed" takeaway; the pipeline slide as an augmentation→displacement card pair over a navy quote band carrying the verbatim quote; and the turn slide contrasting shallow use vs. moving up the skill curve, closing on the research-management framing band. Speaker notes on all four, drawn from Segment 1 of `lesson_1.md`, with a presenter bridge into Segment 2. Refactor bundled per review: the repeated navy emphasis band (4 call sites across segments 1 and 2A) became `template.add_band`, and `add_card`/`add_label` moved from seg2a into `template.py`; README inventory updated. Tests: 6 new segment-1 assertions (20 passing), figures and verbatim quote verified against `lesson_1.md` by the spec review. Visuals verified via PowerPoint COM PNG export; final file reopens cleanly.

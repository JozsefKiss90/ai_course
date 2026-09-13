# 11 — Segment 2: the AI data safety and ethics framework replaces two slides

**What to build:** Slides 8 and 9 of `dist/lesson_2_deck.pptx` — "Data-protection principles — why the rule exists" and "Institutional rules: the dean's directive as reference" — replaced by the content of `.scratch/lesson2_segment_1_template.md` and its sources. The template is a researched brief on AI data safety and ethical use: a four-pillar framework of trustworthy AI, four pillars of data safety, four ethical AI principles, and eleven numbered sources. More slides may be added.

**Decision taken with the user:** replace both slides, and fold the two institutional directives into one of the new slides as a compact reference strip. The directive's six key points come off the slide; its headline rules ride on the faculty card and the section references stay in the speaker notes.

**Blocked by:** 05 — Segment 2 slides: the sensitive-data rule.

**Status:** resolved

- [x] `lesson_2.md` Segment 2 rewritten: the framework, the data-safety pillars, the ethical principles and the sources subsection replace the two old subsections
- [x] Four slides in `deck/lesson2/segments/seg2_sensitive_data_rule.py` replace two
- [x] The two directives survive as a reference strip on the framework slide
- [x] Every bracketed source marker on a slide resolves to a numbered entry on the sources slide
- [x] The deck rebuilds, tests pass, `deck.com_check` opens it in real PowerPoint, and all four new slides were exported through PowerPoint's own renderer and read back


## Resolution

Segment 2 is seven slides instead of five, and the deck is 46 instead of 44 — still inside the density guard, which allows ten for a ten-minute segment. The new block runs framework → data-safety pillars → ethical principles → sources, sitting between the routing slide and the anonymise-before-upload rule. The segment's closing slide is unchanged, because "What must never enter Gemini" is the one the room photographs and it stays last.

**The plan is still the oracle.** `lesson_2.md` authors the four pillars as a table, the two four-item lists as bullets, and the reading list as a numbered list with its URLs. The tests read those subsections and assert the slides against them, so the deck cannot drift from the plan on a pillar, a principle or a link.

**The directives are folded in, not dropped.** The framework slide carries a two-card reference strip: the rector's directive 4/2025. (X. 28.) as the umbrella, and the dean's directive 1/2026 (III.26.) with its own headline rules — human oversight and final responsibility, documented AI use, no sensitive data into external AI tools without explicit permission, critical checking of every output. That last one is what the Segment 1 recap map promises this segment delivers, so it had to survive the rework. The six key points as separate cards did not; the section numbers stay in the notes and a test still holds them there.

**Two sources were dropped, and the numbering moved.** Sources [4] and [6] of the template were YouTube videos, and the deck has a standing rule against linking to YouTube (`test_no_youtube_link_anywhere_in_the_deck`). The rule wins: the reading list is the nine written sources, renumbered 1–9, and the plan's Sources subsection says in one line why two are missing. The "regulatory compliance" card, which the template sourced to one of the videos, now cites the European Commission's trustworthy-AI guidelines — the same document the template itself linked the GDPR to.

**Every claim can be traced.** The bracketed markers on the three content slides are checked against the sources slide by a test: the markers resolve, and the slide lists exactly 1–9. Multi-number markers use non-breaking spaces so a citation never wraps onto its own line.

**Links are live and on-palette.** The sources slide puts the domain on the slide and the full address on the run as a hyperlink. PowerPoint colours hyperlink runs from the theme, so `hlink` and `folHlink` were added to the Lesson 2 theme's colour scheme as slate — the links keep the deck's palette and the underline does the signalling.

**Spelling.** The template is in American English (anonymization, minimization); the deck is in British. The slides follow the deck.

**Timing.** The subsections budget 3 + 1.5 + 1.5 + 1.5 + 0.5 + 1 + 1 = 10 minutes, unchanged at the segment level. The sources slide is the one to skip on the day if the segment runs behind — it loses nothing, because it travels with the deck into the Teams channel.

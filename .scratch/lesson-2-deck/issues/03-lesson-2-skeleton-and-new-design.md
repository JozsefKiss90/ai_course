# 03 — Lesson 2 skeleton with a new design template

**What to build:** Running the Lesson 2 build produces a second deck file whose look is clearly not the Lesson 1 look: a title slide ("Lesson 2 — The Two-Lane Tool Landscape", course name, Week 2, 60 minutes), a section divider per segment showing name, duration and mode from the plan's Timing Overview, and visibly-unfinished placeholder slides for the slide inventory the plan implies, each naming the ticket that replaces it. The new template is the single source of visual truth for Lesson 2 — its own fonts, palette, footer ("Lesson 2 · Week 2"), title/divider/content/placeholder/demo-cue builders and the in-slide blocks (card, band, label) with the same call shapes as Lesson 1 so segment authors work the same way. Suggested motif: a light canvas with two lane colours — one for the Sensitive Lane, one for the Daily Driver — used consistently so every slide about a tool is colour-coded by lane; the implementer may choose another design as long as it is distinct from Lesson 1's dark navy. A new test file asserts the structure against a saved-and-reopened file with the plan's Timing Overview as the oracle.

**Blocked by:** 01 — Lesson 2 session plan document; 02 — Prefactor: shared deck mechanics.

**Status:** ready-for-agent

- [ ] Lesson 2 builds with its own command to its own output file; Lesson 1 build and tests untouched
- [ ] The file opens cleanly in PowerPoint (COM check); title slide, five dividers in session order with duration and mode, placeholders per segment carrying their ticket number in notes
- [ ] Master and theme define fonts, colours and a Lesson 2 footer; the palette and canvas differ from Lesson 1 and the lane colour-coding is documented in the template's docstring
- [ ] Builders exist for title, divider, content, placeholder, demo cue, card, band, label; the README table maps each segment module to its ticket
- [ ] Lesson 2 test file passes with structure tests (title, dividers, placeholders, slide count, master footer and theme fonts)

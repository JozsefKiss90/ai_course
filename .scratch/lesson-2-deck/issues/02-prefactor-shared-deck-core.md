# 02 — Prefactor: shared deck mechanics, multi-lesson layout

**What to build:** The deck package can host more than one lesson with different visual designs. The lesson-independent PowerPoint mechanics — presentation setup at 16:9, writing fonts and colours into the theme part, the master footer, the safe master shape-id helper (the near-2^31 gotcha), the flat/outlined shape styling helpers, run styling, blank-slide and notes helpers — move into one shared core module. The Lesson 1 template keeps its design constants and slide builders on top of that core, and the Lesson 1 build, output file and every existing test keep working unchanged. A sub-package for Lesson 2 exists beside the Lesson 1 modules (empty or with a stub build), so ticket 03 has a home without touching Lesson 1 again. The deck README explains the split: core = mechanics, per-lesson template = design.

"Make the change easy, then make the easy change" — this ticket is the easy-making. Nothing visible changes in the Lesson 1 deck.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] Lesson 1 builds with the same command as before and the full existing test suite passes
- [x] The regenerated Lesson 1 deck opens cleanly in PowerPoint (COM check, as ticket 01 of the Lesson 1 effort did)
- [x] A shared core module holds the mechanics; the Lesson 1 template imports them rather than defining them
- [x] The Lesson 2 sub-package exists with its own place for template, build and segments
- [x] Deck README documents the core / per-lesson split and how to build each lesson

## Comments

**2026-09-10 (agent):** Implemented. `deck/core.py` holds the mechanics (16:9 setup, theme fonts/colours, master footer, `master_next_id`, `solid`/`outlined`, `style`, blank-slide/text/notes helpers) behind a `core.Design` dataclass; `deck/template.py` keeps Lesson 1's constants and slide builders and delegates to the core, re-exporting `solid`, `add_bar`, `set_notes` so segment modules are untouched. `deck/lesson2/` exists with `template.py` (footer + provisional stand-ins for ticket 03), `build.py` (`python -m deck.lesson2.build` → `dist/lesson_2_deck.pptx`, currently 0 slides) and `segments/`. README documents core = mechanics, per-lesson template = design, and both build commands. Lesson 1 builds with the same command (40 slides); the full suite passes (64 existing + 6 new in `tests/test_core.py`); both regenerated decks open cleanly in PowerPoint via COM. One correction found on the way: the near-2^31 ids that break PowerPoint are the stock master's `p:sldLayoutId` entries picked up by python-pptx's id scan, not footer placeholders — docstring, README gotcha and test now say so.

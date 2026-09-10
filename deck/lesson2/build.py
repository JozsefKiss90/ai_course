"""Entry point for the Lesson 2 deck: `python -m deck.lesson2.build`.

Assembles the deck in session order per the Timing Overview in
lesson_2.md: title slide, then per segment a section divider followed by
that segment's slides from its module in deck/lesson2/segments/. Ticket 03
adds the title, dividers and placeholders; tickets 04–08 each own one
segment module. Until then the build writes a valid deck with no slides.
"""

from pathlib import Path

from deck.lesson2 import template

OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "dist" / "lesson_2_deck.pptx"


def build_presentation():
    """Build the Lesson 2 deck and return it (unsaved)."""
    return template.new_presentation()


def main():
    prs = build_presentation()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()

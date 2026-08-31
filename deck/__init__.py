"""Build system for the Lesson 1 slide deck.

The deck is always regenerated from source: `python -m deck.build` writes
dist/lesson_1_deck.pptx. Design decisions (fonts, colors, footer, slide
helpers) live in deck/template.py; each session segment contributes its
slides from its own module under deck/segments/.
"""

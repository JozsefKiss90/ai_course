"""Build system for the Lesson 2 slide deck.

`python -m deck.lesson2.build` writes dist/lesson_2_deck.pptx. The
lesson-independent mechanics come from deck/core.py; Lesson 2's own design
(fonts, palette, footer, slide builders) lives in deck/lesson2/template.py
and each session segment contributes its slides from its own module under
deck/lesson2/segments/.
"""

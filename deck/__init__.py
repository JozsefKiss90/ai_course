"""Build system for the course slide decks.

Decks are always regenerated from source. The lesson-independent
PowerPoint mechanics live in deck/core.py; each lesson keeps its own
design and slide builders on top of that core:

- Lesson 1: `python -m deck.build` writes dist/lesson_1_deck.pptx from
  deck/template.py and deck/segments/.
- Lesson 2: `python -m deck.lesson2.build` writes dist/lesson_2_deck.pptx
  from deck/lesson2/template.py and deck/lesson2/segments/.
"""

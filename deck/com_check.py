"""Open built decks in real PowerPoint via COM and report whether they load.

python-pptx round-trips do not catch everything PowerPoint rejects (the
master shape-id gotcha in README.md was found this way), so run this after
a build: `python -m deck.com_check dist/lesson_1_deck.pptx dist/lesson_2_deck.pptx`.
Windows with PowerPoint and pywin32 only; exits non-zero if any file fails.
"""

import os
import sys

import win32com.client


def main(paths):
    app = win32com.client.Dispatch("PowerPoint.Application")
    ok = True
    try:
        for path in (os.path.abspath(p) for p in paths):
            try:
                pres = app.Presentations.Open(path, True, False, False)  # ReadOnly, Untitled, WithWindow
                fonts = pres.SlideMaster.Theme.ThemeFontScheme
                print(f"OK   {os.path.basename(path)}: {pres.Slides.Count} slides, "
                      f"theme fonts {fonts.MajorFont(1).Name} / {fonts.MinorFont(1).Name}")
                pres.Close()
            except Exception as exc:  # noqa: BLE001 — report every failure, keep going
                ok = False
                print(f"FAIL {os.path.basename(path)}: {exc}")
    finally:
        app.Quit()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["dist/lesson_1_deck.pptx", "dist/lesson_2_deck.pptx"]))

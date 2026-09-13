"""Render a handout markdown file to PDF with reportlab.

Usage: python handouts/build_handout.py handouts/lesson2_prompt_handout.md dist/lesson2_prompt_handout.pdf

Supports the markdown subset the handouts use: #/##/###/#### headings,
paragraphs with **bold** and *italic*, "- " bullets, fenced code blocks
(rendered as shaded prompt boxes), pipe tables and "---" rules.
Fonts and colours follow deck/lesson2/template.py (Cambria + Calibri,
warm-paper palette, teal = Sensitive Lane, violet = Daily Driver).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

FONTS = Path("C:/Windows/Fonts")

# Palette — mirrors deck/lesson2/template.py
CANVAS = colors.HexColor("#F7F4EE")
LINE = colors.HexColor("#D8D2C6")
INK = colors.HexColor("#1C242B")
SLATE = colors.HexColor("#3E4C59")
TEXT = colors.HexColor("#2A333B")
MUTED = colors.HexColor("#6B747D")
TEAL = colors.HexColor("#0E7C7B")
TEAL_TINT = colors.HexColor("#DFF1EF")
VIOLET = colors.HexColor("#6A4CBC")
VIOLET_TINT = colors.HexColor("#EBE6F7")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Cambria", str(FONTS / "cambria.ttc"), subfontIndex=0))
    pdfmetrics.registerFont(TTFont("Cambria-Bold", str(FONTS / "cambriab.ttf")))
    pdfmetrics.registerFont(TTFont("Calibri", str(FONTS / "calibri.ttf")))
    pdfmetrics.registerFont(TTFont("Calibri-Bold", str(FONTS / "calibrib.ttf")))
    pdfmetrics.registerFont(TTFont("Calibri-Italic", str(FONTS / "calibrii.ttf")))
    pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", str(FONTS / "calibriz.ttf")))
    pdfmetrics.registerFont(TTFont("Consolas", str(FONTS / "consola.ttf")))
    pdfmetrics.registerFontFamily(
        "Calibri",
        normal="Calibri",
        bold="Calibri-Bold",
        italic="Calibri-Italic",
        boldItalic="Calibri-BoldItalic",
    )
    pdfmetrics.registerFontFamily("Cambria", normal="Cambria", bold="Cambria-Bold",
                                  italic="Cambria", boldItalic="Cambria-Bold")


S = {}


def build_styles() -> None:
    S["title"] = ParagraphStyle("title", fontName="Cambria-Bold", fontSize=26, leading=31,
                                textColor=INK, spaceAfter=4)
    S["subtitle"] = ParagraphStyle("subtitle", fontName="Cambria", fontSize=15, leading=19,
                                   textColor=VIOLET, spaceAfter=10)
    S["h2"] = ParagraphStyle("h2", fontName="Cambria-Bold", fontSize=17, leading=21,
                             textColor=INK, spaceBefore=14, spaceAfter=6)
    S["h3"] = ParagraphStyle("h3", fontName="Cambria-Bold", fontSize=13.5, leading=17,
                             textColor=VIOLET, spaceBefore=12, spaceAfter=4)
    S["h4"] = ParagraphStyle("h4", fontName="Calibri-Bold", fontSize=11.5, leading=14.5,
                             textColor=INK, spaceBefore=10, spaceAfter=2)
    S["body"] = ParagraphStyle("body", fontName="Calibri", fontSize=10.5, leading=14,
                               textColor=TEXT, spaceAfter=6, alignment=TA_LEFT)
    S["meta"] = ParagraphStyle("meta", parent=S["body"], textColor=MUTED, fontSize=9.5,
                               leading=12.5, spaceAfter=4)
    S["check"] = ParagraphStyle("check", parent=S["body"], leftIndent=10, borderPadding=0,
                                textColor=TEXT)
    S["bullet"] = ParagraphStyle("bullet", parent=S["body"], spaceAfter=3)
    S["code"] = ParagraphStyle("code", fontName="Consolas", fontSize=9, leading=12,
                               textColor=INK)
    S["cell"] = ParagraphStyle("cell", fontName="Calibri", fontSize=9.5, leading=12,
                               textColor=TEXT)
    S["cellhead"] = ParagraphStyle("cellhead", parent=S["cell"], fontName="Calibri-Bold",
                                   textColor=colors.white)
    S["footer"] = ParagraphStyle("footer", fontName="Calibri", fontSize=8.5, textColor=MUTED)


INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*")
INLINE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")


def inline(text: str) -> str:
    """Escape for Paragraph markup and convert **bold** / *italic*."""
    t = escape(text)
    t = INLINE_BOLD.sub(r"<b>\1</b>", t)
    t = INLINE_ITALIC.sub(r"<i>\1</i>", t)
    return t


def code_box(lines: list[str], width: float, tint, edge) -> Table:
    body = "<br/>".join(escape(l).replace(" ", "&nbsp;") or "&nbsp;" for l in lines)
    para = Paragraph(body, S["code"])
    t = Table([[para]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def md_table(rows: list[list[str]], width: float) -> Table:
    ncol = len(rows[0])
    # First column narrower for label-like tables
    if ncol == 3 and rows[0][1].strip().lower() == "length":
        widths = [width * 0.14, width * 0.16, width * 0.70]
    elif ncol == 3:
        widths = [width * 0.20, width * 0.36, width * 0.44]
    elif ncol == 4:
        widths = [width * 0.22, width * 0.22, width * 0.26, width * 0.30]
    else:
        widths = [width / ncol] * ncol
    data = [[Paragraph(inline(c), S["cellhead"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(inline(c), S["cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), SLATE),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), CANVAS))
    t.setStyle(style)
    return t


def parse(md: str, width: float) -> list:
    flow = []
    lines = md.splitlines()
    i = 0
    title_seen = False
    pending: list = []  # flowables to keep together with the next code box (h4 + meta)

    def flush_pending():
        nonlocal pending
        flow.extend(pending)
        pending = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            is_diagram = any("+------>" in l for l in code)
            tint, edge = (TEAL_TINT, TEAL) if is_diagram else (VIOLET_TINT, VIOLET)
            box = code_box(code, width, tint, edge)
            if pending:
                flow.append(KeepTogether(pending + [box]))
                pending = []
            else:
                flow.append(box)
            flow.append(Spacer(1, 5))
            continue

        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            flush_pending()
            table = md_table(rows, width)
            flow.append(KeepTogether(table) if len(rows) <= 10 else table)
            flow.append(Spacer(1, 8))
            continue

        if stripped == "---":
            flush_pending()
            flow.append(HRFlowable(width="100%", thickness=0.6, color=LINE,
                                   spaceBefore=6, spaceAfter=6))
            i += 1
            continue

        if stripped.startswith("#### "):
            flush_pending()
            pending.append(Paragraph(inline(stripped[5:]), S["h4"]))
            i += 1
            continue
        if stripped.startswith("### "):
            flush_pending()
            flow.append(Paragraph(inline(stripped[4:]), S["h3"]))
            i += 1
            continue
        if stripped.startswith("## "):
            flush_pending()
            if not title_seen:
                flow.append(Paragraph(inline(stripped[3:]), S["subtitle"]))
                title_seen = True
            else:
                flow.append(Paragraph(inline(stripped[3:]), S["h2"]))
            i += 1
            continue
        if stripped.startswith("# "):
            flush_pending()
            flow.append(Paragraph(inline(stripped[2:]), S["title"]))
            i += 1
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(ListItem(Paragraph(inline(lines[i].strip()[2:]), S["bullet"]),
                                      leftIndent=14, value="•"))
                i += 1
            flush_pending()
            flow.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=14,
                                     bulletFontName="Calibri", bulletColor=VIOLET))
            flow.append(Spacer(1, 4))
            continue

        if stripped == "":
            i += 1
            continue

        # paragraph: gather consecutive text lines
        buf = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#|```|\||- |---$)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        text = " ".join(buf)
        if text.startswith("Tags:"):
            pending.append(Paragraph(inline(text), S["meta"]))
        elif text.startswith("Check:"):
            flush_pending()
            rest = text[6:].strip()
            rest = rest[:1].upper() + rest[1:]
            flow.append(Paragraph("<b>Check.</b> " + inline(rest), S["check"]))
        else:
            if pending:
                pending.append(Paragraph(inline(text), S["body"]))
            else:
                flow.append(Paragraph(inline(text), S["body"]))
    flush_pending()
    return flow


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Calibri", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 12 * mm,
                      "Lesson 2 assignment · example prompts · Daily Driver lane unless marked")
    canvas.drawRightString(A4[0] - doc.rightMargin, 12 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 16 * mm, A4[0] - doc.rightMargin, 16 * mm)
    canvas.restoreState()


def main(src: str, dst: str) -> None:
    register_fonts()
    build_styles()
    md = Path(src).read_text(encoding="utf-8")
    doc = SimpleDocTemplate(dst, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=22 * mm,
                            title="From unfamiliar videos to a lesson",
                            author="ELTE AI course, Lesson 2",
                            subject="Example prompts for the Lesson 2 assignment")
    width = A4[0] - doc.leftMargin - doc.rightMargin
    doc.build(parse(md, width), onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

#!/usr/bin/env python3
"""Плашка «ОТ СЕБЯ» для резюме кандидатов.

Геометрия, шрифты и цвета сняты с плашки в резюме Шарафутдиновой (стр. 3):
карточка 480 pt по ширине, отступ 60 pt от верха A4, жёлтая полоса слева,
фото 150x200, две подсвеченные строки, «чипы», абзац и подпись.
Высота карточки считается от содержимого.

Резюме остаётся в родном формате, добавляется только плашка:
  * PDF  - новая последняя страница (исходные страницы не трогаются);
  * DOCX - новая последняя страница с плашкой-картинкой 1:1 по размеру.

Использование:
  make_ot_sebya.py TXT OUT_DIR --date 28.10.2026 \
      "Фамилия=резюме.pdf=фото.jpg=имя_файла.pdf" ...  (фото и имя - необязательны)
Если фото не задано (пусто после второго '='), берётся из самого резюме:
  PDF  - первое крупное изображение, DOCX - самое большое изображение в media.
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_DIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("LS", f"{FONT_DIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LS-B", f"{FONT_DIR}/LiberationSans-Bold.ttf"))

PAGE_W, PAGE_H = 595.28, 841.89
CARD_X, CARD_W, CARD_TOP = 57.6, 480.0, 781.89
CARD_R = 7.0
ACCENT_W = 6.0
PHOTO_X, PHOTO_W, PHOTO_H, PHOTO_R = 77.6, 150.0, 200.0, 5.0
TEXT_X = 243.6
RIGHT = CARD_X + CARD_W - 20  # 517.6

INK = (0.113725, 0.113725, 0.105882)
GRAY = (0.333333, 0.333333, 0.333333)
CHIP_INK = (0.227451, 0.227451, 0.227451)
LABEL = (0.541176, 0.415686, 0)
CREAM = (1, 0.984314, 0.917647)
ACCENT = (0.960784, 0.768627, 0)
CARD_STROKE = (0.917647, 0.87451, 0.658824)
PHOTO_STROKE = (0.847059, 0.823529, 0.737255)
MARK = (1, 0.831373, 0.231373)
CHIP_STROKE = (0.803922, 0.74902, 0.521569)


def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        t = f"{cur} {word}".strip()
        if cur and sw(t, font, size) > width:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def parse_txt(path):
    raw = open(path, encoding="utf-8-sig").read().replace("\r", "").replace("\xa0", " ")
    cards = {}
    for block in re.split(r"(?m)^\s*ОТ СЕБЯ\s*$", raw):
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        name = lines[0]
        marks = [l for l in lines[1:] if l.startswith(("Собеседование", "Согласие"))]
        chips = [l.lstrip("•").strip() for l in lines[1:] if l.startswith("•")]
        body = [l for l in lines[1:] if l not in marks and not l.startswith("•")]
        cards[name] = dict(name=name, marks=marks, chips=chips, text=" ".join(body))
    return cards


def cover_jpeg(photo, w=900, h=1200):
    im = Image.open(photo).convert("RGB")
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    buf.seek(0)
    return ImageReader(buf)


def rrect_path(c, x, y, w, h, r):
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    return p


def draw_plate(c, d, photo, date):
    # --- раскладка (сверху вниз), координаты как в шаблоне ---
    photo_top = CARD_TOP - 14
    photo_bot = photo_top - PHOTO_H
    label_base = CARD_TOP - 22
    name_lines = wrap(d["name"], "LS-B", 15, RIGHT - TEXT_X)
    name_base = [label_base - 24 - 18 * i for i in range(len(name_lines))]

    y = name_base[-1] - 16  # верх первой подсветки
    marks = []
    for m in d["marks"]:
        for ln in wrap(m, "LS-B", 13.5, RIGHT - (TEXT_X - 3) - 8):
            marks.append((ln, y - 20.5))
            y -= 22
    y_after_marks = marks[-1][1] if marks else y

    y = y_after_marks - 5.5  # верх первого чипа
    chips = []
    for ch in d["chips"]:
        lines = wrap(ch, "LS", 10.5, RIGHT - TEXT_X - 16)
        h = 6.4 + 12.6 * len(lines)
        chips.append((lines, y, h))
        y -= h + 6
    chips_bot = chips[-1][1] - chips[-1][2] if chips else y_after_marks

    col_bot = min(photo_bot, chips_bot + 8)
    para = [ln for part in d["text"].split("\n") for ln in wrap(part, "LS", 12.5, RIGHT - PHOTO_X)]
    para_base = [col_bot - 43 - 18 * i for i in range(len(para))]
    sig_base = para_base[-1] - 22
    card_bot = sig_base - 17
    card_h = CARD_TOP - card_bot

    # --- рисование ---
    c.saveState()
    c.clipPath(rrect_path(c, CARD_X, card_bot, CARD_W, card_h, CARD_R), stroke=0, fill=0)
    c.setFillColorRGB(*CREAM)
    c.rect(CARD_X, card_bot, CARD_W, card_h, stroke=0, fill=1)
    c.setFillColorRGB(*ACCENT)
    c.rect(CARD_X, card_bot, ACCENT_W, card_h, stroke=0, fill=1)
    c.restoreState()
    c.setStrokeColorRGB(*CARD_STROKE)
    c.setLineWidth(0.75)
    c.roundRect(CARD_X, card_bot, CARD_W, card_h, CARD_R, stroke=1, fill=0)

    c.saveState()
    c.clipPath(rrect_path(c, PHOTO_X, photo_bot, PHOTO_W, PHOTO_H, PHOTO_R), stroke=0, fill=0)
    c.drawImage(photo, PHOTO_X, photo_bot, PHOTO_W, PHOTO_H)
    c.restoreState()
    c.setStrokeColorRGB(*PHOTO_STROKE)
    c.setLineWidth(0.6)
    c.roundRect(PHOTO_X, photo_bot, PHOTO_W, PHOTO_H, PHOTO_R, stroke=1, fill=0)

    t = c.beginText(TEXT_X, label_base)
    t.setFont("LS-B", 9)
    t.setCharSpace(0.8)
    t.setFillColorRGB(*LABEL)
    t.textOut("ОТ СЕБЯ")
    t.setCharSpace(0)  # иначе межбуквенный интервал «протекает» на весь текст
    c.drawText(t)

    c.setFillColorRGB(*INK)
    c.setFont("LS-B", 15)
    for ln, b in zip(name_lines, name_base):
        c.drawString(TEXT_X, b, ln)

    for ln, yb in marks:
        c.setFillColorRGB(*MARK)
        c.rect(TEXT_X - 3, yb, sw(ln, "LS-B", 13.5) + 8, 20.5, stroke=0, fill=1)
        c.setFillColorRGB(*INK)
        c.setFont("LS-B", 13.5)
        c.drawString(TEXT_X + 1, yb + 4.5, ln)

    c.setLineWidth(0.6)
    for lines, top, h in chips:
        w = max(sw(l, "LS", 10.5) for l in lines) + 16
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(*CHIP_STROKE)
        c.roundRect(TEXT_X, top - h, w, h, 9.5, stroke=1, fill=1)
        c.setFillColorRGB(*CHIP_INK)
        c.setFont("LS", 10.5)
        for i, l in enumerate(lines):
            c.drawString(TEXT_X + 8, top - 13.4 - 12.6 * i, l)

    c.setFillColorRGB(*INK)
    c.setFont("LS", 12.5)
    for ln, b in zip(para, para_base):
        c.drawString(PHOTO_X, b, ln)

    sig = f"— Д. Плаксин, {date}"
    c.setFillColorRGB(*GRAY)
    c.setFont("LS", 11)
    c.drawString(CARD_X + CARD_W - 16 - sw(sig, "LS", 11), sig_base, sig)
    return card_bot, card_h


def build_plate_pdf(d, photo, date, path):
    c = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H))
    card_bot, card_h = draw_plate(c, d, cover_jpeg(photo), date)
    c.showPage()
    c.save()
    return card_bot, card_h


# ---------------------------------------------------------------- PDF
def photo_from_pdf(pdf, tmp):
    base = os.path.join(tmp, "pdfimg")
    subprocess.run(["pdfimages", "-png", pdf, base], check=True)
    files = sorted(f for f in os.listdir(tmp) if f.startswith("pdfimg"))
    best = max(files, key=lambda f: Image.open(os.path.join(tmp, f)).size[0] * Image.open(os.path.join(tmp, f)).size[1])
    return os.path.join(tmp, best)


def add_to_pdf(src, plate_pdf, out):
    w = PdfWriter(clone_from=PdfReader(src))
    w.add_page(PdfReader(plate_pdf).pages[0])
    w.write(out)


# --------------------------------------------------------------- DOCX
def photo_from_docx(docx, tmp):
    with zipfile.ZipFile(docx) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/") and n.lower().endswith((".jpg", ".jpeg", ".png"))]
        best = max(media, key=lambda n: z.getinfo(n).file_size)
        p = os.path.join(tmp, "docx_photo" + os.path.splitext(best)[1])
        open(p, "wb").write(z.read(best))
    return p


def add_to_docx(src, plate_pdf, card_bot, card_h, out, tmp):
    import docx
    from docx.shared import Pt, Emu
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    dpi = 300
    base = os.path.join(tmp, "plate")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", plate_pdf, base], check=True)
    im = Image.open(base + ".png").convert("RGB")
    k = dpi / 72
    pad = 2  # pt
    box = (round((CARD_X - pad) * k), round((PAGE_H - CARD_TOP - pad) * k),
           round((CARD_X + CARD_W + pad) * k), round((PAGE_H - card_bot + pad) * k))
    im.crop(box).save(base + "_crop.png", dpi=(dpi, dpi))
    w_pt, h_pt = CARD_W + 2 * pad, card_h + 2 * pad

    d = docx.Document(src)
    sec = d.sections[-1]
    text_w = (sec.page_width - sec.left_margin - sec.right_margin) / 12700  # pt
    p = d.add_paragraph()
    pf = p.paragraph_format
    pf.page_break_before = True
    pf.space_before = pf.space_after = Pt(0)
    pf.left_indent = Pt(-(w_pt - text_w) / 2) if w_pt > text_w else Pt((text_w - w_pt) / 2)
    p.add_run().add_picture(base + "_crop.png", width=Pt(w_pt), height=Pt(h_pt))
    d.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("txt")
    ap.add_argument("out_dir")
    ap.add_argument("--date", required=True)
    ap.add_argument("items", nargs="+", help="Фамилия=файл резюме=[фото]")
    a = ap.parse_args()

    cards = parse_txt(a.txt)
    os.makedirs(a.out_dir, exist_ok=True)
    for item in a.items:
        key, src, *rest = item.split("=")
        photo = rest[0] if rest and rest[0] else None
        out_name = rest[1] if len(rest) > 1 else os.path.basename(src)
        d = next(v for k, v in cards.items() if k.startswith(key))
        with tempfile.TemporaryDirectory() as tmp:
            ext = os.path.splitext(src)[1].lower()
            if not photo:
                photo = photo_from_pdf(src, tmp) if ext == ".pdf" else photo_from_docx(src, tmp)
            plate = os.path.join(tmp, "plate.pdf")
            card_bot, card_h = build_plate_pdf(d, photo, a.date, plate)
            out = os.path.join(a.out_dir, out_name)
            if ext == ".pdf":
                add_to_pdf(src, plate, out)
            else:
                add_to_docx(src, plate, card_bot, card_h, out, tmp)
        print("OK", d["name"], "->", out)


if __name__ == "__main__":
    sys.exit(main())

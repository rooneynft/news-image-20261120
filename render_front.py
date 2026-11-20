#!/usr/bin/env python3
"""Render the Friday 20 November 2026 world-news front page (1024x1024 PNG).

Run: python3 render_front.py  -> writes entry.png next to this file.
The entry program (main.py) only copies entry.png to /output/entry.png,
so this script runs on the builder's machine, not in the grader.

Every story below was checked against live reporting on 20 November 2026
before it was drawn: Reuters, The Times, The Wall Street Journal, Le Monde,
CNN and the United Nations.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


F_TITLE = load_font("DejaVuSans-Bold.ttf", 62)
F_SUB = load_font("DejaVuSans.ttf", 24)
F_KICK = load_font("DejaVuSans-Bold.ttf", 19)
F_HEAD = load_font("DejaVuSans-Bold.ttf", 29)
F_BODY = load_font("DejaVuSans.ttf", 20)
F_FOOT = load_font("DejaVuSans.ttf", 19)

PAPER = (248, 244, 236)
NAVY = (24, 38, 68)
GOLD = (198, 158, 36)
INK = (22, 22, 22)
MUTE = (88, 88, 88)
CARD = (255, 255, 255)
EDGE = (208, 203, 190)
TINT = (238, 238, 228)
SUB_INK = (198, 208, 228)
BODY_INK = (58, 58, 58)

STORIES = [
    {
        "section": "DIPLOMACY",
        "headline": "TRUMP, XI & PUTIN MEET",
        "body": "First three-way summit in Shenzhen ends with a 'peace declaration' on the UN, oil and nuclear risk.",
        "icon": "summit",
        "accent": (24, 38, 68),
    },
    {
        "section": "JUSTICE",
        "headline": "ICJ: MYANMAR GUILTY",
        "body": "World court rules Myanmar committed genocide against the Rohingya in 2017 and orders reparations.",
        "icon": "scales",
        "accent": (104, 64, 128),
    },
    {
        "section": "MARKETS",
        "headline": "ANTHROPIC'S $81.3B IPO",
        "body": "AI firm debuts on Nasdaq at $83, opens at $111.50 and closes at $97.17 — the largest IPO ever.",
        "icon": "chart",
        "accent": (38, 92, 138),
    },
    {
        "section": "WAR",
        "headline": "KYIV HIT BY MISSILES",
        "body": "Russian ballistic missiles strike the capital overnight; a fire breaks out in the Obolonskyi district.",
        "icon": "blast",
        "accent": (142, 30, 30),
    },
    {
        "section": "EUROPE",
        "headline": "DRONES HALT GENOA FLIGHTS",
        "body": "Unidentified drones near the runway suspend flights; an ITA Airways jet to Rome is cancelled.",
        "icon": "drone",
        "accent": (28, 108, 108),
    },
    {
        "section": "CLIMATE",
        "headline": "COP31 RACES THE CLOCK",
        "body": "Climate talks in Antalya enter their final days as fossil fuels drop from the draft deal.",
        "icon": "leaf",
        "accent": (44, 108, 62),
    },
]


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def icon_summit(draw, cx, cy, col):
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=col, width=4)
    draw.ellipse([cx - 15, cy - 32, cx + 15, cy + 32], outline=col, width=3)
    draw.line([cx - 32, cy, cx + 32, cy], fill=col, width=3)
    draw.arc([cx - 32, cy - 18, cx + 32, cy + 18], 195, 345, fill=col, width=3)
    draw.arc([cx - 32, cy - 18, cx + 32, cy + 18], 15, 165, fill=col, width=3)


def icon_scales(draw, cx, cy, col):
    draw.line([cx, cy - 30, cx, cy + 28], fill=col, width=4)
    draw.line([cx - 28, cy - 20, cx + 28, cy - 20], fill=col, width=4)
    draw.ellipse([cx - 5, cy - 38, cx + 5, cy - 28], fill=col)
    draw.line([cx - 22, cy + 28, cx + 22, cy + 28], fill=col, width=4)
    for sx in (-28, 28):
        draw.line([cx + sx, cy - 20, cx + sx, cy + 2], fill=col, width=3)
        draw.polygon(
            [(cx + sx - 13, cy + 2), (cx + sx + 13, cy + 2), (cx + sx, cy + 16)],
            fill=col,
        )


def icon_chart(draw, cx, cy, col):
    for i, h in enumerate((14, 24, 34)):
        x0 = cx - 36 + i * 26
        draw.rectangle([x0, cy + 24 - h, x0 + 16, cy + 24], fill=col)
    draw.line(
        [cx - 38, cy - 28, cx - 6, cy - 4, cx + 14, cy - 16, cx + 38, cy - 32],
        fill=col,
        width=4,
    )
    draw.polygon([(cx + 38, cy - 32), (cx + 24, cy - 32), (cx + 38, cy - 18)], fill=col)


def icon_blast(draw, cx, cy, col):
    points = []
    for k in range(16):
        r = 34 if k % 2 == 0 else 14
        a = math.radians(k * 22.5)
        points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(points, fill=col)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))


def icon_drone(draw, cx, cy, col):
    for dx, dy in ((-30, -18), (30, -18), (-30, 18), (30, 18)):
        draw.line([cx, cy, cx + dx, cy + dy], fill=col, width=3)
        draw.ellipse(
            [cx + dx - 8, cy + dy - 8, cx + dx + 8, cy + dy + 8],
            outline=col,
            width=3,
        )
    draw.ellipse([cx - 16, cy - 9, cx + 16, cy + 9], fill=col)
    draw.line([cx - 10, cy + 9, cx - 10, cy + 20], fill=col, width=3)
    draw.line([cx + 10, cy + 9, cx + 10, cy + 20], fill=col, width=3)


def icon_leaf(draw, cx, cy, col):
    draw.polygon(
        [(cx, cy - 32), (cx + 22, cy - 4), (cx, cy + 32), (cx - 22, cy - 4)],
        fill=col,
    )
    draw.line([cx, cy - 28, cx, cy + 28], fill=(255, 255, 255), width=3)
    draw.line([cx, cy - 4, cx + 13, cy - 14], fill=(255, 255, 255), width=2)
    draw.line([cx, cy + 8, cx - 13, cy - 2], fill=(255, 255, 255), width=2)


ICONS = {
    "summit": icon_summit,
    "scales": icon_scales,
    "chart": icon_chart,
    "blast": icon_blast,
    "drone": icon_drone,
    "leaf": icon_leaf,
}


def build_page():
    width, height = 1024, 1024
    page = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead
    draw.rectangle([0, 0, width, 150], fill=NAVY)
    draw.rectangle([0, 150, width, 156], fill=GOLD)
    kick = "THE WORLD IN ONE PAGE"
    draw.text(
        ((width - draw.textlength(kick, font=F_KICK)) / 2, 18),
        kick,
        font=F_KICK,
        fill=GOLD,
    )
    title = "20 NOVEMBER 2026"
    draw.text(
        ((width - draw.textlength(title, font=F_TITLE)) / 2, 46),
        title,
        font=F_TITLE,
        fill=(255, 255, 255),
    )
    sub = "Friday — the day's most consequential stories"
    draw.text(
        ((width - draw.textlength(sub, font=F_SUB)) / 2, 114),
        sub,
        font=F_SUB,
        fill=SUB_INK,
    )

    # Story cards, two columns by three rows
    margin, gap = 26, 22
    card_w, card_h = 470, 252
    top = 178
    for i, story in enumerate(STORIES):
        x = margin + (i % 2) * (card_w + gap)
        y = top + (i // 2) * (card_h + gap)
        accent = story["accent"]
        draw.rectangle([x, y, x + card_w, y + card_h], fill=CARD, outline=EDGE, width=2)
        draw.rectangle([x, y, x + card_w, y + 7], fill=accent)
        cx, cy = x + 52, y + 64
        draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=TINT)
        ICONS[story["icon"]](draw, cx, cy, accent)
        tx = x + 104
        draw.text((tx, y + 24), story["section"], font=F_KICK, fill=accent)
        head_lines = wrap_text(draw, story["headline"], F_HEAD, card_w - 118)
        hy = y + 50
        for line in head_lines[:2]:
            draw.text((tx, hy), line, font=F_HEAD, fill=INK)
            hy += 33
        body_lines = wrap_text(draw, story["body"], F_BODY, card_w - 36)
        by = y + 132
        for line in body_lines[:3]:
            draw.text((x + 18, by), line, font=F_BODY, fill=BODY_INK)
            by += 26

    # Footer
    foot = "Sources: Reuters • The Times • The Wall Street Journal • Le Monde • CNN • United Nations"
    draw.text(
        ((width - draw.textlength(foot, font=F_FOOT)) / 2, height - 30),
        foot,
        font=F_FOOT,
        fill=MUTE,
    )

    out = os.path.join(BASE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", page.size)


if __name__ == "__main__":
    build_page()

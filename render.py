"""Render the 21 November 2026 news poster (1024x1024) from news.json.

Fresh design for this edition: crimson masthead, lead story with a
strike-map strip, six stories in a 2x3 grid, charcoal footer band.
Drawn with PIL + DejaVu fonts only. Deterministic: no randomness,
no timestamps, fixed layout.
"""
import json
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 33)
CRIMSON = (163, 31, 38)
NAVY = (22, 40, 63)
GOLD = (201, 154, 46)
GOLD_LIGHT = (232, 201, 106)
MUTED = (74, 68, 56)
CHARCOAL = (25, 25, 33)
WHITE = (255, 255, 255)
PANEL = (22, 40, 63)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Shrink font until text fits in max_lines at max_w. Returns (font, lines)."""
    size = fnt.size
    while size > 10:
        f = font(fnt.path, size) if hasattr(fnt, "path") else fnt
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 2
    f = font(fnt.path, 10) if hasattr(fnt, "path") else fnt
    return f, wrap(draw, text, f, max_w)


def text_h(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[3] - box[1]


def draw_chips(draw, chips, x, y, max_w):
    """Draw pill chips in a row; returns total height used."""
    fnt = font(SANS_B, 17)
    widths = []
    total = 0
    for chip in chips:
        w = int(draw.textlength(chip, font=fnt)) + 28
        widths.append(w)
        total += w + 12
    total -= 12
    if total > max_w:
        fnt = font(SANS_B, 15)
        widths = []
        total = 0
        for chip in chips:
            w = int(draw.textlength(chip, font=fnt)) + 26
            widths.append(w)
            total += w + 12
        total -= 12
    cx = x
    h = 34
    for chip, w in zip(chips, widths):
        draw.rounded_rectangle([cx, y, cx + w, y + h], radius=17,
                               outline=CRIMSON, width=2)
        tw = draw.textlength(chip, font=fnt)
        draw.text((cx + (w - tw) / 2, y + (h - text_h(draw, chip, fnt)) / 2 - 1),
                  chip, font=fnt, fill=CRIMSON)
        cx += w + 12
    return h


def bezier(p0, p1, p2, n=48):
    """Sample a quadratic bezier curve; returns list of (x, y) points."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def draw_map_panel(draw, x, y, w, h):
    """Dark navy strike-map strip: curved trails, impact dots, labels."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL)
    # faint grid dots
    for gx in range(x + 40, x + w - 20, 46):
        for gy in range(y + 30, y + h - 12, 30):
            draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(58, 84, 118))
    # impact points
    kyiv = (x + 620, y + 66)
    poland = (x + 330, y + 54)
    # flight trails (bezier curves, all inside the panel)
    trails = [
        ((x + 40, y + h - 14), (x + 200, y + 8), poland, GOLD),
        ((x + 90, y + h - 14), (x + 420, y + 4), kyiv, GOLD_LIGHT),
        ((x + w - 40, y + 14), (x + 760, y + h - 8), kyiv, (120, 150, 190)),
    ]
    for p0, p1, p2, color in trails:
        pts = bezier(p0, p1, p2)
        draw.line(pts, fill=color, width=2)
    for pt, label in ((kyiv, "KYIV"), (poland, "POLAND")):
        r = 7
        draw.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r],
                     fill=CRIMSON, outline=WHITE, width=2)
        for rr in (13, 20):
            draw.ellipse([pt[0] - rr, pt[1] - rr, pt[0] + rr, pt[1] + rr],
                         outline=(232, 201, 106), width=1)
        lab = font(SANS_B, 16)
        draw.text((pt[0] + 26, pt[1] - 9), label, font=lab, fill=WHITE)
    # caption
    cap = font(SANS_B, 15)
    draw.text((x + 18, y + 10), "OVERNIGHT STRIKE — UKRAINE & POLAND",
              font=cap, fill=GOLD_LIGHT)
    sub = font(SANS, 14)
    draw.text((x + 18, y + h - 28),
              "Missiles cross into NATO airspace for the first time in the war",
              font=sub, fill=(190, 205, 225))


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48
    content_w = W - 2 * mx

    # --- masthead: crimson band ---
    d.rectangle([0, 0, W, 106], fill=CRIMSON)
    title_f = font(SERIF_B, 58)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 16), title, font=title_f, fill=WHITE)
    sub_f = font(SANS_B, 16)
    sub = "SATURDAY  •  21 NOVEMBER 2026  •  SEVEN STORIES, ONE DAY"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 76), sub, font=sub_f, fill=GOLD_LIGHT)
    # gold rule
    d.rectangle([0, 106, W, 111], fill=GOLD)

    # --- top story label ---
    y = 124
    lab_f = font(SANS_B, 18)
    d.text((mx, y), "TOP STORY", font=lab_f, fill=CRIMSON)
    y += 26

    # --- main headline (serif, up to 2 lines) ---
    head_f, head_lines = fit_lines(d, news["main"]["headline"],
                                   font(SERIF_B, 52), content_w, 2)
    lh = text_h(d, "Ag", head_f) + 6
    for line in head_lines:
        d.text((mx, y), line, font=head_f, fill=INK)
        y += lh
    y += 4

    # --- deck ---
    deck_f, deck_lines = fit_lines(d, news["main"]["deck"],
                                   font(SANS, 23), content_w, 2)
    dlh = text_h(d, "Ag", deck_f) + 5
    for line in deck_lines:
        d.text((mx, y), line, font=deck_f, fill=INK)
        y += dlh
    y += 10

    # --- fact chips ---
    y += draw_chips(d, news["main"]["chips"], mx, y, content_w)
    y += 10

    # --- strike-map strip ---
    draw_map_panel(d, mx, y, content_w, 118)
    y += 118 + 12

    # --- divider ---
    d.line([(mx, y), (W - mx, y)], fill=(200, 190, 170), width=2)
    y += 12

    # --- 2x3 grid of stories ---
    col_w = (content_w - 24) // 2
    row_h = 132
    for idx, story in enumerate(news["stories"]):
        col = idx % 2
        row = idx // 2
        cx = mx + col * (col_w + 24)
        cy = y + row * row_h
        # number badge
        badge = font(SANS_B, 17)
        num = str(idx + 1)
        d.ellipse([cx, cy + 2, cx + 32, cy + 34], fill=CRIMSON)
        nw = d.textlength(num, font=badge)
        d.text((cx + (32 - nw) / 2, cy + 7), num, font=badge, fill=WHITE)
        tx = cx + 44
        tw2 = col_w - 44
        # kicker
        kick_f = font(SANS_B, 14)
        d.text((tx, cy + 2), story["kicker"], font=kick_f, fill=CRIMSON)
        # headline (up to 2 lines)
        h_f, h_lines = fit_lines(d, story["headline"],
                                 font(SANS_B, 21), tw2, 2)
        hy = cy + 24
        hlh = text_h(d, "Ag", h_f) + 3
        for line in h_lines:
            d.text((tx, hy), line, font=h_f, fill=INK)
            hy += hlh
        # summary (up to 2 lines)
        s_f, s_lines = fit_lines(d, story["summary"],
                                 font(SANS, 16), tw2, 2)
        slh = text_h(d, "Ag", s_f) + 3
        sy = hy + 3
        for line in s_lines:
            d.text((tx, sy), line, font=s_f, fill=MUTED)
            sy += slh

    # --- footer band ---
    fy = 930
    d.rectangle([0, fy, W, H], fill=CHARCOAL)
    f1 = font(SERIF_B, 19)
    line1 = "SATURDAY, 21 NOVEMBER 2026"
    w1 = d.textlength(line1, font=f1)
    d.text(((W - w1) / 2, fy + 16), line1, font=f1, fill=WHITE)
    f2 = font(SANS, 14)
    line2 = news["footer"]
    w2 = d.textlength(line2, font=f2)
    d.text(((W - w2) / 2, fy + 48), line2, font=f2, fill=(190, 190, 200))

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])


if __name__ == "__main__":
    main()

"""Seafoam Pop Theme - store promo tiles + long description.

Code-drawn with PIL, colours read from manifest.json (single source of truth).
English only, as required for store assets.

Outputs (relative ASCII paths):
  store-assets/promo/promo-tile-440x280.png
  store-assets/promo/marquee-1400x560.png
  store-assets/store-description.txt

Run from the project root:  python3 scripts/generate-promo.py
"""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PROMO = Path("store-assets") / "promo"
DESC = Path("store-assets") / "store-description.txt"

SS = 2  # supersample factor

FONT_DIR = "C:/Windows/Fonts"


def colors():
    data = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    return data["theme"]["colors"]


def mix(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def font(name, size):
    try:
        return ImageFont.truetype(f"{FONT_DIR}/{name}", size * SS)
    except OSError:
        return ImageFont.load_default()


def grad(w, h, c1, c2, angle=118):
    n = 96
    sm = Image.new("RGB", (n, n))
    px = sm.load()
    ax, ay = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    span = abs(ax) + abs(ay)
    for y in range(n):
        for x in range(n):
            px[x, y] = mix(c1, c2, ((x / (n - 1)) * ax + (y / (n - 1)) * ay) / span)
    return sm.resize((w, h), Image.BICUBIC)


def glow(img, cx, cy, r, color, alpha, blur):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - r, cy - r, cx + r, cy + r],
                                fill=tuple(color) + (alpha,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def logo_tile(size, ink, seafoam, mint):
    """The store icon mark, scaled to `size` (drawn at 8x then downscaled)."""
    ink, seafoam, mint = tuple(ink), tuple(seafoam), tuple(mint)
    s = size * 8
    t = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.219), fill=ink)
    d.ellipse([s * 0.156, s * 0.156, s * 0.844, s * 0.844],
              outline=seafoam, width=int(s * 0.047))
    d.arc([s * 0.215, s * 0.215, s * 0.785, s * 0.785], start=176, end=262,
          fill=mint, width=int(s * 0.039))
    d.ellipse([s * 0.791, s * 0.735, s * 0.94, s * 0.884],
              outline=mint, width=int(s * 0.033))
    return t.resize((size * SS, size * SS), Image.LANCZOS)


def chip(img, x, y, size, radius, color, label=None, txt=None, txt_size=15):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + size, y + size], radius=radius,
                        fill=tuple(color), outline=(0, 0, 0, 26), width=max(1, SS))
    if label and txt is not None:
        txt.text((x + size + 16 * SS, y + (size - txt_size * SS) / 2 - 2 * SS),
                 label, font=txt, fill=(60, 78, 76))


def promo_tile(c):
    W, H = 440, 280
    img = Image.new("RGBA", (W * SS, H * SS), (255, 255, 255, 255))
    img.paste(grad(W * SS, H * SS, c["toolbar"], mix(c["background_tab"], c["frame"], 0.1)))
    glow(img, 360 * SS, 40 * SS, 210 * SS, c["frame"], 90, 90 * SS)

    margin = 32
    right = W - margin
    img.alpha_composite(logo_tile(104, c["tab_text"], c["frame"], c["background_tab"]),
                        (40 * SS, 56 * SS))

    d = ImageDraw.Draw(img)
    f_title = font("arialbd.ttf", 40)
    f_sub = font("arial.ttf", 19)
    ink = tuple(c["tab_text"])
    muted = tuple(c["toolbar_button_icon"])

    d.text((166 * SS, 70 * SS), "Seafoam Pop", font=f_title, fill=ink)
    d.text((170 * SS, 128 * SS), "Chrome Theme", font=f_sub, fill=muted)

    x = 170
    for col in (c["frame"], c["background_tab"], c["toolbar"], c["tab_text"]):
        chip(img, x * SS, 174 * SS, 32 * SS, 10 * SS, col)
        x += 46
    assert x - 14 <= right, "promo swatch row overflows"

    img = img.resize((W, H), Image.LANCZOS)
    out = PROMO / "promo-tile-440x280.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG")
    print("wrote", out)


def marquee(c):
    W, H = 1400, 560
    img = Image.new("RGBA", (W * SS, H * SS), (255, 255, 255, 255))
    img.paste(grad(W * SS, H * SS, c["toolbar"], mix(c["background_tab"], c["frame"], 0.12)))
    glow(img, 1180 * SS, 120 * SS, 320 * SS, c["frame"], 70, 140 * SS)

    margin = 64
    right = W - margin
    ink = tuple(c["tab_text"])
    muted = tuple(c["toolbar_button_icon"])

    img.alpha_composite(logo_tile(220, c["tab_text"], c["frame"], c["background_tab"]),
                        (margin * SS, 142 * SS))

    d = ImageDraw.Draw(img)
    d.text(((margin + 260) * SS, 164 * SS), "Seafoam Pop",
           font=font("arialbd.ttf", 86), fill=ink)
    d.text(((margin + 264) * SS, 284 * SS), "Chrome Theme",
           font=font("arial.ttf", 28), fill=muted)
    d.text(((margin + 264) * SS, 334 * SS), "Light and refreshing, for a serene workspace",
           font=font("arial.ttf", 23), fill=muted)

    x = margin + 264
    for col in (c["frame"], c["background_tab"], c["toolbar"], c["tab_text"]):
        chip(img, x * SS, 398 * SS, 84 * SS, 22 * SS, col)
        x += 102
    swatch_right = x - 18
    assert swatch_right <= right, "marquee swatch row overflows"

    # palette card, right-aligned to the same right baseline as everything else
    card_w, card_h = 430, 336
    cx, cy = right - card_w, 142
    d.rounded_rectangle([cx * SS, cy * SS, right * SS, (cy + card_h) * SS],
                        radius=30 * SS, fill=(255, 255, 255, 242))
    f_card = font("arialbd.ttf", 22)
    f_hex = font("arial.ttf", 16)
    d.text(((cx + 32) * SS, (cy + 26) * SS), "Palette", font=f_card, fill=ink)
    rows = [("Frame", c["frame"]), ("Tab", c["background_tab"]),
            ("Toolbar", c["toolbar"]), ("Ink", c["tab_text"])]
    y = cy + 78
    for label, col in rows:
        chip(img, (cx + 32) * SS, y * SS, 36 * SS, 12 * SS, col)
        d.text(((cx + 84) * SS, (y + 2) * SS), label, font=f_hex, fill=ink)
        hexs = "#%02X%02X%02X" % tuple(col)
        d.text(((cx + 250) * SS, (y + 2) * SS), hexs, font=f_hex, fill=muted)
        y += 58
    assert y - 22 <= cy + card_h - 20, "palette rows overflow the card"
    assert cy + card_h <= H - 12, "palette card breaks the bottom margin"

    img = img.resize((W, H), Image.LANCZOS)
    out = PROMO / "marquee-1400x560.png"
    img.convert("RGB").save(out, "PNG")
    print("wrote", out)


DESCRIPTION = """Seafoam Pop is a soft, light Chrome theme for calm, unhurried browsing: a fresh \
seafoam green frame, pale mint tabs and a gentle lavender-white toolbar, all tied \
together by deep teal text that stays crisp on every light surface. No wallpaper, \
no gradients, no clutter — just five flat colours that keep the browser quiet \
behind your work."""


def main():
    c = colors()
    promo_tile(c)
    marquee(c)
    DESC.parent.mkdir(parents=True, exist_ok=True)
    DESC.write_text(DESCRIPTION + "\n", encoding="utf-8")
    print("wrote", DESC)


if __name__ == "__main__":
    main()

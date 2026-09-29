"""Seafoam Pop Theme - final logo (code-drawn with PIL).

The chosen mark: an outlined soap bubble with a shine arc plus a small
companion bubble on a deep-teal rounded tile. It reads cleanly at 16 px and
keeps the theme's palette.

Chrome theme icons only need 128 px -> logo/logo.png (no size suffix, so it is
easy to find when uploading to the Chrome Web Store).

Run from the project root:  python3 scripts/generate-logo.py
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("logo") / "logo.png"

SIZE = 1024          # render large, downscale for smooth edges
RADIUS = 224         # rounded-square corner radius
ICON = 128


def colors():
    data = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    return data["theme"]["colors"]


def circ(cx, cy, r):
    return [cx - r, cy - r, cx + r, cy + r]


def main():
    c = colors()
    ink = tuple(c["tab_text"])            # (32, 63, 58)
    seafoam = tuple(c["frame"])           # (77, 218, 194)
    mint = tuple(c["background_tab"])     # (210, 254, 243)

    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=ink)

    d.ellipse(circ(512, 512, 352), outline=seafoam, width=48)
    d.arc(circ(512, 512, 292), start=176, end=262, fill=mint, width=40)
    d.ellipse(circ(886, 828, 76), outline=mint, width=34)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    icon = img.resize((ICON, ICON), Image.LANCZOS)
    icon.save(OUT, "PNG")
    print("wrote", OUT, icon.size)


if __name__ == "__main__":
    main()

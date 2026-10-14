#!/usr/bin/env python3
"""Generate the built-in placeholder scene (a simple fort at sunset).

Writes SaudiColoring/Resources/SampleScene/{regions.png,outline.svg,palette.json}
following the scene asset contract in CLAUDE.md, plus a placeholder AppIcon
(the scene coloured in) until the real icon is designed. The app falls back to this
scene for any scene whose approved art is not in the bundle yet, so Fill mode
is playable before real art exists. Not real content: replace, don't extend.

Requires Pillow (pip install pillow). Re-run after changing SHAPES.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "SaudiColoring" / "Resources" / "SampleScene"
ICON = ROOT / "SaudiColoring" / "Resources" / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon.png"
W, H = 2048, 1536
LINE = 8


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def arch_door(x0, y0, x1, y1):
    """Rectangle with a semicircular top."""
    r = (x1 - x0) / 2
    cx, cy = x0 + r, y0 + r
    top = [(cx - r * math.cos(t), cy - r * math.sin(t)) for t in (i * math.pi / 24 for i in range(25))]
    return top + [(x1, y1), (x0, y1)]


def leaf(cx, cy, angle, length=260, width=70):
    """A pointed leaf from (cx, cy) outwards at `angle` degrees."""
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    tip = (cx + dx * length, cy + dy * length)
    mid = (cx + dx * length * 0.5, cy + dy * length * 0.5)
    return [(cx, cy), (mid[0] + nx * width, mid[1] + ny * width), tip, (mid[0] - nx * width, mid[1] - ny * width)]


# Painter's order: later shapes cover earlier ones. (name, kind, geometry, suggested colour)
SHAPES = [
    ("sky", "poly", rect(0, 0, W - 1, 1100), "#7EC8E3"),
    ("sun", "ellipse", (1480, 160, 1820, 500), "#FFC93C"),
    ("cloud", "ellipse", (220, 180, 640, 360), "#FFFFFF"),
    ("dune", "poly", [(0, 1100), (0, 820), (380, 700), (760, 900), (1300, 760), (W - 1, 940), (W - 1, 1100)], "#E8B86D"),
    ("ground", "poly", rect(0, 1100, W - 1, H - 1), "#F2D49B"),
    ("fort", "poly", rect(640, 640, 1400, 1150), "#C68B59"),
    ("left-tower", "poly", [(520, 1150), (560, 470), (740, 470), (780, 1150)], "#B5764A"),
    ("right-tower", "poly", [(1260, 1150), (1300, 470), (1480, 470), (1520, 1150)], "#B5764A"),
    ("left-cap", "poly", rect(540, 400, 760, 480), "#8C5A3C"),
    ("right-cap", "poly", rect(1280, 400, 1500, 480), "#8C5A3C"),
    ("door", "poly", arch_door(920, 860, 1120, 1150), "#6B3E26"),
    ("left-window", "poly", rect(810, 740, 890, 840), "#3D2817"),
    ("right-window", "poly", rect(1150, 740, 1230, 840), "#3D2817"),
    ("path", "poly", [(940, 1150), (1100, 1150), (1260, H - 1), (780, H - 1)], "#E0C9A6"),
    ("palm-trunk", "poly", [(1690, 1300), (1720, 760), (1770, 760), (1790, 1300)], "#8B5A2B"),
] + [
    (f"palm-leaf-{i}", "poly", leaf(1745, 760, angle), "#4CAF50")
    for i, angle in enumerate((200, 250, 290, 340))
]


def region_color(index):
    """A unique, non-black flat colour per shape."""
    rgb = (index + 1) * 0x0F3A71 & 0xFFFFFF
    assert rgb != 0
    return rgb


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<g fill="white" stroke="black" stroke-width="{LINE}" stroke-linejoin="round">']
    ids = {}
    for i, (name, kind, geo, _) in enumerate(SHAPES):
        rgb = region_color(i)
        assert rgb not in ids.values(), name
        ids[name] = rgb
        fill = (rgb >> 16 & 0xFF, rgb >> 8 & 0xFF, rgb & 0xFF)
        # Fill then outline, shape by shape, so a later shape hides earlier outlines it covers.
        if kind == "ellipse":
            draw.ellipse(geo, fill=fill, outline=(0, 0, 0), width=LINE)
            x0, y0, x1, y1 = geo
            svg.append(f'<ellipse cx="{(x0 + x1) / 2:g}" cy="{(y0 + y1) / 2:g}" rx="{(x1 - x0) / 2:g}" ry="{(y1 - y0) / 2:g}"/>')
        else:
            pts = [(round(x), round(y)) for x, y in geo]
            draw.polygon(pts, fill=fill, outline=(0, 0, 0), width=LINE)
            svg.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + '"/>')
    svg += ["</g>", "</svg>"]

    present = {r << 16 | g << 8 | b for _, (r, g, b) in img.getcolors(maxcolors=1 << 16)}
    stray = present - set(ids.values()) - {0}
    assert not stray, f"unexpected colours in map: {sorted(stray)}"

    colours = sorted({c for _, _, _, c in SHAPES}, key=[c for _, _, _, c in SHAPES].index)
    number = {c: n + 1 for n, c in enumerate(colours)}
    palette = [{"regionId": ids[name], "number": number[colour], "color": colour}
               for name, _, _, colour in SHAPES if ids[name] in present]

    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / "regions.png", optimize=True)
    (OUT / "outline.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")
    (OUT / "palette.json").write_text(json.dumps(palette, indent=2) + "\n", encoding="utf-8")
    # Placeholder app icon: the scene coloured with its palette, square crop around the fort.
    lut = {e["regionId"]: tuple(int(e["color"][i:i + 2], 16) for i in (1, 3, 5)) for e in palette}
    raw = img.tobytes()
    coloured = Image.frombytes("RGB", (W, H), b"".join(
        bytes(lut.get(raw[i] << 16 | raw[i + 1] << 8 | raw[i + 2], (0, 0, 0))) for i in range(0, len(raw), 3)))
    ICON.parent.mkdir(parents=True, exist_ok=True)
    coloured.crop((400, 250, 1640, 1490)).resize((1024, 1024), Image.LANCZOS).save(ICON, optimize=True)

    hidden = [name for name, rgb in ids.items() if rgb not in present]
    print(f"wrote {len(palette)} regions, {len(number)} colours to {OUT.relative_to(ROOT)}"
          + (f" (fully covered, dropped: {hidden})" if hidden else ""))


if __name__ == "__main__":
    main()

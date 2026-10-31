#!/usr/bin/env python3
"""Colour the shapes of a scene's line art from a paint list, for line art that arrives without a colour file.

    python3 Scripts/paint_shapes.py Content/Regions/<region>/<scene>
    python3 Scripts/import_illustration.py Content/Regions/<region>/<scene>

Reads <scene>/art/line.png and <scene>/art/paint.json and writes <scene>/art/color.png, every closed
shape of the line art one flat colour. Start from a blank page (or, with "keep": true, from the
current art/color.png, e.g. the colours adopt_line_art.py carried over) and apply in this order:

    {
      "keep": false,                       # optional; true starts from the current color.png
      "base": "#FFFFFF",                   # colour of every shape nothing below touches
      "colors": {"sky": "#8FD3F4", ...},   # optional names, usable anywhere a colour goes
      "zones": [                           # a shape takes a zone's colour when half or more of it is inside
        {"color": "sky", "rect": [0, 0, 2048, 700]},
        {"color": "sand", "poly": [[0, 1100], [2048, 900], [2048, 1536], [0, 1536]]}
      ],
      "fills": [                           # the shape under each point, applied after the zones
        {"color": "skin", "at": [[610, 420], [1220, 380]]}
      ]
    }

Coordinates are pixels of the 2048x1536 art/line.png. A point that lands on a line moves to the
nearest shape within 12 px. Later zones and fills win over earlier ones. Needs Pillow + numpy.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_illustration import INK_LEVEL, label  # noqa: E402
from scene_kit import H, W  # noqa: E402

SNAP = 12


def shapes(line):
    ink = np.asarray(line) < INK_LEVEL
    ink[:4, :] = ink[-4:, :] = True
    ink[:, :4] = ink[:, -4:] = True
    labels, n = label(~ink)
    return ink, labels, n


def hexval(colour, names):
    colour = names.get(colour, colour)
    if not (isinstance(colour, str) and colour.startswith("#") and len(colour) == 7):
        sys.exit(f"bad colour {colour!r}")
    return int(colour[1:], 16)


def shape_at(labels, x, y):
    x, y = min(max(int(x), 0), W - 1), min(max(int(y), 0), H - 1)
    if labels[y, x]:
        return labels[y, x]
    y0, y1, x0, x1 = max(y - SNAP, 0), min(y + SNAP + 1, H), max(x - SNAP, 0), min(x + SNAP + 1, W)
    ys, xs = np.nonzero(labels[y0:y1, x0:x1])
    if ys.size == 0:
        return 0
    k = ((ys + y0 - y) ** 2 + (xs + x0 - x) ** 2).argmin()
    return labels[ys[k] + y0, xs[k] + x0]


def paint(scene_dir):
    art = Path(scene_dir) / "art"
    spec = json.loads((art / "paint.json").read_text(encoding="utf-8"))
    names = spec.get("colors", {})
    line = Image.open(art / "line.png").convert("L")
    if line.size != (W, H):
        sys.exit(f"{scene_dir}: art/line.png is {line.size}, expected {W}x{H}")
    ink, labels, n = shapes(line)
    flat = labels.ravel()
    areas = np.bincount(flat, minlength=n + 1)

    colour = np.full(n + 1, hexval(spec.get("base", "#FFFFFF"), names), np.int64)
    if spec.get("keep") and (art / "color.png").exists():
        rgb = np.asarray(Image.open(art / "color.png").convert("RGB")).astype(np.int64)
        packed = (rgb[..., 0] << 16 | rgb[..., 1] << 8 | rgb[..., 2]).ravel()
        m = flat > 0
        pairs, counts = np.unique(flat[m].astype(np.int64) << 24 | packed[m], return_counts=True)
        best = np.zeros(n + 1, np.int64)
        for lab, col, cnt in zip((pairs >> 24).tolist(), (pairs & 0xFFFFFF).tolist(), counts.tolist()):
            if cnt > best[lab]:
                colour[lab], best[lab] = col, cnt

    for zone in spec.get("zones", []):
        mask = Image.new("L", (W, H), 0)
        draw = ImageDraw.Draw(mask)
        if "rect" in zone:
            draw.rectangle(zone["rect"], fill=1)
        else:
            draw.polygon([tuple(p) for p in zone["poly"]], fill=1)
        inside = np.bincount(flat[np.asarray(mask).ravel() > 0], minlength=n + 1)
        hit = inside * 2 >= areas
        hit[0] = False
        colour[hit] = hexval(zone["color"], names)

    missed = []
    for fill in spec.get("fills", []):
        value = hexval(fill["color"], names)
        for x, y in fill["at"]:
            lab = shape_at(labels, x, y)
            if lab:
                colour[lab] = value
            else:
                missed.append((x, y))
    if missed:
        print(f"WARN {scene_dir}: no shape near {missed}")

    c = np.where(ink, 0, colour[labels])
    rgb = np.stack([c >> 16, c >> 8 & 0xFF, c & 0xFF], axis=-1).astype(np.uint8)
    Image.fromarray(rgb, "RGB").save(art / "color.png", optimize=True)
    print(f"{Path(scene_dir).parent.name}/{Path(scene_dir).name}: painted {n} shapes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        paint(arg)

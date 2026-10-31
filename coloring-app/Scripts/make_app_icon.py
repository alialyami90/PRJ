#!/usr/bin/env python3
"""Draws the app icon: a date palm on a white page, half coloured in, over a band of Al-Sadu weaving,
on the app's palm green. The same palette and Sadu band as the app (SaudiColoring/Features/Theme/).

    python3 Scripts/make_app_icon.py    # writes Resources/Assets.xcassets/AppIcon.appiconset/AppIcon.png (needs Pillow)

Drawn at 4x and scaled down for smooth edges. Opaque, square corners: iOS rounds the corners itself.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ICON = ROOT / "SaudiColoring" / "Resources" / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon.png"

S = 4096
k = S / 1024  # design units are on a 1024 grid

GREEN = (17, 86, 63)          # AppTheme ground
PAGE = (255, 255, 255)
INK = (24, 22, 20)
SAND = (233, 194, 122)
FROND = (62, 155, 79)
FROND_DARK = (40, 118, 60)
TRUNK = (154, 91, 46)
DATE = (226, 166, 59)         # date gold, AppTheme accent
DATE_RED = (194, 87, 43)
SADU_RED = (158, 43, 37)
WOOL = (243, 234, 223)
SADU_BLACK = (30, 21, 19)
SADU_GOLD = (217, 161, 58)

LINE = 13 * k                 # outline width


def u(*xy):
    return [v * k for v in xy]


def frond(base, tip, bend, width, teeth=8):
    """A palm frond: an arched spine from base to tip with a feathered, zigzag edge of leaflets."""
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    cx, cy = (bx + tx) / 2 + nx * bend, (by + ty) / 2 + ny * bend
    left, right = [], []
    steps = teeth * 2
    for i in range(steps + 1):
        t = i / steps
        px = (1 - t) ** 2 * bx + 2 * (1 - t) * t * cx + t * t * tx
        py = (1 - t) ** 2 * by + 2 * (1 - t) * t * cy + t * t * ty
        gx = 2 * (1 - t) * (cx - bx) + 2 * t * (tx - cx)
        gy = 2 * (1 - t) * (cy - by) + 2 * t * (ty - cy)
        g = math.hypot(gx, gy) or 1
        ox, oy = -gy / g, gx / g
        w = width * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.6 * (1 - 0.45 * t)
        if i % 2:  # notch between leaflets
            w *= 0.42
        # leaflets sweep towards the tip
        sx, sy = gx / g * w * 0.5, gy / g * w * 0.5
        left.append((px + ox * w + sx, py + oy * w + sy))
        right.append((px - ox * w + sx, py - oy * w + sy))
    return left + right[::-1]


def palm_shapes():
    """(polygon or ellipse, colour) in painter's order, in 4x pixels."""
    shapes = []
    # Sand dune at the foot of the page.
    shapes.append(("ellipse", u(250, 600, 900, 900), SAND))
    # Trunk: a gently curving taper from the sand up to the crown.
    trunk = []
    for side in (1, -1):
        pts = []
        for i in range(21):
            t = i / 20
            x = 520 + 34 * math.sin(t * math.pi * 0.9) - 10 * t
            y = 690 - 330 * t
            half = 40 - 16 * t
            pts.append(((x + side * half) * k, y * k))
        trunk += pts if side == 1 else pts[::-1]
    shapes.append(("polygon", trunk, TRUNK))
    crown = (512, 340)
    # Each frond arches up from the crown and droops towards its tip.
    fronds = [
        ((222, 530), 140, 66, FROND_DARK), ((802, 530), -140, 66, FROND_DARK),
        ((190, 318), 100, 70, FROND), ((834, 318), -100, 70, FROND),
        ((330, 160), 60, 64, FROND), ((694, 160), -60, 64, FROND),
    ]
    for tip, bend, width, colour in fronds:
        shapes.append(("polygon", frond((crown[0] * k, crown[1] * k), (tip[0] * k, tip[1] * k), bend * k, width * k), colour))
    # Date clusters hanging under the crown.
    for (x, y), c in [((462, 386), DATE), ((496, 404), DATE_RED), ((530, 394), DATE), ((562, 380), DATE_RED),
                      ((478, 434), DATE_RED), ((514, 444), DATE), ((548, 428), DATE)]:
        shapes.append(("ellipse", u(x - 22, y - 26, x + 22, y + 26), c))
    return shapes


def draw_shapes(draw, shapes, coloured, outline):
    for kind, geom, colour in shapes:
        fill = None if outline else (colour if coloured else PAGE)
        if kind == "ellipse":
            draw.ellipse(geom, fill=fill, outline=INK if outline else None, width=int(LINE) if outline else 0)
        else:
            if fill:
                draw.polygon(geom, fill=fill)
            if outline:
                draw.line(geom + [geom[0]], fill=INK, width=int(LINE), joint="curve")


def main():
    img = Image.new("RGB", (S, S), GREEN)

    # The page: a white disc, the palm drawn on it, coloured on the left half and still white on the right.
    disc = u(152, 92, 872, 812)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse(disc, fill=255)

    shapes = palm_shapes()
    coloured = Image.new("RGB", (S, S), PAGE)
    draw_shapes(ImageDraw.Draw(coloured), shapes, coloured=True, outline=False)
    plain = Image.new("RGB", (S, S), PAGE)
    draw_shapes(ImageDraw.Draw(plain), shapes, coloured=False, outline=False)
    # The edge between coloured and not yet coloured: a slight diagonal, like a crayon still on its way.
    half = Image.new("L", (S, S), 0)
    ImageDraw.Draw(half).polygon(u(0, 0, 566, 0, 506, 1024, 0, 1024), fill=255)
    page = Image.composite(coloured, plain, half)
    lines = ImageDraw.Draw(page)
    draw_shapes(lines, shapes, coloured=False, outline=True)
    img.paste(page, (0, 0), mask)
    ImageDraw.Draw(img).ellipse(disc, outline=INK, width=int(18 * k))

    # Al-Sadu band across the foot of the icon.
    d = ImageDraw.Draw(img)
    top, bottom = 836 * k, 984 * k
    h = bottom - top
    d.rectangle([0, top, S, bottom], fill=SADU_RED)
    edge = h * 0.09
    d.rectangle([0, top, S, top + edge], fill=WOOL)
    d.rectangle([0, bottom - edge, S, bottom], fill=WOOL)
    tooth = h * 0.22
    x = 0.0
    while x < S + tooth:
        d.polygon([(x, top + edge), (x + tooth, top + edge), (x + tooth / 2, top + edge + tooth * 0.75)], fill=SADU_BLACK)
        d.polygon([(x, bottom - edge), (x + tooth, bottom - edge), (x + tooth / 2, bottom - edge - tooth * 0.75)], fill=SADU_BLACK)
        x += tooth
    mid, dh = (top + bottom) / 2, h * 0.22
    unit = dh * 2.5
    x, i = 0.0, 0
    while x < S + unit:
        cx = x + unit / 2
        d.polygon([(cx - dh * 1.15, mid), (cx, mid - dh), (cx + dh * 1.15, mid), (cx, mid + dh)],
                  fill=WOOL if i % 2 == 0 else SADU_GOLD)
        d.polygon([(cx - dh * 0.42, mid), (cx, mid - dh * 0.38), (cx + dh * 0.42, mid), (cx, mid + dh * 0.38)], fill=SADU_BLACK)
        x += unit
        i += 1

    ICON.parent.mkdir(parents=True, exist_ok=True)
    img.resize((1024, 1024), Image.LANCZOS).save(ICON, optimize=True)
    print(f"wrote {ICON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

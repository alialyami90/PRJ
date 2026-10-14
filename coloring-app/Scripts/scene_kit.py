"""Scene authoring kit: one scene.py per scene describes shapes in painter's order,
and build() writes the three contract files plus a coloured preview.

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
    from scene_kit import *

    s = Scene()
    s.add("sky", rect(0, 0, W, 1000), SKY)
    s.add("sun", circle(1700, 250, 140), SUN)
    s.extend(person(1000, 1350, 700, outfit="thobe", headwear="shemagh"))
    s.build(__file__)

Outputs (next to scene.py): outline.svg, regions.png, palette.json, preview.png.
Later shapes cover earlier ones. Every shape is a closed polygon (fillable region),
a solid-black "ink" shape (eyes, pupils: part of the outline, not fillable), or an
open "line" (detail stroke drawn in black). Run `python3 scene.py` to build one
scene, or Scripts/build_scenes.py for all.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 2048, 1536
LINE = 8

# Rules the build enforces (see Content/README.md for art direction).
MIN_REGION_PX = 1200      # smaller visible regions are too small for a child's finger
MAX_REGIONS = 90
MAX_COLOURS = 18          # paint-by-number tray size

# ---------------------------------------------------------------- palette
SKY, SKY_DUSK, SUN, CLOUD = "#8FD3F4", "#FFB38A", "#FFD34E", "#FFFFFF"
SAND, DUNE, ROCK, MUD = "#F2D49B", "#E8B86D", "#C98B5A", "#D9A066"
GRASS, LEAF, TRUNK = "#7BC96F", "#4CAF50", "#8B5A2B"
SEA, DEEP_SEA = "#4FC3F7", "#1E88E5"
WHITE, CREAM, SKIN, SKIN2, SKIN3 = "#FFFFFF", "#FFF4DC", "#F1C27D", "#D9A066", "#A86B3C"
RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK = "#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA", "#F06292"
BROWN, DARK_BROWN, GOLD, BLACK_CLOTH, GREY = "#8D6E63", "#5D4037", "#E6B422", "#424242", "#9E9E9E"


# ---------------------------------------------------------------- geometry
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def ellipse(cx, cy, rx, ry, rot=0, n=72):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def circle(cx, cy, r, n=72):
    return ellipse(cx, cy, r, r, n=n)


def smooth(points, iterations=3):
    """Chaikin-smooth a closed polygon: give rough control points, get a soft blob."""
    pts = list(points)
    for _ in range(iterations):
        out = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            out += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        pts = out
    return pts


def smooth_open(points, iterations=3):
    """Chaikin-smooth an open polyline (for curved detail lines)."""
    pts = list(points)
    for _ in range(iterations):
        out = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            out += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        out.append(pts[-1])
        pts = out
    return pts


def arc(cx, cy, rx, ry, start_deg, end_deg, n=24):
    """Points along an elliptical arc (degrees, 0 = right, 90 = down)."""
    return [(cx + rx * math.cos(math.radians(start_deg + (end_deg - start_deg) * i / n)),
             cy + ry * math.sin(math.radians(start_deg + (end_deg - start_deg) * i / n))) for i in range(n + 1)]


def arch(x0, y_top, x1, y_bottom):
    """Rectangle with a semicircular top (doors, windows, niches)."""
    r = (x1 - x0) / 2
    return arc(x0 + r, y_top + r, r, r, 180, 360) + [(x1, y_bottom), (x0, y_bottom)]


def star(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + 180 * i / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def translate(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def scale(pts, s, ox=0, oy=0):
    return [(ox + (x - ox) * s, oy + (y - oy) * s) for x, y in pts]


def mirror(pts, axis_x):
    return [(2 * axis_x - x, y) for x, y in pts]


def rotate(pts, deg, ox, oy):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]


# ---------------------------------------------------------------- scene
class Scene:
    def __init__(self):
        self.items = []  # (kind, name, points, colour, width)

    def add(self, name, points, colour):
        """A fillable region. `colour` is the paint-by-number answer."""
        self.items.append(("region", name, [tuple(p) for p in points], colour, LINE))
        return self

    def ink(self, points):
        """Solid black detail (eyes, pupils, nostrils). Not fillable."""
        self.items.append(("ink", "ink", [tuple(p) for p in points], None, LINE))
        return self

    def line(self, points, width=LINE):
        """Open black stroke (smile, folds, hair strands). Keep it inside one region."""
        self.items.append(("line", "line", [tuple(p) for p in points], None, width))
        return self

    def extend(self, items):
        """Append items produced by a figure helper (list of ("region"|"ink"|"line", ...))."""
        for it in items:
            kind = it[0]
            if kind == "region":
                self.add(it[1], it[2], it[3])
            elif kind == "ink":
                self.ink(it[1])
            else:
                self.line(it[1], *(it[2:] or ()))
        return self

    # ------------------------------------------------------------ build
    def build(self, scene_file):
        out = Path(scene_file).resolve().parent
        img = Image.new("RGB", (W, H), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
               f'<g fill="white" stroke="black" stroke-width="{LINE}" stroke-linejoin="round" stroke-linecap="round">']
        ids, colours, names = {}, {}, {}
        index = 0
        for kind, name, pts, colour, width in self.items:
            ipts = [(round(x), round(y)) for x, y in pts]
            ptxt = " ".join(f"{x},{y}" for x, y in ipts)
            if kind == "region":
                index += 1
                rgb = (index * 0x0F3A71) & 0xFFFFFF
                assert rgb and rgb not in ids.values()
                ids[index] = rgb
                colours[rgb] = colour.upper()
                names[rgb] = name
                draw.polygon(ipts, fill=(rgb >> 16, rgb >> 8 & 0xFF, rgb & 0xFF), outline=(0, 0, 0), width=LINE)
                svg.append(f'<polygon points="{ptxt}"/>')
            elif kind == "ink":
                draw.polygon(ipts, fill=(0, 0, 0), outline=(0, 0, 0))
                svg.append(f'<polygon fill="black" points="{ptxt}"/>')
            else:
                draw.line(ipts, fill=(0, 0, 0), width=width, joint="curve")
                svg.append(f'<polyline fill="none" stroke-width="{width}" points="{ptxt}"/>')
        svg += ["</g>", "</svg>"]
        # Frame so the canvas edge is an outline too.
        draw.rectangle((0, 0, W - 1, H - 1), outline=(0, 0, 0), width=LINE // 2)

        counts = {}
        for n, c in img.getcolors(maxcolors=1 << 20):
            rgb = c[0] << 16 | c[1] << 8 | c[2]
            counts[rgb] = n
        black = counts.pop(0, 0)
        stray = set(counts) - set(colours)
        assert not stray, f"unexpected colours in map: {sorted(stray)[:5]}"

        problems = []
        if black > W * H * 0.2:
            problems.append(f"{100 * black // (W * H)}% of the canvas is black (a gap no shape covers?)")
        tiny = sorted((names[r], n) for r, n in counts.items() if n < MIN_REGION_PX)
        if tiny:
            problems.append(f"{len(tiny)} region(s) under {MIN_REGION_PX}px: " + ", ".join(f"{a}={b}" for a, b in tiny[:40]))
        # Tiny regions are absorbed into the outline so a child can never miss-tap them.
        if tiny:
            px = img.load()
            tiny_ids = {r for r, n in counts.items() if n < MIN_REGION_PX}
            for y in range(H):
                for x in range(W):
                    p = px[x, y]
                    if (p[0] << 16 | p[1] << 8 | p[2]) in tiny_ids:
                        px[x, y] = (0, 0, 0)
            for r in tiny_ids:
                counts.pop(r)

        present = [r for r in ids.values() if r in counts]
        if len(present) > MAX_REGIONS:
            problems.append(f"{len(present)} regions (max {MAX_REGIONS})")
        order = []
        for r in present:
            if colours[r] not in order:
                order.append(colours[r])
        if len(order) > MAX_COLOURS:
            problems.append(f"{len(order)} distinct colours (max {MAX_COLOURS})")
        palette = [{"regionId": r, "number": order.index(colours[r]) + 1, "color": colours[r]} for r in present]

        img.save(out / "regions.png", optimize=True)
        (out / "outline.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")
        (out / "palette.json").write_text(json.dumps(palette, indent=2) + "\n", encoding="utf-8")
        self._preview(img, colours, out / "preview.png")

        summary = f"{out.parent.name}/{out.name}: {len(present)} regions, {len(order)} colours"
        print(summary + ("  WARN " + "; ".join(problems) if problems else ""))
        return {"regions": len(present), "colours": len(order), "problems": problems}

    @staticmethod
    def _preview(img, colours, path):
        lut = {rgb: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for rgb, c in colours.items()}
        raw = img.tobytes()
        buf = bytearray(len(raw))
        cache = {}
        for i in range(0, len(raw), 3):
            key = raw[i:i + 3]
            v = cache.get(key)
            if v is None:
                v = bytes(lut.get(key[0] << 16 | key[1] << 8 | key[2], (0, 0, 0)))
                cache[key] = v
            buf[i:i + 3] = v
        Image.frombytes("RGB", (W, H), bytes(buf)).resize((1024, 768), Image.LANCZOS).save(path, optimize=True)


# ---------------------------------------------------------------- figures
# Figure helpers return item lists for Scene.extend(). Coordinates: (x, feet_y) is the
# point between the feet; h is total height in px. facing: 1 = right, -1 = left.

def _face(cx, cy, r, smile=True, facing=0):
    items = []
    ex = r * 0.36
    off = r * 0.18 * facing
    for sx in (-1, 1):
        items.append(("ink", ellipse(cx + off + sx * ex, cy - r * 0.08, r * 0.11, r * 0.14)))
    if smile:
        items.append(("line", arc(cx + off, cy + r * 0.18, r * 0.32, r * 0.22, 20, 160, 12), max(4, int(r * 0.07))))
    return items


def person(x, feet_y, h, outfit="thobe", headwear="shemagh", skin=SKIN, cloth=WHITE, accent=RED,
           cloak=BROWN, facing=0, arms="down", name="person", child=False, seated=False):
    """A friendly, chunky person.

    outfit:   thobe | bisht (thobe + open cloak in `cloak`) | dress (A-line + hem band in `accent`)
              | abaya | modern (shirt `cloth`, trousers `accent`) | wrap (top `cloth`, knee wrap `accent`, Asiri/Jazani)
    headwear: shemagh (red-white, use accent) | ghutra (white) | taqiyah | headscarf (in `accent`)
              | cap (in `accent`) | straw_hat | flower_crown | turban (in `accent`) | none
    arms:     down | up (waving both) | wave (one up, on the facing side) | out (holding something)
    seated:   True for riders / sitting figures: (x, feet_y) is then the seat point, the robe
              ends there and one leg hangs down on the facing side. h stays the standing height.
    Returns items; the two hand centres are left in person.hands after the call.
    """
    items = []
    if seated:
        feet_y = feet_y + h * 0.5   # the standing feet line, so all proportions below still apply
    head_r = h * (0.13 if child else 0.11)
    head_cy = feet_y - h + head_r
    neck_y = head_cy + head_r * 0.95
    sh_w = h * (0.17 if child else 0.19)
    hem_y = feet_y - h * 0.06 if not seated else feet_y - h * 0.5
    hem_w = sh_w * (1.35 if outfit in ("thobe", "bisht", "abaya", "dress") else 1.0)

    # feet (seated: one leg hanging over the mount on the facing side)
    if seated:
        side = facing or 1
        items.append(("region", f"{name}-leg", [(x + side * sh_w * 0.1, hem_y - h * 0.04), (x + side * sh_w * 0.9, hem_y - h * 0.04),
                                                (x + side * sh_w * 0.75, hem_y + h * 0.26), (x + side * sh_w * 0.2, hem_y + h * 0.26)],
                      accent if outfit == "modern" else (BLACK_CLOTH if outfit == "abaya" else cloth)))
        items.append(("region", f"{name}-shoe", ellipse(x + side * sh_w * 0.6, hem_y + h * 0.27, sh_w * 0.38, h * 0.035), DARK_BROWN))
    for sx in (() if seated else (-1, 1)):
        items.append(("region", f"{name}-shoe", ellipse(x + sx * sh_w * 0.38, feet_y - h * 0.025, sh_w * 0.32, h * 0.035), DARK_BROWN))

    # arms (behind body)
    def arm(side, up):
        sxp = x + side * sh_w * 1.0
        syp = neck_y + h * 0.05
        if up:
            hx, hy = sxp + side * sh_w * 0.55, syp - h * 0.26
        elif arms == "out":
            hx, hy = sxp + side * sh_w * 0.9, syp + h * 0.12
        else:
            hx, hy = sxp + side * sh_w * 0.22, syp + h * 0.36
        dx, dy = hx - sxp, hy - syp
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln * sh_w * 0.28, dx / ln * sh_w * 0.28
        sleeve = cloak if outfit == "bisht" else (BLACK_CLOTH if outfit == "abaya" else cloth)
        items.append(("region", f"{name}-sleeve", [(sxp + nx, syp + ny), (hx + nx * 0.8, hy + ny * 0.8),
                                                  (hx - nx * 0.8, hy - ny * 0.8), (sxp - nx, syp - ny)], sleeve))
        items.append(("region", f"{name}-hand", circle(hx, hy, sh_w * 0.36), skin))
        return (hx, hy)

    hands = []
    for side in (-1, 1):
        up = arms == "up" or (arms == "wave" and side == (facing or 1))
        hands.append(arm(side, up))
    person.hands = hands

    # body
    if seated and outfit in ("modern", "wrap"):
        top = cloth
        items.append(("region", f"{name}-top", smooth([(x - sh_w, neck_y + h * 0.02), (x + sh_w, neck_y + h * 0.02),
                                                       (x + sh_w * 1.05, hem_y), (x - sh_w * 1.05, hem_y)], 2), top))
    elif outfit == "modern":
        waist = feet_y - h * 0.45
        for sx in (-1, 1):
            items.append(("region", f"{name}-leg", [(x + sx * 4, waist), (x + sx * sh_w * 0.9, waist),
                                                    (x + sx * sh_w * 0.75, feet_y - h * 0.04), (x + sx * sh_w * 0.08, feet_y - h * 0.04)], accent))
        items.append(("region", f"{name}-shirt", smooth([(x - sh_w, neck_y + h * 0.02), (x + sh_w, neck_y + h * 0.02),
                                                         (x + sh_w * 0.95, waist + h * 0.03), (x - sh_w * 0.95, waist + h * 0.03)], 2), cloth))
    elif outfit == "wrap":
        waist = feet_y - h * 0.47
        for sx in (-1, 1):
            items.append(("region", f"{name}-leg", rect(x + sx * sh_w * 0.15 - sh_w * 0.2, waist, x + sx * sh_w * 0.15 + sh_w * 0.2 + sx * sh_w * 0.4, feet_y - h * 0.04) if False else
                          [(x + sx * sh_w * 0.12, waist), (x + sx * sh_w * 0.62, waist), (x + sx * sh_w * 0.55, feet_y - h * 0.04), (x + sx * sh_w * 0.15, feet_y - h * 0.04)], skin))
        items.append(("region", f"{name}-top", smooth([(x - sh_w, neck_y + h * 0.02), (x + sh_w, neck_y + h * 0.02),
                                                       (x + sh_w * 0.95, waist), (x - sh_w * 0.95, waist)], 2), cloth))
        items.append(("region", f"{name}-wrap", [(x - sh_w * 1.0, waist - h * 0.02), (x + sh_w * 1.0, waist - h * 0.02),
                                                 (x + sh_w * 1.1, feet_y - h * 0.22), (x - sh_w * 1.1, feet_y - h * 0.22)], accent))
        items.append(("region", f"{name}-belt", rect(x - sh_w * 1.0, waist - h * 0.03, x + sh_w * 1.0, waist + h * 0.035), BROWN))
    else:
        robe = {"thobe": cloth, "bisht": cloth, "dress": cloth, "abaya": BLACK_CLOTH}[outfit]
        items.append(("region", f"{name}-robe", smooth([(x - sh_w, neck_y + h * 0.02), (x + sh_w, neck_y + h * 0.02),
                                                        (x + hem_w, hem_y), (x - hem_w, hem_y)], 1), robe))
        if outfit == "dress":
            items.append(("region", f"{name}-hem", [(x - hem_w * 0.97, hem_y - h * 0.08), (x + hem_w * 0.97, hem_y - h * 0.08),
                                                    (x + hem_w, hem_y), (x - hem_w, hem_y)], accent))
            items.append(("region", f"{name}-yoke", ellipse(x, neck_y + h * 0.07, sh_w * 0.55, h * 0.06), accent))
        if outfit == "thobe":
            items.append(("line", [(x, neck_y + h * 0.03), (x, neck_y + h * 0.16)], 6))
        if outfit == "bisht":
            for sx in (-1, 1):
                items.append(("region", f"{name}-bisht", [(x + sx * sh_w * 0.35, neck_y + h * 0.01), (x + sx * sh_w * 1.15, neck_y + h * 0.03),
                                                          (x + sx * hem_w * 1.12, hem_y - h * 0.03), (x + sx * hem_w * 0.35, hem_y - h * 0.03)], cloak))
                items.append(("region", f"{name}-bisht-trim", [(x + sx * sh_w * 0.35, neck_y + h * 0.01), (x + sx * sh_w * 0.65, neck_y + h * 0.01),
                                                               (x + sx * hem_w * 0.62, hem_y - h * 0.03), (x + sx * hem_w * 0.35, hem_y - h * 0.03)], GOLD))

    # head
    if headwear in ("shemagh", "ghutra"):
        # drape behind the head
        items.append(("region", f"{name}-headcloth", smooth([(x - head_r * 1.25, head_cy - head_r * 0.6), (x + head_r * 1.25, head_cy - head_r * 0.6),
                                                             (x + head_r * 1.45, neck_y + h * 0.08), (x - head_r * 1.45, neck_y + h * 0.08)], 1),
                      accent if headwear == "shemagh" else WHITE))
    if headwear == "headscarf":
        items.append(("region", f"{name}-scarf", smooth([(x - head_r * 1.3, head_cy - head_r * 0.3), (x, head_cy - head_r * 1.35),
                                                         (x + head_r * 1.3, head_cy - head_r * 0.3), (x + head_r * 1.35, neck_y + h * 0.05),
                                                         (x - head_r * 1.35, neck_y + h * 0.05)], 2), accent))
    items.append(("region", f"{name}-face", circle(x, head_cy, head_r), skin))
    items += _face(x, head_cy, head_r, facing=facing)
    if headwear in ("shemagh", "ghutra"):
        items.append(("region", f"{name}-headcloth-top", smooth([(x - head_r * 1.2, head_cy - head_r * 0.2), (x, head_cy - head_r * 1.45),
                                                         (x + head_r * 1.2, head_cy - head_r * 0.2), (x, head_cy - head_r * 0.45)], 1),
                      accent if headwear == "shemagh" else WHITE))
        items.append(("region", f"{name}-agal", [(x - head_r * 0.9, head_cy - head_r * 0.8), (x, head_cy - head_r * 1.25),
                                                 (x + head_r * 0.9, head_cy - head_r * 0.8), (x + head_r * 0.95, head_cy - head_r * 0.5),
                                                 (x, head_cy - head_r * 0.92), (x - head_r * 0.95, head_cy - head_r * 0.5)], BLACK_CLOTH))
    elif headwear == "headscarf":
        items.append(("region", f"{name}-scarf-front", [(x - head_r * 1.0, head_cy - head_r * 0.25), (x, head_cy - head_r * 1.1),
                                                       (x + head_r * 1.0, head_cy - head_r * 0.25), (x, head_cy - head_r * 0.62)], accent))
    elif headwear == "taqiyah":
        items.append(("region", f"{name}-taqiyah", arc(x, head_cy - head_r * 0.45, head_r * 0.85, head_r * 0.55, 180, 360) +
                      [(x + head_r * 0.85, head_cy - head_r * 0.45)], WHITE))
    elif headwear == "cap":
        items.append(("region", f"{name}-cap", arc(x, head_cy - head_r * 0.35, head_r * 0.95, head_r * 0.75, 180, 360), accent))
        items.append(("region", f"{name}-cap-brim", ellipse(x + (facing or 1) * head_r * 0.7, head_cy - head_r * 0.35, head_r * 0.6, head_r * 0.14), accent))
    elif headwear == "straw_hat":
        items.append(("region", f"{name}-hat-brim", ellipse(x, head_cy - head_r * 0.55, head_r * 1.75, head_r * 0.3), "#E9C46A"))
        items.append(("region", f"{name}-hat-top", arc(x, head_cy - head_r * 0.6, head_r * 0.85, head_r * 0.8, 180, 360), "#E9C46A"))
    elif headwear == "turban":
        items.append(("region", f"{name}-turban", smooth([(x - head_r * 1.05, head_cy - head_r * 0.35), (x - head_r * 0.9, head_cy - head_r * 1.2),
                                                          (x + head_r * 0.9, head_cy - head_r * 1.2), (x + head_r * 1.05, head_cy - head_r * 0.35)], 2), accent))
    elif headwear == "flower_crown":
        items.append(("region", f"{name}-crown-band", [(x - head_r * 1.05, head_cy - head_r * 0.45), (x + head_r * 1.05, head_cy - head_r * 0.45),
                                                       (x + head_r, head_cy - head_r * 0.75), (x - head_r, head_cy - head_r * 0.75)], GREEN))
        for i, fx in enumerate((-0.75, -0.25, 0.25, 0.75)):
            items.append(("region", f"{name}-flower", circle(x + fx * head_r * 1.15, head_cy - head_r * 0.85, head_r * 0.26),
                          (YELLOW, ORANGE, PINK, RED)[i]))
    return items


def camel(x, feet_y, h, facing=1, blanket=RED, tassel=YELLOW, body=DUNE, name="camel", saddle=True):
    """Side-view camel; (x, feet_y) = centre of the feet line, h = height to the hump."""
    f = facing
    def P(px, py):  # local coords: x in units of h (positive = front), y up from feet
        return (x + f * px * h, feet_y - py * h)
    items = []
    for i, lx in enumerate((-0.4, -0.24, 0.24, 0.4)):
        items.append(("region", f"{name}-leg", smooth([P(lx - 0.06, 0.58), P(lx + 0.06, 0.58), P(lx + 0.045, 0.03), P(lx - 0.045, 0.03)], 1), body))
    items.append(("region", f"{name}-body", smooth([P(-0.55, 0.62), P(-0.45, 0.85), P(-0.12, 1.0), P(0.12, 0.95), P(0.4, 0.82), P(0.5, 0.62), P(0.2, 0.5), P(-0.4, 0.5)], 3), body))
    items.append(("region", f"{name}-neck", smooth([P(0.38, 0.8), P(0.6, 0.95), P(0.7, 1.15), P(0.82, 1.18), P(0.78, 1.02), P(0.62, 0.75), P(0.48, 0.62)], 2), body))
    items.append(("region", f"{name}-head", smooth([P(0.68, 1.2), P(0.82, 1.27), P(0.98, 1.2), P(1.0, 1.12), P(0.8, 1.1)], 2), body))
    items.append(("ink", circle(*P(0.84, 1.2), h * 0.022)))
    items.append(("region", f"{name}-ear", ellipse(*P(0.72, 1.28), h * 0.045, h * 0.075, rot=-20 * f), body))
    items.append(("region", f"{name}-tail", smooth([P(-0.5, 0.8), P(-0.64, 0.6), P(-0.6, 0.5), P(-0.54, 0.58), P(-0.46, 0.7)], 2), body))
    if saddle:
        items.append(("region", f"{name}-blanket", [P(-0.32, 0.92), P(0.12, 0.92), P(0.18, 0.6), P(-0.38, 0.6)], blanket))
        items.append(("region", f"{name}-blanket-band", [P(-0.36, 0.68), P(0.16, 0.68), P(0.18, 0.6), P(-0.38, 0.6)], tassel))
        for tx in (-0.28, -0.1, 0.08):
            items.append(("region", f"{name}-tassel", [P(tx - 0.05, 0.6), P(tx + 0.05, 0.6), P(tx, 0.48)], tassel))
    return items


def horse(x, feet_y, h, facing=1, body=BROWN, mane=DARK_BROWN, saddle=RED, name="horse"):
    """Side-view Arabian horse; h = height to the back."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    items.append(("region", f"{name}-tail", smooth([P(-0.55, 0.85), P(-0.75, 0.75), P(-0.78, 0.4), P(-0.62, 0.55), P(-0.55, 0.75)], 2), mane))
    for lx in (-0.42, -0.3, 0.32, 0.44):
        items.append(("region", f"{name}-leg", [P(lx - 0.04, 0.6), P(lx + 0.04, 0.6), P(lx + 0.03, 0.06), P(lx - 0.03, 0.06)], body))
        items.append(("region", f"{name}-hoof", rect(*P(lx - 0.04, 0.06), *P(lx + 0.04, 0.0)) if f == 1 else rect(*P(lx + 0.04, 0.06), *P(lx - 0.04, 0.0)), DARK_BROWN))
    items.append(("region", f"{name}-body", smooth([P(-0.55, 0.65), P(-0.5, 0.98), P(0.35, 1.0), P(0.55, 0.85), P(0.5, 0.58), P(-0.4, 0.55)], 3), body))
    items.append(("region", f"{name}-neck", smooth([P(0.35, 0.9), P(0.55, 1.3), P(0.7, 1.35), P(0.62, 0.85)], 2), body))
    items.append(("region", f"{name}-head", smooth([P(0.55, 1.35), P(0.72, 1.48), P(0.95, 1.25), P(0.9, 1.15), P(0.68, 1.2)], 2), body))
    items.append(("region", f"{name}-mane", smooth([P(0.36, 0.98), P(0.5, 1.32), P(0.62, 1.45), P(0.55, 1.25), P(0.45, 0.95)], 2), mane))
    items.append(("region", f"{name}-ear", [P(0.66, 1.42), P(0.7, 1.56), P(0.74, 1.43)], body))
    items.append(("ink", circle(*P(0.76, 1.33), h * 0.025)))
    if saddle:
        items.append(("region", f"{name}-saddle", smooth([P(-0.25, 1.03), P(0.15, 1.03), P(0.2, 0.75), P(-0.3, 0.75)], 1), saddle))
    return items


def palm(x, base_y, h, trunk=TRUNK, leaf=LEAF, dates=True, name="palm"):
    items = []
    top = (x + h * 0.06, base_y - h)
    items.append(("region", f"{name}-trunk", [(x - h * 0.05, base_y), (x + h * 0.05, base_y), (top[0] + h * 0.03, top[1]), (top[0] - h * 0.03, top[1])], trunk))
    for i in range(1, 5):
        yy = base_y - h * i / 5
        items.append(("line", [(x - h * 0.045 + h * 0.012 * i, yy), (x + h * 0.045 + h * 0.012 * i, yy)], 6))
    for ang in (195, 230, 265, 300, 340, 15):
        a = math.radians(ang)
        L = h * 0.48
        tip = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.75 + L * 0.25)
        mid = ((top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2 - h * 0.06)
        nx, ny = -(tip[1] - top[1]) / L * h * 0.09, (tip[0] - top[0]) / L * h * 0.09
        items.append(("region", f"{name}-leaf", smooth([top, (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx, mid[1] - ny)], 2), leaf))
    if dates:
        items.append(("region", f"{name}-dates", smooth([(top[0] - h * 0.1, top[1] + h * 0.02), (top[0] + h * 0.1, top[1] + h * 0.02), (top[0], top[1] + h * 0.2)], 2), ORANGE))
    return items


def cloud(cx, cy, w, name="cloud"):
    """Puffy cloud w px wide; (cx, cy) is the middle of its flat base."""
    ctrl = [(-0.5, 0), (-0.48, -0.16), (-0.32, -0.26), (-0.2, -0.42), (0.02, -0.5), (0.2, -0.38),
            (0.34, -0.32), (0.48, -0.16), (0.5, 0)]
    return [("region", name, smooth([(cx + dx * w, cy + dy * w * 0.6) for dx, dy in ctrl], 3), CLOUD)]


def sun(cx, cy, r, name="sun"):
    return [("region", name, star(cx, cy, r * 1.35, r * 1.05, 12, 0), "#FFE082"), ("region", name + "-disc", circle(cx, cy, r), SUN)]

"""Extra figure helpers for the Jeddah (Hijaz) scenes.

Same conventions as Scripts/scene_kit.py: every helper returns a list of items for
Scene.extend(): ("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403

CORAL_STONE = "#EDE3CF"   # old Jeddah coral-stone walls
TEAL = "#26A69A"
LIGHT_BLUE = "#B3E5FC"


# ---------------------------------------------------------------- geometry helpers
def clip(poly, clip_poly):
    """Sutherland-Hodgman: clip `poly` to the convex polygon `clip_poly`."""
    def area(p):
        return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
    cp = list(clip_poly)
    if area(cp) < 0:
        cp = cp[::-1]
    out = list(poly)
    for i in range(len(cp)):
        a, b = cp[i], cp[(i + 1) % len(cp)]
        def inside(p):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
        def inter(p, q):
            x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
            x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
            d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if d == 0:
                return q
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return out


def bar(p0, p1, w):
    """A straight thick bar (stick, pole, mast) as a closed polygon."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L * w / 2, (x1 - x0) / L * w / 2
    return [(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)]


def tube(points, w, iterations=3):
    """A thick smooth curved band along an open polyline."""
    pts = smooth_open(points, iterations)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        nx, ny = -(b[1] - a[1]) / L * w / 2, (b[0] - a[0]) / L * w / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    return left + right[::-1]


def drop(items, *suffixes):
    """Remove region items whose name ends with any suffix (and nothing else)."""
    return [it for it in items if not (it[0] == "region" and any(it[1].endswith(s) for s in suffixes))]


def insert_after(items, suffix, new):
    """Insert `new` items right after the first region whose name ends with `suffix`."""
    for i, it in enumerate(items):
        if it[0] == "region" and it[1].endswith(suffix):
            return items[:i + 1] + list(new) + items[i + 1:]
    return items + list(new)


def recolour(items, suffix, colour):
    return [("region", it[1], it[2], colour) if it[0] == "region" and it[1].endswith(suffix) else it for it in items]


def geom(x, feet_y, h, child=False):
    """Key body measurements used by scene_kit.person (to attach clothes / props)."""
    head_r = h * (0.13 if child else 0.11)
    head_cy = feet_y - h + head_r
    neck_y = head_cy + head_r * 0.95
    sh_w = h * (0.17 if child else 0.19)
    return dict(head_r=head_r, head_cy=head_cy, neck_y=neck_y, sh_w=sh_w,
                shoulder_y=neck_y + h * 0.05, waist=feet_y - h * 0.45)


# ---------------------------------------------------------------- people
def tulle_girl(x, feet_y, h, dress=PINK, scarf=GOLD, tulle=WHITE, arms="wave", facing=0, name="girl"):
    """Hijazi girl in a puffy layered tulle dress and gold headscarf."""
    items = person(x, feet_y, h, outfit="dress", headwear="headscarf", cloth=dress, accent=scarf,
                   arms=arms, facing=facing, child=True, name=name)
    hands = person.hands
    g = geom(x, feet_y, h, child=True)
    items = drop(items, "-hem")
    waist = feet_y - h * 0.45
    hem = feet_y - h * 0.07
    sw = g["sh_w"]
    layers = []
    # two scalloped tulle layers + sash
    for k, (top, bot, wid, col) in enumerate(((waist, hem, 1.65, tulle), (waist, waist + (hem - waist) * 0.55, 1.4, dress))):
        n = 6
        pts = [(x - sw * 0.9, top), (x + sw * 0.9, top)]
        for i in range(n + 1):
            t = i / n
            px = x + sw * wid - t * 2 * sw * wid
            pts.append((px, bot + (0 if i % 2 == 0 else h * 0.03)))
        layers.append(("region", f"{name}-tulle{k}", smooth(pts, 2), col))
    layers.append(("region", f"{name}-sash", smooth([(x - sw * 0.98, waist - h * 0.04), (x + sw * 0.98, waist - h * 0.04),
                                                     (x + sw * 1.0, waist + h * 0.035), (x - sw * 1.0, waist + h * 0.035)], 1), scarf))
    items = insert_after(items, "-robe", layers)
    person.hands = hands
    return items


def scale_region(items, suffix, k):
    """Scale every region named *suffix about its own centre (make small parts chunkier)."""
    out = []
    for it in items:
        if it[0] == "region" and it[1].endswith(suffix):
            pts = it[2]
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            it = ("region", it[1], [(cx + (px - cx) * k, cy + (py - cy) * k) for px, py in pts], it[3])
        out.append(it)
    return out


def arms_items(x, feet_y, h, child, targets, sleeve, skin, cap=None, name="kid", cap_frac=0.38):
    """Arms from each shoulder to a target hand point. targets = (left, right) points.
    cap: short-sleeve colour (T-shirt) -> arm is skin with a sleeve cap at the shoulder."""
    g = geom(x, feet_y, h, child)
    sw = g["sh_w"]
    items, caps = [], []
    for side, (hx, hy) in zip((-1, 1), targets):
        sx, sy = x + side * sw * 0.85, g["shoulder_y"]
        items.append(("region", f"{name}-sleeve", bar((sx, sy), (hx, hy), sw * 0.5), skin if cap else sleeve))
        if cap:
            cx, cy = sx + (hx - sx) * cap_frac, sy + (hy - sy) * cap_frac
            caps.append(("region", f"{name}-tsleeve", bar((sx - side * sw * 0.05, sy + sw * 0.12), (cx, cy), sw * 0.56), cap))
        items.append(("region", f"{name}-hand", circle(hx, hy, sw * 0.34), skin))
    return items + caps


def arm_target(x, feet_y, h, child, side, kind):
    g = geom(x, feet_y, h, child)
    sw, sy = g["sh_w"], g["shoulder_y"]
    sx = x + side * sw
    if kind == "up":
        return (sx + side * sw * 0.6, sy - h * 0.27)
    if kind == "down":
        return (sx + side * sw * 0.3, sy + h * 0.34)
    if kind == "out":
        return (sx + side * sw * 0.9, sy + h * 0.12)
    return kind


def shorts_kid(x, feet_y, h, shirt=RED, shorts=BLUE, skin=SKIN, headwear="none", cap=RED, arms=("down", "down"),
               facing=0, name="kid", hair_colour=DARK_BROWN, long_trousers=False, scarf_kid=False):
    """Modern child in a T-shirt and shorts (or jeans). arms = (left, right): up | down | out | (x, y)."""
    acc = cap if headwear in ("cap", "headscarf") else skin
    items = person(x, feet_y, h, outfit="modern", headwear=headwear, cloth=shirt, accent=acc,
                   skin=skin, arms="down", facing=facing, child=True, name=name)
    items = drop(items, "-sleeve", "-hand")
    items = recolour(items, "-leg", shorts if long_trousers else skin)
    g = geom(x, feet_y, h, child=True)
    sw, waist, ny = g["sh_w"], g["waist"], g["neck_y"]
    targets = [arm_target(x, feet_y, h, True, side, k) for side, k in zip((-1, 1), arms)]
    arm = arms_items(x, feet_y, h, True, targets, shirt, skin, cap=shirt, name=name)
    person.hands = targets
    # shirt: a cleaner T-shirt shape
    tee = smooth([(x - sw * 0.95, ny + h * 0.02), (x + sw * 0.95, ny + h * 0.02), (x + sw * 1.02, ny + h * 0.06),
                  (x + sw * 0.92, waist + h * 0.04), (x - sw * 0.92, waist + h * 0.04), (x - sw * 1.02, ny + h * 0.06)], 1)
    items = [("region", it[1], tee, it[3]) if it[0] == "region" and it[1].endswith("-shirt") else it for it in items]
    sh = [] if long_trousers else [("region", f"{name}-shorts", [(x - sw * 0.92, waist), (x + sw * 0.92, waist), (x + sw * 1.0, waist + h * 0.2),
                                        (x + sw * 0.06, waist + h * 0.2), (x, waist + h * 0.11), (x - sw * 0.06, waist + h * 0.2),
                                        (x - sw * 1.0, waist + h * 0.2)], shorts)]
    for i, it in enumerate(items):
        if it[0] == "region" and it[1].endswith("-shirt"):
            items = items[:i] + sh + items[i:]
            break
    # arms go behind the shirt, sleeve caps just after the shirt
    for i, it in enumerate(items):
        if it[0] == "region" and it[1].endswith("-shirt"):
            items = items[:i] + [a for a in arm if not a[1].endswith("-tsleeve")] + items[i:i + 1] + \
                [a for a in arm if a[1].endswith("-tsleeve")] + items[i + 1:]
            break
    if headwear == "none":
        items += hair(x, g["head_cy"], g["head_r"], colour=hair_colour, name=name)
    items = scale_region(items, "-cap-brim", 1.35)
    items = scale_region(items, "-shoe", 1.25)
    return items


def hair(cx, cy, r, colour=DARK_BROWN, name="kid"):
    """Short hair cap over the top of a head."""
    pts = arc(cx, cy, r * 1.04, r * 1.04, 190, 350, 20) + [(cx + r * 0.75, cy - r * 0.45), (cx + r * 0.2, cy - r * 0.62),
                                                          (cx - r * 0.3, cy - r * 0.5), (cx - r * 0.85, cy - r * 0.35)]
    return [("region", f"{name}-hair", pts, colour)]


def vest(x, feet_y, h, colour, trim=GOLD, child=False, name="vest", long=False):
    """Hijazi sidriya: sleeveless vest over the robe (two front panels with a trim band)."""
    g = geom(x, feet_y, h, child)
    sw, ny = g["sh_w"], g["neck_y"]
    bot = feet_y - h * (0.36 if long else 0.47)
    items = []
    for sx in (-1, 1):
        items.append(("region", f"{name}-panel", [(x + sx * sw * 0.3, ny + h * 0.01), (x + sx * sw * 1.02, ny + h * 0.03),
                                                  (x + sx * sw * 1.12, bot), (x + sx * sw * 0.2, bot)], colour))
        items.append(("region", f"{name}-trim", [(x + sx * sw * 0.3, ny + h * 0.01), (x + sx * sw * 0.52, ny + h * 0.01),
                                                 (x + sx * sw * 0.42, bot), (x + sx * sw * 0.2, bot)], trim))
    return items


# ---------------------------------------------------------------- animals
def cat(x, base_y, h, fur=ORANGE, facing=1, name="cat", stripes=True, tail_up=True):
    """A friendly sitting cat, front view. (x, base_y) = bottom centre, h = height to ear tips."""
    f = facing
    items = []
    br = h * 0.36
    # tail behind
    if tail_up:
        tp = [(x - f * br * 0.6, base_y - h * 0.08), (x - f * br * 1.5, base_y - h * 0.15), (x - f * br * 1.7, base_y - h * 0.45),
              (x - f * br * 1.45, base_y - h * 0.62)]
    else:
        tp = [(x - f * br * 0.5, base_y - h * 0.06), (x - f * br * 1.3, base_y - h * 0.02), (x - f * br * 1.9, base_y + h * 0.04),
              (x - f * br * 2.3, base_y + h * 0.18)]
    items.append(("region", f"{name}-tail", tube(tp, h * 0.11), fur))
    body = smooth([(x - br * 0.95, base_y), (x - br * 0.85, base_y - h * 0.35), (x - br * 0.45, base_y - h * 0.55),
                   (x + br * 0.45, base_y - h * 0.55), (x + br * 0.85, base_y - h * 0.35), (x + br * 0.95, base_y)], 2)
    items.append(("region", f"{name}-body", body, fur))
    items.append(("region", f"{name}-chest", ellipse(x, base_y - h * 0.25, br * 0.42, h * 0.2), WHITE))
    for sx in (-1, 1):
        items.append(("region", f"{name}-paw", ellipse(x + sx * br * 0.35, base_y - h * 0.035, br * 0.28, h * 0.06), WHITE))
    hr = h * 0.25
    hcy = base_y - h * 0.62
    for sx in (-1, 1):
        items.append(("region", f"{name}-ear", [(x + sx * hr * 0.1, hcy - hr * 0.85), (x + sx * hr * 1.05, hcy - hr * 1.8),
                                                (x + sx * hr * 1.15, hcy - hr * 0.2)], fur))
        items.append(("region", f"{name}-ear-in", [(x + sx * hr * 0.45, hcy - hr * 0.95), (x + sx * hr * 0.98, hcy - hr * 1.55),
                                                   (x + sx * hr * 1.02, hcy - hr * 0.7)], PINK))
    items.append(("region", f"{name}-head", ellipse(x, hcy, hr * 1.18, hr * 0.98), fur))
    items.append(("region", f"{name}-muzzle", ellipse(x, hcy + hr * 0.38, hr * 0.5, hr * 0.33), WHITE))
    for sx in (-1, 1):
        items.append(("ink", ellipse(x + sx * hr * 0.42, hcy - hr * 0.12, hr * 0.11, hr * 0.17)))
        items.append(("line", [(x + sx * hr * 0.55, hcy + hr * 0.38), (x + sx * hr * 1.0, hcy + hr * 0.3)], 5))
        items.append(("line", [(x + sx * hr * 0.55, hcy + hr * 0.5), (x + sx * hr * 1.0, hcy + hr * 0.56)], 5))
    items.append(("ink", [(x - hr * 0.12, hcy + hr * 0.18), (x + hr * 0.12, hcy + hr * 0.18), (x, hcy + hr * 0.32)]))
    items.append(("line", arc(x - hr * 0.12, hcy + hr * 0.36, hr * 0.12, hr * 0.12, 0, 160, 8), 5))
    items.append(("line", arc(x + hr * 0.12, hcy + hr * 0.36, hr * 0.12, hr * 0.12, 20, 180, 8), 5))
    if stripes:
        for sx in (-1, 1):
            items.append(("line", [(x + sx * hr * 0.98, hcy - hr * 0.1), (x + sx * hr * 0.7, hcy - hr * 0.02)], 6))
        items.append(("line", [(x, hcy - hr * 0.95), (x, hcy - hr * 0.6)], 6))
    return items


def cat_walking(x, base_y, h, fur=GREY, facing=1, name="cat2"):
    """Side-view cat walking; (x, base_y) = centre of feet, h = height to ear tip."""
    f = facing
    def P(px, py):
        return (x + f * px * h, base_y - py * h)
    items = []
    items.append(("region", f"{name}-tail", tube([P(-0.45, 0.5), P(-0.7, 0.7), P(-0.72, 1.0), P(-0.6, 1.05)], h * 0.1), fur))
    for lx in (-0.36, -0.16, 0.18, 0.38):
        items.append(("region", f"{name}-leg", smooth([P(lx - 0.08, 0.45), P(lx + 0.08, 0.45), P(lx + 0.08, 0.0), P(lx - 0.08, 0.0)], 1), fur))
    items.append(("region", f"{name}-body", smooth([P(-0.5, 0.45), P(-0.45, 0.68), P(0.3, 0.7), P(0.5, 0.55), P(0.45, 0.32), P(-0.45, 0.3)], 2), fur))
    hc = P(0.52, 0.75)
    hr = h * 0.2
    items.append(("region", f"{name}-ear", [P(0.3, 0.84), P(0.34, 1.2), P(0.56, 0.96)], fur))
    items.append(("region", f"{name}-ear", [P(0.52, 0.97), P(0.72, 1.2), P(0.76, 0.84)], fur))
    items.append(("region", f"{name}-head", ellipse(hc[0], hc[1], hr * 1.05, hr * 0.92), fur))
    items.append(("ink", ellipse(hc[0] + f * hr * 0.15, hc[1] - hr * 0.15, hr * 0.12, hr * 0.17)))
    items.append(("ink", ellipse(hc[0] + f * hr * 0.6, hc[1] - hr * 0.15, hr * 0.1, hr * 0.15)))
    items.append(("ink", [(hc[0] + f * hr * 0.92, hc[1] + hr * 0.12), (hc[0] + f * hr * 0.7, hc[1] + hr * 0.12), (hc[0] + f * hr * 0.82, hc[1] + hr * 0.28)]))
    items.append(("line", arc(hc[0] + f * hr * 0.5, hc[1] + hr * 0.3, hr * 0.25, hr * 0.18, 20, 160, 8), 5))
    return items


def fish(cx, cy, L, colour=YELLOW, facing=1, fin=None, name="fish", bands=None, band_colour=WHITE):
    """Side-view fish, L long. bands: list of x fractions (-0.5..0.5) for vertical bands."""
    f = facing
    fin = fin or colour
    def P(px, py):
        return (cx + f * px * L, cy + py * L)
    items = []
    items.append(("region", f"{name}-tail", smooth([P(-0.28, 0), P(-0.62, -0.3), P(-0.54, 0), P(-0.62, 0.3)], 1), fin))
    items.append(("region", f"{name}-fin", smooth([P(-0.22, -0.12), P(-0.12, -0.46), P(0.06, -0.44), P(0.18, -0.16)], 1), fin))
    body = ellipse(cx, cy, L * 0.38, L * 0.25)
    items.append(("region", f"{name}-body", body, colour))
    for i, bx in enumerate(bands or ()):
        lo, hi = cx + f * (bx - 0.07) * L, cx + f * (bx + 0.07) * L
        lo, hi = min(lo, hi), max(lo, hi)
        items.append(("region", f"{name}-band{i}", clip(body, rect(lo, cy - L, hi, cy + L)), band_colour))
    e = P(0.2, -0.05)
    items.append(("ink", circle(e[0], e[1], L * 0.045)))
    items.append(("line", arc(*P(0.24, 0.07), L * 0.07, L * 0.045, 20, 150, 8), 6))
    return items


def hamour(cx, cy, L, colour="#D9A066", spots=ORANGE, facing=1, name="hamour"):
    """Big chunky grouper with large spots."""
    f = facing
    def P(px, py):
        return (cx + f * px * L, cy + py * L)
    items = []
    items.append(("region", f"{name}-tail", smooth([P(-0.3, 0), P(-0.62, -0.19), P(-0.56, 0), P(-0.62, 0.19)], 1), colour))
    items.append(("region", f"{name}-fin", smooth([P(-0.25, -0.12), P(-0.1, -0.24), P(0.18, -0.2), P(0.2, -0.12)], 1), colour))
    items.append(("region", f"{name}-fin2", smooth([P(-0.15, 0.12), P(-0.02, 0.25), P(0.08, 0.12)], 1), colour))
    body = smooth([P(-0.42, 0), P(-0.25, -0.16), P(0.15, -0.18), P(0.42, -0.06), P(0.45, 0.04), P(0.3, 0.14), P(-0.2, 0.15)], 3)
    items.append(("region", f"{name}-body", body, colour))
    for i, (sx, sy) in enumerate(((-0.17, -0.05), (-0.03, 0.07), (0.07, -0.08))):
        items.append(("region", f"{name}-spot", circle(*P(sx, sy), L * 0.05), spots))
    e = P(0.3, -0.06)
    items.append(("region", f"{name}-eye", circle(e[0], e[1], L * 0.055), WHITE))
    items.append(("ink", circle(e[0] + f * L * 0.012, e[1], L * 0.026)))
    items.append(("line", smooth_open([P(0.33, 0.06), P(0.4, 0.08), P(0.45, 0.03)], 2), 7))
    return items


def turtle(cx, cy, L, shell=BROWN, plate=GOLD, skin=GREEN, facing=1, name="turtle"):
    """Hawksbill sea turtle seen from above-side, gliding; L = shell length."""
    f = facing
    def P(px, py):
        return (cx + f * px * L, cy + py * L)
    items = []
    # flippers
    items.append(("region", f"{name}-flipper", smooth([P(0.12, -0.2), P(0.3, -0.5), P(0.05, -0.62), P(-0.08, -0.3)], 2), skin))
    items.append(("region", f"{name}-flipper", smooth([P(0.12, 0.2), P(0.35, 0.48), P(0.08, 0.55), P(-0.05, 0.28)], 2), skin))
    items.append(("region", f"{name}-flipper", smooth([P(-0.3, -0.15), P(-0.55, -0.3), P(-0.5, -0.12)], 2), skin))
    items.append(("region", f"{name}-flipper", smooth([P(-0.3, 0.15), P(-0.55, 0.3), P(-0.5, 0.12)], 2), skin))
    # head
    items.append(("region", f"{name}-neck", ellipse(*P(0.5, 0.0), L * 0.12, L * 0.09), skin))
    hc = P(0.62, -0.02)
    items.append(("region", f"{name}-head", smooth([P(0.52, -0.12), P(0.7, -0.13), P(0.8, -0.03), P(0.76, 0.06), P(0.55, 0.1)], 2), skin))
    items.append(("ink", circle(*P(0.66, -0.05), L * 0.025)))
    items.append(("line", arc(*P(0.7, 0.02), L * 0.06, L * 0.035, 20, 150, 8), 5))
    # shell + scutes
    sh = ellipse(cx, cy, L * 0.46, L * 0.3)
    items.append(("region", f"{name}-shell", sh, shell))
    inner = ellipse(cx, cy, L * 0.38, L * 0.23)
    hexes = [(0.0, 0.0), (-0.2, 0.0), (0.2, 0.0), (-0.1, -0.15), (0.1, -0.15), (-0.1, 0.15), (0.1, 0.15)][:7 if L < 0 else 7]
    for i, (hx, hy) in enumerate(hexes):
        c = P(hx, hy)
        hexp = [(c[0] + L * 0.085 * math.cos(math.radians(60 * k)), c[1] + L * 0.085 * math.sin(math.radians(60 * k))) for k in range(6)]
        pts = clip(hexp, inner)
        if len(pts) > 2:
            items.append(("region", f"{name}-scute", pts, plate))
    return items


def snorkeler(cx, cy, L, suit=BLUE, trim=YELLOW, skin=SKIN, facing=1, name="snorkeler", hood=None, hair_colour=BROWN):
    """Swimmer floating face-down at the surface, side view; L = body length head to fins."""
    f = facing
    def P(px, py):
        return (cx + f * px * L, cy + py * L)
    items = []
    # far arm stretched forward
    items.append(("region", f"{name}-arm", bar(P(0.15, -0.03), P(0.5, -0.1), L * 0.1), suit))
    items.append(("region", f"{name}-hand", circle(*P(0.52, -0.1), L * 0.06), skin))
    # legs + fins
    items.append(("region", f"{name}-leg", bar(P(-0.15, -0.02), P(-0.42, -0.06), L * 0.12), suit))
    items.append(("region", f"{name}-leg", bar(P(-0.15, 0.04), P(-0.4, 0.12), L * 0.12), suit))
    items.append(("region", f"{name}-fin", smooth([P(-0.4, -0.12), P(-0.66, -0.17), P(-0.68, 0.0), P(-0.42, 0.0)], 1), trim))
    items.append(("region", f"{name}-fin", smooth([P(-0.38, 0.06), P(-0.62, 0.13), P(-0.6, 0.25), P(-0.37, 0.18)], 1), trim))
    # torso
    items.append(("region", f"{name}-body", smooth([P(-0.24, -0.09), P(0.18, -0.11), P(0.27, 0.0), P(0.18, 0.1), P(-0.24, 0.09)], 2), suit))
    items.append(("region", f"{name}-stripe", [P(-0.04, -0.1), P(0.05, -0.105), P(0.05, 0.1), P(-0.04, 0.095)], trim))
    # near arm by the side
    items.append(("region", f"{name}-arm2", bar(P(0.12, 0.05), P(-0.08, 0.14), L * 0.1), suit))
    items.append(("region", f"{name}-hand2", circle(*P(-0.1, 0.15), L * 0.055), skin))
    # head with mask and snorkel
    hc = P(0.35, -0.01)
    hr = L * 0.12
    items.append(("region", f"{name}-snorkel", tube([(hc[0] - f * hr * 0.5, hc[1] - hr * 0.3), (hc[0] - f * hr * 0.75, hc[1] - hr * 1.0),
                                                     (hc[0] - f * hr * 0.7, hc[1] - hr * 2.0)], L * 0.05), trim))
    items.append(("region", f"{name}-head", circle(hc[0], hc[1], hr), skin))
    items.append(("region", f"{name}-hair", clip(circle(hc[0], hc[1], hr), [P(0.1, -0.3), P(0.6, -0.3), P(0.5, -0.06), P(0.1, -0.03)]),
                  hood or hair_colour))
    items.append(("region", f"{name}-strap", bar((hc[0] - f * hr * 0.95, hc[1] - hr * 0.1), (hc[0] + f * hr * 0.3, hc[1] - hr * 0.3), hr * 0.42), trim))
    items.append(("region", f"{name}-mask", smooth([(hc[0] + f * hr * 0.15, hc[1] - hr * 0.6), (hc[0] + f * hr * 1.1, hc[1] - hr * 0.55),
                                                    (hc[0] + f * hr * 1.1, hc[1] + hr * 0.12), (hc[0] + f * hr * 0.15, hc[1] + hr * 0.1)], 2), LIGHT_BLUE))
    items.append(("ink", circle(hc[0] + f * hr * 0.7, hc[1] - hr * 0.22, hr * 0.12)))
    items.append(("line", arc(hc[0] + f * hr * 0.5, hc[1] + hr * 0.42, hr * 0.28, hr * 0.17, 20, 160, 8), 6))
    return items


def seagull(cx, cy, w, body=WHITE, wing=GREY, beak=YELLOW, facing=1, name="gull", flap=1):
    """Flying gull, w = wingspan."""
    f = facing
    items = []
    up = -w * 0.25 * flap
    for sx in (-1, 1):
        items.append(("region", f"{name}-wing", smooth([(cx + sx * w * 0.05, cy - w * 0.02), (cx + sx * w * 0.25, cy + up),
                                                        (cx + sx * w * 0.5, cy + up * 0.6), (cx + sx * w * 0.24, cy + up * 0.5 + w * 0.06),
                                                        (cx + sx * w * 0.06, cy + w * 0.06)], 2), wing))
    items.append(("region", f"{name}-body", ellipse(cx, cy + w * 0.04, w * 0.22, w * 0.095), body))
    hc = (cx + f * w * 0.19, cy - w * 0.02)
    items.append(("region", f"{name}-beak", [(hc[0] + f * w * 0.06, hc[1] - w * 0.015), (hc[0] + f * w * 0.16, hc[1] + w * 0.01), (hc[0] + f * w * 0.06, hc[1] + w * 0.03)], beak))
    items.append(("region", f"{name}-head", circle(hc[0], hc[1], w * 0.1), body))
    items.append(("ink", circle(hc[0] + f * w * 0.025, hc[1] - w * 0.01, w * 0.013)))
    return items


def gull_standing(x, feet_y, h, facing=1, name="gull2"):
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    for lx in (-0.06, 0.1):
        items.append(("region", f"{name}-leg", bar(P(lx, 0.36), P(lx, 0.04), h * 0.1), ORANGE))
        items.append(("region", f"{name}-foot", ellipse(*P(lx + 0.06, 0.03), h * 0.12, h * 0.05), ORANGE))
    items.append(("region", f"{name}-tail", [P(-0.3, 0.62), P(-0.62, 0.66), P(-0.58, 0.48), P(-0.3, 0.45)], GREY))
    items.append(("region", f"{name}-body", smooth([P(-0.42, 0.58), P(0.0, 0.74), P(0.3, 0.62), P(0.27, 0.32), P(-0.1, 0.3)], 2), WHITE))
    items.append(("region", f"{name}-wing", smooth([P(-0.5, 0.6), P(-0.1, 0.7), P(0.15, 0.58), P(-0.1, 0.42)], 2), GREY))
    items.append(("region", f"{name}-beak", [P(0.3, 0.94), P(0.66, 0.85), P(0.3, 0.74)], YELLOW))
    hc = P(0.24, 0.86)
    items.append(("region", f"{name}-head", circle(hc[0], hc[1], h * 0.15), WHITE))
    items.append(("ink", circle(hc[0] + f * h * 0.05, hc[1] - h * 0.03, h * 0.028)))
    return items


def pelican(cx, cy, s, facing=1, name="pelican", pouch=ORANGE, beak=YELLOW, tips=BLACK_CLOTH):
    """Pelican landing: wings raised, feet reaching down. (cx, cy) = body centre, s = size.
    The feet end near P(0.15, 0.56); pelican.feet holds that point."""
    f = facing
    def P(px, py):
        return (cx + f * px * s, cy + py * s)
    def tip_clip(poly, a, b):
        # keep the part of poly beyond the line a->b (towards the wing tip)
        far = [a, b, (b[0] + (b[0] - a[0]) * 0 + (P(-2, -2)[0] - cx) * 0, b[1] - 3 * s), (a[0], a[1] - 3 * s)]
        return clip(poly, far)
    items = []
    far_wing = smooth([P(0.08, -0.1), P(0.22, -0.55), P(0.12, -0.98), P(-0.12, -1.08), P(-0.18, -0.7), P(-0.22, -0.3)], 2)
    items.append(("region", f"{name}-wing-far", far_wing, WHITE))
    items.append(("region", f"{name}-tip-far", clip(far_wing, rect(min(P(-0.5, 0)[0], P(0.5, 0)[0]), cy - 2 * s,
                                                                    max(P(-0.5, 0)[0], P(0.5, 0)[0]), P(0, -0.8)[1])), tips))
    for k, lx in enumerate((0.06, 0.2)):
        items.append(("region", f"{name}-leg", bar(P(lx, 0.15), P(lx + 0.03, 0.5), s * 0.07), pouch))
        items.append(("region", f"{name}-foot", smooth([P(lx - 0.06, 0.5), P(lx + 0.14, 0.5), P(lx + 0.12, 0.58), P(lx - 0.05, 0.58)], 1), pouch))
    pelican.feet = P(0.13, 0.58)
    items.append(("region", f"{name}-tail", [P(-0.42, -0.02), P(-0.66, 0.06), P(-0.42, 0.16)], WHITE))
    items.append(("region", f"{name}-body", smooth([P(-0.5, 0.02), P(-0.3, -0.2), P(0.2, -0.22), P(0.4, -0.05), P(0.32, 0.22), P(-0.1, 0.26), P(-0.45, 0.14)], 3), WHITE))
    items.append(("region", f"{name}-neck", tube([P(0.28, -0.1), P(0.42, -0.35), P(0.36, -0.55), P(0.42, -0.66)], s * 0.15), WHITE))
    hc = P(0.44, -0.7)
    hr = s * 0.12
    items.append(("region", f"{name}-pouch", smooth([P(0.5, -0.66), P(0.88, -0.6), P(0.94, -0.6), P(0.8, -0.47), P(0.6, -0.48), P(0.48, -0.58)], 2), pouch))
    items.append(("region", f"{name}-beak", smooth([P(0.48, -0.76), P(0.9, -0.66), P(0.96, -0.6), P(0.86, -0.6), P(0.48, -0.64)], 1), beak))
    items.append(("region", f"{name}-head", circle(hc[0], hc[1], hr), WHITE))
    items.append(("ink", circle(hc[0] + f * hr * 0.3, hc[1] - hr * 0.2, hr * 0.17)))
    near = smooth([P(-0.02, -0.08), P(-0.2, -0.55), P(-0.52, -0.92), P(-0.78, -0.8), P(-0.62, -0.42), P(-0.38, -0.02)], 2)
    items.append(("region", f"{name}-wing", near, WHITE))
    items.append(("region", f"{name}-tip", clip(near, rect(min(P(-1.2, 0)[0], P(0, 0)[0]), cy - 2 * s, max(P(-1.2, 0)[0], P(0, 0)[0]), P(0, -0.66)[1])), tips))
    items.append(("line", smooth_open([P(-0.18, -0.32), P(-0.34, -0.5), P(-0.5, -0.62)], 2), 6))
    return items


# ---------------------------------------------------------------- props & buildings
def roshan(x0, y0, w, h, wood=BROWN, panel=TRUNK, name="roshan"):
    """Hijazi wooden projecting window box (roshan) with lattice panels, crown and corbel."""
    items = []
    items.append(("region", f"{name}-corbel", smooth([(x0 + w * 0.08, y0 + h), (x0 + w * 0.92, y0 + h), (x0 + w * 0.7, y0 + h * 1.18),
                                                      (x0 + w * 0.3, y0 + h * 1.18)], 1), wood))
    items.append(("region", f"{name}-frame", rect(x0, y0, x0 + w, y0 + h), wood))
    items.append(("region", f"{name}-crown", [(x0 - w * 0.06, y0), (x0 + w * 1.06, y0), (x0 + w * 0.95, y0 - h * 0.12), (x0 + w * 0.05, y0 - h * 0.12)], wood))
    n = 3 if w > 240 else 2
    gap = w * 0.06
    pw = (w - gap * (n + 1)) / n
    for i in range(n):
        px = x0 + gap + i * (pw + gap)
        items.append(("region", f"{name}-panel", rect(px, y0 + h * 0.08, px + pw, y0 + h * 0.6), panel))
        # lattice (decoration inside the panel)
        for k in range(1, 4):
            yy = y0 + h * 0.08 + (h * 0.52) * k / 4
            items.append(("line", [(px + 10, yy), (px + pw - 10, yy)], 5))
        items.append(("line", [(px + pw / 2, y0 + h * 0.08 + 10), (px + pw / 2, y0 + h * 0.6 - 10)], 5))
        items.append(("region", f"{name}-lowpanel", rect(px, y0 + h * 0.68, px + pw, y0 + h * 0.92), panel))
    return items


def boat(cx, wl, L, hull=WHITE, stripe=RED, cabin=YELLOW, facing=1, name="boat"):
    """Small fishing/motor boat sitting on the waterline wl."""
    f = facing
    def P(px, py):
        return (cx + f * px * L, wl - py * L)
    items = []
    items.append(("region", f"{name}-cabin", rect(*sorted_rect(P(-0.25, 0.42), P(0.12, 0.18))), cabin))
    items.append(("region", f"{name}-window", rect(*sorted_rect(P(-0.15, 0.36), P(0.04, 0.24))), LIGHT_BLUE))
    items.append(("region", f"{name}-hull", [P(-0.5, 0.2), P(0.55, 0.22), P(0.38, -0.08), P(-0.42, -0.08)], hull))
    items.append(("region", f"{name}-stripe", [P(-0.48, 0.12), P(0.48, 0.12), P(0.44, 0.05), P(-0.46, 0.05)], stripe))
    return items


def sorted_rect(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])


def dhow(cx, wl, L, hull=BROWN, trim=GOLD, sail=CREAM, facing=1, name="dhow", sail2=True):
    """Traditional dhow: curved wooden hull, high stern, lateen sail(s). Returns items, tiller point in dhow.tiller."""
    f = facing
    def P(px, py):
        return (cx + f * px * L, wl - py * L)
    items = []
    # mast & yard
    items.append(("region", f"{name}-mast", bar(P(0.05, 0.15), P(0.05, 0.88), L * 0.03), DARK_BROWN))
    items.append(("region", f"{name}-yard", bar(P(-0.38, 0.52), P(0.48, 0.96), L * 0.028), DARK_BROWN))
    items.append(("region", f"{name}-sail", smooth([P(-0.36, 0.53), P(0.46, 0.94), P(0.32, 0.58), P(0.05, 0.22), P(-0.3, 0.25)], 1), sail))
    items.append(("region", f"{name}-sail-band", clip(smooth([P(-0.36, 0.53), P(0.46, 0.94), P(0.32, 0.58), P(0.05, 0.22), P(-0.3, 0.25)], 1),
                                                       rect(*sorted_rect(P(-1, 0.5), P(1, 0.4)))), trim))
    if sail2:
        items.append(("region", f"{name}-jib", [P(0.1, 0.9), P(0.55, 0.22), P(0.12, 0.25)], sail))
    # hull
    hp = smooth([P(-0.5, 0.36), P(-0.44, 0.2), P(-0.35, -0.08), P(0.3, -0.08), P(0.5, 0.12), P(0.62, 0.32), P(0.55, 0.3),
                 P(0.3, 0.2), P(-0.3, 0.22)], 2)
    items.append(("region", f"{name}-hull", hp, hull))
    items.append(("region", f"{name}-band", clip(hp, rect(*sorted_rect(P(-1, 0.1), P(1, 0.03)))), trim))
    dhow.tiller = P(-0.4, 0.28)
    dhow.deck = P(-0.25, 0.21)
    return items


def fountain(x, base_y, h, water=LIGHT_BLUE, name="fountain"):
    """King Fahd's Fountain: a very tall jet whose plume blows over and falls like a feather."""
    items = []
    top = base_y - h
    # falling plume (behind the jet), drifting to the right
    items.append(("region", f"{name}-plume", smooth([(x - h * 0.02, top + h * 0.03), (x + h * 0.06, top - h * 0.01), (x + h * 0.16, top + h * 0.05),
                                                    (x + h * 0.24, top + h * 0.2), (x + h * 0.28, top + h * 0.42), (x + h * 0.26, top + h * 0.62),
                                                    (x + h * 0.2, top + h * 0.5), (x + h * 0.15, top + h * 0.62), (x + h * 0.11, top + h * 0.4),
                                                    (x + h * 0.06, top + h * 0.2), (x + h * 0.02, top + h * 0.14)], 3), WHITE))
    items.append(("region", f"{name}-jet", smooth([(x - h * 0.03, base_y), (x - h * 0.03, top + h * 0.1), (x - h * 0.02, top + h * 0.02),
                                                  (x + h * 0.025, top), (x + h * 0.04, top + h * 0.1), (x + h * 0.045, base_y)], 1), water))
    items.append(("region", f"{name}-cap", smooth([(x - h * 0.06, top + h * 0.06), (x - h * 0.05, top - h * 0.03), (x + h * 0.02, top - h * 0.05),
                                                  (x + h * 0.08, top - h * 0.01), (x + h * 0.06, top + h * 0.06)], 2), WHITE))
    items.append(("region", f"{name}-splash", smooth([(x - h * 0.13, base_y + h * 0.02), (x - h * 0.1, base_y - h * 0.04), (x - h * 0.04, base_y - h * 0.02),
                                                     (x + h * 0.0, base_y - h * 0.07), (x + h * 0.06, base_y - h * 0.02), (x + h * 0.12, base_y - h * 0.045),
                                                     (x + h * 0.15, base_y + h * 0.02)], 2), WHITE))
    return items


def scooter(x, ground, h, colour=GREEN, facing=1, name="scooter"):
    """Kick scooter; h = handlebar height; (x, ground) = middle of the deck on the ground."""
    f = facing
    items = []
    wr = h * 0.12
    front = (x + f * h * 0.38, ground - wr)
    back = (x - f * h * 0.35, ground - wr)
    items.append(("region", f"{name}-stem", bar(front, (x + f * h * 0.3, ground - h), h * 0.075), colour))
    items.append(("region", f"{name}-bar", bar((x + f * h * 0.3 - h * 0.17, ground - h), (x + f * h * 0.3 + h * 0.17, ground - h), h * 0.085), colour))
    items.append(("region", f"{name}-deck", rect(min(back[0], front[0]) + wr * 0.4, ground - wr * 1.6, max(back[0], front[0]) - wr * 0.4, ground - wr * 0.6), colour))
    for c in (front, back):
        items.append(("region", f"{name}-wheel", circle(c[0], c[1], wr), BLACK_CLOTH))
        items.append(("region", f"{name}-hub", circle(c[0], c[1], wr * 0.42), GREY))
    scooter.grip = (x + f * h * 0.3 + f * h * 0.02, ground - h)
    return items


def lantern(cx, top_y, s, colour=GOLD, glass=YELLOW, name="lantern"):
    """Hanging Hijazi lantern (fanous). s = height."""
    items = []
    items.append(("region", f"{name}-cap", [(cx - s * 0.08, top_y), (cx + s * 0.08, top_y), (cx + s * 0.3, top_y + s * 0.22), (cx - s * 0.3, top_y + s * 0.22)], colour))
    items.append(("region", f"{name}-glass", [(cx - s * 0.3, top_y + s * 0.22), (cx + s * 0.3, top_y + s * 0.22), (cx + s * 0.22, top_y + s * 0.78),
                                              (cx - s * 0.22, top_y + s * 0.78)], glass))
    items.append(("line", [(cx, top_y + s * 0.26), (cx, top_y + s * 0.74)], 5))
    items.append(("region", f"{name}-base", [(cx - s * 0.26, top_y + s * 0.76), (cx + s * 0.26, top_y + s * 0.76), (cx, top_y + s * 1.05)], colour))
    return items


def drum(cx, cy, r, body=RED, head=CREAM, name="drum"):
    items = []
    items.append(("region", f"{name}-body", [(cx - r, cy), (cx + r, cy), (cx + r * 0.85, cy + r * 1.1), (cx - r * 0.85, cy + r * 1.1)], body))
    items.append(("region", f"{name}-head", ellipse(cx, cy, r, r * 0.3), head))
    items.append(("line", [(cx - r * 0.9, cy + r * 0.1), (cx - r * 0.3, cy + r * 1.05), (cx + r * 0.3, cy + r * 0.1), (cx + r * 0.88, cy + r * 1.05)], 5))
    return items


def coral_branch(x, base_y, h, colour=PINK, name="coral", seed=0):
    """Branching coral made of a few chunky rounded fingers."""
    items = []
    angles = [(-32, 0.8), (0, 1.0), (32, 0.8)]
    h = h * 1.0
    for i, (a, l) in enumerate(angles):
        a = math.radians(a + (seed * 7 % 11) - 5)
        tip = (x + math.sin(a) * h * l, base_y - math.cos(a) * h * l)
        items.append(("region", f"{name}-finger", tube([(x, base_y), ((x + tip[0]) / 2, (base_y + tip[1]) / 2 + h * 0.05), tip], h * 0.16), colour))
    return items


def coral_fan(x, base_y, w, colour=PURPLE, name="fan"):
    items = [("region", f"{name}-stem", bar((x, base_y), (x, base_y - w * 0.3), w * 0.12), colour)]
    items.append(("region", f"{name}", smooth([(x - w * 0.15, base_y - w * 0.28), (x - w * 0.5, base_y - w * 0.5), (x - w * 0.45, base_y - w * 0.85),
                                              (x, base_y - w * 1.0), (x + w * 0.45, base_y - w * 0.85), (x + w * 0.5, base_y - w * 0.5),
                                              (x + w * 0.15, base_y - w * 0.28)], 2), colour))
    for a in (-50, -25, 0, 25, 50):
        r = math.radians(a)
        items.append(("line", [(x, base_y - w * 0.32), (x + math.sin(r) * w * 0.38, base_y - w * 0.32 - math.cos(r) * w * 0.5)], 5))
    return items


def anemone(x, base_y, w, colour=PINK, name="anemone"):
    items = []
    for i in range(7):
        a = math.radians(-75 + i * 25)
        tip = (x + math.sin(a) * w * 0.55, base_y - w * 0.25 - math.cos(a) * w * 0.4)
        items.append(("region", f"{name}-tentacle", tube([(x + math.sin(a) * w * 0.15, base_y - w * 0.2), tip], w * 0.11), colour))
    items.append(("region", f"{name}-base", smooth([(x - w * 0.35, base_y), (x - w * 0.3, base_y - w * 0.28), (x + w * 0.3, base_y - w * 0.28), (x + w * 0.35, base_y)], 2), PURPLE))
    return items


def seaweed(x, base_y, h, colour=GREEN, name="weed"):
    pts = [(x, base_y)]
    for k in range(1, 5):
        pts.append((x + (25 if k % 2 else -25), base_y - h * k / 4))
    return [("region", name, tube(pts, h * 0.09), colour)]


def mosque(cx, base_y, s, wall=WHITE, dome=LIGHT_BLUE, name="mosque"):
    """Simple mosque building: block, central dome, one minaret on the right. s = width of the block."""
    items = []
    # minaret
    mx = cx + s * 0.62
    items.append(("region", f"{name}-minaret", rect(mx - s * 0.07, base_y - s * 1.0, mx + s * 0.07, base_y), wall))
    items.append(("region", f"{name}-balcony", rect(mx - s * 0.1, base_y - s * 0.75, mx + s * 0.1, base_y - s * 0.68), dome))
    items.append(("region", f"{name}-minaret-top", arc(mx, base_y - s * 1.0, s * 0.07, s * 0.14, 180, 360) + [(mx + s * 0.07, base_y - s * 1.0)], dome))
    # dome
    items.append(("region", f"{name}-drum", rect(cx - s * 0.22, base_y - s * 0.62, cx + s * 0.22, base_y - s * 0.48), wall))
    items.append(("region", f"{name}-dome", arc(cx, base_y - s * 0.62, s * 0.24, s * 0.26, 180, 360) + [(cx + s * 0.24, base_y - s * 0.62)], dome))
    # block
    items.append(("region", f"{name}-wall", rect(cx - s * 0.5, base_y - s * 0.5, cx + s * 0.5, base_y), wall))
    for k in range(4):
        wx = cx - s * 0.4 + k * s * 0.23
        items.append(("region", f"{name}-arch", arch(wx, base_y - s * 0.38, wx + s * 0.14, base_y - s * 0.05), dome))
    return items


def wheel(cx, cy, R, bands, tyre=BLACK_CLOTH, spoke=GREY, hub=GREY, name="wheel", spokes=4):
    """Big spoked wheel. The inside shows the background: bands = [(y0, y1, colour, name)], split by spokes
    into separate regions so every piece is its own fillable area."""
    items = [("region", f"{name}-tyre", circle(cx, cy, R), tyre)]
    inner = circle(cx, cy, R * 0.86)
    for k in range(spokes):
        a0 = math.radians(45 + k * 360 / spokes)
        a1 = math.radians(45 + (k + 1) * 360 / spokes)
        wedge = [(cx, cy), (cx + 3 * R * math.cos(a0), cy + 3 * R * math.sin(a0)),
                 (cx + 3 * R * math.cos((a0 + a1) / 2) * 1.5, cy + 3 * R * math.sin((a0 + a1) / 2) * 1.5),
                 (cx + 3 * R * math.cos(a1), cy + 3 * R * math.sin(a1))]
        piece = clip(inner, wedge)
        for y0, y1, col, bn in bands:
            p = clip(piece, rect(cx - 2 * R, y0, cx + 2 * R, y1))
            if len(p) > 2:
                items.append(("region", f"{name}-{bn}", p, col))
    for k in range(spokes):
        a = math.radians(45 + k * 360 / spokes)
        items.append(("region", f"{name}-spoke", bar((cx, cy), (cx + R * 0.88 * math.cos(a), cy + R * 0.88 * math.sin(a)), R * 0.09), spoke))
    items.append(("region", f"{name}-hub", circle(cx, cy, R * 0.16), hub))
    return items

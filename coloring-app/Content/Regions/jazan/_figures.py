"""Extra figure helpers for the Jazan & Farasan scenes.

Every helper returns an item list for Scene.extend():
("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403
from scene_kit import _face  # noqa: E402

STRAW = "#E9C46A"
JASMINE = WHITE
CLAY = "#C1693C"
MANGO = "#FFA726"
HIVIS = "#FF9800"


# ---------------------------------------------------------------- geometry
def tube(center, w0, w1=None, smooth_it=2):
    """A closed polygon around an open centerline, width tapering from w0 to w1."""
    w1 = w0 if w1 is None else w1
    pts = smooth_open(center, smooth_it) if smooth_it else list(center)
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        nx, ny = -dy / ln * w, dx / ln * w
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    return left + right[::-1]


def blob(cx, cy, rx, ry, wobble=0.12, n=10, seed=0, it=3):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + wobble * math.sin(i * 2.7 + seed * 1.3) * (1 if i % 2 else -1)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    return smooth(pts, it)


def insert_before(items, name_suffix, extra):
    """Insert extra items just before the first region whose name ends with name_suffix."""
    for i, it in enumerate(items):
        if it[0] == "region" and it[1].endswith(name_suffix):
            return items[:i] + extra + items[i:]
    return items + extra


# ---------------------------------------------------------------- people extras
def garland(cx, top_y, w, h, name="garland", colour=JASMINE, r=34, **_):
    """A U-shaped jasmine garland hanging from (cx +- w/2, top_y): one region whose outline is a chain of
    round blossoms (the envelope of overlapping circles), with a dot in each blossom."""
    m = 240
    center = [(cx - math.cos(math.pi * k / m) * w / 2, top_y + math.sin(math.pi * k / m) * h) for k in range(m + 1)]
    cum = [0.0]
    for a, b in zip(center, center[1:]):
        cum.append(cum[-1] + math.dist(a, b))
    length = cum[-1]
    n = max(3, round(length / (r * 1.5)) + 1)
    p = length / (n - 1)
    left, right, dots = [], [], []
    for k, (x, y) in enumerate(center):
        a, b = center[max(0, k - 1)], center[min(m, k + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        u = cum[k] - round(cum[k] / p) * p
        d = math.sqrt(max(r * r - u * u, (r * 0.55) ** 2))
        left.append((x + nx * d, y + ny * d))
        right.append((x - nx * d, y - ny * d))
    def cap(c, frm, to):
        a0 = math.atan2(frm[1] - c[1], frm[0] - c[0])
        a1 = math.atan2(to[1] - c[1], to[0] - c[0])
        return a0, a1

    def cap_pts(c, a0, mid, steps=10):
        # half circle from angle a0 passing through angle mid
        sgn = 1 if math.sin(mid - a0) > 0 else -1
        return [(c[0] + r * math.cos(a0 + sgn * math.pi * q / steps), c[1] + r * math.sin(a0 + sgn * math.pi * q / steps)) for q in range(1, steps)]

    t_end = math.atan2(center[-1][1] - center[-2][1], center[-1][0] - center[-2][0])
    t_start = math.atan2(center[0][1] - center[1][1], center[0][0] - center[1][0])
    a_end = math.atan2(left[-1][1] - center[-1][1], left[-1][0] - center[-1][0])
    a_start = math.atan2(right[0][1] - center[0][1], right[0][0] - center[0][0])
    poly = left + cap_pts(center[-1], a_end, t_end) + right[::-1] + cap_pts(center[0], a_start, t_start)
    items = [("region", name, poly, colour)]
    for k in range(n):
        s_ = k * p
        idx = min(range(len(cum)), key=lambda q: abs(cum[q] - s_))
        x, y = center[idx]
        items.append(("ink", circle(x, y, max(6, r * 0.17), n=12)))
    return items


def jasmine_crown(cx, cy, head_r, name="jasmine", n=3):
    """A ring of jasmine flowers across the forehead (on top of a scarf or hair)."""
    items = [("region", f"{name}-band", smooth([(cx - head_r * 1.1, cy - head_r * 0.3), (cx, cy - head_r * 1.0), (cx + head_r * 1.1, cy - head_r * 0.3),
                                                 (cx + head_r * 1.02, cy - head_r * 0.02), (cx, cy - head_r * 0.62), (cx - head_r * 1.02, cy - head_r * 0.02)], 1), GREEN)]
    for i in range(n):
        a = math.radians(215 + 110 * i / (n - 1))
        fx, fy = cx + math.cos(a) * head_r * 1.0, cy - head_r * 0.05 + math.sin(a) * head_r * 0.85
        items.append(("region", f"{name}-flower", star(fx, fy, head_r * 0.45, head_r * 0.28, 5, -90 + i * 20), JASMINE))
        items.append(("ink", circle(fx, fy, head_r * 0.07, n=12)))
    return items


def hard_hat(cx, cy, head_r, colour=YELLOW, name="hardhat"):
    return [("region", f"{name}-dome", arc(cx, cy - head_r * 0.35, head_r * 1.0, head_r * 0.95, 180, 360), colour),
            ("region", f"{name}-brim", [(cx - head_r * 1.3, cy - head_r * 0.42), (cx + head_r * 1.3, cy - head_r * 0.42),
                                        (cx + head_r * 1.3, cy - head_r * 0.12), (cx - head_r * 1.3, cy - head_r * 0.12)], colour),
            ("region", f"{name}-ridge", [(cx - head_r * 0.22, cy - head_r * 1.33), (cx + head_r * 0.22, cy - head_r * 1.33),
                                         (cx + head_r * 0.22, cy - head_r * 0.42), (cx - head_r * 0.22, cy - head_r * 0.42)], colour)]


# ---------------------------------------------------------------- animals
def flamingo(x, feet_y, h, facing=1, name="flamingo", body=PINK, pose="one-leg", head_down=False):
    """Standing flamingo: (x, feet_y) is the foot of the standing leg, h total height."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)

    items = []
    lw = h * 0.042
    items.append(("region", f"{name}-leg", tube([P(0.0, 0.0), P(0.0, 0.25), P(0.01, 0.55)], lw), body))
    items.append(("ink", ellipse(*P(0.03, 0.0), h * 0.05, h * 0.016)))
    if pose == "one-leg":
        items.append(("region", f"{name}-leg2", tube([P(0.03, 0.52), P(0.15, 0.38), P(0.0, 0.33)], lw * 0.95, smooth_it=0), body))
    else:
        items.append(("region", f"{name}-leg2", tube([P(0.12, 0.0), P(0.1, 0.25), P(0.05, 0.55)], lw), body))
        items.append(("ink", ellipse(*P(0.15, 0.0), h * 0.05, h * 0.016)))
    items.append(("region", f"{name}-tail", smooth([P(-0.14, 0.66), P(-0.33, 0.66), P(-0.36, 0.6), P(-0.16, 0.56)], 2), body))
    items.append(("region", f"{name}-body", smooth([P(-0.2, 0.66), P(-0.05, 0.72), P(0.14, 0.7), P(0.2, 0.6), P(0.08, 0.5), P(-0.15, 0.53)], 3), body))
    items.append(("region", f"{name}-wing", smooth([P(-0.17, 0.64), P(0.0, 0.69), P(0.12, 0.64), P(0.02, 0.56), P(-0.22, 0.58)], 2), "#F8BBD0"))
    items.append(("line", smooth_open([P(-0.12, 0.62), P(-0.02, 0.62), P(0.06, 0.63)], 1), 6))
    if head_down:
        neck = [P(0.15, 0.66), P(0.27, 0.74), P(0.33, 0.6), P(0.35, 0.42), P(0.39, 0.33)]
        hx, hy = 0.41, 0.3
    else:
        neck = [P(0.14, 0.66), P(0.24, 0.76), P(0.19, 0.86), P(0.15, 0.93), P(0.2, 0.98)]
        hx, hy = 0.23, 0.96
    items.append(("region", f"{name}-neck", tube(neck, h * 0.07, h * 0.06), body))
    hr = h * 0.068
    items.append(("region", f"{name}-head", circle(*P(hx, hy), hr), body))
    # bent beak: cream base, black tip
    b0 = hx + 0.04
    items.append(("region", f"{name}-beak", smooth([P(b0, hy + 0.04), P(b0 + 0.08, hy + 0.025), P(b0 + 0.12, hy - 0.02), P(b0 + 0.13, hy - 0.08),
                                                     P(b0 + 0.075, hy - 0.04), P(b0 - 0.01, hy - 0.035)], 1), CREAM))
    items.append(("ink", smooth([P(b0 + 0.095, hy + 0.0), P(b0 + 0.12, hy - 0.02), P(b0 + 0.13, hy - 0.08), P(b0 + 0.09, hy - 0.045)], 1)))
    items.append(("ink", circle(*P(hx + 0.01, hy + 0.015), h * 0.014, n=16)))
    return items


def heron(x, feet_y, h, facing=1, name="heron", body=GREY, wing="#607D8B"):
    """Grey heron standing tall."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)

    items = []
    for lx in (-0.04, 0.06):
        items.append(("region", f"{name}-leg", tube([P(lx, 0.0), P(lx + 0.01, 0.25), P(0.0, 0.48)], h * 0.03), YELLOW))
        items.append(("line", [P(lx - 0.07, 0.0), P(lx + 0.09, 0.0)], 8))
    items.append(("region", f"{name}-tail", [P(-0.2, 0.62), P(-0.36, 0.4), P(-0.22, 0.42)], body))
    items.append(("region", f"{name}-body", ellipse(*P(-0.02, 0.56), h * 0.2, h * 0.11, rot=-28 * f), body))
    items.append(("region", f"{name}-wing", smooth([P(-0.17, 0.66), P(0.06, 0.7), P(0.12, 0.6), P(-0.06, 0.48), P(-0.3, 0.44)], 2), wing))
    items.append(("region", f"{name}-neck", tube([P(0.12, 0.62), P(0.2, 0.74), P(0.13, 0.86), P(0.16, 0.95)], h * 0.07, h * 0.06), WHITE))
    items.append(("region", f"{name}-crest", [P(0.16, 1.0), P(-0.04, 1.02), P(0.12, 0.94)], BLACK_CLOTH))
    items.append(("region", f"{name}-head", ellipse(*P(0.18, 0.96), h * 0.07, h * 0.058), WHITE))
    items.append(("region", f"{name}-beak", [P(0.22, 0.985), P(0.46, 0.95), P(0.22, 0.925)], YELLOW))
    items.append(("ink", circle(*P(0.2, 0.97), h * 0.014, n=16)))
    return items


def crab(cx, cy, s, name="crab", colour=RED, wave=False):
    """Front-view crab, s = body width."""
    items = []
    for sx in (-1, 1):
        for k in range(3):
            items.append(("line", [(cx + sx * s * 0.35, cy + s * (0.02 + k * 0.1)), (cx + sx * s * 0.62, cy + s * (0.0 + k * 0.12)),
                                   (cx + sx * s * 0.72, cy + s * (0.18 + k * 0.1))], max(6, int(s * 0.05))))
        ay = -0.5 if (wave and sx == 1) else -0.25
        items.append(("region", f"{name}-arm", tube([(cx + sx * s * 0.3, cy - s * 0.05), (cx + sx * s * 0.55, cy + s * (ay + 0.05))], s * 0.16, smooth_it=0), colour))
        clx, cly = cx + sx * s * 0.6, cy + s * (ay - 0.06)
        items.append(("region", f"{name}-claw", [*arc(clx, cly, s * 0.17, s * 0.17, 0 if sx == 1 else 180, 300 if sx == 1 else 480, 14), (clx, cly)], colour))
    items.append(("region", f"{name}-body", ellipse(cx, cy, s * 0.42, s * 0.28), colour))
    for sx in (-1, 1):
        items.append(("line", [(cx + sx * s * 0.12, cy - s * 0.2), (cx + sx * s * 0.15, cy - s * 0.38)], 6))
        items.append(("ink", circle(cx + sx * s * 0.15, cy - s * 0.42, s * 0.06, n=16)))
    items.append(("line", arc(cx, cy - s * 0.02, s * 0.14, s * 0.1, 20, 160, 10), 6))
    return items


def goat(x, feet_y, h, facing=1, name="goat", body=WHITE, patch=BROWN):
    """Small side-view goat; h = height to the back."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)

    items = []
    for lx in (-0.42, -0.28, 0.28, 0.42):
        items.append(("region", f"{name}-leg", [P(lx - 0.07, 0.55), P(lx + 0.07, 0.55), P(lx + 0.06, 0.0), P(lx - 0.06, 0.0)], body))
    items.append(("region", f"{name}-tail", smooth([P(-0.45, 0.92), P(-0.74, 1.2), P(-0.62, 0.78)], 1), body))
    items.append(("region", f"{name}-body", smooth([P(-0.56, 0.6), P(-0.52, 0.98), P(0.45, 1.0), P(0.55, 0.62), P(0.2, 0.45), P(-0.4, 0.45)], 3), body))
    items.append(("region", f"{name}-patch", blob(*P(-0.15, 0.78), h * 0.2, h * 0.14, seed=3), patch))
    items.append(("region", f"{name}-head", smooth([P(0.38, 0.85), P(0.48, 1.3), P(0.62, 1.38), P(0.8, 1.15), P(0.75, 1.02), P(0.55, 0.9)], 2), body))
    items.append(("region", f"{name}-horn", tube([P(0.52, 1.32), P(0.44, 1.54), P(0.3, 1.62)], h * 0.13, h * 0.07), DARK_BROWN))
    items.append(("region", f"{name}-ear", ellipse(*P(0.42, 1.2), h * 0.16, h * 0.075, rot=25 * f), patch))
    items.append(("ink", [P(0.66, 1.06), P(0.8, 1.04), P(0.7, 0.86)]))
    items.append(("ink", circle(*P(0.6, 1.24), h * 0.03, n=16)))
    items.append(("line", arc(*P(0.73, 1.1), h * 0.05, h * 0.03, 20, 160, 8), 5))
    return items


# ---------------------------------------------------------------- props & places
def thatched_hut(cx, base_y, w, h, wall=MUD, roof=STRAW, door=DARK_BROWN, name="hut", band=None):
    """Jazani 'ishsha': round hut with a tall conical straw roof."""
    items = []
    wall_top = base_y - h * 0.42
    items.append(("region", f"{name}-wall", [(cx - w * 0.42, wall_top), (cx + w * 0.42, wall_top), (cx + w * 0.44, base_y), (cx - w * 0.44, base_y)], wall))
    if band:
        items.append(("region", f"{name}-band", [(cx - w * 0.425, wall_top + h * 0.06), (cx + w * 0.425, wall_top + h * 0.06),
                                                  (cx + w * 0.43, wall_top + h * 0.13), (cx - w * 0.43, wall_top + h * 0.13)], band))
    items.append(("region", f"{name}-door", arch(cx - w * 0.11, base_y - h * 0.3, cx + w * 0.11, base_y), door))
    items.append(("region", f"{name}-roof", smooth([(cx - w * 0.55, wall_top + h * 0.04), (cx - w * 0.2, base_y - h * 0.82), (cx, base_y - h),
                                                    (cx + w * 0.2, base_y - h * 0.82), (cx + w * 0.55, wall_top + h * 0.04), (cx, wall_top - h * 0.02)], 1), roof))
    # thatch strokes
    for k in (-0.3, -0.12, 0.06, 0.22):
        items.append(("line", [(cx + w * k * 0.35, base_y - h * 0.86), (cx + w * k * 1.2, wall_top - h * 0.02)], 5))
    items.append(("region", f"{name}-tip", [(cx - w * 0.06, base_y - h * 0.95), (cx, base_y - h * 1.12), (cx + w * 0.06, base_y - h * 0.95)], roof))
    return items


def clay_pot(cx, base_y, w, h, colour=CLAY, name="pot", lid=None):
    items = [("region", f"{name}", smooth([(cx - w * 0.28, base_y - h * 0.9), (cx - w * 0.5, base_y - h * 0.5), (cx - w * 0.35, base_y),
                                          (cx + w * 0.35, base_y), (cx + w * 0.5, base_y - h * 0.5), (cx + w * 0.28, base_y - h * 0.9)], 2), colour),
             ("region", f"{name}-rim", rect(cx - w * 0.32, base_y - h * 1.0, cx + w * 0.32, base_y - h * 0.84), colour)]
    items.append(("line", smooth_open([(cx - w * 0.42, base_y - h * 0.5), (cx, base_y - h * 0.44), (cx + w * 0.42, base_y - h * 0.5)], 2), 6))
    if lid:
        items.append(("region", f"{name}-lid", arc(cx, base_y - h * 1.0, w * 0.3, h * 0.2, 180, 360), lid))
    return items


def woven_basket(cx, top_y, w, h, colour=STRAW, band=RED, name="basket"):
    items = [("region", name, [(cx - w / 2, top_y), (cx + w / 2, top_y), (cx + w * 0.38, top_y + h), (cx - w * 0.38, top_y + h)], colour),
             ("region", f"{name}-band", [(cx - w * 0.47, top_y + h * 0.3), (cx + w * 0.47, top_y + h * 0.3),
                                         (cx + w * 0.43, top_y + h * 0.58), (cx - w * 0.43, top_y + h * 0.58)], band)]
    for k in (-0.25, 0.0, 0.25):
        items.append(("line", [(cx + w * k, top_y + h * 0.62), (cx + w * k * 0.85, top_y + h * 0.95)], 5))
    return items


def boat(cx, water_y, L, hull=WHITE, stripe=BLUE, name="boat", facing=1, cabin=None):
    """Small fishing boat (a Red Sea 'houri'). water_y = waterline, L = length."""
    f = facing

    def P(px, py):
        return (cx + f * px * L, water_y - py * L)

    items = []
    if cabin:
        items.append(("region", f"{name}-cabin", [P(-0.35, 0.18), P(-0.05, 0.18), P(-0.05, 0.38), P(-0.35, 0.38)], cabin))
        items.append(("region", f"{name}-cabin-window", rect(*sorted_rect(P(-0.3, 0.25), P(-0.12, 0.33))), SEA))
        items.append(("region", f"{name}-roof", [P(-0.39, 0.38), P(-0.01, 0.38), P(-0.03, 0.43), P(-0.37, 0.43)], stripe))
    items.append(("region", f"{name}-hull", smooth([P(-0.5, 0.2), P(0.56, 0.24), P(0.42, 0.04), P(0.3, -0.04), P(-0.42, -0.04), P(-0.5, 0.06)], 1), hull))
    items.append(("region", f"{name}-stripe", [P(-0.49, 0.14), P(0.5, 0.165), P(0.47, 0.115), P(-0.48, 0.09)], stripe))
    return items


def sorted_rect(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])


def fish(cx, cy, L, colour=ORANGE, name="fish", facing=1):
    f = facing
    items = [("region", f"{name}-tail", [(cx - f * L * 0.35, cy), (cx - f * L * 0.6, cy - L * 0.2), (cx - f * L * 0.6, cy + L * 0.2)], colour),
             ("region", name, ellipse(cx, cy, L * 0.4, L * 0.2), colour),
             ("ink", circle(cx + f * L * 0.22, cy - L * 0.04, L * 0.035, n=12))]
    return items


def mango_tree(cx, base_y, h, name="mangotree", fruit_pos=(), leaf=LEAF):
    """Round mango tree with a sturdy trunk; fruit_pos = list of (dx, dy) in units of h from crown centre."""
    items = []
    items.append(("region", f"{name}-trunk", smooth([(cx - h * 0.08, base_y), (cx - h * 0.05, base_y - h * 0.45), (cx - h * 0.15, base_y - h * 0.62),
                                                     (cx + h * 0.15, base_y - h * 0.62), (cx + h * 0.05, base_y - h * 0.45), (cx + h * 0.09, base_y)], 1), TRUNK))
    ccx, ccy = cx, base_y - h * 0.68
    items.append(("region", f"{name}-crown", smooth([(ccx - h * 0.5, ccy + h * 0.12), (ccx - h * 0.52, ccy - h * 0.15), (ccx - h * 0.3, ccy - h * 0.32),
                                                     (ccx, ccy - h * 0.36), (ccx + h * 0.32, ccy - h * 0.3), (ccx + h * 0.52, ccy - h * 0.12),
                                                     (ccx + h * 0.48, ccy + h * 0.14), (ccx + h * 0.2, ccy + h * 0.2), (ccx - h * 0.2, ccy + h * 0.2)], 3), leaf))
    for i, (dx, dy) in enumerate(fruit_pos):
        mx, my = ccx + dx * h, ccy + dy * h
        items.append(("region", f"{name}-mango", ellipse(mx, my, h * 0.05, h * 0.07, rot=15), MANGO))
    return items


def mango(cx, cy, s, rot=15, name="mango", leaf=None):
    items = [("region", name, ellipse(cx, cy, s * 0.42, s * 0.55, rot=rot), MANGO)]
    if leaf if leaf is not None else s >= 140:
        items.append(("region", f"{name}-leaf", ellipse(cx + s * 0.3, cy - s * 0.6, s * 0.34, s * 0.15, rot=-30), LEAF))
    else:
        items.append(("line", [(cx + s * 0.05, cy - s * 0.5), (cx + s * 0.15, cy - s * 0.72)], 8))
    return items


def crate(x0, y0, x1, y1, colour=BROWN, name="crate"):
    items = [("region", name, rect(x0, y0, x1, y1), colour)]
    for k in (0.35, 0.68):
        y = y0 + (y1 - y0) * k
        items.append(("line", [(x0 + 10, y), (x1 - 10, y)], 6))
    return items


def mountain_terraces(base_y, peak_x, peak_y, half_w, n, colours, name="terrace", outline_col=None):
    """A mountain as stacked terraced bands (bottom to top); each band is a region."""
    items = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        y0 = base_y - (base_y - peak_y) * t0
        y1 = base_y - (base_y - peak_y) * t1
        w0 = half_w * (1 - t0) + 30
        w1 = half_w * (1 - t1) + 30
        band = smooth([(peak_x - w0, y0), (peak_x - w1 - 8, y1 + 8), (peak_x - w1, y1), (peak_x + w1, y1), (peak_x + w1 + 8, y1 + 8), (peak_x + w0, y0)], 1)
        items.append(("region", f"{name}{i}", band, colours[i % len(colours)]))
    return items


# ---------------------------------------------------------------- a friendlier person
def folk(x, feet_y, h, name="p", skin=SKIN, top=WHITE, bottom=BLUE, bottom_style="trousers",
         sleeves="long", sleeve_col=None, head="none", head_col=RED, hair=DARK_BROWN, extra=None,
         arms=("down", "down"), facing=0, child=False, seated=False, shoes=DARK_BROWN, hands_xy=None, belt=BROWN):
    """Chunky friendly person, front view.

    bottom_style: trousers | shorts | wrap (knee/shin futa, bare legs) | dress (long A-line from the
                  shoulders, `top` colour, `bottom` = hem band) | skirt (long skirt from waist)
    sleeves:      long | short
    head:         none | cap | straw_hat | turban | headscarf | hardhat | flower_band | jasmine | helmet
    extra:        None | jacket | vest | hivis | lifejacket  (drawn over the top, `extra_col` = bottom of tuple)
                  pass as (kind, colour)
    arms:         per arm (left, right on screen): down | up | wave | out | hold | reach | (dx, dy) hand
                  offset from the shoulder in units of h
    seated:       sitting cross-legged; (x, feet_y) is then the floor point under the hips.
    Returns items; hand centres are in folk.hands, head centre/radius in folk.head.
    """
    items = []
    hr = h * (0.145 if child else 0.12)
    if seated:
        # a seated figure is about 55% of standing height
        hip_y = feet_y - h * 0.08
        sh_y = hip_y - h * 0.32
    else:
        hip_y = feet_y - h * 0.47
        sh_y = feet_y - h + hr * 2 + h * 0.03
    head_cy = sh_y - h * 0.03 - hr
    sh = h * (0.15 if child else 0.16)
    wa = sh * 0.85
    folk.head = (x, head_cy, hr)
    sleeve_col = sleeve_col or top
    ext_kind, ext_col = (extra if extra else (None, None))

    # ----- hair behind head (long hair for girls without scarf handled by caller via head)
    # ----- legs / bottom
    ankle = feet_y - h * 0.04
    if seated:
        lap = smooth([(x - h * 0.3, feet_y), (x - h * 0.32, feet_y - h * 0.08), (x - h * 0.18, hip_y - h * 0.02), (x + h * 0.18, hip_y - h * 0.02),
                      (x + h * 0.32, feet_y - h * 0.08), (x + h * 0.3, feet_y)], 2)
        items.append(("region", f"{name}-lap", lap, top if bottom_style == "dress" else bottom))
        for sx in (-1, 1):
            items.append(("region", f"{name}-foot", ellipse(x + sx * h * 0.1, feet_y - h * 0.035, h * 0.07, h * 0.035), skin if bottom_style == "wrap" else shoes))
    else:
        for sx in (-1, 1):
            items.append(("region", f"{name}-shoe", ellipse(x + sx * sh * 0.5, feet_y - h * 0.03, sh * 0.45, h * 0.042), shoes))
        if bottom_style in ("trousers", "shorts", "wrap"):
            leg_bot = ankle if bottom_style == "trousers" else ankle
            for sx in (-1, 1):
                leg = [(x + sx * 3, hip_y - h * 0.02), (x + sx * wa * 0.98, hip_y - h * 0.02), (x + sx * sh * 0.78, leg_bot), (x + sx * sh * 0.18, leg_bot)]
                items.append(("region", f"{name}-leg", leg, bottom if bottom_style == "trousers" else skin))
            if bottom_style == "shorts":
                for sx in (-1, 1):
                    items.append(("region", f"{name}-shorts", [(x + sx * 3, hip_y - h * 0.02), (x + sx * wa * 1.02, hip_y - h * 0.02),
                                                               (x + sx * wa * 1.0, hip_y + h * 0.17), (x + sx * sh * 0.08, hip_y + h * 0.17)], bottom))
            if bottom_style == "wrap":
                items.append(("region", f"{name}-wrap", [(x - wa * 1.02, hip_y - h * 0.04), (x + wa * 1.02, hip_y - h * 0.04),
                                                         (x + wa * 1.22, feet_y - h * 0.17), (x - wa * 1.22, feet_y - h * 0.17)], bottom))
                items.append(("line", [(x + wa * 0.35, hip_y), (x + wa * 0.5, feet_y - h * 0.19)], 6))
        elif bottom_style == "skirt":
            items.append(("region", f"{name}-skirt", smooth([(x - wa, hip_y - h * 0.04), (x + wa, hip_y - h * 0.04),
                                                             (x + wa * 1.45, ankle), (x - wa * 1.45, ankle)], 1), bottom))

    # ----- torso
    if bottom_style == "dress" and not seated:
        body = smooth([(x - sh * 0.8, sh_y - h * 0.01), (x + sh * 0.8, sh_y - h * 0.01), (x + sh * 1.05, sh_y + h * 0.06),
                       (x + wa * 1.5, ankle), (x - wa * 1.5, ankle), (x - sh * 1.05, sh_y + h * 0.06)], 1)
        items.append(("region", f"{name}-dress", body, top))
        items.append(("region", f"{name}-hem", [(x - wa * 1.4, ankle - h * 0.13), (x + wa * 1.4, ankle - h * 0.13), (x + wa * 1.5, ankle), (x - wa * 1.5, ankle)], bottom))
        items.append(("region", f"{name}-sash", [(x - wa * 1.0, hip_y - h * 0.06), (x + wa * 1.0, hip_y - h * 0.06), (x + wa * 1.05, hip_y), (x - wa * 1.05, hip_y)], bottom))
    else:
        body = smooth([(x - sh * 0.8, sh_y - h * 0.01), (x + sh * 0.8, sh_y - h * 0.01), (x + sh * 1.05, sh_y + h * 0.06),
                       (x + wa, hip_y), (x - wa, hip_y), (x - sh * 1.05, sh_y + h * 0.06)], 1)
        items.append(("region", f"{name}-top", body, top))
        if bottom_style == "dress":
            items.append(("region", f"{name}-sash", [(x - wa * 1.0, hip_y - h * 0.06), (x + wa * 1.0, hip_y - h * 0.06), (x + wa * 1.0, hip_y), (x - wa * 1.0, hip_y)], bottom))
    if bottom_style == "wrap" and not seated:
        items.append(("region", f"{name}-belt", [(x - wa * 1.03, hip_y - h * 0.065), (x + wa * 1.03, hip_y - h * 0.065), (x + wa * 1.04, hip_y - h * 0.015), (x - wa * 1.04, hip_y - h * 0.015)], belt))
    # neckline
    items.append(("line", arc(x, sh_y - h * 0.012, sh * 0.32, h * 0.04, 10, 170, 10), 6))

    # ----- over-garments
    if ext_kind in ("jacket", "vest", "hivis", "lifejacket"):
        bot = hip_y + (h * 0.02 if ext_kind == "jacket" else -h * 0.02)
        if ext_kind == "lifejacket":
            items.append(("region", f"{name}-lifejacket", smooth([(x - sh * 0.95, sh_y), (x + sh * 0.95, sh_y), (x + sh * 1.12, sh_y + h * 0.08),
                                                                  (x + wa * 1.12, bot), (x - wa * 1.12, bot), (x - sh * 1.12, sh_y + h * 0.08)], 1), ext_col))
            items.append(("region", f"{name}-strap", rect(x - wa * 1.05, sh_y + h * 0.13, x + wa * 1.05, sh_y + h * 0.17), BLACK_CLOTH))
            items.append(("line", [(x, sh_y + h * 0.02), (x, bot)], 6))
        else:
            for sx in (-1, 1):
                panel = [(x + sx * sh * 0.32, sh_y - h * 0.005), (x + sx * sh * 0.85, sh_y - h * 0.008), (x + sx * sh * 1.08, sh_y + h * 0.06),
                         (x + sx * wa * 1.06, bot), (x + sx * wa * 0.42, bot)]
                items.append(("region", f"{name}-{ext_kind}", panel, ext_col))
                if ext_kind == "hivis":
                    items.append(("region", f"{name}-stripe", [(x + sx * wa * 0.5, bot - h * 0.11), (x + sx * wa * 1.07, bot - h * 0.1),
                                                               (x + sx * wa * 1.07, bot - h * 0.035), (x + sx * wa * 0.48, bot - h * 0.035)], GREY))

    # ----- arms
    hands = []
    for i, side in enumerate((-1, 1)):
        pose = arms[i]
        spx, spy = x + side * sh * 0.92, sh_y + h * 0.045
        if isinstance(pose, tuple):
            hx, hy = spx + side * pose[0] * h if pose[0] >= 0 else spx + side * pose[0] * h, spy + pose[1] * h
            ex, ey = (spx + hx) / 2 + side * h * 0.04, (spy + hy) / 2 + h * 0.02
        elif pose == "up":
            hx, hy = spx + side * h * 0.1, spy - h * 0.27
            ex, ey = spx + side * h * 0.1, spy - h * 0.1
        elif pose == "wave":
            hx, hy = spx + side * h * 0.17, spy - h * 0.2
            ex, ey = spx + side * h * 0.16, spy + h * 0.02
        elif pose == "out":
            hx, hy = spx + side * h * 0.2, spy + h * 0.16
            ex, ey = spx + side * h * 0.08, spy + h * 0.12
        elif pose == "hold":
            hx, hy = x + side * sh * 0.45, spy + h * 0.2
            ex, ey = spx + side * h * 0.05, spy + h * 0.16
        elif pose == "reach":
            hx, hy = spx + side * h * 0.12, spy - h * 0.3
            ex, ey = spx + side * h * 0.08, spy - h * 0.13
        else:  # down
            hx, hy = spx + side * h * 0.05, spy + h * 0.3
            ex, ey = spx + side * h * 0.05, spy + h * 0.15
        aw = h * (0.075 if child else 0.07)
        items.append(("region", f"{name}-arm", tube([(spx, spy), (ex, ey), (hx, hy)], aw, aw * 0.9, smooth_it=1), skin if sleeves == "short" else sleeve_col))
        if sleeves == "short":
            mx, my = spx + (ex - spx) * 0.75, spy + (ey - spy) * 0.75
            items.append(("region", f"{name}-sleeve", tube([(spx, spy), (mx, my)], aw * 1.25, aw * 1.2, smooth_it=0) , sleeve_col))
        elif ext_kind == "jacket":
            items.append(("region", f"{name}-jacket-sleeve", tube([(spx, spy), (ex, ey), (hx, hy)], aw * 1.02, aw * 0.92, smooth_it=1), ext_col))
        items.append(("region", f"{name}-hand", circle(hx, hy, aw * 0.72, n=32), skin))
        hands.append((hx, hy))
    folk.hands = hands

    # ----- head
    if head == "headscarf":
        items.append(("region", f"{name}-scarf", smooth([(x - hr * 1.3, head_cy - hr * 0.2), (x - hr * 0.9, head_cy - hr * 1.25), (x + hr * 0.9, head_cy - hr * 1.25),
                                                         (x + hr * 1.3, head_cy - hr * 0.2), (x + sh * 0.95, sh_y + h * 0.05), (x - sh * 0.95, sh_y + h * 0.05)], 2), head_col))
    elif head not in ("turban", "hardhat", "helmet", "cap", "straw_hat") or child:
        if hair:
            items.append(("region", f"{name}-hair", circle(x, head_cy - hr * 0.14, hr * 1.16), hair))
    items.append(("region", f"{name}-face", circle(x, head_cy, hr), skin))
    items += _face(x, head_cy, hr, facing=facing)
    if head == "headscarf":
        items.append(("region", f"{name}-scarf-front", smooth([(x - hr * 1.02, head_cy - hr * 0.1), (x - hr * 0.8, head_cy - hr * 0.95), (x, head_cy - hr * 1.18),
                                                               (x + hr * 0.8, head_cy - hr * 0.95), (x + hr * 1.02, head_cy - hr * 0.1), (x + hr * 0.6, head_cy - hr * 0.45), (x, head_cy - hr * 0.5), (x - hr * 0.6, head_cy - hr * 0.45)], 1), head_col))
    elif hair and head in ("none", "flower_band", "jasmine"):
        items.append(("region", f"{name}-fringe", smooth([(x - hr * 1.0, head_cy - hr * 0.15), (x - hr * 0.7, head_cy - hr * 0.95), (x, head_cy - hr * 1.15),
                                                          (x + hr * 0.7, head_cy - hr * 0.95), (x + hr * 1.0, head_cy - hr * 0.15), (x, head_cy - hr * 0.55)], 1), hair))
    if head == "cap":
        items.append(("region", f"{name}-cap", arc(x, head_cy - hr * 0.3, hr * 1.02, hr * 0.85, 180, 360), head_col))
        items.append(("region", f"{name}-cap-brim", smooth([(x + (facing or 1) * hr * 0.1, head_cy - hr * 0.6), (x + (facing or 1) * hr * 1.6, head_cy - hr * 0.42),
                                                     (x + (facing or 1) * hr * 1.6, head_cy - hr * 0.2), (x + (facing or 1) * hr * 0.1, head_cy - hr * 0.26)], 1), head_col))
    elif head == "hardhat":
        items += hard_hat(x, head_cy, hr, head_col, name=f"{name}-hardhat")
    elif head == "helmet":
        items.append(("region", f"{name}-helmet", arc(x, head_cy - hr * 0.3, hr * 1.05, hr * 0.9, 180, 360), head_col))
    elif head == "straw_hat":
        items.append(("region", f"{name}-hat-brim", ellipse(x, head_cy - hr * 0.55, hr * 2.0, hr * 0.38), STRAW))
        items.append(("region", f"{name}-hat-crown", smooth([(x - hr * 0.95, head_cy - hr * 0.6), (x - hr * 0.7, head_cy - hr * 1.5), (x, head_cy - hr * 1.75),
                                                             (x + hr * 0.7, head_cy - hr * 1.5), (x + hr * 0.95, head_cy - hr * 0.6)], 1) + [(x, head_cy - hr * 0.55)], STRAW))
        items.append(("region", f"{name}-hat-band", [(x - hr * 0.93, head_cy - hr * 0.68), (x + hr * 0.93, head_cy - hr * 0.68),
                                                     (x + hr * 0.85, head_cy - hr * 0.98), (x - hr * 0.85, head_cy - hr * 0.98)], head_col))
    elif head == "turban":
        sd = -(facing or 1)
        items.append(("region", f"{name}-turban-tail", smooth([(x + sd * hr * 0.7, head_cy - hr * 0.6), (x + sd * hr * 1.35, head_cy - hr * 0.3),
                                                               (x + sd * hr * 1.4, head_cy + hr * 0.75), (x + sd * hr * 1.05, head_cy + hr * 0.7),
                                                               (x + sd * hr * 0.95, head_cy - hr * 0.1)], 1), head_col))
        items.append(("region", f"{name}-turban", smooth([(x - hr * 1.15, head_cy - hr * 0.2), (x - hr * 1.2, head_cy - hr * 1.0), (x - hr * 0.6, head_cy - hr * 1.6),
                                                          (x + hr * 0.6, head_cy - hr * 1.6), (x + hr * 1.2, head_cy - hr * 1.0), (x + hr * 1.15, head_cy - hr * 0.2),
                                                          (x, head_cy - hr * 0.5)], 2), head_col))
        for k in (0, 1):
            items.append(("line", smooth_open([(x - hr * 1.05, head_cy - hr * (0.55 + 0.45 * k)), (x, head_cy - hr * (0.85 + 0.45 * k)),
                                               (x + hr * 1.05, head_cy - hr * (0.75 + 0.45 * k))], 1), 6))
    elif head == "flower_band":
        items.append(("region", f"{name}-band", smooth([(x - hr * 1.1, head_cy - hr * 0.3), (x, head_cy - hr * 1.0), (x + hr * 1.1, head_cy - hr * 0.3),
                                                        (x + hr * 1.02, head_cy - hr * 0.02), (x, head_cy - hr * 0.62), (x - hr * 1.02, head_cy - hr * 0.02)], 1), GREEN))
        for i, a in enumerate((215, 270, 325)):
            fx, fy = x + math.cos(math.radians(a)) * hr * 0.98, head_cy - hr * 0.05 + math.sin(math.radians(a)) * hr * 0.85
            items.append(("region", f"{name}-flower", star(fx, fy, hr * 0.42, hr * 0.28, 5, -90 + i * 25), (YELLOW, RED, ORANGE)[i]))
            items.append(("ink", circle(fx, fy, hr * 0.08, n=12)))
    elif head == "jasmine":
        items += jasmine_crown(x, head_cy, hr, name=f"{name}-jasmine")
    return items


def fat_palm(x, base_y, h, name="palm", leaf=LEAF, trunk=TRUNK, lean=0.08, dates=True):
    """Palm with five chunky fronds (kid-finger friendly)."""
    items = []
    top = (x + h * lean, base_y - h)
    items.append(("region", f"{name}-trunk", tube([(x, base_y), (x + h * lean * 0.3, base_y - h * 0.5), top], h * 0.1, h * 0.065, smooth_it=2), trunk))
    for i in range(1, 5):
        t = i / 5
        cx = x + h * lean * (t ** 1.5)
        yy = base_y - h * t
        items.append(("line", [(cx - h * 0.035, yy), (cx + h * 0.035, yy + h * 0.015)], 6))
    for ang, L in ((200, 0.52), (245, 0.42), (290, 0.42), (335, 0.52), (20, 0.4), (160, 0.4)):
        a = math.radians(ang)
        Lp = h * L
        tip = (top[0] + math.cos(a) * Lp, top[1] + math.sin(a) * Lp * 0.7 + Lp * 0.3)
        mid = ((top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2 - h * 0.08)
        d = math.hypot(tip[0] - top[0], tip[1] - top[1]) or 1
        nx, ny = -(tip[1] - top[1]) / d * h * 0.085, (tip[0] - top[0]) / d * h * 0.085
        items.append(("region", f"{name}-leaf", smooth([top, (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx, mid[1] - ny)], 2), leaf))
    if dates:
        items.append(("region", f"{name}-dates", blob(top[0], top[1] + h * 0.07, h * 0.08, h * 0.07, seed=1), ORANGE))
    return items


def terraced_mountain(peak_x, peak_y, base_y, half_w, n, field=GRASS, wall=ROCK, name="mtn", skew=0.0, wall_frac=0.22, fields=None):
    """Mountain whose slopes are stepped terraces: a rock body with n field bands laid over it."""
    def xl(y):
        t = max(0.0, (y - peak_y) / (base_y - peak_y))
        return peak_x - 50 - half_w * t ** 0.8 * (1 - skew)

    def xr(y):
        t = max(0.0, (y - peak_y) / (base_y - peak_y))
        return peak_x + 50 + half_w * t ** 0.8 * (1 + skew)

    ys = [peak_y + (base_y - peak_y) * k / 12 for k in range(13)]
    outline = [(xl(y), y) for y in reversed(ys)] + [(xr(y), y) for y in ys]
    items = [("region", f"{name}-rock", smooth([(xl(base_y), base_y + 60)] + outline + [(xr(base_y), base_y + 60)], 1), wall)]
    step = (base_y - peak_y) / (n + 0.6)
    for i in range(n):
        y_top = peak_y + step * (i + 0.6) + step * wall_frac
        y_bot = peak_y + step * (i + 1.6)
        sag = step * 0.12
        top = [(xl(y_top) + 6, y_top)] + [(xl(y_top) + (xr(y_top) - xl(y_top)) * k / 6, y_top + sag * math.sin(math.pi * k / 6)) for k in range(1, 6)] + [(xr(y_top) - 6, y_top)]
        bot = [(xr(y_bot) - 6, y_bot)] + [(xl(y_bot) + (xr(y_bot) - xl(y_bot)) * k / 6, y_bot + sag * math.sin(math.pi * k / 6)) for k in range(5, 0, -1)] + [(xl(y_bot) + 6, y_bot)]
        col = fields[i % len(fields)] if fields else field
        items.append(("region", f"{name}-terrace{i}", smooth_open(top, 2) + smooth_open(bot, 2), col))
    return items


def stone_house(x0, base_y, w, h, wall=MUD, trim=WHITE, name="house", windows=2, door=True):
    """Tall stone tower-house of the Jazan/Fifa highlands: flat roof, white-framed windows."""
    items = [("region", f"{name}", rect(x0, base_y - h, x0 + w, base_y), wall),
             ("region", f"{name}-roof", rect(x0 - 8, base_y - h - 22, x0 + w + 8, base_y - h + 8), trim)]
    ww = w * 0.3
    for r in range(2 if h > w * 1.1 else 1):
        wy = base_y - h + h * 0.15 + r * h * 0.32
        cols = [x0 + w * 0.5 - ww / 2] if windows == 1 else [x0 + w * 0.2, x0 + w * 0.8 - ww]
        for wx in cols:
            items.append(("region", f"{name}-window", rect(wx, wy, wx + ww, wy + ww * 1.2), DARK_BROWN))
    if door:
        items.append(("region", f"{name}-door", rect(x0 + w * 0.36, base_y - h * 0.3, x0 + w * 0.64, base_y), DARK_BROWN))
    return items


def hoe(hx, hy, length, angle_deg=-70, name="hoe", colour=TRUNK):
    """Long-handled hoe held at (hx, hy); handle points along angle (deg, 0 = right, -90 = up)."""
    a = math.radians(angle_deg)
    x0, y0 = hx - math.cos(a) * length * 0.25, hy - math.sin(a) * length * 0.25
    x1, y1 = hx + math.cos(a) * length * 0.75, hy + math.sin(a) * length * 0.75
    items = [("region", f"{name}-handle", tube([(x0, y0), (x1, y1)], 26, 26, smooth_it=0), colour)]
    bx, by = x0, y0
    items.append(("region", f"{name}-blade", [(bx - 20, by - 30), (bx + 60, by - 10), (bx + 70, by + 70), (bx - 30, by + 50)], GREY))
    return items


def coffee_bush(cx, base_y, w, h, name="coffee", cherries=(), leaf=LEAF, cherry=RED):
    """Bushy coffee shrub; cherries = list of (dx, dy) fractions of (w, h) from the crown centre (clusters of two)."""
    cy = base_y - h * 0.55
    pts = []
    for k in range(9):
        a = math.pi + math.pi * k / 8
        pts.append((cx + math.cos(a) * w * 0.5, cy + math.sin(a) * h * 0.5))
    lump = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ox, oy = mx - cx, my - cy
        d = math.hypot(ox, oy) or 1
        lump += [(x0, y0), (mx + ox / d * w * 0.09, my + oy / d * h * 0.09)]
    lump += [pts[-1], (cx + w * 0.42, base_y - h * 0.12), (cx + w * 0.2, base_y - h * 0.04), (cx - w * 0.2, base_y - h * 0.04), (cx - w * 0.42, base_y - h * 0.12)]
    items = [("region", f"{name}-stem", tube([(cx, base_y + 10), (cx, base_y - h * 0.2)], w * 0.14, w * 0.12, smooth_it=0), TRUNK),
             ("region", f"{name}-bush", smooth(lump, 2), leaf)]
    for k in range(4):
        lx = cx + (-0.3 + 0.2 * k) * w
        ly = cy + (0.15 if k % 2 else -0.12) * h
        items.append(("line", smooth_open([(lx - w * 0.07, ly + h * 0.03), (lx, ly - h * 0.03), (lx + w * 0.07, ly - h * 0.04)], 1), 6))
    r = max(28, w * 0.055)
    for k, (dx, dy) in enumerate(cherries):
        x, y = cx + dx * w, cy + dy * h
        items.append(("region", f"{name}-cherry", circle(x - r * 0.8, y, r, n=28), cherry))
        items.append(("region", f"{name}-cherry", circle(x + r * 0.8, y + r * 0.4, r, n=28), cherry))
    return items


def container(x0, y0, w, h, colour, name="container"):
    items = [("region", name, rect(x0, y0, x0 + w, y0 + h), colour)]
    n = max(2, int(w // 70))
    for k in range(1, n):
        xx = x0 + w * k / n
        items.append(("line", [(xx, y0 + 12), (xx, y0 + h - 12)], 5))
    return items


def cargo_ship(x0, water_y, L, hull=RED, deck=WHITE, name="ship", stacks=None):
    """Side-view container ship, bow on the right. stacks: list of rows (bottom first), each a list of colours."""
    H_ = L * 0.12
    items = []
    # bridge at the stern (left)
    items.append(("region", f"{name}-bridge", rect(x0 + L * 0.05, water_y - H_ - L * 0.2, x0 + L * 0.17, water_y - H_ + 5), deck))
    items.append(("region", f"{name}-bridge-top", rect(x0 + L * 0.03, water_y - H_ - L * 0.235, x0 + L * 0.19, water_y - H_ - L * 0.195), deck))
    items.append(("region", f"{name}-funnel", rect(x0 + L * 0.08, water_y - H_ - L * 0.3, x0 + L * 0.13, water_y - H_ - L * 0.235), hull))
    for k in range(2):
        wx = x0 + L * (0.065 + k * 0.055)
        items.append(("region", f"{name}-window", rect(wx, water_y - H_ - L * 0.17, wx + L * 0.04, water_y - H_ - L * 0.13), SEA))
    cw, ch = L * 0.105, L * 0.055
    if stacks:
        for r, row in enumerate(stacks):
            for c, col in enumerate(row):
                if col:
                    items += container(x0 + L * 0.22 + c * (cw + 6), water_y - H_ - (r + 1) * (ch + 4), cw, ch, col, name=f"{name}-box")
    items.append(("region", f"{name}-hull", [(x0, water_y - H_), (x0 + L, water_y - H_ - L * 0.03), (x0 + L * 0.93, water_y + L * 0.02),
                                             (x0 + L * 0.04, water_y + L * 0.02)], hull))
    items.append(("region", f"{name}-band", [(x0 + L * 0.016, water_y - H_ * 0.35), (x0 + L * 0.968, water_y - H_ * 0.45), (x0 + L * 0.952, water_y - H_ * 0.08),
                                             (x0 + L * 0.024, water_y - H_ * 0.02)], deck))
    return items


def gantry_crane(x, ground_y, h, colour=YELLOW, name="crane", reach=700, cab=WHITE, hook_box=None):
    """Ship-to-shore crane: two A legs, a long boom out to the left, operator cab and a hanging container."""
    items = []
    beam = h * 0.05
    top = ground_y - h
    lw = 260
    for lx in (x - lw, x + lw * 0.2):
        items.append(("region", f"{name}-leg", [(lx - 25, ground_y), (lx + 25, ground_y), (lx + 25, top + h * 0.3), (lx - 25, top + h * 0.3)], colour))
    items.append(("region", f"{name}-crossbar", rect(x - lw - 25, top + h * 0.3, x + lw * 0.2 + 25, top + h * 0.3 + beam), colour))
    items.append(("region", f"{name}-crossbar2", rect(x - lw - 25, top + h * 0.6, x + lw * 0.2 + 25, top + h * 0.6 + beam * 0.8), colour))
    items.append(("region", f"{name}-mast", [(x - lw * 0.55, top + h * 0.3), (x - lw * 0.35, top), (x - lw * 0.15, top), (x + lw * 0.05, top + h * 0.3)], colour))
    items.append(("region", f"{name}-boom", rect(x - lw - reach, top + h * 0.22, x + lw * 0.6, top + h * 0.22 + beam), colour))
    for sx in (-1, 1):
        items.append(("line", [(x - lw * 0.25, top + 10), (x - lw * 0.25 + sx * (reach * 0.8 if sx < 0 else lw * 0.8), top + h * 0.22)], 6))
    items.append(("region", f"{name}-cab", rect(x - lw - 170, top + h * 0.22 + beam, x - lw - 30, top + h * 0.22 + beam + 110), cab))
    items.append(("region", f"{name}-cab-window", rect(x - lw - 150, top + h * 0.22 + beam + 20, x - lw - 60, top + h * 0.22 + beam + 75), SEA))
    hx = x - lw - reach * 0.55
    items.append(("line", [(hx - 40, top + h * 0.22 + beam), (hx - 40, top + h * 0.5)], 6))
    items.append(("line", [(hx + 40, top + h * 0.22 + beam), (hx + 40, top + h * 0.5)], 6))
    if hook_box:
        items += container(hx - 130, top + h * 0.5, 260, 120, hook_box, name=f"{name}-load")
    return items


def mangrove(x, water_y, h, name="mangrove", leaf=LEAF, wood=TRUNK, roots=(-0.42, -0.26, -0.1, 0.12, 0.28, 0.42)):
    """Mangrove tree on arching prop roots standing in water; h = height from water to crown top."""
    items = []
    for k, dx in enumerate(roots):
        sy = water_y - h * (0.42 if k % 2 == 0 else 0.3)
        start = (x + dx * h * 0.15, sy)
        end = (x + dx * h, water_y + 20)
        mid = (x + dx * h * 0.75, sy - h * 0.06)
        items.append(("region", f"{name}-root", tube([start, mid, end], h * 0.05, h * 0.042, smooth_it=2), wood))
    items.append(("region", f"{name}-trunk", tube([(x, water_y - h * 0.28), (x + h * 0.02, water_y - h * 0.62)], h * 0.11, h * 0.08, smooth_it=0), wood))
    cy = water_y - h * 0.72
    pts = []
    for k in range(16):
        ang = 2 * math.pi * k / 16
        rr = 1.0 if k % 2 == 0 else 0.86
        pts.append((x + math.cos(ang) * h * 0.56 * rr, cy + math.sin(ang) * h * 0.3 * rr))
    items.append(("region", f"{name}-crown", smooth(pts, 3), leaf))
    return items


def kayak(cx, water_y, L, colour=ORANGE, name="kayak"):
    hh = L * 0.09
    items = [("region", f"{name}", smooth([(cx - L * 0.5, water_y - hh * 0.9), (cx - L * 0.2, water_y - hh), (cx + L * 0.2, water_y - hh), (cx + L * 0.5, water_y - hh * 0.9),
                                            (cx + L * 0.3, water_y + hh * 0.35), (cx - L * 0.3, water_y + hh * 0.35)], 2), colour)]
    items.append(("line", smooth_open([(cx - L * 0.44, water_y - hh * 0.55), (cx, water_y - hh * 0.45), (cx + L * 0.44, water_y - hh * 0.55)], 1), 6))
    return items


def paddle(x0, y0, x1, y1, colour=YELLOW, blade=RED, name="paddle"):
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    items = [("region", f"{name}-shaft", tube([(x0, y0), (x1, y1)], 26, 26, smooth_it=0), colour)]
    for (bx, by), sgn in (((x0, y0), -1), ((x1, y1), 1)):
        cx, cy = bx + sgn * ux * 50, by + sgn * uy * 50
        ang = math.degrees(math.atan2(uy, ux))
        items.append(("region", f"{name}-blade", ellipse(cx, cy, 80, 40, rot=ang), blade))
    return items

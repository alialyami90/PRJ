"""Extra figure helpers for the Asir region (people with posable arms, animals, houses, props).

All helpers return item lists for Scene.extend(): ("region", name, pts, colour) | ("ink", pts) | ("line", pts, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403

STRAW = "#E9C46A"
SILVER = GREY
NIGHT = BLACK_CLOTH


# ---------------------------------------------------------------- geometry
def thick(pts, w, caps=True):
    """Polygon around a polyline of width w (rounded ends)."""
    pts = [tuple(p) for p in pts]
    n = len(pts)
    left, right, normals = [], [], []
    for i in range(n):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        tx, ty = tx / ln, ty / ln
        nx, ny = -ty, tx
        normals.append((nx, ny, tx, ty))
        left.append((pts[i][0] + nx * w / 2, pts[i][1] + ny * w / 2))
        right.append((pts[i][0] - nx * w / 2, pts[i][1] - ny * w / 2))
    poly = list(left)
    if caps:
        nx, ny, tx, ty = normals[-1]
        px, py = pts[-1]
        for k in range(1, 12):
            t = math.pi * k / 12
            poly.append((px + w / 2 * (math.cos(t) * nx + math.sin(t) * tx), py + w / 2 * (math.cos(t) * ny + math.sin(t) * ty)))
    poly += right[::-1]
    if caps:
        nx, ny, tx, ty = normals[0]
        px, py = pts[0]
        for k in range(1, 12):
            t = math.pi * k / 12
            poly.append((px - w / 2 * (math.cos(t) * nx + math.sin(t) * tx), py - w / 2 * (math.cos(t) * ny + math.sin(t) * ty)))
    return poly


def bumpy(cx, cy, rx, ry, bumps=10, depth=0.12, rot=0, n=240, phase=0):
    """Scalloped ellipse (wool, foliage, clouds)."""
    pts = []
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + depth * abs(math.sin(bumps * (t + phase) / 2))
        x, y = rx * k * math.cos(t), ry * k * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def rrect(x0, y0, x1, y1, r, n=8):
    """Rounded rectangle."""
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flower(cx, cy, r, colour, name="flower", petals=6):
    items = [("region", name, smooth(star(cx, cy, r, r * 0.62, petals, -90), 2), colour)]
    items.append(("ink", circle(cx, cy, r * 0.16)))
    return items


# ---------------------------------------------------------------- people
def figure(x, feet_y, h, facing=0, child=False, skin=SKIN, name="p",
           top=WHITE, jacket=None, jacket_trim=None, bottom="wrap", bottom_colour=BROWN,
           bands=(), belt=None, head="none", head_colour=RED, hat_colour=STRAW, hair=DARK_BROWN,
           beard=False, arms=((0.05, 0.36), (0.05, 0.36)), elbows=(None, None), sleeve=None,
           cuffs=None, point=(False, False), shoes=DARK_BROWN, necklace=None, buckle=False, yoke=None, stride=0.0, zip_line=False, smile=True):
    """A friendly person with posable arms.

    bottom: wrap (knee-length izar, legs bare) | dress (long, uses `top` colour, `bands` = colours of
            hem bands) | trousers (bottom_colour) | thobe (long robe in top colour)
    head:   none (hair) | crown (herb + flower crown) | hat (Asiri straw hat over hair) | wrap (headwrap)
            | scarf (headscarf in head_colour) | scarf_hat (headscarf + straw hat) | cap
    arms:   ((dx, dy) left, (dx, dy) right) hand offsets from the shoulder in units of h; dx > 0 = outward.
    elbows: optional (dx, dy) elbow offsets per arm.
    After the call figure.hands = [left hand centre, right hand centre]; figure.head = (cx, cy, r).
    """
    items = []
    head_r = h * (0.14 if child else 0.12)
    head_cy = feet_y - h + head_r
    neck_y = head_cy + head_r * 0.92
    sw = h * (0.15 if child else 0.165)
    waist = feet_y - h * (0.47 if child else 0.5)
    arm_w = h * (0.075 if child else 0.07)
    hand_r = max(30, h * (0.05 if child else 0.045))
    long_robe = bottom in ("dress", "thobe")
    hem_y = feet_y - h * 0.055
    hem_w = sw * 1.3
    knee_y = feet_y - h * 0.24
    sleeve = sleeve or (jacket if jacket else top)

    # legs + shoes
    leg_w = sw * 0.42
    for sx in (-1, 1):
        lx = x + sx * (sw * 0.36 + stride * h * 0.5)
        if not long_robe:
            leg_col = skin if bottom == "wrap" else bottom_colour
            items.append(("region", f"{name}-leg", [(x + sx * sw * 0.1, waist + h * 0.05), (x + sx * sw * 0.9, waist + h * 0.05),
                                                    (lx + leg_w / 2, feet_y - h * 0.04), (lx - leg_w / 2, feet_y - h * 0.04)] if sx > 0 else
                          [(x + sx * sw * 0.9, waist + h * 0.05), (x + sx * sw * 0.1, waist + h * 0.05),
                           (lx + leg_w / 2, feet_y - h * 0.04), (lx - leg_w / 2, feet_y - h * 0.04)], leg_col))
        fx = lx + (facing * leg_w * 0.35)
        items.append(("region", f"{name}-shoe", smooth([(fx - leg_w * 0.95, feet_y), (fx - leg_w * 0.85, feet_y - h * 0.07),
                                                         (fx + leg_w * 0.85, feet_y - h * 0.07), (fx + leg_w * 1.05, feet_y)], 1), shoes))

    # arms (behind the body)
    hands = []
    for i, sx in enumerate((-1, 1)):
        shx, shy = x + sx * sw * 0.82, neck_y + h * 0.06
        dx, dy = arms[i]
        hx, hy = shx + sx * dx * h, shy + dy * h
        pts = [(shx, shy)]
        if elbows[i]:
            ex, ey = elbows[i]
            pts.append((shx + sx * ex * h, shy + ey * h))
        pts.append((hx, hy))
        items.append(("region", f"{name}-sleeve", thick(pts, arm_w), sleeve))
        if cuffs:
            # cuff band near the wrist
            px, py = pts[-2]
            L = math.hypot(hx - px, hy - py) or 1
            ux, uy = (hx - px) / L, (hy - py) / L
            c0 = (hx - ux * hand_r * 2.4, hy - uy * hand_r * 2.4)
            c1 = (hx - ux * hand_r * 0.6, hy - uy * hand_r * 0.6)
            items.append(("region", f"{name}-cuff", thick([c0, c1], arm_w * 1.08, caps=False), cuffs))
        if point[i]:
            px, py = pts[-2]
            a = math.atan2(hy - py, hx - px)
            hp = [(hx + hand_r * math.cos(a + math.radians(d)), hy + hand_r * math.sin(a + math.radians(d))) for d in range(35, 326, 10)]
            hp.append((hx + math.cos(a) * hand_r * 2.3, hy + math.sin(a) * hand_r * 2.3))
            items.append(("region", f"{name}-hand", hp, skin))
        else:
            items.append(("region", f"{name}-hand", circle(hx, hy, hand_r), skin))
        hands.append((hx, hy))
    figure.hands = hands

    # body
    if long_robe:
        wy = waist - h * 0.05
        def rw(y):
            return sw * 1.08 if y <= wy else sw * 1.08 + (hem_w - sw * 1.08) * (y - wy) / (hem_y - wy)
        robe = [(x - sw * 0.9, neck_y + h * 0.01), (x + sw * 0.9, neck_y + h * 0.01), (x + sw * 1.04, neck_y + h * 0.05), (x + rw(wy), wy),
                (x + hem_w, hem_y), (x - hem_w, hem_y), (x - rw(wy), wy), (x - sw * 1.04, neck_y + h * 0.05)]
        items.append(("region", f"{name}-robe", robe, top))
        by = hem_y
        for j, bc in enumerate(bands):
            bh = h * 0.06
            items.append(("region", f"{name}-band", [(x - rw(by - bh), by - bh), (x + rw(by - bh), by - bh), (x + rw(by), by), (x - rw(by), by)], bc))
            by -= bh + h * 0.05
    else:
        if bottom == "wrap":
            items.append(("region", f"{name}-wrap", [(x - sw * 1.0, waist - h * 0.02), (x + sw * 1.0, waist - h * 0.02),
                                                     (x + sw * 1.18, knee_y), (x - sw * 1.18, knee_y)], bottom_colour))
            if bands:
                items.append(("region", f"{name}-wrap-band", [(x - sw * 1.15, knee_y - h * 0.05), (x + sw * 1.15, knee_y - h * 0.05),
                                                              (x + sw * 1.18, knee_y), (x - sw * 1.18, knee_y)], bands[0]))
        items.append(("region", f"{name}-shirt", [(x - sw * 0.85, neck_y + h * 0.01), (x + sw * 0.85, neck_y + h * 0.01), (x + sw * 1.02, neck_y + h * 0.06),
                                                  (x + sw * 1.0, waist + h * 0.03), (x - sw * 1.0, waist + h * 0.03), (x - sw * 1.02, neck_y + h * 0.06)], top))
    if yoke:
        items.append(("region", f"{name}-yoke", smooth([(x - sw * 0.55, neck_y + h * 0.015), (x + sw * 0.55, neck_y + h * 0.015),
                                                        (x + sw * 0.45, neck_y + h * 0.17), (x, neck_y + h * 0.21), (x - sw * 0.45, neck_y + h * 0.17)], 1), yoke))
    if jacket:
        jy1 = waist + (h * 0.03 if not long_robe else h * 0.04)
        for sx in (-1, 1):
            items.append(("region", f"{name}-jacket", [(x + sx * sw * 0.28, neck_y + h * 0.01), (x + sx * sw * 1.02, neck_y + h * 0.03),
                                                       (x + sx * sw * 1.02, jy1), (x + sx * sw * 0.38, jy1)], jacket))
            if jacket_trim:
                items.append(("region", f"{name}-trim", [(x + sx * sw * 0.28, neck_y + h * 0.01), (x + sx * sw * 0.58, neck_y + h * 0.015),
                                                         (x + sx * sw * 0.7, jy1), (x + sx * sw * 0.38, jy1)], jacket_trim))
        if zip_line:
            pass
    if zip_line:
        items.append(("line", [(x, neck_y + h * 0.04), (x, waist)], 6))
    if belt:
        items.append(("region", f"{name}-belt", rect(x - sw * 1.02, waist - h * 0.03, x + sw * 1.02, waist + h * 0.03), belt))
        if buckle:
            items.append(("region", f"{name}-buckle", rrect(x - h * 0.035, waist - h * 0.038, x + h * 0.035, waist + h * 0.038, 6), GOLD))
    # head
    hx = x
    if head in ("scarf", "scarf_hat"):
        items.append(("region", f"{name}-scarf", smooth([(hx - head_r * 1.3, head_cy - head_r * 0.2), (hx - head_r * 1.1, head_cy - head_r * 1.2),
                                                        (hx + head_r * 1.1, head_cy - head_r * 1.2), (hx + head_r * 1.3, head_cy - head_r * 0.2),
                                                        (hx + head_r * 1.4, neck_y + h * 0.07), (hx - head_r * 1.4, neck_y + h * 0.07)], 2), head_colour))
    elif head == "none":
        # hair behind (sides)
        items.append(("region", f"{name}-hair", smooth([(hx - head_r * 1.12, head_cy + head_r * 0.35), (hx - head_r * 1.15, head_cy - head_r * 0.9),
                                                       (hx, head_cy - head_r * 1.2), (hx + head_r * 1.15, head_cy - head_r * 0.9),
                                                       (hx + head_r * 1.12, head_cy + head_r * 0.35)], 2), hair))
    items.append(("region", f"{name}-face", circle(hx, head_cy, head_r), skin))
    off = head_r * 0.16 * facing
    for sx in (-1, 1):
        items.append(("ink", ellipse(hx + off + sx * head_r * 0.36, head_cy - head_r * 0.02, head_r * 0.1, head_r * 0.14)))
    if beard:
        items.append(("region", f"{name}-beard", arc(hx, head_cy + head_r * 0.15, head_r * 0.92, head_r * 0.92, 15, 165, 16) +
                      arc(hx + off, head_cy + head_r * 0.42, head_r * 0.42, head_r * 0.22, 160, 20, 10), hair))
        if smile:
            items.append(("line", arc(hx + off, head_cy + head_r * 0.36, head_r * 0.24, head_r * 0.14, 20, 160, 10), max(5, int(head_r * 0.07))))
    elif smile:
        items.append(("line", arc(hx + off, head_cy + head_r * 0.22, head_r * 0.34, head_r * 0.24, 20, 160, 12), max(5, int(head_r * 0.08))))
    if head in ("scarf", "scarf_hat"):
        items.append(("region", f"{name}-scarf-front", smooth([(hx - head_r * 1.02, head_cy - head_r * 0.05), (hx - head_r * 0.9, head_cy - head_r * 1.1),
                                                              (hx + head_r * 0.9, head_cy - head_r * 1.1), (hx + head_r * 1.02, head_cy - head_r * 0.05),
                                                              (hx + head_r * 0.7, head_cy - head_r * 0.62), (hx - head_r * 0.7, head_cy - head_r * 0.62)], 2), head_colour))
    elif head in ("none", "hat"):
        cap = arc(hx, head_cy, head_r * 1.03, head_r * 1.06, 192, 348, 24)
        cap += [(hx + head_r * 0.75, head_cy - head_r * 0.45), (hx + head_r * 0.35, head_cy - head_r * 0.6),
                (hx, head_cy - head_r * 0.48), (hx - head_r * 0.35, head_cy - head_r * 0.6), (hx - head_r * 0.75, head_cy - head_r * 0.45)]
        items.append(("region", f"{name}-hair", cap, hair))
    if head == "crown":
        items.append(("region", f"{name}-herbs", bumpy(hx, head_cy - head_r * 0.9, head_r * 1.18, head_r * 0.34, bumps=12, depth=0.28), GREEN))
        cols = head_colour if isinstance(head_colour, (list, tuple)) else (YELLOW, ORANGE, YELLOW)
        for k, fx in enumerate((-0.7, 0.0, 0.7)):
            items += flower(hx + fx * head_r, head_cy - head_r * (1.12 if fx == 0 else 0.98), head_r * 0.46, cols[k % len(cols)], f"{name}-flower")
    elif head in ("hat", "scarf_hat"):
        by = head_cy - head_r * 0.62
        items.append(("region", f"{name}-hat-brim", ellipse(hx, by, head_r * 1.85, head_r * 0.34), hat_colour))
        items.append(("region", f"{name}-hat-crown", [(hx - head_r * 0.82, by), (hx - head_r * 0.6, by - head_r * 1.15),
                                                      (hx + head_r * 0.6, by - head_r * 1.15), (hx + head_r * 0.82, by)], hat_colour))
        items.append(("line", [(hx - head_r * 0.75, by - head_r * 0.3), (hx + head_r * 0.75, by - head_r * 0.3)], 6))
    elif head == "wrap":
        items.append(("region", f"{name}-headwrap", smooth([(hx - head_r * 1.08, head_cy - head_r * 0.3), (hx - head_r * 1.0, head_cy - head_r * 1.15),
                                                           (hx, head_cy - head_r * 1.42), (hx + head_r * 1.0, head_cy - head_r * 1.15),
                                                           (hx + head_r * 1.08, head_cy - head_r * 0.3), (hx, head_cy - head_r * 0.5)], 2), head_colour))
        items.append(("line", smooth_open([(hx - head_r * 0.9, head_cy - head_r * 0.85), (hx, head_cy - head_r * 1.05), (hx + head_r * 0.9, head_cy - head_r * 0.8)], 2), 6))
    elif head == "cap":
        items.append(("region", f"{name}-cap", arc(hx, head_cy - head_r * 0.35, head_r * 1.0, head_r * 0.85, 180, 360), head_colour))
        f = facing or 1
        items.append(("region", f"{name}-cap-brim", ellipse(hx + f * head_r * 0.85, head_cy - head_r * 0.36, head_r * 0.8, head_r * 0.24), head_colour))
    if necklace:
        ny0 = neck_y + h * 0.045
        items.append(("region", f"{name}-necklace", arc(x, ny0, sw * 0.72, h * 0.1, 0, 180, 16) +
                      arc(x, ny0, sw * 0.5, h * 0.055, 180, 0, 16), necklace))
        items.append(("region", f"{name}-pendant", circle(x, ny0 + h * 0.125, h * 0.035), necklace))

    figure.head = (hx, head_cy, head_r)
    return items


# ---------------------------------------------------------------- landscape
def mountains(peaks, base_y, colour, name="mountain"):
    """Rounded mountain range through (x, y) peak points, filled down to base_y."""
    pts = [(peaks[0][0] - 400, base_y)] + list(peaks) + [(peaks[-1][0] + 400, base_y)]
    return [("region", name, smooth(pts + [(peaks[-1][0] + 400, base_y + 50), (peaks[0][0] - 400, base_y + 50)], 3), colour)]


def juniper(x, base_y, h, leaf=LEAF, trunk=TRUNK, name="juniper"):
    tw = max(h * 0.075, 22)
    items = [("region", f"{name}-trunk", [(x - tw, base_y), (x + tw, base_y), (x + tw * 0.7, base_y - h * 0.4), (x - tw * 0.7, base_y - h * 0.4)], trunk)]
    items.append(("region", f"{name}-leaves", bumpy(x, base_y - h * 0.64, h * 0.3, h * 0.38, bumps=9, depth=0.1), leaf))
    return items


def round_tree(x, base_y, h, leaf=GREEN, trunk=TRUNK, name="tree"):
    items = [("region", f"{name}-trunk", [(x - h * 0.07, base_y), (x + h * 0.07, base_y), (x + h * 0.04, base_y - h * 0.5), (x - h * 0.04, base_y - h * 0.5)], trunk)]
    items.append(("region", f"{name}-leaves", bumpy(x, base_y - h * 0.68, h * 0.42, h * 0.32, bumps=11, depth=0.1), leaf))
    return items


def puff(cx, cy, w, h=None, name="cloud", colour=CLOUD):
    h = h or w * 0.35
    return [("region", name, bumpy(cx, cy, w / 2, h / 2, bumps=7, depth=0.14), colour)]


def tower_house(x0, base_y, w, h, wall=ROCK, trim=WHITE, window=DARK_BROWN, floors=None, name="house", crenels=True, bands=None):
    """Asiri / Rijal Almaa stone tower house: x0 = left, base_y = ground, w x h."""
    items = [("region", f"{name}-wall", rect(x0, base_y - h, x0 + w, base_y), wall)]
    floors = floors or max(2, int(h / 220))
    fh = h / floors
    if bands:
        for i in range(1, floors):
            yy = base_y - fh * i
            items.append(("region", f"{name}-band", rect(x0 - 6, yy - fh * 0.08, x0 + w + 6, yy + fh * 0.04), bands))
    ncols = max(1, int(w / 170))
    for i in range(floors):
        yy = base_y - fh * i
        for j in range(ncols):
            cx = x0 + w * (j + 0.5) / ncols
            ww = min(w / ncols * 0.42, fh * 0.32)
            wh = fh * 0.42
            wy1 = yy - fh * 0.22
            if i == 0 and j == ncols // 2 and w > 120:
                # door
                items.append(("region", f"{name}-door-frame", rect(cx - ww * 0.95, yy - fh * 0.7, cx + ww * 0.95, yy), trim))
                items.append(("region", f"{name}-door", rect(cx - ww * 0.62, yy - fh * 0.6, cx + ww * 0.62, yy), window))
                continue
            items.append(("region", f"{name}-frame", rect(cx - ww * 0.9, wy1 - wh - ww * 0.3, cx + ww * 0.9, wy1 + ww * 0.3), trim))
            items.append(("region", f"{name}-window", rect(cx - ww * 0.55, wy1 - wh, cx + ww * 0.55, wy1), window))
    if crenels:
        n = max(3, int(w / 75))
        cw = w / n
        top = base_y - h
        tri = [(x0 - 6, top + cw * 0.35)]
        for i in range(n):
            tri += [(x0 + cw * i, top), (x0 + cw * (i + 0.5), top - cw * 0.95), (x0 + cw * (i + 1), top)]
        tri += [(x0 + w + 6, top + cw * 0.35)]
        tri[1] = (x0 - 6, top)
        tri[-2] = (x0 + w + 6, top)
        items.append(("region", f"{name}-crenels", tri, trim))
    return items


# ---------------------------------------------------------------- animals
def _leg(P, lx, top, w, h):
    a, b = P(lx - w / 2, top), P(lx + w / 2, 0)
    return rrect(min(a[0], b[0]), a[1], max(a[0], b[0]), b[1], w * h * 0.45, 4)


def sheep(x, feet_y, h, facing=1, wool=CREAM, face=DARK_BROWN, legs=DARK_BROWN, name="sheep"):
    """Side-view fluffy sheep; h = height to the top of the back."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    for lx in (-0.4, -0.22, 0.2, 0.38):
        items.append(("region", f"{name}-leg", _leg(P, lx, 0.5, 0.11, h), legs))
    items.append(("region", f"{name}-tail", bumpy(*P(-0.72, 0.76), h * 0.14, h * 0.13, bumps=5, depth=0.2), wool))
    cx, cy = P(0, 0.7)
    items.append(("region", f"{name}-wool", bumpy(cx, cy, h * 0.66, h * 0.33, bumps=14, depth=0.09), wool))
    hx, hy = P(0.66, 0.8)
    items.append(("region", f"{name}-ear", ellipse(*P(0.48, 0.9), h * 0.16, h * 0.075, rot=-20 * f), face))
    items.append(("region", f"{name}-head", ellipse(hx, hy, h * 0.2, h * 0.15, rot=35 * f), face))
    items.append(("region", f"{name}-tuft", bumpy(*P(0.6, 0.96), h * 0.15, h * 0.09, bumps=6, depth=0.2), wool))
    ex, ey = P(0.7, 0.84)
    items.append(("ink", circle(ex, ey, h * 0.028)))
    items.append(("line", arc(*P(0.75, 0.72), h * 0.06, h * 0.035, 20, 160, 8), 6))
    return items


def goat(x, feet_y, h, facing=1, body=BROWN, horn=GREY, legs=None, name="goat", patch=None, beard=DARK_BROWN):
    """Side-view goat; h = height to the back."""
    f = facing
    legs = legs or body
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    for lx in (-0.36, -0.2, 0.22, 0.38):
        items.append(("region", f"{name}-leg", _leg(P, lx, 0.62, 0.13, h), legs))
    items.append(("region", f"{name}-tail", [P(-0.4, 0.88), P(-0.68, 1.06), P(-0.62, 0.86), P(-0.5, 0.7)], body))
    items.append(("region", f"{name}-neck", thick([P(0.34, 0.74), P(0.54, 1.02)], h * 0.26), body))
    items.append(("region", f"{name}-body", ellipse(*P(0, 0.74), h * 0.54, h * 0.28), body))
    if patch:
        items.append(("region", f"{name}-patch", ellipse(*P(-0.16, 0.76), h * 0.2, h * 0.14), patch))
    items.append(("region", f"{name}-horn", thick(smooth_open([P(0.58, 1.16), P(0.52, 1.32), P(0.4, 1.4), P(0.3, 1.36)], 2), h * 0.075), horn))
    items.append(("region", f"{name}-head", ellipse(*P(0.68, 1.06), h * 0.22, h * 0.14, rot=32 * f), body))
    items.append(("region", f"{name}-ear", ellipse(*P(0.5, 1.07), h * 0.16, h * 0.065, rot=-25 * f), body))
    items.append(("region", f"{name}-beard", [P(0.72, 0.98), P(0.92, 0.9), P(0.8, 0.64)], beard))
    items.append(("ink", circle(*P(0.66, 1.12), h * 0.026)))
    items.append(("line", arc(*P(0.78, 0.98), h * 0.045, h * 0.03, 20, 160, 8), 5))
    return items


def donkey(x, feet_y, h, facing=1, body=GREY, muzzle=CREAM, mane=DARK_BROWN, blanket=RED, bags=ORANGE, name="donkey"):
    """Side-view donkey; h = height to the back."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    items.append(("region", f"{name}-tail", thick(smooth_open([P(-0.55, 0.88), P(-0.68, 0.7), P(-0.66, 0.42)], 2), h * 0.05), body))
    for lx in (-0.4, -0.24, 0.26, 0.42):
        items.append(("region", f"{name}-leg", [P(lx - 0.065, 0.62), P(lx + 0.065, 0.62), P(lx + 0.055, 0.1), P(lx - 0.055, 0.1)], body))
        a, b = P(lx - 0.07, 0.12), P(lx + 0.07, 0.0)
        items.append(("region", f"{name}-hoof", rrect(min(a[0], b[0]), a[1], max(a[0], b[0]), b[1], 8), DARK_BROWN))
    items.append(("region", f"{name}-body", smooth([P(-0.58, 0.62), P(-0.54, 1.02), P(0.38, 1.04), P(0.58, 0.85), P(0.52, 0.5), P(-0.44, 0.5)], 3), body))
    items.append(("region", f"{name}-neck", smooth([P(0.32, 0.92), P(0.52, 1.28), P(0.7, 1.3), P(0.62, 0.82)], 2), body))
    items.append(("region", f"{name}-ear", smooth([P(0.56, 1.4), P(0.5, 1.72), P(0.6, 1.72), P(0.64, 1.42)], 2), body))
    items.append(("region", f"{name}-ear", smooth([P(0.64, 1.4), P(0.68, 1.72), P(0.77, 1.68), P(0.71, 1.38)], 2), body))
    items.append(("region", f"{name}-head", smooth([P(0.5, 1.38), P(0.7, 1.5), P(1.0, 1.22), P(0.96, 1.06), P(0.64, 1.14)], 2), body))
    items.append(("region", f"{name}-muzzle", smooth([P(0.82, 1.3), P(1.02, 1.22), P(0.98, 1.04), P(0.78, 1.1)], 2), muzzle))
    items.append(("region", f"{name}-mane", smooth([P(0.34, 1.0), P(0.5, 1.33), P(0.6, 1.42), P(0.52, 1.25), P(0.44, 0.97)], 2), mane))
    ex, ey = P(0.72, 1.3)
    items.append(("ink", circle(ex, ey, h * 0.025)))
    items.append(("ink", circle(*P(0.93, 1.17), h * 0.015)))
    if blanket:
        items.append(("region", f"{name}-blanket", smooth([P(-0.3, 1.04), P(0.2, 1.04), P(0.24, 0.66), P(-0.34, 0.66)], 1), blanket))
    if bags:
        items.append(("region", f"{name}-bag", rrect(*sorted_rect(P(-0.25, 0.84), P(0.12, 0.5)), h * 0.05), bags))
        items.append(("line", [P(-0.25, 0.72), P(0.12, 0.72)], 6))
    return items


def sorted_rect(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def baboon(x, ground_y, h, facing=1, fur="#B0A48A", mane=None, face=PINK, paw=DARK_BROWN, name="baboon", arm_up=False):
    """Seated hamadryas baboon (3/4 view). h = sitting height. mane: colour of the male's silver cape."""
    f = facing
    def P(px, py):
        return (x + f * px * h, ground_y - py * h)
    paws = h >= 380
    items = []
    items.append(("region", f"{name}-tail", thick(smooth_open([P(-0.2, 0.07), P(-0.55, 0.06), P(-0.78, 0.16), P(-0.84, 0.32)], 2), h * 0.1), fur))
    items.append(("region", f"{name}-body", smooth([P(-0.32, 0.0), P(-0.4, 0.3), P(-0.3, 0.6), P(-0.05, 0.72), P(0.2, 0.64), P(0.3, 0.35), P(0.28, 0.0)], 3), fur))
    if mane:
        items.append(("region", f"{name}-mane", smooth([P(-0.42, 0.3), P(-0.46, 0.72), P(-0.24, 1.02), P(0.1, 1.08), P(0.36, 0.94), P(0.32, 0.56), P(0.06, 0.4)], 3), mane))
    items.append(("region", f"{name}-thigh", ellipse(*P(0.08, 0.2), h * 0.25, h * 0.18, rot=-12 * f), fur))
    if paws:
        items.append(("region", f"{name}-foot", ellipse(*P(0.3, 0.05), h * 0.14, h * 0.06), paw))
    if arm_up:
        items.append(("region", f"{name}-arm", thick([P(0.14, 0.55), P(0.36, 0.6), P(0.44, 0.86)], h * 0.13), mane or fur))
    else:
        items.append(("region", f"{name}-arm", thick([P(0.12, 0.56), P(0.3, 0.32), P(0.34, 0.08)], h * 0.13), mane or fur))
        if paws:
            items.append(("region", f"{name}-hand", ellipse(*P(0.38, 0.05), h * 0.1, h * 0.055), paw))
    items.append(("region", f"{name}-head", circle(*P(0.1, 0.8), h * 0.18), mane or fur))
    if not mane:
        items.append(("region", f"{name}-ear", circle(*P(-0.07, 0.92), max(h * 0.08, 30)), fur))
        items.append(("region", f"{name}-head2", circle(*P(0.1, 0.8), h * 0.17), fur))
    items.append(("region", f"{name}-face", smooth([P(0.04, 0.9), P(0.2, 0.93), P(0.4, 0.83), P(0.42, 0.72), P(0.22, 0.67), P(0.04, 0.75)], 3), face))
    for ox in (0.12, 0.22):
        items.append(("ink", circle(*P(ox, 0.86), h * 0.024)))
    items.append(("ink", ellipse(*P(0.39, 0.78), h * 0.016, h * 0.022)))
    items.append(("line", smooth_open([P(0.22, 0.73), P(0.29, 0.71), P(0.36, 0.73)], 2), max(5, int(h * 0.012))))
    return items


def bee(cx, cy, s, facing=1, name="bee"):
    """Cartoon bee, s = body length."""
    f = facing
    items = []
    items.append(("region", f"{name}-wing", ellipse(cx - f * s * 0.16, cy - s * 0.48, s * 0.26, s * 0.36, rot=-25 * f), WHITE))
    items.append(("region", f"{name}-wing", ellipse(cx + f * s * 0.2, cy - s * 0.48, s * 0.24, s * 0.34, rot=25 * f), WHITE))
    items.append(("region", f"{name}-body", ellipse(cx, cy, s * 0.5, s * 0.34), YELLOW))
    for k in (-0.12, 0.12):
        items.append(("line", [(cx + f * s * k - s * 0.04 * f, cy - s * 0.3), (cx + f * s * k + s * 0.04 * f, cy + s * 0.3)], max(8, int(s * 0.1))))
    items.append(("ink", [(cx - f * s * 0.5, cy - s * 0.06), (cx - f * s * 0.66, cy), (cx - f * s * 0.5, cy + s * 0.06)]))
    items.append(("ink", circle(cx + f * s * 0.34, cy - s * 0.07, s * 0.06)))
    return items


def car(x, ground_y, w, colour=RED, facing=1, glass="#BBDEFB", name="car", passenger=None):
    """Side-view family car; x = centre, w = length. passenger = skin colour to show a waving kid."""
    f = facing
    h = w * 0.42
    def P(px, py):
        return (x + f * px * w, ground_y - py * w)
    items = []
    items.append(("region", f"{name}-cabin", smooth([P(-0.32, 0.26), P(-0.24, 0.42), P(0.14, 0.43), P(0.3, 0.26)], 2), colour))
    items.append(("region", f"{name}-window", [P(-0.25, 0.28), P(-0.2, 0.38), P(-0.04, 0.38), P(-0.04, 0.28)], glass))
    items.append(("region", f"{name}-window", [P(0.02, 0.28), P(0.02, 0.38), P(0.12, 0.38), P(0.22, 0.28)], glass))
    if passenger:
        cx, cy = P(-0.13, 0.31)
        items.append(("region", f"{name}-kid", circle(cx, cy + w * 0.01, w * 0.055), passenger))
        for ex in (-0.018, 0.018):
            items.append(("ink", circle(cx + f * w * 0.012 + ex * w, cy, w * 0.007)))
    items.append(("region", f"{name}-body", smooth([P(-0.5, 0.07), P(-0.5, 0.25), P(-0.3, 0.29), P(0.3, 0.29), P(0.48, 0.22), P(0.5, 0.07)], 2), colour))
    items.append(("line", [P(-0.01, 0.27), P(-0.01, 0.1)], 6))
    items.append(("region", f"{name}-light", ellipse(*P(0.45, 0.19), w * 0.05, w * 0.038), YELLOW))
    for wx in (-0.3, 0.3):
        cx, cy = P(wx, 0.07)
        items.append(("region", f"{name}-tyre", circle(cx, cy, w * 0.085), NIGHT))
        items.append(("region", f"{name}-hub", circle(cx, cy, w * 0.05), GREY))
    return items


# ---------------------------------------------------------------- props
def pot(cx, base_y, w, h, colour=ROCK, band=None, name="pot", neck=0.45):
    items = [("region", name, smooth([(cx - w * neck / 2, base_y - h), (cx + w * neck / 2, base_y - h), (cx + w * 0.4, base_y - h * 0.82),
                                      (cx + w * 0.5, base_y - h * 0.45), (cx + w * 0.3, base_y), (cx - w * 0.3, base_y),
                                      (cx - w * 0.5, base_y - h * 0.45), (cx - w * 0.4, base_y - h * 0.82)], 2), colour)]
    items.append(("region", f"{name}-rim", ellipse(cx, base_y - h, w * neck / 2 + 12, max(h * 0.08, 18)), colour))
    if band:
        items.append(("region", f"{name}-band", [(cx - w * 0.48, base_y - h * 0.6), (cx + w * 0.48, base_y - h * 0.6),
                                                 (cx + w * 0.49, base_y - h * 0.44), (cx - w * 0.49, base_y - h * 0.44)], band))
    return items


def basket(cx, base_y, w, h, colour=STRAW, band=RED, name="basket", handle=False):
    items = []
    if handle:
        items.append(("region", f"{name}-handle", thick(arc(cx, base_y - h, w * 0.4, h * 0.9, 180, 360, 20), max(24, w * 0.08), caps=False), colour))
    items.append(("region", name, smooth([(cx - w / 2, base_y - h), (cx + w / 2, base_y - h), (cx + w * 0.38, base_y), (cx - w * 0.38, base_y)], 1), colour))
    if band:
        items.append(("region", f"{name}-band", [(cx - w * 0.47, base_y - h * 0.72), (cx + w * 0.47, base_y - h * 0.72),
                                                 (cx + w * 0.44, base_y - h * 0.48), (cx - w * 0.44, base_y - h * 0.48)], band))
    items.append(("line", [(cx - w * 0.4, base_y - h * 0.25), (cx + w * 0.4, base_y - h * 0.25)], 5))
    return items


def heap(cx, base_y, w, h, colour, bowl=BROWN, name="spice"):
    items = [("region", name, smooth([(cx - w * 0.45, base_y - h * 0.5), (cx - w * 0.15, base_y - h), (cx + w * 0.15, base_y - h), (cx + w * 0.45, base_y - h * 0.5)], 2), colour)]
    items.append(("region", f"{name}-bowl", arc(cx, base_y - h * 0.5, w * 0.5, h * 0.5, 0, 180, 20), bowl))
    return items


def brush(hand, tip, colour, handle=TRUNK, name="brush"):
    """Paint brush held at `hand`, bristles at `tip`."""
    hx, hy = hand
    tx, ty = tip
    L = math.hypot(tx - hx, ty - hy) or 1
    ux, uy = (tx - hx) / L, (ty - hy) / L
    back = (hx - ux * 40, hy - uy * 40)
    mid = (tx - ux * 55, ty - uy * 55)
    return [("region", f"{name}-handle", thick([back, mid], 32), handle),
            ("region", f"{name}-tip", smooth([(mid[0] - uy * 28, mid[1] + ux * 28), (tx - uy * 24, ty + ux * 24), (tx + ux * 30, ty + uy * 30),
                                              (tx + uy * 24, ty - ux * 24), (mid[0] + uy * 28, mid[1] - ux * 28)], 1), colour)]

"""Extra figure helpers for the Al-Ahsa scenes (people, animals, props).

Every helper returns an item list for Scene.extend():
    ("region", name, points, colour) | ("ink", points) | ("line", points, width)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403

# Extra colours used across Al-Ahsa scenes (kept few so each scene stays under 18).
TEAL = "#26A69A"
LIGHT_BLUE = "#90CAF9"
NAVY = "#3949AB"
LIME = "#C0CA33"
FLAMINGO = "#F48FB1"
STONE = "#D7B98E"
CAVE = "#A1785C"
CLAY = "#C8714A"


# ---------------------------------------------------------------- geometry
def thick(pts, w0, w1=None, cap=True):
    """Polygon outlining a polyline with width tapering w0 -> w1 (round caps)."""
    if w1 is None:
        w1 = w0
    n = len(pts)
    lens = [0.0]
    for i in range(1, n):
        lens.append(lens[-1] + math.dist(pts[i], pts[i - 1]))
    total = lens[-1] or 1
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - px, pts[1][1] - py
            k = 1
        elif i == n - 1:
            dx, dy = px - pts[i - 1][0], py - pts[i - 1][1]
            k = 1
        else:
            ax, ay = px - pts[i - 1][0], py - pts[i - 1][1]
            bx, by = pts[i + 1][0] - px, pts[i + 1][1] - py
            la, lb = math.hypot(ax, ay) or 1, math.hypot(bx, by) or 1
            dx, dy = ax / la + bx / lb, ay / la + by / lb
            cosh = max(0.5, (ax * bx + ay * by) / (la * lb) * 0.5 + 0.5) ** 0.5
            k = 1 / cosh
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * lens[i] / total) / 2 * k
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w, py - ny * w))
    out = list(left)
    if cap:
        (ex, ey), (qx, qy) = pts[-1], pts[-2]
        a = math.atan2(ey - qy, ex - qx)
        out += [(ex + math.cos(a + math.pi / 2 - t) * w1 / 2, ey + math.sin(a + math.pi / 2 - t) * w1 / 2)
                for t in [math.pi * j / 8 for j in range(1, 8)]]
    out += right[::-1]
    if cap:
        (sx, sy), (qx, qy) = pts[0], pts[1]
        a = math.atan2(sy - qy, sx - qx)
        out += [(sx + math.cos(a + math.pi / 2 - t) * w0 / 2, sy + math.sin(a + math.pi / 2 - t) * w0 / 2)
                for t in [math.pi * j / 8 for j in range(1, 8)]]
    return out


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def teardrop(cx, top_y, w, h):
    """Tassel/drop shape hanging from (cx, top_y)."""
    return smooth([(cx, top_y), (cx + w * 0.3, top_y + h * 0.35), (cx + w * 0.5, top_y + h * 0.75),
                   (cx, top_y + h), (cx - w * 0.5, top_y + h * 0.75), (cx - w * 0.3, top_y + h * 0.35)], 2)


# ---------------------------------------------------------------- face / heads
def face(cx, cy, r, look=0.0, beard=None, brows=False, name="p", skin=SKIN):
    """Face disc with eyes and a smile. look: -1..1 shifts features sideways."""
    items = [("region", f"{name}-face", circle(cx, cy, r), skin)]
    off = r * 0.22 * look
    if beard:
        items.append(("region", f"{name}-beard", arc(cx, cy, r, r, 12, 168, 20) +
                      smooth_open([(cx - r * 0.86, cy + r * 0.3), (cx - r * 0.5, cy + r * 0.12), (cx + off, cy + r * 0.2),
                                   (cx + r * 0.5, cy + r * 0.12), (cx + r * 0.86, cy + r * 0.3)][::-1], 2), beard))
    for sx in (-1, 1):
        items.append(("ink", ellipse(cx + off + sx * r * 0.36, cy - r * 0.06, r * 0.1, r * 0.14)))
        if brows:
            items.append(("line", arc(cx + off + sx * r * 0.36, cy - r * 0.2, r * 0.17, r * 0.1, 200, 340, 8), max(4, int(r * 0.06))))
    my = cy + r * (0.42 if beard else 0.3)
    items.append(("line", arc(cx + off, my - r * 0.14, r * 0.3, r * 0.2, 25, 155, 12), max(5, int(r * 0.07))))
    return items


def headwear(kind, x, hcy, r, colour=WHITE, hair=DARK_BROWN, look=0.0, name="p", phase="back", chest_y=None):
    """phase 'back' = parts behind the face/body, 'front' = parts over the face."""
    items = []
    if chest_y is None:
        chest_y = hcy + r * 2.2
    if kind in ("ghutra", "shemagh"):
        if phase == "back":
            items.append(("region", f"{name}-ghutra", smooth([
                (x - r * 1.12, hcy - r * 0.55), (x + r * 1.12, hcy - r * 0.55), (x + r * 1.3, hcy + r * 0.4),
                (x + r * 1.55, chest_y), (x + r * 0.8, chest_y - r * 0.15), (x, hcy + r * 1.05),
                (x - r * 0.8, chest_y - r * 0.15), (x - r * 1.55, chest_y), (x - r * 1.3, hcy + r * 0.4)], 2), colour))
        else:
            items.append(("region", f"{name}-ghutra-top", arc(x, hcy - r * 0.45, r * 1.16, r * 0.98, 180, 360) +
                          arc(x, hcy - r * 0.45, r * 1.16, r * 0.15, 0, 180), colour))
            cy0, rx, ry, t = hcy - r * 1.02, r * 0.98, r * 0.3, r * 0.34
            items.append(("region", f"{name}-agal", arc(x, cy0, rx, ry, 0, 180, 20) + arc(x, cy0 + t, rx * 1.02, ry, 180, 0, 20), BLACK_CLOTH))
    elif kind == "wrap":
        if phase == "front":
            items.append(("region", f"{name}-wrap", smooth([(x - r * 1.12, hcy - r * 0.25), (x - r * 1.2, hcy - r * 0.9),
                                                           (x - r * 0.4, hcy - r * 1.45), (x + r * 0.5, hcy - r * 1.42),
                                                           (x + r * 1.2, hcy - r * 0.9), (x + r * 1.12, hcy - r * 0.25),
                                                           (x, hcy - r * 0.48)], 2), colour))
            items.append(("line", smooth_open([(x - r * 0.95, hcy - r * 0.62), (x - r * 0.1, hcy - r * 1.0), (x + r * 0.95, hcy - r * 0.95)], 2), 6))
            items.append(("line", smooth_open([(x - r * 0.75, hcy - r * 1.05), (x + r * 0.2, hcy - r * 1.28), (x + r * 0.85, hcy - r * 1.18)], 2), 6))
    elif kind == "scarf":
        if phase == "back":
            items.append(("region", f"{name}-scarf", smooth([
                (x - r * 1.25, hcy - r * 0.1), (x - r * 1.05, hcy - r * 1.05), (x, hcy - r * 1.32), (x + r * 1.05, hcy - r * 1.05),
                (x + r * 1.25, hcy - r * 0.1), (x + r * 1.45, chest_y), (x, chest_y + r * 0.35), (x - r * 1.45, chest_y)], 2), colour))
        else:
            items.append(("region", f"{name}-scarf-front", arc(x, hcy - r * 0.42, r * 1.1, r * 0.9, 180, 360) +
                          arc(x, hcy - r * 0.42, r * 1.1, r * 0.16, 0, 180), colour))
    elif kind == "cap":
        if phase == "front":
            items.append(("region", f"{name}-cap", arc(x, hcy - r * 0.42, r * 1.05, r * 0.92, 180, 360), colour))
            d = 1 if look >= 0 else -1
            items.append(("region", f"{name}-brim", ellipse(x + d * r * 0.95, hcy - r * 0.44, r * 0.78, r * 0.2), colour))
    elif kind == "hair":
        if phase == "front":
            items.append(("region", f"{name}-hair", arc(x, hcy - r * 0.2, r * 1.04, r * 0.88, 180, 360) +
                          [(x + r * 0.85, hcy - r * 0.45), (x + r * 0.45, hcy - r * 0.62), (x + r * 0.1, hcy - r * 0.5),
                           (x - r * 0.3, hcy - r * 0.65), (x - r * 0.7, hcy - r * 0.48)], hair))
    elif kind == "taqiyah":
        if phase == "front":
            items.append(("region", f"{name}-taqiyah", arc(x, hcy - r * 0.42, r * 0.95, r * 0.65, 180, 360), colour))
    return items


# ---------------------------------------------------------------- people
def figure(x, feet_y, h, outfit="thobe", head="ghutra", skin=SKIN, cloth=WHITE, accent=RED, trim=GOLD,
           headcol=WHITE, shoe=DARK_BROWN, hair=DARK_BROWN, child=False, look=0.0, beard=None, brows=False,
           lhand=None, rhand=None, lfront=True, rfront=True, sit=False, name="p", legs=True):
    """Front-facing friendly person. lhand/rhand: list of points [elbow, hand] or [hand] (absolute);
    None = hanging down. 'l' is the figure's right side on screen-left. sit=True compresses the legs
    (top is then feet_y - 0.8h). Returns (items, info) with info['hands'] etc."""
    top = feet_y - (h * 0.8 if sit else h)
    r = h * (0.135 if child else 0.105)
    hcy = top + r
    neck_y = hcy + r * 0.92
    sw = h * (0.15 if child else 0.15)
    sh_y = neck_y + h * 0.025
    hem_y = feet_y - h * 0.045
    hem_w = sw * 1.28
    waist_y = sh_y + (feet_y - sh_y) * 0.42
    arm_w = h * (0.085 if child else 0.075)
    hand_r = max(h * (0.05 if child else 0.042), 32)
    items_back, items_body, items_front = [], [], []
    info = {"head": (x, hcy, r), "neck": neck_y, "waist": waist_y, "hem": hem_y, "sw": sw}

    def default_hand(side):
        return [(x + side * sw * 1.12, sh_y + h * 0.18), (x + side * sw * 1.1, sh_y + h * 0.36)]

    long_sleeve = outfit not in ("tshirt",)
    sleeve_col = {"bisht": accent, "hasawi": accent, "abaya": BLACK_CLOTH, "uniform": cloth, "tshirt": cloth}.get(outfit, cloth)
    hands = []
    for side, spec, front in ((-1, lhand, lfront), (1, rhand, rfront)):
        pts = spec or default_hand(side)
        shoulder = (x + side * sw * 0.78, sh_y + h * 0.04)
        path = [shoulder] + list(pts)
        hx, hy = path[-1]
        # stop the sleeve short of the hand centre so the hand reads as a round fist
        px, py = path[-2]
        dd = math.hypot(hx - px, hy - py) or 1
        end = (hx - (hx - px) / dd * hand_r * 0.6, hy - (hy - py) / dd * hand_r * 0.6)
        arm_path = path[:-1] + [end]
        tgt = items_front if front else items_back
        if outfit in ("hasawi", "bisht"):
            tgt.append(("region", f"{name}-sleeve", thick(arm_path, arm_w * 1.05, arm_w * 1.75), sleeve_col))
        elif long_sleeve:
            tgt.append(("region", f"{name}-sleeve", thick(arm_path, arm_w, arm_w * 0.9), sleeve_col))
        else:
            tgt.append(("region", f"{name}-arm", thick(arm_path, arm_w * 0.8, arm_w * 0.72), skin))
            seg = [path[0], lerp(path[0], path[1], 0.45)]
            tgt.append(("region", f"{name}-sleeve", thick(seg, arm_w * 1.3, arm_w * 1.15), cloth))
        tgt.append(("region", f"{name}-hand", circle(hx, hy, hand_r), skin))
        hands.append((hx, hy))
    info["hands"] = hands

    hb = headwear(head, x, hcy, r, headcol, hair, look, name, "back", chest_y=sh_y + h * 0.13)
    # body
    def robe(colour, wscale=1.0, bottom=hem_y, nm="robe"):
        hw = hem_w * wscale
        return ("region", f"{name}-{nm}", smooth([(x - sw * 0.5, neck_y), (x - sw * 0.98, sh_y + h * 0.01), (x - sw * 1.05, sh_y + h * 0.1),
                                                  (x - hw, bottom), (x + hw, bottom), (x + sw * 1.05, sh_y + h * 0.1),
                                                  (x + sw * 0.98, sh_y + h * 0.01), (x + sw * 0.5, neck_y)], 1), colour)
    shoes = []
    if legs:
        for sx in (-1, 1):
            k = 1.2 if child else 1.0
            shoes.append(("region", f"{name}-shoe", ellipse(x + sx * sw * 0.48, feet_y - h * 0.03, h * 0.07 * k, h * 0.036 * k), shoe))
    if outfit in ("thobe", "bisht"):
        items_body.append(robe(cloth))
        items_body.append(("line", [(x, neck_y + h * 0.02), (x, neck_y + h * 0.13)], 6))
        if outfit == "bisht":
            for sx in (-1, 1):
                items_body.append(("region", f"{name}-bisht", smooth([(x + sx * sw * 0.32, neck_y), (x + sx * sw * 1.02, sh_y + h * 0.0),
                                                                       (x + sx * sw * 1.12, sh_y + h * 0.1), (x + sx * hem_w * 1.12, hem_y - h * 0.05),
                                                                       (x + sx * hem_w * 0.42, hem_y - h * 0.05)], 1), accent))
                items_body.append(("region", f"{name}-bisht-trim", [(x + sx * sw * 0.32, neck_y), (x + sx * sw * 0.62, neck_y + h * 0.01),
                                                                     (x + sx * hem_w * 0.66, hem_y - h * 0.05), (x + sx * hem_w * 0.42, hem_y - h * 0.05)], trim))
    elif outfit == "abaya":
        items_body.append(robe(BLACK_CLOTH))
    elif outfit == "hasawi":
        items_body.append(robe(cloth, 0.95))
        items_body.append(("region", f"{name}-hem", [(x - hem_w * 0.9, hem_y - h * 0.09), (x + hem_w * 0.9, hem_y - h * 0.09),
                                                      (x + hem_w * 0.95, hem_y), (x - hem_w * 0.95, hem_y)], trim))
        for sx in (-1, 1):
            items_body.append(("region", f"{name}-thawb", smooth([(x + sx * sw * 0.35, neck_y), (x + sx * sw * 1.0, sh_y),
                                                                   (x + sx * sw * 1.2, sh_y + h * 0.12), (x + sx * hem_w * 1.3, hem_y - h * 0.14),
                                                                   (x + sx * hem_w * 0.45, hem_y - h * 0.14)], 1), accent))
            items_body.append(("region", f"{name}-thawb-trim", [(x + sx * sw * 0.35, neck_y), (x + sx * sw * 0.68, neck_y + h * 0.01),
                                                                 (x + sx * hem_w * 0.72, hem_y - h * 0.14), (x + sx * hem_w * 0.45, hem_y - h * 0.14)], trim))
    elif outfit == "uniform":
        items_body.append(robe(cloth, 0.9, waist_y + h * 0.05, "blouse"))
        items_body.append(("region", f"{name}-pinafore", smooth([(x - sw * 0.55, sh_y + h * 0.07), (x + sw * 0.55, sh_y + h * 0.07),
                                                                 (x + sw * 0.85, waist_y), (x + hem_w * 1.05, hem_y), (x - hem_w * 1.05, hem_y),
                                                                 (x - sw * 0.85, waist_y)], 1), accent))
        for sx in (-1, 1):
            items_body.append(("line", [(x + sx * sw * 0.5, sh_y + h * 0.075), (x + sx * sw * 0.7, sh_y)], 8))
    elif outfit in ("tshirt", "tracksuit"):
        pants = accent if outfit == "tshirt" else cloth
        ank = feet_y - h * 0.05
        items_body.append(("region", f"{name}-pants", [(x - sw * 0.92, waist_y), (x + sw * 0.92, waist_y), (x + sw * 0.9, ank),
                                                       (x + sw * 0.08, ank), (x, waist_y + h * 0.16), (x - sw * 0.08, ank), (x - sw * 0.9, ank)], pants))
        items_body.append(("region", f"{name}-top", smooth([(x - sw * 0.5, neck_y), (x - sw * 0.98, sh_y + h * 0.01), (x - sw * 1.04, sh_y + h * 0.1),
                                                           (x - sw * 0.98, waist_y + h * 0.05), (x + sw * 0.98, waist_y + h * 0.05),
                                                           (x + sw * 1.04, sh_y + h * 0.1), (x + sw * 0.98, sh_y + h * 0.01), (x + sw * 0.5, neck_y)], 1), cloth))
        if outfit == "tracksuit":
            items_body.append(("line", [(x, neck_y + h * 0.03), (x, waist_y + h * 0.04)], 6))
            for sx in (-1, 1):
                items_body.append(("line", [(x + sx * sw * 0.55, waist_y + h * 0.1), (x + sx * sw * 0.55, ank - h * 0.02)], 6))
        else:
            items_body.append(("line", arc(x, neck_y - h * 0.005, sw * 0.38, h * 0.04, 10, 170, 10), 6))
    items = []
    items += hb
    items += items_back
    items += items_body
    items += shoes
    if head in ("ghutra", "shemagh", "scarf"):
        pass
    items += face(x, hcy, r, look, beard, brows, name, skin)
    items += headwear(head, x, hcy, r, headcol, hair, look, name, "front")
    items += items_front
    return items, info


# ---------------------------------------------------------------- props
def basket(cx, top_y, w, h, colour=MUD, name="basket", handle=True):
    items = []
    if handle:
        items.append(("line", arc(cx, top_y, w * 0.38, h * 0.75, 180, 360, 16), 10))
    body = [(cx - w / 2, top_y), (cx + w / 2, top_y), (cx + w * 0.38, top_y + h), (cx - w * 0.38, top_y + h)]
    items.append(("region", name, smooth(body, 1), colour))
    for i in (1, 2):
        yy = top_y + h * i / 3
        f = 1 - 0.24 * i / 3
        items.append(("line", [(cx - w / 2 * f * 0.88, yy), (cx + w / 2 * f * 0.88, yy)], 5))
    items.append(("region", f"{name}-rim", rect(cx - w * 0.53, top_y - h * 0.08, cx + w * 0.53, top_y + h * 0.12), colour))
    return items


def date_bunch(cx, top_y, w, h, colour=ORANGE, stem=YELLOW, name="dates"):
    """A hanging date cluster: stem fan + bumpy bunch."""
    items = [("region", f"{name}-stem", [(cx - w * 0.08, top_y), (cx + w * 0.08, top_y), (cx + w * 0.3, top_y + h * 0.35), (cx - w * 0.3, top_y + h * 0.35)], stem)]
    pts = []
    n = 14
    for i in range(n):
        t = 2 * math.pi * i / n
        rr = 1.0 if i % 2 == 0 else 0.86
        pts.append((cx + math.cos(t) * w * 0.5 * rr, top_y + h * 0.62 + math.sin(t) * h * 0.38 * rr))
    items.append(("region", name, smooth(pts, 2), colour))
    for dx, dy in ((-0.22, 0.55), (0.18, 0.62), (-0.02, 0.8)):
        items.append(("line", arc(cx + dx * w, top_y + dy * h, w * 0.06, h * 0.07, 100, 260, 6), 5))
    return items


def big_palm(x, base_y, top_y, lean=0.0, trunk=TRUNK, leaf=LEAF, w=110, n_leaves=8, span=1.0, name="palm", rings=True, dates=None):
    """Tall palm; (x, base_y) is the trunk foot, top_y the crown; lean shifts the crown sideways (px)."""
    items = []
    tx = x + lean
    items.append(("region", f"{name}-trunk", smooth([(x - w * 0.55, base_y), (x + w * 0.55, base_y),
                                                      (tx + w * 0.3, top_y + 10), (tx - w * 0.3, top_y + 10)], 0) if False else
                  [(x - w * 0.55, base_y), (x + w * 0.55, base_y), (tx + w * 0.32, top_y + 10), (tx - w * 0.32, top_y + 10)], trunk))
    if rings:
        hgt = base_y - top_y
        for i in range(1, int(hgt / (w * 0.7))):
            t = i * w * 0.7 / hgt
            cxp = x + lean * t
            ww = w * (0.55 - 0.23 * t)
            items.append(("line", [(cxp - ww * 0.9, base_y - hgt * t + 8), (cxp, base_y - hgt * t - 6), (cxp + ww * 0.9, base_y - hgt * t + 8)], 5))
    L = 380 * span
    angs = [200, 228, 256, 284, 312, 340, 10, 160][:n_leaves]
    for ang in angs:
        a = math.radians(ang)
        tip = (tx + math.cos(a) * L, top_y + math.sin(a) * L * 0.72 + L * 0.26)
        mid = ((tx + tip[0]) / 2, (top_y + tip[1]) / 2 - L * 0.18)
        dx, dy = tip[0] - tx, tip[1] - top_y
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln * L * 0.13, dx / ln * L * 0.13
        items.append(("region", f"{name}-leaf", smooth([(tx, top_y), (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx * 0.6, mid[1] - ny * 0.6)], 2), leaf))
        items.append(("line", smooth_open([(tx + dx * 0.12, top_y + dy * 0.12 - L * 0.03), (mid[0], mid[1] + L * 0.01), lerp(tip, mid, 0.25)], 2), 5))
    items.append(("region", f"{name}-crown", circle(tx, top_y, w * 0.42), trunk))
    return items


def distant_palm(x, base_y, h, trunk=TRUNK, leaf=LEAF, name="farpalm"):
    """Simple background palm: chunky trunk + 5 broad fronds (sized to stay finger-friendly)."""
    tw = max(h * 0.05, 22)
    tx, ty = x + h * 0.05, base_y - h
    items = [("region", f"{name}-trunk", [(x - tw, base_y), (x + tw, base_y), (tx + tw * 0.7, ty), (tx - tw * 0.7, ty)], trunk)]
    for ang in (190, 248, 298, 352):
        a = math.radians(ang)
        L = h * 0.5
        tip = (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.8 + L * 0.25)
        mid = ((tx + tip[0]) / 2, (ty + tip[1]) / 2 - L * 0.16)
        dx, dy = tip[0] - tx, tip[1] - ty
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln * L * 0.26, dx / ln * L * 0.26
        items.append(("region", f"{name}-leaf", smooth([(tx, ty), (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx * 0.5, mid[1] - ny * 0.5)], 2), leaf))
    return items


def lantern(cx, top_y, w, h, frame=GOLD, glass=YELLOW, name="lantern", chain=60):
    items = []
    if chain:
        items.append(("line", [(cx, top_y - chain), (cx, top_y)], 6))
    outer = [(cx - w * 0.18, top_y), (cx + w * 0.18, top_y), (cx + w * 0.5, top_y + h * 0.22), (cx + w * 0.5, top_y + h * 0.82),
             (cx + w * 0.3, top_y + h), (cx - w * 0.3, top_y + h), (cx - w * 0.5, top_y + h * 0.82), (cx - w * 0.5, top_y + h * 0.22)]
    items.append(("region", f"{name}-frame", outer, frame))
    items.append(("region", f"{name}-glass", smooth([(cx - w * 0.36, top_y + h * 0.26), (cx + w * 0.36, top_y + h * 0.26),
                                                     (cx + w * 0.36, top_y + h * 0.78), (cx - w * 0.36, top_y + h * 0.78)], 1), glass))
    items.append(("line", [(cx, top_y + h * 0.3), (cx, top_y + h * 0.74)], 5))
    return items


def jar(cx, base_y, w, h, colour=CLAY, name="jar", band=None):
    """Clay jar (bulging pot with a neck and a flared lip), one region."""
    right = smooth_open([(cx + w * 0.3, base_y - h), (cx + w * 0.2, base_y - h * 0.86), (cx + w * 0.24, base_y - h * 0.78),
                         (cx + w * 0.5, base_y - h * 0.52), (cx + w * 0.44, base_y - h * 0.14), (cx + w * 0.24, base_y)], 2)
    left = [(2 * cx - px, py) for px, py in right][::-1]
    items = [("region", name, right + left, colour)]
    if band:
        items.append(("line", arc(cx, base_y - h * 0.5, w * 0.49, h * 0.06, 10, 170, 12), 6))
    return items


# ---------------------------------------------------------------- animals
def flamingo(x, feet_y, h, facing=1, body=FLAMINGO, wing=PINK, beak=CREAM, name="flamingo", one_leg=True, head_down=False):
    """Standing flamingo, h = total height (feet to top of head)."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    lw = max(10, int(h * 0.018))
    # legs (thin black strokes, with knee)
    items.append(("line", [P(0.0, 0.0), P(0.0, 0.22), P(-0.02, 0.48)], lw))
    if one_leg:
        items.append(("line", [P(-0.02, 0.48), P(0.04, 0.33), P(-0.08, 0.38)], lw))
    else:
        items.append(("line", [P(0.08, 0.0), P(0.06, 0.24), P(0.02, 0.48)], lw))
    # tail + body
    items.append(("region", f"{name}-body", smooth([P(-0.28, 0.66), P(-0.12, 0.74), P(0.12, 0.72), P(0.22, 0.6), P(0.1, 0.48),
                                                    P(-0.1, 0.46), P(-0.3, 0.55), P(-0.36, 0.58)], 3), body))
    items.append(("region", f"{name}-wing", smooth([P(-0.3, 0.6), P(-0.12, 0.7), P(0.1, 0.66), P(0.02, 0.56), P(-0.18, 0.54), P(-0.34, 0.56)], 2), wing))
    items.append(("line", smooth_open([P(-0.22, 0.6), P(-0.06, 0.63), P(0.04, 0.62)], 2), 5))
    # neck S-curve
    if head_down:
        neck = [P(0.16, 0.66), P(0.26, 0.78), P(0.3, 0.62), P(0.34, 0.4)]
        hd = P(0.36, 0.36)
    else:
        neck = [P(0.16, 0.66), P(0.27, 0.74), P(0.22, 0.86), P(0.12, 0.92), P(0.14, 0.98)]
        hd = P(0.18, 0.95)
    items.append(("region", f"{name}-neck", thick(smooth_open(neck, 2), h * 0.07, h * 0.055), body))
    items.append(("region", f"{name}-head", circle(*hd, h * 0.05), body))
    ex, ey = hd
    # hooked beak
    if head_down:
        bk = [(ex + f * h * 0.01, ey + h * 0.03), (ex + f * h * 0.09, ey + h * 0.02), (ex + f * h * 0.1, ey + h * 0.12), (ex + f * h * 0.06, ey + h * 0.16), (ex - f * h * 0.01, ey + h * 0.07)]
        items.append(("region", f"{name}-beak", smooth(bk, 1), beak))
        items.append(("ink", smooth([(ex + f * h * 0.098, ey + h * 0.11), (ex + f * h * 0.06, ey + h * 0.165), (ex + f * h * 0.05, ey + h * 0.125)], 1)))
        items.append(("ink", circle(ex + f * h * 0.0, ey - h * 0.01, h * 0.011)))
    else:
        bk = [(ex + f * h * 0.03, ey - h * 0.03), (ex + f * h * 0.13, ey - h * 0.01), (ex + f * h * 0.15, ey + h * 0.06), (ex + f * h * 0.12, ey + h * 0.08), (ex + f * h * 0.04, ey + h * 0.03)]
        items.append(("region", f"{name}-beak", smooth(bk, 1), beak))
        items.append(("ink", smooth([(ex + f * h * 0.152, ey + h * 0.02), (ex + f * h * 0.15, ey + h * 0.065), (ex + f * h * 0.12, ey + h * 0.083), (ex + f * h * 0.115, ey + h * 0.05)], 1)))
        items.append(("ink", circle(ex + f * h * 0.0, ey - h * 0.012, h * 0.011)))
    return items


def heron(x, feet_y, h, facing=1, body=GREY, neckc=WHITE, beak=YELLOW, name="heron"):
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    lw = max(10, int(h * 0.02))
    items.append(("line", [P(-0.06, 0.0), P(-0.04, 0.42)], lw))
    items.append(("line", [P(0.06, 0.0), P(0.04, 0.42)], lw))
    items.append(("line", [P(-0.14, 0.0), P(0.02, 0.0)], lw - 2))
    items.append(("line", [P(-0.02, 0.0), P(0.14, 0.0)], lw - 2))
    items.append(("region", f"{name}-body", smooth([P(-0.36, 0.52), P(-0.2, 0.66), P(0.08, 0.7), P(0.2, 0.6), P(0.06, 0.42), P(-0.16, 0.42)], 3), body))
    items.append(("region", f"{name}-wing", smooth([P(-0.4, 0.5), P(-0.2, 0.62), P(0.04, 0.62), P(-0.08, 0.5), P(-0.28, 0.46)], 2), DARK_BROWN if False else GREY))
    neck = [P(0.14, 0.62), P(0.24, 0.72), P(0.17, 0.82), P(0.2, 0.92)]
    items.append(("region", f"{name}-neck", thick(smooth_open(neck, 2), h * 0.08, h * 0.065), neckc))
    hx, hy = P(0.21, 0.94)
    items.append(("region", f"{name}-head", circle(hx, hy, h * 0.055), neckc))
    items.append(("region", f"{name}-crest", smooth([(hx - f * h * 0.02, hy - h * 0.055), (hx - f * h * 0.2, hy - h * 0.08), (hx - f * h * 0.17, hy - h * 0.02), (hx - f * h * 0.03, hy + h * 0.01)], 1), BLACK_CLOTH))
    items.append(("region", f"{name}-beak", [(hx + f * h * 0.035, hy - h * 0.045), (hx + f * h * 0.25, hy + h * 0.005), (hx + f * h * 0.035, hy + h * 0.05)], beak))
    items.append(("ink", circle(hx + f * h * 0.012, hy - h * 0.012, h * 0.011)))
    return items


def bird(cx, cy, s):
    """Simple 'v' flying bird stroke."""
    return [("line", smooth_open([(cx - s, cy - s * 0.2), (cx - s * 0.45, cy - s * 0.45), (cx, cy), (cx + s * 0.45, cy - s * 0.45), (cx + s, cy - s * 0.2)], 2), 7)]


def horse2(x, feet_y, h, facing=1, body=BLACK_CLOTH, mane=BLACK_CLOTH, hoof=DARK_BROWN, name="horse", prance=True):
    """Side-view Arabian horse, h = height at the withers. Returns (items, info)."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    items = []
    lw = h * 0.18
    hw, hh = max(h * 0.07, 40), max(h * 0.085, 48)
    info = {"P": P}

    def hoof_at(px, py, ang=0):
        pts = [(px - hw, py - hh * 0.2), (px + hw, py - hh * 0.2), (px + hw * 1.15, py + hh * 0.8), (px - hw * 1.15, py + hh * 0.8)]
        return rotate(pts, ang, px, py) if ang else pts

    # far legs (behind the body)
    far = [[P(-0.3, 0.72), P(-0.36, 0.42), P(-0.3, 0.1)], [P(0.28, 0.72), P(0.3, 0.38), P(0.3, 0.1)]]
    for leg in far:
        items.append(("region", f"{name}-leg-far", thick(leg, lw * 0.95, lw * 0.62), body))
        items.append(("region", f"{name}-hoof", hoof_at(*leg[-1]), hoof))
    # tail: lifted, then flowing down
    items.append(("region", f"{name}-tail", smooth([P(-0.5, 0.98), P(-0.72, 1.08), P(-0.9, 0.9), P(-0.92, 0.55), P(-0.82, 0.32),
                                                    P(-0.78, 0.55), P(-0.72, 0.8), P(-0.55, 0.86)], 2), mane))
    # neck and head
    items.append(("region", f"{name}-neck", smooth([P(0.08, 1.0), P(0.32, 1.32), P(0.54, 1.52), P(0.74, 1.46), P(0.78, 1.28), P(0.66, 0.84), P(0.42, 0.7)], 2), body))
    items.append(("region", f"{name}-head", smooth([P(0.54, 1.52), P(0.7, 1.58), P(0.84, 1.45), P(1.02, 1.2), P(1.02, 1.08),
                                                    P(0.88, 1.04), P(0.76, 1.16), P(0.6, 1.3)], 2), body))
    items.append(("region", f"{name}-mane", smooth([P(0.12, 1.02), P(0.34, 1.34), P(0.56, 1.56), P(0.62, 1.46), P(0.44, 1.24), P(0.26, 0.98)], 2), mane))
    items.append(("region", f"{name}-ear", smooth([P(0.53, 1.48), P(0.6, 1.76), P(0.75, 1.5)], 1), body))
    # body
    items.append(("region", f"{name}-body", smooth([P(-0.62, 0.8), P(-0.52, 1.04), P(-0.1, 0.99), P(0.25, 1.06), P(0.62, 0.9),
                                                    P(0.58, 0.6), P(0.0, 0.48), P(-0.48, 0.52)], 3), body))
    ex, ey = P(0.77, 1.4)
    items.append(("region", f"{name}-eye", circle(ex, ey, max(h * 0.055, 34)), WHITE))
    items.append(("ink", circle(ex + f * h * 0.012, ey, max(h * 0.028, 13))))
    items.append(("ink", ellipse(*P(0.96, 1.15), max(h * 0.016, 8), max(h * 0.024, 11))))
    items.append(("line", smooth_open([P(0.9, 1.08), P(0.95, 1.065), P(1.0, 1.09)], 1), 5))
    info["bit"] = P(0.9, 1.12)
    # near legs
    back_near = [P(-0.4, 0.72), P(-0.46, 0.42), P(-0.4, 0.1)]
    front_near = [P(0.4, 0.72), P(0.56, 0.48), P(0.5, 0.3)] if prance else [P(0.4, 0.72), P(0.42, 0.38), P(0.42, 0.1)]
    for leg in (back_near, front_near):
        items.append(("region", f"{name}-leg", thick(leg, lw, lw * 0.64), body))
        if leg is front_near and prance:
            items.append(("region", f"{name}-hoof", hoof_at(*leg[-1], ang=-35 * f), hoof))
        else:
            items.append(("region", f"{name}-hoof", hoof_at(*leg[-1]), hoof))
    return items, info

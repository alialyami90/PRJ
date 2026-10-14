"""Extra figure helpers for the AlUla scenes (built on Scripts/scene_kit.py).

All helpers return item lists for Scene.extend():
("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2].parent / "Scripts"))
from scene_kit import *  # noqa: E402,F403


class Items(list):
    """A list of items that can also carry anchor points (hands, head...)."""


# ---------------------------------------------------------------- geometry
def thick(path, widths):
    """Closed polygon around an open polyline; `widths` is one width per point (or a number)."""
    if not isinstance(widths, (list, tuple)):
        widths = [widths] * len(path)
    elif len(widths) != len(path):
        k = len(widths) - 1
        res = []
        for i in range(len(path)):
            t = i / max(len(path) - 1, 1) * k
            j = min(int(t), k - 1)
            res.append(widths[j] + (widths[j + 1] - widths[j]) * (t - j))
        widths = res
    left, right = [], []
    n = len(path)
    for i in range(n):
        if i == 0:
            dx, dy = path[1][0] - path[0][0], path[1][1] - path[0][1]
        elif i == n - 1:
            dx, dy = path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]
        else:
            d1 = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
            d2 = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
            l1, l2 = math.hypot(*d1) or 1, math.hypot(*d2) or 1
            dx, dy = d1[0] / l1 + d2[0] / l2, d1[1] / l1 + d2[1] / l2
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        left.append((path[i][0] + nx * w, path[i][1] + ny * w))
        right.append((path[i][0] - nx * w, path[i][1] - ny * w))
    return left + right[::-1]


def band(cx, cy, r_out, r_in, a0, a1, n=24, cy_in=None, rx_scale=1.0):
    """Curved band between two concentric-ish arcs (angles in degrees)."""
    cy_in = cy if cy_in is None else cy_in
    outer = arc(cx, cy, r_out * rx_scale, r_out, a0, a1, n)
    inner = arc(cx, cy_in, r_in * rx_scale, r_in, a1, a0, n)
    return outer + inner


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ---------------------------------------------------------------- person
ARM_POSES = {
    # (elbow, hand) relative to the shoulder, in units of h; +x = outward from the body
    "down": ((0.05, 0.15), (0.07, 0.31)),
    "up": ((0.09, -0.11), (0.12, -0.27)),
    "wave": ((0.17, 0.02), (0.20, -0.17)),
    "out": ((0.11, 0.13), (0.24, 0.10)),
    "point": ((0.14, -0.05), (0.29, -0.16)),
    "front": ((0.07, 0.16), (-0.03, 0.24)),
    "hold": ((0.08, 0.15), (0.05, 0.26)),
    "high": ((0.13, -0.07), (0.27, -0.22)),
}


def person(x, feet_y, h, *, child=False, outfit="thobe", robe=WHITE, cloak=BROWN, trim=GOLD,
           top=RED, bottom=BLUE, shoes=DARK_BROWN, top_style="tshirt", top_accent=None,
           headwear="shemagh", head_colour=RED, hair=DARK_BROWN, skin=SKIN,
           arms=("down", "down"), facing=0, sunglasses=False, hem=None, legs=True, seated=False, mouth="smile",
           name="person"):
    """Front-view friendly person, (x, feet_y) = point between the feet, h = standing height.

    outfit:    thobe | bisht | dress (long dress, hem band in `trim`) | abaya | modern (top + trousers)
               | modern_dress (top + long skirt in `bottom`)
    top_style: tshirt | hoodie | jacket | sweater (modern tops; `top_accent` for stripe/pocket)
    headwear:  shemagh | ghutra | taqiyah | hijab | cap | hair | girl_hair | beanie | none
               (`head_colour` colours shemagh/hijab/cap/beanie)
    arms:      (left_pose, right_pose): names from ARM_POSES or ((ex, ey), (hx, hy)) tuples
    seated:    front-view sitting; feet stay on feet_y, hips drop to feet_y - 0.27h
    Returns Items with .hands (left, right), .head (cx, cy, r).
    """
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    head_r = h * (0.125 if child else 0.105)
    sw = h * (0.13 if child else 0.15)          # shoulder half width
    top_y = feet_y - h
    head_cy = top_y + head_r
    neck_y = head_cy + head_r * 0.92
    sh_y = neck_y + h * 0.03
    waist_y = feet_y - h * (0.43 if child else 0.47)
    drop = 0.0
    if seated:
        hip_seated = feet_y - h * 0.27
        drop = hip_seated - waist_y
        head_cy += drop; neck_y += drop; sh_y += drop; waist_y += drop; top_y += drop
    hem_y = feet_y - h * 0.055
    hem_w = sw * 1.3
    long_robe = outfit in ("thobe", "bisht", "dress", "abaya", "modern_dress")
    shoe_rx, shoe_ry = max(h * 0.08, 44), max(h * 0.042, 26)

    # ---- legs and shoes
    if seated:
        knee_y = waist_y + h * 0.04
        leg_col = bottom if outfit == "modern" else (BLACK_CLOTH if outfit == "abaya" else robe)
        if outfit == "modern_dress":
            leg_col = bottom
        for sx in (-1, 1):
            R(f"{name}-shin", [(x + sx * sw * 0.08, knee_y), (x + sx * sw * 0.9, knee_y),
                               (x + sx * sw * 0.82, feet_y - shoe_ry), (x + sx * sw * 0.16, feet_y - shoe_ry)], leg_col)
        for sx in (-1, 1):
            R(f"{name}-shoe", ellipse(x + sx * sw * 0.52, feet_y - shoe_ry * 0.9, shoe_rx, shoe_ry), shoes)
        R(f"{name}-lap", smooth([(x - sw * 1.05, waist_y - h * 0.03), (x + sw * 1.05, waist_y - h * 0.03),
                                 (x + sw * 1.0, knee_y + h * 0.05), (x - sw * 1.0, knee_y + h * 0.05)], 2), leg_col)
    elif legs:
        for sx in (-1, 1):
            R(f"{name}-shoe", ellipse(x + sx * sw * 0.5, feet_y - shoe_ry, shoe_rx, shoe_ry), shoes)
        if outfit == "modern":
            ww = sw * 0.92
            ank = feet_y - shoe_ry * 1.3
            R(f"{name}-trousers", [(x - ww, waist_y - h * 0.02), (x + ww, waist_y - h * 0.02), (x + ww * 0.95, ank),
                                   (x + ww * 0.12, ank), (x, waist_y + h * 0.13), (x - ww * 0.12, ank), (x - ww * 0.95, ank)], bottom)

    # ---- hood / headcloth drapes behind the body
    if headwear == "girl_hair":
        R(f"{name}-hair-back", smooth([(x - head_r * 1.15, head_cy - head_r * 0.3), (x, head_cy - head_r * 1.2),
                                       (x + head_r * 1.15, head_cy - head_r * 0.3), (x + head_r * 1.25, sh_y + h * 0.08),
                                       (x - head_r * 1.25, sh_y + h * 0.08)], 2), hair)
    if outfit == "modern" and top_style == "hoodie" or (outfit == "modern_dress" and top_style == "hoodie"):
        R(f"{name}-hood", smooth([(x - head_r * 1.25, neck_y - head_r * 0.35), (x + head_r * 1.25, neck_y - head_r * 0.35),
                                  (x + head_r * 1.35, sh_y + h * 0.04), (x - head_r * 1.35, sh_y + h * 0.04)], 2), top)

    # ---- body
    hands = []
    arm_specs = []
    for i, side in enumerate((-1, 1)):
        pose = arms[i]
        sxp, syp = x + side * sw * 0.92, sh_y + h * 0.03
        if not isinstance(pose, str) and pose[0] == "to":
            hand = pose[1]
            elbow = ((sxp + hand[0]) / 2 + side * h * 0.05, (syp + hand[1]) / 2 + h * 0.02)
        else:
            e, hd = ARM_POSES[pose] if isinstance(pose, str) else pose
            elbow = (sxp + side * e[0] * h, syp + e[1] * h)
            hand = (sxp + side * hd[0] * h, syp + hd[1] * h)
        arm_specs.append((side, (sxp, syp), elbow, hand))
        hands.append(hand)

    if outfit in ("modern", "modern_dress"):
        if outfit == "modern_dress":
            R(f"{name}-skirt", smooth([(x - sw * 0.9, waist_y - h * 0.03), (x + sw * 0.9, waist_y - h * 0.03),
                                       (x + hem_w * 1.05, hem_y), (x - hem_w * 1.05, hem_y)], 1) if not seated else
              smooth([(x - sw * 0.95, waist_y - h * 0.03), (x + sw * 0.95, waist_y - h * 0.03),
                      (x + sw * 1.05, waist_y + h * 0.09), (x - sw * 1.05, waist_y + h * 0.09)], 1), bottom)
            if hem and not seated:
                R(f"{name}-skirt-hem", [(x - hem_w * 0.99, hem_y - h * 0.07), (x + hem_w * 0.99, hem_y - h * 0.07),
                                        (x + hem_w * 1.05, hem_y), (x - hem_w * 1.05, hem_y)], hem)
        R(f"{name}-top", smooth([(x - sw * 0.75, sh_y - h * 0.02), (x + sw * 0.75, sh_y - h * 0.02), (x + sw * 1.02, sh_y + h * 0.04),
                                 (x + sw * 1.0, waist_y + h * 0.04), (x - sw * 1.0, waist_y + h * 0.04), (x - sw * 1.02, sh_y + h * 0.04)], 2), top)
        if top_style == "hoodie" and not seated and top_accent != "none":
            R(f"{name}-pocket", smooth([(x - sw * 0.6, waist_y - h * 0.08), (x + sw * 0.6, waist_y - h * 0.08),
                                        (x + sw * 0.75, waist_y + h * 0.02), (x - sw * 0.75, waist_y + h * 0.02)], 1), top_accent or top)
            for sx in (-1, 1):
                it.append(("line", [(x + sx * sw * 0.22, neck_y + h * 0.02), (x + sx * sw * 0.25, neck_y + h * 0.11)], 6))
        elif top_style == "jacket":
            it.append(("line", [(x, neck_y + h * 0.03), (x, waist_y + h * 0.035)], 7))
            for sx in (-1, 1):
                R(f"{name}-collar", [(x + sx * sw * 0.08, neck_y), (x + sx * sw * 0.7, neck_y - h * 0.01),
                                     (x + sx * sw * 0.5, neck_y + h * 0.08)], top_accent or top)
        elif top_style == "sweater":
            R(f"{name}-stripe", [(x - sw * 1.01, sh_y + h * 0.1), (x + sw * 1.01, sh_y + h * 0.1),
                                 (x + sw * 1.0, sh_y + h * 0.16), (x - sw * 1.0, sh_y + h * 0.16)], top_accent or WHITE)
        elif top_style == "tshirt" and top_accent:
            R(f"{name}-star", star(x, sh_y + h * 0.14, h * 0.085, h * 0.042), top_accent)
    else:
        body_col = BLACK_CLOTH if outfit == "abaya" else robe
        if seated:
            pts = [(x - sw, sh_y - h * 0.01), (x + sw, sh_y - h * 0.01), (x + sw * 1.08, waist_y + h * 0.03), (x - sw * 1.08, waist_y + h * 0.03)]
        else:
            pts = [(x - sw * 0.8, sh_y - h * 0.025), (x + sw * 0.8, sh_y - h * 0.025), (x + sw * 1.02, sh_y + h * 0.04),
                   (x + hem_w, hem_y), (x - hem_w, hem_y), (x - sw * 1.02, sh_y + h * 0.04)]
        R(f"{name}-robe", smooth(pts, 1), body_col)
        if outfit == "thobe" or outfit == "bisht":
            it.append(("line", [(x, neck_y + h * 0.02), (x, neck_y + h * 0.14)], 6))
        if outfit == "dress" and not seated:
            R(f"{name}-hem", [(x - hem_w * 0.96, hem_y - h * 0.08), (x + hem_w * 0.96, hem_y - h * 0.08),
                              (x + hem_w, hem_y), (x - hem_w, hem_y)], trim)
            R(f"{name}-belt", [(x - sw * 1.04, waist_y - h * 0.045), (x + sw * 1.04, waist_y - h * 0.045),
                               (x + sw * 1.07, waist_y + h * 0.025), (x - sw * 1.07, waist_y + h * 0.025)], trim)
        if outfit == "bisht":
            bot = hem_y - h * 0.035 if not seated else waist_y + h * 0.03
            for sx in (-1, 1):
                R(f"{name}-bisht", [(x + sx * sw * 0.3, sh_y - h * 0.03), (x + sx * sw * 1.12, sh_y + h * 0.02),
                                    (x + sx * hem_w * 1.12, bot), (x + sx * hem_w * 0.38, bot)], cloak)
                R(f"{name}-bisht-trim", [(x + sx * sw * 0.3, sh_y - h * 0.03), (x + sx * sw * 0.58, sh_y - h * 0.02),
                                         (x + sx * hem_w * 0.62, bot), (x + sx * hem_w * 0.38, bot)], trim)

    # ---- arms (in front of the body)
    for side, sh, el, hd in arm_specs:
        aw = h * (0.085 if outfit in ("bisht",) else 0.07)
        sleeve = cloak if outfit == "bisht" else (BLACK_CLOTH if outfit == "abaya" else
                                                  (top if outfit in ("modern", "modern_dress") else robe))
        wrist = lerp(el, hd, 0.78)
        if outfit in ("modern", "modern_dress") and top_style == "tshirt":
            R(f"{name}-arm", thick([sh, el, wrist], [aw, aw * 0.85, aw * 0.75]), skin)
            R(f"{name}-sleeve", thick([lerp(sh, el, -0.15), lerp(sh, el, 0.6)], [aw * 1.25, aw * 1.15]), sleeve)
        else:
            R(f"{name}-sleeve", thick([sh, el, wrist], [aw * 1.05, aw * 0.95, aw * 0.85]), sleeve)
        R(f"{name}-hand", circle(hd[0], hd[1], max(h * 0.046, 27)), skin)

    # ---- neck + head
    if headwear in ("shemagh", "ghutra"):
        hc = head_colour if headwear == "shemagh" else WHITE
        for sx in (-1, 1):
            R(f"{name}-headcloth-flap", smooth([(x + sx * head_r * 0.7, head_cy + head_r * 0.2), (x + sx * head_r * 1.25, head_cy - head_r * 0.1),
                                                (x + sx * head_r * 1.55, sh_y + h * 0.03), (x + sx * head_r * 1.35, sh_y + h * 0.19),
                                                (x + sx * head_r * 0.75, sh_y + h * 0.15), (x + sx * head_r * 0.45, sh_y)], 1), hc)
    if headwear == "hijab":
        R(f"{name}-hijab", smooth([(x - head_r * 1.3, head_cy - head_r * 0.2), (x - head_r * 0.9, head_cy - head_r * 1.15),
                                   (x + head_r * 0.9, head_cy - head_r * 1.15), (x + head_r * 1.3, head_cy - head_r * 0.2),
                                   (x + head_r * 1.35, sh_y + h * 0.06), (x, sh_y + h * 0.1), (x - head_r * 1.35, sh_y + h * 0.06)], 2), head_colour)
    R(f"{name}-face", circle(x, head_cy, head_r), skin)
    # face features
    off = head_r * 0.15 * facing
    ey = head_cy + head_r * 0.02
    if sunglasses:
        for sx in (-1, 1):
            R(f"{name}-glasses", smooth(rect(x + off + sx * head_r * 0.9, ey - head_r * 0.32, x + off + sx * head_r * 0.05, ey + head_r * 0.3), 2), BLACK_CLOTH)
        it.append(("line", [(x + off - head_r * 0.1, ey - head_r * 0.08), (x + off + head_r * 0.1, ey - head_r * 0.08)], 7))
    else:
        for sx in (-1, 1):
            it.append(("ink", ellipse(x + off + sx * head_r * 0.36, ey, head_r * 0.1, head_r * 0.14)))
    if mouth == "open":
        it.append(("ink", arc(x + off, head_cy + head_r * 0.38, head_r * 0.24, head_r * 0.2, 0, 180, 14)))
    else:
        it.append(("line", arc(x + off, head_cy + head_r * 0.3, head_r * 0.32, head_r * 0.2, 20, 160, 12), max(5, int(head_r * 0.07))))
    # headwear on top
    if headwear in ("shemagh", "ghutra"):
        hc = head_colour if headwear == "shemagh" else WHITE
        R(f"{name}-headcloth-top", band(x, head_cy + head_r * 0.1, head_r * 1.32, head_r * 1.0, 180, 360, cy_in=head_cy + head_r * 0.4), hc)
        it.append(("ink", band(x, head_cy + head_r * 0.12, head_r * 1.2, head_r * 1.02, 200, 340, cy_in=head_cy + head_r * 0.16)))
    elif headwear == "hijab":
        R(f"{name}-hijab-front", band(x, head_cy + head_r * 0.08, head_r * 1.12, head_r * 1.0, 185, 355, cy_in=head_cy + head_r * 0.38), head_colour)
    elif headwear == "taqiyah":
        R(f"{name}-taqiyah", arc(x, head_cy - head_r * 0.4, head_r * 0.92, head_r * 0.7, 180, 360) +
          [(x + head_r * 0.92, head_cy - head_r * 0.35), (x - head_r * 0.92, head_cy - head_r * 0.35)], WHITE)
    elif headwear == "hair":
        R(f"{name}-hair", arc(x, head_cy, head_r * 1.06, head_r * 1.08, 180, 360, 20) +
          [(x + head_r * 0.85, head_cy - head_r * 0.45), (x + head_r * 0.3, head_cy - head_r * 0.6), (x - head_r * 0.2, head_cy - head_r * 0.42),
           (x - head_r * 0.6, head_cy - head_r * 0.55), (x - head_r * 0.95, head_cy - head_r * 0.2)], hair)
    elif headwear == "girl_hair":
        R(f"{name}-fringe", arc(x, head_cy, head_r * 1.06, head_r * 1.08, 180, 360, 20) +
          [(x + head_r * 0.9, head_cy - head_r * 0.25), (x + head_r * 0.5, head_cy - head_r * 0.5), (x, head_cy - head_r * 0.38),
           (x - head_r * 0.5, head_cy - head_r * 0.5), (x - head_r * 0.9, head_cy - head_r * 0.25)], hair)
        for sx in (-1, 1):
            R(f"{name}-bow", circle(x + sx * head_r * 0.95, head_cy - head_r * 0.75, max(head_r * 0.28, 24)), head_colour)
    elif headwear == "cap":
        f = facing or 1
        R(f"{name}-cap", arc(x, head_cy - head_r * 0.25, head_r * 1.04, head_r * 0.95, 180, 360) +
          [(x + head_r * 1.04, head_cy - head_r * 0.2), (x - head_r * 1.04, head_cy - head_r * 0.2)], head_colour)
        R(f"{name}-cap-brim", smooth([(x - head_r * 0.2 * f, head_cy - head_r * 0.48), (x + head_r * 1.7 * f, head_cy - head_r * 0.48),
                                      (x + head_r * 1.7 * f, head_cy + head_r * 0.0), (x - head_r * 0.2 * f, head_cy - head_r * 0.08)], 1), head_colour)
    elif headwear == "beanie":
        R(f"{name}-beanie", arc(x, head_cy - head_r * 0.3, head_r * 1.04, head_r * 1.0, 180, 360) +
          [(x + head_r * 1.04, head_cy - head_r * 0.25)], head_colour)
        R(f"{name}-beanie-band", rect(x - head_r * 1.08, head_cy - head_r * 0.55, x + head_r * 1.08, head_cy - head_r * 0.2), WHITE)
        R(f"{name}-pompom", circle(x, head_cy - head_r * 1.38, max(head_r * 0.36, 30)), WHITE)
    it.hands = hands
    it.head = (x, head_cy, head_r)
    it.waist = (x, waist_y)
    it.shoulders = (sh_y, sw)
    return Items([i for i in it if i is not None]) if None in it else it


def _fix(items):
    out = Items(i for i in items if i is not None)
    for k in ("hands", "head", "waist", "shoulders"):
        if hasattr(items, k):
            setattr(out, k, getattr(items, k))
    return out


_person_raw = person


def person(*a, **k):  # noqa: F811
    return _fix(_person_raw(*a, **k))


# ---------------------------------------------------------------- animals
def camel2(x, feet_y, h, facing=1, body=DUNE, blanket=RED, band_col=YELLOW, tassel=ORANGE, saddle=True,
           rope=False, name="camel"):
    """Chunky side-view camel. (x, feet_y) = centre of the feet line, h = height to the hump top."""
    f = facing
    P = lambda px, py: (x + f * px * h, feet_y - py * h)  # noqa: E731
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    # far legs (slightly darker? same colour, outline separates)
    for lx in (-0.24, 0.24):
        R(f"{name}-leg", smooth([P(lx - 0.1, 0.6), P(lx + 0.1, 0.6), P(lx + 0.07, 0.34), P(lx + 0.075, 0.28), P(lx + 0.065, 0.06),
                                 P(lx - 0.065, 0.06), P(lx - 0.075, 0.28), P(lx - 0.07, 0.34)], 1), body)
        R(f"{name}-foot", smooth([P(lx - 0.09, 0.1), P(lx + 0.11, 0.1), P(lx + 0.13, 0.0), P(lx - 0.11, 0.0)], 1), body)
    R(f"{name}-tail", smooth([P(-0.48, 0.8), P(-0.62, 0.64), P(-0.66, 0.4), P(-0.56, 0.42), P(-0.5, 0.6), P(-0.42, 0.7)], 2), body)
    R(f"{name}-body", smooth([P(-0.56, 0.6), P(-0.5, 0.82), P(-0.25, 1.0), P(-0.05, 1.02), P(0.18, 0.92),
                              P(0.42, 0.8), P(0.52, 0.62), P(0.3, 0.48), P(-0.4, 0.48)], 3), body)
    R(f"{name}-neck", smooth([P(0.34, 0.86), P(0.56, 0.84), P(0.64, 1.0), P(0.7, 1.2), P(0.88, 1.24), P(0.85, 1.06),
                              P(0.76, 0.82), P(0.6, 0.56), P(0.42, 0.54)], 2), body)
    R(f"{name}-ear", ellipse(*P(0.73, 1.33), h * 0.065, h * 0.1, rot=-25 * f), body)
    R(f"{name}-head", smooth([P(0.68, 1.17), P(0.74, 1.32), P(0.88, 1.35), P(1.04, 1.26), P(1.07, 1.14), P(0.96, 1.08), P(0.76, 1.08)], 2), body)
    it.append(("ink", circle(*P(0.86, 1.25), h * 0.024)))
    it.append(("line", [P(0.99, 1.2), P(1.03, 1.18)], 6))
    it.append(("line", smooth_open([P(0.92, 1.12), P(0.98, 1.13), P(1.03, 1.12)], 2), 5))
    for lx in (-0.42, 0.42):
        R(f"{name}-leg", smooth([P(lx - 0.1, 0.6), P(lx + 0.1, 0.6), P(lx + 0.07, 0.34), P(lx + 0.075, 0.28), P(lx + 0.065, 0.06),
                                 P(lx - 0.065, 0.06), P(lx - 0.075, 0.28), P(lx - 0.07, 0.34)], 1), body)
        R(f"{name}-foot", smooth([P(lx - 0.09, 0.1), P(lx + 0.11, 0.1), P(lx + 0.14, 0.0), P(lx - 0.12, 0.0)], 1), body)
    if saddle:
        R(f"{name}-blanket", smooth([P(-0.36, 0.94), P(0.16, 0.94), P(0.22, 0.58), P(-0.42, 0.58)], 1), blanket)
        R(f"{name}-blanket-band", [P(-0.415, 0.69), P(0.205, 0.69), P(0.22, 0.58), P(-0.42, 0.58)], band_col)
        for tx in (-0.3, -0.1, 0.1):
            R(f"{name}-tassel", smooth([P(tx - 0.08, 0.585), P(tx + 0.08, 0.585), P(tx + 0.03, 0.38), P(tx - 0.03, 0.38)], 1), tassel)
        R(f"{name}-saddle", smooth([P(-0.26, 0.92), P(0.06, 0.92), P(0.1, 1.08), P(0.02, 1.1), P(-0.1, 1.02), P(-0.22, 1.1), P(-0.3, 1.08)], 1), BROWN)
    it.halter = P(1.02, 1.13)
    it.seat = P(-0.1, 1.0)
    return it


def fox(x, base_y, h, facing=1, body=ORANGE, light=CREAM, name="fox"):
    """Sitting fennec fox, front view with huge ears. h = height to the ear tips."""
    f = facing
    P = lambda px, py: (x + f * px * h, base_y - py * h)  # noqa: E731
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    R(f"{name}-tail", smooth([P(-0.12, 0.02), P(-0.45, 0.0), P(-0.66, 0.12), P(-0.66, 0.32), P(-0.5, 0.3), P(-0.4, 0.14), P(-0.14, 0.14)], 2), body)
    R(f"{name}-tail-tip", smooth([P(-0.52, 0.04), P(-0.68, 0.14), P(-0.68, 0.32), P(-0.5, 0.31), P(-0.52, 0.18)], 2), light)
    R(f"{name}-body", smooth([P(-0.26, 0.0), P(0.26, 0.0), P(0.24, 0.24), P(0.14, 0.46), P(-0.14, 0.46), P(-0.24, 0.24)], 2), body)
    R(f"{name}-chest", smooth([P(-0.12, 0.12), P(0.12, 0.12), P(0.1, 0.32), P(0.0, 0.44), P(-0.1, 0.32)], 2), light)
    for lx in (-0.1, 0.1):
        R(f"{name}-leg", rect(*P(lx - 0.055, 0.2), *P(lx + 0.055, 0.03)) if f == 1 else rect(*P(lx + 0.055, 0.2), *P(lx - 0.055, 0.03)), body)
        R(f"{name}-paw", ellipse(*P(lx, 0.035), h * 0.08, h * 0.045), light)
    for sx in (-1, 1):
        base_in, base_out, tip = P(sx * 0.05, 0.66), P(sx * 0.25, 0.54), P(sx * 0.4, 1.0)
        R(f"{name}-ear", smooth([base_in, tip, base_out, P(sx * 0.15, 0.5)], 1), body)
        c = ((base_in[0] + base_out[0] + tip[0]) / 3, (base_in[1] + base_out[1] + tip[1]) / 3)
        R(f"{name}-ear-in", smooth(scale([base_in, tip, base_out], 0.62, *c), 1), PINK)
    R(f"{name}-head", smooth([P(-0.26, 0.6), P(-0.12, 0.72), P(0.12, 0.72), P(0.26, 0.6), P(0.24, 0.48),
                              P(0.08, 0.36), P(-0.08, 0.36), P(-0.24, 0.48)], 2), body)
    R(f"{name}-muzzle", smooth([P(-0.13, 0.5), P(0.13, 0.5), P(0.07, 0.37), P(-0.07, 0.37)], 2), light)
    it.append(("ink", ellipse(*P(0.0, 0.46), h * 0.035, h * 0.025)))
    it.append(("line", arc(*P(0.0, 0.42), h * 0.04, h * 0.025, 20, 160, 8), 5))
    for ex in (-0.11, 0.11):
        it.append(("ink", ellipse(*P(ex, 0.57), h * 0.026, h * 0.036)))
    return it


def frog(cx, base_y, w, body=GREEN, belly=YELLOW, name="frog", mouth=True, feet=True):
    """Front-view sitting frog, w wide."""
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    s = w
    for sx in (-1, 1):
        R(f"{name}-leg", smooth([(cx + sx * s * 0.15, base_y - s * 0.12), (cx + sx * s * 0.42, base_y - s * 0.38),
                                 (cx + sx * s * 0.62, base_y - s * 0.2), (cx + sx * s * 0.55, base_y), (cx + sx * s * 0.25, base_y)], 2), body)
    R(f"{name}-body", smooth([(cx - s * 0.4, base_y), (cx - s * 0.44, base_y - s * 0.32), (cx - s * 0.28, base_y - s * 0.52),
                              (cx + s * 0.28, base_y - s * 0.52), (cx + s * 0.44, base_y - s * 0.32), (cx + s * 0.4, base_y)], 2), body)
    R(f"{name}-belly", ellipse(cx, base_y - s * 0.16, s * 0.24, s * 0.15), belly)
    for sx in (-1, 1):
        R(f"{name}-eye", circle(cx + sx * s * 0.22, base_y - s * 0.55, s * 0.16), body)
        R(f"{name}-eye-white", circle(cx + sx * s * 0.22, base_y - s * 0.56, s * 0.105), WHITE)
        it.append(("ink", circle(cx + sx * s * 0.22, base_y - s * 0.55, s * 0.045)))
        if feet:
            R(f"{name}-foot", ellipse(cx + sx * s * 0.2, base_y - s * 0.01, s * 0.14, s * 0.06), body)
    if mouth:
        it.append(("line", arc(cx, base_y - s * 0.4, s * 0.2, s * 0.08, 15, 165, 12), 7))
    return it


def kingfisher(x, y, s, facing=1, back=BLUE, belly=ORANGE, name="kingfisher"):
    """Perched kingfisher; (x, y) = feet on branch, s ~ body height."""
    f = facing
    P = lambda px, py: (x + f * px * s, y - py * s)  # noqa: E731
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    R(f"{name}-tail", smooth([P(-0.2, 0.25), P(-0.55, -0.12), P(-0.38, -0.2), P(-0.05, 0.15)], 1), back)
    R(f"{name}-body", smooth([P(-0.3, 0.3), P(-0.15, 0.62), P(0.2, 0.62), P(0.3, 0.35), P(0.18, 0.04), P(-0.12, 0.04)], 2), back)
    R(f"{name}-belly", smooth([P(-0.02, 0.05), P(0.2, 0.08), P(0.3, 0.36), P(0.18, 0.55), P(0.02, 0.32)], 2), belly)
    R(f"{name}-wing", smooth([P(-0.34, 0.45), P(-0.04, 0.55), P(0.06, 0.32), P(-0.42, 0.06)], 2), back)
    R(f"{name}-head", circle(*P(0.06, 0.78), s * 0.24), back)
    R(f"{name}-cheek", ellipse(*P(0.12, 0.69), s * 0.15, s * 0.08), belly)
    R(f"{name}-beak", smooth([P(0.2, 0.86), P(0.7, 0.76), P(0.22, 0.66)], 1), DARK_BROWN)
    it.append(("ink", circle(*P(0.1, 0.83), s * 0.045)))
    return it


# ---------------------------------------------------------------- props & scenery
def palm2(x, base_y, h, trunk=TRUNK, leaf=LEAF, dates=True, lean=0.0, name="palm"):
    """Fuller date palm: curved trunk, 7 fronds, date bunches."""
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    top = (x + h * lean, base_y - h)
    mid = (x + h * lean * 0.3, base_y - h * 0.5)
    spine = smooth_open([(x, base_y), mid, top], 3)
    n = len(spine)
    R(f"{name}-trunk", thick(spine, [h * 0.11 - h * 0.05 * i / (n - 1) for i in range(n)]), trunk)
    for i in range(1, 6):
        p = spine[int(i * (n - 1) / 6)]
        w = (h * 0.11 - h * 0.05 * i / 6) / 2 * 0.8
        it.append(("line", [(p[0] - w, p[1] + 6), (p[0] + w, p[1] - 6)], 5))
    if dates:
        for sx in (-1, 1):
            R(f"{name}-dates", smooth([(top[0] + sx * h * 0.01, top[1] + h * 0.01), (top[0] + sx * h * 0.16, top[1] + h * 0.03),
                                       (top[0] + sx * h * 0.11, top[1] + h * 0.2), (top[0] + sx * h * 0.03, top[1] + h * 0.14)], 2), ORANGE)
    for ang in (180, 210, 245, 280, 310, 340, 0):
        a = math.radians(ang)
        L = h * 0.5
        tip = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.55 + L * (0.35 if ang in (180, 0) else 0.15))
        midp = ((top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2 - h * 0.08)
        d = math.hypot(tip[0] - top[0], tip[1] - top[1]) or 1
        nx, ny = -(tip[1] - top[1]) / d * h * 0.085, (tip[0] - top[0]) / d * h * 0.085
        R(f"{name}-leaf", smooth([top, (midp[0] + nx, midp[1] + ny), tip, (midp[0] - nx * 0.6, midp[1] - ny * 0.6)], 2), leaf)
    R(f"{name}-crown", circle(top[0], top[1], max(h * 0.05, 30)), trunk)
    return it


def campfire(cx, base_y, w, name="fire"):
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    for i, sx in enumerate((-1, 1)):
        R(f"{name}-log", thick([(cx - sx * w * 0.5, base_y - w * 0.02), (cx + sx * w * 0.42, base_y - w * 0.22)], w * 0.17), TRUNK)
    R(f"{name}-flame", smooth([(cx - w * 0.32, base_y - w * 0.12), (cx - w * 0.36, base_y - w * 0.45), (cx - w * 0.2, base_y - w * 0.4),
                               (cx - w * 0.15, base_y - w * 0.8), (cx, base_y - w * 0.6), (cx + w * 0.12, base_y - w * 1.0),
                               (cx + w * 0.22, base_y - w * 0.55), (cx + w * 0.34, base_y - w * 0.62), (cx + w * 0.32, base_y - w * 0.12)], 2), ORANGE)
    R(f"{name}-flame-in", smooth([(cx - w * 0.16, base_y - w * 0.14), (cx - w * 0.14, base_y - w * 0.4), (cx - w * 0.02, base_y - w * 0.32),
                                  (cx + w * 0.06, base_y - w * 0.6), (cx + w * 0.16, base_y - w * 0.36), (cx + w * 0.17, base_y - w * 0.14)], 2), YELLOW)
    R(f"{name}-stones", smooth([(cx - w * 0.6, base_y + w * 0.02), (cx - w * 0.55, base_y - w * 0.08), (cx + w * 0.55, base_y - w * 0.08),
                                (cx + w * 0.6, base_y + w * 0.02), (cx + w * 0.5, base_y + w * 0.1), (cx - w * 0.5, base_y + w * 0.1)], 2), GREY)
    return it


def stick_with_treat(hand, tip, treat=WHITE, name="stick"):
    """A roasting stick from a hand to a tip with a marshmallow on the end."""
    it = Items()
    it.append(("region", f"{name}", thick([hand, tip], 30), TRUNK))
    dx, dy = tip[0] - hand[0], tip[1] - hand[1]
    ln = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    c = (tip[0] - dx / ln * 30, tip[1] - dy / ln * 30)
    it.append(("region", f"{name}-marshmallow", ellipse(c[0], c[1], 44, 32, rot=ang), treat))
    return it


def water_jar(cx, base_y, h, colour=ROCK, name="jar", rim=True):
    it = Items()
    it.append(("region", f"{name}", smooth([(cx - h * 0.14, base_y - h * 0.82), (cx + h * 0.14, base_y - h * 0.82), (cx + h * 0.12, base_y - h * 0.68),
                                            (cx + h * 0.42, base_y - h * 0.45), (cx + h * 0.3, base_y - h * 0.08), (cx + h * 0.12, base_y),
                                            (cx - h * 0.12, base_y), (cx - h * 0.3, base_y - h * 0.08), (cx - h * 0.42, base_y - h * 0.45),
                                            (cx - h * 0.12, base_y - h * 0.68)], 2), colour))
    if rim:
        it.append(("region", f"{name}-rim", ellipse(cx, base_y - h * 0.86, h * 0.2, h * 0.08), colour))
    it.append(("region", f"{name}-band", smooth([(cx - h * 0.39, base_y - h * 0.5), (cx + h * 0.39, base_y - h * 0.5),
                                                 (cx + h * 0.4, base_y - h * 0.38), (cx - h * 0.4, base_y - h * 0.38)], 1), BLUE))
    return it


def telescope(base_x, base_y, h, tube=BLUE, legs=GREY, angle=-35, name="scope"):
    """Telescope on a tripod; returns .eyepiece point."""
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    head = (base_x, base_y - h * 0.62)
    for fx in (-0.32, 0.0, 0.32):
        R(f"{name}-leg", thick([head, (base_x + fx * h, base_y)], h * 0.06), legs)
    a = math.radians(angle)
    L = h * 0.75
    back = (head[0] - math.cos(a) * L * 0.4, head[1] - math.sin(a) * L * 0.4)
    front = (head[0] + math.cos(a) * L * 0.6, head[1] + math.sin(a) * L * 0.6)
    R(f"{name}-tube", thick([back, front], [h * 0.12, h * 0.17]), tube)
    R(f"{name}-lens", thick([lerp(back, front, 0.9), lerp(back, front, 1.06)], h * 0.21), GOLD)
    R(f"{name}-band", thick([lerp(back, front, 0.36), lerp(back, front, 0.52)], h * 0.165), GOLD)
    R(f"{name}-eyepiece", thick([lerp(back, front, -0.14), back], h * 0.09), legs)
    R(f"{name}-mount", circle(head[0], head[1], h * 0.075), legs)
    it.eyepiece = lerp(back, front, -0.14)
    return it


def balloon(cx, top_y, w, colours=(RED, YELLOW), basket=TRUNK, name="balloon", basket_h=None, rope=0.32, basket_w=0.4):
    """Hot-air balloon w wide; returns .basket_rect (x0, y0, x1, y1)."""
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    r = w / 2
    cy = top_y + r
    neck_y = cy + r * 1.25
    bh = basket_h or w * 0.28
    by0 = neck_y + w * rope
    bx0, bx1 = cx - w * basket_w / 2, cx + w * basket_w / 2
    # ropes
    for sx in (-1, 1):
        it.append(("line", [(cx + sx * r * 0.3, neck_y), (cx + sx * w * basket_w * 0.47, by0)], 7))
    # envelope gores
    outline_pts = arc(cx, cy, r, r, 160, 380, 40) + [(cx + r * 0.32, neck_y), (cx - r * 0.32, neck_y)]
    R(f"{name}", smooth(outline_pts, 1), colours[0])
    n = 5
    for i in range(n):
        if i % 2 == 0:
            continue
        t0, t1 = -1 + 2 * i / n, -1 + 2 * (i + 1) / n
        pts = []
        for k in range(21):
            yy = top_y + (neck_y - top_y) * k / 20
            # half-width of envelope at this height
            if yy <= cy + r * 0.34:
                hw = math.sqrt(max(r * r - (yy - cy) ** 2, 0))
            else:
                y0 = cy + r * 0.34
                hw0 = math.sqrt(r * r - (r * 0.34) ** 2)
                hw = hw0 + (r * 0.32 - hw0) * (yy - y0) / (neck_y - y0)
            pts.append((yy, hw))
        left = [(cx + t0 * hw * 0.98, yy) for yy, hw in pts]
        right = [(cx + t1 * hw * 0.98, yy) for yy, hw in pts][::-1]
        R(f"{name}-gore", left + right, colours[1])
    if w >= 400:
        R(f"{name}-skirt", [(cx - r * 0.34, neck_y - w * 0.02), (cx + r * 0.34, neck_y - w * 0.02), (cx + r * 0.26, neck_y + w * 0.08),
                        (cx - r * 0.26, neck_y + w * 0.08)], colours[2] if len(colours) > 2 else colours[1])
    it.basket_rect = (bx0, by0, bx1, by0 + bh)
    it.basket = basket
    return it


def basket_front(rect_, colour=TRUNK, name="basket"):
    x0, y0, x1, y1 = rect_
    it = Items()
    it.append(("region", f"{name}", smooth([(x0, y0), (x1, y0), (x1 - (x1 - x0) * 0.06, y1), (x0 + (x1 - x0) * 0.06, y1)], 1), colour))
    it.append(("region", f"{name}-rim", rect(x0 - 10, y0 - 14, x1 + 10, y0 + 22), DARK_BROWN))
    for k in (1, 2):
        yy = y0 + 22 + (y1 - y0 - 22) * k / 3
        it.append(("line", [(x0 + 20, yy), (x1 - 20, yy)], 5))
    return it


def phone(cx, cy, w, colour=PURPLE, name="phone", rot=0):
    it = Items()
    body = rotate(smooth(rect(cx - w / 2, cy - w * 0.9, cx + w / 2, cy + w * 0.9), 2), rot, cx, cy)
    screen = rotate(rect(cx - w * 0.28, cy - w * 0.64, cx + w * 0.28, cy + w * 0.52), rot, cx, cy)
    it.append(("region", name, body, colour))
    it.append(("region", name + "-screen", screen, SKY))
    return it


def moon(cx, cy, r, name="moon"):
    return [("region", name, arc(cx, cy, r, r, 60, 300, 36) + arc(cx + r * 0.45, cy - r * 0.15, r * 0.8, r * 0.8, 260, 100, 30)[::1][::-1][::-1], "#FFF59D")]


def crescent(cx, cy, r, colour="#FFF59D", name="moon"):
    outer = arc(cx, cy, r, r, 50, 310, 40)
    inner = arc(cx + r * 0.42, cy - r * 0.12, r * 0.78, r * 0.78, 290, 70, 30)
    return [("region", name, outer + inner, colour)]


def twinkle(cx, cy, r, colour=YELLOW, name="star"):
    return [("region", name, star(cx, cy, r, r * 0.45, 5), colour)]


def rock_blob(points, colour=ROCK, name="rock", it=2):
    return [("region", name, smooth(points, it), colour)]


def hill(top, bottom=H, iterations=3):
    """Terrain band: a smoothed top edge from x=0 to x=W, closed straight down to `bottom`."""
    pts = smooth_open(top, iterations)
    return pts + [(pts[-1][0], bottom), (pts[0][0], bottom)]


def cat(x, base_y, h, facing=1, body=GREY, light=WHITE, name="cat"):
    """Sitting cat, front view with a curled-up tail. h = height to the ear tips."""
    f = facing
    P = lambda px, py: (x + f * px * h, base_y - py * h)  # noqa: E731
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    R(f"{name}-tail", thick(smooth_open([P(0.2, 0.06), P(0.5, 0.08), P(0.58, 0.3), P(0.48, 0.48)], 2), h * 0.1), body)
    R(f"{name}-body", smooth([P(-0.28, 0.0), P(0.28, 0.0), P(0.26, 0.26), P(0.16, 0.5), P(-0.16, 0.5), P(-0.26, 0.26)], 2), body)
    R(f"{name}-chest", smooth([P(-0.13, 0.08), P(0.13, 0.08), P(0.11, 0.32), P(0.0, 0.44), P(-0.11, 0.32)], 2), light)
    for lx in (-0.12, 0.12):
        R(f"{name}-paw", ellipse(*P(lx, 0.045), h * 0.11, h * 0.06), light)
    for sx in (-1, 1):
        R(f"{name}-ear", [P(sx * 0.02, 0.8), P(sx * 0.3, 1.04), P(sx * 0.33, 0.62)], body)
    R(f"{name}-head", ellipse(*P(0.0, 0.66), h * 0.3, h * 0.24), body)
    R(f"{name}-muzzle", ellipse(*P(0.0, 0.57), h * 0.13, h * 0.08), light)
    it.append(("ink", [P(-0.04, 0.63), P(0.04, 0.63), P(0.0, 0.59)]))
    for ex in (-0.12, 0.12):
        it.append(("ink", ellipse(*P(ex, 0.7), h * 0.03, h * 0.045)))
    return it


def crenellated(x0, y0, x1, y1, tooth=60, depth=45, kind="square"):
    """Rectangle whose top edge has merlons (square) or Najdi triangles (tri), as ONE polygon."""
    n = max(2, int(round((x1 - x0) / (tooth * 2))))
    step = (x1 - x0) / n
    top = []
    for k in range(n):
        a, b = x0 + k * step, x0 + (k + 1) * step
        if kind == "tri":
            top += [(a, y0), (a + step * 0.5, y0 - depth)]
        else:
            top += [(a, y0 - depth), (a + step * 0.5, y0 - depth), (a + step * 0.5, y0), (b, y0)]
    if kind == "tri":
        top.append((x1, y0))
    else:
        top = top[:-1] + [(x1, y0 - depth)]
    return top + [(x1, y1), (x0, y1)]


def lion(x, base_y, h, facing=1, body=DUNE, mane=MUD, name="lion"):
    """Sitting lion in side view (for carved reliefs). h = height to the top of the mane."""
    f = facing
    P = lambda px, py: (x + f * px * h, base_y - py * h)  # noqa: E731
    it = Items()
    R = lambda *a: it.append(("region", *a))  # noqa: E731
    R(f"{name}-tail", thick(smooth_open([P(-0.38, 0.1), P(-0.62, 0.12), P(-0.72, 0.32), P(-0.62, 0.44)], 2), h * 0.1), body)
    R(f"{name}-tail-tuft", circle(*P(-0.6, 0.48), h * 0.11), mane)
    R(f"{name}-body", smooth([P(-0.45, 0.0), P(0.3, 0.0), P(0.32, 0.4), P(0.2, 0.62), P(-0.1, 0.6), P(-0.42, 0.42)], 2), body)
    R(f"{name}-leg", smooth([P(0.08, 0.0), P(0.3, 0.0), P(0.28, 0.4), P(0.1, 0.4)], 1), body)
    R(f"{name}-haunch", ellipse(*P(-0.24, 0.2), h * 0.22, h * 0.19), body)
    R(f"{name}-mane", smooth([P(0.0, 0.5), P(0.0, 0.85), P(0.2, 1.0), P(0.45, 0.95), P(0.55, 0.7), P(0.45, 0.42), P(0.2, 0.36)], 2), mane)
    R(f"{name}-head", ellipse(*P(0.33, 0.7), h * 0.17, h * 0.16), body)
    R(f"{name}-muzzle", ellipse(*P(0.45, 0.64), h * 0.1, h * 0.08), body)
    it.append(("ink", circle(*P(0.36, 0.76), h * 0.025)))
    it.append(("ink", ellipse(*P(0.53, 0.68), h * 0.025, h * 0.02)))
    return it

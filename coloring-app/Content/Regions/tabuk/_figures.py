"""Extra figures for the Tabuk scenes (people, animals, props).

Every helper returns an item list for Scene.extend():
("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403
from scene_kit import _face  # noqa: E402,F401

HAIR = DARK_BROWN


# ------------------------------------------------------------------ geometry helpers
def limb(pts, w0, w1=None, iters=2):
    """Thick polygon around a polyline; half-width tapers from w0 to w1."""
    w1 = w0 if w1 is None else w1
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = w0 + (w1 - w0) * i / max(1, n - 1)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    poly = left + right[::-1]
    return smooth(poly, iters) if iters else poly


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def wavy_line(x0, x1, y, amp, n):
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append((x0 + (x1 - x0) * t, y + amp * math.sin(t * n * 2 * math.pi)))
    return pts


def zigzag(x0, x1, y, amp, n):
    return [(x0 + (x1 - x0) * i / (2 * n), y + (amp if i % 2 else -amp)) for i in range(2 * n + 1)]


# ------------------------------------------------------------------ people
def kid(x, feet_y, h, outfit="modern", top=RED, bottom=BLUE, accent=YELLOW, headwear="none", hw=RED,
        skin=SKIN, hair=HAIR, arms=(15, 15), facing=0, child=True, backpack=None, shoes=DARK_BROWN,
        sleeves="long", name="kid", hair_style="short", cloak=BROWN):
    """A chunky, friendly cartoon person (bigger head than the kit's person()).

    outfit: modern (shirt `top`, trousers `bottom`) | tshirt (short sleeves) | puffer (padded jacket)
            | jumpsuit (one-piece `top`, belt `accent`) | thobe (`top`) | bisht (thobe + cloak)
            | dress (long dress `top`, embroidered bib + hem `accent`) | thobe_rolled (thobe tucked up to knees)
    headwear: none | cap | beanie (`hw`, pompom `accent`) | shemagh (`hw`) | ghutra | headwrap (`hw`)
              | headscarf (`hw`) | station (shemagh + peaked cap `accent`)
    arms: (left_deg, right_deg) from straight down, outward positive (170 = straight up,
          negative = across the body). Hand centres are left in kid.hands = [left, right].
    """
    it = []
    hr = h * (0.13 if child else 0.105)
    hcy = feet_y - h + hr
    neck_y = hcy + hr * 0.92
    shy = neck_y + h * 0.035
    shw = h * (0.15 if child else 0.165)
    waist = feet_y - h * 0.44
    hem_y = feet_y - h * 0.045
    hem_w = shw * 1.25
    ankle = feet_y - h * 0.04
    f = facing or 0
    robe = outfit in ("thobe", "bisht", "dress", "thobe_rolled")

    # back layer: backpack, head cloth drape, long hair
    if backpack:
        bx = x - (f or -1) * shw * 0.55 if f else x
        if f:
            it.append(("region", f"{name}-backpack", smooth([(bx - shw * 0.75, shy - h * 0.01), (bx + shw * 0.75, shy - h * 0.01),
                                                            (bx + shw * 0.85, waist + h * 0.04), (bx - shw * 0.85, waist + h * 0.04)], 2), backpack))
        else:
            # seen from the front: only the sides peek out
            it.append(("region", f"{name}-backpack", smooth([(x - shw * 1.3, shy + h * 0.02), (x + shw * 1.3, shy + h * 0.02),
                                                            (x + shw * 1.32, waist + h * 0.0), (x - shw * 1.32, waist + h * 0.0)], 2), backpack))
    if headwear in ("shemagh", "ghutra", "station"):
        c = WHITE if headwear == "ghutra" else hw
        it.append(("region", f"{name}-headcloth", smooth([(x - hr * 1.15, hcy - hr * 0.9), (x, hcy - hr * 1.3), (x + hr * 1.15, hcy - hr * 0.9),
                                                         (x + hr * 1.35, hcy + hr * 0.6), (x + hr * 1.55, neck_y + h * 0.075),
                                                         (x - hr * 1.55, neck_y + h * 0.075), (x - hr * 1.35, hcy + hr * 0.6)], 2), c))
    if headwear == "headscarf":
        it.append(("region", f"{name}-scarf", smooth([(x - hr * 1.2, hcy - hr * 0.5), (x - hr * 0.8, hcy - hr * 1.25), (x + hr * 0.8, hcy - hr * 1.25),
                                                     (x + hr * 1.2, hcy - hr * 0.5), (x + hr * 1.3, hcy + hr * 0.7), (x + shw * 1.05, neck_y + h * 0.1),
                                                     (x - shw * 1.05, neck_y + h * 0.1), (x - hr * 1.3, hcy + hr * 0.7)], 2), hw))
    if headwear in ("none", "cap") and hair_style == "pony":
        side = -(f or 1)
        it.append(("region", f"{name}-ponytail", limb([(x + side * hr * 0.7, hcy - hr * 0.5), (x + side * hr * 1.35, hcy + hr * 0.1),
                                                       (x + side * hr * 1.25, hcy + hr * 1.0)], hr * 0.32, hr * 0.12), hair))
    if headwear == "none" and hair_style == "buns":
        for sx in (-1, 1):
            it.append(("region", f"{name}-bun", circle(x + sx * hr * 0.85, hcy - hr * 0.75, hr * 0.38), hair))

    # legs / trousers
    if outfit in ("modern", "tshirt", "puffer", "jumpsuit"):
        hip = shw * 0.92
        gap = h * 0.012
        crotch = waist + h * 0.13
        pc = top if outfit == "jumpsuit" else bottom
        it.append(("region", f"{name}-trousers", [(x - hip, waist - h * 0.02), (x + hip, waist - h * 0.02), (x + hip * 0.98, ankle),
                                                   (x + gap, ankle), (x, crotch), (x - gap, ankle), (x - hip * 0.98, ankle)], pc))
    if outfit == "thobe_rolled":
        for sx in (-1, 1):
            it.append(("region", f"{name}-leg", rect(x + sx * shw * 0.45 - h * 0.05, feet_y - h * 0.3, x + sx * shw * 0.45 + h * 0.05, ankle), skin))
    # shoes
    for sx in (-1, 1):
        fx = x + sx * shw * 0.5 + f * h * 0.02
        sw, sh_ = max(h * 0.07, 48), max(h * 0.06, 40)
        it.append(("region", f"{name}-shoe", smooth([(fx - sw + f * h * 0.01, feet_y), (fx + sw + f * h * 0.035, feet_y),
                                                    (fx + sw * 0.86 + f * h * 0.02, feet_y - sh_), (fx - sw * 0.86, feet_y - sh_)], 2), shoes))

    # body
    if robe:
        hy = feet_y - h * 0.28 if outfit == "thobe_rolled" else hem_y
        hw2 = shw * 1.12 if outfit == "thobe_rolled" else hem_w
        body = smooth([(x - shw * 0.55, neck_y), (x - shw, shy + h * 0.015), (x - shw * 1.02, shy + h * 0.1), (x - hw2, hy), (x + hw2, hy),
                       (x + shw * 1.02, shy + h * 0.1), (x + shw, shy + h * 0.015), (x + shw * 0.55, neck_y)], 2)
        it.append(("region", f"{name}-robe", body, top))
        if outfit == "dress":
            it.append(("region", f"{name}-hem", [(x - hem_w * 0.955, hem_y - h * 0.09), (x + hem_w * 0.955, hem_y - h * 0.09),
                                                 (x + hem_w * 0.995, hem_y - h * 0.004), (x - hem_w * 0.995, hem_y - h * 0.004)], accent))
            it.append(("line", zigzag(x - hem_w * 0.85, x + hem_w * 0.85, hem_y - h * 0.047, h * 0.016, 7), 5))
            it.append(("region", f"{name}-bib", smooth([(x - shw * 0.5, neck_y + h * 0.01), (x + shw * 0.5, neck_y + h * 0.01),
                                                       (x + shw * 0.45, shy + h * 0.17), (x, shy + h * 0.2), (x - shw * 0.45, shy + h * 0.17)], 1), accent))
            it.append(("line", zigzag(x - shw * 0.3, x + shw * 0.3, shy + h * 0.1, h * 0.014, 3), 5))
            it.append(("region", f"{name}-sash", rect(x - shw * 1.03, waist - h * 0.02, x + shw * 1.03, waist + h * 0.025), accent))
        elif outfit in ("thobe", "thobe_rolled", "bisht"):
            it.append(("line", [(x, neck_y + h * 0.02), (x, shy + h * 0.13)], 5))
        if outfit == "thobe_rolled":
            it.append(("region", f"{name}-roll", smooth([(x - hw2 * 1.06, hy - h * 0.06), (x + hw2 * 1.06, hy - h * 0.06),
                                                        (x + hw2 * 1.08, hy + h * 0.01), (x - hw2 * 1.08, hy + h * 0.01)], 1), top))
            it.append(("region", f"{name}-belt", rect(x - shw * 1.06, waist - h * 0.03, x + shw * 1.06, waist + h * 0.02), BROWN))
        if outfit == "bisht":
            for sx in (-1, 1):
                it.append(("region", f"{name}-bisht", [(x + sx * shw * 0.42, neck_y + h * 0.005), (x + sx * shw * 1.08, shy + h * 0.005),
                                                       (x + sx * hem_w * 1.1, hem_y - h * 0.03), (x + sx * hem_w * 0.42, hem_y - h * 0.03)], cloak))
                it.append(("region", f"{name}-bisht-trim", [(x + sx * shw * 0.42, neck_y + h * 0.005), (x + sx * shw * 0.75, neck_y + h * 0.01),
                                                            (x + sx * hem_w * 0.72, hem_y - h * 0.03), (x + sx * hem_w * 0.42, hem_y - h * 0.03)], GOLD))
    else:
        bot = waist + h * 0.04
        if outfit == "jumpsuit":
            bot = waist + h * 0.02
        body = smooth([(x - shw * 0.55, neck_y), (x - shw, shy + h * 0.015), (x - shw * 1.03, shy + h * 0.1), (x - shw * 1.0, bot),
                       (x + shw * 1.0, bot), (x + shw * 1.03, shy + h * 0.1), (x + shw, shy + h * 0.015), (x + shw * 0.55, neck_y)], 2)
        it.append(("region", f"{name}-top", body, top))
        if outfit == "puffer":
            for k in (1, 2, 3):
                yy = shy + (bot - shy) * k / 4
                it.append(("line", smooth_open([(x - shw * 0.95, yy), (x, yy + h * 0.012), (x + shw * 0.95, yy)], 2), 5))
            it.append(("line", [(x, neck_y + h * 0.02), (x, bot - 4)], 5))
            it.append(("region", f"{name}-collar", smooth([(x - shw * 0.62, neck_y - h * 0.01), (x + shw * 0.62, neck_y - h * 0.01),
                                                          (x + shw * 0.58, neck_y + h * 0.05), (x - shw * 0.58, neck_y + h * 0.05)], 1), top))
        if outfit == "jumpsuit":
            it.append(("region", f"{name}-belt", rect(x - shw * 1.0, waist - h * 0.015, x + shw * 1.0, waist + h * 0.03), accent))
            it.append(("region", f"{name}-badge", star(x + shw * 0.5, shy + h * 0.1, h * 0.075, h * 0.038), accent))
            it.append(("line", [(x - shw * 0.2, neck_y + h * 0.02), (x - shw * 0.2, waist - h * 0.02)], 5))
        if outfit == "tshirt":
            it.append(("region", f"{name}-print", circle(x, shy + h * 0.1, max(h * 0.05, 30)), accent))

    if backpack and not f:
        for sx in (-1, 1):
            it.append(("region", f"{name}-strap", [(x + sx * shw * 0.45, neck_y + h * 0.01), (x + sx * shw * 0.8, neck_y + h * 0.02),
                                                   (x + sx * shw * 0.75, waist - h * 0.02), (x + sx * shw * 0.45, waist - h * 0.02)], backpack))
    # arms
    hands = []
    L = h * 0.33
    sleeve_c = cloak if outfit == "bisht" else top
    for side, ang in ((-1, arms[0]), (1, arms[1])):
        sx, sy = x + side * shw * 0.82, shy + h * 0.035
        a = math.radians(ang)
        hx, hy = sx + side * L * math.sin(a), sy + L * math.cos(a)
        # elbow bends slightly outward / down
        mx, my = (sx + hx) / 2, (sy + hy) / 2
        px, py = -(hy - sy) / L, (hx - sx) / L
        bend = h * 0.03 * side * (-1 if ang > 90 else 1)
        ex, ey = mx + px * bend * (1 if side > 0 else -1), my + py * bend * (1 if side > 0 else -1)
        pts = [(sx, sy), (ex, ey), (hx, hy)]
        wr = lerp((ex, ey), (hx, hy), 0.92)
        if sleeves == "short" or outfit == "tshirt":
            it.append(("region", f"{name}-arm", limb([(sx, sy), (ex, ey), wr], h * 0.036, h * 0.032), skin))
            it.append(("region", f"{name}-sleeve", limb([(sx, sy), lerp((sx, sy), (ex, ey), 0.75)], h * 0.05, h * 0.048, 1), sleeve_c))
        else:
            w0 = h * (0.058 if outfit == "puffer" else 0.047)
            it.append(("region", f"{name}-sleeve", limb([(sx, sy), (ex, ey), wr], w0, w0 * 0.9), sleeve_c))
        it.append(("region", f"{name}-hand", circle(hx, hy, max(h * 0.042, 28)), skin))
        hands.append((hx, hy))
    kid.hands = hands

    # head
    it.append(("region", f"{name}-face", circle(x, hcy, hr), skin))
    # ears not drawn (they'd be tiny)
    off = hr * 0.18 * f
    for sx in (-1, 1):
        it.append(("ink", ellipse(x + off + sx * hr * 0.36, hcy - hr * 0.02, hr * 0.1, hr * 0.14)))
    it.append(("line", arc(x + off, hcy + hr * 0.25, hr * 0.33, hr * 0.24, 20, 160, 12), max(5, int(hr * 0.06))))

    if headwear in ("none", "cap", "beanie"):
        # hair cap with a fringe
        fy = 0.42 if headwear == "none" else 0.05
        if headwear == "none":
            it.append(("region", f"{name}-hair", smooth([(x - hr * 1.05, hcy - hr * 0.05), (x - hr * 1.0, hcy - hr * 0.75), (x, hcy - hr * 1.15),
                                                         (x + hr * 1.0, hcy - hr * 0.75), (x + hr * 1.05, hcy - hr * 0.05),
                                                         (x + hr * 0.7, hcy - hr * fy), (x + hr * 0.2, hcy - hr * (fy + 0.08)), (x - hr * 0.3, hcy - hr * (fy - 0.04)),
                                                         (x - hr * 0.75, hcy - hr * (fy + 0.03))], 2), hair))
    if headwear == "cap":
        it.append(("region", f"{name}-cap", arc(x, hcy - hr * 0.5, hr * 1.04, hr * 0.72, 180, 360), hw))
        d = f or 1
        if f:
            it.append(("region", f"{name}-cap-brim", smooth([(x + d * hr * 0.2, hcy - hr * 0.7), (x + d * hr * 1.0, hcy - hr * 0.7), (x + d * hr * 1.8, hcy - hr * 0.5),
                                                             (x + d * hr * 1.65, hcy - hr * 0.28), (x + d * hr * 0.2, hcy - hr * 0.3)], 1), hw))
        else:
            it.append(("region", f"{name}-cap-brim", smooth([(x - hr * 1.2, hcy - hr * 0.68), (x + hr * 1.2, hcy - hr * 0.68),
                                                             (x + hr * 1.0, hcy - hr * 0.4), (x, hcy - hr * 0.27), (x - hr * 1.0, hcy - hr * 0.4)], 1), hw))
    elif headwear == "beanie":
        it.append(("region", f"{name}-pompom", circle(x, hcy - hr * 1.25, hr * 0.36), accent))
        it.append(("region", f"{name}-beanie", arc(x, hcy - hr * 0.35, hr * 1.04, hr * 0.85, 180, 360), hw))
        it.append(("region", f"{name}-beanie-band", smooth([(x - hr * 1.12, hcy - hr * 0.62), (x + hr * 1.12, hcy - hr * 0.62),
                                                           (x + hr * 1.12, hcy - hr * 0.22), (x - hr * 1.12, hcy - hr * 0.22)], 1), accent))
    elif headwear in ("shemagh", "ghutra", "station"):
        c = WHITE if headwear == "ghutra" else hw
        if headwear != "station":
            it.append(("region", f"{name}-headcloth-top", smooth([(x - hr * 1.15, hcy + hr * 0.1), (x - hr * 1.1, hcy - hr * 0.85), (x, hcy - hr * 1.3),
                                                                 (x + hr * 1.1, hcy - hr * 0.85), (x + hr * 1.15, hcy + hr * 0.1),
                                                                 (x + hr * 0.9, hcy - hr * 0.35), (x, hcy - hr * 0.55), (x - hr * 0.9, hcy - hr * 0.35)], 2), c))
        if headwear == "station":
            # peaked cap sitting on the head cloth
            it.append(("region", f"{name}-cap-crown", smooth([(x - hr * 1.05, hcy - hr * 0.5), (x - hr * 1.2, hcy - hr * 1.3), (x, hcy - hr * 1.45),
                                                              (x + hr * 1.2, hcy - hr * 1.3), (x + hr * 1.05, hcy - hr * 0.5)], 1), accent))
            it.append(("region", f"{name}-cap-band", smooth([(x - hr * 1.08, hcy - hr * 0.82), (x + hr * 1.08, hcy - hr * 0.82),
                                                             (x + hr * 1.06, hcy - hr * 0.5), (x - hr * 1.06, hcy - hr * 0.5)], 1), BLACK_CLOTH))
            it.append(("region", f"{name}-cap-peak", smooth([(x - hr * 1.0, hcy - hr * 0.55), (x + hr * 1.0, hcy - hr * 0.55),
                                                             (x + hr * 0.7, hcy - hr * 0.22), (x - hr * 0.7, hcy - hr * 0.22)], 1), BLACK_CLOTH))
        else:
            it.append(("region", f"{name}-agal", limb(arc(x, hcy - hr * 0.42, hr * 0.98, hr * 0.62, 195, 345, 16), hr * 0.13, hr * 0.13, 1), BLACK_CLOTH))
    elif headwear == "headwrap":
        it.append(("region", f"{name}-wrap-tail", limb([(x - hr * 0.7, hcy - hr * 0.6), (x - hr * 1.35, hcy - hr * 0.1), (x - hr * 1.3, hcy + hr * 0.5)],
                                                       hr * 0.22, hr * 0.14), hw))
        it.append(("region", f"{name}-headwrap", smooth([(x - hr * 1.08, hcy - hr * 0.3), (x - hr * 1.0, hcy - hr * 1.05), (x - hr * 0.3, hcy - hr * 1.3),
                                                         (x + hr * 0.6, hcy - hr * 1.25), (x + hr * 1.08, hcy - hr * 0.95), (x + hr * 1.08, hcy - hr * 0.3),
                                                         (x, hcy - hr * 0.48)], 2), hw))
        it.append(("line", smooth_open([(x - hr * 0.95, hcy - hr * 0.75), (x, hcy - hr * 0.95), (x + hr * 0.95, hcy - hr * 0.62)], 2), 5))
    elif headwear == "headscarf":
        it.append(("region", f"{name}-scarf-front", smooth([(x - hr * 1.1, hcy - hr * 0.05), (x - hr * 1.0, hcy - hr * 0.8), (x, hcy - hr * 1.18),
                                                           (x + hr * 1.0, hcy - hr * 0.8), (x + hr * 1.1, hcy - hr * 0.05),
                                                           (x + hr * 0.85, hcy - hr * 0.45), (x, hcy - hr * 0.62), (x - hr * 0.85, hcy - hr * 0.45)], 2), hw))
    return it


# ------------------------------------------------------------------ animals
def goat(x, feet_y, h, facing=1, body=WHITE, patch=BROWN, name="goat"):
    """Standing goat; h = height to the back."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    it = []
    it.append(("region", f"{name}-tail", limb([P(-0.52, 0.9), P(-0.64, 1.06), P(-0.62, 1.14)], h * 0.07, h * 0.05), body))
    for lx in (-0.42, -0.26, 0.28, 0.44):
        it.append(("region", f"{name}-leg", limb([P(lx, 0.62), P(lx, 0.1)], h * 0.09, h * 0.075, 1), body))
        it.append(("region", f"{name}-hoof", smooth([P(lx - 0.1, 0.0), P(lx + 0.1, 0.0), P(lx + 0.085, 0.14), P(lx - 0.085, 0.14)], 1), DARK_BROWN))
    it.append(("region", f"{name}-body", smooth([P(-0.6, 0.62), P(-0.58, 0.95), P(0.0, 1.02), P(0.45, 0.98), P(0.62, 0.8), P(0.5, 0.52), P(-0.45, 0.5)], 3), body))
    it.append(("region", f"{name}-patch", smooth([P(-0.3, 0.98), P(0.05, 1.0), P(0.12, 0.8), P(-0.1, 0.66), P(-0.35, 0.75)], 2), patch))
    it.append(("region", f"{name}-neck", limb([P(0.4, 0.8), P(0.6, 1.12)], h * 0.15, h * 0.12), body))
    it.append(("region", f"{name}-horn", limb([P(0.6, 1.36), P(0.52, 1.58), P(0.36, 1.66)], h * 0.065, h * 0.03), DUNE))
    it.append(("region", f"{name}-ear", limb([P(0.56, 1.3), P(0.34, 1.2)], h * 0.085, h * 0.05), patch))
    it.append(("region", f"{name}-head", smooth([P(0.52, 1.44), P(0.76, 1.44), P(0.98, 1.12), P(0.9, 1.0), P(0.72, 1.04), P(0.5, 1.18)], 2), body))
    it.append(("region", f"{name}-beard", smooth([P(0.74, 1.08), P(0.94, 1.04), P(0.86, 0.76)], 1), patch))
    it.append(("ink", ellipse(*P(0.73, 1.27), h * 0.035, h * 0.045)))
    it.append(("line", arc(*P(0.85, 1.12), h * 0.06, h * 0.035, 20, 160, 8), 5))
    return it


def lamb(x, feet_y, h, facing=1, wool=WHITE, face=CREAM, legs=DARK_BROWN, name="lamb"):
    """Fluffy lamb; h = height to the top of the wool."""
    f = facing
    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    it = []
    for lx in (-0.36, -0.2, 0.2, 0.36):
        it.append(("region", f"{name}-leg", limb([P(lx, 0.5), P(lx, 0.03)], h * 0.075, h * 0.07, 1), legs))
    ctrl = []
    n = 16
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1.0 + (0.1 if i % 2 else 0)
        ctrl.append(P(0.52 * r * math.cos(t), 0.68 + 0.3 * r * math.sin(t)))
    it.append(("region", f"{name}-wool", smooth(ctrl, 2), wool))
    it.append(("region", f"{name}-ear", ellipse(*P(0.4, 0.98), h * 0.2, h * 0.1, rot=25 * f), face))
    it.append(("region", f"{name}-head", ellipse(*P(0.6, 0.9), h * 0.21, h * 0.25, rot=-20 * f), face))
    it.append(("region", f"{name}-tuft", smooth([P(0.42, 1.08), P(0.58, 1.22), P(0.78, 1.12), P(0.62, 1.04)], 2), wool))
    it.append(("ink", ellipse(*P(0.67, 0.94), h * 0.032, h * 0.04)))
    it.append(("line", arc(*P(0.7, 0.78), h * 0.06, h * 0.035, 20, 160, 8), 5))
    return it


def dolphin(x, y, L, angle=0, body=GREY, belly=CREAM, name="dolphin", flip=1):
    """Friendly leaping dolphin, nose pointing right (flip=-1: left). L = body length. angle rotates (deg, +ve clockwise)."""
    def P(px, py):
        return (x + flip * px * L, y + py * L)
    rot = lambda pts: rotate(pts, angle * flip, x, y)
    it = []
    outline = smooth([P(-0.46, -0.01), P(-0.3, -0.1), P(0.0, -0.17), P(0.24, -0.18), P(0.36, -0.15), P(0.43, -0.08),
                      P(0.5, -0.04), P(0.6, -0.02), P(0.6, 0.03), P(0.5, 0.05), P(0.4, 0.08), P(0.2, 0.14), P(-0.1, 0.11), P(-0.4, 0.04)], 3)
    tail = smooth([P(-0.38, -0.02), P(-0.56, -0.15), P(-0.68, -0.15), P(-0.58, 0.0), P(-0.68, 0.14), P(-0.56, 0.15), P(-0.38, 0.03)], 2)
    fin = smooth([P(-0.14, -0.13), P(-0.08, -0.24), P(-0.02, -0.33), P(0.03, -0.3), P(0.06, -0.2), P(0.12, -0.15)], 2)
    flipper = smooth([P(0.06, 0.08), P(0.22, 0.1), P(0.08, 0.27), P(0.02, 0.2)], 2)
    bel = smooth([P(-0.25, 0.06), P(0.05, 0.05), P(0.3, 0.04), P(0.48, 0.02), P(0.56, 0.02), P(0.5, 0.06), P(0.38, 0.09), P(0.18, 0.13), P(-0.1, 0.105)], 2)
    it.append(("region", f"{name}-tail", rot(tail), body))
    it.append(("region", f"{name}-fin", rot(fin), body))
    it.append(("region", f"{name}-body", rot(outline), body))
    it.append(("region", f"{name}-belly", rot(bel), belly))
    it.append(("region", f"{name}-flipper", rot(flipper), body))
    it.append(("ink", rot(ellipse(*P(0.33, -0.07), L * 0.026, L * 0.032))))
    it.append(("line", rot(smooth_open([P(0.44, -0.0), P(0.5, 0.02), P(0.58, 0.0)], 2)), 6))
    return it


def turtle(x, y, s, angle=0, shell=GREEN, skin=GRASS, name="turtle"):
    """Swimming sea turtle seen from above, head pointing right before rotation; s = shell length."""
    def P(px, py):
        return (x + px * s, y + py * s)
    rot = lambda pts: rotate(pts, angle, x, y)
    it = []
    for (fx, fy, r) in ((0.25, -0.45, -30), (0.25, 0.45, 30)):
        it.append(("region", f"{name}-flipper", rot(ellipse(*P(fx, fy), s * 0.32, s * 0.12, rot=r)), skin))
    for (fx, fy) in ((-0.42, -0.28), (-0.42, 0.28)):
        it.append(("region", f"{name}-foot", rot(ellipse(*P(fx, fy), s * 0.18, s * 0.11)), skin))
    it.append(("region", f"{name}-head", rot(ellipse(*P(0.6, 0), s * 0.17, s * 0.13)), skin))
    it.append(("ink", rot(circle(*P(0.66, -0.07), s * 0.025))))
    it.append(("ink", rot(circle(*P(0.66, 0.07), s * 0.025))))
    it.append(("region", f"{name}-shell", rot(ellipse(x, y, s * 0.5, s * 0.4)), shell))
    it.append(("region", f"{name}-scute", rot(ellipse(x, y, s * 0.2, s * 0.16)), GRASS if shell != GRASS else LEAF))
    for a in range(0, 360, 60):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        it.append(("line", rot([P(0.2 * ca, 0.16 * sa), P(0.47 * ca, 0.37 * sa)]), 5))
    return it


def dugong(x, y, L, body=GREY, name="dugong", flip=1):
    """Plump dugong swimming right (flip=-1 left); L = length."""
    def P(px, py):
        return (x + flip * px * L, y + py * L)
    it = []
    it.append(("region", f"{name}-tail", smooth([P(-0.3, -0.06), P(-0.55, -0.08), P(-0.68, -0.18), P(-0.64, 0.0), P(-0.68, 0.18), P(-0.55, 0.08), P(-0.3, 0.06)], 2), body))
    it.append(("region", f"{name}-body", smooth([P(-0.48, 0.0), P(-0.2, -0.14), P(0.2, -0.16), P(0.42, -0.1), P(0.5, 0.0),
                                               P(0.44, 0.1), P(0.2, 0.15), P(-0.2, 0.12)], 3), body))
    it.append(("region", f"{name}-flipper", smooth([P(0.12, 0.08), P(0.28, 0.12), P(0.1, 0.25)], 2), body))
    it.append(("region", f"{name}-snout", ellipse(*P(0.47, 0.04), L * 0.07, L * 0.08), CREAM))
    it.append(("ink", circle(*P(0.36, -0.06), L * 0.016)))
    it.append(("line", arc(*P(0.46, 0.06), L * 0.03, L * 0.02, 20, 160, 6), 5))
    return it


def fish(x, y, L, colour=ORANGE, stripe=WHITE, flip=1, name="fish"):
    def P(px, py):
        return (x + flip * px * L, y + py * L)
    it = [("region", f"{name}-tail", [P(-0.3, 0), P(-0.66, -0.32), P(-0.62, 0.0), P(-0.66, 0.32)], colour),
          ("region", f"{name}", ellipse(x, y, L * 0.42, L * 0.26), colour),
          ("region", f"{name}-stripe", smooth([P(-0.06, -0.25), P(0.14, -0.24), P(0.12, 0.24), P(-0.08, 0.25)], 1), stripe),
          ("ink", circle(*P(0.24, -0.06), L * 0.04))]
    return it


def kneeling_camel(x, ground_y, h, facing=1, body=DUNE, blanket=RED, band=YELLOW, name="camel"):
    """Camel resting on the ground with its legs folded; h = height of the hump."""
    f = facing
    def P(px, py):
        return (x + f * px * h, ground_y - py * h)
    it = []
    it.append(("region", f"{name}-tail", limb([P(-0.62, 0.55), P(-0.82, 0.4), P(-0.84, 0.18)], h * 0.06, h * 0.05), body))
    it.append(("region", f"{name}-body", smooth([P(-0.7, 0.06), P(-0.74, 0.35), P(-0.58, 0.62), P(-0.32, 0.88), P(-0.1, 0.97),
                                                P(0.12, 0.86), P(0.3, 0.64), P(0.46, 0.48), P(0.56, 0.22), P(0.46, 0.04), P(0.0, 0.02)], 3), body))
    it.append(("region", f"{name}-neck", limb([P(0.4, 0.36), P(0.62, 0.46), P(0.76, 0.7), P(0.82, 0.96)], h * 0.13, h * 0.085), body))
    it.append(("region", f"{name}-ear", ellipse(*P(0.79, 1.13), h * 0.055, h * 0.09, rot=-25 * f), body))
    it.append(("region", f"{name}-head", smooth([P(0.72, 1.02), P(0.8, 1.12), P(0.98, 1.12), P(1.14, 1.02), P(1.16, 0.93), P(1.0, 0.89), P(0.78, 0.9)], 2), body))
    it.append(("ink", ellipse(*P(0.92, 1.04), h * 0.022, h * 0.028)))
    it.append(("line", arc(*P(1.06, 0.96), h * 0.05, h * 0.03, 20, 160, 8), 6))
    it.append(("region", f"{name}-hind-leg", ellipse(*P(-0.42, 0.11), h * 0.3, h * 0.11), body))
    it.append(("region", f"{name}-front-leg", ellipse(*P(0.34, 0.08), h * 0.26, h * 0.085), body))
    if blanket:
        it.append(("region", f"{name}-blanket", smooth([P(-0.4, 0.84), P(-0.1, 0.99), P(0.16, 0.86), P(0.2, 0.52), P(-0.46, 0.5)], 1), blanket))
        it.append(("region", f"{name}-band", [P(-0.47, 0.6), P(0.21, 0.6), P(0.2, 0.47), P(-0.47, 0.47)], band))
    return it


# ------------------------------------------------------------------ props
def boat(x, waterline, L, hull=RED, cabin=WHITE, stripe=YELLOW, name="boat"):
    """Small motor boat facing right; L = length. cabin=None for an open boat."""
    it = []
    if cabin:
      it.append(("region", f"{name}-cabin", rect(x - L * 0.22, waterline - L * 0.38, x + L * 0.12, waterline - L * 0.12), cabin))
      it.append(("region", f"{name}-roof", [(x - L * 0.27, waterline - L * 0.38), (x + L * 0.17, waterline - L * 0.38),
                                          (x + L * 0.12, waterline - L * 0.45), (x - L * 0.22, waterline - L * 0.45)], stripe))
      it.append(("region", f"{name}-window", rect(x - L * 0.17, waterline - L * 0.32, x - L * 0.06, waterline - L * 0.2), SKY))
      it.append(("region", f"{name}-window", rect(x - L * 0.02, waterline - L * 0.32, x + L * 0.08, waterline - L * 0.2), SKY))
    it.append(("region", f"{name}-hull", smooth([(x - L * 0.5, waterline - L * 0.16), (x + L * 0.55, waterline - L * 0.2),
                                                (x + L * 0.35, waterline + L * 0.06), (x - L * 0.42, waterline + L * 0.06)], 1), hull))
    it.append(("region", f"{name}-stripe", [(x - L * 0.49, waterline - L * 0.1), (x + L * 0.49, waterline - L * 0.12),
                                            (x + L * 0.44, waterline - L * 0.06), (x - L * 0.47, waterline - L * 0.04)], stripe))
    return it


def dallah(x, base_y, h, colour=GOLD, name="dallah"):
    """Arabic coffee pot (beak spout to the right); h = height."""
    it = []
    it.append(("region", f"{name}-spout", smooth([(x + h * 0.1, base_y - h * 0.3), (x + h * 0.3, base_y - h * 0.55), (x + h * 0.5, base_y - h * 0.86),
                                                 (x + h * 0.6, base_y - h * 0.86), (x + h * 0.42, base_y - h * 0.5), (x + h * 0.2, base_y - h * 0.22)], 1), colour))
    it.append(("region", f"{name}-handle", limb([(x - h * 0.15, base_y - h * 0.7), (x - h * 0.42, base_y - h * 0.58), (x - h * 0.28, base_y - h * 0.22)],
                                                h * 0.07, h * 0.07), colour))
    it.append(("region", f"{name}-body", smooth([(x - h * 0.32, base_y), (x + h * 0.32, base_y), (x + h * 0.28, base_y - h * 0.35),
                                                (x + h * 0.13, base_y - h * 0.55), (x + h * 0.16, base_y - h * 0.75), (x - h * 0.16, base_y - h * 0.75),
                                                (x - h * 0.13, base_y - h * 0.55), (x - h * 0.28, base_y - h * 0.35)], 2), colour))
    it.append(("region", f"{name}-lid", smooth([(x - h * 0.2, base_y - h * 0.73), (x + h * 0.2, base_y - h * 0.73), (x, base_y - h * 1.02)], 1), colour))
    return it


def snowman(x, base_y, h, name="snowman", scarf=RED, hat=BLACK_CLOTH):
    it = []
    r1, r2, r3 = h * 0.24, h * 0.18, h * 0.13
    y1 = base_y - r1
    y2 = y1 - r1 - r2 * 0.7
    y3 = y2 - r2 - r3 * 0.7
    # stick arms
    for sx in (-1, 1):
        it.append(("region", f"{name}-arm", limb([(x + sx * r2 * 0.8, y2), (x + sx * r2 * 1.9, y2 - r2 * 0.6), (x + sx * r2 * 2.4, y2 - r2 * 1.2)],
                                                 h * 0.018, h * 0.012, 1), TRUNK))
    it.append(("region", f"{name}-base", circle(x, y1, r1), WHITE))
    it.append(("region", f"{name}-middle", circle(x, y2, r2), WHITE))
    for k in (-0.35, 0.15):
        it.append(("ink", circle(x, y2 + r2 * k + r2 * 0.25, h * 0.018)))
    it.append(("region", f"{name}-head", circle(x, y3, r3), WHITE))
    it.append(("region", f"{name}-scarf", smooth([(x - r3 * 1.05, y3 + r3 * 0.6), (x + r3 * 1.05, y3 + r3 * 0.6),
                                                 (x + r3 * 1.0, y3 + r3 * 1.05), (x - r3 * 1.0, y3 + r3 * 1.05)], 1), scarf))
    it.append(("region", f"{name}-scarf-end", [(x + r3 * 0.35, y3 + r3 * 0.9), (x + r3 * 0.85, y3 + r3 * 0.9),
                                               (x + r3 * 0.95, y3 + r3 * 2.0), (x + r3 * 0.45, y3 + r3 * 2.0)], scarf))
    it.append(("region", f"{name}-hat-brim", rect(x - r3 * 1.05, y3 - r3 * 0.85, x + r3 * 1.05, y3 - r3 * 0.6), hat))
    it.append(("region", f"{name}-hat", rect(x - r3 * 0.68, y3 - r3 * 1.75, x + r3 * 0.68, y3 - r3 * 0.85), hat))
    it.append(("region", f"{name}-hatband", rect(x - r3 * 0.68, y3 - r3 * 1.12, x + r3 * 0.68, y3 - r3 * 0.85), scarf))
    it.append(("region", f"{name}-nose", [(x - r3 * 0.05, y3 - r3 * 0.24), (x + r3 * 1.15, y3 + r3 * 0.05), (x - r3 * 0.05, y3 + r3 * 0.3)], ORANGE))
    for sx in (-1, 1):
        it.append(("ink", circle(x + sx * r3 * 0.38, y3 - r3 * 0.35, r3 * 0.11)))
    it.append(("line", arc(x, y3 + r3 * 0.2, r3 * 0.5, r3 * 0.35, 30, 150, 10), 6))
    return it


def robot(x, feet_y, h, body=GREY, accent=BLUE, screen=SKY, name="robot", wave=True):
    """Friendly round robot; h = total height incl. antenna."""
    it = []
    hx = x
    # legs
    for sx in (-1, 1):
        it.append(("region", f"{name}-leg", rect(x + sx * h * 0.1 - h * 0.045, feet_y - h * 0.22, x + sx * h * 0.1 + h * 0.045, feet_y - h * 0.05), body))
        it.append(("region", f"{name}-foot", smooth([(x + sx * h * 0.1 - h * 0.09, feet_y), (x + sx * h * 0.1 + h * 0.09, feet_y),
                                                    (x + sx * h * 0.1 + h * 0.08, feet_y - h * 0.07), (x + sx * h * 0.1 - h * 0.08, feet_y - h * 0.07)], 1), accent))
    # arms
    for sx in (-1, 1):
        up = wave and sx == -1
        sxp, syp = x + sx * h * 0.2, feet_y - h * 0.5
        ex, ey = (sxp + sx * h * 0.17, syp - h * 0.2) if up else (sxp + sx * h * 0.12, syp + h * 0.16)
        it.append(("region", f"{name}-arm", limb([(sxp, syp), (ex, ey)], h * 0.035, h * 0.035, 1), body))
        it.append(("region", f"{name}-hand", circle(ex, ey - (h * 0.03 if up else -h * 0.03), h * 0.055), accent))
    it.append(("region", f"{name}-body", smooth([(x - h * 0.22, feet_y - h * 0.62), (x + h * 0.22, feet_y - h * 0.62),
                                                (x + h * 0.23, feet_y - h * 0.22), (x - h * 0.23, feet_y - h * 0.22)], 3), body))
    it.append(("region", f"{name}-heart", smooth([(x, feet_y - h * 0.32), (x - h * 0.1, feet_y - h * 0.42), (x - h * 0.065, feet_y - h * 0.5),
                                                 (x, feet_y - h * 0.46), (x + h * 0.065, feet_y - h * 0.5), (x + h * 0.1, feet_y - h * 0.42)], 1), RED))
    # head
    it.append(("region", f"{name}-antenna", rect(hx - h * 0.03, feet_y - h * 1.0, hx + h * 0.03, feet_y - h * 0.87), body))
    it.append(("region", f"{name}-bulb", circle(hx, feet_y - h * 1.03, h * 0.05), YELLOW))
    for sx in (-1, 1):
        it.append(("region", f"{name}-ear", ellipse(hx + sx * h * 0.24, feet_y - h * 0.76, h * 0.04, h * 0.065), accent))
    it.append(("region", f"{name}-head", smooth([(hx - h * 0.23, feet_y - h * 0.89), (hx + h * 0.23, feet_y - h * 0.89),
                                                (hx + h * 0.24, feet_y - h * 0.64), (hx - h * 0.24, feet_y - h * 0.64)], 3), body))
    it.append(("region", f"{name}-screen", smooth([(hx - h * 0.17, feet_y - h * 0.85), (hx + h * 0.17, feet_y - h * 0.85),
                                                  (hx + h * 0.18, feet_y - h * 0.68), (hx - h * 0.18, feet_y - h * 0.68)], 2), screen))
    for sx in (-1, 1):
        it.append(("ink", ellipse(hx + sx * h * 0.07, feet_y - h * 0.785, h * 0.022, h * 0.03)))
    it.append(("line", arc(hx, feet_y - h * 0.745, h * 0.06, h * 0.03, 20, 160, 10), 6))
    return it


def flying_taxi(x, y, L, body=YELLOW, glass=SKY, rotor=GREY, name="taxi", flip=1):
    """Bubble-shaped air taxi with rotor arms; L = width."""
    def P(px, py):
        return (x + flip * px * L, y + py * L)
    it = []
    for sx in (-0.42, 0.42):
        it.append(("region", f"{name}-arm", rect(*P(min(sx, sx * 0.5), -0.24), *P(max(sx, sx * 0.5), -0.19)) if flip == 1 else
                   rect(*P(max(sx, sx * 0.5), -0.24), *P(min(sx, sx * 0.5), -0.19)), rotor))
        it.append(("region", f"{name}-rotor", ellipse(*P(sx, -0.28), L * 0.2, max(L * 0.055, 21)), rotor))
    it.append(("region", f"{name}-body", smooth([P(-0.4, 0.05), P(-0.35, -0.2), P(0.0, -0.3), P(0.38, -0.18), P(0.45, 0.05), P(0.3, 0.18), P(-0.3, 0.18)], 3), body))
    it.append(("region", f"{name}-glass", smooth([P(-0.05, -0.24), P(0.25, -0.19), P(0.36, 0.0), P(-0.05, 0.0)], 2), glass))
    it.append(("region", f"{name}-skid", rect(*P(-0.3, 0.2), *P(0.3, 0.25)) if flip == 1 else rect(*P(0.3, 0.2), *P(-0.3, 0.25)), rotor))
    return it


def tulip(x, base_y, h, colour=RED, leaf=LEAF, name="tulip"):
    it = [("region", f"{name}-stem", limb([(x, base_y), (x, base_y - h * 0.75)], max(h * 0.05, 19), max(h * 0.045, 17), 1), leaf),
          ("region", f"{name}-leaf", smooth([(x + 4, base_y - h * 0.02), (x - h * 0.34, base_y - h * 0.5), (x - h * 0.08, base_y - h * 0.38), (x + 4, base_y - h * 0.3)], 2), leaf),
          ("region", f"{name}-head", smooth([(x - h * 0.2, base_y - h * 0.97), (x - h * 0.07, base_y - h * 0.83), (x, base_y - h * 1.0),
                                            (x + h * 0.07, base_y - h * 0.83), (x + h * 0.2, base_y - h * 0.97), (x + h * 0.18, base_y - h * 0.72),
                                            (x, base_y - h * 0.6), (x - h * 0.18, base_y - h * 0.72)], 1), colour)]
    return it


def daisy(x, y, r, petal=WHITE, centre=YELLOW, name="daisy", stem_to=None, leaf=LEAF):
    it = []
    if stem_to:
        it.append(("region", f"{name}-stem", limb([(x, stem_to), (x, y)], max(r * 0.2, 13), max(r * 0.2, 13), 1), leaf))
    it.append(("region", f"{name}-petals", smooth(star(x, y, r, r * 0.7, 8, -90), 1), petal))
    it.append(("region", f"{name}-centre", circle(x, y, r * 0.45), centre))
    return it


def band(top_points, bottom_y, iters=2):
    """Ground/hill band: a smoothed top edge down to a straight bottom edge (no rounded corners)."""
    top = smooth_open(top_points, iters)
    return top + [(top[-1][0], bottom_y), (top[0][0], bottom_y)]

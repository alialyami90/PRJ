"""Extra figure helpers for the Riyadh (Najd) scenes.

Every helper returns an item list for Scene.extend():
("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403

SHEMAGH_RED = RED
SADU_RED = "#C62828"


# ---------------------------------------------------------------- geometry
def limb(pts, w0, w1=None, caps=True):
    """Thick tapered polyline -> closed polygon (rounded ends)."""
    w1 = w0 if w1 is None else w1
    n = len(pts)
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - px, pts[1][1] - py
        elif i == n - 1:
            dx, dy = px - pts[i - 1][0], py - pts[i - 1][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w, py - ny * w))
    out = left
    if caps:
        (ex, ey), (bx, by) = pts[-1], pts[-2]
        a = math.atan2(ey - by, ex - bx)
        out = out + [(ex + math.cos(a + t) * w1 / 2, ey + math.sin(a + t) * w1 / 2)
                     for t in [math.pi / 2 - k * math.pi / 6 for k in range(1, 6)]]
    out = out + right[::-1]
    if caps:
        (sx, sy), (cx, cy) = pts[0], pts[1]
        a = math.atan2(sy - cy, sx - cx)
        out = out + [(sx + math.cos(a + t) * w0 / 2, sy + math.sin(a + t) * w0 / 2)
                     for t in [math.pi / 2 - k * math.pi / 6 for k in range(1, 6)]]
    return out


def bezier(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def R(name, pts, colour):
    return ("region", name, pts, colour)


def L(pts, w=6):
    return ("line", pts, w)


def I(pts):
    return ("ink", pts)


# ---------------------------------------------------------------- people
def face(cx, cy, r, look=0.0, smile=True, old=False):
    it = []
    ex = r * 0.36
    off = r * 0.15 * look
    for sx in (-1, 1):
        ecx, ecy = cx + off + sx * ex, cy - r * 0.02
        it.append(I(ellipse(ecx, ecy, r * 0.105, r * 0.15)))
        it.append(L(arc(ecx, ecy - r * 0.2, r * 0.16, r * 0.08, 200, 340, 8), max(4, int(r * 0.05))))
    # nose
    it.append(L(arc(cx + off * 1.4, cy + r * 0.2, r * 0.08, r * 0.06, 0, 160, 6), max(4, int(r * 0.045))))
    if smile:
        it.append(L(arc(cx + off, cy + r * 0.38, r * 0.3, r * 0.2, 20, 160, 12), max(5, int(r * 0.06))))
    if old:
        for sx in (-1, 1):
            it.append(L([(cx + off + sx * r * 0.62, cy + r * 0.0), (cx + off + sx * r * 0.72, cy - r * 0.08)], 4))
    return it


def human(x, feet_y, h, outfit="thobe", head="shemagh", skin=SKIN, robe=WHITE, accent=RED,
          cloak=BROWN, trim=GOLD, top=BLUE, pants=BLUE, shoes=DARK_BROWN, hands=None, look=0.0,
          child=False, beard=None, name="p", front_arms=(True, True), hem=None, seated_y=None,
          leg_side=1, hood=False, skirt=None, hair=DARK_BROWN, sleeve=None, mitt=None, emb=None, mitt_side=0):
    """Front-view chunky person. (x, feet_y) between the feet, h = standing height.

    outfit: thobe | bisht | dress | abaya | modern | hoodie
    head:   shemagh | ghutra | ghutra_plain | hijab | cap | hair | taqiyah | girl_scarf
    hands:  (left_xy, right_xy) absolute hand positions (left = viewer's left). None = down.
    seated_y: if set, the figure sits with its seat at that y (legs dangle on leg_side).
    """
    it = []
    hr = h * (0.125 if child else 0.09)
    top_y = feet_y - h
    hcy = top_y + hr * 1.05
    neck_y = hcy + hr * 0.92
    sw = h * (0.13 if child else 0.125)
    sh_y = neck_y + h * 0.03
    hem_y = feet_y - h * 0.045 if hem is None else hem
    hw = sw * (1.3 if outfit in ("thobe", "bisht", "abaya", "dress") else 1.0)
    waist_y = feet_y - h * 0.44
    seated = seated_y is not None
    if seated:
        hem_y = seated_y + h * 0.02
    sl = sleeve or {"bisht": cloak, "abaya": robe, "modern": top, "hoodie": top}.get(outfit, robe)

    # arm geometry
    arm_len = h * (0.36 if child else 0.37)
    shoulders = [(x - sw * 0.82, sh_y + h * 0.03), (x + sw * 0.82, sh_y + h * 0.03)]
    if hands is None:
        hands = [None, None]
    hands = list(hands)
    for i, side in enumerate((-1, 1)):
        if hands[i] is None:
            hands[i] = (shoulders[i][0] + side * sw * 0.45, shoulders[i][1] + arm_len * 0.95)
    human.hands = hands
    aw = sw * (0.7 if outfit == "bisht" else 0.58)

    def arm_items(i):
        side = (-1, 1)[i]
        s = shoulders[i]
        hx, hy = hands[i]
        mx, my = (s[0] + hx) / 2, (s[1] + hy) / 2
        d = math.hypot(hx - s[0], hy - s[1]) or 1
        bend = max(0.0, arm_len - d) * 0.5
        # elbow pushed outward / downward
        ex_, ey_ = mx + side * bend * 0.9, my + bend * 0.5
        out = [R(f"{name}-sleeve", smooth(limb([s, (ex_, ey_), (hx, hy)], aw, aw * 0.8), 1), sl)]
        if mitt and i == mitt_side:
            out.append(R(f"{name}-glove", smooth(limb([(hx - (hx - ex_) * 0.45, hy - (hy - ey_) * 0.45), (hx, hy)], aw * 1.25, aw * 1.15), 1), mitt))
        else:
            out.append(R(f"{name}-hand", circle(hx, hy, max(sw * 0.38, 28)), skin))
        return out

    # legs / feet
    if seated:
        sx = leg_side
        lx0 = x + sx * sw * 0.15
        knee = (x + sx * sw * 0.6, seated_y + h * 0.05)
        foot = (x + sx * sw * 0.75, seated_y + h * 0.3)
        legc = pants if outfit in ("modern", "hoodie") else robe
        it.append(R(f"{name}-leg", smooth(limb([(lx0, seated_y - h * 0.02), knee, foot], sw * 0.62, sw * 0.5), 1), legc))
        it.append(R(f"{name}-shoe", ellipse(foot[0] + sx * sw * 0.12, foot[1] + h * 0.02, max(sw * 0.55, 36), max(h * 0.05, 24)), shoes))
    else:
        if outfit in ("modern", "hoodie"):
            for sxx in (-1, 1):
                it.append(R(f"{name}-leg", [(x + sxx * 3, waist_y), (x + sxx * sw * 0.92, waist_y),
                                           (x + sxx * sw * 0.8, feet_y - h * 0.045), (x + sxx * sw * 0.1, feet_y - h * 0.045)], pants))
            for sxx in (-1, 1):
                it.append(R(f"{name}-shoe", smooth([(x + sxx * sw * 0.02, feet_y), (x + sxx * sw * 0.02, feet_y - h * 0.075),
                                                    (x + sxx * sw * 0.85, feet_y - h * 0.075), (x + sxx * sw * 1.2, feet_y - h * 0.015),
                                                    (x + sxx * sw * 1.15, feet_y)], 1), shoes))
        else:
            for sxx in (-1, 1):
                it.append(R(f"{name}-shoe", ellipse(x + sxx * sw * 0.48, feet_y - h * 0.03, max(sw * 0.5, 42), max(h * 0.04, 27)), shoes))

    # arms drawn behind the body
    for i in (0, 1):
        if not front_arms[i]:
            it += arm_items(i)

    # body
    if outfit in ("modern", "hoodie"):
        bot = waist_y + h * 0.06 if not seated else hem_y
        if hood:
            it.append(R(f"{name}-hood", smooth([(x - hr * 1.15, neck_y - hr * 0.3), (x + hr * 1.15, neck_y - hr * 0.3),
                                                (x + hr * 1.3, neck_y + h * 0.05), (x - hr * 1.3, neck_y + h * 0.05)], 2), top))
        it.append(R(f"{name}-shirt", smooth([(x - sw, sh_y), (x - sw * 0.4, neck_y), (x + sw * 0.4, neck_y), (x + sw, sh_y),
                                             (x + sw * 0.98, bot), (x - sw * 0.98, bot)], 1), top))
        if outfit == "hoodie":
            pk_y = bot - h * 0.03
            it.append(R(f"{name}-pocket", [(x - sw * 0.55, pk_y - h * 0.12), (x + sw * 0.55, pk_y - h * 0.12),
                                           (x + sw * 0.7, pk_y), (x - sw * 0.7, pk_y)], accent))
            it.append(L([(x - hr * 0.25, neck_y + h * 0.01), (x - hr * 0.3, neck_y + h * 0.12)], 5))
            it.append(L([(x + hr * 0.25, neck_y + h * 0.01), (x + hr * 0.3, neck_y + h * 0.12)], 5))
        else:
            it.append(L(arc(x, neck_y, hr * 0.45, hr * 0.35, 10, 170, 10), 5))
    else:
        rc = robe
        body = smooth([(x - sw, sh_y), (x - sw * 0.45, neck_y), (x + sw * 0.45, neck_y), (x + sw, sh_y),
                       (x + sw * 1.02, sh_y + h * 0.12), (x + hw, hem_y), (x - hw, hem_y), (x - sw * 1.02, sh_y + h * 0.12)], 1)
        it.append(R(f"{name}-robe", body, rc))
        if outfit == "dress":
            sk = skirt or accent
            it.append(R(f"{name}-hem", [(x - hw * 0.955, hem_y - h * 0.1), (x + hw * 0.955, hem_y - h * 0.1),
                                        (x + hw * 0.995, hem_y - 3), (x - hw * 0.995, hem_y - 3)], sk))
            it.append(R(f"{name}-yoke", smooth([(x - sw * 0.5, neck_y + h * 0.005), (x + sw * 0.5, neck_y + h * 0.005),
                                                (x + sw * 0.32, neck_y + h * 0.19), (x, neck_y + h * 0.23), (x - sw * 0.32, neck_y + h * 0.19)], 2), emb or accent))
            # embroidery dots on the yoke and hem (lines inside regions)
            for k in range(5):
                yy = hem_y - h * 0.05
                xx = x - hw * 0.7 + k * hw * 0.35
                it.append(L([(xx - h * 0.02, yy), (xx, yy - h * 0.025), (xx + h * 0.02, yy), (xx, yy + h * 0.025), (xx - h * 0.02, yy)], 5))
            it.append(L([(x, neck_y + h * 0.04), (x, neck_y + h * 0.17)], 5))
        elif outfit in ("thobe", "bisht"):
            it.append(L([(x, neck_y + h * 0.02), (x, neck_y + h * 0.18)], 6))
            it.append(L(arc(x, neck_y - h * 0.005, sw * 0.33, h * 0.025, 15, 165, 10), 5))
        elif outfit == "abaya":
            if emb:
                for sxx in (-1, 1):
                    it.append(R(f"{name}-abaya-trim", [(x + sxx * 2, neck_y + h * 0.04), (x + sxx * sw * 0.32, neck_y + h * 0.03),
                                                       (x + sxx * hw * 0.3, hem_y - 4), (x + sxx * 2, hem_y - 4)], emb))
            else:
                it.append(L([(x, neck_y + h * 0.06), (x, hem_y - h * 0.02)], 5))
        if outfit == "bisht":
            for sxx in (-1, 1):
                it.append(R(f"{name}-bisht", smooth([(x + sxx * sw * 0.42, neck_y + h * 0.005), (x + sxx * sw * 1.12, sh_y),
                                                     (x + sxx * sw * 1.2, sh_y + h * 0.15), (x + sxx * hw * 1.12, hem_y - h * 0.035),
                                                     (x + sxx * hw * 0.42, hem_y - h * 0.035), (x + sxx * sw * 0.3, neck_y + h * 0.05)], 1), cloak))
                it.append(R(f"{name}-trim", [(x + sxx * sw * 0.34, neck_y + h * 0.01), (x + sxx * sw * 0.7, neck_y + h * 0.005),
                                             (x + sxx * hw * 0.68, hem_y - h * 0.035), (x + sxx * hw * 0.36, hem_y - h * 0.035)], trim))

    for i in (0, 1):
        if front_arms[i]:
            it += arm_items(i)

    # head
    if head in ("shemagh", "ghutra", "ghutra_plain", "ghutra_taqiyah"):
        cc = accent if head == "shemagh" else WHITE
        tt = 1.0 if hr >= 55 else 1.55
        it.append(R(f"{name}-headcloth", smooth([(x - hr * 1.18, hcy - hr * tt), (x + hr * 1.18, hcy - hr * tt),
                                                 (x + hr * 1.4, hcy + hr * 0.3), (x + sw * 0.8, neck_y + h * 0.13),
                                                 (x + sw * 0.3, neck_y + h * 0.16), (x - sw * 0.3, neck_y + h * 0.16),
                                                 (x - sw * 0.8, neck_y + h * 0.13), (x - hr * 1.4, hcy + hr * 0.3)], 2), cc))
    elif head in ("hijab", "girl_scarf"):
        it.append(R(f"{name}-scarf", smooth([(x - hr * 1.25, hcy - hr * 0.6), (x, hcy - hr * 1.4), (x + hr * 1.25, hcy - hr * 0.6),
                                             (x + hr * 1.35, hcy + hr * 0.6), (x + sw * 0.85, neck_y + h * 0.1),
                                             (x, neck_y + h * 0.13), (x - sw * 0.85, neck_y + h * 0.1), (x - hr * 1.35, hcy + hr * 0.6)], 2), accent))
    it.append(R(f"{name}-face", circle(x, hcy, hr), skin))
    if beard:
        it.append(R(f"{name}-beard", smooth([(x - hr * 0.92, hcy + hr * 0.2), (x - hr * 0.5, hcy + hr * 0.5), (x, hcy + hr * 0.42),
                                             (x + hr * 0.5, hcy + hr * 0.5), (x + hr * 0.92, hcy + hr * 0.2),
                                             (x + hr * 0.7, hcy + hr * 0.95), (x, hcy + hr * 1.3), (x - hr * 0.7, hcy + hr * 0.95)], 2), beard))
        it += face(x, hcy, hr, look, smile=False, old=(beard in (GREY, WHITE)))
        it.append(L(arc(x + hr * 0.15 * look, hcy + hr * 0.66, hr * 0.26, hr * 0.15, 20, 160, 12), max(5, int(hr * 0.06))))
    else:
        it += face(x, hcy, hr, look)
    if head == "ghutra_taqiyah":
        it.append(R(f"{name}-taqiyah", smooth([(x - hr * 1.02, hcy - hr * 0.25), (x - hr * 0.95, hcy - hr * 0.95), (x + hr * 0.95, hcy - hr * 0.95),
                                               (x + hr * 1.02, hcy - hr * 0.25), (x + hr * 0.8, hcy - hr * 0.38), (x, hcy - hr * 0.45),
                                               (x - hr * 0.8, hcy - hr * 0.38)], 1), WHITE))
        for k in range(-3, 4):
            it.append(I(circle(x + k * hr * 0.24, hcy - hr * 0.66 + abs(k) * hr * 0.05, max(4, hr * 0.05), n=10)))
        it.append(R(f"{name}-headcloth-top", smooth([(x - hr * 1.22, hcy - hr * 0.05), (x - hr * 1.12, hcy - hr * 1.05), (x, hcy - hr * 1.6),
                                                     (x + hr * 1.12, hcy - hr * 1.05), (x + hr * 1.22, hcy - hr * 0.05),
                                                     (x + hr * 1.05, hcy - hr * 0.72), (x, hcy - hr * 0.98), (x - hr * 1.05, hcy - hr * 0.72)], 2), WHITE))
    if head in ("shemagh", "ghutra", "ghutra_plain"):
        cc = accent if head == "shemagh" else WHITE
        if hr >= 55:
            it.append(R(f"{name}-headcloth-top", smooth([(x - hr * 1.2, hcy - hr * 0.05), (x - hr * 1.12, hcy - hr * 1.05), (x, hcy - hr * 1.58),
                                                         (x + hr * 1.12, hcy - hr * 1.05), (x + hr * 1.2, hcy - hr * 0.05),
                                                         (x + hr * 0.85, hcy - hr * 0.42), (x, hcy - hr * 0.55), (x - hr * 0.85, hcy - hr * 0.42)], 2), cc))
        if head == "shemagh" and hr >= 55:
            # a hint of the woven pattern, kept inside the cloth
            for k in (-1, 1):
                it.append(L([(x + k * hr * 0.5, hcy - hr * 0.7), (x + k * hr * 0.75, hcy - hr * 0.95)], 4))
        if head != "ghutra_plain":
            agal = arc(x, hcy - hr * 0.33, hr * 1.04, hr * 0.66, 192, 348, 12)
            if hr >= 70:
                it.append(R(f"{name}-agal", smooth(limb(agal, hr * 0.3), 1), BLACK_CLOTH))
            else:
                it.append(L(agal, max(12, int(hr * 0.24))))
    elif head == "taqiyah":
        it.append(R(f"{name}-taqiyah", arc(x, hcy - hr * 0.3, hr * 1.0, hr * 0.85, 180, 360, 20), WHITE))
        it.append(L(arc(x, hcy - hr * 0.3, hr * 0.7, hr * 0.5, 205, 335, 12), 4))
    elif head in ("hijab", "girl_scarf"):
        it.append(R(f"{name}-scarf-front", smooth([(x - hr * 1.12, hcy + hr * 0.1), (x - hr * 1.0, hcy - hr * 0.85), (x, hcy - hr * 1.28),
                                                   (x + hr * 1.0, hcy - hr * 0.85), (x + hr * 1.12, hcy + hr * 0.1),
                                                   (x + hr * 0.9, hcy - hr * 0.42), (x, hcy - hr * 0.62), (x - hr * 0.9, hcy - hr * 0.42)], 2), accent))
    elif head == "cap":
        it.append(R(f"{name}-hair", smooth([(x - hr * 1.02, hcy - hr * 0.1), (x - hr * 0.9, hcy - hr * 0.5), (x + hr * 0.9, hcy - hr * 0.5),
                                            (x + hr * 1.02, hcy - hr * 0.1), (x + hr * 0.95, hcy - hr * 0.35), (x - hr * 0.95, hcy - hr * 0.35)], 1), hair))
        it.append(R(f"{name}-cap", arc(x, hcy - hr * 0.4, hr * 1.02, hr * 0.85, 180, 360, 20), accent))
        bx = x + (1 if look >= 0 else -1) * hr * 0.75
        it.append(R(f"{name}-brim", smooth([(bx - hr * 0.75, hcy - hr * 0.48), (bx + hr * 0.85, hcy - hr * 0.48),
                                            (bx + hr * 0.7, hcy - hr * 0.3), (bx - hr * 0.6, hcy - hr * 0.3)], 1), accent))
    elif head == "hair":
        it.append(R(f"{name}-hair", smooth([(x - hr * 1.05, hcy - hr * 0.05), (x - hr * 1.0, hcy - hr * 0.8), (x, hcy - hr * 1.18),
                                            (x + hr * 1.0, hcy - hr * 0.8), (x + hr * 1.05, hcy - hr * 0.05), (x + hr * 0.8, hcy - hr * 0.45),
                                            (x + hr * 0.2, hcy - hr * 0.6), (x - hr * 0.5, hcy - hr * 0.42), (x - hr * 0.85, hcy - hr * 0.4)], 2), hair))
    human.head = (x, hcy, hr)
    human.shoulders = shoulders
    human.arm_w = aw
    human.neck_y = neck_y
    human.sw = sw
    return it


# ---------------------------------------------------------------- animals
def band(top_pts, bottom_y=None, iterations=2):
    """A ground/sky band: smooth top edge through top_pts (left to right), straight down to bottom_y."""
    bottom_y = H if bottom_y is None else bottom_y
    top = smooth_open(top_pts, iterations)
    return top + [(top[-1][0], bottom_y), (top[0][0], bottom_y)]


def camel2(x, feet_y, h, facing=1, body=DUNE, blanket=RED, band=YELLOW, tassel=YELLOW, name="camel",
           gallop=False, saddle=True, garland=None, halter=RED, lift_head=0.0, tassels=4):
    """A chunky side-view camel. h = height to the top of the hump."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    it = []
    if gallop:
        legs = [((-0.34, 0.6), (-0.46, 0.32), (-0.54, 0.06)), ((0.3, 0.6), (0.44, 0.34), (0.54, 0.1)),
                ((-0.2, 0.6), (-0.14, 0.3), (-0.22, 0.05)), ((0.18, 0.6), (0.26, 0.3), (0.2, 0.05))]
    else:
        legs = [((-0.36, 0.6), (-0.38, 0.3), (-0.38, 0.05)), ((0.34, 0.6), (0.36, 0.3), (0.34, 0.05)),
                ((-0.2, 0.6), (-0.22, 0.3), (-0.2, 0.05)), ((0.2, 0.6), (0.2, 0.3), (0.2, 0.05))]
    for a, b, c in legs:
        it.append(R(f"{name}-leg", smooth(limb([P(*a), P(*b), P(*c)], h * 0.15, h * 0.11), 1), body))
        it.append(R(f"{name}-foot", ellipse(P(*c)[0] + f * h * 0.03, P(*c)[1] + h * 0.0, max(h * 0.1, 46), max(h * 0.05, 25)), body))
    it.append(R(f"{name}-tail", smooth(limb([P(-0.5, 0.8), P(-0.62, 0.62), P(-0.62, 0.46)], h * 0.09, h * 0.075), 1), body))
    it.append(R(f"{name}-body", smooth([P(-0.58, 0.6), P(-0.57, 0.84), P(-0.36, 0.98), P(-0.1, 1.05), P(0.12, 1.0),
                                        P(0.34, 0.88), P(0.52, 0.8), P(0.54, 0.6), P(0.32, 0.46), P(-0.42, 0.46)], 3), body))
    lh = lift_head
    it.append(R(f"{name}-neck", smooth(limb([P(0.4, 0.68), P(0.62, 0.84), P(0.72, 1.1 + lh), P(0.78, 1.24 + lh)], h * 0.24, h * 0.15), 2), body))
    it.append(R(f"{name}-head", smooth([P(0.66, 1.29 + lh), P(0.76, 1.38 + lh), P(0.92, 1.35 + lh), P(1.06, 1.27 + lh),
                                        P(1.06, 1.16 + lh), P(0.9, 1.13 + lh), P(0.74, 1.15 + lh)], 2), body))
    it.append(R(f"{name}-ear", ellipse(*P(0.69, 1.41 + lh), max(h * 0.05, 24), max(h * 0.085, 40), rot=-25 * f), body))
    it.append(I(circle(*P(0.83, 1.29 + lh), h * 0.022)))
    it.append(L(arc(*P(0.83, 1.31 + lh), h * 0.04, h * 0.022, 200, 340, 6), 4))
    it.append(L(arc(*P(1.02, 1.21 + lh), h * 0.03, h * 0.03, 160 if f == 1 else 20, 250 if f == 1 else -70, 6), 5))
    it.append(L([P(0.93, 1.17 + lh), P(1.03, 1.17 + lh)], 4))
    if halter:
        it.append(R(f"{name}-halter", smooth(limb([P(0.76, 1.36 + lh), P(0.78, 1.25 + lh), P(0.8, 1.14 + lh)], max(h * 0.055, 32)), 1), halter))
    if garland:
        for k, (gx, gy) in enumerate([P(0.5, 0.84), P(0.6, 0.93), P(0.68, 1.03)]):
            it.append(R(f"{name}-pompom", circle(gx, gy, max(h * 0.06, 22)), garland[k % len(garland)]))
    if saddle:
        it.append(R(f"{name}-blanket", smooth([P(-0.38, 0.95), P(-0.05, 1.07), P(0.24, 0.95), P(0.32, 0.6), P(-0.44, 0.6)], 1), blanket))
        it.append(R(f"{name}-band", [P(-0.45, 0.71), P(0.31, 0.71), P(0.32, 0.6), P(-0.46, 0.6)], band))
        step = 0.66 / tassels
        for k in range(tassels):
            tx = -0.38 + step * (k + 0.5)
            tw = min(0.075, step * 0.4)
            it.append(R(f"{name}-tassel", smooth([P(tx - tw, 0.6), P(tx + tw, 0.6), P(tx + tw * 0.6, 0.46), P(tx, 0.42), P(tx - tw * 0.6, 0.46)], 1), tassel))
    camel2.seat = P(-0.06, 1.02)
    camel2.mouth = P(1.04, 1.2 + lh)
    camel2.P = P
    return it


def falcon(x, y, s, facing=1, body=BROWN, belly=CREAM, hood=RED, plume=GOLD, name="falcon", talons=YELLOW):
    """Perched hooded saker falcon, three-quarter view. (x, y) = where the feet grip; s = height."""
    f = facing

    def P(px, py):
        return (x + f * px * s, y - py * s)
    it = []
    it.append(R(f"{name}-tail", smooth([P(-0.2, 0.25), P(0.0, 0.2), P(-0.12, -0.38), P(-0.26, -0.42), P(-0.34, -0.34)], 1), body))
    it.append(L([P(-0.14, 0.12), P(-0.22, -0.36)], 5))
    it.append(R(f"{name}-body", smooth([P(-0.26, 0.15), P(-0.3, 0.5), P(-0.18, 0.74), P(0.08, 0.8), P(0.28, 0.66), P(0.32, 0.38),
                                        P(0.22, 0.08), P(0.04, -0.02), P(-0.16, 0.0)], 3), body))
    it.append(R(f"{name}-belly", smooth([P(0.0, 0.66), P(0.24, 0.62), P(0.3, 0.36), P(0.2, 0.08), P(0.04, 0.02), P(-0.04, 0.3)], 3), belly))
    for k in range(3):
        cx, cy = P(0.15, 0.48 - k * 0.13)
        for dx in (-0.06, 0.06):
            it.append(L(arc(cx + f * dx * s, cy, s * 0.03, s * 0.02, 20, 160, 6), 4))
    it.append(R(f"{name}-wing", smooth([P(-0.16, 0.7), P(0.06, 0.66), P(0.1, 0.4), P(0.0, 0.06), P(-0.22, -0.2), P(-0.3, 0.2), P(-0.28, 0.5)], 3), body))
    it.append(L(smooth_open([P(-0.12, 0.5), P(-0.04, 0.3), P(-0.12, 0.06)], 2), 5))
    it.append(L(smooth_open([P(-0.2, 0.42), P(-0.17, 0.2), P(-0.22, -0.02)], 2), 5))
    # head with leather hood (burqa) and plume
    hx, hy = P(0.12, 0.88)
    it.append(R(f"{name}-head", circle(hx, hy, s * 0.2), belly))
    it.append(R(f"{name}-beak", smooth([P(0.24, 0.84), P(0.42, 0.82), P(0.44, 0.7), P(0.36, 0.62), P(0.26, 0.7)], 1), YELLOW))
    it.append(R(f"{name}-hood", smooth([P(-0.08, 0.8), P(-0.07, 1.0), P(0.08, 1.1), P(0.28, 1.04), P(0.36, 0.86), P(0.24, 0.84), P(0.1, 0.76)], 2), hood))
    it.append(L(smooth_open([P(0.0, 0.92), P(0.14, 0.97), P(0.3, 0.92)], 2), 5))
    it.append(R(f"{name}-plume", smooth([P(0.06, 1.06), P(0.0, 1.3), P(0.12, 1.36), P(0.2, 1.08)], 2), plume))
    it.append(R(f"{name}-feet", smooth([P(-0.12, 0.06), P(0.18, 0.06), P(0.2, -0.05), P(-0.14, -0.05)], 1), talons))
    for k in (-0.04, 0.06, 0.15):
        it.append(L([P(k, 0.04), P(k, -0.05)], 4))
    return it


# ---------------------------------------------------------------- Najdi architecture
def crenels(x0, x1, y, size, colour, name="crenel", step=None):
    """Najdi triangular stepped merlons along a parapet (y = parapet top)."""
    it = []
    step = step or size * 1.25
    n = max(1, int((x1 - x0) // step))
    pad = ((x1 - x0) - n * step) / 2
    for k in range(n):
        cx = x0 + pad + step * (k + 0.5)
        it.append(R(name, [(cx - size * 0.5, y + 2), (cx - size * 0.5, y - size * 0.35), (cx - size * 0.25, y - size * 0.35),
                           (cx - size * 0.25, y - size * 0.7), (cx, y - size * 1.0), (cx + size * 0.25, y - size * 0.7),
                           (cx + size * 0.25, y - size * 0.35), (cx + size * 0.5, y - size * 0.35), (cx + size * 0.5, y + 2)], colour))
    return it


def tri_window(cx, cy, s, colour=None, name="window"):
    """Small triangular Najdi vent: solid ink (too small to colour)."""
    return [I([(cx - s / 2, cy + s * 0.43), (cx + s / 2, cy + s * 0.43), (cx, cy - s * 0.43)])]


def crenel_top(x0, x1, y, size, step=None):
    """Points (left to right) of a parapet line with Najdi stepped triangular merlons."""
    step = step or size * 1.3
    n = max(1, int((x1 - x0) // step))
    pad = ((x1 - x0) - n * step) / 2
    pts = [(x0, y)]
    for k in range(n):
        cx = x0 + pad + step * (k + 0.5)
        pts += [(cx - size * 0.5, y), (cx - size * 0.5, y - size * 0.35), (cx - size * 0.25, y - size * 0.35),
                (cx - size * 0.25, y - size * 0.7), (cx, y - size * 1.0), (cx + size * 0.25, y - size * 0.7),
                (cx + size * 0.25, y - size * 0.35), (cx + size * 0.5, y - size * 0.35), (cx + size * 0.5, y)]
    pts.append((x1, y))
    return pts


def najdi_block(x0, x1, top, base, size=56, taper=0, step=None):
    """A mud-brick wall/tower outline with crenellated top; taper = inward slope of each side."""
    return [(x0, base)] + crenel_top(x0 + taper, x1 - taper, top, size, step) + [(x1, base)]


def sun2(cx, cy, r, name="sun"):
    return [R(name + "-rays", star(cx, cy, r * 1.4, r * 1.08, 12, 0), YELLOW), R(name, circle(cx, cy, r), SUN)]


def puff(cx, cy, w, colour=CREAM, name="dust", bumps=7):
    """Bumpy dust/smoke puff, (cx, cy) = centre of its base."""
    pts = []
    for k in range(bumps * 2 + 1):
        a = math.pi + math.pi * k / (bumps * 2)
        rr = 1.0 if k % 2 == 0 else 1.18
        pts.append((cx + math.cos(a) * w / 2 * rr, cy + math.sin(a) * w * 0.38 * rr))
    return [R(name, smooth(pts, 2), colour)]


def najdi_door(x0, y0, x1, y1, colour=BLUE, frame=WHITE, accent=None, name="door"):
    it = [R(f"{name}-frame", rect(x0 - 22, y0 - 22, x1 + 22, y1), frame), R(name, rect(x0, y0, x1, y1), colour)]
    mx = (x0 + x1) / 2
    it.append(L([(mx, y0), (mx, y1)], 6))
    # painted geometric triangles, kept inside the door panel
    for k in range(3):
        yy = y0 + (y1 - y0) * (0.2 + 0.25 * k)
        for cx in ((x0 + mx) / 2, (mx + x1) / 2):
            w = (x1 - x0) * 0.16
            it.append(L([(cx - w, yy + w * 0.8), (cx, yy - w * 0.4), (cx + w, yy + w * 0.8), (cx - w, yy + w * 0.8)], 5))
    return it


# ---------------------------------------------------------------- props
def kite(cx, cy, s, colours=(RED, YELLOW, BLUE, GREEN), rot=0, name="kite", tail_to=None, bows=(PINK, ORANGE, PURPLE)):
    top, right, bot, left = (cx, cy - s), (cx + s * 0.7, cy - s * 0.15), (cx, cy + s * 1.0), (cx - s * 0.7, cy - s * 0.15)
    mid = (cx, cy - s * 0.15)
    tri = [[top, right, mid], [right, bot, mid], [bot, left, mid], [left, top, mid]]
    it = []
    for k, t in enumerate(tri):
        it.append(R(name, rotate(t, rot, cx, cy), colours[k % len(colours)]))
    tail = rotate([bot], rot, cx, cy)[0]
    kite.bottom = tail
    if tail_to is not None:
        pts = smooth_open([tail, ((tail[0] + tail_to[0]) / 2 - s * 0.5, (tail[1] + tail_to[1]) / 2 + s * 0.2), tail_to], 3)
        it.append(L(pts, 6))
        for k in range(1, 3):
            px, py = pts[int(len(pts) * k / 3)]
            a, b = max(s * 0.36, 58), max(s * 0.22, 36)
            it.append(R(f"{name}-bow", [(px - a, py - b), (px, py - b * 0.25), (px + a, py - b), (px + a, py + b), (px, py + b * 0.25), (px - a, py + b)], bows[k - 1]))
    return it


def sword(hx, hy, length, angle_deg, blade=GREY, hilt=GOLD, name="sword"):
    """Curved Arabian sword held at (hx, hy), blade pointing along angle."""
    a = math.radians(angle_deg)
    d = (math.cos(a), math.sin(a))
    n = (-d[1], d[0])
    w = max(length * 0.12, 34)
    pts = []
    for k in range(9):
        t = k / 8
        bend = (t ** 2) * length * 0.16
        px = hx + d[0] * length * t + n[0] * bend
        py = hy + d[1] * length * t + n[1] * bend
        pts.append((px, py))
    blade_poly = limb(pts, w, w * 0.45, caps=False)
    tip = pts[-1]
    it = [R(name, smooth(blade_poly + [], 1), blade)]
    gl = max(length * 0.16, 60)
    g0 = (hx + d[0] * w * 0.2 - n[0] * gl, hy + d[1] * w * 0.2 - n[1] * gl)
    g1 = (hx + d[0] * w * 0.2 + n[0] * gl, hy + d[1] * w * 0.2 + n[1] * gl)
    it.append(R(f"{name}-guard", smooth(limb([g0, g1], max(w * 0.85, 44)), 1), hilt))
    return it


def drum(cx, cy, r, body=RED, skin_c=CREAM, name="drum"):
    """Ardah tar frame drum seen at an angle."""
    it = [R(f"{name}-rim", ellipse(cx, cy, r, r * 1.05, rot=-15), body),
          R(f"{name}-skin", ellipse(cx + r * 0.08, cy - r * 0.02, r * 0.8, r * 0.86, rot=-15), skin_c)]
    return it


def flag(px, py, h, colour=GREEN, name="flag", wave=1, pole=BROWN):
    """Plain green pennant on a pole (no writing). (px, py) = pole base."""
    pw = max(h * 0.022, 16)
    it = [R(f"{name}-pole", rect(px - pw, py - h, px + pw, py), pole)]
    fx, fy = px + pw, py - h * 0.97
    fw, fh = h * 0.5 * wave, h * 0.32
    if wave < 0:
        fx = px - pw
    top = [(fx + fw * t, fy + math.sin(t * math.pi * 2) * fh * 0.14 + t * fh * 0.1) for t in [i / 8 for i in range(9)]]
    bot = [(fx + fw * t, fy + fh + math.sin(t * math.pi * 2) * fh * 0.14 - t * fh * 0.05) for t in [i / 8 for i in range(9)]]
    it.append(R(name, smooth(top + bot[::-1], 1), colour))
    it.append(R(f"{name}-knob", circle(px, py - h - h * 0.02, max(h * 0.045, 28)), GOLD))
    return it


def dallah(cx, base_y, s, colour=GOLD, name="dallah"):
    """Arabic coffee pot, s = height."""
    it = []
    it.append(R(f"{name}-spout", smooth(limb([(cx + s * 0.16, base_y - s * 0.32), (cx + s * 0.38, base_y - s * 0.6), (cx + s * 0.54, base_y - s * 0.8)], s * 0.18, s * 0.1), 1), colour))
    it.append(R(f"{name}-handle", smooth(limb(arc(cx - s * 0.24, base_y - s * 0.52, s * 0.2, s * 0.26, 80, 280, 10), s * 0.1), 1), colour))
    it.append(R(name, smooth([(cx - s * 0.3, base_y), (cx + s * 0.3, base_y), (cx + s * 0.24, base_y - s * 0.35),
                              (cx + s * 0.12, base_y - s * 0.5), (cx + s * 0.16, base_y - s * 0.7), (cx - s * 0.16, base_y - s * 0.7),
                              (cx - s * 0.12, base_y - s * 0.5), (cx - s * 0.24, base_y - s * 0.35)], 1), colour))
    it.append(R(f"{name}-lid", smooth([(cx - s * 0.17, base_y - s * 0.68), (cx + s * 0.17, base_y - s * 0.68), (cx + s * 0.08, base_y - s * 0.86),
                                       (cx, base_y - s * 1.0), (cx - s * 0.08, base_y - s * 0.86)], 1), colour))
    it.append(L([(cx - s * 0.22, base_y - s * 0.36), (cx + s * 0.22, base_y - s * 0.36)], 5))
    return it


def basket(cx, base_y, w, h, colour=MUD, fill=DARK_BROWN, name="basket", heap=True):
    """Woven basket heaped with dates."""
    it = []
    if heap:
        it.append(R(f"{name}-dates", smooth([(cx - w * 0.5, base_y - h * 0.9), (cx - w * 0.42, base_y - h * 1.35), (cx - w * 0.2, base_y - h * 1.62),
                                             (cx + w * 0.1, base_y - h * 1.66), (cx + w * 0.38, base_y - h * 1.42), (cx + w * 0.5, base_y - h * 0.9)], 2), fill))
        for k, (dx, dy) in enumerate(((-0.28, 1.25), (-0.05, 1.45), (0.2, 1.3), (0.02, 1.15), (0.3, 1.1), (-0.22, 1.05))):
            e = ellipse(cx + dx * w, base_y - dy * h, w * 0.065, h * 0.1, rot=20 * (k % 3 - 1), n=16)
            it.append(L(e + [e[0]], 4))
    it.append(R(name, smooth([(cx - w * 0.52, base_y - h), (cx + w * 0.52, base_y - h), (cx + w * 0.42, base_y), (cx - w * 0.42, base_y)], 1), colour))
    it.append(R(f"{name}-rim", smooth(limb([(cx - w * 0.54, base_y - h), (cx + w * 0.54, base_y - h)], max(h * 0.24, 34)), 1), colour))
    for k in range(1, 3):
        yy = base_y - h * 0.85 * k / 3
        it.append(L([(cx - w * (0.43 + 0.08 * k / 3), yy), (cx + w * (0.43 + 0.08 * k / 3), yy)], 5))
    for k in range(-2, 3):
        it.append(L([(cx + k * w * 0.17, base_y - h * 0.85), (cx + k * w * 0.14, base_y - h * 0.05)], 4))
    return it


def sack(cx, base_y, w, h, colour=CREAM, tie=BROWN, name="sack"):
    it = [R(name, smooth([(cx - w * 0.5, base_y), (cx - w * 0.55, base_y - h * 0.5), (cx - w * 0.3, base_y - h * 0.85), (cx - w * 0.12, base_y - h * 0.9),
                          (cx - w * 0.25, base_y - h * 1.1), (cx, base_y - h * 1.0), (cx + w * 0.25, base_y - h * 1.12), (cx + w * 0.12, base_y - h * 0.9),
                          (cx + w * 0.3, base_y - h * 0.85), (cx + w * 0.55, base_y - h * 0.5), (cx + w * 0.5, base_y)], 2), colour)]
    it.append(R(f"{name}-tie", smooth(limb([(cx - w * 0.26, base_y - h * 0.86), (cx + w * 0.26, base_y - h * 0.86)], max(h * 0.1, 34)), 1), tie))
    return it


def tent_black(x0, x1, base_y, h, colour=BLACK_CLOTH, inside=DARK_BROWN, rug=RED, name="tent"):
    """Bedouin goat-hair tent (bait al-sha'ar): long and low with a peaked ridge and an open front."""
    it = []
    w = x1 - x0
    T = lambda u, v: (x0 + w * u, base_y - h * v)
    for gx in (-0.08, 1.08):
        it.append(L([T(0.03 if gx < 0 else 0.97, 0.6), T(gx, -0.05)], 5))
    it.append(R(name, [T(0, 0), T(0.04, 0.6), T(0.24, 0.9), T(0.36, 0.8), T(0.5, 1.0), T(0.64, 0.8), T(0.76, 0.9), T(0.96, 0.6), T(1, 0)], colour))
    for u in (0.24, 0.5, 0.76):
        it.append(L([T(u, 0.95 if u == 0.5 else 0.86), T(u, 0.62)], 5))
    it.append(R(f"{name}-opening", [T(0.28, 0), T(0.3, 0.6), T(0.7, 0.6), T(0.72, 0)], inside))
    it.append(R(f"{name}-flap", [T(0.26, 0.62), T(0.74, 0.62), T(0.72, 0.5), T(0.28, 0.5)], colour))
    it.append(R(f"{name}-rug", [T(0.26, -0.12), T(0.3, 0.12), T(0.7, 0.12), T(0.74, -0.12)], rug))
    zz = [T(0.3 + 0.4 * k / 10, 0.04 if k % 2 else -0.06) for k in range(11)]
    it.append(L(zz, 5))
    return it


def fire(cx, base_y, s, name="fire"):
    it = []
    for k, a in enumerate((-25, 25)):
        it.append(R(f"{name}-log", rotate(rect(cx - s * 0.55, base_y - s * 0.12, cx + s * 0.55, base_y + s * 0.02), a, cx, base_y - s * 0.05), TRUNK))
    it.append(R(f"{name}-flame", smooth([(cx - s * 0.42, base_y - s * 0.08), (cx - s * 0.5, base_y - s * 0.45), (cx - s * 0.28, base_y - s * 0.7),
                                         (cx - s * 0.2, base_y - s * 0.5), (cx - s * 0.05, base_y - s * 1.05), (cx + s * 0.18, base_y - s * 0.62),
                                         (cx + s * 0.3, base_y - s * 0.78), (cx + s * 0.48, base_y - s * 0.4), (cx + s * 0.4, base_y - s * 0.08)], 2), ORANGE))
    it.append(R(f"{name}-core", smooth([(cx - s * 0.22, base_y - s * 0.08), (cx - s * 0.2, base_y - s * 0.35), (cx, base_y - s * 0.58),
                                        (cx + s * 0.18, base_y - s * 0.32), (cx + s * 0.2, base_y - s * 0.08)], 2), YELLOW))
    return it


def firework(cx, cy, r, colour, name="firework", rays=10):
    it = [R(name, star(cx, cy, r, r * 0.45, rays, -90), colour)]
    if r >= 120:
        it.append(R(f"{name}-c", circle(cx, cy, r * 0.28), YELLOW if colour != YELLOW else WHITE))
    for k in range(rays):
        a = 2 * math.pi * (k + 0.5) / rays - math.pi / 2
        it.append(I(circle(cx + math.cos(a) * r * 1.05, cy + math.sin(a) * r * 1.05, max(5, r * 0.05), n=12)))
    return it


def cotton_candy(hx, hy, s, colour=PINK, name="candy"):
    """Cotton candy on a stick held at (hx, hy)."""
    top = (hx, hy - s * 0.9)
    it = [R(f"{name}-stick", smooth(limb([(hx, hy + s * 0.25), top], max(s * 0.15, 30)), 1), WHITE)]
    it.append(R(name, smooth([(top[0] - s * 0.45, top[1] + s * 0.1), (top[0] - s * 0.6, top[1] - s * 0.3), (top[0] - s * 0.35, top[1] - s * 0.7),
                              (top[0], top[1] - s * 0.8), (top[0] + s * 0.38, top[1] - s * 0.68), (top[0] + s * 0.58, top[1] - s * 0.3),
                              (top[0] + s * 0.42, top[1] + s * 0.1), (top[0], top[1] + s * 0.18)], 3), colour))
    it.append(L(smooth_open([(top[0] - s * 0.32, top[1] - s * 0.42), (top[0] - s * 0.1, top[1] - s * 0.22), (top[0] + s * 0.15, top[1] - s * 0.3), (top[0] + s * 0.3, top[1] - s * 0.5)], 2), 5))
    return it


def balance_scale(cx, top_y, s, name="scale", colour=GOLD, left_load=None, right_load=None):
    """Hanging balance: hook at (cx, top_y); s = beam width."""
    it = []
    beam_y = top_y + s * 0.25
    pan_y = beam_y + s * 0.5
    it.append(L([(cx, top_y), (cx, beam_y)], 8))
    for sx in (-1, 1):
        px = cx + sx * s * 0.5
        it.append(L([(px, beam_y), (px - s * 0.2, pan_y)], 5))
        it.append(L([(px, beam_y), (px + s * 0.2, pan_y)], 5))
    it.append(R(f"{name}-beam", smooth(limb([(cx - s * 0.55, beam_y), (cx + s * 0.55, beam_y)], s * 0.07), 1), colour))
    it.append(R(f"{name}-pivot", circle(cx, beam_y, max(s * 0.07, 30)), colour))
    for sx, load in ((-1, left_load), (1, right_load)):
        px = cx + sx * s * 0.5
        if load:
            it.append(R(f"{name}-load", smooth([(px - s * 0.18, pan_y + 2), (px - s * 0.1, pan_y - s * 0.12), (px, pan_y - s * 0.16),
                                                (px + s * 0.1, pan_y - s * 0.12), (px + s * 0.18, pan_y + 2)], 2), load))
        it.append(R(f"{name}-pan", arc(px, pan_y, s * 0.26, s * 0.13, 0, 180, 14), colour))
    return it


def cat(x, feet_y, s, facing=1, colour=ORANGE, name="cat"):
    """Sitting cat, s = height."""
    f = facing

    def P(px, py):
        return (x + f * px * s, feet_y - py * s)
    it = [R(f"{name}-tail", smooth(limb([P(-0.22, 0.06), P(-0.5, 0.1), P(-0.58, 0.32), P(-0.5, 0.5)], s * 0.14, s * 0.12), 1), colour)]
    it.append(R(f"{name}-body", smooth([P(-0.32, 0.0), P(-0.34, 0.3), P(-0.17, 0.62), P(0.14, 0.64), P(0.28, 0.3), P(0.3, 0.0)], 2), colour))
    hx, hy = P(0.0, 0.8)
    head = [P(-0.3, 0.78), P(-0.3, 1.1), P(-0.12, 0.98), P(0.12, 0.98), P(0.3, 1.1), P(0.3, 0.78), P(0.2, 0.6), P(-0.2, 0.6)]
    it.append(R(f"{name}-head", smooth(head, 1), colour))
    for sx in (-1, 1):
        it.append(I(ellipse(hx + sx * s * 0.11, hy - s * 0.01, s * 0.035, s * 0.05)))
        it.append(L([(hx + sx * s * 0.16, hy + s * 0.09), (hx + sx * s * 0.36, hy + s * 0.06)], 4))
    it.append(L(arc(hx, hy + s * 0.08, s * 0.06, s * 0.04, 20, 160, 6), 4))
    it.append(L([P(-0.04, 0.0), P(-0.04, 0.25)], 4))
    return it


def lantern(cx, top_y, s, glass=YELLOW, metal=GOLD, name="lantern"):
    it = [L([(cx, top_y - s * 0.3), (cx, top_y)], 5)]
    it.append(I([(cx - s * 0.32, top_y + s * 0.22), (cx, top_y), (cx + s * 0.32, top_y + s * 0.22)]))
    it.append(R(name, smooth([(cx - s * 0.26, top_y + s * 0.2), (cx + s * 0.26, top_y + s * 0.2), (cx + s * 0.32, top_y + s * 0.6),
                              (cx + s * 0.2, top_y + s * 0.9), (cx - s * 0.2, top_y + s * 0.9), (cx - s * 0.32, top_y + s * 0.6)], 1), glass))
    it.append(I(rect(cx - s * 0.22, top_y + s * 0.88, cx + s * 0.22, top_y + s * 1.0)))
    return it


def backpack(cx, cy, w, h, colour=ORANGE, pocket=YELLOW, name="backpack"):
    """Backpack seen from the front peeking out behind a person (straps drawn separately)."""
    return [R(name, smooth([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], 2), colour)]


def sheep(x, feet_y, s, facing=1, wool=WHITE, face_c=DARK_BROWN, name="sheep"):
    f = facing

    def P(px, py):
        return (x + f * px * s, feet_y - py * s)
    it = []
    for lx in (-0.35, -0.2, 0.2, 0.35):
        it.append(R(f"{name}-leg", rect(*P(lx - 0.04, 0.4), *P(lx + 0.04, 0.0)) if f == 1 else rect(*P(lx + 0.04, 0.4), *P(lx - 0.04, 0.0)), face_c))
    blob = []
    for k in range(14):
        a = 2 * math.pi * k / 14
        rr = 1.0 if k % 2 == 0 else 0.86
        blob.append(P(math.cos(a) * 0.5 * rr, 0.62 + math.sin(a) * 0.3 * rr))
    it.append(R(f"{name}-wool", smooth(blob, 2), wool))
    it.append(R(f"{name}-head", ellipse(*P(0.52, 0.78), s * 0.15, s * 0.2, rot=25 * f), face_c))
    it.append(R(f"{name}-ear", ellipse(*P(0.42, 0.88), s * 0.1, s * 0.05, rot=-20 * f), face_c))
    hx, hy = P(0.56, 0.82)
    it.append(R(f"{name}-eye", circle(hx, hy, s * 0.045), WHITE))
    it.append(I(circle(hx, hy, s * 0.022)))
    return it


def crenel_line(p0, p1, s0, s1, n):
    """Points from p0 to p1 with n stepped merlons whose size shrinks from s0 to s1 (perspective walls)."""
    pts = [p0]
    for k in range(n):
        t0, t1 = (k + 0.2) / n, (k + 0.8) / n
        tm = (t0 + t1) / 2
        sz = s0 + (s1 - s0) * tm

        def at(t, up):
            return (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t - up)
        pts += [at(t0, 0), at(t0, sz * 0.4), at(t0 + (t1 - t0) * 0.25, sz * 0.4), at(t0 + (t1 - t0) * 0.25, sz * 0.75),
                at(tm, sz * 1.05), at(t1 - (t1 - t0) * 0.25, sz * 0.75), at(t1 - (t1 - t0) * 0.25, sz * 0.4), at(t1, sz * 0.4), at(t1, 0)]
    pts.append(p1)
    return pts


def quad_lerp(q, u, v):
    """Bilinear point in quad q = [top-left, top-right, bottom-right, bottom-left]."""
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = q
    tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
    bx2, by2 = dx + (cx - dx) * u, dy + (cy - dy) * u
    return (tx + (bx2 - tx) * v, ty + (by2 - ty) * v)


def sub_quad(q, u0, v0, u1, v1):
    return [quad_lerp(q, u0, v0), quad_lerp(q, u1, v0), quad_lerp(q, u1, v1), quad_lerp(q, u0, v1)]


def ferris_wheel(cx, cy, r, base_y, rim=PURPLE, cabins=(RED, YELLOW, BLUE, GREEN, ORANGE, PINK), legs=GREY,
                 inner=None, n=8, name="wheel"):
    it = []
    for sx in (-1, 1):
        it.append(R(f"{name}-leg", smooth(limb([(cx, cy), (cx + sx * r * 0.62, base_y)], r * 0.09), 1), legs))
    it.append(R(f"{name}-rim", circle(cx, cy, r), rim))
    it.append(R(f"{name}-inside", circle(cx, cy, r * 0.88), inner))
    for k in range(n):
        a = 2 * math.pi * k / n
        it.append(L([(cx, cy), (cx + math.cos(a) * r * 0.88, cy + math.sin(a) * r * 0.88)], 6))
    it.append(R(f"{name}-hub", circle(cx, cy, r * 0.1), YELLOW))
    for k in range(n):
        a = 2 * math.pi * (k + 0.5) / n
        px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
        cw = r * 0.2
        it.append(L([(px, py), (px, py + cw * 0.3)], 6))
        it.append(R(f"{name}-cabin", smooth([(px - cw * 0.6, py + cw * 0.25), (px + cw * 0.6, py + cw * 0.25),
                                             (px + cw * 0.5, py + cw * 1.05), (px - cw * 0.5, py + cw * 1.05)], 1), cabins[k % len(cabins)]))
    return it


def bunting(p0, p1, n, colours, size, sag=60, name="flag"):
    pts = smooth_open([p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + sag), p1], 3)
    it = [L(pts, 5)]
    for k in range(n):
        t = (k + 0.5) / n
        i = int(t * (len(pts) - 1))
        px, py = pts[i]
        it.append(R(name, [(px - size * 0.5, py), (px + size * 0.5, py), (px, py + size * 1.1)], colours[k % len(colours)]))
    return it


def crescent(cx, cy, r, ox, oy, r2, n=90):
    """Crescent: circle (cx, cy, r) minus circle (cx+ox, cy+oy, r2)."""
    A = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    bx, by = cx + ox, cy + oy
    out = [i for i, (x, y) in enumerate(A) if math.hypot(x - bx, y - by) > r2]
    # rotate so the outside arc is contiguous
    start = next(i for i in out if (i - 1) % n not in out)
    arcA = [A[(start + k) % n] for k in range(len(out))]
    B = [(bx + r2 * math.cos(2 * math.pi * k / n), by + r2 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    ins = [i for i, (x, y) in enumerate(B) if math.hypot(x - cx, y - cy) < r]
    startb = next(i for i in ins if (i - 1) % n not in ins)
    arcB = [B[(startb + k) % n] for k in range(len(ins))]
    return arcA + arcB[::-1]


def rosette(cx, cy, r, colour=BLUE, centre=GOLD, ribbon=RED, name="rosette"):
    """Prize rosette (no writing)."""
    it = []
    for sx in (-1, 1):
        it.append(R(f"{name}-ribbon", [(cx - sx * r * 0.3, cy), (cx + sx * r * 0.95, cy + r * 1.9), (cx + sx * r * 0.6, cy + r * 1.65),
                                       (cx + sx * r * 0.3, cy + r * 2.05), (cx - sx * r * 0.45, cy + r * 0.3)], ribbon))
    it.append(R(name, star(cx, cy, r, r * 0.8, 14, 0), colour))
    it.append(R(f"{name}-centre", circle(cx, cy, r * 0.55), centre))
    return it


def pavilion(x0, x1, base_y, h, colour=WHITE, stripe=RED, name="pavilion", door=True):
    """Festival tent: walls plus a peaked roof, with stripes."""
    w = x1 - x0
    it = [R(name, rect(x0, base_y - h * 0.5, x1, base_y), colour)]
    if door:
        it.append(R(f"{name}-door", [(x0 + w * 0.4, base_y), (x0 + w * 0.42, base_y - h * 0.38), (x0 + w * 0.58, base_y - h * 0.38), (x0 + w * 0.6, base_y)], DARK_BROWN))
    it.append(R(f"{name}-roof", [(x0 - w * 0.06, base_y - h * 0.5), (x0 + w * 0.5, base_y - h), (x1 + w * 0.06, base_y - h * 0.5)], stripe))
    it.append(R(f"{name}-roof-band", [(x0 - w * 0.06, base_y - h * 0.5), (x1 + w * 0.06, base_y - h * 0.5), (x1, base_y - h * 0.42), (x0, base_y - h * 0.42)], colour))
    it.append(L([(x0 + w * 0.5, base_y - h), (x0 + w * 0.5, base_y - h * 1.2)], 8))
    it.append(R(f"{name}-pennant", [(x0 + w * 0.5, base_y - h * 1.2), (x0 + w * 0.5 + h * 0.32, base_y - h * 1.1), (x0 + w * 0.5, base_y - h * 1.0)], GREEN))
    return it

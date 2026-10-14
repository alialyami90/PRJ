"""Extra figure helpers for the Hail scenes (people, horse, falcon, saluki, vehicles, props).

Every helper returns an item list for Scene.extend():
("region", name, points, colour) | ("ink", points) | ("line", points, width).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))
from scene_kit import *  # noqa: E402,F403

DENIM = "#5C7FBF"


def R(name, pts, col):
    return ("region", name, [tuple(p) for p in pts], col)


def INK(pts):
    return ("ink", [tuple(p) for p in pts])


def LN(pts, w=6):
    return ("line", [tuple(p) for p in pts], w)


def limb(path, w0, w1=None, caps=True):
    """Polygon around an open polyline, width tapering w0 -> w1, round ends."""
    w1 = w0 if w1 is None else w1
    path = [tuple(p) for p in path]
    n = len(path)
    left, right = [], []
    for i, (x, y) in enumerate(path):
        if i == 0:
            dx, dy = path[1][0] - x, path[1][1] - y
        elif i == n - 1:
            dx, dy = x - path[i - 1][0], y - path[i - 1][1]
        else:
            dx, dy = path[i + 1][0] - path[i - 1][0], path[i + 1][1] - path[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))

    def cap(p, q, w, forward):
        # half circle around p, from left side to right side, bulging away from q
        a = math.atan2(p[1] - q[1], p[0] - q[0])
        pts = []
        for k in range(1, 12):
            t = a + math.pi / 2 - math.pi * k / 12
            pts.append((p[0] + math.cos(t) * w / 2, p[1] + math.sin(t) * w / 2))
        return pts if forward else pts

    if not caps:
        return left + right[::-1]
    end = cap(path[-1], path[-2], w1, True)
    start = cap(path[0], path[1], w0, True)
    return left + end + right[::-1] + start


def clip_below(pts, y0):
    """Part of polygon pts with y >= y0 (Sutherland-Hodgman against one horizontal line)."""
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        ina, inb = a[1] >= y0, b[1] >= y0
        if ina:
            out.append(a)
        if ina != inb:
            t = (y0 - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, y0))
    return out


def clip_above(pts, y0):
    return [(x, -y) for x, y in clip_below([(x, -y) for x, y in pts], -y0)]


def bend(p0, p1, amount):
    """Mid point of p0-p1 pushed sideways by `amount` (positive = to the right of the travel direction)."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    return (mx - dy / L * amount, my + dx / L * amount)


# ------------------------------------------------------------------ people
def human(x, feet_y, h, *, name="kid", adult=False, facing=0, skin=SKIN,
          outfit="tshirt", top=WHITE, bottom=DENIM, accent=RED, cloak=BROWN, trim=GOLD,
          shoes=DARK_BROWN, head="none", head_col=RED, hair=DARK_BROWN,
          hands=None, elbows=None, feet=None, knees=None, seated_y=None,
          beard=None, print_col=None, mouth="smile", hand_r=None, ponytail=False, hem_col=None):
    """A chunky, friendly front-facing person.

    outfit: tshirt | hoodie | tracksuit | overalls | racing | thobe | bisht
    head:   none | cap | shemagh | ghutra | headscarf | turban
    hands:  (left_hand_xy, right_hand_xy) absolute, None = hanging by the side.
    feet:   (left_foot_xy, right_foot_xy) absolute, None = standing.
    seated_y: for riders/drivers: torso/robe ends at this y (the seat), legs follow `feet`/`knees`.
    Returns items; human.hands / human.head / human.shoulders hold useful anchor points afterwards.
    """
    it = []
    hr = h * (0.095 if adult else 0.135)
    head_cy = feet_y - h + hr * (1.25 if head in ("shemagh", "ghutra", "turban") else 1.05)
    neck_y = head_cy + hr * 0.92
    sh = h * (0.16 if adult else 0.145)
    sho_y = neck_y + h * 0.035
    hip_y = feet_y - h * (0.47 if adult else 0.38)
    robe = outfit in ("thobe", "bisht")
    one_piece = outfit == "racing"
    hem_y = feet_y - h * 0.07
    arm_w = h * (0.075 if adult else 0.085)
    hand_r = hand_r or max(h * (0.042 if adult else 0.05), 30)
    leg_w = h * (0.105 if adult else 0.11)
    off = hr * 0.2 * facing

    # ---- legs and shoes
    hipL, hipR = (x - sh * 0.45, hip_y), (x + sh * 0.45, hip_y)
    if seated_y is not None:
        hipL, hipR = (x - sh * 0.45, seated_y - leg_w * 0.4), (x + sh * 0.45, seated_y - leg_w * 0.4)
    if feet is None:
        feet = ((x - sh * 0.45, feet_y - h * 0.035), (x + sh * 0.45, feet_y - h * 0.035))
    leg_col = top if one_piece else (bottom if not robe else top)
    for i, (hp, ft) in enumerate(zip((hipL, hipR), feet)):
        if robe and seated_y is None:
            break
        kn = knees[i] if knees else None
        path = [hp, kn, ft] if kn else [hp, ft]
        it.append(R(f"{name}-leg", limb(path, leg_w, leg_w * 0.85), leg_col))
    for i, ft in enumerate(feet if shoes else ()):
        side = -1 if i == 0 else 1
        fdir = facing if facing else side * 0.3
        if robe and seated_y is None:
            ft = (ft[0] + side * leg_w * 0.2, ft[1] + leg_w * 0.05)
            fdir *= 1.2
        sw = 1.3 if robe and seated_y is None else 1.0
        it.append(R(f"{name}-shoe", scale(smooth([(ft[0] - leg_w * 0.7 + fdir * leg_w * 0.2, ft[1] - leg_w * 0.45),
                                            (ft[0] + leg_w * 0.5 + fdir * leg_w * 0.5, ft[1] - leg_w * 0.4),
                                            (ft[0] + leg_w * 0.75 + fdir * leg_w * 0.7, ft[1] + leg_w * 0.4),
                                            (ft[0] - leg_w * 0.75 + fdir * leg_w * 0.2, ft[1] + leg_w * 0.4)], 2), sw, ft[0], ft[1] + leg_w * 0.4), shoes))

    # ---- torso
    bot_y = seated_y if seated_y is not None else (hem_y if robe else hip_y + h * 0.05)
    hem_w = sh * (1.25 if robe and seated_y is None else (1.05 if robe else 0.96))
    if outfit == "bisht":
        # cloak back panel, wider than the robe
        it.append(R(f"{name}-bisht-back", smooth([(x - sh * 1.05, sho_y - h * 0.01), (x + sh * 1.05, sho_y - h * 0.01),
                                                    (x + hem_w * 1.2, bot_y - h * 0.02), (x - hem_w * 1.2, bot_y - h * 0.02)], 1), cloak))
    torso_col = top
    body_pts = smooth([(x - sh * 0.4, neck_y), (x - sh, sho_y), (x - sh * 0.98, sho_y + h * 0.08),
                       (x - hem_w, bot_y), (x - hem_w * 0.6, bot_y + h * 0.008), (x + hem_w * 0.6, bot_y + h * 0.008), (x + hem_w, bot_y),
                       (x + sh * 0.98, sho_y + h * 0.08), (x + sh, sho_y), (x + sh * 0.4, neck_y)], 1)
    it.append(R(f"{name}-body", body_pts, torso_col))
    if hem_col:
        it.append(R(f"{name}-hem", clip_below(body_pts, bot_y - h * 0.075), hem_col))
    if outfit == "thobe" or outfit == "bisht":
        it.append(LN([(x + off * 0.3, neck_y + h * 0.02), (x + off * 0.3, neck_y + h * 0.15)], 6))
    if outfit == "tshirt" and print_col:
        it.append(R(f"{name}-shirt-star", star(x, sho_y + h * 0.12, h * 0.065, h * 0.03), print_col))
    if outfit == "hoodie":
        it.append(R(f"{name}-pocket", smooth([(x - sh * 0.6, bot_y - h * 0.02), (x - sh * 0.45, bot_y - h * 0.11),
                                              (x + sh * 0.45, bot_y - h * 0.11), (x + sh * 0.6, bot_y - h * 0.02)], 1), accent))
    if outfit == "tracksuit":
        it.append(LN([(x, neck_y + h * 0.03), (x, bot_y - h * 0.01)], 6))
        it.append(R(f"{name}-hem", rect(x - hem_w * 0.98, bot_y - h * 0.035, x + hem_w * 0.98, bot_y), accent))
        it.append(R(f"{name}-collar", smooth([(x - sh * 0.55, neck_y - h * 0.005), (x + sh * 0.55, neck_y - h * 0.005),
                                              (x + sh * 0.3, neck_y + h * 0.05), (x - sh * 0.3, neck_y + h * 0.05)], 1), accent))
    if outfit == "overalls":
        it.append(R(f"{name}-bib", smooth([(x - sh * 0.62, sho_y + h * 0.075), (x + sh * 0.62, sho_y + h * 0.075),
                                           (x + sh * 0.7, bot_y), (x - sh * 0.7, bot_y)], 1) if True else None, bottom))
        it.append(R(f"{name}-bib-pocket", rect(x - sh * 0.32, sho_y + h * 0.11, x + sh * 0.32, sho_y + h * 0.18), accent))
    if outfit == "racing":
        it.append(R(f"{name}-stripe", smooth([(x - sh * 0.99, sho_y + h * 0.07), (x + sh * 0.99, sho_y + h * 0.07),
                                              (x + sh * 0.99, sho_y + h * 0.13), (x - sh * 0.99, sho_y + h * 0.13)], 1), accent))
        it.append(R(f"{name}-belt", rect(x - hem_w * 0.97, bot_y - h * 0.05, x + hem_w * 0.97, bot_y - h * 0.005), BLACK_CLOTH))
        it.append(R(f"{name}-collar", smooth([(x - sh * 0.5, neck_y - h * 0.005), (x + sh * 0.5, neck_y - h * 0.005),
                                              (x + sh * 0.3, neck_y + h * 0.045), (x - sh * 0.3, neck_y + h * 0.045)], 1), accent))
    if outfit == "bisht":
        for sx in (-1, 1):
            it.append(R(f"{name}-bisht", smooth([(x + sx * sh * 0.32, neck_y + h * 0.005), (x + sx * sh * 1.08, sho_y - h * 0.005),
                                                 (x + sx * hem_w * 1.2, bot_y - h * 0.02), (x + sx * hem_w * 0.42, bot_y - h * 0.02)], 1), cloak))
            it.append(R(f"{name}-bisht-trim", [(x + sx * sh * 0.32, neck_y + h * 0.005), (x + sx * sh * 0.62, neck_y + h * 0.01),
                                               (x + sx * hem_w * 0.66, bot_y - h * 0.02), (x + sx * hem_w * 0.42, bot_y - h * 0.02)], trim))

    # ---- head-cloth drape (over the shoulders, behind the face)
    if head in ("shemagh", "ghutra", "headscarf"):
        col = WHITE if head == "ghutra" else head_col
        drop = h * (0.10 if head == "headscarf" else 0.14)
        it.append(R(f"{name}-headcloth", smooth([(x - hr * 1.2, head_cy - hr * 0.5), (x, head_cy - hr * 1.32), (x + hr * 1.2, head_cy - hr * 0.5),
                                                 (x + hr * 1.5, neck_y + drop * 0.6), (x + hr * 1.25, neck_y + drop),
                                                 (x - hr * 1.25, neck_y + drop), (x - hr * 1.5, neck_y + drop * 0.6)], 2), col))
        if head == "shemagh":
            for sx in (-1, 1):
                it.append(LN([(x + sx * hr * 1.05, neck_y + drop * 0.05), (x + sx * hr * 1.22, neck_y + drop * 0.85)], 5))
    if head in ("none", "cap") and (head == "none" or ponytail):
        if ponytail:
            px = x - (facing or 1) * hr * 0.9
            it.append(R(f"{name}-ponytail", smooth([(px, head_cy - hr * 0.5), (px - (facing or 1) * hr * 0.8, head_cy),
                                                    (px - (facing or 1) * hr * 0.6, head_cy + hr * 1.3), (px + (facing or 1) * hr * 0.1, head_cy + hr * 0.6)], 2), hair))
        it.append(R(f"{name}-hair", smooth([(x - hr * 1.08, head_cy + hr * 0.1), (x - hr * 1.0, head_cy - hr * 0.8), (x, head_cy - hr * 1.18),
                                            (x + hr * 1.0, head_cy - hr * 0.8), (x + hr * 1.08, head_cy + hr * 0.1)], 2), hair))

    # ---- arms
    shL, shR = (x - sh * 0.82, sho_y + h * 0.035), (x + sh * 0.82, sho_y + h * 0.035)
    if hands is None:
        hands = (None, None)
    out_hands = []
    sleeve_col = cloak if outfit == "bisht" else top
    for i, (sp, hp) in enumerate(zip((shL, shR), hands)):
        side = -1 if i == 0 else 1
        if hp is None:
            hp = (sp[0] + side * sh * 0.32, sp[1] + h * 0.30)
        el = elbows[i] if elbows and elbows[i] else bend(sp, hp, side * h * 0.025 * (1 if hp[1] > sp[1] else -1))
        path = [sp, el, hp]
        if outfit == "tshirt":
            it.append(R(f"{name}-arm", limb(path, arm_w * 0.85, arm_w * 0.75), skin))
            ex, ey = el
            mid = (sp[0] + (ex - sp[0]) * 0.75, sp[1] + (ey - sp[1]) * 0.75)
            it.append(R(f"{name}-sleeve", limb([sp, mid], arm_w * 1.15, arm_w * 1.05), sleeve_col))
        else:
            # sleeve stops just short of the hand
            dx, dy = hp[0] - el[0], hp[1] - el[1]
            cuff = (hp[0] - dx * 0.18, hp[1] - dy * 0.18)
            w0 = arm_w * (1.25 if outfit == "bisht" else 1.0)
            w1 = arm_w * (1.35 if outfit == "bisht" else 0.85)
            it.append(R(f"{name}-sleeve", limb([sp, el, cuff], w0, w1), sleeve_col))
            if outfit in ("tracksuit", "racing") and math.hypot(dx, dy) * 0.27 * w1 > 2600:
                c2 = (hp[0] - dx * 0.45, hp[1] - dy * 0.45)
                it.append(R(f"{name}-cuff", limb([c2, cuff], w1 * 1.05, w1 * 1.05, caps=False), accent))
        it.append(R(f"{name}-hand", circle(hp[0], hp[1], hand_r), skin))
        out_hands.append(hp)
    human.hands = out_hands

    if outfit == "overalls":
        for sx in (-1, 1):
            it.append(R(f"{name}-strap", [(x + sx * sh * 0.3, sho_y + h * 0.09), (x + sx * sh * 0.66, sho_y + h * 0.09),
                                          (x + sx * sh * 0.62, sho_y - h * 0.01), (x + sx * sh * 0.3, sho_y - h * 0.01)], bottom))
    # ---- face
    it.append(R(f"{name}-face", circle(x, head_cy, hr), skin))
    for sx in (-1, 1):
        it.append(INK(ellipse(x + off + sx * hr * 0.36, head_cy - hr * 0.02, hr * 0.105, hr * 0.14)))
    if beard:
        it.append(R(f"{name}-beard", smooth([(x - hr * 0.92, head_cy + hr * 0.1), (x - hr * 0.55, head_cy + hr * 0.42),
                                             (x + hr * 0.55, head_cy + hr * 0.42), (x + hr * 0.92, head_cy + hr * 0.1),
                                             (x + hr * 0.7, head_cy + hr * 0.95), (x, head_cy + hr * 1.18),
                                             (x - hr * 0.7, head_cy + hr * 0.95)], 2), beard))
        it.append(LN(arc(x + off, head_cy + hr * 0.52, hr * 0.28, hr * 0.16, 15, 165, 10), max(5, int(hr * 0.07))))
    elif mouth == "smile":
        it.append(LN(arc(x + off, head_cy + hr * 0.25, hr * 0.32, hr * 0.24, 20, 160, 12), max(5, int(hr * 0.075))))
    elif mouth == "open":
        it.append(INK(arc(x + off, head_cy + hr * 0.28, hr * 0.3, hr * 0.3, 0, 180, 14)))
    if head == "none":
        it.append(R(f"{name}-fringe", smooth([(x - hr * 1.02, head_cy - hr * 0.05), (x - hr * 0.95, head_cy - hr * 0.7), (x - hr * 0.3, head_cy - hr * 1.12),
                                              (x + hr * 0.5, head_cy - hr * 1.08), (x + hr * 1.0, head_cy - hr * 0.6), (x + hr * 1.03, head_cy - hr * 0.1),
                                              (x + hr * 0.8, head_cy - hr * 0.42), (x + hr * 0.2, head_cy - hr * 0.55), (x - hr * 0.5, head_cy - hr * 0.45),
                                              (x - hr * 0.85, head_cy - hr * 0.35)], 2), hair))
    # nose hint
    it.append(LN(arc(x + off * 1.6, head_cy + hr * 0.1, hr * 0.08, hr * 0.06, 20, 160, 6), 5))

    # ---- headwear front
    if head in ("shemagh", "ghutra", "headscarf"):
        col = WHITE if head == "ghutra" else head_col
        it.append(R(f"{name}-headcloth-top", smooth([(x - hr * 1.1, head_cy - hr * 0.1), (x - hr * 0.95, head_cy - hr * 0.95), (x, head_cy - hr * 1.3),
                                                     (x + hr * 0.95, head_cy - hr * 0.95), (x + hr * 1.1, head_cy - hr * 0.1),
                                                     (x + hr * 0.75, head_cy - hr * 0.4), (x, head_cy - hr * 0.5), (x - hr * 0.75, head_cy - hr * 0.4)], 2), col))
        if head != "headscarf":
            it.append(R(f"{name}-agal", limb(arc(x, head_cy - hr * 1.08, hr * 1.04, hr * 0.34, 8, 172, 16), max(hr * 0.27, 28)), BLACK_CLOTH))
    elif head == "cap":
        it.append(R(f"{name}-cap", arc(x, head_cy - hr * 0.3, hr * 1.02, hr * 0.92, 180, 360, 30), head_col))
        fc = facing if facing else 1
        it.append(R(f"{name}-cap-brim", smooth([(x + fc * hr * 0.1, head_cy - hr * 0.66), (x + fc * hr * 1.65, head_cy - hr * 0.68),
                                                (x + fc * hr * 1.72, head_cy - hr * 0.24), (x + fc * hr * 0.1, head_cy - hr * 0.2)], 2), head_col))
    elif head == "turban":
        it.append(R(f"{name}-turban", smooth([(x - hr * 1.15, head_cy - hr * 0.15), (x - hr * 1.25, head_cy - hr * 0.95), (x - hr * 0.7, head_cy - hr * 1.6),
                                              (x + hr * 0.7, head_cy - hr * 1.6), (x + hr * 1.25, head_cy - hr * 0.95), (x + hr * 1.15, head_cy - hr * 0.15),
                                              (x + hr * 0.6, head_cy - hr * 0.5), (x, head_cy - hr * 0.6), (x - hr * 0.6, head_cy - hr * 0.5)], 2), head_col))
        for k in range(3):
            it.append(LN(smooth_open([(x - hr * (1.05 - 0.1 * k), head_cy - hr * (0.55 + 0.32 * k)), (x, head_cy - hr * (0.95 + 0.25 * k)),
                                      (x + hr * (1.05 - 0.1 * k), head_cy - hr * (0.75 + 0.3 * k))], 2), 6))
    human.head = (x, head_cy, hr)
    human.shoulders = (shL, shR)
    return it


# ------------------------------------------------------------------ animals
def arab_horse(x, feet_y, h, facing=1, body=WHITE, mane=GREY, hoof=GREY, blanket=RED, band=GOLD,
               tassel=YELLOW, name="horse", step=0.0, saddle=True, rein_to=None, deco=True, seat=True):
    """Chunky side-view Arabian horse, (x, feet_y) centre of the hooves, h = height to the back.
    step (0..1) lifts the near front leg for a parade walk. Anchors: arab_horse.seat, .mouth."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    it = []
    lw = h * 0.14

    def leg(top, knee, foot, nm, col):
        a = (foot[0] - knee[0], foot[1] - knee[1])
        L = math.hypot(*a) or 1
        tip = (foot[0] + a[0] / L * h * 0.1, foot[1] + a[1] / L * h * 0.1)
        if nm == "leg-far":
            it.append(R(f"{name}-{nm}", limb([top, knee, foot, tip], lw * 1.25, lw * 0.95), col))
            return
        it.append(R(f"{name}-{nm}", limb([top, knee, foot], lw * 1.25, lw * 0.85), col))
        it.append(R(f"{name}-hoof", limb([foot, tip], lw * 1.0, lw * 1.2, caps=False), hoof))
    # far legs
    leg(P(-0.32, 0.6), P(-0.38, 0.32), P(-0.32, 0.09), "leg-far", body)
    leg(P(0.36, 0.6), P(0.4, 0.32), P(0.38, 0.09), "leg-far", body)
    # tail (high, flowing)
    it.append(R(f"{name}-tail", smooth([P(-0.5, 0.95), P(-0.72, 1.05), P(-0.9, 0.85), P(-0.88, 0.45), P(-0.75, 0.32),
                                        P(-0.76, 0.6), P(-0.68, 0.8), P(-0.52, 0.8)], 2), mane))
    # body
    it.append(R(f"{name}-body", ellipse(*P(0.0, 0.8), h * 0.6, h * 0.27), body))
    # neck and head
    it.append(R(f"{name}-neck", smooth([P(0.22, 0.98), P(0.38, 1.35), P(0.56, 1.52), P(0.8, 1.4), P(0.74, 1.12), P(0.62, 0.62), P(0.36, 0.62)], 2), body))
    it.append(R(f"{name}-head", smooth([P(0.52, 1.5), P(0.64, 1.66), P(0.82, 1.52), P(1.04, 1.26), P(1.02, 1.08), P(0.86, 1.04), P(0.66, 1.22)], 2), body))
    it.append(R(f"{name}-ear", [P(0.58, 1.55), P(0.66, 1.84), P(0.76, 1.55)], body))
    it.append(R(f"{name}-mane", smooth([P(0.26, 1.0), P(0.36, 1.32), P(0.52, 1.56), P(0.66, 1.66), P(0.6, 1.5),
                                        P(0.5, 1.36), P(0.4, 1.0)], 2), mane))
    it.append(INK(ellipse(*P(0.74, 1.42), h * 0.032, h * 0.04)))
    it.append(INK(ellipse(*P(0.97, 1.16), h * 0.022, h * 0.018)))
    it.append(LN(arc(*P(0.92, 1.1), h * 0.06, h * 0.03, 30, 150, 6), 6))
    # near legs
    if step:
        leg(P(0.42, 0.66), P(0.62, 0.42), P(0.55, 0.22), "leg", body)
    else:
        leg(P(0.42, 0.66), P(0.46, 0.32), P(0.44, 0.09), "leg", body)
    leg(P(-0.38, 0.68), P(-0.46, 0.34), P(-0.4, 0.09), "leg", body)
    # bridle
    it.append(R(f"{name}-bridle", limb([P(0.64, 1.58), P(0.76, 1.32), P(0.86, 1.14)], h * 0.05), band))
    if saddle:
        it.append(R(f"{name}-blanket", smooth([P(-0.32, 1.05), P(0.2, 1.05), P(0.24, 0.6), P(-0.36, 0.6)], 1), blanket))
        it.append(R(f"{name}-blanket-band", [P(-0.37, 0.74), P(0.25, 0.74), P(0.25, 0.6), P(-0.37, 0.6)], band))
        for tx in ((-0.27, -0.07) if deco else ()):
            it.append(R(f"{name}-saddle-diamond", [P(tx, 0.98), P(tx + 0.075, 0.87), P(tx, 0.76), P(tx - 0.075, 0.87)], band))
        for tx in ((-0.27, -0.06, 0.15) if deco else ()):
            it.append(R(f"{name}-tassel", smooth([P(tx - 0.07, 0.62), P(tx + 0.07, 0.62), P(tx + 0.05, 0.48), P(tx, 0.42), P(tx - 0.05, 0.48)], 1), tassel))
        if seat:
            it.append(R(f"{name}-saddle", smooth([P(-0.24, 1.12), P(0.12, 1.12), P(0.16, 1.0), P(-0.28, 1.0)], 1), DARK_BROWN))
    arab_horse.mouth = P(0.9, 1.16)
    arab_horse.seat = P(-0.06, 1.06)
    if rein_to:
        it.append(R(f"{name}-rein", limb([P(0.86, 1.16), rein_to], h * 0.035), band))
    return it


def falcon(cx, cy, s, facing=1, body=GREY, back="#607D8B", belly=CREAM, cap=BLACK_CLOTH, feet=YELLOW, name="falcon"):
    """Peregrine falcon taking off, wings raised in a V. (cx, cy) = body centre, s = body height unit.
    Anchors: falcon.feet (between the talons)."""
    f = facing

    def P(px, py):
        return (cx + f * px * s, cy - py * s)
    it = []
    for side in (-1, 1):
        # wing: from shoulder up and out, scalloped trailing edge
        sh = P(side * 0.25, 0.25)
        tip = P(side * 1.55, 1.25)
        wing = [P(side * 0.2, 0.05), P(side * 0.25, 0.32), P(side * 0.6, 0.85), P(side * 1.1, 1.25), tip,
                P(side * 1.38, 0.9), P(side * 1.3, 0.62), P(side * 1.0, 0.38), P(side * 0.7, 0.1), P(side * 0.45, 0.0)]
        it.append(R(f"{name}-wing", smooth(wing, 1), body))
        it.append(R(f"{name}-wing-tips", smooth([P(side * 1.0, 1.08), P(side * 1.1, 1.25), tip, P(side * 1.38, 0.9), P(side * 1.3, 0.62),
                                                 P(side * 1.12, 0.48), P(side * 1.05, 0.75)], 1), back))
        for k in range(3):
            a = P(side * (0.45 + k * 0.17), 0.3 + k * 0.08)
            b = P(side * (0.62 + k * 0.17), 0.62 + k * 0.1)
            it.append(LN([a, b], 6))
    it.append(R(f"{name}-tail", smooth([P(-0.22, -0.4), P(0.22, -0.4), P(0.34, -0.95), P(0.0, -1.05), P(-0.34, -0.95)], 2), back))
    it.append(LN([P(0, -0.55), P(0, -0.95)], 6))
    for side in (-1, 1):
        it.append(R(f"{name}-leg", limb([P(side * 0.16, -0.35), P(side * 0.2, -0.72)], s * 0.16, s * 0.13), feet))
        fx, fy = P(side * 0.2, -0.78)
        it.append(R(f"{name}-talon", smooth([(fx - s * 0.17, fy - s * 0.06), (fx + s * 0.17, fy - s * 0.06),
                                             (fx + s * 0.2, fy + s * 0.1), (fx - s * 0.2, fy + s * 0.1)], 2), feet))
    it.append(R(f"{name}-body", smooth([P(-0.42, 0.3), P(0.0, 0.5), P(0.42, 0.3), P(0.44, -0.2), P(0.0, -0.55), P(-0.44, -0.2)], 2), body))
    it.append(R(f"{name}-belly", smooth([P(-0.28, 0.25), P(0.28, 0.25), P(0.32, -0.15), P(0.0, -0.46), P(-0.32, -0.15)], 2), belly))
    for k in range(3):
        for sx in (-1, 1):
            bx, by = P(sx * 0.13, 0.05 - k * 0.15)
            it.append(LN(arc(bx, by, s * 0.07, s * 0.045, 20, 160, 6), 6))
    # head, turned in profile towards `facing`
    hx, hy = P(0.02, 0.72)
    it.append(R(f"{name}-head", circle(hx, hy, s * 0.36), belly))
    it.append(R(f"{name}-hood", smooth([P(-0.36, 0.6), P(-0.3, 0.98), P(0.05, 1.1), P(0.32, 0.96), P(0.36, 0.78), P(0.18, 0.8),
                                        P(0.1, 0.6), P(0.06, 0.4), P(-0.12, 0.38), P(-0.3, 0.45)], 2), cap))
    it.append(R(f"{name}-eye-ring", circle(*P(0.18, 0.76), s * 0.14), YELLOW))
    it.append(INK(circle(*P(0.2, 0.76), s * 0.07)))
    it.append(R(f"{name}-beak", smooth([P(0.28, 0.7), P(0.52, 0.7), P(0.62, 0.56), P(0.52, 0.42), P(0.47, 0.54), P(0.28, 0.54)], 1), YELLOW))
    falcon.feet = P(0.0, -0.84)
    return it


def saluki(x, feet_y, h, facing=1, body=CREAM, ear=DUNE, name="saluki"):
    """Slim desert hound (saluki), side view, standing alert. h = height to the top of the head."""
    f = facing

    def P(px, py):
        return (x + f * px * h, feet_y - py * h)
    it = []
    lw = h * 0.1
    # far legs
    it.append(R(f"{name}-leg-far", limb([P(-0.36, 0.5), P(-0.46, 0.28), P(-0.4, 0.04)], lw, lw * 0.8), ear))
    it.append(R(f"{name}-leg-far", limb([P(0.2, 0.5), P(0.24, 0.26), P(0.22, 0.04)], lw, lw * 0.8), ear))
    # curled feathered tail
    it.append(R(f"{name}-tail", limb(smooth_open([P(-0.46, 0.58), P(-0.66, 0.5), P(-0.72, 0.3), P(-0.62, 0.18), P(-0.5, 0.24)], 2), lw * 1.1, lw * 0.8), ear))
    # body: deep chest, tucked waist
    it.append(R(f"{name}-body", smooth([P(-0.5, 0.56), P(-0.42, 0.7), P(-0.05, 0.66), P(0.28, 0.74), P(0.36, 0.6), P(0.28, 0.36),
                                        P(0.08, 0.36), P(-0.18, 0.5), P(-0.46, 0.44)], 2), body))
    it.append(R(f"{name}-neck", smooth([P(0.18, 0.66), P(0.3, 0.92), P(0.46, 0.94), P(0.4, 0.58)], 2), body))
    it.append(R(f"{name}-head", smooth([P(0.3, 0.94), P(0.42, 1.03), P(0.56, 0.99), P(0.84, 0.88), P(0.82, 0.83), P(0.52, 0.8), P(0.36, 0.84)], 2), body))
    it.append(INK(circle(*P(0.5, 0.92), h * 0.022)))
    it.append(INK(circle(*P(0.82, 0.86), h * 0.022)))
    it.append(R(f"{name}-ear", smooth([P(0.4, 0.98), P(0.33, 0.95), P(0.28, 0.76), P(0.33, 0.72), P(0.4, 0.78), P(0.44, 0.92)], 2), ear))
    # near legs
    it.append(R(f"{name}-leg", limb([P(-0.42, 0.52), P(-0.52, 0.28), P(-0.46, 0.04)], lw * 1.25, lw * 0.85), body))
    it.append(R(f"{name}-leg", limb([P(0.27, 0.5), P(0.3, 0.26), P(0.28, 0.04)], lw * 1.2, lw * 0.85), body))
    return it


# ------------------------------------------------------------------ props
def dallah(cx, base_y, h, body=GOLD, band=ORANGE, name="dallah", tilt=0, facing=1):
    """Arabic coffee pot, side view, spout towards `facing`. (cx, base_y) = bottom centre, h = height.
    tilt rotates around the base (degrees, positive = clockwise). Anchors: dallah.spout, .handle, .belly."""
    def P(px, py):
        return (cx + facing * px * h, base_y - py * h)

    def solid(profile):
        right = [P(w, y) for y, w in profile]
        left = [P(-w, y) for y, w in reversed(profile)]
        return smooth(right + left, 2)
    it = []
    it.append(R(f"{name}-handle", limb(smooth_open([P(-0.14, 0.64), P(-0.42, 0.62), P(-0.46, 0.4), P(-0.28, 0.16)], 2), h * 0.065), body))
    it.append(R(f"{name}-spout", limb(smooth_open([P(0.2, 0.2), P(0.38, 0.3), P(0.48, 0.5), P(0.56, 0.72)], 2), h * 0.16, h * 0.075), body))
    it.append(R(f"{name}-bulb", solid([(0.0, 0.25), (0.06, 0.31), (0.2, 0.34), (0.34, 0.27), (0.43, 0.15)]), body))
    it.append(R(f"{name}-waist", solid([(0.41, 0.16), (0.5, 0.11), (0.53, 0.12)]), band))
    it.append(R(f"{name}-neck", solid([(0.52, 0.12), (0.6, 0.18), (0.68, 0.2), (0.72, 0.16)]), body))
    it.append(R(f"{name}-lid", solid([(0.71, 0.17), (0.76, 0.15), (0.86, 0.08), (0.96, 0.03)]), band))
    it.append(R(f"{name}-finial", circle(*P(0, 1.0), max(h * 0.07, 30)), body))
    it.append(LN(arc(*P(0, 0.12), h * 0.27, h * 0.05, 15, 165, 10), 6))
    fn = lambda p: rotate([p], tilt, cx, base_y)[0]
    out = _xf(it, fn) if tilt else it
    dallah.spout = fn(P(0.57, 0.76))
    dallah.handle = fn(P(-0.46, 0.42))
    dallah.belly = fn(P(0.0, 0.2))
    return out


def finjan(cx, cy, s, col=WHITE, name="cup"):
    """Small handleless coffee cup, (cx, cy) centre of the rim, s = rim width."""
    return [R(name, smooth([(cx - s / 2, cy), (cx + s / 2, cy), (cx + s * 0.32, cy + s * 0.7), (cx - s * 0.32, cy + s * 0.7)], 1), col)]


def wheel(cx, cy, r, tyre=BLACK_CLOTH, hub=GREY, name="wheel", spokes=0, hub_frac=0.55):
    it = [R(f"{name}-tyre", circle(cx, cy, r), tyre)]
    if r * hub_frac >= 30:
        it.append(R(f"{name}-hub", circle(cx, cy, r * hub_frac), hub))
    if r * hub_frac * 0.5 >= 28:
        it.append(R(f"{name}-cap", circle(cx, cy, r * hub_frac * 0.5), YELLOW))
    for k in range(spokes):
        a = math.radians(360 * k / spokes + 20)
        it.append(LN([(cx + math.cos(a) * r * hub_frac * 0.45, cy + math.sin(a) * r * hub_frac * 0.45),
                      (cx + math.cos(a) * r * hub_frac * 0.92, cy + math.sin(a) * r * hub_frac * 0.92)], 6))
    return it


def bush(cx, base_y, w, col=GREEN, name="bush"):
    ctrl = [(-0.5, 0), (-0.5, -0.3), (-0.3, -0.55), (0, -0.62), (0.3, -0.55), (0.5, -0.3), (0.5, 0)]
    return [R(name, smooth([(cx + dx * w, base_y + dy * w) for dx, dy in ctrl], 3), col)]


def rock(cx, base_y, w, hgt, col=ROCK, name="rock", seed=0):
    import random
    rnd = random.Random(seed)
    pts = [(cx - w / 2, base_y)]
    n = 7
    for k in range(n + 1):
        t = math.pi * k / n
        rr = 1 + rnd.uniform(-0.12, 0.12)
        pts.append((cx - math.cos(t) * w / 2 * rr, base_y - math.sin(t) * hgt * rr))
    pts.append((cx + w / 2, base_y))
    return [R(name, smooth(pts, 2), col)]


def fat_palm(x, base_y, h, lean=0.06, trunk=TRUNK, leaf=LEAF, dates=ORANGE, name="palm"):
    """Date palm with chunky leaves (no slivers). lean > 0 bends the top to the right."""
    it = []
    top = (x + h * lean, base_y - h)
    tw = h * 0.075
    it.append(R(f"{name}-trunk", smooth([(x - tw, base_y), (x + tw, base_y), (top[0] + tw * 0.6, top[1] + h * 0.05),
                                         (top[0] - tw * 0.6, top[1] + h * 0.05)], 1), trunk))
    for i in range(1, 5):
        t = i / 5
        cx = x + (top[0] - x) * t
        yy = base_y - h * t
        w = tw * (1 - 0.4 * t) * 0.9
        it.append(LN(arc(cx, yy - h * 0.02, w, h * 0.02, 20, 160, 6), 6))
    for ang, ln_ in ((200, 0.5), (240, 0.42), (300, 0.42), (340, 0.5), (160, 0.38), (20, 0.38)):
        a = math.radians(ang)
        L = h * ln_
        tip = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.55 + L * 0.35)
        mid = (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 * 0.9 - h * 0.02)
        it.append(R(f"{name}-leaf", limb(smooth_open([top, mid, tip], 2), h * 0.13, h * 0.035), leaf))
    it.append(R(f"{name}-crown", circle(top[0], top[1] + h * 0.01, h * 0.07), leaf))
    if dates:
        for dx in (-1, 1):
            it.append(R(f"{name}-dates", ellipse(top[0] + dx * h * 0.085, top[1] + h * 0.12, h * 0.06, h * 0.08, rot=-dx * 20), dates))
    return it


def _xf(items, fn):
    out = []
    for item in items:
        if item[0] == "region":
            out.append(("region", item[1], [fn(p) for p in item[2]], item[3]))
        else:
            out.append((item[0], [fn(p) for p in item[1]], *item[2:]))
    return out


def buggy(x, ground_y, L, facing=1, body=RED, trim=YELLOW, cage=BLACK_CLOTH, tyre=BLACK_CLOTH, hub=GREY,
          driver_helmet=None, visor=BLUE, tilt=0, name="buggy", seat=BLACK_CLOTH):
    """Desert dune buggy, side view. (x, ground_y) = point under the middle, L = length.
    driver_helmet: colour of a helmeted driver sitting inside (None = empty seat)."""
    def P(px, py):
        return (x + px * L, ground_y - py * L)
    it = []
    r = L * 0.155
    # cage (behind body)
    it.append(R(f"{name}-cage", limb([P(-0.24, 0.36), P(-0.17, 0.72), P(0.1, 0.72), P(0.3, 0.38)], L * 0.04), cage))
    it.append(R(f"{name}-spoiler-leg", limb([P(-0.42, 0.4), P(-0.44, 0.55)], L * 0.07, caps=False), cage))
    it.append(R(f"{name}-spoiler", smooth([P(-0.56, 0.6), P(-0.34, 0.6), P(-0.36, 0.53), P(-0.55, 0.52)], 1), trim))
    it.append(R(f"{name}-seat", smooth([P(-0.2, 0.36), P(-0.17, 0.62), P(-0.08, 0.62), P(-0.08, 0.36)], 1), seat))
    if driver_helmet:
        it.append(R(f"{name}-driver-arm", limb([P(-0.05, 0.44), P(0.1, 0.42), P(0.17, 0.48)], L * 0.06), BLACK_CLOTH))
        it.append(R(f"{name}-helmet", circle(*P(-0.06, 0.6), L * 0.1), driver_helmet))
        it.append(R(f"{name}-visor", smooth([P(-0.03, 0.66), P(0.05, 0.65), P(0.05, 0.54), P(-0.03, 0.55)], 1), visor))
    # body
    it.append(R(f"{name}-body", smooth([P(-0.5, 0.18), P(-0.5, 0.44), P(-0.22, 0.44), P(-0.18, 0.36), P(0.16, 0.36),
                                        P(0.22, 0.4), P(0.5, 0.33), P(0.53, 0.2), P(0.3, 0.12), P(-0.3, 0.12)], 1), body))
    it.append(R(f"{name}-stripe", [P(-0.49, 0.32), P(0.5, 0.29), P(0.51, 0.24), P(-0.5, 0.26)], trim))
    it.append(R(f"{name}-roundel", circle(*P(0.0, 0.215), L * 0.05), WHITE))
    it.append(R(f"{name}-light", ellipse(*P(0.44, 0.36), L * 0.055, L * 0.04), YELLOW))
    it.append(R(f"{name}-bumper", limb([P(0.5, 0.1), P(0.59, 0.18), P(0.56, 0.32)], L * 0.045), cage))
    # wheels
    for wx in (-0.32, 0.32):
        it += wheel(*P(wx, r / L), r, tyre=tyre, hub=hub, name=f"{name}-wheel", spokes=0, hub_frac=0.5)
    fn = (lambda p: (2 * x - p[0], p[1])) if facing < 0 else (lambda p: p)
    it = _xf(it, fn)
    if tilt:
        it = _xf(it, lambda p: rotate([p], tilt, x, ground_y - L * 0.25)[0])
    return it


def dust(cx, cy, w, col=CREAM, name="dust"):
    ctrl = [(-0.5, 0.1), (-0.45, -0.2), (-0.25, -0.35), (0.0, -0.3), (0.2, -0.45), (0.42, -0.3), (0.5, 0.0), (0.3, 0.2), (-0.2, 0.22)]
    return [R(name, smooth([(cx + dx * w, cy + dy * w) for dx, dy in ctrl], 3), col)]


def rally_car(x, ground_y, L, facing=1, body=GREEN, trim=WHITE, window=SKY, tilt=0, name="car"):
    """Boxy rally 4x4, side view."""
    def P(px, py):
        return (x + px * L, ground_y - py * L)
    it = []
    r = L * 0.14
    it.append(R(f"{name}-body", smooth([P(-0.5, 0.14), P(-0.5, 0.42), P(-0.34, 0.44), P(-0.28, 0.66), P(0.16, 0.66), P(0.28, 0.44),
                                        P(0.5, 0.4), P(0.52, 0.16), P(0.3, 0.12), P(-0.3, 0.12)], 1), body))
    it.append(R(f"{name}-window", [P(-0.24, 0.6), P(-0.04, 0.6), P(-0.04, 0.45), P(-0.29, 0.45)], window))
    it.append(R(f"{name}-window", [P(0.02, 0.6), P(0.14, 0.6), P(0.22, 0.45), P(0.02, 0.45)], window))
    it.append(R(f"{name}-stripe", [P(-0.5, 0.34), P(0.51, 0.31), P(0.51, 0.25), P(-0.5, 0.27)], trim))
    it.append(R(f"{name}-roof-lights", rect(*P(-0.22, 0.73), *P(0.1, 0.66)), YELLOW))
    for wx in (-0.3, 0.3):
        it += wheel(*P(wx, r / L), r, name=f"{name}-wheel", hub_frac=0.5)
    fn = (lambda p: (2 * x - p[0], p[1])) if facing < 0 else (lambda p: p)
    it = _xf(it, fn)
    if tilt:
        it = _xf(it, lambda p: rotate([p], tilt, x, ground_y - L * 0.3)[0])
    return it

"""Wheat and peach farms of Hail: a farmer in overalls and cap driving his tractor with peach baskets (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

PEACH = "#FFAB76"

s = Scene()
s.add("sky", rect(0, 0, W, 800), SKY)
s.add("sun", circle(260, 180, 110), SUN)
s.extend(cloud(1000, 170, 380, "cloud"))
s.extend(cloud(1650, 120, 280, "cloud2"))
s.add("mountain", [(-20, 760)] + smooth_open([(-20, 640), (300, 560), (560, 620), (900, 520), (1300, 610), (1650, 540), (2070, 600)], 2) + [(2070, 760)], ROCK)
# green centre-pivot circles on the plain
s.add("plain", rect(0, 640, W, 900), GRASS)
for cx, col in ((300, LEAF), (900, GOLD), (1500, LEAF)):
    s.add("pivot-field", ellipse(cx, 720, 260, 55), col)
# golden wheat field
s.add("wheat-field", [(-20, 1000)] + smooth_open([(-20, 830), (700, 800), (1400, 840), (2070, 810)], 2) + [(2070, 1000)], GOLD)
for k in range(9):
    x0 = 60 + k * 230
    s.line(smooth_open([(x0, 960), (x0 + 10, 900), (x0 + 30, 860)], 2), 6)
# farm track
s.add("track", [(-20, 1560), (-20, 980)] + smooth_open([(-20, 980), (800, 960), (2070, 990)], 2) + [(2070, 1560)], DUNE)

# peach tree on the right
s.add("tree-trunk", smooth([(1640, 1180), (1670, 900), (1630, 760), (1720, 760), (1730, 900), (1750, 1180)], 1), BROWN)
s.add("tree-crown", smooth([(1430, 820), (1470, 620), (1630, 500), (1820, 520), (1940, 640), (1940, 820), (1780, 900), (1570, 900)], 3), LEAF)
for px, py in ((1520, 700), (1630, 610), (1760, 600), (1860, 700), (1570, 820), (1720, 760), (1860, 815)):
    s.add("peach", circle(px, py, 36), PEACH)

# girl with a basket of peaches
s.add("small-basket-handle", limb(arc(1660, 1260, 95, 120, 190, 350, 12), 22), BROWN)
for k, px in enumerate((1600, 1660, 1720)):
    s.add("basket-peach", circle(px, 1250 - (15 if k == 1 else 0), 36), PEACH)
s.add("small-basket", smooth([(1560, 1260), (1760, 1260), (1735, 1380), (1585, 1380)], 1), BROWN)
s.extend(human(1840, 1480, 640, name="girl", facing=-1, outfit="hoodie", top=PINK, bottom=BLUE, accent=PURPLE,
               shoes=WHITE, head="headscarf", head_col=PURPLE, hands=((1690, 1150), (1960, 1110))))
s.add("girl-peach", circle(1960, 1050, 44), PEACH)
s.add("girl-hand", circle(1960, 1110, 32), SKIN)

# trailer with peach baskets
s.add("trailer-wheel", circle(310, 1300, 105), BLACK_CLOTH)
s.add("trailer-hub", circle(310, 1300, 48), GREY)
s.add("hitch", limb([(540, 1230), (640, 1240)], 30), GREY)
for bx in (110, 260, 410):
    s.add("basket", smooth([(bx - 75, 1080), (bx + 75, 1080), (bx + 60, 1180), (bx - 60, 1180)], 1), BROWN)
    s.line([(bx - 65, 1130), (bx + 65, 1130)], 6)
    for k, px in enumerate((bx - 40, bx, bx + 40)):
        s.add("peach", circle(px, 1062 - (14 if k == 1 else 0), 36), PEACH)
s.add("trailer", rect(40, 1170, 560, 1250), YELLOW)

# the tractor
s.add("exhaust", rect(1220, 780, 1260, 1010), GREY)
s.add("exhaust-cap", rect(1200, 750, 1280, 795), BLACK_CLOTH)
s.add("hood", smooth([(880, 1240), (870, 1010), (920, 970), (1420, 990), (1480, 1050), (1490, 1240)], 1), RED)
s.add("grille", rect(1440, 1040, 1500, 1220), GREY)
s.add("headlight", ellipse(1440, 1015, 32, 26), YELLOW)
s.add("stripe", rect(900, 1080, 1430, 1120), WHITE)
s.add("front-wheel", circle(1380, 1340, 135), BLACK_CLOTH)
s.add("front-hub", circle(1380, 1340, 62), YELLOW)
s.add("rear-wheel", circle(740, 1230, 250), BLACK_CLOTH)
s.add("rear-hub", circle(740, 1230, 130), YELLOW)
s.add("rear-cap", circle(740, 1230, 50), RED)
for k in range(8):
    import math as _m
    a = _m.radians(k * 45)
    s.line([(740 + _m.cos(a) * 140, 1230 + _m.sin(a) * 140), (740 + _m.cos(a) * 235, 1230 + _m.sin(a) * 235)], 10)
s.add("fender", limb(arc(740, 1230, 280, 280, 190, 350, 20), 64), RED)
s.add("seat", smooth([(560, 960), (580, 780), (660, 780), (690, 960)], 1), BLACK_CLOTH)
s.add("steering-column", limb([(895, 1010), (930, 870)], 52), GREY)

# the hero farmer in overalls and cap, driving
fx, seat_y, fh = 760, 950, 800
s.extend(human(fx, seat_y + 0.44 * fh, fh, name="farmer", adult=True, facing=1, outfit="overalls", top=WHITE, bottom=BLUE, accent=BLUE,
               head="cap", head_col=LEAF, shoes=BROWN, seated_y=seat_y, beard=None,
               feet=((fx, seat_y - 60), (960, 1180)), knees=((fx, seat_y - 40), (930, 960)), hands=((880, 860), (990, 845))))
s.add("steering-wheel", ellipse(935, 865, 85, 26, rot=-15), BLACK_CLOTH)
s.add("farmer-hand", circle(870, 865, 40), SKIN)
s.add("farmer-hand", circle(1000, 845, 40), SKIN)
s.build(__file__)

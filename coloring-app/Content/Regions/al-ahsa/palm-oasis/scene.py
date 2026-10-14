"""A date farmer climbs a palm in the Al-Ahsa oasis while a boy waits with a basket (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(sun(260, 230, 120))
s.extend(cloud(760, 250, 380))
s.extend(cloud(1800, 170, 300, name="cloud2"))
# distant palm grove along the horizon
s.add("far-field", smooth([(0, 900), (0, 820), (600, 790), (1300, 830), (W, 800), (W, 900)], 2), GRASS)
for i, (px, ph) in enumerate(((90, 360), (640, 410), (1690, 330), (1930, 400))):
    s.extend(distant_palm(px, 870 + (i % 2) * 15, ph, name=f"farpalm{i}"))
s.add("field", rect(0, 860, W, H), GRASS)
# irrigation channel winding through the farm
s.add("channel", smooth([(0, 1010), (500, 960), (1000, 1000), (1500, 950), (W, 980), (W, 1060), (1500, 1030),
                         (1000, 1080), (500, 1040), (0, 1090)], 2), SEA)
s.add("path", smooth([(0, 1290), (700, 1250), (1100, 1330), (W, 1290), (W, H), (0, H)], 2), SAND)
# a second palm on the left, behind the boy
s.extend(big_palm(330, 1250, 380, lean=-30, w=95, span=0.8, n_leaves=6, name="palm-left"))
s.extend(date_bunch(315, 410, 150, 180, name="dates-left"))
# hero palm
s.extend(big_palm(1250, 1470, 250, lean=40, w=170, span=1.25, n_leaves=8, name="palm"))
s.extend(date_bunch(1180, 300, 150, 190, name="dates-a"))
s.extend(date_bunch(1460, 320, 170, 210, name="dates-b"))
# the farmer, climbing: one hand grips the trunk, the other picks dates
fx, ffeet, fh = 1270, 1150, 700
items, info = figure(fx, ffeet, fh, "thobe", "wrap", skin=SKIN2, beard=DARK_BROWN, legs=False,
                     lhand=[(1180, 560), (1250, 455)], rhand=[(1400, 580), (1450, 480)], name="farmer")
hem = info["hem"]
# legs gripping the trunk (white sirwal under the hitched thobe)
s.add("farmer-leg", thick([(fx - 45, hem - 30), (fx - 120, hem + 30), (fx - 95, hem + 120)], 62, 56), WHITE)
s.add("farmer-leg", thick([(fx + 45, hem - 30), (fx + 110, hem + 60), (fx + 95, hem + 170)], 62, 56), WHITE)
s.extend(items)
s.add("farmer-shoe", ellipse(fx - 80, hem + 140, 58, 30, rot=-15), DARK_BROWN)
s.add("farmer-shoe", ellipse(fx + 115, hem + 190, 58, 30, rot=15), DARK_BROWN)
wy = info["waist"]
s.add("climbing-belt", smooth([(fx - 185, wy - 40), (fx, wy + 10), (fx + 185, wy - 40), (fx + 185, wy + 15), (fx, wy + 65), (fx - 185, wy + 15)], 2), BROWN)
s.line(smooth_open([(fx - 130, wy - 6), (fx, wy + 36), (fx + 130, wy - 6)], 2), 5)
# basket hanging from the belt
s.line([(fx - 170, wy), (fx - 250, wy + 110)], 8)
s.line([(fx - 170, wy), (fx - 330, wy + 110)], 8)
s.extend(basket(fx - 290, wy + 110, 210, 150, name="farmer-basket", handle=False))
s.add("farmer-basket-dates", smooth([(fx - 395, wy + 112), (fx - 360, wy + 60), (fx - 290, wy + 45), (fx - 220, wy + 60), (fx - 185, wy + 112)], 2), ORANGE)
# boy below holding up a basket
items, binfo = figure(720, 1450, 560, "thobe", "taqiyah", child=True, look=0.4,
                      lhand=[(560, 960), (630, 835)], rhand=[(880, 960), (810, 835)], name="boy")
s.extend(items)
s.extend(basket(720, 690, 270, 160, name="boy-basket", handle=False))
s.add("boy-basket-dates", smooth([(605, 692), (650, 630), (720, 612), (790, 630), (835, 692)], 2), ORANGE)
# full basket of dates on the ground
s.extend(basket(1680, 1300, 300, 190, name="ground-basket", handle=False))
s.add("ground-dates", smooth([(1545, 1302), (1590, 1225), (1680, 1200), (1770, 1225), (1815, 1302)], 2), ORANGE)
for dx in (-70, 0, 70):
    s.line(arc(1680 + dx, 1262 - abs(dx) * 0.3, 14, 18, 100, 260, 6), 5)
s.build(__file__)

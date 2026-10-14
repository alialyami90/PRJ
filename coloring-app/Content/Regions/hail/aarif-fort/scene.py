"""Aarif Fort on the hill above the old town: a boy in thobe and shemagh ringing the fort bell (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1300), SKY)
s.extend(sun(1880, 170, 95))
s.extend(cloud(620, 200, 380, "cloud"))
s.extend(cloud(1180, 110, 260, "cloud2"))

# rocky hill
s.add("hill", smooth([(780, 1150), (900, 900), (1040, 700), (1150, 610), (1500, 590), (1820, 610), (1960, 720), (2100, 860), (2100, 1150)], 2), ROCK)
s.line(smooth_open([(1850, 760), (1930, 840)], 1), 6)

# the fort
FX0, FX1, FTOP, FBOT = 1260, 1820, 400, 650
s.add("fort-wall", rect(FX0, FTOP, FX1, FBOT), MUD)
for k in range(5):
    tx = FX0 + 90 + k * 92
    s.add("crenel", [(tx, FTOP + 2), (tx + 84, FTOP + 2), (tx + 42, FTOP - 70)], MUD)
s.add("fort-gate", arch(1560, 500, 1660, FBOT), DARK_BROWN)
s.line([(1610, 552), (1610, FBOT)], 6)
for wx in (1380, 1730):
    s.ink([(wx - 22, 520), (wx + 22, 520), (wx, 480)])
# tall watch tower
s.add("tower", [(1150, FBOT), (1180, 190), (1340, 190), (1370, FBOT)], SAND)
for k in range(2):
    tx = 1180 + k * 80
    s.add("tower-crenel", [(tx, 192), (tx + 80, 192), (tx + 40, 115)], SAND)
for wy in (300, 430):
    s.ink([(1238, wy + 40), (1282, wy + 40), (1260, wy)])
s.add("tower-door", arch(1225, 530, 1295, FBOT), DARK_BROWN)
# flag pole with a plain green flag
s.add("flag-pole", rect(1244, 40, 1276, 135), DARK_BROWN)
s.add("flag", smooth([(1267, 45), (1390, 60), (1360, 85), (1390, 115), (1267, 110)], 1), LEAF)

# old town at the foot of the hill
houses = [(860, 990, 1080, 1180), (1060, 930, 1300, 1180), (1290, 990, 1500, 1180), (1480, 900, 1760, 1180), (1740, 970, 1960, 1180), (1940, 920, 2060, 1180)]
for i, (x0, y0, x1, y1) in enumerate(houses):
    col = SAND if i % 2 else MUD
    s.add("house", rect(x0, y0, x1, y1), col)
    s.line([(x0 + 10, y0 + 30), (x1 - 10, y0 + 30)], 6)
    if x1 - x0 > 200:
        if not (1150 < (x0 + x1) / 2 < 1450):
            s.add("house-door", arch((x0 + x1) / 2 - 40, y1 - 140, (x0 + x1) / 2 + 40, y1), DARK_BROWN)
s.extend(fat_palm(1880, 1180, 420, name="palm"))

s.add("ground", [(-20, 1170)] + smooth_open([(-20, 1170), (600, 1120), (1200, 1180), (2070, 1150)], 2) + [(2070, 1560), (-20, 1560)], SAND)
s.add("path", smooth_open([(1020, 1560), (1100, 1330), (1190, 1190)], 2) + smooth_open([(1270, 1190), (1330, 1330), (1580, 1560)], 2), DUNE)

# birds startled by the bell
for bx, by, k in ((900, 300, 1.0), (1010, 240, 0.8), (780, 220, 0.7)):
    s.line(smooth_open([(bx - 50 * k, by - 10 * k), (bx - 20 * k, by - 25 * k), (bx, by)], 2), 8)
    s.line(smooth_open([(bx, by), (bx + 20 * k, by - 25 * k), (bx + 50 * k, by - 10 * k)], 2), 8)

# bell frame
s.add("post", rect(150, 360, 215, 1290), TRUNK)
s.add("post", rect(705, 360, 770, 1290), TRUNK)
s.add("beam", rect(110, 320, 810, 395), TRUNK)
s.add("beam-cap", rect(90, 290, 830, 330), DARK_BROWN)
s.add("post-foot", rect(120, 1270, 245, 1320), DARK_BROWN)
s.add("post-foot", rect(675, 1270, 800, 1320), DARK_BROWN)
# the bell
BX, BY = 460, 395
s.add("bell-hanger", rect(BX - 35, BY, BX + 35, BY + 55), DARK_BROWN)
s.add("bell", smooth([(BX - 80, BY + 60), (BX - 50, BY + 30), (BX + 50, BY + 30), (BX + 80, BY + 60), (BX + 100, BY + 200),
                      (BX + 150, BY + 260), (BX - 150, BY + 260), (BX - 100, BY + 200)], 2), GOLD)
s.add("bell-rim", smooth([(BX - 160, BY + 240), (BX + 160, BY + 240), (BX + 160, BY + 290), (BX - 160, BY + 290)], 1), ORANGE)
s.line(smooth_open([(BX - 85, BY + 140), (BX, BY + 155), (BX + 85, BY + 140)], 2), 6)
s.add("clapper", circle(BX + 20, BY + 315, 38), DARK_BROWN)
# ring lines
for k in range(2):
    for sgn in (-1, 1):
        a0, a1 = (330, 380) if sgn > 0 else (160, 210)
        s.line(arc(BX, BY + 140, 185 + k * 45, 150 + k * 45, a0, a1, 8), 8)
# rope from the clapper to the boy's hands
s.add("rope", limb(smooth_open([(BX + 30, BY + 330), (600, 860), (680, 980), (670, 1110)], 2), 30), TRUNK)

# little sister covering her ears and laughing
sx, sfeet, sh_ = 1330, 1470, 560
hr = 0.135 * sh_
hcy = sfeet - sh_ + hr * 1.05
s.extend(human(sx, sfeet, sh_, name="sister", outfit="thobe", top=PINK, head="headscarf", head_col=PURPLE, hem_col=GOLD,
               shoes=RED, facing=-1, mouth="open", hand_r=34,
               hands=((sx - hr * 1.15, hcy + hr * 0.1), (sx + hr * 1.15, hcy + hr * 0.1))))

# the hero: boy in thobe and red shemagh pulling the bell rope with one hand, cheering with the other
s.extend(human(880, 1480, 820, name="boy", outfit="thobe", top=WHITE, head="shemagh", head_col=RED,
               shoes=DARK_BROWN, facing=-1, mouth="open", hands=((672, 960), (1080, 780))))
s.build(__file__)

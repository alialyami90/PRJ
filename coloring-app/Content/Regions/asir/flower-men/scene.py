"""Flower-men of Rijal Almaa in herb crowns walking a mountain path (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.add("sun", circle(1840, 170, 92), YELLOW)
s.extend(puff(330, 170, 380, name="cloud"))
s.extend(mountains([(0, 560), (300, 330), (640, 520), (980, 300), (1400, 500), (1750, 280), (2048, 450)], 1000, LEAF, "far-mountain"))
# Rijal Almaa village on the hill
s.extend(mountains([(-100, 760), (500, 640), (1100, 700), (1600, 600), (2148, 680)], 1100, GRASS, "hill"))
s.extend(tower_house(1500, 700, 160, 300, wall=ROCK, name="tower1", floors=2))
s.extend(tower_house(1700, 690, 200, 400, wall=ROCK, name="tower2", floors=2))
# path winding up
s.add("ground", smooth([(-400, 1060), (500, 960), (1100, 1010), (1600, 940), (2450, 1000), (2450, H + 400), (-400, H + 400)], 3), GRASS)
s.add("path", smooth([(380, H + 40), (520, 1150), (900, 960), (1250, 850), (1450, 760), (1560, 700), (1640, 705), (1520, 790), (1330, 920), (1050, 1080), (950, 1250), (1250, H + 40)], 2), SAND)
for (px, py, r) in ((600, 1420, 60), (1500, 1450, 70), (1200, 900, 40)):
    pass
s.extend(juniper(160, 1060, 420, name="juniper1"))
# flowers by the path
for i, (fx, fy, c) in enumerate(((1890, 1420, ORANGE),)):
    s.add("leaves", bumpy(fx, fy + 55, 85, 45, bumps=6, depth=0.2), LEAF)
    s.extend(flower(fx, fy, 48, c, "path-flower"))

# boy with a flower basket, waving (supporting)
s.extend(figure(1700, 1340, 600, facing=-1, child=True, top=WHITE, jacket=BLUE, bottom="wrap", bottom_colour=GREEN, head="crown", head_colour=(YELLOW, PINK, ORANGE), arms=((0.16, -0.24), (0.1, 0.3)),
                elbows=((0.18, -0.02), None), shoes=DARK_BROWN, name="boy"))
bx, by = figure.hands[1]
s.extend(basket(bx + 10, by + 150, 170, 120, colour=STRAW, band=None, name="flower-basket", handle=True))
s.add("basket-flowers", bumpy(bx + 10, by + 35, 80, 30, bumps=6, depth=0.25), PINK)
s.add("boy-hand", circle(bx, by, 30), SKIN)

# second flower-man waving
s.extend(figure(1250, 1390, 780, facing=-1, top=WHITE, jacket=GREEN, bottom="wrap", bottom_colour=RED,
                belt=BROWN, head="crown", head_colour=(ORANGE, YELLOW, PINK), beard=True, arms=((0.06, 0.36), (0.12, -0.3)),
                elbows=(None, (0.16, -0.06)), name="man2"))

# hero flower-man holding a bunch of marigolds
s.extend(figure(700, 1490, 900, facing=1, top=WHITE, jacket=RED, jacket_trim=YELLOW, bottom="wrap", bottom_colour=BLUE, bands=(ORANGE,),
                belt=BROWN, buckle=True, head="crown", head_colour=(YELLOW, ORANGE, PINK), beard=True, arms=((0.06, 0.36), (0.2, -0.05)),
                elbows=(None, (0.18, 0.12)), name="man1"))
hx, hy = figure.hands[1]
s.add("bouquet-leaves", bumpy(hx - 5, hy - 110, 105, 80, bumps=7, depth=0.2), LEAF)
for k, (dx, dy, c) in enumerate(((-30, -150, YELLOW), (55, -120, ORANGE), (-70, -95, PINK))):
    s.extend(flower(hx + dx, hy + dy, 52, c, "bouquet-flower"))
s.add("hand-front", circle(hx, hy, 900 * 0.045), SKIN)
s.build(__file__)

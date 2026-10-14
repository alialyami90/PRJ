"""Grandmother and girl painting Al-Qatt Al-Asiri patterns on a wall (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
WALL = CREAM
s.add("wall", rect(0, 0, W, 1260), WALL)
# --- top border: stripes then a row of triangles (finished part of the pattern)
s.add("stripe", rect(0, 40, W, 95), RED)
s.add("stripe", rect(0, 95, W, 150), YELLOW)
s.add("stripe", rect(0, 150, W, 205), GREEN)
n = 9
tw = W / n
for i in range(n):
    x0 = i * tw
    s.add("triangle", [(x0, 380), (x0 + tw / 2, 215), (x0 + tw, 380)], (BLUE, RED, PURPLE)[i % 3])
s.add("stripe", rect(0, 380, W, 425), NIGHT)
# --- window with a painted frame (zigzag border)
wx0, wy0, wx1, wy1 = 560, 520, 900, 880
s.add("window-frame", rect(wx0 - 70, wy0 - 70, wx1 + 70, wy1 + 70), YELLOW)
zz = [(wx0 - 70, wy0 - 70)]
for k in range(5):
    zz += [(wx0 - 70 + (k + 0.5) * (wx1 - wx0 + 140) / 5, wy0 - 10), (wx0 - 70 + (k + 1) * (wx1 - wx0 + 140) / 5, wy0 - 70)]
s.add("window-zigzag", zz, RED)
s.add("window", rect(wx0, wy0, wx1, wy1), SKY)
s.add("window-hill", smooth([(wx0, wy1), (wx0, 760), (680, 700), (800, 770), (wx1, 740), (wx1, wy1)], 1), GREEN)
s.add("window-sun", circle(810, 620, 50), YELLOW)
s.line([(730, wy0), (730, wy1)], 14)
# vertical Al-Qatt column the grandmother is painting
cx0, cx1 = 1060, 1260
s.add("column", rect(cx0, 470, cx1, 940), NIGHT)
for k in range(4):
    y0 = 490 + k * 110
    s.add("chevron", [(cx0 + 20, y0), (cx1 - 20, y0), ((cx0 + cx1) / 2, y0 + 100)], (YELLOW, GREEN, RED, WALL)[k])
# --- lower band: diamonds being painted
s.add("band", rect(0, 1000, W, 1200), WALL)
s.add("stripe", rect(0, 960, W, 1000), NIGHT)
s.add("stripe", rect(0, 1200, W, 1240), NIGHT)
for i in range(8):
    if i in (1, 6):
        continue
    cx = 128 + i * 256
    col = (GREEN, ORANGE, BLUE, YELLOW, GREEN, ORANGE, BLUE, YELLOW)[i]
    s.add("diamond", [(cx, 1010), (cx + 110, 1100), (cx, 1190), (cx - 110, 1100)], col)
s.add("floor", rect(0, 1240, W, H), BROWN)
s.line([(0, 1390), (W, 1390)], 6)

# paint bowls on the floor
for i, (bx, col) in enumerate(((560, RED), (720, BLUE), (1930, GREEN))):
    s.add("paint", ellipse(bx, 1405, 85, 26), col)
    s.add("bowl", arc(bx, 1405, 95, 85, 0, 180, 20), ORANGE)

# --- girl (left) painting a diamond in the lower band
s.extend(figure(330, 1470, 640, facing=1, child=True, top=PINK, bottom="dress", bands=(YELLOW,), yoke=GREEN, head="scarf",
                head_colour=GREEN, cuffs=YELLOW, arms=((-0.02, 0.32), (0.3, 0.02)), elbows=(None, (0.2, 0.2)), shoes=RED, name="girl"))
gh = figure.hands
s.extend(brush(gh[1], (gh[1][0] + 190, gh[1][1] - 60), GREEN, name="girl-brush"))
s.add("girl-hand", circle(*gh[1], 32), SKIN)
# small paint pot in her other hand
s.extend(pot(gh[0][0], gh[0][1] + 150, 150, 120, colour=ORANGE, name="girl-pot", neck=0.7))
s.add("girl-hand", circle(*gh[0], 32), SKIN)

# --- grandmother (right) painting a triangle near the window
s.extend(figure(1560, 1490, 900, facing=-1, top=NIGHT, bottom="dress", bands=(RED, ORANGE), yoke=RED, head="scarf_hat",
                head_colour=NIGHT, hat_colour=STRAW, cuffs=RED, necklace=GREY, arms=((0.165, -0.025), (0.13, 0.33)),
                elbows=((0.12, 0.1), None), shoes=DARK_BROWN, skin=SKIN2, name="grandma"))
mh = figure.hands
s.extend(brush(mh[0], (mh[0][0] - 175, mh[0][1] + 25), RED, name="grandma-brush"))
s.add("grandma-hand", circle(*mh[0], 40), SKIN2)
s.build(__file__)

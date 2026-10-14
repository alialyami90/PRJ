"""A beekeeper collecting Sidr honey in the Asir mountains (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 950), SKY)
s.add("sun", circle(1880, 160, 95), YELLOW)
s.extend(puff(1250, 150, 360, name="cloud"))
s.extend(mountains([(-100, 520), (300, 300), (700, 480), (1150, 280), (1600, 470), (2100, 330)], 1000, LEAF, "far-mountain"))
s.add("hill", smooth([(-400, 980), (500, 860), (1200, 940), (2450, 860), (2450, H + 400), (-400, H + 400)], 3), GRASS)

# sidr tree (left)
s.add("sidr-trunk", [(330, 1180), (430, 1180), (420, 900), (480, 760), (440, 740), (380, 860), (330, 760), (300, 780), (350, 900)], TRUNK)
s.add("sidr-leaves", bumpy(390, 600, 360, 230, bumps=13, depth=0.08), GREEN)
s.add("sidr-leaves2", bumpy(180, 760, 170, 110, bumps=8, depth=0.12), GREEN)

# stacked log hives on a stone base
s.add("hive-base", rect(560, 1150, 1180, 1250), ROCK)
for i, (hx, hy) in enumerate(((620, 1030), (880, 1030), (750, 910))):
    s.add("hive", rrect(hx, hy, hx + 330, hy + 120, 50), BROWN)
    s.add("hive-end", ellipse(hx + 300, hy + 60, 45, 60), STRAW)
    s.ink(ellipse(hx + 300, hy + 70, 14, 16))
s.add("hive-roof", rrect(720, 850, 1120, 920, 18), DARK_BROWN)

# beekeeper holding up a jar of sidr honey
s.extend(figure(1530, 1450, 880, facing=-1, top=WHITE, jacket=BLUE, jacket_trim=YELLOW, bottom="wrap", bottom_colour=RED, bands=(YELLOW,),
                belt=BROWN, buckle=True, head="hat", hat_colour=STRAW, beard=True,
                arms=((0.18, -0.22), (0.16, 0.2)), elbows=((0.2, 0.02), (0.14, 0.12)), name="keeper"))
(lx, ly), (rx, ry) = figure.hands
# honey jar in the raised hand
jx, jy = lx, ly - 40
s.add("jar", rrect(jx - 95, jy - 200, jx + 95, jy + 20, 40), GOLD)
s.add("jar-lid", rrect(jx - 75, jy - 245, jx + 75, jy - 195, 14), DARK_BROWN)
s.line(smooth_open([(jx - 50, jy - 120), (jx - 20, jy - 140), (jx + 20, jy - 140), (jx + 50, jy - 120)], 2), 6)
s.add("keeper-hand", circle(lx, ly, 40), SKIN)
# honeycomb in the other hand
s.add("comb", smooth([(rx - 50, ry - 30), (rx + 120, ry - 50), (rx + 150, ry + 150), (rx - 20, ry + 170)], 1), GOLD)
for cxo, cyo in ((40, 30), (95, 30), (65, 85), (15, 85), (115, 90)):
    s.line([(rx + cxo + 18 * math.cos(math.radians(a)), ry + cyo + 18 * math.sin(math.radians(a))) for a in range(0, 361, 60)], 5)
s.add("keeper-hand", circle(rx, ry, 40), SKIN)

# bees
for fx, fy, c in ((150, 1330, WHITE), (330, 1430, YELLOW), (620, 1400, WHITE), (900, 1450, YELLOW)):
    s.add("bush", bumpy(fx, fy + 50, 110, 55, bumps=7, depth=0.18), LEAF)
    s.extend(flower(fx, fy, 50, c, "blossom"))
for i, (bx, by, sz, f) in enumerate(((1060, 620, 130, 1), (1780, 600, 130, -1), (1450, 260, 120, -1),
                                     (1880, 1260, 120, -1), (640, 360, 120, 1), (1050, 1280, 130, 1), (480, 1180, 120, -1))):
    s.extend(bee(bx, by, sz, facing=f, name="bee"))
s.build(__file__)

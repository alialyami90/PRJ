"""Foggy terraces of Abha with a shepherd, his sheep and goats (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(mountains([(0, 380), (380, 200), (760, 420), (1150, 230), (1550, 400), (1900, 180), (2048, 260)], 900, LEAF, "far-mountain"))
s.extend(puff(560, 400, 900, 120, name="fog"))
s.extend(puff(1650, 360, 800, 110, name="fog"))


def terraces(peaks, top_shift, levels, step, base_y, wall=ROCK, field=GRASS, name="terrace"):
    out = []
    for k in range(levels):
        dy = top_shift + k * step
        pts = [(px, py + dy) for px, py in peaks]
        poly = smooth([(pts[0][0] - 400, base_y + 300)] + pts + [(pts[-1][0] + 400, base_y + 300)], 3)
        out.append(("region", f"{name}-wall", poly, wall))
        out.append(("region", f"{name}-field", [(x, y + 38) for x, y in poly], field if k % 2 == 0 else GRASS))
    return out


# left terraced hill
s.extend(terraces([(-200, 760), (200, 560), (520, 520), (900, 640), (1250, 860)], 0, 4, 95, 1000, name="terrace-left"))
# right terraced hill
s.extend(terraces([(1000, 860), (1400, 600), (1750, 520), (2100, 600), (2300, 700)], 0, 4, 95, 1000, field=GREEN, name="terrace-right"))
s.extend(puff(1100, 760, 1500, 140, name="fog"))
# meadow
s.add("meadow", smooth([(-400, 1060), (600, 990), (1300, 1030), (2450, 980), (2450, H + 400), (-400, H + 400)], 3), GRASS)
s.extend(puff(300, 1000, 760, 110, name="fog"))
s.extend(juniper(1390, 1090, 400, name="juniper"))

for fx, fy in ((700, 1150), (1985, 1500), (820, 1480), (120, 1480)):
    s.extend(flower(fx, fy, 46, YELLOW, "daisy"))
# animals
s.extend(sheep(400, 1450, 400, facing=1, name="sheep"))
s.extend(goat(1050, 1480, 380, facing=-1, body=WHITE, patch=BROWN, horn=GREY, name="goat"))
s.extend(sheep(1230, 1530, 280, facing=1, name="lamb"))

# shepherd with a staff
s.extend(figure(1820, 1440, 860, facing=-1, top=WHITE, bottom="wrap", bottom_colour=ORANGE, bands=(RED,), belt=BROWN, buckle=True,
                head="hat", hat_colour=STRAW, beard=True, arms=((0.18, 0.12), (0.06, 0.36)), elbows=((0.14, 0.1), None), name="shepherd"))
hx, hy = figure.hands[0]
s.add("staff", thick([(hx - 30, hy - 330), (hx + 30, 1440)], 32), TRUNK)
s.add("shepherd-hand", circle(hx, hy, 840 * 0.045), SKIN)
s.build(__file__)

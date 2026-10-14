"""Flamingos and a heron among the reeds of Al-Asfar Lake, watched by a boy with binoculars (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403


def reeds(x, base_y, h, n=4, name="reed"):
    items = []
    for i in range(n):
        dx = (i - (n - 1) / 2) * 55
        lean = (i - (n - 1) / 2) * 40
        hh = h * (0.8 + 0.2 * ((i * 7) % 3) / 2)
        items.append(("region", f"{name}-leaf", smooth([(x + dx - 26, base_y), (x + dx + 26, base_y), (x + dx + lean + 4, base_y - hh)], 1), GREEN))
    for i in range(0, n, 2):
        dx = (i - (n - 1) / 2) * 55 + 25
        top = base_y - h * 1.05
        items.append(("line", [(x + dx, base_y - 10), (x + dx + 5, top + 90)], 8))
        items.append(("region", f"{name}-cattail", ellipse(x + dx + 6, top + 50, 24, 62), BROWN))
    return items


s = Scene()
s.add("sky", rect(0, 0, W, 800), SKY)
s.add("sun", circle(1780, 190, 110), SUN)
s.extend(cloud(520, 230, 420))
s.extend(bird(1150, 200, 50))
s.extend(bird(1290, 150, 40))
s.extend(bird(1380, 250, 34))
# golden dunes around the lake
s.add("dune-far", smooth_open([(0, 760), (300, 600), (650, 700), (1000, 580), (1400, 690), (1750, 560), (W, 680)], 2) + [(W, 860), (0, 860)], DUNE)
s.add("dune-near", smooth_open([(1100, 860), (1400, 740), (1750, 780), (W, 720)], 2) + [(W, 860)], SAND)
# the lake
s.add("lake", rect(0, 820, W, 1330), SEA)
for (lx, ly, lw) in ((300, 950, 220), (1050, 920, 260), (1700, 960, 200), (900, 1160, 240), (1500, 1220, 200)):
    s.line([(lx - lw / 2, ly), (lx + lw / 2, ly)], 6)
s.add("shore", smooth_open([(0, 1240), (500, 1270), (1000, 1340), (1500, 1320), (W, 1360)], 2) + [(W, H), (0, H)], SAND)

# reeds at the back
s.extend(reeds(130, 900, 380, 4, "reed-a"))
s.extend(reeds(1920, 900, 420, 3, "reed-b"))
# heron wading on the left
s.extend(heron(640, 1170, 660, facing=1))
# two flamingos, one feeding
s.extend(flamingo(1790, 1230, 600, facing=-1, head_down=True, one_leg=False, name="flamingo2"))
s.extend(flamingo(1300, 1260, 840, facing=-1, name="flamingo"))
# reeds in front
s.extend(reeds(1880, 1360, 330, 3, "reed-c"))
s.extend(reeds(960, 1330, 260, 3, "reed-d"))

# boy on the shore looking through binoculars
bx, bfeet, bh = 320, 1490, 680
r = bh * 0.135
hcy = bfeet - bh + r
items, info = figure(bx, bfeet, bh, "tracksuit", "hair", skin=SKIN2, cloth=TEAL, shoe=WHITE, child=True,
                     lhand=[(bx - r * 1.6, hcy + r * 1.9), (bx - r * 0.95, hcy + r * 0.25)],
                     rhand=[(bx + r * 1.6, hcy + r * 1.9), (bx + r * 0.95, hcy + r * 0.25)], name="boy")
s.extend(items[:-4])  # everything except the front arms and hands
s.add("binocular-bridge", rect(bx - r * 0.3, hcy - r * 0.35, bx + r * 0.3, hcy + r * 0.05), BLACK_CLOTH)
for sx in (-1, 1):
    s.add("binocular", circle(bx + sx * r * 0.45, hcy - r * 0.12, r * 0.5), BLACK_CLOTH)
    s.add("binocular-lens", circle(bx + sx * r * 0.45, hcy - r * 0.12, r * 0.31), SKY)
s.extend(items[-4:])
s.build(__file__)

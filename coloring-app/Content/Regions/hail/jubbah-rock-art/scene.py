"""Children in caps and sneakers tracing an ancient ibex carving at Jubbah (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

CARVE = CREAM


def ibex(x, y, s, name="ibex"):
    """Petroglyph-style ibex facing right; (x, y) = middle of the back, s = body length."""
    it = []
    # horns sweeping back in a big arc
    horn = arc(x + s * 0.2, y - s * 0.4, s * 0.28, s * 0.36, 355, 190, 18)
    it.append(R(f"{name}-horn", limb(horn, s * 0.13, s * 0.07), CARVE))
    for lx, d in ((-0.38, -0.04), (-0.22, 0.03), (0.2, -0.03), (0.34, 0.04)):
        it.append(R(f"{name}-leg", limb([(x + lx * s, y + s * 0.25), (x + (lx + d) * s, y + s * 0.7)], max(s * 0.13, 40), max(s * 0.1, 34)), CARVE))
    it.append(R(f"{name}-body", smooth([(x - s * 0.5, y + s * 0.02), (x - s * 0.56, y - s * 0.12), (x - s * 0.44, y - s * 0.06),
                                        (x + s * 0.2, y - s * 0.04), (x + s * 0.34, y - s * 0.3), (x + s * 0.44, y - s * 0.42),
                                        (x + s * 0.62, y - s * 0.32), (x + s * 0.6, y - s * 0.24), (x + s * 0.46, y - s * 0.2),
                                        (x + s * 0.42, y + s * 0.3), (x - s * 0.45, y + s * 0.3)], 2), CARVE))
    it.append(R(f"{name}-beard", smooth([(x + s * 0.5, y - s * 0.23), (x + s * 0.56, y - s * 0.24), (x + s * 0.52, y - s * 0.08)], 1), CARVE))
    return it


s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(sun(1830, 200, 105))
s.extend(cloud(1180, 230, 420, "cloud"))
s.extend(cloud(260, 170, 300, "cloud2"))
# Jubbah's sandstone mountain (Umm Sinman) behind
s.add("mountain", smooth([(1050, 1000), (1150, 650), (1300, 520), (1420, 470), (1560, 560), (1700, 450), (1850, 520),
                          (1960, 620), (2100, 700), (2100, 1000)], 2), MUD)
s.add("far-dune", smooth([(-60, 1000), (-60, 820), (300, 760), (700, 830), (1000, 780), (1400, 860), (2100, 820), (2100, 1000)], 2), DUNE)
s.add("ground", rect(0, 960, W, H), SAND)

# the big carved boulder
s.add("boulder", smooth([(60, 1220), (40, 820), (110, 470), (300, 330), (620, 290), (900, 320), (1180, 300), (1360, 420),
                         (1420, 700), (1400, 1000), (1350, 1240)], 2), ROCK)
s.line(smooth_open([(150, 1080), (330, 1110), (520, 1090)], 2), 6)
s.line(smooth_open([(1240, 380), (1300, 470), (1310, 560)], 2), 6)
# carvings
s.extend(ibex(990, 610, 300, "ibex"))
s.extend(ibex(470, 500, 220, "ibex-small"))
# a carved camel
cx, cy = 380, 860
s.add("camel-carving", smooth([(cx - 120, cy), (cx - 90, cy - 70), (cx - 20, cy - 95), (cx + 40, cy - 60), (cx + 80, cy - 90),
                               (cx + 120, cy - 120), (cx + 150, cy - 100), (cx + 105, cy - 70), (cx + 85, cy - 20), (cx + 70, cy + 15),
                               (cx - 110, cy + 15)], 2), CARVE)
for lx in (-90, -45, 20, 62):
    s.add("camel-carving-leg", limb([(cx + lx, cy + 5), (cx + lx, cy + 105)], 32, 28), CARVE)
# carved sun spiral
s.add("sun-carving", circle(190, 600, 62), CARVE)
s.line(arc(190, 600, 32, 32, 0, 300, 16), 7)

# backpack on the ground
s.add("backpack-loop", limb(arc(1790, 1235, 45, 40, 180, 360, 12), 26), RED)
s.add("backpack", smooth([(1690, 1430), (1680, 1300), (1700, 1240), (1790, 1215), (1880, 1240), (1900, 1300), (1890, 1430)], 2), RED)
s.add("backpack-pocket", smooth([(1720, 1420), (1715, 1340), (1865, 1340), (1860, 1420)], 1), YELLOW)
s.add("backpack-flap", smooth([(1695, 1300), (1715, 1245), (1790, 1225), (1865, 1245), (1885, 1300), (1790, 1320)], 1), YELLOW)
s.extend(bush(1500, 1080, 220, GREEN, "shrub"))
s.extend(bush(1960, 1240, 200, GREEN, "shrub2"))

# a friendly spiny-tailed lizard (dhub) watching from the sand
lx, ly = 260, 1370
s.add("lizard-tail", limb(smooth_open([(lx - 40, ly), (lx - 140, ly + 20), (lx - 230, ly - 10)], 2), 60, 26), YELLOW)
for dx, d in ((-20, -1), (90, 1)):
    for sy in (-1, 1):
        s.add("lizard-leg", limb([(lx + dx, ly), (lx + dx + d * 40, ly + sy * 85)], 42, 36), YELLOW)
s.add("lizard-body", ellipse(lx + 40, ly, 120, 52), YELLOW)
s.add("lizard-head", ellipse(lx + 175, ly - 12, 62, 44), YELLOW)
s.ink(circle(lx + 192, ly - 26, 9))
s.line(arc(lx + 200, ly - 4, 22, 12, 20, 150, 8), 5)
for k in range(3):
    s.line(arc(lx - 10 + k * 45, ly - 5, 16, 12, 200, 340, 8), 5)

# girl with a magnifying glass looking at the camel carving
g = human(760, 1440, 640, name="girl", facing=-1, outfit="hoodie", top=PINK, bottom=DENIM, accent=PURPLE,
          shoes=WHITE, head="cap", head_col=PURPLE, hair=DARK_BROWN, ponytail=True,
          hands=((600, 1010), (880, 1180)))
s.extend(g)
hx, hy = human.hands[0]
s.add("magnifier-handle", limb([(hx + 20, hy + 35), (hx - 40, hy - 80)], 38), DARK_BROWN)
s.add("magnifier-rim", circle(hx - 80, hy - 140, 72), DARK_BROWN)
s.add("magnifier-glass", circle(hx - 80, hy - 140, 50), SKY)
s.add("girl-hand", circle(hx, hy, 34), SKIN)

# boy reaching up to trace the big ibex
b = human(1490, 1470, 800, name="boy", facing=-1, outfit="tshirt", top=BLUE, bottom=DENIM, print_col=YELLOW,
          shoes=RED, head="cap", head_col=RED, hair=DARK_BROWN, skin=SKIN2,
          hands=((1120, 610), (1600, 1150)))
s.extend(b)
s.build(__file__)

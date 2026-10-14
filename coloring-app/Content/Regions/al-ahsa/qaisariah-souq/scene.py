"""A Hasawi grandmother chooses fabric in the lantern-lit Qaisariah Souq (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
# covered souq corridor: plastered wall, wooden ceiling, arched shop fronts
s.add("wall", rect(0, 0, W, 1080), MUD)
s.add("ceiling", rect(0, 0, W, 130), BROWN)
for bx in range(120, W, 260):
    s.line([(bx, 10), (bx, 125)], 6)
for i, ax in enumerate((60, 590, 1120, 1650)):
    s.add("arch", arch(ax, 300, ax + 340, 1080), DARK_BROWN)
    s.add("arch-frame", arch(ax - 30, 270, ax + 370, 300 + 1) if False else arc(ax + 170, 470, 200, 200, 180, 360) +
          arc(ax + 170, 470, 170, 170, 360, 180), CREAM)
# carved wooden door in the third arch, jars on a shelf in the fourth
s.add("door", arch(1150, 330, 1490, 1080), BROWN)
s.line([(1320, 500), (1320, 1080)], 7)
for dx in (1270, 1370):
    s.ink(circle(dx, 760, 14))
s.add("jar-shelf", rect(1660, 700, 1980, 740), BROWN)
s.extend(jar(1740, 700, 120, 170, MUD, name="jar"))
s.extend(jar(1900, 700, 120, 150, MUD, name="jar2"))
s.add("floor", rect(0, 1080, W, H), SAND)
for fy in (1180, 1320, 1480):
    s.line([(0, fy), (W, fy)], 5)
# shelf of cloth in the first arch
s.add("shelf", rect(70, 638, 390, 695), BROWN)
for j, (c, x0) in enumerate(((BLUE, 95), (YELLOW, 190), (PINK, 285))):
    s.add("shelf-bolt", rect(x0, 520, x0 + 85, 640), c)
# cloth hanging from a pole across the second arch
s.add("pole", rect(560, 430, 960, 455), BROWN)
for k, (c, x0) in enumerate(((GREEN, 600), (PURPLE, 720), (ORANGE, 840))):
    s.add("hanging-cloth", [(x0, 455), (x0 + 100, 455), (x0 + 110, 800), (x0 + 50, 760), (x0 - 10, 800)], c)
# lanterns
for lx in (330, 1290, 1810):
    s.extend(lantern(lx, 150, 120, 180, name="lantern"))
s.line([(330, 130), (330, 150)], 6)

# cloth stall counter with the shopkeeper behind it
items, _ = figure(320, 1420, 760, "thobe", "ghutra", skin=SKIN2, beard=WHITE, look=0.5, legs=False,
                  lhand=[(170, 880), (200, 760)], rhand=[(470, 880), (500, 800)], name="seller")
s.extend(items)
s.add("raised-bolt", rotate(rect(130, 600, 250, 725), -12, 200, 760), GREEN)
s.add("seller-hand2", circle(200, 760, 34), SKIN2)
s.add("counter", rect(40, 950, 600, 1420), BROWN)
s.add("counter-top", rect(20, 920, 620, 965), DARK_BROWN)
s.line([(40, 1180), (600, 1180)], 6)
for j, (c, x0) in enumerate(((BLUE, 60), (YELLOW, 190))):
    s.add("bolt", rect(x0, 820, x0 + 120, 920), c)
    s.line([(x0 + 20, 870), (x0 + 100, 870)], 5)
# the red cloth the grandmother is feeling, unrolled from the counter
s.add("bolt-hero", rect(460, 840, 600, 920), RED)
# grandmother in a Hasawi dress with a gold-trimmed thawb
items, info = figure(960, 1460, 830, "hasawi", "scarf", skin=SKIN2, cloth=GREEN, accent=PURPLE, headcol=BLACK_CLOTH, brows=True, look=-0.4,
                     lhand=[(830, 1000), (760, 960)], rhand=[(1110, 1010), (1060, 880)], name="grandma")
s.extend(items)
# the red cloth she is feeling, unrolled from the bolt on the counter and hanging from her hand
s.add("cloth-drape", smooth([(570, 850), (690, 880), (790, 920), (820, 1010), (835, 1260), (715, 1250), (720, 1050), (660, 960), (570, 915)], 1), RED)
for dx in (0, 45):
    s.line(smooth_open([(745 + dx * 0.4, 1000), (760 + dx, 1120), (765 + dx, 1230)], 2), 5)
s.add("grandma-hand2", circle(*info["hands"][0], 35), SKIN2)

# granddaughter holding a little bag of spices
items, ginfo = figure(1330, 1470, 560, "hasawi", "scarf", cloth=PINK, accent=BLUE, headcol=GREEN, child=True, look=-0.5,
                      lhand=[(1190, 1150), (1150, 1110)], rhand=[(1450, 1060), (1480, 960)], name="girl")
s.extend(items)
s.line([(1150, 1110), (1140, 1170)], 7)
s.add("spice-bag", smooth([(1100, 1165), (1180, 1165), (1225, 1250), (1205, 1310), (1075, 1310), (1055, 1250)], 2), CREAM)
s.add("girl-hand2", circle(1150, 1110, 32), SKIN)

# spice stall: sacks with heaped spices
s.add("spice-table", rect(1540, 1060, W, 1110), DARK_BROWN)
for k, (sx, c) in enumerate(((1620, ORANGE), (1800, RED), (1970, YELLOW))):
    s.add("sack", smooth([(sx - 105, 1120), (sx + 105, 1120), (sx + 120, 1330), (sx + 90, 1390), (sx - 90, 1390), (sx - 120, 1330)], 2), CREAM)
    s.add("sack-rim", smooth([(sx - 115, 1095), (sx + 115, 1095), (sx + 110, 1150), (sx - 110, 1150)], 1), CREAM)
    s.add("spice", smooth([(sx - 105, 1105), (sx - 40, 1020), (sx + 40, 1020), (sx + 105, 1105)], 2), c)
s.build(__file__)

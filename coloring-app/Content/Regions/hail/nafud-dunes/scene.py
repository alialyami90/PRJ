"""Sandboarding down the red Nafud dunes: a girl in a tracksuit riding her board (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

NAFUD = "#E2703A"

s = Scene()
s.add("sky", rect(0, 0, W, 1300), SKY)
s.extend(sun(1780, 210, 110))
s.extend(cloud(1050, 190, 380, "cloud"))
s.extend(cloud(420, 120, 260, "cloud2"))
# distant dunes
s.add("far-dune", smooth([(-50, 1100), (-50, 700), (500, 620), (900, 700), (1300, 560), (1700, 640), (2100, 560), (2100, 1300), (2300, 1400), (-300, 1400), (-50, 1300)], 2), DUNE)
s.add("mid-dune", smooth_open([(1100, 1200), (1450, 800), (1640, 760), (2070, 900)], 2) + [(2070, 1500), (1100, 1500)], ROCK)
# the big red dune the girl is riding down
surface = smooth_open([(-20, 560), (300, 620), (900, 1040), (1500, 1360), (2070, 1440)], 3)
s.add("red-dune", [(-20, 1560)] + surface + [(2070, 1560)], NAFUD)
for k, (a, b) in enumerate((((100, 900), (380, 1080)), ((420, 1240), (760, 1420)), ((60, 1250), (240, 1360)))):
    s.line(smooth_open([a, ((a[0] + b[0]) / 2 + 40, (a[1] + b[1]) / 2 - 20), b], 2), 6)

# camel resting at the foot of the dune
s.extend([it for it in camel(1760, 1510, 360, facing=-1, body=DUNE, name="camel", saddle=False) if it[0] != "region" or it[1] not in ("camel-tail", "camel-ear")])
s.add("camel-ear", ellipse(1501, 1049, 26, 42, rot=20), DUNE)
s.add("camel-tail", limb([(1925, 1220), (1955, 1290), (1945, 1370)], 42, 30), DUNE)
s.add("camel-blanket", smooth([(1640, 1180), (1840, 1180), (1860, 1310), (1620, 1310)], 1), BLUE)
s.add("camel-blanket-band", rect(1615, 1290, 1865, 1335), YELLOW)

# brother cheering at the top with his own board
s.add("board2", limb([(380, 400), (395, 640)], 70), YELLOW)
s.extend(human(230, 640, 510, name="brother", facing=1, outfit="hoodie", top=GREEN, bottom=DENIM, accent=YELLOW,
               shoes=WHITE, head="cap", head_col=RED, mouth="open", hands=((100, 360), (355, 380))))

# sand spray behind the board
s.extend(dust(610, 900, 240, CREAM, "spray"))
s.extend(dust(470, 820, 170, CREAM, "spray2"))

# the sandboard following the slope
s.add("board", limb([(690, 930), (1160, 1170)], 82), BLUE)
s.add("board-stripe", limb([(800, 980), (1060, 1112)], 30), YELLOW)

# the hero: girl in a tracksuit and sports headscarf, arms out for balance
gx, gfeet, gh = 920, 1070, 820
s.extend(human(gx, gfeet, gh, name="girl", facing=1, outfit="tracksuit", top=PURPLE, bottom=PURPLE, accent=PINK,
               shoes=WHITE, head="headscarf", head_col=PINK, mouth="open",
               feet=((800, 975), (1040, 1090)), knees=((750, 860), (1000, 950)),
               hands=((590, 650), (1260, 640))))
s.build(__file__)

"""Floating Mosque by the sea with pelicans (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

HOR = 760
s = Scene()
s.add("sky", rect(0, 0, W, HOR), SKY)
s.extend(sun(1850, 170, 100))
s.extend(cloud(330, 200, 380))
s.extend(cloud(1350, 150, 280))
s.add("sea", rect(0, HOR, W, 1180), SEA)
for wx, wy in ((200, 900), (1450, 860), (1800, 1000), (300, 1080)):
    s.line(arc(wx, wy, 60, 20, 200, 340, 10), 6)
# the floating mosque on its stilts
MX, MB, MS = 700, 930, 640
s.add("platform", rect(MX - MS * 0.6, MB - 20, MX + MS * 0.75, MB + 30), CREAM)
s.extend(mosque(MX, MB - 20, MS, wall=WHITE, dome=TEAL, name="mosque"))
s.add("reflection", smooth([(MX - 300, MB + 140), (MX + 360, MB + 140), (MX + 300, MB + 190), (MX - 240, MB + 190)], 1), LIGHT_BLUE)
# a second pelican floating on the water
s.add("pelican2-body", smooth([(1270, 1120), (1300, 1060), (1440, 1050), (1500, 1110)], 2), WHITE)
s.add("pelican2-neck", tube([(1330, 1070), (1315, 1000), (1330, 960)], 44), WHITE)
s.add("pelican2-beak", smooth([(1320, 935), (1150, 985), (1170, 1010), (1240, 1020), (1315, 990)], 1), ORANGE)
s.add("pelican2-head", circle(1330, 955, 40), WHITE)
s.ink(circle(1318, 946, 8))
# the pier
s.add("pier", rect(0, 1160, W, H), MUD)
for y in (1250, 1350, 1450):
    s.line([(0, y), (W, y)], 6)
s.add("pier-edge", rect(0, 1150, W, 1200), BROWN)
s.add("post", rect(1500, 1080, 1640, 1340), BROWN)
s.add("post-top", ellipse(1570, 1080, 78, 34), DARK_BROWN)
# the family: father, mother, child
s.extend(person(320, 1470, 780, outfit="thobe", headwear="ghutra", cloth=WHITE, skin=SKIN2, arms="down", name="father"))
s.extend(drop(person(590, 1470, 700, outfit="abaya", headwear="headscarf", accent=BLACK_CLOTH, skin=SKIN, arms="out", name="mother"), "-scarf-front"))
kid = shorts_kid(910, 1480, 520, shirt=YELLOW, shorts=BLUE, long_trousers=True, arms=("down", "up"), facing=1, name="kid")
s.extend(scale_region(kid, "-shoe", 1.2))
# the hero pelican landing on the post
s.extend(pelican(1640, 1080 - 0.56 * 500, 500, facing=-1, name="pelican"))
s.build(__file__)

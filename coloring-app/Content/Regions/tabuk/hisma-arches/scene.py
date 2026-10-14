"""Hikers waving from under a sandstone rock arch in the Hisma desert (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(sun(1820, 190, 95))
s.extend(cloud(330, 210, 360, name="cloud1"))
s.extend(cloud(1180, 150, 300, name="cloud2"))

# distant mesas
s.add("far-mesa", smooth([(-20, 1000), (-20, 640), (60, 600), (300, 590), (360, 660), (430, 700), (520, 1000)], 1), MUD)
s.add("far-mesa", smooth([(1500, 1000), (1580, 700), (1640, 620), (1900, 600), (1980, 640), (2070, 660), (2070, 1000)], 1), MUD)
s.add("far-dunes", band([(-20, 900), (400, 840), (900, 900), (1400, 830), (1800, 880), (2070, 850)], 1250), DUNE)

# the big arch (outer contour, then the opening traced back)
outer = [(250, 1160), (270, 900), (230, 700), (290, 470), (380, 330), (560, 240), (820, 200), (1080, 190),
         (1340, 210), (1560, 270), (1720, 380), (1800, 560), (1780, 780), (1820, 1000), (1830, 1160)]
inner = [(1560, 1160), (1560, 950), (1530, 750), (1480, 590), (1380, 480), (1200, 420), (1000, 410),
         (790, 430), (640, 500), (560, 620), (530, 800), (520, 1000), (510, 1160)]
s.add("arch", smooth_open(outer, 2) + smooth_open(inner, 2), ROCK)
# rock layers (stay inside the arch)
s.line(smooth_open([(330, 450), (600, 330), (900, 285), (1200, 290), (1480, 340), (1680, 450)], 2), 6)
s.line(smooth_open([(300, 640), (420, 560), (520, 520)], 2), 6)
s.line(smooth_open([(1560, 520), (1660, 600), (1740, 700)], 2), 6)
s.line(smooth_open([(300, 880), (380, 840), (470, 860)], 2), 6)
s.line(smooth_open([(1610, 900), (1700, 860), (1770, 880)], 2), 6)
# a dark cave hollow on the left leg
s.add("hollow", smooth([(300, 760), (320, 690), (390, 680), (420, 750), (410, 820), (320, 820)], 2), DARK_BROWN)

# sandy ground
s.add("ground", band([(-20, 1130), (500, 1110), (1000, 1150), (1500, 1110), (2070, 1140)], H + 20), SAND)
# boulders and a desert shrub
s.add("boulder", smooth([(40, 1330), (60, 1230), (170, 1190), (290, 1240), (310, 1330)], 2), ROCK)
s.add("boulder-small", smooth([(240, 1340), (260, 1280), (340, 1270), (390, 1340)], 2), MUD)
s.add("shrub", smooth([(1780, 1390), (1760, 1300), (1820, 1240), (1900, 1250), (1960, 1220), (2020, 1290), (2010, 1390)], 2), GRASS)
s.line(smooth_open([(1830, 1380), (1860, 1320), (1880, 1270)], 1), 6)
s.line(smooth_open([(1950, 1380), (1940, 1320), (1960, 1270)], 1), 6)

# hikers: dad, girl and boy waving under the arch
s.extend(kid(1470, 1470, 860, outfit="modern", top=GREEN, bottom=DARK_BROWN, headwear="cap", hw=ORANGE, backpack=RED,
             arms=(25, 165), facing=0, child=False, shoes=DARK_BROWN, name="dad"))
dad_left = kid.hands[0]
s.add("pole", limb([(dad_left[0] - 10, dad_left[1] - 60), (dad_left[0] - 40, 1470)], 12, 12, 0), GREY)
s.add("dad-hand", circle(dad_left[0], dad_left[1], 860 * 0.042), SKIN)
s.extend(kid(940, 1480, 700, outfit="modern", top=YELLOW, bottom=BLUE, headwear="cap", hw=PURPLE, hair_style="pony", backpack=PURPLE,
             arms=(160, 30), facing=0, shoes=RED, name="girl"))
s.extend(kid(430, 1490, 640, outfit="tshirt", top=RED, bottom=BLUE, accent=YELLOW, headwear="cap", hw=BLUE, backpack=ORANGE,
             arms=(150, 160), facing=0, shoes=DARK_BROWN, name="boy"))
s.build(__file__)

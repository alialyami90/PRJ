"""Hatim Al-Tai, famous for his generosity, welcoming guests at his tent with coffee and a feast (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1100), SKY_DUSK)
s.extend(sun(1500, 330, 120))
s.extend(cloud(560, 200, 360, "cloud"))
# the Aja mountains of Hail
s.add("mountain", [(-20, 1000)] + smooth_open([(-20, 700), (250, 520), (480, 640), (760, 430), (1050, 620), (1300, 560), (1600, 700),
                                               (1820, 500), (2070, 640)], 2) + [(2070, 1000)], ROCK)
s.line(smooth_open([(760, 440), (720, 560), (760, 660)], 2), 6)
s.line(smooth_open([(1820, 510), (1780, 620), (1830, 720)], 2), 6)
s.add("ground", [(-20, 1560), (-20, 960)] + smooth_open([(-20, 960), (700, 1000), (1400, 960), (2070, 990)], 2) + [(2070, 1560)], SAND)


# the black goat-hair tent
s.add("tent-inside", rect(80, 700, 1000, 1070), DARK_BROWN)
s.add("tent-roof", smooth_open([(30, 760), (60, 690), (300, 610), (540, 650), (780, 600), (1000, 680), (1050, 760)], 2)
      + [(1050, 790), (30, 790)], BLACK_CLOTH)
for cx in (130, 545, 960):
    s.add("sadu", [(cx - 90, 1070), (cx + 90, 1070), (cx, 935)], RED)
for px in (300, 780):
    s.add("tent-pole", rect(px - 16, 790, px + 16, 1070), TRUNK)

# the rug with a woven border
s.add("rug-border", [(70, 1140), (1060, 1140), (1160, 1480), (-20, 1480)], GOLD)
s.add("rug", [(120, 1175), (1015, 1175), (1095, 1440), (40, 1440)], RED)

# guest one, seated, clapping happily
g1x, g1s = 300, 1300
s.extend(human(g1x, g1s + 380, 760, name="guest1", adult=True, facing=1, outfit="thobe", top=WHITE, head="ghutra", shoes=None,
               seated_y=g1s, feet=((g1x - 150, g1s + 40), (g1x + 150, g1s + 40)), knees=((g1x - 190, g1s + 5), (g1x + 190, g1s + 5)),
               beard=DARK_BROWN, hands=((g1x - 40, g1s - 170), (g1x + 40, g1s - 170))))

# the feast platter of rice and lamb
s.add("platter", ellipse(560, 1410, 240, 72), GOLD)
s.add("rice", smooth([(360, 1410), (420, 1320), (560, 1280), (700, 1320), (760, 1410)], 2), CREAM)
s.add("lamb", smooth([(470, 1350), (500, 1290), (600, 1270), (660, 1310), (640, 1360)], 2), BROWN)

# guest two holding out his cup
g2x, g2s = 800, 1270
s.extend(human(g2x, g2s + 380, 760, name="guest2", adult=True, facing=1, outfit="thobe", top=CREAM, head="shemagh", head_col=RED, shoes=None,
               seated_y=g2s, feet=((g2x - 150, g2s + 40), (g2x + 150, g2s + 40)), knees=((g2x - 190, g2s + 5), (g2x + 190, g2s + 5)),
               hands=((g2x - 120, g2s - 50), (g2x + 240, g2s - 190))))
cupx, cupy = human.hands[1]
s.extend(finjan(cupx + 5, cupy - 78, 100, WHITE, "cup"))
s.add("guest2-hand", circle(cupx, cupy, 32), SKIN)

# fire to keep the coffee warm
s.add("fire-stones", ellipse(1880, 1450, 150, 55), ROCK)
s.add("firewood", limb([(1780, 1440), (1980, 1400)], 40), TRUNK)
s.add("flame", smooth([(1780, 1440), (1780, 1340), (1840, 1260), (1870, 1340), (1910, 1220), (1960, 1340), (1980, 1440)], 2), ORANGE)
s.add("flame-inner", smooth([(1830, 1440), (1840, 1370), (1880, 1310), (1920, 1370), (1930, 1440)], 2), YELLOW)

# the hero: Hatim Al-Tai in bisht and turban pouring from a giant coffee pot
hx, hfeet, hh = 1500, 1490, 940
d = dallah(1320, 900, 360, name="dallah", facing=-1, tilt=-45)
handle = dallah.handle
spout = dallah.spout
s.extend(human(hx, hfeet, hh, name="hatim", adult=True, facing=-1, outfit="bisht", top=WHITE, cloak=BROWN, trim=GOLD,
               head="turban", head_col=WHITE, beard=DARK_BROWN, shoes=DARK_BROWN,
               hands=((handle[0] + 5, handle[1] + 10), (1730, 1010))))
hands = human.hands
s.add("coffee", limb(smooth_open([spout, (spout[0] + 10, spout[1] + 70), (cupx, cupy - 85)], 2), 28, 22), DARK_BROWN)
s.extend(d)
s.add("hatim-hand", circle(*hands[0], 40), SKIN)
# a second cup ready in his other hand
s.extend(finjan(hands[1][0], hands[1][1] - 75, 100, WHITE, "cup2"))
s.add("hatim-hand", circle(*hands[1], 40), SKIN)
s.build(__file__)

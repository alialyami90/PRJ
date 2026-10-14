"""A rare snow day on Jabal Al-Lawz: kids in puffer jackets and beanies build a snowman (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, snowman  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(cloud(330, 200, 420, name="cloud1"))
s.extend(cloud(1700, 150, 360, name="cloud2"))

# Jabal Al-Lawz peaks with snow caps
s.add("mountain-back", band([(-20, 700), (200, 520), (420, 600), (1250, 330), (1500, 470), (1750, 380), (2070, 560)], 1000, 1), BROWN)
s.add("mountain", smooth_open([(300, 1000), (620, 560), (820, 300), (900, 260), (1000, 330), (1250, 620), (1500, 1000)], 1) , ROCK)
s.add("snow-cap", smooth_open([(680, 480), (820, 300), (900, 260), (1000, 330), (1120, 470)], 1)
      + smooth_open([(1120, 470), (1060, 520), (1000, 460), (930, 540), (860, 470), (780, 540), (720, 500)], 1), WHITE)
s.add("peak-right", smooth_open([(1300, 1000), (1550, 600), (1720, 420), (1880, 540), (2070, 720)], 1) + [(2070, 1000)], ROCK)
s.add("snow-cap", smooth_open([(1580, 560), (1720, 420), (1860, 525)], 1)
      + smooth_open([(1860, 525), (1800, 560), (1740, 520), (1680, 580), (1620, 545)], 1), WHITE)
s.add("peak-left", smooth_open([(-20, 640), (150, 520), (300, 640), (520, 1000)], 1) + [(-20, 1000)], ROCK)

# snowy ground
s.add("snow-far", band([(-20, 940), (600, 900), (1200, 950), (2070, 900)], 1100), CREAM)
s.add("snow", band([(-20, 1060), (500, 1020), (1100, 1070), (1600, 1030), (2070, 1060)], H + 20), WHITE)
# almond trees dusted with snow
for tx, th in ((170, 420), (1880, 460)):
    s.add("tree-trunk", limb([(tx, 1150), (tx + 5, 1150 - th * 0.55)], 26, 18, 1), TRUNK)
    s.add("tree-top", smooth([(tx - th * 0.4, 1150 - th * 0.5), (tx - th * 0.3, 1150 - th * 0.85), (tx, 1150 - th), (tx + th * 0.32, 1150 - th * 0.85),
                              (tx + th * 0.42, 1150 - th * 0.5), (tx, 1150 - th * 0.4)], 2), LEAF)
    s.add("tree-snow", smooth([(tx - th * 0.3, 1150 - th * 0.82), (tx, 1150 - th * 0.98), (tx + th * 0.3, 1150 - th * 0.82), (tx, 1150 - th * 0.75)], 2), WHITE)
# snowballs
for bx, by, r in ((300, 1400, 70), (400, 1450, 50), (1800, 1420, 65)):
    s.add("snowball", circle(bx, by, r), WHITE)

# the snowman in the middle
s.extend(snowman(1020, 1470, 820, scarf=RED, hat=BLACK_CLOTH))
# boy on the left patting the snowman, girl on the right waving
s.extend(kid(560, 1470, 740, outfit="puffer", top=BLUE, bottom=BLACK_CLOTH, headwear="beanie", hw=YELLOW, accent=RED,
             arms=(30, 110), facing=1, shoes=BROWN, name="boy"))
s.extend(kid(1530, 1470, 720, outfit="puffer", top=PINK, bottom=PURPLE, headwear="beanie", hw=PURPLE, accent=YELLOW,
             arms=(150, 30), facing=-1, shoes=BROWN, name="girl"))
# a few snowflakes
for fx, fy in ((640, 110), (1180, 90), (1420, 250), (110, 420)):
    s.add("snowflake", star(fx, fy, 60, 32, 6), WHITE)
s.build(__file__)

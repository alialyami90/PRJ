"""A boy in a thobe and headwrap wading in the Wadi Al-Disah stream with his goat (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, goat  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(cloud(1020, 170, 340, name="cloud"))
s.add("sun", circle(1250, 330, 80), SUN)

# far canyon walls
s.add("far-cliff", smooth_open([(500, 1000), (560, 520), (700, 470), (820, 560), (900, 640), (960, 700)], 2) + [(960, 1000)], MUD)
s.add("far-cliff", smooth_open([(930, 1000), (1060, 650), (1180, 560), (1330, 470), (1480, 520), (1540, 1000)], 2), MUD)
# tall sandstone cliffs either side
s.add("cliff-left", smooth_open([(-20, 1200), (-20, 60), (180, 30), (320, 110), (420, 260), (470, 420), (560, 640), (600, 900), (700, 1150)], 2)
      + [(700, 1200)], ROCK)
s.add("cliff-right", smooth_open([(1340, 1200), (1450, 950), (1480, 700), (1560, 420), (1660, 220), (1820, 90), (2070, 60)], 2)
      + [(2070, 1200)], ROCK)
for pts in ([(60, 300), (200, 260), (340, 330)], [(40, 620), (240, 560), (450, 640)], [(60, 900), (300, 860), (520, 930)],
            [(1600, 420), (1800, 360), (2030, 400)], [(1540, 700), (1780, 650), (2030, 700)], [(1480, 960), (1760, 920), (2030, 960)]):
    s.line(smooth_open(pts, 2), 6)

# grassy valley floor
s.add("valley", band([(-20, 1000), (500, 960), (1000, 980), (1500, 950), (2070, 1000)], H + 20), GRASS)
# palms on both banks
s.extend(palm(330, 1130, 560, name="palm1"))
s.extend(palm(560, 1060, 420, name="palm2"))
s.extend(palm(1620, 1080, 480, name="palm3"))
s.extend(palm(1850, 1160, 600, name="palm4"))
# the stream winding towards us
s.add("stream", smooth([(940, 990), (1060, 990), (1150, 1080), (1120, 1180), (1350, 1300), (1700, 1420), (1820, H + 30),
                        (200, H + 30), (420, 1400), (720, 1260), (860, 1150), (900, 1060)], 2), SEA)
s.line(smooth_open([(600, 1420), (700, 1400), (800, 1420)], 1), 6)
s.line(smooth_open([(1150, 1330), (1230, 1310), (1310, 1330)], 1), 6)
s.line(smooth_open([(980, 1080), (1030, 1070), (1080, 1080)], 1), 6)
# pebbles on the bank
for px, py, rx in ((160, 1300, 60), (260, 1360, 45), (1880, 1330, 60), (1980, 1390, 45)):
    s.add("pebble", ellipse(px, py, rx, rx * 0.6), GREY)

# the goat on the bank, looking at the boy
s.extend(goat(1500, 1420, 360, facing=-1, body=WHITE, patch=BROWN))
# the boy wading, thobe tucked up, waving
s.extend(kid(880, 1440, 780, outfit="thobe_rolled", top=WHITE, headwear="headwrap", hw=RED, arms=(35, 150),
             facing=1, name="boy"))
# water ripples hiding his feet
s.add("ripple", smooth([(700, 1450), (760, 1395), (880, 1385), (1000, 1395), (1060, 1450), (1000, 1500), (760, 1500)], 2), DEEP_SEA)
s.build(__file__)

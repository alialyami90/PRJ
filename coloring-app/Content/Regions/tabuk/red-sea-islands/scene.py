"""Dolphins leaping beside a boat near the Red Sea islands; a dugong and a turtle below (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, boat, dolphin, dugong, turtle, fish, wavy_line  # noqa: E402

WATERLINE = 880

s = Scene()
s.add("sky", rect(0, 0, W, 800), SKY)
s.add("sun", circle(1580, 150, 90), SUN)
s.extend(cloud(420, 200, 380, name="cloud1"))
s.extend(cloud(1250, 140, 260, name="cloud2"))
# islands on the horizon
s.add("island-far", band([(1380, 760), (1500, 700), (1700, 690), (1820, 735)], 790, 2), SAND)
s.add("island", band([(1600, 770), (1760, 640), (1960, 610), (2070, 640)], 790, 2), SAND)
s.extend(palm(1830, 690, 380, dates=False))
s.add("far-sea", rect(0, 760, W, 960), DEEP_SEA)

# boat with two kids
s.extend(kid(270, 1010, 520, outfit="tshirt", top=YELLOW, bottom=BLUE, accent=RED, headwear="cap", hw=RED,
             arms=(165, 160), facing=1, name="boy"))
s.extend(kid(590, 1010, 500, outfit="modern", top=RED, bottom=BLUE, headwear="headscarf", hw=PINK,
             arms=(160, 145), facing=1, name="girl"))
s.add("motor", smooth([(30, 760), (110, 750), (120, 900), (60, 920), (40, 860)], 1), GREY)
s.extend(boat(420, 900, 760, hull=WHITE, cabin=None, stripe=RED))
s.add("life-ring", circle(200, 830, 60), ORANGE)
s.add("life-ring-hole", circle(200, 830, 28), WHITE)

# leaping dolphins and their splash
s.extend(dolphin(1060, 520, 660, angle=-30, body=GREY, belly=CREAM, name="dolphin1"))
s.extend(dolphin(1700, 680, 560, angle=35, body=GREY, belly=CREAM, name="dolphin2"))

# underwater
s.add("water", band(wavy_line(-20, W + 20, WATERLINE, 18, 6), H + 20, 0), SEA)
s.add("splash", smooth([(1720, 910), (1750, 830), (1800, 870), (1840, 800), (1880, 860), (1930, 820), (1950, 910), (1840, 940)], 1), WHITE)
s.add("splash", smooth([(740, 910), (770, 840), (820, 870), (860, 820), (900, 910), (820, 940)], 1), WHITE)
s.add("seabed", band([(-20, 1430), (400, 1400), (900, 1440), (1400, 1410), (2070, 1440)], H + 20), SAND)
# sea grass and coral
for gx, gh in ((120, 230), (190, 300), (1080, 220), (1150, 280), (1880, 260), (1950, 200)):
    s.add("seagrass", limb(smooth_open([(gx, 1440), (gx + 30, 1440 - gh * 0.5), (gx - 10, 1440 - gh)], 1), 18, 8), GRASS)
s.add("coral", smooth([(1300, 1440), (1290, 1330), (1330, 1300), (1350, 1370), (1380, 1280), (1420, 1300), (1410, 1380),
                       (1450, 1340), (1480, 1380), (1460, 1440)], 1), PINK)
s.add("rock", smooth([(1620, 1450), (1640, 1380), (1720, 1360), (1800, 1400), (1820, 1450)], 2), GREY)
# the dugong grazing and a turtle swimming
s.extend(dugong(720, 1240, 720, body=GREY, flip=-1))
s.extend(turtle(1520, 1150, 300, angle=-15, shell=GREEN, skin=GRASS))
s.extend(fish(250, 1080, 180, colour=ORANGE, stripe=WHITE, flip=1, name="fish1"))
s.extend(fish(1850, 1090, 190, colour=YELLOW, stripe=WHITE, flip=-1, name="fish2"))
# bubbles
for bx, by, r in ((1110, 1110, 40), (1150, 1030, 32), (1120, 960, 30)):
    s.add("bubble", circle(bx, by, r), WHITE)
s.build(__file__)

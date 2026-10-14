"""A hamadryas baboon family watching a car on the mountain road (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

FUR = "#B0A48A"
GLASS = "#BBDEFB"
s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(puff(420, 170, 380, name="cloud"))
s.extend(puff(1500, 120, 320, name="cloud"))
s.extend(mountains([(-100, 480), (350, 260), (800, 450), (1250, 240), (1700, 420), (2100, 300)], 950, LEAF, "far-mountain"))
s.extend(mountains([(-200, 760), (300, 640), (800, 740), (1300, 620), (1800, 700), (2300, 640)], 1000, GRASS, "near-hill"))
for i, (tx, ty, th) in enumerate(((250, 790, 280), (720, 810, 260), (1880, 780, 280))):
    s.extend(juniper(tx, ty, th, name=f"tree{i}"))
# road
road_top = [(-300, 870), (500, 820), (1100, 840), (1600, 800), (2350, 770)]
road_bot = [(2350, 980), (1600, 1010), (1100, 1050), (500, 1030), (-300, 1070)]
s.add("road", smooth(road_top + road_bot, 2), NIGHT)
for i in range(7):
    x0 = 80 + i * 300
    if 1060 < x0 < 1780:
        continue
    yy = 935 + 10 * math.sin(i)
    s.add("road-dash", thick([(x0, yy), (x0 + 140, yy - 4)], 30), YELLOW)
s.extend(car(1430, 985, 680, colour=RED, facing=-1, glass=GLASS, passenger=SKIN))
# stone wall along the road
s.add("wall", smooth([(-300, 1015), (600, 990), (1200, 1010), (2350, 955), (2350, 1110), (1200, 1150), (600, 1120), (-300, 1155)], 1), ROCK)
for k in range(1, 9):
    x = k * 230
    s.line([(x, 1010 - 0.03 * x + 5), (x, 1125 - 0.02 * x)], 6)
# ground
s.add("ground", smooth([(-400, 1150), (700, 1110), (1300, 1140), (2450, 1100), (2450, H + 400), (-400, H + 400)], 3), SAND)
s.add("rock", smooth([(1580, 1420), (1620, 1300), (1780, 1260), (1900, 1330), (1920, 1430)], 2), ROCK)
s.add("bush", bumpy(1960, 1300, 120, 80, bumps=8, depth=0.15), LEAF)
s.add("bush", bumpy(120, 1250, 140, 90, bumps=8, depth=0.15), LEAF)

# baboon family
s.extend(baboon(520, 1450, 560, facing=1, fur=FUR, mane=GREY, name="dad"))
s.extend(baboon(1430, 1480, 300, facing=1, fur=FUR, name="baby", arm_up=True))
s.extend(baboon(1060, 1440, 440, facing=1, fur=FUR, name="mum"))
s.build(__file__)

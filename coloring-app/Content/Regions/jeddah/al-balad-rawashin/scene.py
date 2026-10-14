"""Old Jeddah (Al-Balad) street with wooden rawashin balconies and cats (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1170), SKY)
s.extend(cloud(1030, 200, 300))
# distant house at the end of the street
s.add("far-house", rect(780, 330, 1290, 1150), CORAL_STONE)
s.extend(roshan(900, 440, 270, 260, wood=GREEN, panel=LEAF, name="far-roshan"))
s.add("far-door", arch(980, 880, 1100, 1150), BROWN)
# street
s.add("street", [(0, 1150), (W, 1150), (W, H), (0, H)], SAND)
s.add("path", [(860, 1150), (1210, 1150), (1500, H), (560, H)], MUD)
# left house
s.add("left-house", [(0, 80), (760, 80), (760, 1210), (0, 1210)], CORAL_STONE)
s.add("left-top", [(0, 40), (790, 40), (790, 110), (0, 110)], MUD)
s.extend(roshan(150, 200, 470, 370, wood=BROWN, panel=TRUNK, name="roshan-left"))
s.add("left-window", rect(230, 790, 630, 1010), DARK_BROWN)
s.add("left-shutter", rect(250, 810, 420, 990), TRUNK)
s.add("left-shutter2", rect(440, 810, 610, 990), TRUNK)
s.add("left-sill", rect(220, 1000, 640, 1050), MUD)
# right house
s.add("right-house", [(1290, 0), (W, 0), (W, 1220), (1290, 1220)], CORAL_STONE)
s.extend(roshan(1430, 140, 480, 420, wood=BLUE, panel=DEEP_SEA, name="roshan-right"))
s.add("right-door", arch(1540, 820, 1820, 1220), BROWN)
s.line([(1680, 900), (1680, 1210)], 6)
s.add("door-step", rect(1500, 1200, 1860, 1250), MUD)
s.add("pot", [(1360, 1080), (1470, 1080), (1450, 1220), (1380, 1220)], ORANGE)
s.add("plant", smooth([(1340, 1080), (1360, 960), (1415, 920), (1470, 960), (1490, 1080)], 2), LEAF)
# lantern hanging from the right house
s.line([(1300, 700), (1230, 700), (1230, 740)], 8)
s.extend(lantern(1230, 740, 210, colour=GOLD, glass=YELLOW, name="lantern"))
# the hero cat on the windowsill
s.extend(cat(430, 1005, 440, fur=ORANGE, name="cat"))
# a second cat strolling in the street
s.extend(cat_walking(1720, 1470, 270, fur=GREY, facing=-1, name="cat2"))
# girl waving at the cat
s.extend(tulle_girl(930, 1470, 660, dress=PINK, scarf=GOLD, tulle=WHITE, arms="wave", facing=-1, name="girl"))
s.build(__file__)

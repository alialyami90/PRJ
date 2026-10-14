"""A girl in a futuristic jumpsuit and her friendly robot in a coastal city of the future with flying taxis (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, robot, flying_taxi, wavy_line  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.add("sun", circle(1080, 170, 90), SUN)
s.add("mountains", band([(-20, 700), (250, 560), (520, 640), (800, 520), (1100, 650), (1400, 560), (1700, 640), (2070, 560)], 900, 1), MUD)
s.add("sea", rect(0, 820, W, 1080), SEA)

# the city on the coast
s.add("line-wall", rect(-10, 620, 520, 860), GREY)            # long mirrored wall city
for x0 in (60, 200, 340):
    s.add("wall-window", rect(x0, 660, x0 + 90, 820), SKY)
s.add("tower", smooth([(600, 880), (620, 400), (680, 300), (740, 400), (760, 880)], 1), WHITE)
s.add("tower-band", rect(612, 520, 768, 580), BLUE)
s.add("tower-band", rect(606, 700, 774, 760), BLUE)
s.add("dome", arc(980, 880, 200, 220, 180, 360) + [(1180, 880)], CREAM)
s.add("dome-window", arch(940, 760, 1020, 880), SKY)
s.add("tower2", rect(1260, 380, 1420, 880), PURPLE)
s.add("tower2-top", arc(1340, 380, 80, 70, 180, 360) + [(1420, 380)], PURPLE)
for y0 in (450, 570, 690):
    s.add("tower2-window", rect(1285, y0, 1395, y0 + 70), SKY)
s.add("tower3", smooth([(1520, 880), (1560, 520), (1700, 460), (1760, 520), (1800, 880)], 1), WHITE)
s.add("tower3-garden", smooth([(1530, 600), (1580, 540), (1660, 520), (1760, 560), (1790, 620), (1660, 640)], 1), GRASS)
s.add("tower4", rect(1860, 560, 2060, 880), BLUE)
for y0 in (610, 730):
    s.add("tower4-window", rect(1890, y0, 2030, y0 + 70), SKY)
s.add("monorail", rect(-10, 870, W + 10, 910), GREY)

# flying taxis
s.extend(flying_taxi(470, 260, 300, body=YELLOW, name="taxi1", flip=1))
s.extend(flying_taxi(1550, 230, 260, body=ORANGE, name="taxi2", flip=-1))
s.extend(flying_taxi(1010, 500, 220, body=PINK, name="taxi3", flip=1))

# promenade by the water
s.add("water-edge", band(wavy_line(-20, W + 20, 1000, 12, 8), 1110, 0), DEEP_SEA)
s.add("promenade", band([(-20, 1080), (2070, 1080)], H + 20, 0), CREAM)
for x0 in range(60, 1700, 300):
    s.add("light-pad", ellipse(x0, 1250, 95, 34), WHITE)
s.add("planter", rect(1780, 1180, 2060, 1300), GREY)
s.add("bush", smooth([(1780, 1190), (1790, 1080), (1880, 1030), (1960, 1060), (2050, 1040), (2060, 1190)], 2), GRASS)

# the girl and her robot friend
s.extend(kid(760, 1460, 820, outfit="jumpsuit", top=PURPLE, accent=YELLOW, headwear="none", hair_style="buns",
             arms=(30, 150), facing=1, shoes=WHITE, name="girl"))
s.extend(robot(1300, 1470, 680, body=GREY, accent=BLUE, screen=SKY))
s.build(__file__)

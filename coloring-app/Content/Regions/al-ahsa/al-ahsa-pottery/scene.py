"""A Hasawi potter at his wheel teaches a girl to shape a clay jar (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
# mud-brick workshop
s.add("wall", rect(0, 0, W, 1100), MUD)
for yy in (150, 330, 510, 690, 870):
    s.line([(0, yy), (W, yy)], 5)
s.add("window", arch(1120, 180, 1420, 520), SKY)
s.add("window-sill", rect(1090, 520, 1450, 570), BROWN)
s.extend(cloud(1270, 420, 200, name="window-cloud"))
s.add("roof-beam", rect(0, 0, W, 70), BROWN)
# shelves of finished jars
for sy in (420, 760):
    s.add("shelf", rect(60, sy, 560, sy + 45), BROWN)
s.extend(jar(150, 420, 140, 200, CLAY, name="shelf-jar", band=True))
s.extend(jar(310, 420, 120, 160, CLAY, name="shelf-jar"))
s.extend(jar(460, 420, 130, 220, CLAY, name="shelf-jar", band=True))
s.extend(jar(180, 760, 170, 210, CLAY, name="shelf-jar"))
s.extend(jar(400, 760, 150, 180, CLAY, name="shelf-jar", band=True))
# dome kiln with a fire inside
s.add("kiln", smooth_open([(1560, 1180), (1580, 860), (1700, 650), (1820, 630), (1960, 700), (2060, 820)], 2) + [(W, 1180)], ROCK)
s.add("kiln-door", arch(1700, 930, 1900, 1180), DARK_BROWN)
s.add("fire", smooth([(1730, 1180), (1740, 1080), (1780, 1110), (1800, 1000), (1830, 1090), (1860, 1050), (1870, 1180)], 1), ORANGE)
s.add("fire-core", smooth([(1770, 1180), (1790, 1110), (1810, 1140), (1830, 1100), (1840, 1180)], 1), YELLOW)
for yy in (780, 900):
    s.line(smooth_open([(1620, yy + 60), (1800, yy - 20), (W, yy + 20)], 2), 5)
s.add("floor", rect(0, 1100, W, H), SAND)

# the potter sits behind his wheel
px = 820
items, info = figure(px, 1470, 880, "thobe", "ghutra", skin=SKIN2, beard=GREY, look=0.3, legs=False,
                     lhand=[(640, 1100), (735, 1120)], rhand=[(1000, 1080), (935, 1050)], name="potter")
s.extend(items)
hands = info["hands"]
# the wheel and the jar being shaped
s.add("stool", rect(560, 1250, 1080, 1330), BROWN)
s.add("wheel-stand", [(700, 1250), (1000, 1250), (970, 1440), (730, 1440)], BROWN)
s.add("kick-wheel", ellipse(850, 1430, 290, 62), DARK_BROWN)
s.add("wheel-head", ellipse(850, 1250, 240, 52), DARK_BROWN)
s.extend(jar(850, 1260, 230, 250, CLAY, name="clay-jar"))
s.line(arc(850, 1135, 112, 18, 15, 165, 12), 6)
for hx, hy in hands:
    s.add("potter-hand", circle(hx, hy, 40), SKIN2)

# the girl in a Hasawi dress, hands on the clay
items, ginfo = figure(1260, 1470, 600, "hasawi", "scarf", skin=SKIN, cloth=GREEN, accent=PINK, headcol=PURPLE, child=True, look=-0.6,
                      lhand=[(1110, 1220), (975, 1160)], rhand=[(1390, 1150), (1380, 1240)], name="girl")
s.extend(items)
# drying jars on the floor
s.extend(jar(1580, 1450, 180, 220, CLAY, name="floor-jar", band=True))
s.extend(jar(1800, 1480, 220, 270, CLAY, name="floor-jar2"))
s.extend(jar(250, 1440, 200, 240, CLAY, name="floor-jar3", band=True))
s.build(__file__)

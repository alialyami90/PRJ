"""Two kids with caps and a flashlight explore the cool passages of Jabal Al-Qarah (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
# far, sunlit walls of the narrow passage with a slit of sky high above
s.add("far-wall", rect(0, 0, W, 1100), STONE)
s.add("sky-slit", smooth([(900, -20), (1160, -20), (1090, 200), (1050, 430), (1015, 200)], 1), SKY)
s.line(smooth_open([(900, 560), (1040, 520), (1200, 570)], 2), 6)
s.line(smooth_open([(820, 800), (1040, 760), (1300, 820)], 2), 6)
s.add("floor", smooth_open([(0, 1050), (700, 1020), (1400, 1030), (W, 1060)], 2) + [(W, H), (0, H)], SAND)
# left canyon wall: rounded sandstone layers
s.add("left-wall", [(0, -10), (930, -10)] + smooth_open([(930, -10), (900, 200), (820, 330), (860, 470), (740, 620), (790, 780), (680, 940), (720, 1110)], 2) + [(0, 1180)], ROCK)
s.add("left-ledge", smooth_open([(0, 800), (420, 760), (740, 850), (700, 990), (300, 1010), (0, 990)], 2), CAVE)
s.add("left-top", smooth_open([(0, 260), (400, 230), (760, 330), (700, 470), (350, 470), (0, 440)], 2), CAVE)
for yy in (160, 640):
    s.line(smooth_open([(0, yy), (300, yy - 30), (600, yy + 10), (780, yy - 10)], 2), 6)
# right canyon wall
s.add("right-wall", [(W, -10), (1130, -10)] + smooth_open([(1130, -10), (1170, 180), (1260, 300), (1220, 470), (1340, 620), (1290, 790), (1400, 950), (1360, 1120)], 2) + [(W, 1180)], ROCK)
s.add("right-ledge", smooth_open([(W, 640), (1700, 610), (1320, 680), (1370, 800), (1700, 840), (W, 820)], 2), CAVE)
s.add("right-top", smooth_open([(W, 140), (1650, 110), (1250, 220), (1300, 350), (1700, 380), (W, 360)], 2), CAVE)
for yy in (480, 980):
    s.line(smooth_open([(1290, yy), (1550, yy - 30), (1800, yy + 10), (W, yy - 10)], 2), 6)
s.add("rock", smooth([(1720, 1270), (1770, 1130), (1900, 1090), (2020, 1150), (2040, 1300)], 2), CAVE)
s.add("rock-small", smooth([(80, 1330), (120, 1220), (260, 1200), (330, 1300), (300, 1360)], 2), CAVE)

# flashlight beam reaching up to a sleepy bat
hx, hy = 760, 840          # flashlight head
cx, cy, rr = 470, 330, 210  # light spot
dx, dy = cx - hx, cy - hy
ln = math.hypot(dx, dy)
px, py = -dy / ln, dx / ln
s.add("beam", [(hx + px * 30, hy + py * 30), (cx + px * rr, cy + py * rr), (cx - px * rr, cy - py * rr), (hx - px * 30, hy - py * 30)], YELLOW)
s.add("light-spot", circle(cx, cy, rr), YELLOW)
# bat hanging upside down from the overhang
s.line([(470, 200), (470, 262)], 8)
s.add("bat-wing", smooth([(470, 270), (330, 290), (310, 420), (380, 395), (420, 450), (470, 410)], 1), BROWN)
s.add("bat-wing", smooth([(470, 270), (610, 290), (630, 420), (560, 395), (520, 450), (470, 410)], 1), BROWN)
s.add("bat-body", ellipse(470, 345, 55, 80), DARK_BROWN)
s.ink(circle(450, 380, 8)); s.ink(circle(490, 380, 8))
s.line(arc(470, 352, 18, 12, 200, 340, 6), 5)

# boy with cap shining the flashlight
items, info = figure(1090, 1460, 760, "tshirt", "cap", skin=SKIN2, cloth=ORANGE, accent=BLUE, headcol=RED, shoe=WHITE,
                     child=True, look=-0.5, lhand=[(930, 990), (830, 925)], name="boy")
s.extend(items)
s.add("flashlight", thick([(840, 935), (780, 862)], 52, 52, cap=False), GREY)
s.add("flashlight-head", thick([(788, 872), (750, 826)], 84, 84, cap=False), GREY)
s.add("boy-hand2", circle(835, 930, 40), SKIN2)

# girl with cap and ponytail pointing at the bat
gx, gfeet, gh = 1500, 1470, 660
gr = gh * 0.135
s.add("girl-ponytail", smooth([(gx + gr * 0.6, gfeet - gh + gr * 0.6), (gx + gr * 1.6, gfeet - gh + gr * 0.9), (gx + gr * 1.8, gfeet - gh + gr * 2.4),
                               (gx + gr * 1.3, gfeet - gh + gr * 2.2), (gx + gr * 0.8, gfeet - gh + gr * 1.4)], 2), DARK_BROWN)
items, ginfo = figure(gx, gfeet, gh, "tracksuit", "cap", skin=SKIN, cloth=PINK, headcol=PURPLE, shoe=WHITE,
                      child=True, look=-0.6, lhand=[(1360, 1000), (1290, 880)], name="girl")
s.extend(items)
s.build(__file__)

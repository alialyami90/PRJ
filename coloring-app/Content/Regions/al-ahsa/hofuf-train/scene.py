"""A schoolgirl waves at the driver of a steam train arriving at old Hofuf station (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403


def wheel(cx, cy, r, colour=RED, name="wheel"):
    items = [("region", name, circle(cx, cy, r), colour)]
    for k in range(4):
        a = math.pi * k / 4
        items.append(("line", [(cx - math.cos(a) * r * 0.9, cy - math.sin(a) * r * 0.9), (cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9)], 7))
    items.append(("region", f"{name}-hub", circle(cx, cy, max(r * 0.3, 28)), BLACK_CLOTH))
    return items


s = Scene()
s.add("sky", rect(0, 0, W, 1050), SKY)
s.extend(cloud(1650, 200, 380))
# old station building behind the line
s.add("station", rect(80, 300, 1980, 1000), MUD)
s.add("station-roof", [(40, 300), (2010, 300), (1960, 220), (90, 220)], CREAM)
s.add("clock-tower", rect(900, 90, 1150, 300), MUD)
s.add("clock-tower-roof", [(870, 100), (1180, 100), (1025, 20)], CREAM)
s.add("clock", circle(1025, 200, 72), WHITE)
s.line([(1025, 200), (1025, 150)], 8)
s.line([(1025, 200), (1062, 215)], 8)
for ax in (160, 380, 600, 1420, 1640, 1860):
    s.add("station-window", arch(ax - 70, 380, ax + 70, 560), DARK_BROWN)
s.add("ballast", rect(0, 1000, W, 1110), ROCK)

# steam puffs
for (cx, cy, rr) in ((520, 390, 70), (430, 290, 90), (300, 190, 105), (150, 110, 95)):
    s.add("steam", circle(cx, cy, rr), WHITE)

# carriage behind the engine
s.add("carriage", smooth([(1460, 560), (2100, 560), (2100, 960), (1460, 960)], 1), BLUE)
s.add("carriage-roof", smooth([(1440, 560), (2100, 560), (2100, 500), (1480, 500)], 1), GREY)
for wx in (1520, 1700, 1880):
    s.add("carriage-window", rect(wx, 610, wx + 130, 760), SKY)
s.add("carriage-stripe", rect(1460, 820, 2100, 870), YELLOW)
for cx in (1580, 1960):
    s.extend(wheel(cx, 990, 70, name="carriage-wheel"))

# the steam locomotive, facing left
s.add("chimney", [(470, 620), (560, 620), (580, 480), (450, 480)], BLACK_CLOTH)
s.add("chimney-top", rect(430, 440, 600, 490), BLACK_CLOTH)
s.add("dome", arc(820, 620, 75, 70, 180, 360), GOLD)
s.add("boiler", rect(500, 610, 1140, 870), GREEN)
for bx in (700, 950):
    s.line([(bx, 615), (bx, 865)], 7)
s.add("smokebox", ellipse(500, 740, 90, 130), BLACK_CLOTH)
s.add("headlamp", circle(470, 660, 42), YELLOW)
s.add("cab", rect(1100, 470, 1440, 880), GREEN)
s.add("cab-roof", rect(1070, 430, 1470, 490), BLACK_CLOTH)
s.add("cab-window", rect(1170, 540, 1360, 720), DARK_BROWN)
s.add("running-board", rect(380, 860, 1460, 910), RED)
s.add("buffer-beam", rect(360, 870, 440, 950), RED)
s.add("cowcatcher", [(440, 910), (440, 1050), (330, 1050)], BLACK_CLOTH)
for k in range(3):
    s.line([(440, 940 + k * 35), (400, 1050)], 5)
s.extend(wheel(560, 1000, 70, name="pony-wheel"))
for cx in (770, 1000, 1230):
    s.extend(wheel(cx, 960, 105, name="drive-wheel"))
s.add("coupling-rod", rect(760, 998, 1240, 1030), GREY)
# rails
s.line([(0, 1060), (W, 1060)], 12)
s.line([(0, 1095), (W, 1095)], 12)

# the driver leaning out of the cab window, waving
dx, dy, dr = 1265, 625, 62
s.add("driver-body", smooth([(1185, 720), (1200, 680), (1330, 680), (1345, 720)], 1), BLUE)
s.extend(face(dx, dy, dr, look=-0.5, beard=None, name="driver", skin=SKIN2))
s.add("driver-cap", arc(dx, dy - dr * 0.42, dr * 1.05, dr * 0.92, 180, 360), BLUE)
s.add("driver-brim", ellipse(dx - dr * 0.95, dy - dr * 0.44, dr * 0.85, dr * 0.3), BLUE)
s.add("driver-arm", thick([(1190, 700), (1120, 640), (1090, 540)], 52, 46), BLUE)
s.add("driver-hand", circle(1088, 520, 38), SKIN2)

# platform in the foreground
s.add("platform", rect(0, 1130, W, H), SAND)
s.add("platform-edge", rect(0, 1110, W, 1170), YELLOW)
for px in range(150, W, 300):
    s.line([(px, 1170), (px - 60, H)], 5)

# bench with a suitcase waiting on the platform
s.add("bench-back", rect(180, 1180, 700, 1250), DARK_BROWN)
s.add("bench-seat", rect(150, 1300, 730, 1350), DARK_BROWN)
for lx in (190, 660):
    s.add("bench-leg", rect(lx, 1350, lx + 40, 1450), DARK_BROWN)
s.add("suitcase", rect(290, 1140, 560, 1300), RED)
s.add("suitcase-handle", thick([(390, 1142), (390, 1095), (460, 1095), (460, 1142)], 26, 26, cap=False), BLACK_CLOTH)
s.line([(330, 1220), (520, 1220)], 6)

# schoolgirl with a backpack, waving at the driver
gx, gfeet, gh = 1700, 1490, 720
r = gh * 0.135
sh_y = gfeet - gh + r * 2 + gh * 0.03
s.add("backpack", smooth([(gx - gh * 0.2, sh_y + 10), (gx + gh * 0.2, sh_y + 10), (gx + gh * 0.22, sh_y + gh * 0.36), (gx - gh * 0.22, sh_y + gh * 0.36)], 2), ORANGE)
items, info = figure(gx, gfeet, gh, "uniform", "scarf", skin=SKIN, cloth=WHITE, accent=NAVY, headcol=WHITE, shoe=BLACK_CLOTH,
                     child=True, look=-0.6, lhand=[(gx - 180, sh_y - 30), (gx - 230, sh_y - 170)], name="girl")
s.extend(items)
for sx in (-1, 1):
    s.add("backpack-strap", thick([(gx + sx * gh * 0.11, sh_y + 5), (gx + sx * gh * 0.12, sh_y + gh * 0.2)], 34, 34, cap=False), ORANGE)
s.build(__file__)

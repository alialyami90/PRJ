"""The old Hejaz Railway station in Tabuk with a steam locomotive and its station master (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(sun(1880, 150, 85))
s.add("hills", band([(-20, 820), (300, 760), (700, 800), (1200, 740), (1700, 790), (2070, 750)], 1100), DUNE)

# station building (stone, arched windows, crenellated parapet)
s.add("station", rect(60, 470, 760, 1080), CREAM)
s.add("station-upper", rect(160, 330, 660, 470), CREAM)
for i in range(5):
    cx = 175 + i * 100
    s.add("parapet", rect(cx, 290, cx + 70, 330), CREAM)
s.add("cornice", rect(40, 455, 780, 495), MUD)
s.add("door", arch(320, 760, 500, 1080), DARK_BROWN)
for wx in (120, 580):
    s.add("window", arch(wx, 600, wx + 110, 780), DARK_BROWN)
for wx in (230, 470):
    s.add("window-up", arch(wx, 360, wx + 80, 450), DARK_BROWN)
s.add("clock", circle(410, 400, 52), WHITE)
s.line([(410, 400), (410, 368)], 6)
s.line([(410, 400), (436, 412)], 6)

# platform and track
s.add("platform", band([(-20, 1060), (2070, 1060)], H + 20, 0), MUD)
s.add("track-bed", rect(560, 1180, W + 10, 1300), SAND)
for i in range(9):
    sx = 600 + i * 165
    s.add("sleeper", rect(sx, 1235, sx + 110, 1290), BROWN)
s.add("rail", rect(560, 1215, W + 10, 1240), GREY)
s.line([(-10, 1180), (560, 1180)], 8)

# smoke puffs
s.add("smoke", smooth([(860, 560), (830, 480), (880, 420), (960, 430), (1000, 380), (1090, 390), (1110, 460), (1070, 520), (960, 540)], 2), WHITE)
s.add("smoke", smooth([(1040, 330), (1030, 270), (1090, 230), (1170, 240), (1200, 290), (1160, 340)], 2), WHITE)
s.add("smoke", smooth([(1200, 220), (1200, 170), (1250, 140), (1310, 160), (1310, 210)], 2), WHITE)

# locomotive facing left
s.add("chimney", [(860, 760), (840, 600), (960, 600), (940, 760)], BLACK_CLOTH)
s.add("chimney-cap", rect(825, 570, 975, 610), RED)
s.add("dome", arch(1110, 680, 1220, 770), GOLD)
s.add("boiler", rect(800, 750, 1480, 1000), BLACK_CLOTH)
s.add("boiler-band", rect(1000, 750, 1040, 1000), GOLD)
s.add("boiler-band", rect(1300, 750, 1340, 1000), GOLD)
s.add("smokebox", ellipse(800, 875, 75, 125), GREY)
s.add("lamp", circle(790, 720, 40), YELLOW)
s.add("lamp-base", rect(750, 742, 830, 792), BLACK_CLOTH)
# cab with a waving boy at the window
s.add("cab", rect(1460, 620, 1820, 1010), RED)
s.add("cab-window", rect(1510, 670, 1780, 870), CREAM)
boy = kid(1645, 1110, 440, outfit="thobe", top=WHITE, headwear="ghutra", arms=(20, 150), facing=-1, name="boy")
s.extend([i for i in boy if not (i[0] == "region" and i[1].endswith("-shoe"))])
s.add("cab-lower", rect(1460, 870, 1820, 1010), RED)
s.add("cab-roof", rect(1430, 580, 1850, 630), BLACK_CLOTH)
s.add("footplate", rect(700, 1000, 1860, 1060), RED)
s.add("frame", rect(1440, 1055, 1840, 1120), BLACK_CLOTH)
s.add("cowcatcher", [(700, 1060), (800, 1060), (800, 1200), (640, 1200)], GREY)
# wheels
for wx, r in ((900, 85), (1170, 125), (1450, 125), (1700, 85)):
    s.add("wheel", circle(wx, 1215 - r, r), RED)
    s.add("hub", circle(wx, 1215 - r, r * 0.38), GOLD)
s.add("rod", rect(1150, 1080, 1470, 1105), GREY)

# station master in thobe, shemagh and peaked cap, waving the green flag
s.extend(kid(390, 1480, 880, outfit="thobe", top=WHITE, headwear="station", hw=RED, accent=BLUE,
             arms=(20, 150), facing=1, child=False, name="master"))
hx, hy = kid.hands[1]
s.add("master-belt", rect(390 - 160, 1480 - 880 * 0.46, 390 + 160, 1480 - 880 * 0.41), BROWN)
s.add("master-buckle", rect(390 - 40, 1480 - 880 * 0.47, 390 + 40, 1480 - 880 * 0.40), GOLD)
s.add("flag-stick", limb([(hx - 10, hy + 70), (hx + 30, hy - 300)], 10, 10, 0), BROWN)
s.add("flag", smooth([(hx + 25, hy - 290), (hx + 220, hy - 270), (hx + 200, hy - 190), (hx + 22, hy - 170)], 1), GREEN)
s.add("master-hand", circle(hx, hy, 880 * 0.042), SKIN)
# lantern in the other hand
lx, ly = kid.hands[0]
s.add("lantern-handle", limb(arc(lx, ly + 30, 35, 40, 200, 340, 8), 8, 8, 0), BLACK_CLOTH)
s.add("lantern", smooth([(lx - 45, ly + 40), (lx + 45, ly + 40), (lx + 50, ly + 160), (lx - 50, ly + 160)], 1), YELLOW)
s.add("lantern-top", rect(lx - 55, ly + 25, lx + 55, ly + 55), BLACK_CLOTH)
s.add("lantern-base", rect(lx - 55, ly + 150, lx + 55, ly + 195), BLACK_CLOTH)
s.add("master-hand", circle(lx, ly, 880 * 0.042), SKIN)
s.build(__file__)

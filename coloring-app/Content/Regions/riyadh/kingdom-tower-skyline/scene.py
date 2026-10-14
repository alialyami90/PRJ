"""Kids flying kites over the Riyadh skyline with Kingdom Tower (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

GLASS = "#B3E5FC"
s = Scene()
s.add("sky", rect(0, 0, W, 1100), SKY)
s.extend(sun2(250, 210, 110))
s.extend(cloud(760, 190, 360, name="cloud"))
s.extend(cloud(1580, 470, 300, name="cloud"))

# skyline: plain towers behind, then Al Faisaliah (pyramid + golden ball) and Kingdom Tower (arch opening + skybridge)
for x0, x1, top, col in ((80, 300, 700, GREY), (330, 470, 610, GLASS), (1460, 1640, 640, GREY), (1700, 1900, 720, GLASS), (1880, W, 800, GREY)):
    s.add("building", rect(x0, top, x1, 1060), col)
    for k in range(1, 6):
        yy = top + (1060 - top) * k / 6
        s.line([(x0 + 20, yy), (x1 - 20, yy)], 5)
# Al Faisaliah
FX = 640
s.add("faisaliah", [(FX - 120, 1060), (FX - 95, 700), (FX - 18, 330), (FX + 18, 330), (FX + 95, 700), (FX + 120, 1060)], GLASS)
s.add("faisaliah-ball", circle(FX, 420, 52), GOLD)
s.ink([(FX - 12, 332), (FX, 200), (FX + 12, 332)])
for yy in (560, 700, 840, 960):
    s.line([(FX - 85 - (yy - 560) * 0.06, yy), (FX + 85 + (yy - 560) * 0.06, yy)], 5)
# Kingdom Tower: tapering body, U-shaped opening at the top with the skybridge across it
KX, KTOP, KB = 1150, 90, 1060
outer = [(KX - 220, KB), (KX - 210, 800), (KX - 185, 560), (KX - 150, 330), (KX - 122, 180), (KX - 108, KTOP)]
inner = [(KX - 72 * ((1 - t) ** 0.5), KTOP + 360 * t) for t in [i / 12 for i in range(13)]]
inner = inner + [(2 * KX - x, y) for x, y in inner[::-1][1:]]
s.add("kingdom-tower", outer + inner + [(2 * KX - x, y) for x, y in outer[::-1]], GLASS)
s.add("skybridge", smooth(limb([(KX - 128, 245), (KX + 128, 245)], 48), 1), GREY)
for yy in (640, 760, 880, 990):
    w = 175 + (yy - 640) * 0.1
    s.line([(KX - w, yy), (KX + w, yy)], 5)

# park
s.add("grass", band([(0, 1040), (600, 1010), (1300, 1050), (W, 1020)]), GRASS)
s.add("path", smooth_open([(1000, H + 10), (1150, 1250), (1500, 1110), (1700, 1040)], 3) + smooth_open([(1790, 1040), (1650, 1130), (1400, 1300), (1350, H + 10)], 3), SAND)
# tree
s.add("tree-trunk", [(1840, 1200), (1870, 900), (1910, 900), (1940, 1200)], TRUNK)
s.add("tree-top", smooth([(1720, 940), (1700, 790), (1790, 690), (1890, 660), (2000, 720), (2040, 860), (1990, 960), (1860, 990)], 3), GREEN)

# little brother cheering
s.extend(human(1500, 1440, 630, outfit="modern", head="cap", child=True, top=YELLOW, pants=BLUE, accent=RED, shoes=WHITE,
               hands=[(1320, 920), (1690, 900)], look=1, name="boy"))
bh = human.hands[1]
s.extend(kite(1850, 260, 115, colours=(PURPLE, ORANGE, PURPLE, ORANGE), rot=12, name="kite2", tail_to=(1960, 620), bows=(GREEN, BLUE)))
s.line([bh, (1850 - 115 * 0.2, 260 + 112)], 5)

# kite and string
GX, GFEET, GH = 640, 1470, 860
kx, ky = 1430, 330
s.extend(kite(kx, ky, 170, colours=(RED, YELLOW, BLUE, GREEN), rot=-15, name="kite", tail_to=(kx - 330, ky + 520)))

# hero girl: modern abaya, pink hijab, colourful backpack, flying the kite
s.add("backpack", smooth([(GX - 175, 790), (GX + 175, 790), (GX + 185, 1120), (GX - 185, 1120)], 2), ORANGE)
s.extend(human(GX, GFEET, GH, outfit="abaya", head="hijab", child=True, robe=BLACK_CLOTH, accent=PINK, shoes=WHITE, emb=PINK,
               hands=[(GX + 130, 960), (GX + 290, 700)], look=1, name="girl", front_arms=(True, True)))
h1, h2 = human.hands
for sx in (-1, 1):
    s.add("backpack-strap", smooth(limb([(GX + sx * 78, 835), (GX + sx * 98, 960), (GX + sx * 110, 1060)], 44), 1), PURPLE)
s.line([h1, h2, (kx, ky + 170)], 5)
s.build(__file__)

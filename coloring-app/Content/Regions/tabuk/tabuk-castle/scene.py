"""Pilgrims' camels resting by Tabuk Castle while a guide in a bisht pours coffee (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, kneeling_camel, dallah  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY_DUSK)
s.add("sun", circle(1700, 250, 110), SUN)
s.extend(cloud(520, 190, 380, name="cloud"))
s.add("mountains", band([(-20, 760), (250, 600), (520, 720), (900, 560), (1250, 700), (1600, 590), (1900, 700), (2070, 640)], 1100, 1), DUNE)

# Tabuk Castle: square stone fort with two towers and a gate
for i in range(8):
    cx = 340 + i * 100
    s.add("crenel", rect(cx, 460, cx + 60, 520), CREAM)
s.add("castle-wall", rect(300, 515, 1260, 1040), CREAM)
for tx in (180, 1150):
    for i in range(3):
        s.add("tower-crenel", rect(tx + 5 + i * 80, 330, tx + 55 + i * 80, 380), ROCK)
    s.add("tower", rect(tx, 375, tx + 230, 1040), ROCK)
    s.add("tower-window", arch(tx + 80, 520, tx + 150, 640), DARK_BROWN)
s.add("gate-frame", arch(620, 680, 940, 1040), MUD)
s.add("gate", arch(670, 730, 890, 1040), DARK_BROWN)
for wx in (460, 1020):
    s.add("window", rect(wx, 620, wx + 70, 720), DARK_BROWN)

# palms behind the right camel
s.extend(palm(1820, 1100, 600, trunk=BROWN, dates=False, name="palm1"))

s.add("ground", band([(-20, 1020), (600, 1040), (1200, 1010), (2070, 1040)], H + 20), SAND)

# resting camels: one behind, one in front
s.extend(kneeling_camel(560, 1190, 310, facing=-1, body=MUD, blanket=BLUE, band=YELLOW, name="camel2"))
s.extend(kneeling_camel(330, 1450, 430, facing=1, body=MUD, blanket=RED, band=YELLOW, name="camel1"))
s.add("saddle-bag", smooth([(200, 1200), (320, 1200), (312, 1310), (208, 1310)], 2), GREEN)

# a rug under the guide
s.add("rug", [(1440, 1510), (2000, 1510), (1940, 1390), (1500, 1390)], RED)
s.add("rug-border", [(1470, 1480), (1970, 1480), (1925, 1415), (1515, 1415)], YELLOW)

# the guide in thobe, shemagh and bisht pouring coffee
GX, GH = 1720, 830
s.extend(kid(GX, 1460, GH, outfit="bisht", top=WHITE, cloak=BROWN, headwear="shemagh", hw=RED,
             arms=(85, 20), facing=-1, child=False, name="guide"))
lx, ly = kid.hands[0]
PH = 280
grip = (PH * 0.32, -PH * 0.5)          # handle (pot mirrored: spout to the left)
tip0 = (-PH * 0.58, -PH * 0.86)        # spout tip
def place(pts):
    return rotate(translate(pts, lx - grip[0], ly - grip[1]), -60, lx, ly)
s.extend([(k[0], k[1], place(mirror(k[2], 0)), k[3]) for k in dallah(0, 0, PH, colour=GOLD)])
s.add("guide-hand", circle(lx, ly, GH * 0.042), SKIN)
tx, ty = place([tip0])[0]

# a young pilgrim holding his cup under the spout
PK = 520
kid(0, 0, PK, arms=(20, 60), facing=1)
ox, oy = kid.hands[1]
feet = ty + 90 + 75 - oy
s.extend(kid(tx - ox, feet, PK, outfit="thobe", top=WHITE, headwear="ghutra", arms=(20, 60), facing=1, name="pilgrim"))
cx, cy = kid.hands[1]
s.add("coffee", rect(tx - 15, ty - 10, tx + 15, cy - 70), BROWN)
s.add("cup", [(cx - 48, cy - 78), (cx + 48, cy - 78), (cx + 32, cy - 10), (cx - 32, cy - 10)], WHITE)
s.add("pilgrim-hand", circle(cx, cy, 30), SKIN)

s.build(__file__)

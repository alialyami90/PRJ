"""Decorated camels at a camel beauty festival (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 950), SKY)
s.extend(sun2(1830, 180, 105))
s.extend(cloud(330, 170, 380, name="cloud"))
s.add("far-dune", band([(0, 760), (500, 680), (1000, 760), (1500, 670), (W, 740)], 960), DUNE)
# festival pavilions
s.extend(pavilion(80, 520, 900, 380, colour=WHITE, stripe=RED, name="pavilion"))
s.extend(pavilion(1450, 1900, 880, 360, colour=WHITE, stripe=GREEN, name="pavilion", door=False))
s.add("ground", band([(0, 880), (900, 910), (W, 870)]), SAND)
# a fence line for the show ring
s.add("fence", rect(0, 1000, W, 1040), BROWN)
for fx in (1470, 2010):
    s.add("fence-post", rect(fx - 18, 960, fx + 18, 1070), BROWN)

# another contestant behind
s.extend(camel2(270, 1230, 380, facing=1, body=MUD, blanket=GREEN, band=YELLOW, tassel=YELLOW, name="camel-b", halter=YELLOW, tassels=2))

# hero: prize camel with embroidered blankets and tassels
CX, CF, CH = 880, 1490, 600
s.extend(camel2(CX, CF, CH, facing=1, body=DUNE, blanket=RED, band=GOLD, tassel=YELLOW, garland=(BLUE, ORANGE, PURPLE),
                halter=GOLD, name="camel", tassels=5))
P = camel2.P
mouth = camel2.mouth
# embroidered diamonds on the blanket (inside the blanket region)
for u in (-0.26, -0.06, 0.14):
    cx, cy = P(u, 0.84)
    s.line([(cx - 40, cy), (cx, cy - 45), (cx + 40, cy), (cx, cy + 45), (cx - 40, cy)], 6)
s.extend(rosette(*P(0.76, 1.12), 80, colour=BLUE, centre=GOLD, ribbon=RED, name="rosette"))

# the Bedouin owner in a bisht leading his camel
BX = 1780
s.extend(human(BX, 1480, 920, outfit="bisht", head="shemagh", accent=RED, cloak=DARK_BROWN, trim=GOLD, beard=DARK_BROWN,
               hands=[(BX - 230, 1050), (BX + 170, 1200)], look=-1, name="bedouin"))
s.line(smooth_open([mouth, (mouth[0] + 60, 1080), human.hands[0]], 3), 7)
s.build(__file__)

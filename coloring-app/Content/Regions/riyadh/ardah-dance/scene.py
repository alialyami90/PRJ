"""Ardah sword-dance celebration with drummers and flags (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(sun2(1800, 180, 100))
s.extend(cloud(380, 170, 380, name="cloud"))

# Najdi mud-brick palace behind the square
s.add("palace-tower", najdi_block(130, 390, 330, 960, 60, taper=25, step=78), ROCK)
s.add("palace-wall", najdi_block(360, 1690, 520, 960, 62, step=86), MUD)
s.add("palace-tower", najdi_block(1650, 1910, 330, 960, 60, taper=25, step=78), ROCK)
for wx in (500, 640, 1410, 1550):
    s.extend(tri_window(wx, 640, 52))
for tx in (260, 1780):
    for wy in (440, 600):
        s.extend(tri_window(tx, wy, 52))
s.extend(najdi_door(940, 680, 1110, 960, colour=GREEN, frame=WHITE, name="palace-door"))
s.extend(flag(400, 1010, 640, colour=GREEN, name="flag", wave=-1))
s.extend(flag(1530, 1010, 680, colour=GREEN, name="flag"))

s.add("ground", band([(0, 950), (900, 970), (W, 945)]), SAND)

# second dancer, behind on the left
s.extend(sword(360, 700, 350, -72, name="sword2"))
s.extend(human(250, 1300, 660, outfit="thobe", head="shemagh", accent=RED, hands=[(140, 1000), (360, 700)], look=1, name="dancer2"))

# back row of dancers
for bx in (560, 1230):
    s.extend(sword(bx + 135, 640, 220, -75, name="sword-b"))
    s.extend(human(bx, 1060, 480, outfit="thobe", head="shemagh", accent=RED, hands=[(bx - 120, 860), (bx + 135, 640)],
                   look=1, name="dancer-b"))

# drummer on the right with the frame drum
DX = 1660
s.extend(human(DX, 1460, 800, outfit="bisht", head="ghutra", cloak=DARK_BROWN, hands=[(DX - 40, 1030), (DX + 200, 1010)], look=-1, name="drummer", front_arms=(False, True)))
s.extend(drum(DX - 190, 1000, 165, body=RED, skin_c=CREAM, name="drum"))
s.add("drum-stick", smooth(limb([(DX - 40, 1090), (DX - 160, 1010)], 30), 1), TRUNK)
s.add("drummer-hand", circle(DX - 30, 1095, 40), SKIN)

# hero: Ardah dancer in white thobe, gold-trimmed bisht and red shemagh, sword raised high
HX = 860
s.extend(sword(1020, 560, 420, -80, name="sword"))
s.extend(human(HX, 1490, 900, outfit="bisht", head="shemagh", accent=RED, cloak=BROWN, trim=GOLD,
               hands=[(HX - 215, 1150), (1020, 560)], look=1, name="dancer"))
s.build(__file__)

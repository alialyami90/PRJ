"""Boys on camels racing past Masmak Fort at sunset (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
# sunset sky
s.add("sky", rect(0, 0, W, 1000), SKY_DUSK)
s.extend(cloud(330, 230, 420, name="cloud"))
s.extend(cloud(1000, 170, 340, name="cloud"))
s.extend(sun2(1830, 300, 125))
s.add("far-dune", band([(0, 850), (500, 780), (1100, 860), (1600, 780), (W, 840)], 1000), DUNE)

# Masmak Fort: tapered mud towers with stepped crenels, small triangle vents and the big wooden gate
BASE = 1010
s.add("watchtower", najdi_block(1060, 1260, 300, BASE, 60, taper=18, step=70), ROCK)
s.extend(tri_window(1160, 400, 56))
s.add("fort-wall", najdi_block(730, 1590, 560, BASE, 60, step=82), MUD)
for tx in (590, 1510):
    s.add("tower", najdi_block(tx, tx + 230, 400, BASE, 58, taper=36, step=74), ROCK)
    for wy in (510, 650):
        s.extend(tri_window(tx + 115, wy, 54))
for wx in (850, 960, 1360, 1450):
    s.extend(tri_window(wx, 660, 50))
s.add("gate-frame", arch(1030, 680, 1290, BASE), WHITE)
s.add("gate", rect(1065, 755, 1255, BASE), TRUNK)
s.add("gate-door", rect(1110, 840, 1210, BASE), DARK_BROWN)
for gy in (790, 815):
    s.line([(1070, gy), (1250, gy)], 5)

s.add("ground", band([(0, 990), (700, 1005), (1400, 975), (W, 995)]), SAND)

# the second racer, a little behind
s.extend(camel2(1520, 1290, 430, facing=1, body=DUNE, blanket=BLUE, band=GOLD, tassel=GOLD, gallop=True,
                name="camel2", halter=GOLD, tassels=3))
seat2, mouth2 = camel2.seat, camel2.mouth
H2 = 520
s.extend(human(seat2[0], seat2[1] + H2 * 0.48, H2, outfit="thobe", head="ghutra", child=True, seated_y=seat2[1],
               hands=[(seat2[0] - 180, seat2[1] - 320), (seat2[0] + 200, seat2[1] - 90)], look=1, name="boy2"))
s.line([human.hands[1], mouth2], 5)

# the hero: Najdi boy in thobe, shemagh and bisht on a decorated racing camel
s.extend(puff(150, 1500, 260, colour=WHITE, name="dust"))
s.extend(camel2(560, 1490, 540, facing=1, body=DUNE, blanket=RED, band=GOLD, tassel=GOLD, gallop=True,
                garland=(BLUE, GREEN, ORANGE), name="camel1"))
seat, mouth = camel2.seat, camel2.mouth
HB = 640
s.extend(human(seat[0], seat[1] + HB * 0.48, HB, outfit="bisht", head="shemagh", accent=RED, cloak=BROWN, child=True,
               seated_y=seat[1], hands=[(seat[0] - 200, seat[1] - 450), (seat[0] + 220, seat[1] - 130)], look=1, name="boy1"))
s.line([human.hands[1], mouth], 6)
s.build(__file__)

"""Market day: a vendor in a wrap and jacket, jasmine garlands round his neck, sells garlands and fuul from clay pots (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(1880, 150, 90))
# old market buildings
s.add("building1", rect(-20, 260, 560, 1000), MUD)
s.add("building1-roof", rect(-30, 230, 580, 280), CREAM)
s.add("building2", rect(1450, 330, 2070, 1000), CREAM)
s.add("building2-roof", rect(1440, 300, 2080, 350), MUD)
for wx in (80, 330):
    s.add("b1-window", arch(wx, 360, wx + 110, 520), BLUE)
for wx in (1560, 1820):
    s.add("b2-window", arch(wx, 420, wx + 110, 580), GREEN)
s.add("street", rect(0, 980, W, H), SAND)
# stall with striped awning
s.add("stall-post", rect(560, 520, 600, 1100), TRUNK)
s.add("stall-post", rect(1440, 520, 1480, 1100), TRUNK)
for k in range(6):
    s.add("awning", [(540 + k * 160, 480), (700 + k * 160, 480), (700 + k * 160, 600), (540 + k * 160, 600)], RED if k % 2 == 0 else WHITE)
for k in range(6):
    s.add("awning-flap", arc(620 + k * 160, 600, 80, 50, 0, 180, 12), RED if k % 2 == 0 else WHITE)
# garlands hanging under the awning
for k, gx in enumerate((760, 1240)):
    s.extend(garland(gx, 650, 200, 200, name="hanging-garland", r=32))
# table with clay fuul pots
s.add("table", rect(60, 1060, 640, 1130), TRUNK)
s.add("table-leg", rect(100, 1130, 150, 1380), TRUNK)
s.add("table-leg", rect(550, 1130, 600, 1380), TRUNK)
s.extend(clay_pot(200, 1065, 240, 260, colour=CLAY, name="pot1", lid=DARK_BROWN))
s.extend(clay_pot(480, 1065, 260, 300, colour=CLAY, name="pot2"))
for k in range(3):
    s.line(smooth_open([(420 + k * 55, 740), (440 + k * 55, 690), (420 + k * 55, 640), (440 + k * 55, 590)], 2), 7)
s.add("bowl", arc(340, 1062, 90, 60, 0, 180, 16) , ORANGE)
# the vendor (hero)
vendor = folk(1080, 1480, 900, name="vendor", skin=SKIN3, top=WHITE, bottom=BLUE, bottom_style="wrap", head="turban", head_col=WHITE,
              extra=("jacket", DARK_BROWN), arms=("down", (0.25, 0.02)), facing=1, hair=None, belt=YELLOW)
hx, hy, hr = folk.head
(lx, ly), (rx, ry) = folk.hands
neck_garlands = garland(hx, hy + hr * 0.7, 2 * hr * 1.1, 260, name="vendor-garland2", colour=JASMINE, r=36)
s.extend(insert_before(vendor, "-face", neck_garlands))
s.extend(garland(hx, hy + hr * 1.15, 2 * hr * 0.75, 130, name="vendor-garland", colour=JASMINE, r=36))
# garland offered in his hand
s.extend(garland(rx + 20, ry, 110, 260, name="offered-garland", r=34))
s.add("vendor-hand", circle(rx, ry, 45), SKIN3)
# small customer: a girl holding out her hand for a garland
s.extend(folk(1720, 1460, 620, name="girl", skin=SKIN, top=YELLOW, bottom=PURPLE, bottom_style="dress", child=True,
              head="headscarf", head_col=GREEN, arms=((0.2, 0.06), "down"), facing=-1))
s.build(__file__)

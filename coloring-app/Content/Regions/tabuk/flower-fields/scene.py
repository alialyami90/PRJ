"""A shepherd girl in an embroidered dress with her lambs in Tabuk's spring flower fields (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import kid, limb, band, lamb, tulip, daisy  # noqa: E402

s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(sun(1800, 190, 100))
s.extend(cloud(400, 180, 400, name="cloud1"))
s.extend(cloud(1150, 260, 300, name="cloud2"))
# far mountains and rolling green hills
s.add("mountains", band([(-20, 640), (300, 480), (560, 590), (900, 430), (1250, 580), (1600, 470), (2070, 600)], 900, 1), ROCK)
s.add("hill-far", band([(-20, 780), (500, 680), (1000, 760), (1500, 690), (2070, 760)], 1000), LEAF)
s.add("meadow", band([(-20, 930), (600, 880), (1300, 930), (2070, 890)], H + 20), GRASS)
# flower patches in the meadow
for fx, fy, c in ((110, 1010, YELLOW), (1940, 1000, YELLOW), (1450, 1150, YELLOW), (1000, 1250, PINK)):
    s.extend(daisy(fx, fy, 72, petal=c, centre=ORANGE, name="meadow-flower"))

# lambs
s.extend(lamb(1720, 1250, 300, facing=-1, name="lamb1"))
s.extend(lamb(1330, 1400, 380, facing=-1, name="lamb2"))
s.extend(lamb(330, 1300, 300, facing=1, name="lamb3"))

# the shepherd girl with her crook
s.extend(kid(820, 1470, 840, outfit="dress", top=PURPLE, accent=RED, headwear="headscarf", hw=BLACK_CLOTH,
             arms=(40, 70), facing=1, name="girl"))
(lx, ly), (rx, ry) = kid.hands
s.add("crook", limb([(lx - 20, 1480), (lx, ly), (lx + 10, ly - 330), (lx + 50, ly - 420), (lx + 120, ly - 420), (lx + 140, ly - 360)], 17, 17, 1), BROWN)
s.add("girl-hand", circle(lx, ly, 840 * 0.042), SKIN)
# she offers a flower to the lamb
s.extend(daisy(rx + 50, ry - 40, 70, petal=WHITE, centre=YELLOW, name="gift"))
s.add("girl-hand", circle(rx, ry, 840 * 0.042), SKIN)

# big foreground flowers
for fx, fh, c in ((120, 330, RED), (240, 260, ORANGE), (1980, 320, RED), (1240, 250, ORANGE), (560, 250, RED)):
    s.extend(tulip(fx, H + 10, fh, colour=c, name="tulip"))
for fx, fy in ((1060, 1460), (1880, 1470), (420, 1470)):
    s.extend(daisy(fx, fy, 65, name="daisy"))
# butterfly
s.add("butterfly", smooth([(1180, 700), (1100, 620), (1080, 730), (1180, 720), (1280, 730), (1260, 620)], 1), YELLOW)
s.add("butterfly-body", ellipse(1180, 700, 20, 50), DARK_BROWN)
s.build(__file__)

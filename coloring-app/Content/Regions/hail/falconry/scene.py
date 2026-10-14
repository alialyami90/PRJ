"""Falconer and his falcon at dawn: a peregrine taking off from the gloved hand of a falconer in bisht and shemagh (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1100), SKY)
s.add("dawn-glow", [(-20, 1100)] + smooth_open([(-20, 520), (700, 420), (1400, 450), (2070, 380)], 2) + [(2070, 1100)], SKY_DUSK)
s.add("sun-rays", star(1500, 840, 330, 250, 14, 0), "#FFE082")
s.add("sun", circle(1500, 840, 220), SUN)
s.extend(cloud(1650, 200, 380, "cloud"))
# Aja mountains at dawn
s.add("mountain", [(-20, 1100)] + smooth_open([(-20, 760), (250, 600), (520, 720), (800, 560), (1080, 760), (1300, 840), (1700, 820),
                                               (1900, 700), (2070, 760)], 2) + [(2070, 1100)], ROCK)
s.add("ground", [(-20, 1560), (-20, 980)] + smooth_open([(-20, 980), (700, 1000), (1400, 960), (2070, 990)], 2) + [(2070, 1560)], SAND)
s.add("dune", [(1200, 1560)] + smooth_open([(1200, 1560), (1500, 1300), (1800, 1240), (2070, 1280)], 2) + [(2070, 1560)], DUNE)

# falcon perch (wakr) in the sand
s.add("perch-post", rect(250, 1000, 305, 1370), BROWN)
s.add("perch-top", ellipse(278, 990, 100, 38), LEAF)
s.add("perch-base", ellipse(278, 1375, 90, 32), DARK_BROWN)
s.extend(bush(470, 1440, 230, LEAF, "bush"))

# saluki hound watching the falcon
s.extend(saluki(1700, 1470, 430, facing=-1, body=CREAM, ear=DUNE))

# the falconer in bisht and red shemagh, launching the falcon from his gloved fist
fx, ffeet, fh = 1170, 1490, 960
glove = (840, 760)
s.extend(human(fx, ffeet, fh, name="falconer", adult=True, facing=-1, outfit="bisht", top=WHITE, cloak=BROWN, trim=GOLD,
               head="shemagh", head_col=RED, beard=DARK_BROWN, shoes=DARK_BROWN,
               hands=(glove, (1330, 1000))))
# leather glove
s.add("glove", smooth([(glove[0] - 50, glove[1] - 40), (glove[0] + 60, glove[1] - 30), (glove[0] + 110, glove[1] + 60),
                       (glove[0] + 50, glove[1] + 100), (glove[0] - 55, glove[1] + 45)], 2), DARK_BROWN)
# the little hood in his other hand
hx, hy = human.hands[1]
s.add("hood-plume", limb([(hx, hy - 90), (hx + 10, hy - 150)], 36), GOLD)
s.add("falcon-hood", smooth([(hx - 60, hy + 20), (hx - 45, hy - 70), (hx, hy - 105), (hx + 45, hy - 70), (hx + 60, hy + 20)], 2), RED)
s.add("falconer-hand", circle(hx, hy + 20, 40), SKIN)

# the falcon taking off
s.extend(falcon(770, 375, 255, facing=-1, back=BLACK_CLOTH))

s.build(__file__)

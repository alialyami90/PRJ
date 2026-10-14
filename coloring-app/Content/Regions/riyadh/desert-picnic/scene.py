"""Desert picnic with tents, a campfire and a falcon (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 950), SKY)
s.extend(sun2(1560, 170, 100))
s.extend(cloud(420, 200, 400, name="cloud"))
s.extend(cloud(1180, 130, 300, name="cloud"))
s.add("far-dune", band([(0, 760), (450, 640), (900, 760), (1400, 650), (W, 760)], 1000), DUNE)
s.add("near-dune", band([(0, 900), (700, 860), (1300, 930), (W, 870)]), SAND)

# goat-hair tent with a sadu rug
s.extend(palm(1890, 960, 600, leaf=GREEN, dates=True, name="palm"))
s.extend(tent_black(80, 900, 1060, 360, colour=BLACK_CLOTH, inside=DARK_BROWN, rug=RED, name="tent"))

# campfire and coffee pot
s.extend(fire(560, 1360, 230, name="fire"))
s.add("picnic-rug", [(700, 1500), (760, 1330), (1180, 1330), (1240, 1500)], BLUE)
s.add("picnic-rug-band", [(735, 1400), (747, 1365), (1193, 1365), (1205, 1400)], YELLOW)
s.extend(dallah(860, 1450, 260, colour=GOLD, name="dallah"))
for cx in (1020, 1120):
    s.add("coffee-cup", [(cx - 40, 1385), (cx + 40, 1385), (cx + 30, 1450), (cx - 30, 1450)], WHITE)

# a boy watching the falcon
s.extend(human(260, 1470, 600, outfit="thobe", head="taqiyah", child=True, hands=[(150, 1180), (420, 980)], look=1, name="boy"))

# the handler in thobe and shemagh, falcon on his gloved arm
HX = 1460
perch = (1150, 930)
s.extend(human(HX, 1480, 940, outfit="thobe", head="shemagh", accent=RED, beard=DARK_BROWN, hands=[perch, (HX + 160, 1180)],
               mitt=BROWN, mitt_side=0, look=-1, name="handler"))
sh = human.shoulders[0]
aw = human.arm_w
fal = falcon(perch[0] + 5, perch[1] - 48, 430, facing=-1, body=BROWN, belly=CREAM, hood=RED, plume=GOLD, name="falcon")
feet = [it for it in fal if it[0] == "region" and it[1] == "falcon-feet"]
s.extend([it for it in fal if not (it[0] == "region" and it[1] == "falcon-feet")])
# the leather gauntlet in front of the tail, the talons gripping it
g0 = (perch[0] + (sh[0] - perch[0]) * 0.45, perch[1] + (sh[1] - perch[1]) * 0.45)
s.add("handler-glove", smooth(limb([g0, perch], aw * 1.25, aw * 1.15), 1), BROWN)
s.extend(feet)
s.build(__file__)

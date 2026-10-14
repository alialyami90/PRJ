"""A storyteller in a bisht points out the carved lion tombs of Dadan to children in thobes (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 500), SKY)
s.extend(cloud(1700, 120, 330))
# the red sandstone cliff with tombs cut into it
s.add("cliff", hill([(0, 230), (180, 160), (420, 190), (640, 120), (980, 150), (1300, 110), (1520, 210), (1700, 260),
                     (1900, 230), (2048, 300)], 1150, 1), ROCK)
# main lion tomb: niche with a frame and a lion carved on each side
s.add("tomb-frame", rect(860, 300, 1200, 680), DUNE)
s.add("tomb-niche", rect(920, 360, 1140, 680), DARK_BROWN)
s.add("tomb-ledge", rect(560, 680, 1500, 740), DUNE)
s.extend(lion(690, 680, 340, facing=-1, name="lion-left"))
s.extend(lion(1370, 680, 340, facing=1, name="lion-right"))
# smaller tombs
for i, (x0, y0, w, hh) in enumerate([(1620, 380, 150, 190), (1830, 560, 140, 180), (330, 330, 150, 190)]):
    s.add(f"small-frame{i}", rect(x0 - 25, y0 - 25, x0 + w + 25, y0 + hh), DUNE)
    s.add(f"small-niche{i}", rect(x0, y0, x0 + w, y0 + hh), DARK_BROWN)
# ground and rocks
s.add("ground", hill([(0, 1080), (600, 1060), (1300, 1090), (2048, 1060)]), SAND)
s.add("boulder", smooth([(1720, 1140), (1760, 1020), (1900, 990), (2048, 1020), (2048, 1150)], 2), MUD)
s.add("boulder2", smooth([(-20, 1130), (0, 1030), (120, 1010), (220, 1060), (230, 1140)], 2), MUD)

# storyteller and children
teller = person(380, 1480, 860, outfit="bisht", robe=WHITE, cloak=BROWN, trim=GOLD, headwear="shemagh", head_colour=RED,
                arms=("down", "high"), facing=1, mouth="open", name="storyteller")
s.extend(teller)
kid1 = person(860, 1460, 560, child=True, outfit="thobe", robe=WHITE, headwear="ghutra", arms=("down", "down"),
              facing=-1, name="boy1")
kid2 = person(1250, 1470, 620, child=True, outfit="thobe", robe=WHITE, headwear="taqiyah", skin=SKIN2,
              arms=("down", "high"), facing=-1, mouth="open", name="boy2")
kid3 = person(1640, 1470, 580, child=True, outfit="dress", robe=GREEN, trim=GOLD, headwear="hijab", head_colour=PINK,
              arms=("down", "down"), facing=-1, name="girl")
s.extend(kid1)
s.extend(kid2)
s.extend(kid3)
s.build(__file__)

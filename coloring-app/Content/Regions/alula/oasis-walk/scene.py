"""Shaded palm oasis walk: frogs and a kingfisher by the stream, kids on the path (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 800), SKY)
s.add("far-cliffs", hill([(0, 560), (200, 520), (380, 600), (900, 620), (1100, 520), (1400, 500), (1600, 590), (2048, 560)], 820, 1), ROCK)
s.add("grass", hill([(0, 760), (500, 740), (1000, 770), (1500, 735), (2048, 760)]), GRASS)
# back palms
for i, (px, base, ph, lean, dates) in enumerate([(230, 830, 580, 0.05, True), (1860, 840, 600, -0.05, False)]):
    s.extend(palm2(px, base, ph, lean=lean, dates=dates, name=f"palm{i}"))
# path winding back between the palms
s.add("path", smooth([(1130, 765), (1210, 765), (1150, 860), (1040, 960), (1060, 1060), (1380, 1140), (620, 1140),
                      (760, 1040), (900, 930), (1060, 840)], 1), SAND)
# kids on the path
boy = person(810, 1110, 570, child=True, outfit="modern", top_style="tshirt", top=RED, bottom=BLUE,
             headwear="cap", head_colour=BLUE, shoes=WHITE, arms=("down", ((0.13, 0.1), (0.27, 0.22))), facing=1, mouth="open", name="boy")
girl = person(1250, 1100, 550, child=True, outfit="modern", top_style="hoodie", top=PURPLE, top_accent="none", bottom=BLUE,
              headwear="hijab", head_colour=PINK, shoes=WHITE, arms=("down", "wave"), facing=-1, name="girl")
s.extend(boy)
s.extend(girl)
# the stream
s.add("stream", hill([(0, 1150), (400, 1120), (900, 1170), (1400, 1130), (2048, 1160)]), SEA)
s.line(smooth_open([(150, 1260), (260, 1245), (360, 1262)], 2), 7)
s.line(smooth_open([(1500, 1240), (1620, 1225), (1730, 1245)], 2), 7)
s.add("near-bank", hill([(0, 1450), (500, 1420), (1100, 1470), (1600, 1430), (2048, 1460)]), GRASS)
# reeds on the left bank
for i, (rx, rh, tilt) in enumerate([(70, 360, -40), (140, 420, 10), (210, 330, 50)]):
    s.add("reed", thick(smooth_open([(rx, 1480), (rx + tilt * 0.5, 1480 - rh * 0.5), (rx + tilt, 1480 - rh)], 2), [44, 36, 10]), LEAF)
# frogs: one on a stone, one on a lily pad
s.add("stone", smooth([(420, 1380), (450, 1300), (620, 1270), (790, 1300), (820, 1380), (620, 1410)], 2), GREY)
s.extend(frog(620, 1320, 330, name="frog1", feet=False))
s.add("lily-pad", ellipse(1250, 1335, 230, 70), LEAF)
s.extend(frog(1250, 1330, 300, name="frog2", feet=False))
# kingfisher on a branch over the water
s.add("branch", thick([(2060, 900), (1880, 960), (1640, 980)], [60, 48, 34]), TRUNK)
s.extend(kingfisher(1790, 965, 300, facing=-1, name="kingfisher"))
# shady palm fronds hanging in from the top corners
for i, (root, tip, bend) in enumerate([((-60, -40), (520, 260), 90), ((-60, 120), (330, 470), 60),
                                       ((2110, -40), (1530, 250), 90), ((2110, 200), (1760, 500), 50)]):
    mid = ((root[0] + tip[0]) / 2, (root[1] + tip[1]) / 2 - bend)
    s.add(f"canopy{i}", smooth([root, (mid[0] - 30, mid[1] - 70), tip, (mid[0] + 30, mid[1] + 70)], 2), LEAF)
s.build(__file__)

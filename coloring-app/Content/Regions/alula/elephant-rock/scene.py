"""Family picnic under Elephant Rock at night, roasting marshmallows under the stars (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

NIGHT = "#3949AB"
s = Scene()
s.add("night-sky", rect(0, 0, W, 1100), NIGHT)
for i, (sx, sy, r) in enumerate([(130, 130, 66), (430, 250, 58), (720, 100, 70), (1010, 210, 60), (1310, 110, 66),
                                 (1480, 360, 58), (1900, 480, 62), (240, 440, 58), (1260, 420, 56), (1880, 110, 60)]):
    s.add(f"star{i}", star(sx, sy, r, r * 0.5, 5), YELLOW)
s.extend(crescent(1620, 200, 110))
s.add("far-hills", hill([(0, 880), (300, 840), (700, 900), (1200, 820), (1500, 760), (1750, 820), (2048, 760)], 1100, 2), DUNE)
# Elephant Rock (Jabal AlFil): body on the left, head and trunk on the right, arch underneath
s.add("elephant-rock", smooth([(150, 1040), (170, 720), (260, 540), (450, 430), (680, 390), (780, 340), (930, 290),
                               (1110, 320), (1230, 420), (1290, 560), (1270, 700), (1250, 860), (1270, 1040), (1130, 1040),
                               (1140, 860), (1130, 740), (1060, 670), (940, 670), (850, 760), (830, 1040)], 2), ROCK)
s.line(smooth_open([(1080, 400), (1000, 500), (1040, 600)], 2), 7)   # ear fold
s.line(smooth_open([(430, 520), (520, 640), (500, 780)], 2), 6)       # cracks
s.line(smooth_open([(640, 420), (700, 520)], 1), 6)
s.add("ground", hill([(0, 1000), (600, 1030), (1300, 990), (2048, 1020)]), SAND)

# rug behind the fire
s.add("rug", [(470, 1230), (1650, 1230), (1760, 1420), (360, 1420)], RED)
s.add("rug-band", [(560, 1275), (1560, 1275), (1630, 1375), (490, 1375)], YELLOW)

# parents standing at the sides
dad = person(300, 1460, 820, outfit="modern", top_style="jacket", top=BLUE, top_accent=GREY, bottom=BLACK_CLOTH,
             shoes=BLACK_CLOTH, headwear="beanie", head_colour=GREEN, arms=("down", "point"), facing=1, name="dad")
s.extend(dad)
mom = person(1790, 1460, 780, outfit="modern_dress", top_style="jacket", top=GREEN, top_accent=GREY, bottom=BLACK_CLOTH,
             shoes=BLACK_CLOTH, headwear="hijab", head_colour=PINK, arms=("front", "front"), facing=-1, name="mom")
s.extend(mom)
(hx0, hy0), (hx1, hy1) = mom.hands
s.add("marshmallow-bag", smooth(rect(hx0 - 30, hy0 - 120, hx1 + 30, hy0 + 30), 1), WHITE)
s.add("bag-label", ellipse((hx0 + hx1) / 2, hy0 - 45, 45, 35), PINK)
for hx, hy in mom.hands:
    s.add("mom-hand", circle(hx, hy, 36), SKIN)

# kids sitting on the rug with roasting sticks
boy = person(600, 1400, 580, child=True, outfit="modern", top_style="hoodie", top=ORANGE, top_accent=YELLOW, bottom=BLUE,
             shoes=BLACK_CLOTH, headwear="hair", hair=BLACK_CLOTH, arms=("down", ((0.12, 0.08), (0.27, 0.0))),
             seated=True, facing=1, mouth="open", name="boy")
girl = person(1520, 1400, 560, child=True, outfit="modern", top_style="jacket", top=PINK, top_accent=WHITE, bottom=BLUE,
              shoes=BLACK_CLOTH, headwear="hijab", head_colour=PURPLE, arms=(((0.12, 0.08), (0.27, 0.0)), "down"),
              seated=True, facing=-1, name="girl")
s.extend(stick_with_treat(boy.hands[1], (990, 1170), name="stick1"))
s.extend(stick_with_treat(girl.hands[0], (1130, 1185), name="stick2"))
s.extend(boy)
s.extend(girl)
s.extend(campfire(1060, 1475, 360))
s.build(__file__)

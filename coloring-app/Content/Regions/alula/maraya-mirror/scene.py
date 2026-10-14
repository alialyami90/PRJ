"""A girl in a modern dress takes a selfie with her reflection at the mirrored Maraya building (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

MIRROR_SKY = "#B3E5FC"
s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.add("sun", circle(1820, 170, 100), SUN)
s.extend(cloud(1350, 200, 360))
# canyon rocks behind the building
s.add("rocks-right", smooth([(1380, 1000), (1420, 560), (1560, 400), (1760, 430), (1900, 560), (1960, 1000)], 2), ROCK)
s.add("rocks-far", hill([(0, 860), (500, 820), (1000, 850), (1500, 800), (2048, 840)], 1060, 2), DUNE)
s.add("ground", hill([(0, 1040), (700, 1060), (1400, 1030), (2048, 1050)]), SAND)

# Maraya: a big mirrored box that reflects the desert
mx0, my0, mx1, my1 = -20, 300, 1220, 1130
s.add("maraya-roof", rect(mx0 - 20, my0 - 40, mx1 + 20, my0 + 6), GREY)
s.add("mirror-sky", rect(mx0, my0, mx1, my1), MIRROR_SKY)
# the box's side face, going back in perspective
sx1 = mx1 + 190
s.add("side-roof", [(mx1 + 20, my0 - 40), (sx1 + 10, my0 + 30), (sx1 + 10, my0 + 62), (mx1 + 20, my0 + 6)], GREY)
s.add("side-sky", [(mx1, my0 + 6), (sx1, my0 + 62), (sx1, my1 - 50), (mx1, my1)], MIRROR_SKY)
s.add("side-rocks", [(mx1, 760), (sx1, 780), (sx1, 920), (mx1, 960)], DUNE)
s.add("side-sand", [(mx1, 960), (sx1, 920), (sx1, my1 - 50), (mx1, my1)], SAND)
s.add("mirror-cloud", smooth([(260, 520), (290, 450), (380, 420), (470, 440), (520, 520)], 2), CLOUD)
s.add("mirror-rocks", [(mx0, 840), (120, 700), (300, 660), (460, 740), (600, 690), (800, 640), (960, 700), (1100, 660),
                       (mx1, 720), (mx1, 960), (mx0, 960)], DUNE)
for i, (gx, gy, gr) in enumerate([(120, 400, 72), (1110, 420, 72)]):
    s.add(f"glint{i}", star(gx, gy, gr, gr * 0.35, 4), WHITE)
s.add("mirror-sand", rect(mx0, 950, mx1, my1), SAND)
# her reflection inside the mirror (mirror image: phone in the left hand)
refl = person(880, 1110, 640, child=True, outfit="modern_dress", top_style="plain", top=RED, bottom=RED, hem=WHITE,
              headwear="hijab", head_colour=PINK, shoes=BLACK_CLOTH, arms=("high", "down"), facing=1, name="reflection")
s.extend(phone(refl.hands[0][0] + 5, refl.hands[0][1] - 55, 90, colour=PURPLE, name="reflection-phone", rot=-12))
s.extend(refl)
s.add("reflection-belt", rect(refl.waist[0] - 82, refl.waist[1] - 40, refl.waist[0] + 82, refl.waist[1] + 5), WHITE)

# the real girl in front
girl = person(1620, 1470, 840, child=True, outfit="modern_dress", top_style="plain", top=RED, bottom=RED, hem=WHITE,
              headwear="hijab", head_colour=PINK, shoes=BLACK_CLOTH, arms=("down", "high"), facing=-1, mouth="open", name="girl")
s.extend(phone(girl.hands[1][0] - 5, girl.hands[1][1] - 70, 115, colour=PURPLE, name="phone", rot=12))
s.extend(girl)
s.add("girl-belt", rect(girl.waist[0] - 108, girl.waist[1] - 50, girl.waist[0] + 108, girl.waist[1] + 6), WHITE)
# desert plants
for bx, by, bw in ((1900, 1180, 140), (90, 1300, 160)):
    s.add("bush", smooth([(bx - bw, by), (bx - bw * 0.8, by - bw * 0.55), (bx - bw * 0.1, by - bw * 0.8), (bx + bw * 0.6, by - bw * 0.6),
                          (bx + bw, by)], 2), GREEN)
s.build(__file__)

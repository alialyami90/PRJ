"""Camel caravan passing the carved tombs of Hegra, led by a Bedouin guide (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

CAMEL = MUD
s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.add("sun", circle(1780, 200, 110), SUN)
s.extend(cloud(1250, 230, 420))
s.extend(cloud(260, 170, 300, name="cloud2"))
# distant sandstone hills
s.add("far-hills", hill([(0, 760), (120, 700), (260, 760), (1200, 780), (1350, 640), (1500, 620), (1620, 720),
                         (1800, 700), (1900, 600), (2048, 620)], 1120, 2), DUNE)
# Qasr al-Farid style rock with carved facade
s.add("tomb-rock", smooth([(260, 1060), (240, 600), (330, 360), (520, 250), (800, 230), (1020, 300), (1150, 480),
                           (1180, 760), (1170, 1060)], 3), ROCK)
fx0, fx1, ftop, fbot = 470, 950, 420, 1050
# crow steps (two stepped half-pyramids) on top of the facade
for cx in (fx0 + 120, fx1 - 120):
    sh, w0, dw = 40, 120, 30
    left, right = [], []
    for k in range(4):
        left += [(cx - w0 + k * dw, ftop - k * sh), (cx - w0 + k * dw, ftop - (k + 1) * sh)]
        right += [(cx + w0 - k * dw, ftop - k * sh), (cx + w0 - k * dw, ftop - (k + 1) * sh)]
    s.add("crow-steps", left + right[::-1], DUNE)
s.add("facade", rect(fx0, ftop, fx1, fbot), DUNE)
s.add("cornice", rect(fx0 - 25, ftop + 70, fx1 + 25, ftop + 130), SAND)
for px in (fx0 + 15, fx1 - 75):
    s.add("pilaster", rect(px, ftop + 130, px + 60, fbot), SAND)
s.add("pediment", [(615, 690), (710, 600), (805, 690)], SAND)
s.add("door", rect(630, 700, 790, fbot), DARK_BROWN)
# ground
s.add("ground", hill([(0, 1050), (500, 1030), (1100, 1060), (1600, 1040), (2048, 1060)]), SAND)
s.add("dune-front", hill([(0, 1380), (400, 1330), (900, 1400), (1400, 1350), (2048, 1420)]), DUNE)
for bx, by, bw in ((140, 1120, 150), (1300, 1110, 130), (1960, 1150, 120)):
    s.add("shrub", smooth([(bx - bw, by), (bx - bw * 0.8, by - bw * 0.5), (bx - bw * 0.2, by - bw * 0.75), (bx + bw * 0.4, by - bw * 0.65),
                           (bx + bw, by - bw * 0.2), (bx + bw, by)], 2), GREEN)

# caravan: second camel behind, lead camel, guide
c2 = camel2(385, 1345, 425, facing=1, body=CAMEL, blanket=BLUE, band_col=YELLOW, tassel=RED, name="camel2")
s.extend(c2)
c1 = camel2(1000, 1450, 540, facing=1, body=CAMEL, blanket=RED, band_col=YELLOW, tassel=ORANGE, name="camel1")

s.extend(c1)
g = person(1780, 1480, 740, outfit="bisht", robe=WHITE, cloak=BROWN, trim=GOLD, headwear="shemagh", head_colour=RED,
           arms=("out", "down"), facing=-1, name="guide")
lh = g.hands[0]
s.extend(g)
s.line(smooth_open([c1.halter, ((c1.halter[0] + lh[0]) / 2, max(c1.halter[1], lh[1]) + 30), lh], 2), 10)
s.line(smooth_open([c2.halter, (c2.halter[0] + 90, c2.halter[1] + 140), (1000 - 0.5 * 540, 1450 - 0.75 * 540)], 2), 10)
s.build(__file__)

"""Tuesday market in Abha: a woman in a colourful Asiri dress selling baskets (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(puff(1700, 130, 320, name="cloud"))
# Abha mud houses with slate bands
s.extend(mountains([(-200, 640), (300, 520), (800, 600), (1300, 480), (1800, 560), (2300, 500)], 1000, GREEN, "hill"))
s.extend(tower_house(1500, 960, 360, 700, wall=MUD, bands=DARK_BROWN, name="house2", floors=3))
s.extend(tower_house(1870, 990, 260, 520, wall=ROCK, name="house3", floors=2))
s.add("ground", rect(0, 960, W, H), SAND)
s.line([(0, 1130), (W, 1110)], 6)

# stall awning
s.add("pole", rect(170, 470, 210, 1120), TRUNK)
s.add("pole", rect(1190, 470, 1230, 1120), TRUNK)
ax0, ax1, ay0, ay1 = 120, 1280, 330, 500
k = 6
sw_ = (ax1 - ax0) / k
for i in range(k):
    x0 = ax0 + i * sw_
    pts = [(x0, ay0), (x0 + sw_, ay0), (x0 + sw_, ay1)] + arc(x0 + sw_ / 2, ay1, sw_ / 2, 50, 0, 180, 12)[1:-1] + [(x0, ay1)]
    s.add("awning", pts, RED if i % 2 == 0 else WHITE)
s.add("awning-top", [(ax0 - 20, ay0 + 10), (ax1 + 20, ay0 + 10), (ax1 - 40, ay0 - 80), (ax0 + 40, ay0 - 80)], YELLOW)

# table with spices
s.add("table-top", rect(130, 980, 1270, 1040), TRUNK)
s.add("table-cloth", [(150, 1040), (1250, 1040), (1230, 1250), (170, 1250)], GREEN)
s.add("cloth-band", [(160, 1170), (1240, 1170), (1232, 1250), (168, 1250)], YELLOW)
for i, (cx, col) in enumerate(((290, RED), (520, ORANGE), (750, YELLOW))):
    s.extend(heap(cx, 985, 210, 150, col, bowl=TRUNK, name="spice"))
s.extend(basket(1030, 985, 240, 140, colour=STRAW, band=PURPLE, name="table-basket", handle=True))

# pottery and baskets on the ground
s.extend(pot(260, 1490, 230, 230, colour=ROCK, band=WHITE, name="jar"))
s.extend(pot(500, 1500, 190, 170, colour=ORANGE, band=None, name="pot"))
s.extend(basket(760, 1500, 260, 160, colour=STRAW, band=RED, name="basket"))
s.extend(basket(1030, 1490, 220, 140, colour=STRAW, band=BLUE, name="basket"))

# young customer reaching for the basket
s.extend(figure(1900, 1490, 600, facing=-1, child=True, top=BLUE, bottom="dress", bands=(PINK,), head="scarf", head_colour=PINK,
                arms=((0.16, 0.1), (-0.1, 0.3)), elbows=((0.08, 0.14), None), shoes=RED, name="girl"))

# basket seller
s.extend(figure(1400, 1470, 900, facing=1, top=PURPLE, bottom="dress", bands=(YELLOW, GREEN), yoke=RED, head="scarf_hat",
                head_colour=GREEN, hat_colour=STRAW, cuffs=GREY, necklace=GREY, arms=((0.12, 0.33), (0.2, 0.28)),
                elbows=(None, (0.12, 0.22)), shoes=DARK_BROWN, name="seller"))
hx, hy = figure.hands[1]
s.extend(basket(hx + 60, hy + 175, 240, 160, colour=STRAW, band=RED, name="offered-basket", handle=True))
s.add("seller-hand", circle(hx, hy, 40), SKIN)
s.build(__file__)

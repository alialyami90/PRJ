"""Morning fish market with fishermen and seagulls (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 700), SKY_DUSK)
s.extend(sun(170, 170, 95))
s.add("sea", rect(0, 640, W, 960), SEA)
s.extend(drop(dhow(470, 770, 600, hull=BROWN, trim=YELLOW, sail=WHITE, facing=1, name="boat", sail2=False), "-mast"))
s.extend(seagull(1080, 230, 320, facing=1, name="gull1"))
s.extend(seagull(760, 110, 310, facing=-1, flap=0.7, name="gull2"))
# harbour ground
s.add("quay-edge", rect(0, 930, W, 990), GREY)
s.add("ground", rect(0, 980, W, H), SAND)
# market stall: posts, striped awning, the seller, then the counter in front of him
for px in (1300, 1880):
    s.add("post", rect(px, 380, px + 40, 1200), BROWN)
s.add("awning-back", rect(1260, 360, 1960, 440), RED)
for i in range(7):
    x0 = 1260 + i * 100
    s.add("awning", arc(x0 + 50, 440, 50, 55, 0, 180, 10) + [(x0, 440), (x0 + 100, 440)], WHITE if i % 2 else RED)
s.extend(drop(person(1610, 1250, 640, outfit="thobe", headwear="turban", cloth=WHITE, accent=GREEN, skin=SKIN2, arms="wave", facing=-1, name="seller"), "-shoe"))
s.add("ice", smooth([(1270, 880), (1320, 820), (1950, 820), (1960, 880)], 1), WHITE)
s.extend(fish(1400, 810, 250, colour=GREY, fin=GREY, facing=1, name="f1"))
s.extend(fish(1840, 810, 240, colour=YELLOW, fin=YELLOW, facing=-1, name="f3"))
s.add("counter", rect(1250, 870, 1980, 960), BROWN)
s.add("counter-front", rect(1270, 960, 1960, 1230), TRUNK)
s.add("crate-band", rect(1270, 1060, 1960, 1110), BROWN)
# basket with fish and a cheeky gull
s.add("basket", smooth([(30, 1300), (50, 1500), (410, 1500), (430, 1300)], 1), YELLOW)
s.line([(60, 1380), (400, 1380)], 6)
s.line([(65, 1440), (395, 1440)], 6)
s.extend(fish(160, 1270, 240, colour=ORANGE, facing=-1, name="bf1"))
s.extend(fish(320, 1280, 230, colour=GREY, fin=GREY, facing=1, name="bf2"))
s.add("basket-rim", rect(20, 1290, 440, 1330), BROWN)
s.extend(gull_standing(1680, 1500, 400, facing=-1, name="gull3"))
# hero fisherman (izar + undershirt + white taqiyah) holding a big hamour
X, FEET, HH = 1040, 1480, 820
g = geom(X, FEET, HH)
fisher = person(X, FEET, HH, outfit="wrap", headwear="taqiyah", cloth=WHITE, accent=BLUE, skin=SKIN2, arms="down", name="fisher")
fisher = drop(fisher, "-sleeve", "-hand", "-belt")
izar = [(X - g["sh_w"] * 1.0, g["waist"] - HH * 0.02), (X + g["sh_w"] * 1.0, g["waist"] - HH * 0.02),
        (X + g["sh_w"] * 1.12, FEET - HH * 0.08), (X - g["sh_w"] * 1.12, FEET - HH * 0.08)]
fisher = [("region", it[1], izar, it[3]) if it[0] == "region" and it[1].endswith("-wrap") else it for it in fisher]
fy = g["waist"] - 20
targets = [(X - 210, fy), (X + 165, fy + 10)]
arms = arms_items(X, FEET, HH, False, targets, WHITE, SKIN2, cap=WHITE, name="fisher")
s.extend([a for a in arms if not a[1].endswith("-hand")])
s.extend(fisher)
for yy in (1250, 1340):
    s.line([(X - g["sh_w"] * 1.02, yy), (X + g["sh_w"] * 1.05, yy)], 6)
s.extend(hamour(X + 10, fy + 10, 760, colour=DUNE, spots=ORANGE, facing=1, name="hamour"))
s.extend([a for a in arms if a[1].endswith("-hand")])
s.build(__file__)

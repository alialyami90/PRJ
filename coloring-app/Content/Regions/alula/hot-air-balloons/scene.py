"""A girl in a hoodie and sunglasses waves from a hot-air balloon over AlUla's sandstone canyons (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(cloud(1500, 560, 380))
s.extend(cloud(240, 300, 300, name="cloud2"))
# canyon landscape far below
s.add("far-ridge", hill([(0, 900), (250, 860), (420, 900), (800, 880), (1150, 820), (1500, 860), (1800, 800), (2048, 840)], 1200, 2), DUNE)
# flat-topped mesas
s.add("mesa1", [(1180, 1200), (1230, 960), (1300, 900), (1560, 900), (1620, 960), (1680, 1200)], ROCK)
s.add("mesa2", [(1600, 1200), (1650, 1010), (1720, 960), (2048, 950), (2048, 1200)], ROCK)
s.add("mesa3", [(0, 1200), (0, 980), (180, 950), (330, 1000), (380, 1200)], ROCK)
for y in (1010, 1080):
    s.line([(1250, y), (1640, y)], 6)
s.line([(1680, 1060), (2040, 1060)], 6)
s.add("valley", hill([(0, 1180), (500, 1150), (1000, 1190), (1500, 1160), (2048, 1180)]), SAND)
s.add("palm-grove", smooth([(380, 1240), (520, 1190), (760, 1200), (980, 1230), (1150, 1210), (1300, 1250), (1260, 1300),
                            (900, 1290), (600, 1300), (400, 1290)], 2), GREEN)
# near canyon walls with layered stripes
s.add("canyon-left", hill([(0, 1260), (200, 1230), (360, 1320), (480, 1420), (560, 1536)], H, 2) if False else
      smooth([(0, 1536), (0, 1250), (180, 1220), (330, 1300), (450, 1420), (540, 1536)], 2), MUD)
s.add("canyon-left-band", smooth([(0, 1400), (300, 1380), (430, 1470), (480, 1536), (0, 1536)], 1), ROCK)
s.add("canyon-right", smooth([(2048, 1536), (2048, 1220), (1850, 1240), (1680, 1330), (1560, 1450), (1500, 1536)], 2), MUD)
s.add("canyon-right-band", smooth([(2048, 1390), (1760, 1400), (1620, 1480), (1580, 1536), (2048, 1536)], 1), ROCK)
s.add("canyon-floor", hill([(0, 1530), (2048, 1530)], H, 1), SAND) if False else None

# distant balloons
for i, (bx, by, bw, cols) in enumerate([(1680, 90, 300, (BLUE, YELLOW, RED)), (1930, 520, 210, (ORANGE, PURPLE, BLUE)),
                                        (260, 560, 230, (PURPLE, YELLOW, ORANGE))]):
    b = balloon(bx, by, bw, colours=cols, name=f"far-balloon{i}", rope=0.22, basket_w=0.42, basket_h=bw * 0.3)
    s.extend(b)
    s.extend(basket_front(b.basket_rect, name=f"far-basket{i}"))

# hero balloon
b = balloon(930, -60, 760, colours=(RED, YELLOW, ORANGE), name="balloon", rope=0.55, basket_w=0.72, basket_h=290)
s.extend(b)
bx0, by0, bx1, by1 = b.basket_rect
gx, kx = 800, 1130
girl = person(gx, by0 + 300, 640, child=True, outfit="modern", top_style="hoodie", top=PINK, top_accent="none",
              bottom=BLUE, headwear="hijab", head_colour=PURPLE, sunglasses=True, arms=("high", ("to", (gx + 125, by0 + 8))),
              facing=1, mouth="open", legs=False, name="girl")
boy = person(kx, by0 + 285, 560, child=True, outfit="modern", top_style="sweater", top=GREEN, top_accent=YELLOW,
             bottom=BLUE, headwear="cap", head_colour=BLUE, arms=(("to", (kx - 115, by0 + 8)), "point"), facing=1, legs=False, name="brother")
s.extend(boy)
s.extend(girl)
s.extend(basket_front(b.basket_rect))
for hx, hy in (girl.hands[1], boy.hands[0]):
    s.add("hand-on-rim", circle(hx, hy, 36), SKIN)
s.build(__file__)

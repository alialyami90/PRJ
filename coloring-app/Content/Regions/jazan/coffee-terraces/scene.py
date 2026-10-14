"""A coffee farmer in a wrap and headwrap picks red coffee cherries into a woven basket on mountain terraces (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(260, 200, 100))
s.extend(cloud(1000, 250, 420))
s.extend(terraced_mountain(1650, 300, 1150, 820, 6, wall=ROCK, name="mtnR", fields=(LEAF, GRASS)))
s.extend(terraced_mountain(500, 520, 1150, 760, 4, wall=ROCK, name="mtnL", fields=(GRASS, LEAF)))
s.extend(stone_house(1560, 340, 170, 220, wall=MUD, trim=WHITE, name="hut", windows=2, door=False))
# middle terrace with a row of small coffee bushes
s.add("mid-wall", smooth([(-200, 1020), (700, 980), (1400, 1010), (W + 200, 970), (W + 200, H + 200), (-200, H + 200)], 2), ROCK)
s.add("mid-field", smooth([(-200, 1070), (700, 1030), (1400, 1060), (W + 200, 1020), (W + 200, H + 200), (-200, H + 200)], 2), GRASS)
for i, bx in enumerate((1310,)):
    s.extend(coffee_bush(bx, 1120, 340, 260, name=f"bgbush{i}", cherries=((0.12, -0.1),)))
# front terrace
s.add("front-wall", smooth([(-200, 1210), (700, 1180), (1400, 1210), (W + 200, 1180), (W + 200, H + 200), (-200, H + 200)], 2), ROCK)
s.add("front-field", smooth([(-200, 1270), (700, 1240), (1400, 1270), (W + 200, 1240), (W + 200, H + 200), (-200, H + 200)], 2), "#A1887F")
# big coffee bushes
s.extend(coffee_bush(540, 1440, 680, 560, name="bush1", cherries=((-0.3, -0.05), (-0.08, 0.2), (0.12, -0.28), (0.28, 0.1), (-0.15, -0.3))))
s.extend(coffee_bush(1740, 1450, 620, 520, name="bush2", cherries=((-0.25, 0.05), (0.0, -0.28), (0.22, 0.18), (0.28, -0.12))))
# the coffee farmer (hero) reaching into the bush
farmer = folk(1100, 1480, 900, name="farmer", skin=SKIN3, top=WHITE, bottom=ORANGE, bottom_style="wrap", head="turban", head_col=YELLOW,
              hair=None, arms=((0.26, 0.0), "hold"), facing=-1, shoes=DARK_BROWN, belt=GREEN)
s.extend(farmer)
(lx, ly), (rx, ry) = folk.hands
s.add("picked-cherry", circle(lx - 40, ly - 40, 34), RED)
# basket strap and basket at the waist
s.add("strap", tube([(1000, 1000), (1100, 1100), (1210, 1200)], 34, 34, smooth_it=1), DARK_BROWN)
s.extend(woven_basket(1170, 1190, 250, 170, colour=STRAW, band=GREEN, name="basket"))
for k, (cx, cy) in enumerate(((1110, 1180), (1170, 1165), (1230, 1182))):
    s.add("basket-cherry", circle(cx, cy, 36), RED)
s.build(__file__)

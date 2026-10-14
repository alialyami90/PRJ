"""Kids in T-shirts picking mangoes with a farmer in a straw hat at a Jazan mango farm (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(1840, 190, 105))
s.extend(cloud(1300, 230, 380))
s.add("hill", smooth([(-200, 900), (400, 760), (1100, 820), (1700, 740), (W + 200, 820), (W + 200, 1100), (-200, 1100)], 2), GRASS)
# orchard rows in the distance
for i, tx in enumerate((1180, 1480, 1790, 2060)):
    s.extend(mango_tree(tx, 1000, 420, name=f"bgtree{i}"))
s.add("field", smooth([(-200, 1000), (700, 960), (1400, 990), (W + 200, 950), (W + 200, H + 200), (-200, H + 200)], 2), GRASS)
s.line(smooth_open([(1100, 1120), (1500, 1100), (2000, 1110)], 2), 6)
# big mango tree
s.extend(mango_tree(620, 1260, 920, name="tree", fruit_pos=((-0.36, -0.05), (-0.2, 0.1), (0.05, -0.15), (0.3, 0.06), (0.4, -0.12),
                                                                (-0.08, 0.13), (0.18, 0.15), (-0.3, -0.2), (0.12, -0.02))))
# girl reaching for a mango
s.extend(folk(470, 1440, 600, name="girl", top=PINK, bottom=BLUE, sleeves="short", child=True, hair=DARK_BROWN,
              head="headscarf", head_col=PURPLE, arms=("reach", "reach"), facing=1))
(lx, ly), (rx, ry) = folk.hands
s.extend(mango(rx + 15, ry - 115, 150, name="picked"))
# boy carrying a basket of mangoes
boy = folk(900, 1460, 600, name="boy", top=RED, bottom=BLUE, bottom_style="trousers", sleeves="short", child=True, hair=DARK_BROWN,
           arms=("hold", "hold"), facing=1, skin=SKIN2)
s.extend(boy)
for i, (mx, my) in enumerate(((840, 1190), (905, 1170), (965, 1195))):
    s.extend(mango(mx, my, 110, rot=20 * (i - 1), name=f"basket-mango{i}"))
s.extend(woven_basket(900, 1215, 260, 150, colour=STRAW, band=RED, name="basket"))
# farmer in a straw hat with a crate
s.extend(folk(1500, 1480, 900, name="farmer", top=WHITE, bottom=DARK_BROWN, sleeves="long", sleeve_col=WHITE, head="straw_hat", head_col=RED,
              arms=("hold", "hold"), facing=-1, skin=SKIN3, extra=("vest", LEAF)))
for i, mx in enumerate((1395, 1500, 1605)):
    s.extend(mango(mx, 1150, 130, rot=-15 + 15 * i, name=f"crate-mango{i}"))
s.extend(crate(1340, 1160, 1660, 1350, colour=ORANGE, name="crate"))
s.extend(crate(1730, 1340, 2000, 1480, colour=ORANGE, name="crate2"))
for i, mx in enumerate((1790, 1870, 1945)):
    s.extend(mango(mx, 1320, 100, name=f"crate2-mango{i}"))
s.build(__file__)

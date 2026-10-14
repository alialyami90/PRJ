"""A farmer in a colourful wrap, jacket and flower headband on the green terraces of the Fifa Mountains (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(1850, 170, 95))
# far mountain on the left
s.extend(terraced_mountain(150, 470, 1250, 560, 5, wall=ROCK, name="left", fields=(LEAF, GRASS)))
s.extend(terraced_mountain(1950, 560, 1250, 450, 4, wall=ROCK, name="right", fields=(LEAF, GRASS)))
# main terraced mountain with the village on top
s.extend(terraced_mountain(1130, 370, 1250, 760, 6, field=GRASS, wall=ROCK, name="fifa", fields=(GRASS, LEAF)))
for i, (hx, hw, hh, col) in enumerate(((930, 160, 200, MUD), (1065, 180, 290, CREAM), (1220, 160, 230, MUD))):
    s.extend(stone_house(hx, 440, hw, hh, wall=col, trim=WHITE if col == MUD else MUD, name=f"house{i}", windows=1 if hw < 170 else 2, door=False))
s.extend(cloud(560, 330, 380, name="cloud1"))
s.extend(cloud(1640, 420, 420, name="cloud2"))
# near terrace field (foreground)
s.add("near-wall", smooth([(-200, 1180), (500, 1120), (1200, 1150), (W + 200, 1100), (W + 200, H + 200), (-200, H + 200)], 2), ROCK)
s.add("near-field", smooth([(-200, 1230), (500, 1180), (1200, 1210), (W + 200, 1160), (W + 200, H + 200), (-200, H + 200)], 2), GRASS)
for y0 in (1330, 1440):
    s.line(smooth_open([(40, y0), (700, y0 - 30), (1300, y0 - 10), (2010, y0 - 40)], 2), 6)
# sorghum plants along the terrace
for i, px in enumerate((90, 1680, 1960)):
    s.add(f"plant{i}-stem", tube([(px, 1300), (px + 5, 1050)], 26), LEAF)
    s.add(f"plant{i}-leaf", ellipse(px - 55, 1180, 70, 24, rot=-30), LEAF)
    s.add(f"plant{i}-leaf2", ellipse(px + 60, 1130, 70, 24, rot=30), LEAF)
    s.add(f"plant{i}-head", blob(px + 5, 1010, 45, 70, seed=i), ORANGE)
# goat
s.extend(goat(470, 1450, 320, facing=1, body=WHITE, patch=DARK_BROWN, name="goat"))
# the farmer (hero)
farmer = folk(1180, 1460, 880, name="farmer", skin=SKIN3, top=WHITE, bottom=PURPLE, bottom_style="wrap", head="flower_band",
              hair=BLACK_CLOTH, extra=("jacket", DARK_BROWN), arms=("wave", (0.16, 0.08)), facing=1, shoes=DARK_BROWN, belt=ORANGE)
hx, hy = folk.hands[1]
s.extend(hoe(hx, hy, 640, angle_deg=-78, colour=DARK_BROWN))
s.extend(farmer)
s.add("farmer-wrap-band", [(1180 - 129, 1460 - 0.17 * 880 - 50), (1180 + 129, 1460 - 0.17 * 880 - 50), (1180 + 133, 1460 - 0.17 * 880 - 2), (1180 - 133, 1460 - 0.17 * 880 - 2)], YELLOW)
s.build(__file__)

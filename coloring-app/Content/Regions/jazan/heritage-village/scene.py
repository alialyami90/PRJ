"""A woman in a bright Jazani dress and jasmine crown weaves a straw hat outside the straw-roofed huts of a heritage village (traditional)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(1000, 170, 95))
s.extend(cloud(420, 200, 380))
s.extend(cloud(1500, 150, 300, name="cloud2"))
s.add("ground", smooth([(-200, 980), (800, 940), (1500, 960), (W + 200, 930), (W + 200, H + 200), (-200, H + 200)], 2), SAND)
# huts
s.extend(fat_palm(1960, 1000, 620, name="palm", lean=-0.08))
s.extend(thatched_hut(1630, 1060, 520, 720, wall=MUD, roof=STRAW, name="hut2", band=RED))
s.extend(thatched_hut(330, 1080, 600, 820, wall=CREAM, roof=STRAW, name="hut1", band=BLUE))
s.extend(goat(290, 1420, 300, facing=1, body=WHITE, patch=DARK_BROWN, name="goat"))
# mat
s.add("mat", smooth([(560, 1500), (620, 1330), (1500, 1330), (1580, 1500)], 1), ORANGE)
s.line(smooth_open([(640, 1420), (1070, 1410), (1500, 1420)], 1), 6)
# basket of palm-leaf strips
for k, (dx, ang) in enumerate(((-50, -110), (0, -90), (50, -70))):
    a = math.radians(ang)
    s.add("strip", tube([(1420 + dx, 1330), (1420 + dx + math.cos(a) * 200, 1330 + math.sin(a) * 200)], 40, 34, smooth_it=0), STRAW)
s.extend(woven_basket(1420, 1290, 220, 140, colour=STRAW, band=GREEN, name="basket"))
# weaver (hero): seated, dress + headscarf + jasmine crown
s.extend(folk(980, 1430, 1150, name="weaver", skin=SKIN2, top=PINK, bottom=YELLOW, bottom_style="dress", head="headscarf", head_col=PURPLE,
              arms=("hold", "hold"), facing=0, seated=True, shoes=DARK_BROWN))
hx, hy, hr = folk.head
s.extend(jasmine_crown(hx, hy, hr, name="crown"))
# half-woven straw hat in her hands
(lx, ly), (rx, ry) = folk.hands
s.add("hat-brim", ellipse(980, ly + 40, 230, 70), STRAW)
s.add("hat-crown", arc(980, ly + 30, 120, 120, 180, 360), STRAW)
s.line(smooth_open([(870, ly - 10), (980, ly - 30), (1090, ly - 10)], 1), 6)
s.line(smooth_open([(800, ly + 60), (980, ly + 85), (1160, ly + 60)], 1), 6)
s.add("weaver-hand", circle(lx, ly + 20, 52), SKIN2)
s.add("weaver-hand", circle(rx, ry + 20, 52), SKIN2)
# daughter showing off a finished hat
s.extend(folk(1780, 1470, 620, name="girl", skin=SKIN, top=GREEN, bottom=RED, bottom_style="dress", child=True, hair=DARK_BROWN,
              head="straw_hat", head_col=RED, arms=("wave", "down"), facing=-1))
s.build(__file__)

"""Flamingos wading at the Farasan Islands while a fisherman waves from his boat (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 760), SKY)
s.extend(sun(1330, 190, 105))
s.extend(cloud(520, 220, 440))
s.extend(cloud(1760, 330, 300, name="cloud2"))
s.add("sea", rect(0, 700, W, H), DEEP_SEA)
# far island: coral-stone house and palms
s.add("island", smooth([(-80, 800), (-60, 720), (300, 660), (700, 650), (1000, 700), (1150, 780), (1150, 830), (-80, 830)], 2), SAND)
s.add("house", rect(330, 470, 640, 680), CREAM)
s.add("house-top", rect(310, 440, 660, 480), CREAM)
s.add("house-door", arch(450, 560, 520, 680), BLUE)
for wx in (365, 560):
    s.add("house-window", arch(wx, 520, wx + 50, 600), BLUE)
s.extend(fat_palm(880, 720, 420, name="palm1"))
s.extend(fat_palm(150, 740, 400, name="palm2", lean=-0.06))
# boat with fisherman
fisher = folk(1560, 900, 600, name="fisher", top=YELLOW, bottom=BLUE, sleeves="short", head="cap", head_col=RED,
              arms=("wave", (0.12, 0.12)), facing=-1, skin=SKIN2)
hx, hy = folk.hands[1]
s.add("rod", tube([(hx - 30, hy + 40), (hx + 140, hy - 200), (hx + 260, hy - 440)], 22, 14, smooth_it=1), DARK_BROWN)
s.line([(hx + 260, hy - 440), (hx + 320, hy - 150), (hx + 320, 905)], 5)
s.extend(fisher)
s.extend(boat(1540, 905, 720, hull=WHITE, stripe=RED, name="boat", facing=-1))
s.add("motor", smooth([(1880, 790), (1960, 790), (1960, 880), (1925, 970), (1905, 970), (1880, 880)], 1), GREY)
# shallow lagoon in front
s.add("shallows", smooth([(-300, 1020), (500, 960), (1100, 1000), (1700, 970), (W + 300, 1010), (W + 300, H + 300), (-300, H + 300)], 2), SEA)
s.add("sandbar", smooth([(-300, 1440), (300, 1350), (800, 1400), (1150, 1500), (1250, H + 300), (-300, H + 300)], 2), SAND)
s.add("shell", smooth([(850, 1500), (900, 1440), (950, 1500)], 1) , PINK)
s.extend(fish(1700, 1300, 230, colour=ORANGE, name="fish1", facing=-1))
s.extend(fish(1880, 1440, 200, colour=RED, name="fish2", facing=-1))
# flamingos (heroes)
s.extend(flamingo(1320, 1250, 620, facing=-1, name="flamingo3"))
s.extend(flamingo(300, 1420, 640, facing=1, name="flamingo2", pose="two-legs", head_down=True))
s.extend(flamingo(760, 1340, 820, facing=1, name="flamingo1"))
for (rx, ry, rw) in ((780, 1340, 100), (1320, 1250, 80)):
    s.line(arc(rx, ry, rw, rw * 0.22, 0, 180, 14), 6)
s.build(__file__)

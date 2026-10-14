"""Desert rally: buggies jumping over the Hail dunes, a driver in racing suit beside his buggy (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(sun(1850, 180, 100))
s.extend(cloud(1250, 170, 360, "cloud"))
s.add("far-dune", smooth([(-50, 1000), (-50, 640), (350, 560), (800, 650), (1150, 640), (1420, 560), (1700, 680), (2100, 640), (2100, 1000)], 2), DUNE)
# the jump dune with a crest on the left
s.add("jump-dune", [(-20, 1100), (-20, 800)] + smooth_open([(-20, 800), (300, 720), (560, 640), (640, 650)], 2)
      + smooth_open([(640, 650), (900, 820), (1300, 900), (2070, 880)], 2) + [(2070, 1100)], ORANGE)
s.line(smooth_open([(200, 860), (420, 800), (560, 760)], 2), 6)
s.add("ground", [(-20, 1560), (-20, 1060)] + smooth_open([(-20, 1060), (500, 1000), (1100, 1050), (2070, 990)], 2) + [(2070, 1560)], SAND)

# a rally 4x4 leaping over the far dune
s.extend(dust(1400, 600, 200, CREAM, "dust3"))
s.extend(rally_car(1660, 600, 420, facing=1, body=GREEN, tilt=-8, name="car"))

# buggy flying off the crest
s.extend(dust(470, 640, 300, CREAM, "dust"))
s.extend(dust(260, 700, 220, CREAM, "dust2"))
s.extend(buggy(960, 520, 600, facing=1, body=BLUE, trim=YELLOW, driver_helmet=RED, visor=GREY, tilt=-12, name="jumper"))
for k in range(3):
    s.line([(540 - k * 25, 330 + k * 60), (650 - k * 25, 330 + k * 60)], 8)

# checkered flag on a pole
s.add("flag-pole", limb([(130, 1420), (130, 880)], 30), GREY)
fx0, fy0, sq = 144, 890, 72
for i in range(4):
    for j in range(3):
        s.add("flag", rect(fx0 + i * sq, fy0 + j * sq, fx0 + (i + 1) * sq, fy0 + (j + 1) * sq), BLACK_CLOTH if (i + j) % 2 else WHITE)
s.add("flag-top", circle(130, 870, 32), YELLOW)

# the driver's own buggy parked in the foreground
s.extend(buggy(1520, 1440, 880, facing=-1, body=RED, trim=YELLOW, name="buggy"))
s.extend(dust(1990, 1430, 160, CREAM, "puff"))

# the hero: driver in racing suit, helmet under his arm, waving
s.extend(human(800, 1470, 880, name="driver", adult=True, facing=1, outfit="racing", top=ORANGE, accent=BLUE,
               shoes=BLACK_CLOTH, head="none", hair=DARK_BROWN, hands=((610, 1080), (1040, 690))))
hx, hy = human.hands[0]
s.add("helmet", circle(hx - 15, hy - 70, 110), WHITE)
s.add("helmet-stripe", limb(arc(hx - 15, hy - 70, 80, 80, 200, 340, 10), 34), BLUE)
s.add("helmet-visor", smooth([(hx - 120, hy - 95), (hx - 40, hy - 105), (hx - 30, hy - 20), (hx - 110, hy - 25)], 2), GREY)
s.add("driver-hand", circle(hx + 40, hy + 5, 37), SKIN)
s.build(__file__)

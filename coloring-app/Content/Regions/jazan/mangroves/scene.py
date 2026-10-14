"""Kids in life jackets kayak through the mangrove forest while a heron and crabs watch from the roots (modern)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(1020, 160, 90))
s.extend(cloud(1500, 200, 360))
s.add("far-mangroves", smooth([(-100, 760), (-80, 600), (150, 540), (350, 600), (600, 520), (850, 590), (1100, 530), (1350, 600),
                               (1600, 530), (1850, 590), (W + 100, 540), (W + 100, 760)], 2), GRASS)
s.add("water", rect(0, 720, W, H), SEA)
for wy, wx in ((1350, 820), (1380, 1150), (800, 1250)):
    s.line(smooth_open([(wx, wy), (wx + 60, wy - 15), (wx + 120, wy), (wx + 180, wy - 15)], 1), 6)
s.extend(mangrove(330, 1010, 820, name="mangrove1"))
s.extend(mangrove(1760, 980, 760, name="mangrove2"))
# mud bank with crabs (front left) and heron (front right)
s.add("mudbank-left", smooth([(-200, 1300), (200, 1240), (620, 1300), (760, 1420), (760, H + 200), (-200, H + 200)], 2), "#A1887F")
s.add("mudbank-right", smooth([(1500, H + 200), (1560, 1360), (1800, 1290), (W + 200, 1300), (W + 200, H + 200)], 2), "#A1887F")
s.extend(crab(210, 1410, 280, name="crab1", colour=RED, wave=True))
s.extend(crab(560, 1450, 220, name="crab2", colour=ORANGE))
s.extend(heron(1840, 1420, 760, facing=-1, name="heron", wing=BLACK_CLOTH))
# kayak with two kids paddling
for (kx, name, hc, head, sk, hair, top) in ((760, "kid1", PINK, "headscarf", SKIN, DARK_BROWN, RED), (1190, "kid2", RED, "cap", SKIN2, BLACK_CLOTH, WHITE)):
    kid = folk(kx, 1265, 600, name=name, top=top, bottom=BLUE, sleeves="short", child=True, hair=hair, head=head, head_col=hc,
               extra=("lifejacket", ORANGE), arms=((0.1, 0.1), (0.13, -0.05)), facing=1, skin=sk, seated=True)
    (lx, ly), (rx, ry) = folk.hands
    s.extend(kid)
    dx, dy = rx - lx, ry - ly
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    s.extend(paddle(lx - ux * 150, ly - uy * 150, rx + ux * 150, ry + uy * 150, colour=DARK_BROWN, blade=RED, name=f"{name}-paddle"))
    s.add(f"{name}-hand", circle(lx, ly, 40), sk)
    s.add(f"{name}-hand", circle(rx, ry, 40), sk)
s.extend(kayak(980, 1290, 1150, colour=YELLOW, name="kayak"))
s.build(__file__)

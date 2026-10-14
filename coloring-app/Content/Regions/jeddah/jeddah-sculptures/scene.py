"""Playing hide and seek among the giant sculptures of the Corniche (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

HORIZON, PROM = 740, 1050
s = Scene()
s.add("sky", rect(0, 0, W, HORIZON), SKY)
s.extend(sun(1840, 180, 100))
s.extend(cloud(520, 230, 380))
s.extend(cloud(1300, 160, 260))
s.add("sea", rect(0, HORIZON, W, PROM), SEA)
s.line(arc(300, 880, 60, 20, 200, 340, 10), 6)
s.line(arc(1980, 900, 40, 14, 200, 340, 10), 6)
s.add("promenade", rect(0, PROM, W, H), SAND)
s.add("grass", smooth_open([(0, 1300), (700, 1260), (1400, 1320), (W, 1280)], 2) + [(W, H), (0, H)], GRASS)

# the giant bicycle sculpture on its plinth
R = 330
FW, RW = (860, 1040 - R), (1600, 1040 - R)
D = RW[0] - FW[0]
def B(fx, fy):
    return (FW[0] + fx * D, FW[1] + fy * D)
bands = [(0, HORIZON, SKY, "sky"), (HORIZON, PROM, SEA, "sea"), (PROM, 2000, SAND, "prom")]
# a girl peeking out from behind the back wheel
s.extend(drop(shorts_kid(1925, 1250, 560, shirt=PINK, shorts=BLUE, headwear="headscarf", cap=PURPLE, long_trousers=True,
                         arms=("out", (1985, 1060)), facing=-1, name="girl"), "-scarf-front"))
s.add("plinth", rect(560, 1080, 1890, 1260), GREY)
s.add("plinth-top", rect(530, 1030, 1920, 1090), WHITE)
s.extend(wheel(*RW, R, bands, name="rear"))
s.extend(wheel(*FW, R, bands, name="front"))
BB, SEAT, HEAD = B(0.518, 0.054), B(0.768, -0.482), B(0.16, -0.482)
bw = 0.075 * D
for a, b in ((RW, BB), (RW, SEAT), (SEAT, BB), (HEAD, BB), (HEAD, SEAT)):
    s.add("frame", bar(a, b, bw), RED)
s.add("fork", bar(FW, HEAD, bw), RED)
s.add("stem", bar(HEAD, B(0.107, -0.643), bw), RED)
s.add("handlebar", tube([B(0.232, -0.652), B(0.071, -0.67), B(-0.054, -0.643), B(-0.08, -0.518)], bw * 0.95), BLACK_CLOTH)
s.add("seat", smooth([B(0.66, -0.47), B(0.73, -0.54), B(0.96, -0.56), B(0.99, -0.49), B(0.89, -0.45)], 2), BLACK_CLOTH)
s.add("crank", circle(*BB, 0.09 * D), YELLOW)
s.add("crank-arm", bar(BB, B(0.38, -0.12), bw * 0.7), YELLOW)
s.add("pedal", rect(*B(0.3, -0.16), *B(0.44, -0.09)), BLACK_CLOTH)

# a boy hiding behind a bush
boy = shorts_kid(230, 1560, 560, shirt=YELLOW, shorts=BLUE, headwear="cap", cap=RED, arms=((150, 1150), (330, 1160)), facing=1, name="boy")
s.extend([it for it in boy if not (it[0] == "region" and it[1].endswith("-hand"))])
s.add("bush", smooth([(-40, 1536), (-40, 1200), (100, 1110), (260, 1140), (380, 1190), (440, 1300), (460, 1536)], 2), GREEN)
for hx, hy in ((150, 1150), (330, 1160)):
    s.add("boy-hand", circle(hx, hy, 36), SKIN)
for bx, by in ((120, 1230), (300, 1260), (200, 1400)):
    s.line(arc(bx, by, 50, 30, 200, 340, 8), 6)

# the hero: the seeker counting with hands over the eyes
X, FEET, HH = 1240, 1520, 700
g = geom(X, FEET, HH, child=True)
kid = shorts_kid(X, FEET, HH, shirt=ORANGE, shorts=BLUE, hair_colour=DARK_BROWN, arms=("down", "down"), name="seeker")
kid = drop(kid, "-sleeve", "-hand", "-tsleeve")
r = g["head_r"]
eyes = [(X - r * 0.42, g["head_cy"] - r * 0.05), (X + r * 0.42, g["head_cy"] - r * 0.05)]
arms = arms_items(X, FEET, HH, True, eyes, ORANGE, SKIN, cap=ORANGE, name="seeker", cap_frac=0.3)
for i, it in enumerate(kid):
    if it[0] == "region" and it[1].endswith("-face"):
        kid = kid[:i] + [a for a in arms if not a[1].endswith("-hand")] + kid[i:]
        break
s.extend(kid)
for hx, hy in eyes:
    s.add("seeker-hand", smooth([(hx - r * 0.42, hy + r * 0.45), (hx - r * 0.5, hy - r * 0.3), (hx - r * 0.2, hy - r * 0.6), (hx + r * 0.2, hy - r * 0.62),
                                 (hx + r * 0.5, hy - r * 0.3), (hx + r * 0.42, hy + r * 0.45)], 2), SKIN)
    for fx in (-0.18, 0.0, 0.18):
        s.line([(hx + r * fx, hy - r * 0.5), (hx + r * fx, hy - r * 0.15)], 5)
s.build(__file__)

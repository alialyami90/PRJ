"""A boy leading his donkey up the stone steps of Rijal Almaa village (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.extend(puff(300, 150, 340, name="cloud"))
s.extend(mountains([(-100, 480), (350, 260), (800, 420), (1300, 230), (1750, 400), (2150, 280)], 1000, LEAF, "mountain"))
s.add("hillside", smooth([(-400, 900), (600, 820), (1300, 860), (2450, 800), (2450, H + 400), (-400, H + 400)], 3), GRASS)
# tower houses of the village
s.extend(tower_house(60, 960, 240, 520, wall=ROCK, name="house1", floors=3))
s.extend(tower_house(330, 930, 300, 640, wall=MUD, name="house2", floors=3))
s.extend(tower_house(680, 950, 220, 450, wall=ROCK, name="house3", floors=2))
s.extend(tower_house(1430, 900, 260, 600, wall=MUD, name="house4", floors=3))
s.extend(tower_house(1740, 930, 250, 480, wall=ROCK, name="house5", floors=2))

# stone stairway climbing to the right
n = 10
tread = W / n
RISE = 46
tops = [1470 - i * RISE for i in range(n)]
sil = [(-20, H + 20), (-20, tops[0])]
for i in range(n):
    sil += [(i * tread, tops[i]), ((i + 1) * tread, tops[i])]
sil += [(W + 20, tops[-1]), (W + 20, H + 20)]
s.add("stairs", sil, ROCK)
for i in range(n):
    x0 = i * tread
    s.add("tread", [(x0 - 4, tops[i]), (x0 + tread + 4, tops[i]), (x0 + tread + 4, tops[i] - 34), (x0 - 4, tops[i] - 34)], SAND)
    if i:
        s.line([(x0, tops[i]), (x0, tops[i - 1])], 6)
    # masonry joints on the stair face below this tread
    row = 0
    y = tops[i] + 75
    while y < H - 20:
        s.line([(x0 + 6, y), (x0 + tread - 6, y)], 6)
        off = 0.25 if row % 2 else 0.75
        s.line([(x0 + tread * off, y), (x0 + tread * off, min(y + 75, H))], 6)
        row += 1
        y += 75


def step_top(x):
    i = max(0, min(n - 1, int(x // tread)))
    return tops[i] - 34


# donkey climbing behind the boy
dx, dfeet = 800, step_top(800) + 20
don = donkey(dx, dfeet, 420, facing=1, body=GREY, muzzle=CREAM, mane=DARK_BROWN, blanket=RED, bags=ORANGE, name="donkey")
for it in don:
    if it[0] == "region":
        s.add(it[1], rotate(it[2], -9, dx, dfeet), it[3])
    elif it[0] == "ink":
        s.ink(rotate(it[1], -9, dx, dfeet))
    else:
        s.line(rotate(it[1], -9, dx, dfeet), *(it[2:]))

# boy leading with a rope
bx = 1530
s.extend(figure(bx, step_top(bx) + 18, 640, facing=-1, child=True, top=WHITE, jacket=RED, jacket_trim=YELLOW, bottom="wrap", bottom_colour=BLUE,
                belt=BROWN, head="wrap", head_colour=ORANGE, arms=((0.28, -0.04), (0.08, 0.32)), elbows=((0.16, 0.12), None), name="boy"))
hx, hy = figure.hands[0]
head = rotate([(dx + 0.95 * 420, dfeet - 1.18 * 420)], -9, dx, dfeet)[0]
s.line(smooth_open([head, ((head[0] + hx) / 2, max(head[1], hy) + 70), (hx, hy)], 3), 10)
s.add("boy-hand", circle(hx, hy, 32), SKIN)
s.build(__file__)

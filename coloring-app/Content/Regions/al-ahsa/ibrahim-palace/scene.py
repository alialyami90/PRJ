"""A boy in a thobe and bisht rides a black Arabian horse past Ibrahim Palace in Hofuf (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403


def tower(cx, base_y, top_y, w, colour=ROCK, name="tower"):
    items = [("region", name, [(cx - w / 2, base_y), (cx - w / 2 + 15, top_y), (cx + w / 2 - 15, top_y), (cx + w / 2, base_y)], colour)]
    n = 3
    mw = (w - 30) / n
    for i in range(n):
        x0 = cx - w / 2 + 15 + i * mw
        items.append(("region", f"{name}-merlon", [(x0 + 4, top_y + 2), (x0 + mw - 4, top_y + 2), (x0 + mw / 2, top_y - mw * 0.85)], colour))
    items.append(("region", f"{name}-window", arch(cx - 28, top_y + 90, cx + 28, top_y + 200), DARK_BROWN))
    return items


def rider(x, seat_y, h, facing=1, hands=None, cloak=BROWN, headcol=RED, name="rider", outfit="bisht", head="shemagh"):
    """Frontal child rider whose thobe drapes over the horse; one shoe peeks below the hem."""
    feet = seat_y + h * 0.42
    items, info = figure(x, feet, h, outfit, head, skin=SKIN, accent=cloak, headcol=headcol, child=True,
                         look=0.5 * facing, legs=False, lhand=hands[0] if hands else None,
                         rhand=hands[1] if hands else None, name=name)
    items.append(("region", f"{name}-shoe", ellipse(x + facing * h * 0.12, feet - h * 0.01, h * 0.085, h * 0.045, rot=10 * facing), DARK_BROWN))
    return items, info


s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.add("sun", circle(1820, 170, 100), SUN)
s.extend(cloud(330, 200, 360))
# Ibrahim Palace: mud walls, the white dome of the Al-Quba mosque, round towers
s.add("dome-base", rect(990, 420, 1330, 620), CREAM)
s.add("dome", arc(1160, 430, 165, 190, 180, 360), WHITE)
s.line([(1160, 240), (1160, 190)], 9)
s.add("dome-finial", circle(1160, 180, 34), GOLD)
s.add("palace-wall", rect(0, 560, W, 1000), MUD)
for i in range(13):
    x0 = i * 160 + 5
    if 140 < x0 + 80 < 520 or 1520 < x0 + 80 < 1920 or 960 < x0 + 80 < 1360:
        continue
    s.add("wall-merlon", [(x0 + 15, 562), (x0 + 145, 562), (x0 + 80, 470)], MUD)
s.extend(tower(330, 1000, 420, 300, name="tower-left"))
s.extend(tower(1720, 1000, 400, 320, name="tower-right"))
s.add("gate", arch(1040, 700, 1300, 1000), DARK_BROWN)
s.line([(1170, 830), (1170, 1000)], 7)
s.add("ground", smooth_open([(0, 980), (700, 960), (1400, 990), (W, 970)], 2) + [(W, H), (0, H)], SAND)
s.extend(big_palm(120, 1080, 620, lean=10, w=90, span=0.8, n_leaves=5, name="palm"))

# a second rider in the distance on a brown horse
items, hinfo = horse2(1650, 1200, 380, facing=1, body=BROWN, mane=DARK_BROWN, name="horse-far", prance=False)
s.extend(items)
Pf = hinfo["P"]
fs = Pf(-0.04, 1.0)
items, finfo = rider(fs[0], fs[1], 450, facing=1, headcol=WHITE, name="far-rider", outfit="thobe", head="wrap",
                     hands=([(fs[0] + 40, fs[1] - 60), (fs[0] + 150, fs[1] - 90)], [(fs[0] + 110, fs[1] - 10), (fs[0] + 200, fs[1] - 30)]))
s.extend(items)

# hero: black Arabian horse with a tasselled bridle
H0 = 620
hx0, hfeet = 800, 1450
items, hinfo = horse2(hx0, hfeet, H0, facing=1, body=BLACK_CLOTH, mane=BLACK_CLOTH, name="horse")
P = hinfo["P"]
s.extend(items)
# saddle blanket with fringe tassels
s.add("blanket", smooth([P(-0.3, 1.05), P(0.22, 1.05), P(0.26, 0.66), P(-0.34, 0.66)], 1), RED)
s.add("blanket-band", [P(-0.33, 0.76), P(0.255, 0.76), P(0.26, 0.66), P(-0.34, 0.66)], GOLD)
for tx in (-0.24, -0.04, 0.16):
    s.add("blanket-tassel", teardrop(*P(tx, 0.68), 66, 120), YELLOW)
# breast collar with tassels
s.add("breast-collar", thick([P(0.3, 1.0), P(0.48, 0.92), P(0.58, 0.78)], 44, 44), RED)
s.add("collar-tassel", teardrop(*P(0.48, 0.92), 64, 120), YELLOW)
# bridle: straps and tassels on the head
s.line([P(0.66, 1.46), P(0.7, 1.24), P(0.86, 1.1)], 10)
s.line([P(0.84, 1.3), P(0.9, 1.12)], 10)
s.add("brow-tassel", teardrop(*P(0.69, 1.4), 64, 120), RED)

# the boy rider in a thobe and bisht
seat = P(-0.06, 1.02)
hands = ([(seat[0] + 30, seat[1] - 80), (seat[0] + 160, seat[1] - 120)], [(seat[0] + 230, seat[1] - 60), (seat[0] + 200, seat[1] - 140)])
items, rinfo = rider(seat[0], seat[1], 600, facing=1, hands=hands, name="boy")
s.extend(items)
bit = hinfo["bit"]
for hx, hy in rinfo["hands"]:
    s.line([(hx, hy), bit], 7)
for hx, hy in rinfo["hands"]:
    s.add("boy-hand2", circle(hx, hy, 34), SKIN)
s.build(__file__)

"""A bisht weaver works golden thread at his loom, helped by a boy (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("wall", rect(0, 0, W, 1120), CREAM)
s.add("wall-band", rect(0, 0, W, 90), MUD)
s.add("window", arch(1180, 200, 1460, 560), SKY)
s.add("window-sun", circle(1320, 430, 70), SUN)
s.add("window-frame", [(1160, 560), (1480, 560), (1480, 600), (1160, 600)], MUD)
s.add("floor", rect(0, 1120, W, H), SAND)
s.add("rug", [(250, 1300), (1700, 1300), (1850, 1500), (100, 1500)], RED)
s.add("rug-band", [(320, 1340), (1640, 1340), (1720, 1460), (230, 1460)], ORANGE)

# the loom: wooden frame, warp threads and the cloth growing at the bottom
s.add("loom-post", rect(130, 220, 210, 1440), BROWN)
s.add("loom-post", rect(760, 220, 840, 1440), BROWN)
s.add("loom-top", rect(100, 230, 870, 300), BROWN)
s.add("warp", rect(210, 300, 760, 1000), WHITE)
for wx in range(250, 760, 55):
    s.line([(wx, 300), (wx, 1000)], 5)
s.add("cloth", rect(210, 1000, 760, 1320), BLACK_CLOTH)
s.add("cloth-gold", rect(210, 1000, 760, 1080), GOLD)
s.add("loom-beam", rect(100, 1320, 870, 1390), BROWN)
s.add("heddle", rect(190, 640, 780, 700), DARK_BROWN)

# the finished bisht on its stand
s.add("stand", rect(1785, 380, 1825, 1400), BROWN)
s.add("stand-foot", rect(1680, 1390, 1930, 1440), BROWN)
cloak = smooth([(1805, 450), (1640, 500), (1585, 620), (1570, 900), (1600, 1230), (2010, 1230), (2040, 900), (2025, 620), (1970, 500)], 2)
s.add("bisht-cloak", cloak, BROWN)
s.add("bisht-inside", [(1765, 480), (1845, 480), (1890, 1225), (1720, 1225)], CREAM)
for sx in (-1, 1):
    s.add("bisht-trim", [(1805 + sx * 40, 470), (1805 + sx * 100, 480), (1805 + sx * 150, 1225), (1805 + sx * 85, 1225)], GOLD)
s.add("bisht-collar", smooth([(1660, 500), (1805, 430), (1950, 500), (1920, 545), (1805, 490), (1690, 545)], 1), GOLD)
s.line(smooth_open([(1620, 700), (1600, 950), (1625, 1180)], 2), 6)
s.line(smooth_open([(1990, 700), (2010, 950), (1985, 1180)], 2), 6)

# the weaver passing golden thread through the warp
items, info = figure(1080, 1450, 860, "thobe", "ghutra", skin=SKIN2, beard=BLACK_CLOTH, look=-0.5,
                     lhand=[(880, 960), (700, 900)], rhand=[(1250, 1060), (1180, 1130)], name="weaver")
s.extend(items)
s.add("shuttle", smooth([(560, 870), (720, 860), (780, 890), (720, 920), (560, 920), (520, 895)], 1), BROWN)
# small spool in his other hand, its golden thread running to the shuttle
s.add("spool", rect(1120, 990, 1240, 1090), GOLD)
s.add("spool-end", rect(1100, 965, 1260, 1000), BROWN)
s.add("spool-end", rect(1100, 1080, 1260, 1115), BROWN)
s.add("gold-thread", thick(smooth_open([(1120, 1030), (950, 1080), (800, 1010), (720, 905)], 2), 26), GOLD)
s.add("weaver-hand2", circle(700, 895, 40), SKIN2)
s.add("weaver-hand3", circle(1180, 1130, 40), SKIN2)

# the boy helper carrying a big spool of golden thread
items, binfo = figure(1400, 1470, 600, "thobe", "taqiyah", skin=SKIN, child=True, look=-0.4,
                      lhand=[(1300, 1230), (1320, 1200)], rhand=[(1500, 1230), (1480, 1200)], name="boy")
s.extend(items)
s.add("big-spool", rect(1300, 1120, 1500, 1290), GOLD)
for yy in (1165, 1210, 1250):
    s.line([(1310, yy), (1490, yy)], 5)
s.add("big-spool-end", rect(1280, 1090, 1520, 1130), BROWN)
s.add("big-spool-end", rect(1280, 1280, 1520, 1320), BROWN)
for hx in (1300, 1500):
    s.add("boy-hand2", circle(hx, 1205, 36), SKIN)
s.build(__file__)

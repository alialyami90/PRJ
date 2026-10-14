"""Traditional dhow sailing past the city at sunset (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

HOR = 900
s = Scene()
s.add("sky", rect(0, 0, W, HOR), SKY_DUSK)
s.add("sky-glow", smooth_open([(0, 560), (700, 520), (1400, 560), (W, 520)], 2) + [(W, HOR), (0, HOR)], "#FFD8A8")
s.extend(sun(1700, 820, 150))
s.extend(cloud(1550, 260, 380))
# city skyline
city = [(1180, 900), (1180, 700), (1260, 700), (1260, 640), (1340, 640), (1340, 760), (1420, 760), (1420, 560), (1460, 500),
        (1500, 560), (1500, 900)]
s.add("city", city, PURPLE)
s.add("city2", [(1860, 900), (1860, 720), (1940, 720), (1940, 620), (2000, 620), (2000, 700), (W, 700), (W, 900)], PURPLE)
s.add("minaret", rect(1590, 640, 1650, 900), PURPLE)
s.add("minaret-top", arc(1620, 640, 30, 60, 180, 360) + [(1650, 640)], PURPLE)
s.add("sea", rect(0, HOR, W, H), SEA)
for wx, wy in ((1500, 1010), (1850, 1120), (1300, 1430), (1900, 1380)):
    s.line(arc(wx, wy, 60, 20, 200, 340, 10), 6)
s.add("sun-path", smooth([(1600, 905), (1800, 905), (1760, 960), (1640, 960)], 1), "#FFD8A8")
s.extend(seagull(1860, 500, 320, facing=-1, name="gull1"))
s.extend(seagull(1480, 420, 300, facing=-1, flap=0.7, name="gull2"))

# the dhow
CX, WL, L = 820, 1340, 1300
boat = dhow(CX, WL, L, hull=BROWN, trim=GOLD, sail=CREAM, facing=1, name="dhow", sail2=False)
k = next(i for i, it in enumerate(boat) if it[0] == "region" and it[1].endswith("-hull"))
s.extend(boat[:k])
# sailor at the tiller: izar, sidriya vest, turban
SX, SF, SH = 520, 1110, 640
g = geom(SX, SF, SH)
sailor = person(SX, SF, SH, outfit="wrap", headwear="turban", cloth=WHITE, accent=GREEN, skin=SKIN2, arms="down", facing=1, name="sailor")
sailor = drop(sailor, "-sleeve", "-hand")
izar = [(SX - g["sh_w"], g["waist"] - SH * 0.02), (SX + g["sh_w"], g["waist"] - SH * 0.02),
        (SX + g["sh_w"] * 1.12, SF - SH * 0.08), (SX - g["sh_w"] * 1.12, SF - SH * 0.08)]
sailor = [("region", it[1], izar, it[3]) if it[0] == "region" and it[1].endswith("-wrap") else it for it in sailor]
tiller_hand = (SX - 230, g["waist"] - 10)
targets = [tiller_hand, arm_target(SX, SF, SH, False, 1, "up")]
arms = arms_items(SX, SF, SH, False, targets, WHITE, SKIN2, name="sailor")
s.extend([arms[0], arms[2]])
s.extend(insert_after(sailor, "-belt", vest(SX, SF, SH, RED, trim=GOLD, name="sidriya")))
s.extend([arms[1], arms[3]])
# tiller from the rudder post to his hand
post = (170, 1010)
s.add("tiller", bar(tiller_hand, post, 34), DARK_BROWN)
s.add("sailor-hand2", circle(*tiller_hand, g["sh_w"] * 0.36), SKIN2)
s.extend(boat[k:])
# portholes / decoration on the hull
for px in (600, 820, 1040):
    s.add("porthole", circle(px, WL - 200, 34), GOLD)
s.add("wave-front", smooth_open([(0, 1400), (300, 1370), (700, 1420), (1100, 1380), (1500, 1420), (W, 1390)], 2) + [(W, H), (0, H)], DEEP_SEA)
s.build(__file__)

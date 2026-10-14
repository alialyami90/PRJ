"""A family in a cable car over the green mountains to Al-Souda (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

GLASS = "#BBDEFB"
s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(puff(250, 200, 360, name="cloud"))
s.extend(puff(1780, 140, 300, name="cloud"))
# Al-Souda peak on the right with the summit station
s.extend(mountains([(-100, 700), (300, 520), (700, 640), (1100, 470), (1500, 330), (1760, 250), (2100, 380)], 1000, LEAF, "far-mountain"))
s.add("station", rect(1690, 190, 1880, 290), WHITE)
s.add("station-roof", [(1670, 195), (1785, 130), (1900, 195)], RED)
s.add("station-window", rect(1740, 220, 1830, 270), GLASS)
s.extend(puff(1500, 470, 700, 110, name="fog"))
s.extend(mountains([(-200, 900), (250, 760), (650, 900), (1000, 820), (1500, 960), (2000, 800), (2300, 900)], 1300, GRASS, "near-mountain"))
s.add("valley", smooth([(-400, 1250), (500, 1150), (1000, 1250), (1500, 1180), (2450, 1260), (2450, H + 400), (-400, H + 400)], 3), GREEN)
for i, (tx, ty, th) in enumerate(((180, 1150, 260), (1640, 1150, 270), (1880, 1200, 300), (1520, 1460, 280), (1830, 1500, 320), (130, 1500, 300))):
    s.extend(juniper(tx, ty, th, name=f"tree{i}"))

# cables and a second cabin going down the valley
s.line([(0, 120), (W, 470)], 10)
s.line([(0, 60), (W, 400)], 10)
c2x = 1650
c2y = 120 + (470 - 120) * c2x / W
s.add("cabin2-arm", thick([(c2x, c2y), (c2x, c2y + 90)], 32), GREY)
s.add("cabin2", rrect(c2x - 110, c2y + 80, c2x + 110, c2y + 260, 30), YELLOW)
s.add("cabin2-window", rrect(c2x - 80, c2y + 110, c2x + 80, c2y + 190, 18), GLASS)

# main cabin
cx = 900
cy = 120 + (470 - 120) * cx / W
s.add("grip", rrect(cx - 70, cy - 40, cx + 70, cy + 40, 16), GREY)
s.add("arm", thick([(cx, cy + 20), (cx, 400)], 46), GREY)
s.add("roof", smooth([(380, 520), (420, 400), (1380, 400), (1420, 520)], 2), RED)
s.add("cabin", rrect(340, 470, 1460, 1440, 70), RED)
s.add("window", rrect(410, 550, 1390, 1230, 40), GLASS)

# family (feet on the cabin floor, legs hidden by the lower panel)
FLOOR = 1350
s.extend(figure(610, FLOOR, 720, facing=1, top=PURPLE, bottom="trousers", bottom_colour=BLUE, head="scarf", head_colour=PINK,
                skin=SKIN2, arms=((0.07, -0.3), (0.074, 0.336)), elbows=((0.14, -0.08), None), zip_line=True, name="mom"))
s.extend(figure(925, FLOOR, 770, facing=1, top=GREEN, bottom="trousers", bottom_colour=BLUE, head="none", hair=DARK_BROWN, beard=True,
                arms=((0.078, 0.36), (0.24, -0.2)), elbows=(None, (0.15, -0.02)), point=(False, True), zip_line=True, name="dad"))
s.extend(figure(1220, FLOOR - 30, 540, facing=1, child=True, top=ORANGE, bottom="trousers", bottom_colour=BLUE, head="cap", head_colour=RED,
                arms=((0.06, 0.34), (0.3, -0.06)), elbows=(None, (0.15, 0.05)), point=(False, True), zip_line=True, name="kid"))
s.add("held-hands", circle(760, 1080, 38), SKIN)
s.add("panel", rrect(340, 1190, 1460, 1440, 60), RED)
s.add("panel-stripe", rect(340, 1250, 1460, 1320), WHITE)
s.build(__file__)

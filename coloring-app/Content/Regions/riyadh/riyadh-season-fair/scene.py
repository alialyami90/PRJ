"""Ferris wheel and fireworks at a Riyadh Season fair (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

NIGHT = "#283593"
s = Scene()
s.add("night-sky", rect(0, 0, W, 1150), NIGHT)
s.add("moon", crescent(1860, 180, 100, 50, -35, 90), CREAM)
for (fx, fy, fr, col) in ((280, 230, 150, PINK), (760, 140, 110, YELLOW), (1600, 330, 140, GREEN), (1330, 120, 95, ORANGE)):
    s.extend(firework(fx, fy, fr, col, name="firework", rays=10))
for (sx, sy) in ((560, 330), (1080, 90), (1990, 420), (90, 470), (1450, 520)):
    s.ink(star(sx, sy, 22, 9, 5))

# ferris wheel behind the fair
s.extend(ferris_wheel(1040, 620, 420, 1130, rim=PURPLE, inner=NIGHT, legs=GREY, name="wheel"))
# a striped carousel-style tent on the left
s.add("tent", [(60, 1130), (60, 860), (430, 860), (430, 1130)], WHITE)
s.add("tent-roof", smooth([(20, 880), (245, 640), (470, 880)], 1) + [(470, 880), (20, 880)], RED)
for x0 in (60, 190, 310):
    s.add("tent-stripe", rect(x0 + 30, 860, x0 + 90, 1130), RED)
s.add("tent-pole", rect(230, 520, 260, 650), GREY)
s.add("tent-flag", [(260, 520), (370, 555), (260, 600)], YELLOW)
s.add("plaza", band([(0, 1120), (W, 1120)], H, 1), SAND)
for k in range(-4, 5):
    s.line([(1040 + k * 120, 1130), (1040 + k * 420, H)], 5)
s.line([(0, 1300), (W, 1300)], 5)
# balloons tied to a post on the right
s.add("post", rect(1945, 760, 1975, 1130), GREY)
for (bx_, by_, col) in ((1870, 640, RED), (1985, 560, YELLOW), (1960, 720, GREEN)):
    s.line([(bx_, by_ + 75), (1960, 770)], 5)
    s.add("balloon", ellipse(bx_, by_, 62, 75), col)

# teen cousins in jeans and hoodies with cotton candy
BX, GX = 1600, 520
s.extend(human(BX, 1490, 880, outfit="hoodie", head="hair", child=False, top=GREEN, pants=BLUE, accent=YELLOW, shoes=WHITE,
               hood=True, hands=[(BX - 200, 1150), (BX + 230, 1020)], look=-1, name="boy"))
s.extend(cotton_candy(BX + 230, 1020, 200, colour=BLUE, name="candy"))
s.add("boy-hand2", circle(BX + 230, 1020, 40), SKIN)
s.extend(human(GX, 1490, 860, outfit="hoodie", head="hijab", child=False, top=ORANGE, pants=BLUE, accent=PURPLE, shoes=WHITE,
               hands=[(GX - 230, 1000), (GX + 210, 1150)], look=1, name="girl"))
s.extend(cotton_candy(GX - 230, 1000, 210, colour=PINK, name="candy"))
s.add("girl-hand2", circle(GX - 230, 1000, 40), SKIN)
s.build(__file__)

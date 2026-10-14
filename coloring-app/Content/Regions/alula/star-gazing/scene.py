"""Kids in sweaters look through a telescope under the Milky Way while a desert fox peeks at them (modern)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

NIGHT, MILKY = "#3949AB", "#7986CB"
s = Scene()
s.add("night-sky", rect(0, 0, W, 1000), NIGHT)
s.add("milky-way", smooth([(-60, 820), (300, 560), (800, 330), (1300, 160), (1800, 20), (2110, -40), (2110, 240),
                           (1700, 330), (1250, 440), (800, 620), (350, 840), (-60, 1000)], 2), MILKY)
for i, (sx, sy, r) in enumerate([(160, 160, 60), (520, 260, 56), (900, 120, 64), (1180, 330, 56), (1560, 160, 62),
                                 (1880, 400, 58), (420, 620, 54), (1000, 470, 60), (1500, 520, 56), (240, 420, 50),
                                 (1880, 110, 52), (700, 480, 50)]):
    s.add(f"star{i}", star(sx, sy, r, r * 0.5, 5), YELLOW)
s.add("hills", hill([(0, 900), (300, 840), (520, 900), (900, 860), (1300, 820), (1600, 880), (2048, 830)], 1080, 2), ROCK)
s.add("ground", hill([(0, 1040), (800, 1020), (1500, 1050), (2048, 1030)]), SAND)

# the girl pointing at the sky
girl = person(330, 1460, 640, child=True, outfit="modern", top_style="sweater", top=GREEN, top_accent=YELLOW, bottom=BLUE,
              shoes=BLACK_CLOTH, headwear="hijab", head_colour=PURPLE, arms=("down", "high"), facing=1, mouth="open", name="girl")
s.extend(girl)
# the boy at the telescope eyepiece
bx = 820
th = 780
a = math.radians(-35)
L = th * 0.75
_tmp = person(bx, 1470, 600, child=True)
_hx, _hy, _hr = _tmp.head
_eye = (_hx + _hr * 0.75, _hy)
_head = (_eye[0] + math.cos(a) * L * 0.54, _eye[1] + math.sin(a) * L * 0.54)
TUBE_PT = (_head[0] - math.cos(a) * L * 0.12, _head[1] - math.sin(a) * L * 0.12)
boy = person(bx, 1470, 600, child=True, outfit="modern", top_style="sweater", top=RED, top_accent=WHITE, bottom=BLUE,
             shoes=BLACK_CLOTH, headwear="beanie", head_colour=RED, arms=("down", ("to", TUBE_PT)), facing=1, name="boy")
s.extend(boy)
hx, hy, hr = boy.head
eye = (hx + hr * 0.75, hy)
th = 780
a = math.radians(-35)
L = th * 0.75
head = (eye[0] + math.cos(a) * L * 0.54, eye[1] + math.sin(a) * L * 0.54)
s.extend(telescope(head[0], head[1] + th * 0.62, th, tube=BLUE, legs=GREY, angle=-35, name="scope"))
s.add("boy-hand2", circle(*TUBE_PT, 36), SKIN)

# the fox peeking out from behind a rock
s.extend(fox(1690, 1420, 600, facing=-1, name="fox"))
s.add("rock", smooth([(1360, 1520), (1400, 1320), (1560, 1240), (1780, 1250), (1860, 1400), (1830, 1520)], 2), GREY)
s.add("rock2", smooth([(1880, 1480), (1900, 1380), (2000, 1340), (2080, 1380), (2080, 1480)], 2), GREY)
s.build(__file__)

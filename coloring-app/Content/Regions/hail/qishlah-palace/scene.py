"""Horse parade in front of Al-Qishlah Palace: white Arabian horses with embroidered saddles, riders in bishts (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403


def rider(horse_x, horse_feet, horse_h, facing, h, cloak, head, head_col, name, wave=True, beard=None, deco=True):
    """Horse + rider in a bisht holding the reins, waving with the other hand."""
    it = arab_horse(horse_x, horse_feet, horse_h, facing=facing, body=WHITE, mane=GREY, hoof=GREY,
                    blanket=RED if name == "rider1" else BLUE, band=GOLD, tassel=YELLOW, name=name + "-horse", step=0.8, deco=deco, seat=False)
    seat = arab_horse.seat
    mouth = arab_horse.mouth
    sx, sy = seat
    feet_y = sy + 0.44 * h
    leg_foot = (sx + facing * h * 0.1, sy + h * 0.33)
    leg_knee = (sx + facing * h * 0.17, sy + h * 0.12)
    rein_hand = (sx + facing * h * 0.33, sy - h * 0.12)
    other = (sx - facing * h * 0.34, sy - h * 0.62) if wave else (sx - facing * h * 0.2, sy - h * 0.1)
    hands = (rein_hand, other) if facing < 0 else (other, rein_hand)
    it.append(R(f"{name}-rein", limb([mouth, (mouth[0] - facing * horse_h * 0.15, mouth[1] + horse_h * 0.05), rein_hand], max(horse_h * 0.04, 22)), GOLD))
    it += human(sx, feet_y, h, name=name, adult=True, facing=facing, outfit="bisht", top=WHITE, cloak=cloak, trim=GOLD,
                head=head, head_col=head_col, shoes=DARK_BROWN, seated_y=sy, beard=beard,
                feet=(leg_foot, leg_foot), knees=(leg_knee, leg_knee), hands=hands)
    return it


s = Scene()
s.add("sky", rect(0, 0, W, 1000), SKY)
s.add("sun", circle(1600, 140, 95), SUN)
s.extend(cloud(330, 140, 340, "cloud"))

# Al-Qishlah Palace: two-storey mud fortress with corner towers and pointed crenellations
PX0, PX1, PTOP, PBOT = 120, 1930, 370, 960
teeth = []
for k in range(11):
    tx = PX0 + 40 + k * 160
    teeth += [(tx, PTOP), (tx + 55, PTOP - 85), (tx + 110, PTOP)]
s.add("palace-wall", [(PX0, PBOT), (PX0, PTOP)] + teeth + [(PX1, PTOP), (PX1, PBOT)], MUD)
s.line([(PX0 + 10, 650), (PX1 - 10, 650)], 6)
for i, tx in enumerate((60, 900, 1810)):
    w = 220 if i != 1 else 250
    n = 2 if i != 1 else 3
    cw = (w - 36) / n
    top = []
    for k in range(n):
        cx0 = tx + 18 + k * cw
        top += [(cx0, 250), (cx0 + cw / 2, 170), (cx0 + cw, 250)]
    s.add("tower", [(tx, PBOT)] + top + [(tx + w, PBOT)], SAND)
    for wy in (370, 520):
        cx = tx + w / 2
        s.ink([(cx - 26, wy + 50), (cx + 26, wy + 50), (cx, wy)])
# upper-floor windows
for wx in list(range(270, 880, 150)) + list(range(1240, 1800, 150)):
    s.ink([(wx - 24, 560), (wx + 24, 560), (wx, 515)])
s.add("ground", rect(0, 940, W, H), SAND)
s.line(smooth_open([(0, 1100), (700, 1060), (1400, 1080), (2048, 1050)], 2), 6)

# second horse and rider behind
s.extend(rider(1450, 1250, 420, 1, 650, DARK_BROWN, "ghutra", WHITE, "rider2", deco=False))
# the hero horse and rider
s.extend(rider(700, 1480, 560, 1, 760, BROWN, "shemagh", RED, "rider1", beard=DARK_BROWN))

# boy cheering with a little green flag
bx, bfeet = 1780, 1500
s.extend(human(bx, bfeet, 560, name="boy", facing=-1, outfit="thobe", top=WHITE, head="taqiyah" if False else "ghutra",
               shoes=DARK_BROWN, mouth="open", hands=((1650, 1000), (1910, 1000))))
s.build(__file__)

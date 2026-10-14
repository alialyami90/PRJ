"""Hijazi wedding with mizmar dancers and lanterns (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("night-sky", rect(0, 0, W, 1100), DEEP_SEA)
s.add("moon", circle(1300, 150, 85), CREAM)
for sx, sy in ((300, 110), (720, 120), (1040, 150), (1700, 170)):
    s.add("star", star(sx, sy, 62, 30), YELLOW)
# houses with rawashin on both sides
s.add("house-left", rect(0, 260, 520, 1150), CORAL_STONE)
s.add("house-left-top", rect(0, 220, 560, 280), MUD)
s.extend(roshan(110, 380, 300, 320, wood=GREEN, panel=LEAF, name="roshan-l"))
s.add("door-left", arch(170, 840, 380, 1150), BROWN)
s.add("house-right", rect(1540, 300, W, 1150), CORAL_STONE)
s.add("house-right-top", rect(1500, 260, W, 320), MUD)
s.extend(roshan(1640, 410, 300, 320, wood=BROWN, panel=TRUNK, name="roshan-r"))
s.add("door-right", arch(1700, 860, 1900, 1150), GREEN)
s.add("ground", rect(0, 1100, W, H), SAND)
s.add("carpet", [(380, 1330), (1660, 1330), (1800, 1520), (240, 1520)], RED)
s.add("carpet-band", [(460, 1370), (1590, 1370), (1660, 1470), (390, 1470)], GOLD)
# string of lanterns
s.line(smooth_open([(520, 290), (800, 360), (1040, 395), (1290, 380), (1540, 320)], 2), 6)
for lx, ly, col in ((760, 345, ORANGE), (1040, 382, PINK), (1290, 370, ORANGE), (1460, 340, PINK)):
    s.extend(lantern(lx, ly, 220, colour=GOLD, glass=col, name="lantern"))

def dancer(x, feet, h, vest_col, wrap_col, stick_side, name, stick_col=BROWN):
    """Mizmar dancer: white thobe, embroidered sidriya vest, headwrap, stick held high."""
    g = geom(x, feet, h)
    items = person(x, feet, h, outfit="thobe", headwear="turban", cloth=WHITE, accent=wrap_col, skin=SKIN2,
                   arms="down", name=name)
    items = drop(items, "-sleeve", "-hand")
    up = arm_target(x, feet, h, False, stick_side, "up")
    other = arm_target(x, feet, h, False, -stick_side, "out")
    targets = [up, other] if stick_side == -1 else [other, up]
    arms = arms_items(x, feet, h, False, targets, WHITE, SKIN2, name=name)
    # long stick held in the raised hand, tilted
    a = (up[0] - stick_side * h * 0.06, up[1] + h * 0.14)
    b = (up[0] + stick_side * h * 0.24, up[1] - h * 0.32)
    dancer.tip = b
    stick = [("region", f"{name}-stick", bar(a, b, h * 0.045), stick_col)]
    body = insert_after(items, "-robe", vest(x, feet, h, vest_col, trim=GOLD, name=f"{name}-vest", long=True))
    body = insert_after(body, "-vest-trim", [("region", f"{name}-sash", rect(x - g["sh_w"] * 1.1, g["waist"] - h * 0.02,
                                                                             x + g["sh_w"] * 1.1, g["waist"] + h * 0.04), wrap_col)])
    return [arms[0], arms[2]] + body + stick + [arms[1], arms[3]]

s.extend(dancer(560, 1430, 680, GREEN, ORANGE, 1, "dancer2"))
tip2 = dancer.tip
# drummer
drummer = drop(person(1650, 1440, 640, outfit="thobe", headwear="turban", cloth=WHITE, accent=RED, skin=SKIN3, arms="down", name="drummer"), "-sleeve", "-hand")
darms = arms_items(1650, 1440, 640, False, [(1560, 1090), (1750, 1080)], WHITE, SKIN3, name="drummer")
s.extend([darms[0], darms[2]] + drummer)
s.extend(drum(1650, 1120, 170, body=ORANGE, head=CREAM, name="drum"))
s.extend([darms[1], darms[3]])
# the hero dancer in the middle
s.extend(dancer(1080, 1500, 840, RED, YELLOW, -1, "dancer"))
tip = dancer.tip
s.build(__file__)

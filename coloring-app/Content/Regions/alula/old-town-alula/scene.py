"""A boy in thobe and shemagh carries water jars through AlUla Old Town, castle on the hill (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 900), SKY)
s.extend(cloud(330, 200, 380))
s.extend(cloud(1720, 150, 330, name="cloud2"))
# sandstone cliffs behind the town
s.add("cliffs", hill([(0, 420), (200, 400), (260, 520), (520, 540), (600, 470), (1450, 480), (1550, 380), (1800, 360),
                      (1880, 470), (2048, 450)], 1220, 1), ROCK)
# rocky hill with the castle
s.add("castle-hill", smooth([(640, 1000), (720, 760), (850, 560), (1000, 500), (1200, 510), (1330, 620), (1420, 800), (1480, 1000)], 2), DUNE)
s.add("castle-tower", crenellated(1100, 260, 1260, 560, tooth=40, depth=50), MUD)
s.add("castle-wall", crenellated(890, 390, 1160, 570, tooth=34, depth=45, kind="tri"), MUD)
s.add("castle-window", arch(1155, 320, 1205, 400), DARK_BROWN)
s.add("castle-door", arch(990, 470, 1070, 570), DARK_BROWN)

# old-town mud houses
def house(x0, y0, x1, y1, colour, name, windows=(), door=None, crenels=True):
    s.add(name, crenellated(x0, y0, x1, y1, tooth=36, depth=50, kind="tri") if crenels else rect(x0, y0, x1, y1), colour)
    for wx, wy in windows:
        s.add(name + "-window", rect(wx, wy, wx + 70, wy + 85), DARK_BROWN)
    if door:
        dx, dw = door
        s.add(name + "-door", arch(dx, y1 - 220, dx + dw, y1), DARK_BROWN)

house(-20, 560, 380, 1200, MUD, "house1", windows=[(70, 650), (240, 650), (240, 850)], door=(60, 130))
house(330, 760, 720, 1200, CREAM, "house2", windows=[(420, 840), (590, 840)], door=(500, 120))
house(1360, 720, 1720, 1200, CREAM, "house3", windows=[(1420, 800), (1600, 800)], door=(1470, 120))
house(1680, 540, 2068, 1200, MUD, "house4", windows=[(1770, 630), (1930, 630), (1930, 830)])
s.add("house4-door", arch(1760, 960, 1880, 1200), DARK_BROWN)

# palm peeking between the houses
s.extend(palm2(1340, 1180, 520, lean=-0.05, name="palm"))
# alley floor
s.add("alley", hill([(0, 1190), (500, 1180), (1000, 1200), (1500, 1180), (2048, 1195)]), SAND)
s.add("path", [(760, 1200), (1300, 1200), (1600, 1536), (460, 1536)], DUNE)
# cat on the doorstep
s.extend(cat(250, 1370, 340, facing=1, name="cat"))

# the boy with two water jars
boy = person(1030, 1480, 780, child=True, outfit="thobe", robe=WHITE, headwear="shemagh", head_colour=RED,
             shoes=BROWN, arms=(((0.06, 0.15), (0.11, 0.29)), ((0.06, 0.15), (0.11, 0.29))), name="boy")
s.extend(boy)
for i, (hx, hy) in enumerate(boy.hands):
    s.extend(water_jar(hx, hy + 225, 240, colour=ORANGE, name=f"jar{i}", rim=False))
    s.add("boy-hand", circle(hx, hy, 38), SKIN)
s.build(__file__)

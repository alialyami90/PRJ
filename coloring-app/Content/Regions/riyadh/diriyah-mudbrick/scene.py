"""Family walking through the mud-brick alleys of Diriyah (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 1050), SKY)
s.extend(cloud(1400, 150, 300, name="cloud"))

# far end of the alley: At-Turaif tower and a facade
VX0, VX1, VTOP, VB = 760, 1290, 470, 1010
s.extend(palm(880, 660, 470, leaf=GREEN, dates=True, name="palm"))
s.add("far-tower", najdi_block(1020, 1220, 250, VB, 54, taper=18, step=66), ROCK)
s.extend(tri_window(1120, 340, 48))
s.extend(tri_window(1120, 420, 48))
s.add("far-facade", najdi_block(VX0, VX1, VTOP, VB, 52, step=70), MUD)
for wx in (850, 960, 1100, 1200):
    s.extend(tri_window(wx, 560, 44))
s.add("far-door", arch(980, 760, 1080, VB), DARK_BROWN)

# perspective side walls with stepped crenels
LW = [(0, 130)] + crenel_line((0, 130), (VX0, VTOP - 10), 120, 45, 6)[1:] + [(VX0, VB), (0, 1330)]
s.add("left-wall", LW, MUD)
RW = crenel_line((VX1, VTOP - 10), (W, 110), 45, 120, 6) + [(W, 1330), (VX1, VB)]
s.add("right-wall", RW, ROCK)
# a decorated Najdi door on each wall (painted triangles), plus little vents
ldoor = [(170, 700), (420, 760), (420, 1200), (170, 1270)]
s.add("left-door-frame", [(140, 660), (450, 735), (450, 1210), (140, 1290)], WHITE)
s.add("left-door", ldoor, BLUE)
s.line([quad_lerp(ldoor, 0.5, 0), quad_lerp(ldoor, 0.5, 1)], 6)
for v in (0.25, 0.55):
    for u in (0.25, 0.75):
        a, b, c = quad_lerp(ldoor, u - 0.17, v + 0.12), quad_lerp(ldoor, u, v - 0.06), quad_lerp(ldoor, u + 0.17, v + 0.12)
        s.line([a, b, c, a], 6)
rdoor = [(1640, 790), (1830, 745), (1830, 1210), (1640, 1150)]
s.add("right-door-frame", [(1615, 760), (1860, 705), (1860, 1220), (1615, 1160)], WHITE)
s.add("right-door", rdoor, GREEN)
s.line([quad_lerp(rdoor, 0.5, 0), quad_lerp(rdoor, 0.5, 1)], 6)
for u in (0.25, 0.75):
    a, b, c = quad_lerp(rdoor, u - 0.18, 0.4), quad_lerp(rdoor, u, 0.25), quad_lerp(rdoor, u + 0.18, 0.4)
    s.line([a, b, c, a], 6)
for (wx, wy, sz) in ((560, 640, 60), (640, 700, 50), (250, 470, 80), (1450, 650, 60), (1560, 600, 70), (1900, 460, 90)):
    s.extend(tri_window(wx, wy, sz))

# the path
s.add("path", [(0, 1330), (VX0, VB), (VX1, VB), (W, 1330), (W, H), (0, H)], SAND)
s.line([(330, 1460), (480, 1380)], 6)
s.line([(1600, 1420), (1720, 1470)], 6)

# a cat on the ledge
s.extend(cat(1480, 1170, 230, facing=-1, colour=ORANGE, name="cat"))

# father in thobe and ghutra holding his daughter's hand
FX, GX = 830, 1160
hold = (1000, 1130)
s.extend(human(FX, 1470, 940, outfit="thobe", head="ghutra", robe=WHITE, beard=DARK_BROWN, hands=[(FX - 160, 1150), hold],
               look=1, name="father"))
s.extend(human(GX, 1490, 640, outfit="dress", head="girl_scarf", child=True, robe=RED, accent=PURPLE, skirt=GOLD, emb=GOLD,
               hands=[hold, (GX + 150, 1080)], look=-1, name="girl", front_arms=(True, True)))
s.add("hands", circle(hold[0], hold[1], 40), SKIN)
s.build(__file__)

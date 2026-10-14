"""A crane operator in a hard hat and hi-vis vest waves on the quay at Jazan port, with a container ship and a big crane (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, H), SKY)
s.extend(sun(230, 190, 95))
s.extend(cloud(1050, 170, 360))
s.add("sea", rect(0, 820, W, 1080), SEA)
s.extend(cargo_ship(60, 960, 1250, hull=RED, deck=WHITE, name="ship",
                    stacks=[[BLUE, GREEN, YELLOW, ORANGE, BLUE, GREEN, RED],
                            [ORANGE, BLUE, RED, GREEN, YELLOW, None, None],
                            [None, YELLOW, GREEN, BLUE, None, None, None]]))
s.extend(gantry_crane(1650, 1080, 900, colour=YELLOW, name="crane", reach=600, cab=WHITE, hook_box=PURPLE))
# seagulls
for gx, gy in ((560, 300), (700, 360)):
    s.line(arc(gx - 35, gy, 35, 22, 200, 340, 10), 8)
    s.line(arc(gx + 35, gy, 35, 22, 200, 340, 10), 8)
# quay
s.add("quay-edge", rect(0, 1060, W, 1110), GREY)
s.add("quay", rect(0, 1100, W, H), "#BDBDBD")
for x in range(0, W, 340):
    s.line([(x + 60, 1120), (x - 40, H)], 6)
# containers stacked on the quay
s.extend(container(60, 1250, 330, 160, BLUE, name="quay-box1"))
s.extend(container(400, 1250, 330, 160, RED, name="quay-box2"))
s.extend(container(230, 1080, 330, 160, GREEN, name="quay-box3"))
s.add("bollard", rect(1760, 1200, 1840, 1320), BLACK_CLOTH)
s.add("bollard-cap", ellipse(1800, 1200, 75, 32), BLACK_CLOTH)
# the crane operator (hero), waving
s.extend(folk(1180, 1480, 900, name="operator", skin=SKIN2, top=BLUE, bottom=BLACK_CLOTH, sleeves="long", head="hardhat", head_col=YELLOW,
              extra=("hivis", ORANGE), arms=("wave", "down"), facing=1, hair=None))
s.build(__file__)

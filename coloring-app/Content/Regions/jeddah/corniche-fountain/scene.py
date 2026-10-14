"""Kids on the Corniche watching King Fahd's Fountain and boats (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 760), SKY)
s.extend(sun(260, 200, 110))
s.extend(cloud(760, 230, 360))
s.extend(seagull(1800, 330, 350, facing=-1, name="gull"))
s.extend(seagull(1500, 170, 310, facing=-1, flap=0.8, name="gull2"))
# far city skyline on the horizon
s.add("far-shore", smooth([(0, 760), (0, 700), (300, 690), (600, 705), (900, 690), (W, 700), (W, 760)], 1), DUNE)
for i, (bx, bw, bh) in enumerate(((60, 90, 170), (180, 70, 240), (1720, 100, 200), (1850, 80, 280))):
    s.add("tower", rect(bx, 700 - bh, bx + bw, 705), GREY if i % 2 else WHITE)
s.add("sea", rect(0, 745, W, 1130), SEA)
for wx, wy in ((150, 860), (520, 980), (1700, 900), (1400, 1060)):
    s.line(arc(wx, wy, 50, 18, 200, 340, 10), 6)
# the fountain
s.extend(fountain(1180, 900, 840, name="fountain"))
# boats
s.extend(boat(470, 890, 380, hull=WHITE, stripe=RED, cabin=YELLOW, facing=1, name="boat1"))
s.extend(boat(1530, 1030, 400, hull=WHITE, stripe=BLUE, cabin=ORANGE, facing=-1, name="boat2"))
# corniche promenade
s.add("sea-wall", rect(0, 1110, W, 1180), GREY)
s.add("promenade", rect(0, 1170, W, H), SAND)
for tx in (300, 750, 1200, 1650):
    s.line([(tx, 1180), (tx - 120, H)], 6)
# little sister with a balloon
sis = person(1790, 1460, 560, outfit="dress", headwear="headscarf", cloth=YELLOW, accent=PINK, arms="wave", facing=1, child=True, name="sister")
hand = person.hands[1]
s.line(smooth_open([hand, (hand[0] - 20, hand[1] - 120), (hand[0] + 10, 640)], 2), 5)
s.add("balloon", smooth([(hand[0] + 10, 640), (hand[0] - 70, 560), (hand[0] - 60, 460), (hand[0] + 10, 420), (hand[0] + 80, 460), (hand[0] + 90, 560)], 2), RED)
s.extend(scale_region(scale_region(drop(sis, "-scarf-front"), "-shoe", 1.3), "-hand", 1.15))
# the hero boy riding his scooter, waving at the fountain
s.extend(scooter(780, 1490, 560, colour=GREEN, facing=1, name="scooter"))
s.extend(shorts_kid(700, 1372, 700, shirt=ORANGE, shorts=BLUE, headwear="cap", cap=RED, arms=("up", scooter.grip), facing=1, name="boy"))
s.build(__file__)

"""Snorkelers above a Red Sea coral reef full of fish (modern)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 260), SKY)
s.extend(cloud(1100, 170, 340))
wave = [(0, 230)]
for i in range(1, 17):
    wave.append((i * W / 16, 230 + (18 if i % 2 else -10)))
s.add("sea", smooth_open(wave, 2) + [(W, 1200), (0, 1200)], SEA)
s.add("deep", smooth_open([(0, 900), (500, 860), (1100, 920), (1600, 870), (W, 900)], 2) + [(W, H), (0, H)], DEEP_SEA)
s.add("sand", smooth_open([(0, 1350), (400, 1300), (900, 1360), (1400, 1310), (W, 1350)], 2) + [(W, H), (0, H)], SAND)
# snorkelers at the surface
s.extend(snorkeler(520, 320, 720, suit=BLUE, trim=YELLOW, facing=1, name="diver1"))
s.extend(snorkeler(1560, 340, 680, suit=PURPLE, trim=PINK, facing=-1, name="diver2", hood=PURPLE))
# corals and plants
s.extend(coral_branch(330, 1420, 330, colour=ORANGE, name="coral1"))
s.extend(coral_fan(620, 1460, 360, colour=PURPLE, name="fan"))
s.extend(coral_branch(1600, 1440, 300, colour=PINK, name="coral2", seed=3))
s.extend(seaweed(1950, 1430, 420, colour=GREEN, name="weed2"))
s.add("rock", smooth([(820, 1500), (850, 1380), (1000, 1340), (1150, 1370), (1200, 1500)], 2), BROWN)
s.add("starfish", star(1000, 1430, 70, 32), RED)
# anemone with the clownfish
s.extend(anemone(1320, 1440, 300, colour=PINK, name="anemone"))
s.extend(fish(1370, 1150, 290, colour=ORANGE, fin=ORANGE, facing=-1, name="clownfish", bands=(-0.2, 0.08)))
# other fish
s.extend(fish(1760, 760, 280, colour=YELLOW, facing=-1, name="fish1"))
s.extend(fish(1840, 1060, 240, colour=BLUE, fin=YELLOW, facing=-1, name="fish2"))
s.extend(fish(230, 820, 260, colour=RED, fin=YELLOW, facing=1, name="fish3"))
# bubbles
for bx, by, br in ((1350, 600, 46), (1395, 500, 38)):
    s.add("bubble", circle(bx, by, br), WHITE)
# the hero hawksbill turtle
s.extend(turtle(950, 820, 760, shell=BROWN, plate=GOLD, skin=GREEN, facing=1, name="turtle"))
s.build(__file__)

"""Busy date souq with baskets and a friendly shopkeeper (traditional)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "Scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scene_kit import *  # noqa: E402,F403
from _figures import *  # noqa: E402,F403

s = Scene()
s.add("sky", rect(0, 0, W, 500), SKY)
s.extend(cloud(1700, 160, 340, name="cloud"))
s.extend(cloud(300, 120, 300, name="cloud"))
# souq arcade: mud wall with arched shop openings
s.add("souq-wall", [(0, 1100)] + crenel_top(0, W, 360, 64, 86) + [(W, 1100)], MUD)
for ax in (60, 560, 1060, 1560):
    s.add("shop-arch", arch(ax + 40, 520, ax + 420, 1100), DARK_BROWN)
# striped awnings over two shops
for ax, col in ((560, GREEN), (1560, RED)):
    s.add("awning", [(ax + 10, 520), (ax + 450, 520), (ax + 500, 660), (ax - 40, 660)], col)
    for k in range(1, 4):
        xx = ax + 10 + k * 110
        s.line([(xx, 522), (xx + (k - 2) * 25 - 5, 658)], 6)
# lanterns
s.extend(lantern(330, 560, 170, glass=YELLOW, metal=GOLD, name="lantern"))
s.extend(lantern(1830, 690, 150, glass=YELLOW, metal=GOLD, name="lantern"))
# sacks of dates in the back shops
s.extend(sack(1700, 1100, 180, 250, name="sack"))

s.add("floor", band([(0, 1090), (W, 1090)], H, 1), SAND)

# stall counter with baskets of different dates
s.add("counter", [(330, 1350), (330, 1120), (1060, 1120), (1060, 1350)], TRUNK)
s.add("counter-top", [(300, 1140), (340, 1080), (1050, 1080), (1090, 1140)], BROWN)
s.line([(520, 1150), (520, 1340)], 6)
s.line([(860, 1150), (860, 1340)], 6)
s.extend(basket(470, 1125, 220, 130, colour=MUD, fill=DARK_BROWN, name="basket"))
s.extend(basket(705, 1125, 220, 130, colour=MUD, fill=ORANGE, name="basket"))
s.extend(basket(940, 1125, 220, 130, colour=MUD, fill=YELLOW, name="basket"))
s.extend(basket(420, 1490, 300, 150, colour=MUD, fill=DARK_BROWN, name="basket"))

# a girl customer pointing at the dates
s.extend(human(180, 1500, 620, outfit="dress", head="girl_scarf", child=True, robe=PINK, accent=PURPLE, skirt=GREEN, emb=GREEN,
               hands=[(60, 1250), (330, 1100)], look=1, name="girl", front_arms=(True, False)))
# a boy carrying home a basket of dates
s.extend(human(1820, 1480, 600, outfit="thobe", head="shemagh", accent=RED, child=True, hands=[(1700, 1200), (1950, 1200)], look=-1, name="boy"))
s.extend(basket(1825, 1290, 230, 110, colour=MUD, fill=DARK_BROWN, name="boy-basket"))
s.add("boy-hand", circle(1700, 1200, 36), SKIN)
s.add("boy-hand", circle(1950, 1200, 36), SKIN)

# the smiling old shopkeeper weighing dates on a hanging balance
SX = 1420
hook = (990, 560)
s.extend(human(SX, 1490, 940, outfit="thobe", head="ghutra_taqiyah", beard=GREY, hands=[hook, (SX + 170, 1180)], look=-1, name="shopkeeper"))
s.extend(balance_scale(hook[0], hook[1] + 20, 360, name="scale", colour=GOLD, left_load=DARK_BROWN, right_load=GREY))
s.add("shopkeeper-hand", circle(hook[0], hook[1], 42), SKIN)
s.build(__file__)

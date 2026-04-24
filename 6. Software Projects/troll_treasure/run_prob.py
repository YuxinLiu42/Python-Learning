from treasure.dungeon import Dungeon
from treasure.games import Game

d = Dungeon.from_file("dungeons/dungeon.yml")
g = Game(d)
print(g.probability(max_steps=10))
# {-1: 0.1965, 0: 0.7541, 1: 0.0494}
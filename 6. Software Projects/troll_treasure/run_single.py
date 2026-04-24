from treasure.dungeon import Dungeon
from treasure.games import Game

d = Dungeon.from_file("dungeons/dungeon.yml")
g = Game(d)
g.run(max_steps=10)
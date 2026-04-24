import argparse
from treasure.dungeon import Dungeon
from treasure.games import Game


def main():
    parser = argparse.ArgumentParser(description="Troll Treasure game")
    parser.add_argument("dungeon", help="Path to dungeon YAML file")
    parser.add_argument(
        "--mode",
        choices=["play", "prob"],
        default="play",
        help="play: run a single game; prob: estimate outcome probabilities",
    )
    parser.add_argument(
        "-n",
        type=int,
        default=10000,
        help="Number of trials for probability estimation (default: 10000)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Max steps per game (default: 1000)",
    )
    args = parser.parse_args()

    dungeon = Dungeon.from_file(args.dungeon)
    game = Game(dungeon)

    if args.mode == "play":
        game.run(max_steps=args.steps)
    else:
        results = game.probability(trials=args.n, max_steps=args.steps)
        print(f"Troll wins:      {results[-1]:.2%}")
        print(f"Stalemate:       {results[0]:.2%}")
        print(f"Adventurer wins: {results[1]:.2%}")


if __name__ == "__main__":
    main()
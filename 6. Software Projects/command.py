from argparse import ArgumentParser

from greeter import greet


def process():
    parser = ArgumentParser(description="Generate appropriate greetings")

    # required (positional) arguments
    parser.add_argument("personal")
    parser.add_argument("family")

    # optional (keyword) arguments
    parser.add_argument("--title", "-t")
    parser.add_argument("--polite", "-p", action="store_true")
    #   polite will be false unless "--polite" or "-p" given at command-line

    args = parser.parse_args()

    print(greet(args.personal, args.family, args.title, args.polite))


if __name__ == "__main__":
    process()

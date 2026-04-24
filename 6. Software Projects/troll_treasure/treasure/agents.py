import random
from treasure.rooms import direction

class Agent:
    """
    Base functionality to create and load (but not move) an Agent
    """

    def __init__(self, point, name, symbol, verbose=True, allow_wait=True, **kwargs):
        self.point = tuple(point)  # (x, y) grid location of the agent
        self.name = name  # e.g. adventurer or troll
        self.symbol = symbol  # single char symbol to show the agent on dungeon maps
        self.verbose = verbose  # print output on agent behaviour if True
        self.allow_wait = allow_wait  # allow the agent to move nowhere

    def move(self, rooms):
        raise NotImplementedError("Use an Agent base class")

    @classmethod
    def from_dict(cls, agent_dict):
        return cls(
            agent_dict["point"],
            agent_dict["name"],
            agent_dict["symbol"],
            allow_wait=agent_dict["allow_wait"],
        )


class RandomAgent(Agent):
    """
    Agent that makes random moves
    """

    def move(self, rooms):
        if not rooms[self.point].links:
            # this room isn't linked to anything, can't move
            if self.verbose:
                print(f"{self.name} is trapped")
            return

        # pick a random room to move to
        options = rooms[self.point].links
        if self.allow_wait:
            options.append(self)
        new_room = random.choice(options)

        if self.verbose:
            move = direction(self.point, new_room.point)
            print(f"{self.name} moves {move}")
        self.point = new_room.point

class HumanAgent(Agent):
    """
    Agent that prompts the user where to move next
    """

    def move(self, rooms):
        if not rooms:
            if self.verbose:
                print(f"{self.name} is trapped")
            return
        # populate movement options depending on available rooms
        if self.allow_wait:
            options = ["wait"]
        else:
            options = []
        if (self.point[0] - 1, self.point[1]) in rooms:
            options.append("left")
        if (self.point[0] + 1, self.point[1]) in rooms:
            options.append("right")
        if (self.point[0], self.point[1] - 1) in rooms:
            options.append("up")
        if (self.point[0], self.point[1] + 1) in rooms:
            options.append("down")

        # prompt user for movement input
        choice = None
        while choice not in options:
            choice = input(f"Where will {self.name} move \n{options}? ")

        # move the agent
        if choice == "left":
            self.point = (self.point[0] - 1, self.point[1])
        elif choice == "right":
            self.point = (self.point[0] + 1, self.point[1])
        elif choice == "up":
            self.point = (self.point[0], self.point[1] - 1)
        elif choice == "down":
            self.point = (self.point[0], self.point[1] + 1)

"""
Record one step of the boids simulation to fixture.yml.
Run this script once to regenerate the fixture if needed —
but normally you should NEVER need to modify fixture.yml.
"""

import yaml
from boids import Flock


def record_fixture(filename: str = "fixture.yml") -> None:
    flock = Flock.initialise_random()

    before = [
        [b.x  for b in flock.boids],
        [b.y  for b in flock.boids],
        [b.vx for b in flock.boids],
        [b.vy for b in flock.boids],
    ]

    flock.update()

    after = [
        [b.x  for b in flock.boids],
        [b.y  for b in flock.boids],
        [b.vx for b in flock.boids],
        [b.vy for b in flock.boids],
    ]

    with open(filename, "w") as f:
        yaml.dump({"before": before, "after": after}, f)


if __name__ == "__main__":
    record_fixture()
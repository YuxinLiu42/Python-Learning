"""
Matplotlib animation of the Boids flocking simulation.
Run this file directly to watch the flock.

    python animate.py
"""

from matplotlib import animation
from matplotlib import pyplot as plt

from boids import Flock, AXES_XLIM, AXES_YLIM

NUM_FRAMES: int = 200
INTERVAL_MS: int = 50


def run_animation(flock: Flock) -> None:
    """Set up and display the Matplotlib animation for a given flock."""
    figure = plt.figure()
    axes = plt.axes(xlim=AXES_XLIM, ylim=AXES_YLIM)
    scatter = axes.scatter(flock.xs, flock.ys)

    def animate(frame: int) -> None:
        flock.update()
        scatter.set_offsets(flock.positions)

    # Keep a reference so garbage collection doesn't kill the animation
    _anim = animation.FuncAnimation(  # noqa: F841
        figure, animate, frames=NUM_FRAMES, interval=INTERVAL_MS
    )
    plt.show()


if __name__ == "__main__":
    flock = Flock.initialise_random()
    run_animation(flock)
"""
Boids flocking simulation.

Implements the three rules described by Craig Reynolds (1986):
  - Cohesion:   steer toward the average position of the flock
  - Separation: avoid crowding nearby boids
  - Alignment:  match velocity with nearby boids

Reference: http://dl.acm.org/citation.cfm?doid=37401.37406
"""

import random
from typing import List


# ---------------------------------------------------------------------------
# Named constants (no more magic numbers)
# ---------------------------------------------------------------------------
COHESION_STRENGTH: float = 0.01
SEPARATION_RADIUS_SQUARED: float = 100.0     # separation radius = 10 units
ALIGNMENT_RADIUS_SQUARED: float = 10_000.0  # alignment radius  = 100 units
ALIGNMENT_STRENGTH: float = 0.125

DEFAULT_NUM_BOIDS: int = 50
DEFAULT_X_RANGE: tuple = (-450.0, 50.0)
DEFAULT_Y_RANGE: tuple = (300.0, 600.0)
DEFAULT_VX_RANGE: tuple = (0.0, 10.0)
DEFAULT_VY_RANGE: tuple = (-20.0, 20.0)

AXES_XLIM: tuple = (-500, 1500)
AXES_YLIM: tuple = (-500, 1500)


# ---------------------------------------------------------------------------
# Boid: represents one individual agent
# ---------------------------------------------------------------------------
class Boid:
    """A single boid with 2D position (x, y) and velocity (vx, vy)."""

    def __init__(self, x: float, y: float, vx: float, vy: float) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def distance_squared(self, other: "Boid") -> float:
        """Return squared Euclidean distance to another boid."""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def move(self) -> None:
        """Update position by one timestep using current velocity."""
        self.x += self.vx
        self.y += self.vy

    def __repr__(self) -> str:
        return f"Boid(x={self.x:.1f}, y={self.y:.1f}, vx={self.vx:.2f}, vy={self.vy:.2f})"


# ---------------------------------------------------------------------------
# Flock: collection of boids + the three steering rules
# ---------------------------------------------------------------------------
class Flock:
    """A flock of boids that interact according to Reynolds' flocking rules."""

    def __init__(self, boids: List[Boid]) -> None:
        self.boids = boids

    @classmethod
    def initialise_random(
        cls,
        num_boids: int = DEFAULT_NUM_BOIDS,
        x_range: tuple = DEFAULT_X_RANGE,
        y_range: tuple = DEFAULT_Y_RANGE,
        vx_range: tuple = DEFAULT_VX_RANGE,
        vy_range: tuple = DEFAULT_VY_RANGE,
    ) -> "Flock":
        """Create a flock with randomly initialised boids."""
        boids = [
            Boid(
                x=random.uniform(*x_range),
                y=random.uniform(*y_range),
                vx=random.uniform(*vx_range),
                vy=random.uniform(*vy_range),
            )
            for _ in range(num_boids)
        ]
        return cls(boids)

    # ------------------------------------------------------------------
    # The three steering rules (each is a self-contained method)
    # ------------------------------------------------------------------

    def _apply_cohesion(self) -> None:
        """Rule 1 — Fly toward the centre of mass of the flock."""
        n = len(self.boids)
        for boid in self.boids:
            for other in self.boids:
                boid.vx += (other.x - boid.x) * COHESION_STRENGTH / n
                boid.vy += (other.y - boid.y) * COHESION_STRENGTH / n

    def _apply_separation(self) -> None:
        """Rule 2 — Steer away from boids that are too close."""
        for boid in self.boids:
            for other in self.boids:
                if boid.distance_squared(other) < SEPARATION_RADIUS_SQUARED:
                    boid.vx += boid.x - other.x
                    boid.vy += boid.y - other.y

    def _apply_alignment(self) -> None:
        """Rule 3 — Match velocity with boids in the neighbourhood."""
        n = len(self.boids)
        for boid in self.boids:
            for other in self.boids:
                if boid.distance_squared(other) < ALIGNMENT_RADIUS_SQUARED:
                    boid.vx += (other.vx - boid.vx) * ALIGNMENT_STRENGTH / n
                    boid.vy += (other.vy - boid.vy) * ALIGNMENT_STRENGTH / n

    # ------------------------------------------------------------------
    # Public one-step update
    # ------------------------------------------------------------------

    def update(self) -> None:
        """Advance the simulation by one timestep."""
        self._apply_cohesion()
        self._apply_separation()
        self._apply_alignment()
        for boid in self.boids:
            boid.move()

    # ------------------------------------------------------------------
    # Convenience properties for visualisation
    # ------------------------------------------------------------------

    @property
    def xs(self) -> List[float]:
        return [b.x for b in self.boids]

    @property
    def ys(self) -> List[float]:
        return [b.y for b in self.boids]

    @property
    def positions(self) -> List[tuple]:
        return [(b.x, b.y) for b in self.boids]
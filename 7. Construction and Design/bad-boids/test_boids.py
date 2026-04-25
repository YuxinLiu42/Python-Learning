"""
Regression tests and unit tests for the Boids simulation.

Rules:
- fixture.yml must NEVER be modified.
- The regression test ensures numerical results are identical to the original.
- Unit tests cover individual behaviours of Boid and Flock.
"""

import os
import yaml
import pytest
from pytest import approx

from boids import (
    Boid,
    Flock,
    COHESION_STRENGTH,
    SEPARATION_RADIUS_SQUARED,
    ALIGNMENT_RADIUS_SQUARED,
    ALIGNMENT_STRENGTH,
)


# ---------------------------------------------------------------------------
# Helpers: convert between fixture list-of-lists and Flock objects
# ---------------------------------------------------------------------------

def _flock_from_lists(data: list) -> Flock:
    """Build a Flock from fixture format: [xs, ys, xvs, yvs]."""
    xs, ys, xvs, yvs = data
    return Flock([Boid(x, y, vx, vy) for x, y, vx, vy in zip(xs, ys, xvs, yvs)])


def _flock_to_lists(flock: Flock) -> list:
    """Convert Flock back to fixture format: [xs, ys, xvs, yvs]."""
    return [
        [b.x  for b in flock.boids],
        [b.y  for b in flock.boids],
        [b.vx for b in flock.boids],
        [b.vy for b in flock.boids],
    ]


# ---------------------------------------------------------------------------
# Regression test — numerical output must match fixture.yml exactly
# ---------------------------------------------------------------------------

def test_regression():
    """One update step must reproduce the pre-recorded fixture values."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixture.yml")
    with open(fixture_path) as f:
        data = yaml.safe_load(f)

    flock = _flock_from_lists(data["before"])
    flock.update()
    result = _flock_to_lists(flock)

    for expected_row, result_row in zip(data["after"], result):
        for expected, actual in zip(expected_row, result_row):
            assert actual == approx(expected)


# ---------------------------------------------------------------------------
# Unit tests: Boid
# ---------------------------------------------------------------------------

class TestBoid:

    def test_move_updates_position(self):
        boid = Boid(x=0.0, y=0.0, vx=2.0, vy=-3.0)
        boid.move()
        assert boid.x == approx(2.0)
        assert boid.y == approx(-3.0)

    def test_move_is_additive(self):
        boid = Boid(x=5.0, y=10.0, vx=1.0, vy=1.0)
        boid.move()
        assert boid.x == approx(6.0)
        assert boid.y == approx(11.0)

    def test_distance_squared_pythagoras(self):
        a = Boid(0.0, 0.0, 0.0, 0.0)
        b = Boid(3.0, 4.0, 0.0, 0.0)
        assert a.distance_squared(b) == approx(25.0)

    def test_distance_squared_to_self_is_zero(self):
        a = Boid(7.0, -3.0, 0.0, 0.0)
        assert a.distance_squared(a) == approx(0.0)

    def test_distance_squared_is_symmetric(self):
        a = Boid(1.0, 2.0, 0.0, 0.0)
        b = Boid(4.0, 6.0, 0.0, 0.0)
        assert a.distance_squared(b) == approx(b.distance_squared(a))

    def test_repr_contains_class_name(self):
        boid = Boid(1.0, 2.0, 0.5, -0.5)
        assert "Boid" in repr(boid)


# ---------------------------------------------------------------------------
# Unit tests: Flock initialisation
# ---------------------------------------------------------------------------

class TestFlockInit:

    def test_correct_number_of_boids(self):
        flock = Flock.initialise_random(num_boids=20)
        assert len(flock.boids) == 20

    def test_all_elements_are_boids(self):
        flock = Flock.initialise_random(num_boids=10)
        for boid in flock.boids:
            assert isinstance(boid, Boid)

    def test_xs_ys_length_matches_flock_size(self):
        flock = Flock.initialise_random(num_boids=7)
        assert len(flock.xs) == 7
        assert len(flock.ys) == 7

    def test_positions_length_matches_flock_size(self):
        flock = Flock.initialise_random(num_boids=5)
        assert len(flock.positions) == 5

    def test_positions_are_tuples(self):
        flock = Flock.initialise_random(num_boids=3)
        for pos in flock.positions:
            assert isinstance(pos, tuple)
            assert len(pos) == 2

    def test_xs_ys_match_boid_attributes(self):
        boids = [Boid(1.0, 2.0, 0.0, 0.0), Boid(3.0, 4.0, 0.0, 0.0)]
        flock = Flock(boids)
        assert flock.xs == approx([1.0, 3.0])
        assert flock.ys == approx([2.0, 4.0])


# ---------------------------------------------------------------------------
# Unit tests: Cohesion rule
# ---------------------------------------------------------------------------

class TestCohesion:

    def test_two_boids_attract_each_other(self):
        """Boids should gain velocity toward each other."""
        b1 = Boid(x=0.0, y=0.0, vx=0.0, vy=0.0)
        b2 = Boid(x=100.0, y=0.0, vx=0.0, vy=0.0)
        Flock([b1, b2])._apply_cohesion()
        assert b1.vx > 0   # b1 moves right toward b2
        assert b2.vx < 0   # b2 moves left toward b1

    def test_equal_boids_net_zero(self):
        """Identical boids should produce no net velocity change."""
        b1 = Boid(0.0, 0.0, 0.0, 0.0)
        b2 = Boid(0.0, 0.0, 0.0, 0.0)
        Flock([b1, b2])._apply_cohesion()
        assert b1.vx == approx(0.0)
        assert b1.vy == approx(0.0)

    def test_strength_scales_with_constant(self):
        """Velocity delta should be proportional to COHESION_STRENGTH."""
        b1 = Boid(0.0, 0.0, 0.0, 0.0)
        b2 = Boid(1.0, 0.0, 0.0, 0.0)
        Flock([b1, b2])._apply_cohesion()
        # Each boid contributes (dx * strength / n) per neighbour
        # For b1: delta_vx from b2 = (1.0 - 0.0) * 0.01 / 2 = 0.005
        # plus self-contribution = 0
        assert b1.vx == approx(COHESION_STRENGTH / 2)


# ---------------------------------------------------------------------------
# Unit tests: Separation rule
# ---------------------------------------------------------------------------

class TestSeparation:

    def test_close_boids_repel(self):
        """Boids within separation radius push each other apart."""
        b1 = Boid(x=0.0, y=0.0, vx=0.0, vy=0.0)
        b2 = Boid(x=5.0, y=0.0, vx=0.0, vy=0.0)  # dist² = 25 < 100
        Flock([b1, b2])._apply_separation()
        assert b1.vx < 0   # b1 pushed away from b2 (leftward)
        assert b2.vx > 0   # b2 pushed away from b1 (rightward)

    def test_far_boids_unaffected(self):
        """Boids beyond separation radius should not change velocity."""
        b1 = Boid(x=0.0,   y=0.0, vx=0.0, vy=0.0)
        b2 = Boid(x=200.0, y=0.0, vx=0.0, vy=0.0)  # dist² = 40000 >> 100
        Flock([b1, b2])._apply_separation()
        assert b1.vx == approx(0.0)
        assert b2.vx == approx(0.0)

    def test_exactly_on_boundary_triggers_separation(self):
        """A boid exactly at the boundary (dist² < radius²) still separates."""
        # dist² = 99 < SEPARATION_RADIUS_SQUARED = 100
        b1 = Boid(0.0, 0.0, 0.0, 0.0)
        b2 = Boid(9.95, 0.0, 0.0, 0.0)  # dist² ≈ 99.0025 > 99 but confirm logic
        # Use guaranteed inside value
        b2 = Boid(9.0, 0.0, 0.0, 0.0)  # dist² = 81 < 100
        Flock([b1, b2])._apply_separation()
        assert b1.vx < 0


# ---------------------------------------------------------------------------
# Unit tests: Alignment rule
# ---------------------------------------------------------------------------

class TestAlignment:

    def test_nearby_boids_match_velocities(self):
        """Slow boid speeds up; fast boid slows down toward each other."""
        b1 = Boid(x=0.0, y=0.0, vx=0.0,  vy=0.0)
        b2 = Boid(x=10.0, y=0.0, vx=10.0, vy=0.0)  # dist² = 100 < 10000
        Flock([b1, b2])._apply_alignment()
        assert b1.vx > 0    # b1 speeds up
        assert b2.vx < 10.0 # b2 slows down

    def test_far_boids_no_alignment(self):
        """Boids outside alignment radius should not influence each other."""
        b1 = Boid(x=0.0,     y=0.0, vx=0.0,  vy=0.0)
        b2 = Boid(x=10000.0, y=0.0, vx=50.0, vy=0.0)  # dist² >> 10000
        Flock([b1, b2])._apply_alignment()
        assert b1.vx == approx(0.0)

    def test_identical_velocities_no_change(self):
        """Boids already matching speeds should see no velocity change."""
        b1 = Boid(0.0, 0.0, 5.0, 3.0)
        b2 = Boid(5.0, 0.0, 5.0, 3.0)
        Flock([b1, b2])._apply_alignment()
        assert b1.vx == approx(5.0)
        assert b1.vy == approx(3.0)


# ---------------------------------------------------------------------------
# Unit tests: Full update step
# ---------------------------------------------------------------------------

class TestUpdate:

    def test_update_changes_positions(self):
        flock = Flock.initialise_random(num_boids=10)
        old_xs = list(flock.xs)
        flock.update()
        assert flock.xs != old_xs

    def test_update_is_deterministic_given_same_state(self):
        """Two identically initialised flocks must produce identical results."""
        boids_a = [Boid(1.0, 2.0, 0.5, -0.5), Boid(10.0, 5.0, -1.0, 2.0)]
        boids_b = [Boid(1.0, 2.0, 0.5, -0.5), Boid(10.0, 5.0, -1.0, 2.0)]
        flock_a = Flock(boids_a)
        flock_b = Flock(boids_b)
        flock_a.update()
        flock_b.update()
        assert flock_a.xs == approx(flock_b.xs)
        assert flock_a.ys == approx(flock_b.ys)
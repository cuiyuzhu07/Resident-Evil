"""Tests for fleeing."""
import random
from V1 import config
from V1.infection import build_grid
from V1.model import World, flee, find_nearest_zombie, make_person


def test_flee_increases_distance():
    """A fleeing person ends up farther from the zombie."""
    person = {"x": 50.0, "y": 50.0, "state": "S"}
    zombie = {"x": 52.0, "y": 50.0, "state": "I"}
    flee(person, zombie, 1.5, 100)
    assert abs(person["x"] - zombie["x"]) > 2.0


def test_nearest_zombie_matches_bruteforce():
    """Grid search finds the same zombie as a brute-force search."""
    random.seed(2)
    zombies = [make_person(100, "I") for _ in range(30)]
    grid = build_grid(zombies, 10.0)
    for _ in range(50):
        person = make_person(100)
        found = find_nearest_zombie(person, grid, 10.0)
        near = [z for z in zombies
                if 0 < (person["x"] - z["x"]) ** 2
                + (person["y"] - z["y"]) ** 2 <= 100.0]
        if near:
            expected = min(near, key=lambda z: (person["x"] - z["x"]) ** 2
                           + (person["y"] - z["y"]) ** 2)
            assert found is expected
        else:
            assert found is None


def test_inside_bounds_with_fleeing():
    """Fleeing never pushes anyone off the map."""
    world = World(config)
    for _ in range(300):
        world.step()
        assert all(0 <= x <= world.size and 0 <= y <= world.size
                   for x, y in world.get_positions())
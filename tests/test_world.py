"""Tests for the world and movement."""
from V0 import config
from V0.model import World


def test_population_conserved():
    """Total population never changes."""
    world = World(config)
    for _ in range(100):
        world.step()
    assert sum(world.get_counts().values()) == config.N


def test_inside_bounds():
    """Nobody ever leaves the map."""
    world = World(config)
    for _ in range(500):
        world.step()
        assert all(0 <= x <= world.size and 0 <= y <= world.size
                   for x, y in world.get_positions())
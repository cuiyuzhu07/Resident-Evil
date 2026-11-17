"""Tests for quarantine zones and walls (task 3.5)."""
from V1 import config
from V1.model import World
from V1.quarantine import make_walls, path_hits_wall


def inside(person, zone):
    """Return True if the person is inside the rectangle zone."""
    x0, y0, x1, y1 = zone
    return x0 < person["x"] < x1 and y0 < person["y"] < y1


def test_walls_on_zone_border():
    """A 10x10 zone has a closed ring of wall cells on its border."""
    walls = make_walls([(0, 0, 10, 10)])
    assert (0, 5) in walls and (10, 5) in walls
    assert (5, 0) in walls and (5, 10) in walls
    assert (5, 5) not in walls


def test_path_through_wall_is_blocked():
    """A straight move across a wall is detected, a move beside it is not."""
    walls = make_walls([(0, 0, 10, 10)])
    assert path_hits_wall(5, 5, 15, 5, walls)
    assert not path_hits_wall(3, 3, 6, 6, walls)


def test_no_agent_crosses_a_wall():
    """Nobody ever moves from inside a quarantine zone to outside, or back."""
    world = World(config)
    zone = config.QUARANTINE_ZONES[0]
    start = [inside(p, zone) for p in world.people]
    assert any(start) and not all(start)
    for _ in range(300):
        world.step()
        assert [inside(p, zone) for p in world.people] == start

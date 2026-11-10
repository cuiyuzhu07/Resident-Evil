"""Tests for shelters."""
from V1 import config
from V1.model import World


def test_capacity_never_exceeded():
    """Shelter occupancy never exceeds capacity."""
    world = World(config)
    for _ in range(300):
        world.step()
        assert all(s["occupants"] <= s["capacity"] for s in world.shelters)


def test_sheltered_never_infected():
    """Nobody inside a shelter becomes infected."""
    world = World(config)
    for _ in range(300):
        world.step()
    sheltered = [p for p in world.people if p.get("sheltered")]
    assert sheltered, "nobody entered a shelter"
    assert all(p["state"] == "S" for p in sheltered)
"""Tests for the supplies system (task 3.7)."""
from types import SimpleNamespace

from V1 import config
from V1.model import World
from V1.supplies import pick_up_supplies, resolve_fights


def settings(**changes):
    """Copy the V1 config, with some values changed."""
    values = {k: v for k, v in vars(config).items() if k.isupper()}
    values.update(changes)
    return SimpleNamespace(**values)


def test_survivor_picks_up_crate():
    """A survivor standing on a crate takes it, and it leaves the map."""
    person = {"x": 10.0, "y": 10.0, "state": "S"}
    crates = [{"x": 10.5, "y": 10.0, "kind": "ammo"},
              {"x": 50.0, "y": 50.0, "kind": "food"}]
    left = pick_up_supplies([person], crates, 2.0, 3, 20)
    assert person["ammo"] == 3
    assert left == [crates[1]]


def test_zombie_cannot_pick_up():
    """Zombies do not collect supplies."""
    zombie = {"x": 10.0, "y": 10.0, "state": "I"}
    crates = [{"x": 10.0, "y": 10.0, "kind": "ammo"}]
    assert pick_up_supplies([zombie], crates, 2.0, 3, 20) == crates


def test_sure_win_kills_zombie_and_uses_ammo():
    """With win probability 1, the zombie dies and the survivor is safe."""
    survivor = {"x": 0, "y": 0, "state": "S", "ammo": 2}
    zombie = {"x": 1, "y": 0, "state": "I"}
    contacts = [(survivor, zombie), (zombie, survivor)]
    left, killed = resolve_fights(contacts, 1.0, 0.0)
    assert killed == 1 and zombie["state"] == "R"
    assert survivor["ammo"] == 1
    assert left == []


def test_no_ammo_no_fight():
    """A survivor without ammo cannot fight."""
    survivor = {"x": 0, "y": 0, "state": "S"}
    zombie = {"x": 1, "y": 0, "state": "I"}
    left, killed = resolve_fights([(survivor, zombie)], 1.0, 0.0)
    assert killed == 0 and left == [(survivor, zombie)]


def test_population_conserved_with_supplies():
    """Supplies and fights never create or lose people."""
    world = World(settings(SUPPLY_COUNT=60, FIGHT_WIN_PROB=0.9))
    for _ in range(150):
        world.step()
        assert sum(world.get_counts().values()) == config.N
    assert world.zombies_killed > 0

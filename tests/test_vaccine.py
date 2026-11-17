"""Tests for the vaccine event (task 3.6)."""
from types import SimpleNamespace

from V1 import config
from V1.model import World
from V1.vaccine import make_vaccine_schedule


def settings(**changes):
    """Copy the V1 config, with some values changed."""
    values = {k: v for k, v in vars(config).items() if k.isupper()}
    values.update(changes)
    return SimpleNamespace(**values)


def test_schedule_starts_on_vaccine_day():
    """The event table only contains days from the start day on."""
    table = make_vaccine_schedule(5, 0.1, 10)
    assert sorted(table) == [5, 6, 7, 8, 9]
    assert make_vaccine_schedule(None, 0.1, 10) == {}


def test_population_conserved_with_vaccine():
    """Vaccination never creates or loses people."""
    world = World(settings(VACCINE_DAY=0))
    for _ in range(100):
        world.step()
        assert sum(world.get_counts().values()) == config.N


def test_vaccine_reduces_final_infections():
    """On average, the vaccine lowers the number of people ever infected."""
    with_vaccine, without_vaccine = 0, 0
    for seed in range(5):
        on = World(settings(SEED=seed, VACCINE_DAY=0, VACCINE_RATE=0.05))
        off = World(settings(SEED=seed, VACCINE_DAY=None))
        for _ in range(200):
            on.step()
            off.step()
        with_vaccine += on.get_total_infected()
        without_vaccine += off.get_total_infected()
    assert with_vaccine < without_vaccine

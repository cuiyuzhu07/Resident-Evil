"""Tests for the player controls behind the interface (task 4.3)."""
from V1 import config
from V1.interface import Game, LOCKDOWN_FACTOR


def test_vaccine_waits_for_the_player():
    """Nobody is vaccinated until the player starts the vaccine."""
    game = Game()
    for _ in range(30):
        game.step()
    assert game.world.get_vaccinated_count() == 0
    game.start_vaccine()
    for _ in range(30):
        game.step()
    assert game.world.get_vaccinated_count() > 0


def test_lockdown_slows_movement():
    """A lockdown reduces the movement step, and lifting it restores it."""
    game = Game()
    game.set_lockdown(True)
    assert game.world.step_size == config.STEP_SIZE * LOCKDOWN_FACTOR
    game.set_lockdown(False)
    assert game.world.step_size == config.STEP_SIZE


def test_status_shows_the_day():
    """The status line reports the current day."""
    game = Game()
    game.step()
    assert game.status().startswith("Day 1")

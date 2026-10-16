def simulate_sir(n, i0, beta, gamma, days, dt=0.1):
    """Simulate the SIR model with Euler steps.

    Returns three lists (S, I, R) with one value per day.
    """
    s, i, r = n - i0, i0, 0
    S, I, R = [], [], []
    steps_per_day = round(1 / dt)
    for _ in range(days):
        for _ in range(steps_per_day):
            new_infected = beta * s * i / n * dt
            new_removed = gamma * i * dt
            s -= new_infected
            i += new_infected - new_removed
            r += new_removed
        S.append(s)
        I.append(i)
        R.append(r)
    return S, I, R

import random


def make_person(size, state="S"):
    """Create a person at a uniformly random position inside the map.

    Returns a dict with keys 'x', 'y' and 'state'.
    """
    return {"x": random.uniform(0, size),
            "y": random.uniform(0, size),
            "state": state}


def move(person, step_size, size):
    """Move a person by a Gaussian random step, reflecting at the borders."""
    for axis in ("x", "y"):
        person[axis] += random.gauss(0, step_size)
        if person[axis] < 0:
            person[axis] = -person[axis]
        elif person[axis] > size:
            person[axis] = 2 * size - person[axis]

class World:
    """Container for the population and the simulation clock."""

    def __init__(self, config):
        """Create N people and mark the first I0 as infected."""
        random.seed(config.SEED)
        self.size = config.SIZE
        self.step_size = config.STEP_SIZE
        self.day = 0
        self.people = [make_person(self.size) for _ in range(config.N)]
        for person in self.people[:config.I0]:
            person["state"] = "I"

    def step(self):
        """Advance the simulation by one step: everybody moves."""
        for person in self.people:
            move(person, self.step_size, self.size)
        # --- B plugs the infection logic here ---
        self.day += 1

    def get_positions(self):
        """Return a list of (x, y) tuples, one per person."""
        return [(p["x"], p["y"]) for p in self.people]

    def get_states(self):
        """Return a list of state strings ('S', 'I', 'R'), one per person."""
        return [p["state"] for p in self.people]

    def get_counts(self):
        """Return a dict such as {'S': 195, 'I': 5, 'R': 0}."""
        counts = {"S": 0, "I": 0, "R": 0}
        for person in self.people:
            counts[person["state"]] += 1
        return counts

from . import config
from .model import World

world = World(config)
print("start:", world.get_counts())
for _ in range(100):
    world.step()
print("after 100 steps:", world.get_counts())
print("first 3 positions:", world.get_positions()[:3])
"""Simulation logic for V1: SIR equations, people, shelters and World.

No plotting here. V1 adds shelters, fleeing, quarantine walls, a
vaccine event and supplies on top of V0.
"""
import math
import random

from .infection import (find_contacts, update_infection, cell_size,
                        build_grid, get_cell)
from .quarantine import (WALL_CELL, make_walls, move_off_walls,
                         undo_if_blocked, wall_between)
from .vaccine import make_vaccine_schedule, vaccinate
from .supplies import make_supplies, pick_up_supplies, eat, resolve_fights


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


def make_shelters(specs):
    """Create shelter dicts from (x, y, radius, capacity) tuples."""
    return [{"x": x, "y": y, "radius": r, "capacity": c, "occupants": 0}
            for x, y, r, c in specs]


def enter_shelters(people, shelters):
    """Let susceptible people inside a shelter's radius enter it.

    A person enters only if the shelter is not full. Sheltered people
    are flagged with person["sheltered"] = True.
    """
    for person in people:
        if person["state"] != "S" or person.get("sheltered"):
            continue
        for shelter in shelters:
            if shelter["occupants"] >= shelter["capacity"]:
                continue
            dx = person["x"] - shelter["x"]
            dy = person["y"] - shelter["y"]
            if dx * dx + dy * dy <= shelter["radius"] ** 2:
                person["sheltered"] = True
                shelter["occupants"] += 1
                break

def reflect(value, size):
    """Reflect a coordinate back inside [0, size]."""
    if value < 0:
        return -value
    if value > size:
        return 2 * size - value
    return value


def find_nearest_zombie(person, grid, radius):
    """Return the nearest infected person within `radius`, or None.

    `grid` is built with build_grid(zombies, radius), so only the cell
    of the person and its 8 neighbours need to be checked.
    """
    cx, cy = get_cell(person["x"], person["y"], radius)
    best, best_d2 = None, radius * radius
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for zombie in grid.get((cx + dx, cy + dy), []):
                d2 = ((person["x"] - zombie["x"]) ** 2
                      + (person["y"] - zombie["y"]) ** 2)
                if 0 < d2 <= best_d2:
                    best, best_d2 = zombie, d2
    return best


def flee(person, zombie, speed, size):
    """Move `person` a distance `speed` directly away from `zombie`."""
    dx = person["x"] - zombie["x"]
    dy = person["y"] - zombie["y"]
    dist = math.hypot(dx, dy)
    person["x"] = reflect(person["x"] + speed * dx / dist, size)
    person["y"] = reflect(person["y"] + speed * dy / dist, size)

class World:
    """Container for the population and the simulation clock."""

    def __init__(self, config):
        """Create N people, mark the first I0 as infected, set up shelters."""
        self.config = config
        random.seed(config.SEED)
        self.size = config.SIZE
        self.step_size = config.STEP_SIZE
        self.day = 0
        self.shelters = make_shelters(getattr(config, "SHELTERS", []))
        self.people = [make_person(self.size) for _ in range(config.N)]
        for person in self.people[:config.I0]:
            person["state"] = "I"
        # Task 3.5: quarantine walls
        self.wall_cell = WALL_CELL
        self.walls = make_walls(getattr(config, "QUARANTINE_ZONES", []))
        move_off_walls(self.people, self.walls, self.size)
        # Task 3.6: vaccine event table {day: rate}
        self.vaccine_schedule = make_vaccine_schedule(
            getattr(config, "VACCINE_DAY", None),
            getattr(config, "VACCINE_RATE", 0),
            config.DAYS)
        self.vaccine_efficacy = getattr(config, "VACCINE_EFFICACY", 0)
        # Task 3.7: supply crates and fights
        self.supplies = make_supplies(getattr(config, "SUPPLY_COUNT", 0),
                                      self.size)
        self.zombies_killed = 0

    def step(self):
        """Advance one step: vaccine, move/flee, shelters, then infection."""
        rate = self.vaccine_schedule.get(self.day)
        if rate:
            vaccinate(self.people, rate, self.vaccine_efficacy)
        radius = getattr(self.config, "FLEE_RADIUS", 0)
        speed = getattr(self.config, "FLEE_SPEED", 0)
        zombie_grid = {}
        if radius > 0:
            zombie_grid = build_grid(
                [p for p in self.people if p["state"] == "I"], radius)
        for person in self.people:
            if person.get("sheltered"):
                continue
            old_x, old_y = person["x"], person["y"]
            zombie = None
            if radius > 0 and person["state"] == "S":
                zombie = find_nearest_zombie(person, zombie_grid, radius)
            if zombie is not None:
                flee(person, zombie, speed, self.size)
            else:
                move(person, self.step_size, self.size)
            undo_if_blocked(person, old_x, old_y, self.walls)
        enter_shelters(self.people, self.shelters)
        if self.supplies:
            self.supplies = pick_up_supplies(
                self.people, self.supplies,
                getattr(self.config, "SUPPLY_PICKUP_RADIUS", 2.0),
                getattr(self.config, "AMMO_PER_CRATE", 0),
                getattr(self.config, "FOOD_PER_CRATE", 0))
        eat(self.people)
        contacts = find_contacts(self.people, cell_size)
        contacts = [(a, b) for a, b in contacts
                    if not a.get("sheltered") and not b.get("sheltered")]
        if self.walls:
            contacts = [(a, b) for a, b in contacts
                        if not wall_between(a, b, self.walls)]
        contacts, killed = resolve_fights(
            contacts,
            getattr(self.config, "FIGHT_WIN_PROB", 0),
            getattr(self.config, "FOOD_BONUS", 0))
        self.zombies_killed += killed
        update_infection(
            self.people,
            contacts,
            self.config.BETA,
            self.config.GAMMA
        )
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

    def get_sheltered_count(self):
        """Return the number of people currently inside a shelter."""
        return sum(1 for p in self.people if p.get("sheltered"))


    def get_vaccinated_count(self):
        """Return the number of people who have been vaccinated."""
        return sum(1 for p in self.people if p.get("vaccinated"))

    def get_total_infected(self):
        """Return how many people have ever been infected.

        Removed people who are only immune thanks to the vaccine are
        not counted.
        """
        return sum(1 for p in self.people
                   if p["state"] in ("I", "R") and not p.get("immune"))

    def get_supply_counts(self):
        """Return crates left on the map and supplies carried by survivors.

        Example: {'crates': 12, 'ammo': 20, 'food': 35}.
        """
        alive = [p for p in self.people if p["state"] == "S"]
        return {"crates": len(self.supplies),
                "ammo": sum(p.get("ammo", 0) for p in alive),
                "food": sum(p.get("food", 0) for p in alive)}

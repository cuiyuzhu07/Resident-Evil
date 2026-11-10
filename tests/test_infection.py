"""Tests for contact detection."""
import random
from V0.infection import find_contacts, cell_size, contact_dis
from V0.model import make_person


def test_grid_matches_bruteforce():
    """Grid-based contacts equal brute-force contacts."""
    random.seed(1)
    people = [make_person(100) for _ in range(200)]
    grid = {frozenset((id(a), id(b)))
            for a, b in find_contacts(people, cell_size)}
    brute = {frozenset((id(a), id(b)))
             for i, a in enumerate(people) for b in people[i + 1:]
             if ((a["x"] - b["x"]) ** 2
                 + (a["y"] - b["y"]) ** 2) ** 0.5 <= contact_dis}
    assert grid == brute
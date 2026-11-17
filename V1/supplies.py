"""Supplies system for V1 (task 3.7, optional).

Supply crates lie on the map. A survivor who walks over a crate picks
it up: an ammo crate gives bullets, a food crate gives days of food.
When a survivor with ammo meets a zombie, they fight: with probability
FIGHT_WIN_PROB (plus FOOD_BONUS if the survivor still has food) the
zombie is killed (state 'R') instead of infecting the survivor.
Each fight uses one bullet. Food goes down by one every day.
"""
import random


def make_supplies(count, size):
    """Create `count` crates at random positions, half ammo and half food."""
    return [{"x": random.uniform(0, size),
             "y": random.uniform(0, size),
             "kind": "ammo" if k % 2 == 0 else "food"}
            for k in range(count)]


def pick_up_supplies(people, crates, radius, ammo_per_crate, food_per_crate):
    """Let survivors pick up every crate within `radius` of them.

    A picked-up crate is removed from the map. Returns the remaining crates.
    """
    remaining = []
    r2 = radius * radius
    for crate in crates:
        taker = None
        for person in people:
            if person["state"] != "S" or person.get("sheltered"):
                continue
            dx = person["x"] - crate["x"]
            dy = person["y"] - crate["y"]
            if dx * dx + dy * dy <= r2:
                taker = person
                break
        if taker is None:
            remaining.append(crate)
        elif crate["kind"] == "ammo":
            taker["ammo"] = taker.get("ammo", 0) + ammo_per_crate
        else:
            taker["food"] = taker.get("food", 0) + food_per_crate
    return remaining


def eat(people):
    """Every survivor with food eats one day of it."""
    for person in people:
        if person.get("food", 0) > 0:
            person["food"] -= 1


def win_probability(person, win_prob, food_bonus):
    """Chance that `person` kills a zombie in a fight (0 without ammo)."""
    if person.get("ammo", 0) <= 0:
        return 0.0
    bonus = food_bonus if person.get("food", 0) > 0 else 0.0
    return min(1.0, win_prob + bonus)


def resolve_fights(contacts, win_prob, food_bonus):
    """Let armed survivors fight the zombies they are in contact with.

    Each survivor-zombie pair fights at most once per step, and every
    fight uses one bullet. Killed zombies become 'R' at the end, and all
    contacts involving them, or a survivor who won a fight, are dropped
    so they cannot cause an infection this step.

    Returns (remaining_contacts, number_of_zombies_killed).
    """
    fought = set()
    killed = {}
    winners = set()
    for a, b in contacts:
        if a["state"] == "S" and b["state"] == "I":
            survivor, zombie = a, b
        elif a["state"] == "I" and b["state"] == "S":
            survivor, zombie = b, a
        else:
            continue
        pair = (id(survivor), id(zombie))
        if pair in fought or id(zombie) in killed:
            continue
        chance = win_probability(survivor, win_prob, food_bonus)
        if chance == 0.0:
            continue
        fought.add(pair)
        survivor["ammo"] -= 1
        if random.random() < chance:
            killed[id(zombie)] = zombie
            winners.add(id(survivor))

    for zombie in killed.values():
        zombie["state"] = "R"
    blocked = set(killed) | winners
    remaining = [(a, b) for a, b in contacts
                 if id(a) not in blocked and id(b) not in blocked]
    return remaining, len(killed)

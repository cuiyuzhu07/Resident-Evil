"""Quarantine zones and walls for V1 (task 3.5).

Walls are stored as a set of grid cells (cx, cy), each WALL_CELL wide.
A move that would enter or pass through a wall cell is cancelled, and
two people on opposite sides of a wall cannot infect each other.
"""
import math
import random

WALL_CELL = 1.0


def to_cell(x, y, cell=WALL_CELL):
    """Return the wall-grid cell (cx, cy) that contains the point (x, y)."""
    return int(x // cell), int(y // cell)


def make_walls(zones, cell=WALL_CELL):
    """Build the set of wall cells on the border of each quarantine zone.

    `zones` is a list of rectangles (x0, y0, x1, y1) in map coordinates.
    Returns a set of (cx, cy) tuples.
    """
    walls = set()
    for x0, y0, x1, y1 in zones:
        cx0, cy0 = to_cell(x0, y0, cell)
        cx1, cy1 = to_cell(x1, y1, cell)
        for cx in range(cx0, cx1 + 1):
            walls.add((cx, cy0))
            walls.add((cx, cy1))
        for cy in range(cy0, cy1 + 1):
            walls.add((cx0, cy))
            walls.add((cx1, cy))
    return walls


def path_hits_wall(x0, y0, x1, y1, walls, cell=WALL_CELL):
    """Return True if the straight path from (x0, y0) to (x1, y1) touches a wall.

    The path is sampled every quarter of a cell, so a one-cell-thick
    wall cannot be jumped over. The starting point itself is not checked.
    """
    if not walls:
        return False
    dist = math.hypot(x1 - x0, y1 - y0)
    n = max(1, math.ceil(dist / (cell / 4)))
    for k in range(1, n + 1):
        t = k / n
        if to_cell(x0 + t * (x1 - x0), y0 + t * (y1 - y0), cell) in walls:
            return True
    return False


def undo_if_blocked(person, old_x, old_y, walls):
    """Put `person` back at (old_x, old_y) if their last move hit a wall."""
    if path_hits_wall(old_x, old_y, person["x"], person["y"], walls):
        person["x"], person["y"] = old_x, old_y


def wall_between(a, b, walls):
    """Return True if a wall separates person `a` from person `b`."""
    return path_hits_wall(a["x"], a["y"], b["x"], b["y"], walls)


def move_off_walls(people, walls, size):
    """Give a new random position to anyone who starts on a wall cell."""
    for person in people:
        while to_cell(person["x"], person["y"]) in walls:
            person["x"] = random.uniform(0, size)
            person["y"] = random.uniform(0, size)

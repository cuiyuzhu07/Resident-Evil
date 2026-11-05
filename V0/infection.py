# Grid partioning to find nearby people and transmit the disease
# Contact infection
# if a zombie comes closer to human it will catch and bite
# along with transmit the disease
import random
import math

contact_dis = 8.0
cell_size = 8.0
def get_cell(x, y, cell_size):
    return int(x // cell_size), int(y // cell_size)

def build_grid(people, cell_size):
    grid = {}

    for person in people:
        cell = get_cell(person["x"], person["y"], cell_size)

        if cell not in grid:
            grid[cell] = []

        grid[cell].append(person)

    return grid

def find_contacts(people, cell_size):
    grid = build_grid(people, cell_size)
    contacts = []

    for cell, cell_people in grid.items():

        cx, cy = cell

        # Check this cell and all 8 neighbouring cells
        for dx_cell in (-1, 0, 1):
            for dy_cell in (-1, 0, 1):

                neighbour = (cx + dx_cell, cy + dy_cell)

                if neighbour not in grid:
                    continue

                for person in cell_people:
                    for other in grid[neighbour]:

                        if person is other:
                            continue

                        dx = person["x"] - other["x"]
                        dy = person["y"] - other["y"]

                        distance = (dx**2 + dy**2) ** 0.5

                        if distance <= contact_dis:
                            contacts.append((person, other))

    return contacts

p1 = {"x": 10, "y": 10, "state": "I"}
p2 = {"x": 11, "y": 11, "state": "S"}
p3 = {"x": 20, "y": 20, "state": "S"}

people = [p1, p2, p3]

print(find_contacts(people, cell_size))

def update_infection(people, contacts, beta, gamma):
    """Update infection and removal states after contacts are found."""

    to_infect = set()
    to_remove = set()

    for person, other in contacts:

        # Infected person meets susceptible person
        if person["state"] == "I" and other["state"] == "S":
            if random.random() < beta:
                to_infect.add(id(other))

        elif person["state"] == "S" and other["state"] == "I":
            if random.random() < beta:
                to_infect.add(id(person))

    # Check infected people for removal
    for person in people:
        if person["state"] == "I":
            if random.random() < gamma:
                to_remove.add(id(person))

    # Apply all changes AFTER checking the old states
    for person in people:
        if id(person) in to_infect:
            person["state"] = "I"

        if id(person) in to_remove:
            person["state"] = "R"
"""Simulation parameters."""

N = 200            # total population
I0 = 5             # initially infected
BETA = 0.8         # infection rate
GAMMA = 0.03        # removal rate
DAYS = 300         # simulation length (days)
SEED = 42          # random seed

SIZE = 100         # map size (for agent-based model later)
STEP_SIZE = 1.0    # movement per step (for agent-based model later)
SHELTERS = [(20, 20, 8, 10),    # x, y, radius, capacity
            (80, 80, 8, 10)]
FLEE_RADIUS = 10.0   # survivors react to zombies within this distance
FLEE_SPEED = 1.5     # distance run per step when fleeing

# Task 3.5: quarantine zones, as rectangles (x0, y0, x1, y1).
# Walls are built on the border of each zone. Use [] to switch off.
QUARANTINE_ZONES = [(55, 10, 90, 45)]

# Task 3.6: vaccine event. Set VACCINE_DAY = None to switch off.
VACCINE_DAY = 20          # first day of vaccination
VACCINE_RATE = 0.05       # fraction of susceptibles vaccinated per day
VACCINE_EFFICACY = 0.9    # probability that a vaccination gives immunity

# Task 3.7 (optional): supplies. Set SUPPLY_COUNT = 0 to switch off.
SUPPLY_COUNT = 30           # crates on the map at the start (half ammo, half food)
SUPPLY_PICKUP_RADIUS = 2.0  # a survivor this close to a crate picks it up
AMMO_PER_CRATE = 3          # bullets in one ammo crate
FOOD_PER_CRATE = 20         # days of food in one food crate
FIGHT_WIN_PROB = 0.5        # chance an armed survivor kills a zombie
FOOD_BONUS = 0.2            # extra chance when the survivor has food

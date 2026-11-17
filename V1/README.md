# V1: Extended version

Built on V0 by adding code only. V0 is unchanged and still runs on its own.

## Run (from the project root)
    pip install -r requirements.txt
    python -m V1.main

Do not run `python V1/main.py` directly: the modules use relative imports.

## New in V1
- **Shelters (task 3.1)**: circular safe zones with limited capacity,
  defined in `config.py` as `(x, y, radius, capacity)`. A survivor who
  walks inside a non-full shelter stops moving and cannot be infected.
- **Fleeing (task 3.2)**: a survivor with a zombie within `FLEE_RADIUS`
  runs directly away from the nearest one at `FLEE_SPEED`. The search
  reuses the grid from `infection.py`.
- **Quarantine zones and walls (task 3.5)**: each zone in
  `QUARANTINE_ZONES` is a rectangle `(x0, y0, x1, y1)` surrounded by walls.
  Walls are a set of grid cells (`quarantine.py`). A move into or through
  a wall cell is cancelled, and nobody is infected through a wall.
- **Vaccine event (task 3.6)**: from `VACCINE_DAY`, every day each
  susceptible person outside a shelter is vaccinated with probability
  `VACCINE_RATE`. The vaccine works with probability `VACCINE_EFFICACY`;
  immune people become `'R'`. The days are stored in an event table
  `{day: rate}` (`vaccine.py`).

## What changed compared to V0
| File | Change |
|---|---|
| `config.py` | added `SHELTERS`, `FLEE_RADIUS`, `FLEE_SPEED`, `QUARANTINE_ZONES`, `VACCINE_DAY`, `VACCINE_RATE`, `VACCINE_EFFICACY` |
| `model.py` | added `make_shelters`, `enter_shelters`, `reflect`, `find_nearest_zombie`, `flee`, `get_sheltered_count`, `get_vaccinated_count`, `get_total_infected`; `World.step()` extended |
| `quarantine.py` | new: wall cells, wall collision, no infection through walls |
| `vaccine.py` | new: vaccine event table and daily vaccination |
| `render.py` | draws shelters and walls, shows the number vaccinated |
| `infection.py` | unchanged |

Setting `FLEE_RADIUS = 0`, `SHELTERS = []`, `QUARANTINE_ZONES = []` or
`VACCINE_DAY = None` switches a feature off, which gives the V0 behaviour.

## Tests
    python -m pytest tests/

## Limitations
- Zombies move randomly; they do not chase survivors.
- Survivors never leave a shelter.
- Quarantine walls have no doors.
- Incubation and zombie types are not implemented yet.

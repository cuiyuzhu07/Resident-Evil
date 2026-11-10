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

## What changed compared to V0
| File | Change |
|---|---|
| `config.py` | added `SHELTERS`, `FLEE_RADIUS`, `FLEE_SPEED` |
| `model.py` | added `make_shelters`, `enter_shelters`, `reflect`, `find_nearest_zombie`, `flee`, `get_sheltered_count`; `World.step()` extended |
| `infection.py`, `render.py` | unchanged (render may also draw shelters) |

Setting `FLEE_RADIUS = 0` or `SHELTERS = []` switches a feature off,
which gives the V0 behaviour.

## Tests
    python -m pytest tests/

## Limitations
- Zombies move randomly; they do not chase survivors.
- Survivors never leave a shelter.
- Incubation, zombie types, quarantine and vaccine are not implemented yet.
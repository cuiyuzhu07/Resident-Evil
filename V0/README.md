# V0: Minimal viable version

Agent-based SIR simulation: people move randomly on a 2D map and infect
each other. The SIR equations are provided as a reference curve.

## Run (from the project root)
    pip install -r requirements.txt
    python -m V0.main

Do not run `python V0/main.py` directly: the modules use relative imports.

## Contents
- `config.py`: simulation parameters
- `model.py`: SIR equations, people, movement, `World`
- `infection.py`: contact detection and infection logic
- `render.py`: plots and animation
- `main.py`: entry point

## Design choices
- A person is a dict (`x`, `y`, `state`).
- Movement: Gaussian random steps, reflection at the borders.
- SIR equations use Euler steps with `dt = 0.1`.

## Limitations
- No incubation, shelters, quarantine or vaccine (added in V1).
- No command-line arguments or logging yet (added in V2).

## UPDATE 10.16: task 2.1/2.2 is merged into main (git pull to get it).

- World interface (in V0/model.py):
  world = World(config)       # creates N people, first I0 are infected
  world.step()                # advances one step (everyone moves)
  world.get_positions()       # -> [(x, y), ...]
  world.get_states()          # -> ['S', 'I', ...]
  world.get_counts()          # -> {'S': 195, 'I': 5, 'R': 0}

## Conventions:
- States are strings: 'S', 'I', 'R'.
- A person is a dict: {"x": float, "y": float, "state": str}.
- Coordinates are floats in [0, SIZE] (SIZE = 100).
- Borders: people REFLECT off the walls (they bounce back, they don't wrap around or disappear).
- Movement: Gaussian random step, std = STEP_SIZE (1.0).
- World(config) seeds the RNG with config.SEED, so runs are reproducible.

For B: infection plugs into World.step(), right after everybody has moved
(there is a marked comment line). Proposed signature:
apply_infection(people, config). It should apply all state changes at the
END of the step. Please confirm the name, then I will add the call.

For C: you can animate on this World now; only positions and states change
for the moment (no infection yet).

If you want to change any interface, tell me first. Thanks!
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


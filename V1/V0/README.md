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
- `infection.py`: grid contact detection, infection and removal
- `render.py`: SIR plot and live animation
- `main.py`: entry point

## Design choices
- A person is a dict (`x`, `y`, `state`).
- Movement: Gaussian random steps, reflection at the borders.
- Contacts: grid partitioning, cell size equal to the contact distance.
- Infection: synchronous update (all changes applied at the end of a step).

## Limitations
- BETA means a per-contact probability in the agent model, but a daily
  contact rate in the SIR equations, so the two curves differ.
- No incubation, shelters, quarantine or vaccine (added in V1).
- No command-line arguments or logging yet (added in V2).
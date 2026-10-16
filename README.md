# Resident-Evil
DSBA Python group project
## steps

1. Clone the repository: In VS Code, press Ctrl+Shift+P (Cmd+Shift+P on Mac), type Git: Clone, paste the repository's HTTPS URL, select a local folder, and click "Open".
2. Create a virtual environment: Run the following in the VS Code terminal (Ctrl+``): python -m venv .venvActivation for Mac/Linux:source .venv/bin/activateOnce activated successfully,(.venv)` will appear on the far left of the terminal.
3. Install dependencies: pip install -r requirements.txtSelect the interpreter: Ctrl+Shift+P (Cmd+Shift+P on Mac) $\rightarrow$ Python: Select Interpreter $\rightarrow$ choose the one inside .venv.Verify: Run python main.py. If you see project skeleton ready, it is set up successfully.


git add render.py
git commit -m “add plot_sir”
git push


**before work, run `git pull`，when it ends `git add`、`git commit`、`git push`。**

# Resident-Evil: Zombie Outbreak Simulator

An agent-based epidemic simulation built on the SIR model. People move on a
2D map, infect each other, and we compare the result with the SIR equations.
The project is developed in three runnable stages (V0, V1, V2).

## Team
- Member A: world and movement, SIR equations, model comparison
- Member B: infection logic, performance, batch experiments
- Member C: plotting, animation, interface

## Versions
| Version | Content | Status |
|---|---|---|
| V0 | SIR equations + agent-based simulation (move, infect, animate) | in progress |
| V1 | Story extensions (incubation, zombie types, quarantine, vaccine) | planned |
| V2 | Tests, logging, argparse, config file, interface, experiments | planned |

## Setup
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run (from the project root)
    python -m V0.main

## Run tests
    python -m pytest tests/

## Project structure
    Resident-Evil/
    ├── README.md
    ├── requirements.txt
    ├── tests/
    └── V0/        (V1/ and V2/ will be copies of the previous version, extended)

## Workflow
- Work on your own branch (`feature/...`), merge into `main` by Pull Request.
- `main` must always run.
- Pull before starting, push before stopping.
- Every module, class and function has a docstring.

## Interface agreement
## Interface agreement

### Conventions
- States are strings: `'S'` (susceptible), `'I'` (infected), `'R'` (removed).
- Coordinates are floats in `[0, SIZE]` (default `SIZE = 100`).
- Borders: people **reflect** off the walls.
- All parameters live in `config.py`.

### config.py
N, I0, BETA, GAMMA, DAYS, SEED, SIZE, STEP_SIZE

### model.py (member A)
| Function / method | Input | Output |
|---|---|---|
| `simulate_sir(n, i0, beta, gamma, days, dt=0.1)` | numbers | `(S, I, R)`, three lists of length `days` |
| `make_person(size, state="S")` | map size | dict with `x`, `y`, `state` |
| `move(person, step_size, size)` | person dict | None (modifies in place) |
| `World(config)` | config module | a world object |
| `world.step()` | none | None (advances one step) |
| `world.get_positions()` | none | `[(x, y), ...]` |
| `world.get_states()` | none | `['S', 'I', ...]` |
| `world.get_counts()` | none | `{'S': 195, 'I': 5, 'R': 0}` |

### infection.py (member B)
| Function | Input | Output |
|---|---|---|
| `apply_infection(people, config)` | list of person dicts, config | None (applies all state changes at the end of the step) |

Called from `World.step()` after everybody has moved.

### render.py (member C)
| Function | Input | Output |
|---|---|---|
| `plot_sir(S, I, R)` | three lists | displays the curves |
| `animate(world)` | a `World` | displays the live animation |

### Rules
- Changing an interface requires telling the others first.
- Simulation logic never imports plotting code.

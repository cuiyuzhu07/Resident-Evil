"""Result charts for the report (task 4.4, member C).

Reads batch-experiment results and draws report-ready figures:
  1. infected curves per strategy, mean with a +/- 1 std band;
  2. a boxplot of the total number of people ever infected per strategy.

Results format (to agree with task 4.2): a CSV file with one row per
strategy, seed and day, and the columns
    strategy, seed, day, S, I, R, total_infected

Until 4.2 exists, `demo_results()` runs a few small experiments
(no vaccine vs. early vs. late vaccine) so the charts can be tested.

Run from the project root:
    python -m V1.charts                     # demo data
    python -m V1.charts results.csv         # real data from 4.2
"""
import csv
import os
import statistics
import sys
from types import SimpleNamespace

import matplotlib.pyplot as plt

COLUMNS = ["strategy", "seed", "day", "S", "I", "R", "total_infected"]


def save_results(results, path):
    """Write `results` to a CSV file in the agreed format."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for strategy, runs in results.items():
            for seed, run in runs.items():
                for k, day in enumerate(run["day"]):
                    writer.writerow([strategy, seed, day] +
                                    [run[col][k] for col in COLUMNS[3:]])


def load_results(path):
    """Read a results CSV.

    Returns {strategy: {seed: {"day": [...], "S": [...], "I": [...],
    "R": [...], "total_infected": [...]}}}.
    """
    results = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            run = results.setdefault(row["strategy"], {}).setdefault(
                int(row["seed"]), {col: [] for col in COLUMNS[2:]})
            for col in COLUMNS[2:]:
                run[col].append(int(float(row[col])))
    return results


def mean_and_std(runs, column):
    """Return (days, mean, std) of `column` over all runs, day by day."""
    series = [run[column] for run in runs.values()]
    length = min(len(s) for s in series)
    days = list(runs.values())[0]["day"][:length]
    mean = [statistics.mean(s[k] for s in series) for k in range(length)]
    if len(series) > 1:
        std = [statistics.stdev(s[k] for s in series) for k in range(length)]
    else:
        std = [0.0] * length
    return days, mean, std


def plot_curves_with_bands(results, column="I", ax=None):
    """Plot the mean `column` curve of each strategy with a +/- 1 std band."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))
    for strategy, runs in results.items():
        days, mean, std = mean_and_std(runs, column)
        low = [m - s for m, s in zip(mean, std)]
        high = [m + s for m, s in zip(mean, std)]
        line, = ax.plot(days, mean, label=f"{strategy} (n={len(runs)})")
        ax.fill_between(days, low, high, color=line.get_color(), alpha=0.2)
    names = {"S": "survivors", "I": "zombies", "R": "removed"}
    ax.set_xlabel("Day")
    ax.set_ylabel(f"Number of {names.get(column, column)}")
    ax.set_title(f"{column} over time: mean ± 1 std over seeds")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax


def plot_final_boxplot(results, ax=None):
    """Boxplot of the total number ever infected at the end of each run."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))
    names = list(results)
    finals = [[run["total_infected"][-1] for run in results[name].values()]
              for name in names]
    ax.boxplot(finals)
    ax.set_xticks(range(1, len(names) + 1), names)
    ax.set_ylabel("People ever infected")
    ax.set_title("Final infections per strategy")
    ax.grid(True, axis="y", alpha=0.3)
    return ax


def make_report_figures(results, out_dir="figures", show=True):
    """Save both figures as PNG files in `out_dir`, and optionally show them.

    Returns the list of saved file paths.
    """
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    ax = plot_curves_with_bands(results, "I")
    paths.append(os.path.join(out_dir, "infected_curves.png"))
    ax.figure.savefig(paths[-1], dpi=150, bbox_inches="tight")
    ax = plot_final_boxplot(results)
    paths.append(os.path.join(out_dir, "final_infections_boxplot.png"))
    ax.figure.savefig(paths[-1], dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    else:
        plt.close("all")
    return paths


def demo_results(seeds=5, days=150):
    """Run small demo experiments: no vaccine, early and late vaccine.

    Only a stand-in until the real batch experiments of task 4.2 exist.
    """
    from . import config
    from .model import World

    base = {k: v for k, v in vars(config).items() if k.isupper()}
    strategies = {"no vaccine": {"VACCINE_DAY": None},
                  "early vaccine (day 5)": {"VACCINE_DAY": 5},
                  "late vaccine (day 40)": {"VACCINE_DAY": 40}}
    results = {}
    for name, changes in strategies.items():
        results[name] = {}
        for seed in range(seeds):
            world = World(SimpleNamespace(**{**base, **changes,
                                             "SEED": seed}))
            run = {col: [] for col in COLUMNS[2:]}
            for _ in range(days):
                world.step()
                counts = world.get_counts()
                run["day"].append(world.day)
                for col in "SIR":
                    run[col].append(counts[col])
                run["total_infected"].append(world.get_total_infected())
            results[name][seed] = run
    return results


def main():
    """Draw the figures from a CSV given on the command line, or demo data."""
    if len(sys.argv) > 1:
        results = load_results(sys.argv[1])
    else:
        print("No CSV given: running demo experiments (about 15 runs)...")
        results = demo_results()
        save_results(results, os.path.join("results", "demo_results.csv"))
    for path in make_report_figures(results):
        print("saved", path)


if __name__ == "__main__":
    main()

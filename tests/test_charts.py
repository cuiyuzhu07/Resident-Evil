"""Tests for the result charts (task 4.4)."""
import matplotlib
matplotlib.use("Agg")

from V1.charts import (demo_results, load_results, make_report_figures,
                       mean_and_std, save_results)


def test_csv_round_trip(tmp_path):
    """Results saved to CSV are read back unchanged."""
    results = demo_results(seeds=2, days=10)
    path = tmp_path / "results.csv"
    save_results(results, str(path))
    assert load_results(str(path)) == results


def test_mean_and_std():
    """Mean and std are computed day by day over the seeds."""
    runs = {0: {"day": [1, 2], "I": [2, 4]}, 1: {"day": [1, 2], "I": [4, 8]}}
    days, mean, std = mean_and_std(runs, "I")
    assert days == [1, 2] and mean == [3, 6]
    assert std[0] > 0


def test_figures_are_saved(tmp_path):
    """Both report figures are written as PNG files."""
    results = demo_results(seeds=2, days=20)
    paths = make_report_figures(results, str(tmp_path), show=False)
    assert len(paths) == 2
    assert all((tmp_path / p.split("/")[-1]).exists() for p in paths)

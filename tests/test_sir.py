from V0 import config
from V0.model import simulate_sir


def test_population_conserved():
    S, I, R = simulate_sir(
        config.N,
        config.I0,
        config.BETA,
        config.GAMMA,
        config.DAYS
    )

    for s, i, r in zip(S, I, R):
        assert abs(s + i + r - config.N) < 1e-9
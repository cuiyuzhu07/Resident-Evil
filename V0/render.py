
import matplotlib.pyplot as plt


def plot_sir(S, I, R):
    """Plot the SIR epidemic curves."""

    days = range(len(S))

    plt.figure(figsize=(10, 6))

    plt.plot(days, S, label="Susceptible (S)")
    plt.plot(days, I, label="Infected (I)")
    plt.plot(days, R, label="Removed (R)")

    plt.xlabel("Time (days)")
    plt.ylabel("Number of people")
    plt.title("SIR Epidemic Simulation")

    plt.legend()
    plt.grid(True)

    plt.show()

#1.3

if __name__ == "__main__":
    from . import config
    from .model import simulate_sir

    S, I, R = simulate_sir(
        config.N,
        config.I0,
        config.BETA,
        config.GAMMA,
        config.DAYS
    )

    plot_sir(S, I, R)


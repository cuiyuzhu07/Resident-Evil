"""Entry point of V0: SIR reference curve + agent-based animation."""
from . import config
from .model import simulate_sir, World
from .render import plot_sir, animate_world


def main():
    """Run the SIR equations, then the agent-based simulation."""
    S, I, R = simulate_sir(config.N, config.I0, config.BETA,
                           config.GAMMA, config.DAYS)
    assert all(abs(s + i + r - config.N) < 1e-6
               for s, i, r in zip(S, I, R))
    print("SIR conservation OK")
    plot_sir(S, I, R)

    world = World(config)
    print("start:", world.get_counts())
    animation = animate_world(world, frames=300, interval=100)
    print("end:", world.get_counts())
    return animation


if __name__ == "__main__":
    main()
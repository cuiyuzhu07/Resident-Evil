
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

#2.5

def animate_world(world, frames=100, interval=100):
    """Animate moving agents and display live S/I/R counts."""

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim(0, world.size)
    ax.set_ylim(0, world.size)
    ax.set_aspect("equal")
    ax.set_title("Resident Evil - Epidemic Simulation",pad=30)
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")

    # Create scatter points and text once
    scatter = ax.scatter([], [], s=25)
    count_text = ax.text(
    0.02, 1.02, "",
    transform=ax.transAxes,
    fontsize=11,
    va="bottom"
)

    colors = {
        "S": "green",
        "I": "red",
        "R": "grey"
    }

    def update(frame):
        world.step()

        positions = world.get_positions()
        states = world.get_states()
        counts = world.get_counts()

        # Update existing points instead of drawing new ones
        scatter.set_offsets(positions)
        scatter.set_color([colors[s] for s in states])

        # Update live counts
        count_text.set_text(
            f"Day: {world.day} | "
            f"S: {counts['S']} | "
            f"I: {counts['I']} | "
            f"R: {counts['R']}"
        )

        return scatter, count_text

    animation = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=interval,
        blit=False,
        repeat=False
    )

    plt.show()
    return animation

"""Player control interface (task 4.3, member C).

A tkinter window shows the live outbreak. The player can pause it,
trigger a lockdown (everybody moves much less), start a vaccination
campaign at any moment, change the speed, or restart.

Run from the project root:
    python -m V1.interface

tkinter repeats the simulation with root.after() callbacks instead of a
while loop, so the window stays responsive.
"""
from types import SimpleNamespace

from matplotlib.figure import Figure

from . import config
from .model import World
from .render import draw_map
from .vaccine import make_vaccine_schedule

try:
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:          # tkinter is missing on some Python installs
    tk = None

LOCKDOWN_FACTOR = 0.2        # movement during a lockdown, compared to normal
COLORS = {"S": "green", "I": "red", "R": "grey"}


class Game:
    """The simulation plus the player's actions, without any window.

    Kept separate from the window so it can be tested.
    """

    def __init__(self, cfg=config):
        """Start a new outbreak. The vaccine only starts when the player asks."""
        values = {k: v for k, v in vars(cfg).items() if k.isupper()}
        values["VACCINE_DAY"] = None
        self.config = SimpleNamespace(**values)
        self.world = World(self.config)
        self.lockdown = False
        self.vaccine_started = False

    def set_lockdown(self, on):
        """Switch the lockdown on or off."""
        self.lockdown = on
        factor = LOCKDOWN_FACTOR if on else 1.0
        self.world.step_size = self.config.STEP_SIZE * factor

    def start_vaccine(self):
        """Start vaccinating from today on, until the end of the simulation."""
        if self.vaccine_started:
            return
        self.vaccine_started = True
        rate = getattr(self.config, "VACCINE_RATE", 0.05)
        today = self.world.day
        self.world.vaccine_schedule = make_vaccine_schedule(
            today, rate, today + self.config.DAYS)

    def step(self):
        """Advance the simulation by one day."""
        self.world.step()

    def finished(self):
        """The game ends when no zombie is left or the last day is reached."""
        no_zombies = self.world.get_counts()["I"] == 0
        return no_zombies or self.world.day >= self.config.DAYS

    def status(self):
        """Return a one-line summary of the current day."""
        c = self.world.get_counts()
        text = (f"Day {self.world.day}   Survivors {c['S']}   "
                f"Zombies {c['I']}   Removed {c['R']}   "
                f"Vaccinated {self.world.get_vaccinated_count()}")
        if hasattr(self.world, "zombies_killed"):
            text += f"   Killed {self.world.zombies_killed}"
        return text


class App:
    """The tkinter window: a map of the outbreak and control buttons."""

    def __init__(self, root):
        """Build the window and draw the first frame."""
        self.root = root
        self.root.title("Resident Evil - Outbreak control")
        self.running = False
        self.job = None

        self.figure = Figure(figsize=(6, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,
                                         expand=True)

        self.status = tk.Label(root, text="", font=("Helvetica", 13))
        self.status.pack(side=tk.TOP, pady=4)

        bar = tk.Frame(root)
        bar.pack(side=tk.TOP, pady=6)
        self.play_button = tk.Button(bar, text="Start", width=10,
                                     command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=4)
        self.lockdown_button = tk.Button(bar, text="Lockdown: OFF", width=14,
                                         command=self.toggle_lockdown)
        self.lockdown_button.pack(side=tk.LEFT, padx=4)
        self.vaccine_button = tk.Button(bar, text="Start vaccine", width=12,
                                        command=self.start_vaccine)
        self.vaccine_button.pack(side=tk.LEFT, padx=4)
        tk.Button(bar, text="Restart", width=8,
                  command=self.restart).pack(side=tk.LEFT, padx=4)

        self.speed = tk.Scale(root, from_=10, to=500, orient=tk.HORIZONTAL,
                              label="Delay between days (ms)", length=300)
        self.speed.set(100)
        self.speed.pack(side=tk.TOP, pady=4)

        self.restart()

    def new_axes(self):
        """Clear the map and draw the fixed parts and empty markers."""
        world = self.game.world
        self.ax.clear()
        self.ax.set_xlim(0, world.size)
        self.ax.set_ylim(0, world.size)
        self.ax.set_aspect("equal")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        draw_map(self.ax, world)
        self.crates = self.ax.scatter([], [], s=30, marker="s",
                                      color="saddlebrown")
        self.dots = self.ax.scatter([], [], s=25)

    def draw(self):
        """Update the markers and the status line for the current day."""
        world = self.game.world
        self.dots.set_offsets(world.get_positions())
        self.dots.set_color([COLORS[s] for s in world.get_states()])
        supplies = getattr(world, "supplies", [])
        self.crates.set_offsets([(c["x"], c["y"]) for c in supplies]
                                or [(float("nan"), float("nan"))])
        self.status.config(text=self.game.status())
        self.canvas.draw_idle()

    def tick(self):
        """Run one day, redraw, and plan the next day with root.after()."""
        self.job = None
        if not self.running:
            return
        self.game.step()
        self.draw()
        if self.game.finished():
            self.running = False
            self.play_button.config(text="Start", state=tk.DISABLED)
            self.status.config(text=self.game.status() + "   (game over)")
            return
        self.job = self.root.after(self.speed.get(), self.tick)

    def toggle_play(self):
        """Start or pause the simulation."""
        self.running = not self.running
        self.play_button.config(text="Pause" if self.running else "Start")
        if self.running and self.job is None:
            self.tick()

    def toggle_lockdown(self):
        """Switch the lockdown on or off."""
        self.game.set_lockdown(not self.game.lockdown)
        state = "ON" if self.game.lockdown else "OFF"
        self.lockdown_button.config(text=f"Lockdown: {state}")

    def start_vaccine(self):
        """Start the vaccination campaign (only once per game)."""
        self.game.start_vaccine()
        self.vaccine_button.config(text="Vaccinating...", state=tk.DISABLED)

    def restart(self):
        """Start a fresh outbreak with all controls reset."""
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.running = False
        self.game = Game()
        self.play_button.config(text="Start", state=tk.NORMAL)
        self.lockdown_button.config(text="Lockdown: OFF")
        self.vaccine_button.config(text="Start vaccine", state=tk.NORMAL)
        self.new_axes()
        self.draw()


def main():
    """Open the control window."""
    if tk is None:
        print("tkinter is not available in this Python installation.")
        return
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

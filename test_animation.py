from V0 import config
from V0.model import World
from V0.render import animate_world

world = World(config)
animation = animate_world(world, frames=100, interval=100)
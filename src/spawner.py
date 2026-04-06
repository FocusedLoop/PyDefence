import random as rand
from src.entities import enemy

def spawn_enemies(world, count=1):
    enemies = []
    for _ in range(count):
        spawn = rand.randint(0, world.map['xy'][0] - 1), rand.randint(0, world.map['xy'][1] - 1)
        new_enemy = enemy(world, spawn)
        enemies += [new_enemy]
    
    return enemies
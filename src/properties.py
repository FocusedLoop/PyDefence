from src.seed import world
from src.entities import enemy
import random as rand

class game():
    def __init__(self, world, max_time=2400):
        self.world = world
        self.max_time = max_time
        self.time = 0
        self.enemies = []
        self.humans = [] # TODO: WILL BE A SUBCLASS OF ENTITY, WITH HEALTH, DAMAGE, AND OTHER PROPERTIESs
    
    def pass_time(self):
        self.time += 1
        if self.time >= self.max_time:
            self.time = 0
            return True
        return False
    
    def spawn_enmies(self, count=1):
        for _ in range(count):
            spawn = rand.randint(0, self.world.map['xy'][0] - 1), rand.randint(0, self.world.map['xy'][1] - 1)
            new_enemy = enemy(self.world, spawn)
            self.enemies += [new_enemy]
        return self.enemies
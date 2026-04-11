from src.seed import world
from src.entities import enemy
import random as rand

class game():
    def __init__(self, world, events_of_day):
        self.world = world
        self.events_of_day = sorted(events_of_day)
        self.time = 0
        self.event_index = 0
        self.enemies = []
        self.humans = [] # TODO: WILL BE A SUBCLASS OF ENTITY, WITH HEALTH, DAMAGE, AND OTHER PROPERTIESs

    def pass_time(self, tick_rate=0.05):
        self.time += tick_rate
        next_event = self.events_of_day[self.event_index]
        if self.time >= next_event[0]:
            self.event_index += 1
            if self.event_index >= len(self.events_of_day):
                self.event_index = 0
                self.time = 0
            return next_event
        return None
    
    def spawn_enmies(self, count=1):
        for _ in range(count):
            spawn = rand.randint(0, self.world.map['xy'][0] - 1), rand.randint(0, self.world.map['xy'][1] - 1)
            new_enemy = enemy(self.world, spawn)
            self.enemies += [new_enemy]
        return self.enemies
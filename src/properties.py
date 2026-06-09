from src.seed import world
from src.entities import enemy, humans
from src import debug
import random as rand
import time

class game():
    def __init__(self, world, events_of_day, world_events, tick_rate=0.05, seconds_per_hour=1.0):
        self.world = world
        self.events_of_day = sorted(events_of_day)
        self.world_events = world_events

        self.seconds_per_hour = seconds_per_hour # real seconds per in-game hour
        self.time = 0
        self.event_index = 0
        self.enemies = []
        self.humans = [] # TODO: WILL BE A SUBCLASS OF ENTITY, WITH HEALTH, DAMAGE, AND OTHER PROPERTIESs

        self.tick_rate = tick_rate
        self.last_tick = 0
    
    def game_tick(self, display):
        now = time.time()
        if now - self.last_tick >= self.tick_rate:
            self.last_tick = now
            event = self.pass_world_time(self.tick_rate)
            if event:
                display.set_brightness(event[1])
            for enemy in self.enemies: enemy.brain()
            for human in self.humans: human.brain()

    def pass_world_time(self, tick_rate=0.05):
        self.time += tick_rate / self.seconds_per_hour
        next_event = self.events_of_day[self.event_index]

        # debug.watch("time", round(self.time, 2))
        # debug.watch("event", next_event[2])
        # debug.watch("enemies", len(self.enemies))

        if self.time >= next_event[0]:
            self.event_index += 1
            if self.event_index >= len(self.events_of_day):
                self.event_index = 0
                self.time = 0
            return next_event
        return None
    
    def select_world_event(self):
        weights = [chance for chance, _ in self.world_events]
        chosen_event = rand.choices(self.world_events, weights=weights)[0]

        debug.watch("world_event_chance", chosen_event)
        debug.watch("Chosen event", chosen_event[1])
        self._trigger_world_event(chosen_event[1])
    
    def _trigger_world_event(self, event_name):
        if event_name == "PEACE": return
        elif event_name == "RAID":
            self.spawn_entities(entity="enemy", count=5)
        elif event_name == "FLASH_STORM":
            debug.watch("world_event", "FLASH_STORM - NOT IMPLEMENTED")
    
    def spawn_entities(self, entity="enemy", spawn_location=None, count=1):
        if spawn_location is None:
            spawn_location = lambda: (rand.randint(0, self.world.map['xy'][0] - 1), rand.randint(0, self.world.map['xy'][1] - 1))
        for _ in range(count):
            spawn = spawn_location()
            if entity == "enemy":
                new_enemy = enemy(self.world, spawn)
                self.enemies += [new_enemy]
            elif entity == "human":
                new_human = humans(self.world, spawn)
                self.humans += [new_human]

        return self.enemies if entity == "enemy" else self.humans
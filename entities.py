class entity:
    def __init__(self, world, xy=[25, 25]):
        self.type = "entity", 1
        self.xy = xy
        self.health = 100
        self.starting_position(world)
    
    # Place player on the map at the starting position
    def starting_position(self, world):
        map_data = world.map
        index = self.xy[0] * map_data['xy'][1] + self.xy[1]
        map_data['nodes'][index].type = self.type

import random as rand

# Tile types: (probability, id)
tile_type = {
    "empty": (0.95, 0),
    "rock": (0.015, 7),
    "tree": (0.025, 8),
    "bush": (0.010, 9),
    "leaf": (0.0, 10),
}

# Create each node
class node:
    def __init__(self, xy):
        self.xy = xy
        self.type = None
        self.neighbours = []
        self.processed = False

    def createTile(self):
        select_tile = rand.random()
        total_prob = 0
        for tile, (prob, id_value) in tile_type.items():
            total_prob += prob
            if select_tile <= total_prob:
                self.type = (tile, id_value)
                return
        self.type = "empty", 0

    def createObject(self, map_data):
        if self.processed:
            return

        if self.type[1] == tile_type["tree"][1]:
            formation_coords = [(0, 0), (-1, 0)]
            self.placeObject(map_data, formation_coords, "tree", clear_area=True)

        elif self.type[1] == tile_type["rock"][1]:
            formation_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
            self.placeObject(map_data, formation_coords, "rock", clear_area=True)

        elif self.type[1] == tile_type["bush"][1]:
            formation_coords = [(0, 0)]
            self.placeObject(map_data, formation_coords, "bush", clear_area=True)

    def placeObject(self, map_data, formation_coords, object_type, clear_area=False):
        object_nodes = []
        for dx, dy in formation_coords:
            x, y = self.xy[0] + dx, self.xy[1] + dy
            if 0 <= x < map_data['xy'][0] and 0 <= y < map_data['xy'][1]:
                index = x * map_data['xy'][1] + y
                n2 = map_data['nodes'][index]
                object_nodes.append(n2)

        if clear_area:
            surrounding_nodes = []
            for obj_node in object_nodes:
                for n in obj_node.neighbours:
                    if n not in object_nodes:
                        surrounding_nodes.append(n)

            surrounding_nodes = list(set(surrounding_nodes))
            for n in surrounding_nodes:
                n.type = ("empty", 0)
                n.processed = True

        for obj_node in object_nodes:
            if object_type == "tree" and obj_node != self:
                obj_node.type = ("leaf", 10)
            else:
                obj_node.type = (object_type, tile_type[object_type][1])
            obj_node.processed = True

        self.processed = True


class world:
    def __init__(self, xy=[100, 100], seed=None, spread=3):
        self.map = {
            "xy": xy,
            "nodes": [],
            "seed": seed,
            "choice": [-100, 100]
        }
        self.spread = spread

    # Generate the full world
    def generate(self):
        self.genSeed()
        self.genNodes()
        self.getNeighbours()
        #self.genRivers()    #FUTURE FEATURE
        #self.genMountains() #FUTURE FEATURE
        self.setTile()
        self.clearExtras()

    # Create a seed to make everything random
    def genSeed(self):
        seed = self.map['seed']
        if seed is None:
            seed = round(rand.randint(0, 999999) + rand.randint(0, 999999) * 3.145 ** rand.choice(self.map['choice']))
        self.map['seed'] = rand.seed(seed)

    # Plot the nodes on the map
    def genNodes(self):
        for i in range(self.map['xy'][0]):
            for j in range(self.map['xy'][1]):
                self.map['nodes'].append(node([i, j]))

    # Get all node neighbours
    def getNeighbours(self):
        tiles = list(self.map['nodes'])
        for n1 in self.map['nodes']:
            for n2 in tiles:
                if n1 != n2:
                    distance = max(abs(n1.xy[0] - n2.xy[0]), abs(n1.xy[1] - n2.xy[1]))
                    if distance <= self.spread:
                        n1.neighbours.append(n2)

    # Create the tiles
    def setTile(self):
        for n in self.map['nodes']:
            n.createTile()
        for n in self.map['nodes']:
            n.createObject(self.map)

    # Clear left over tiles
    def clearExtras(self):
        for n in self.map['nodes']:
            if n.type[1] in [tile_type["tree"][1], tile_type["leaf"][1], tile_type["rock"][1]]:
                validNeighbour = False
                for neighbor in n.neighbours:
                    if neighbor.type[1] != tile_type["empty"][1]:
                        validNeighbour = True
                        break
                if not validNeighbour:
                    n.type = ("empty", 0)


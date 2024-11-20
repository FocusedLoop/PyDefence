import numpy as np
import random as rand
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# Map Configuration
map = {
    "xy":[100, 100],
    "nodes":[],
    'seed':None,
    'choice':[-100, 100]
}

tile_type = {
    "empty": (0.95, 0),
    "rock": (0.015, 7),
    "tree": (0.025, 8),
    "bush": (0.010, 9),
    "leaf": (0.0, 10),
}

spread = 3

# Create a seed to make everything random
def genSeed():
    seed = map['seed']
    if seed == None:
        seed = round(rand.randint(0, 999999) + rand.randint(0, 999999) * 3.145 ** rand.choice(map['choice']))
    map['seed'] = rand.seed(seed)

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

    def createObject(self, n1):
        if n1.processed:
            return

        if n1.type[1] == tile_type["tree"][1]:
            formation_coords = [(0, 0), (-1, 0)]
            self.placeObject(n1, formation_coords, "tree", clear_area=True)

        elif n1.type[1] == tile_type["rock"][1]:
            formation_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
            self.placeObject(n1, formation_coords, "rock", clear_area=True)

        elif n1.type[1] == tile_type["bush"][1]:
            formation_coords = [(0, 0)]
            self.placeObject(n1, formation_coords, "bush", clear_area=True)
            
    def placeObject(self, n1, formation_coords, object_type, clear_area=False):
        object_nodes = []
        for dx, dy in formation_coords:
            x, y = n1.xy[0] + dx, n1.xy[1] + dy
            if 0 <= x < map['xy'][0] and 0 <= y < map['xy'][1]:
                index = x * map['xy'][1] + y
                n2 = map['nodes'][index]
                object_nodes.append(n2)

        if clear_area:
            surrounding_nodes = []
            for node in object_nodes:
                for n in node.neighbours:
                    if n not in object_nodes:
                        surrounding_nodes.append(n)

            surrounding_nodes = list(set(surrounding_nodes))
            for n in surrounding_nodes:
                n.type = ("empty", 0)
                n.processed = True

        for node in object_nodes:
            if object_type == "tree" and node != n1:
                node.type = ("leaf", 10)
            else:
                node.type = (object_type, tile_type[object_type][1])
            node.processed = True

        n1.processed = True

# Plot the node on the map
def genNodes():
    for i in range(map['xy'][0]):
        for j in range(map['xy'][1]):
            map['nodes'].append(node([i, j]))

# Get all node neighbours
def getNeighbours(spread):
    tiles = []
    for n in map['nodes']:
        tiles.append(n)
    for n1 in map['nodes']:
        for n2 in tiles:
            if n1 != n2:
                distance = max(abs(n1.xy[0] - n2.xy[0]), abs(n1.xy[1] - n2.xy[1]))
                if distance <= spread:
                    n1.neighbours.append(n2)

# Create the tiles
def setTile():
    for n in map['nodes']:
        n.createTile()
    
    for n in map['nodes']:
        n.createObject(n)

# Clear left over tiles
def clearExtras():
    for n in map['nodes']:
        if n.type[1] in [tile_type["tree"][1], tile_type["leaf"][1], tile_type["rock"][1]]:
            validNeighbour = False
            for neighbor in n.neighbours:
                if neighbor.type[1] != tile_type["empty"][1]:
                    validNeighbour = True
                    break
            if not validNeighbour:
                n.type = ("empty", 0)

# Generate a visual display
def renderMap():
    tile_colours = {
        0: 'green',
        7: 'grey',
        8: 'brown',
        9: 'lightgreen',
        10: 'darkgreen'
    }
    cmap = ListedColormap([tile_colours[key] for key in sorted(tile_colours.keys())])
    bounds = sorted(tile_colours.keys()) + [max(tile_colours.keys()) + 1]
    norm = BoundaryNorm(bounds, cmap.N)
    world = np.matrix(np.full((map["xy"]), tile_type["empty"][1], dtype=int))

    for n in map['nodes']:
        x, y = n.xy
        world[x, y] = n.type[1]
    print(world)
    plt.imshow(world, cmap=cmap, norm=norm, interpolation="nearest")
    plt.show()

# Generate
genSeed()
genNodes()
getNeighbours(spread)
#genRivers() #FUTURE FEATURE
#genMountains() #FUTURE FEATURE
setTile()
clearExtras()

# Text Display
# for n in map['nodes']:
#     n_XY = [neighbour.xy for neighbour in  n.neighbours]
#     print(f"XY: {n.xy}, Tile Type: {n.type}, Neighbours: {n_XY}")

renderMap()


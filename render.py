import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

class render:
    @staticmethod
    def render_methods(method):
        if method == "terminal":
            return render.terminal_render
        elif method == "gui":
            return render.matplotlib_render
        else:
            raise ValueError("Invalid render method specified. Use 'terminal' or 'gui'.")
    
    def __init__(self, mode = "terminal"):
        self.mode = render.render_methods(mode)

    # Render the world in the terminal
    def terminal_render(self, map):
        tile_chars = {
            0:  '\033[48;2;34;139;34m  \033[0m',   # empty: forest green bg
            7:  '\033[47m  \033[0m',               # rock: grey bg
            8:  '\033[48;2;101;67;33m  \033[0m',   # tree: dark brown trunk
            9:  '\033[48;2;50;205;50m  \033[0m',   # bush: lime green bg
            10: '\033[48;2;0;100;0m  \033[0m',     # leaf: dark green canopy
        }

        for x in range(map['xy'][0]):
            row = ''
            for y in range(map['xy'][1]):
                index = x * map['xy'][1] + y
                tile_id = map['nodes'][index].type[1]
                row += tile_chars.get(tile_id, '  ')
            print(row)

    # Generate a visual display of the world using matplotlib
    def matplotlib_render(self, map):
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
        world = np.matrix(np.full((map["xy"]), 0, dtype=int))

        for n in map['nodes']:
            x, y = n.xy
            world[x, y] = n.type[1]
        plt.imshow(world, cmap=cmap, norm=norm, interpolation="nearest")
        plt.show()
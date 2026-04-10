import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import curses

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
    
    def set_night(self, tilte_map):
        for tile_id in tilte_map:
            tilte_map[tile_id] = tuple(color // 4 for color in tilte_map[tile_id])
        return tilte_map

    # Render the world in the terminal using curses
    def terminal_render(self, map, stdscr, night_mode=False):
        map_data = map.map

        tile_render = {
            0:  (133, 545, 133), # empty: forest green
            7:  (753, 753, 753), # rock: grey
            8:  (396, 263, 129), # tree: dark brown
            9:  (196, 804, 196), # bush: lime green
            10: (0, 392, 0), # leaf: dark green

            1: (0, 0, 1000), # player: blue
            2: (1000, 0, 0) # enemy: red
        }

        if night_mode:
            tile_render = render.set_night(self, tile_render)

        # Initialize color pairs for curses
        if not hasattr(render, '_colors_init'):
            curses.start_color()
            curses.use_default_colors()
            for i, (tile_id, (r, g, b)) in enumerate(tile_render.items(), start=1):
                curses.init_color(i, r, g, b)
                curses.init_pair(i, -1, i)
            render._colors_init = True

        # Apply color pairs
        tile_colors = {
            tile_id: curses.color_pair(i)
            for i, tile_id in enumerate(tile_render, start=1)
        }

        max_y, max_x = stdscr.getmaxyx()

        for x in range(min(map_data['xy'][0], max_y)):
            for y in range(min(map_data['xy'][1], max_x // 2)):
                index = x * map_data['xy'][1] + y
                tile_id = map_data['nodes'][index].type[1]
                color = tile_colors.get(tile_id, curses.color_pair(0))
                try:
                    stdscr.addstr(x, y * 2, '  ', color)
                except curses.error:
                    pass

    # Generate a visual display of the world using matplotlib
    # NOTE: DEPRECATED
    # TODO: REFACTOR INTO MY OWN RENDERING SYSTEM WITH SDL2
    def matplotlib_render(self, map):
        tile_colours = {
            0: 'green',
            7: 'grey',
            8: 'brown',
            9: 'lightgreen',
            10: 'darkgreen',

            -1: 'blue',
            -2: 'red'
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
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

    # Render the world in the terminal using curses
    def terminal_render(self, map, stdscr):
        import curses
        map_data = map.map

        # Init custom RGB colours
        if not hasattr(render, '_colors_init'):
            curses.start_color()
            curses.use_default_colors()

            # Define custom colors (id, r, g, b)
            curses.init_color(10, 133, 545, 133)   # forest green
            curses.init_color(11, 753, 753, 753)   # grey
            curses.init_color(12, 396, 263, 129)   # dark brown
            curses.init_color(13, 196, 804, 196)   # lime green
            curses.init_color(14, 0,   392, 0)     # dark green
            curses.init_color(15, 1000, 0,  0)     # red

            # Init pairs (pair_id, fg, bg)
            curses.init_pair(1, -1, 10)   # empty: forest green
            curses.init_pair(2, -1, 11)   # rock: grey
            curses.init_pair(3, -1, 12)   # tree: dark brown
            curses.init_pair(4, -1, 13)   # bush: lime green
            curses.init_pair(5, -1, 14)   # leaf: dark green
            curses.init_pair(6, -1, 15)   # player: red
            render._colors_init = True

        tile_colors = {
            0:  curses.color_pair(1),
            7:  curses.color_pair(2),
            8:  curses.color_pair(3),
            9:  curses.color_pair(4),
            10: curses.color_pair(5),
            -1: curses.color_pair(6),
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
    # TODO: REFACTOR INTO MY OWN RENDERING SYSTEM
    def matplotlib_render(self, map):
        tile_colours = {
            0: 'green',
            7: 'grey',
            8: 'brown',
            9: 'lightgreen',
            10: 'darkgreen',

            -1: 'red'
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
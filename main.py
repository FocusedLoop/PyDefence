from seed import world
from render import render
from entities import player, enemy
import curses

# Initialize the world
generated_world = world(xy=[200, 200], spread=3)
generated_world.generate()

# Initialize the player and enemy entities
player = player(generated_world, xy=[25, 25])
enemy = enemy(generated_world)

def game(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    stdscr.timeout(50)
    display = render(mode="terminal")

    # Main Game Loop
    while True:
        key = stdscr.getch()
        player.handle_input(key)
        enemy.brain()
        stdscr.erase()
        display.mode(display, generated_world, stdscr)
        stdscr.refresh()

curses.wrapper(game)
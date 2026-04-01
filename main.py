from seed import world
from render import render
from input import inputHandler, player
import curses

# Initialize the world
generated_world = world(xy=[100, 100], spread=3)
generated_world.generate()

# Initialize the player and input handler
player_character = player(generated_world)
handler = inputHandler(generated_world, player_character)

def game(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    stdscr.timeout(50)
    display = render(mode="terminal")

    # Main Game Loop
    while True:
        key = stdscr.getch()
        handler.handle_input(key)
        stdscr.erase()
        display.mode(display, generated_world, stdscr)
        stdscr.refresh()

curses.wrapper(game)
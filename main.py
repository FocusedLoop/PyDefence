from src.seed import world
from src.render import render
from src.entities import player
from src.properties import game

import curses
import time

# Initialize the world
generated_world = world(xy=[200, 200], spread=3)
generated_world.generate()

# Initialize the player and game state
player = player(generated_world, xy=[25, 25])
game = game(generated_world, 3)

enemies = game.spawn_enmies(count=25)

def game_loop(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    display = render(mode="terminal")
    tick_rate = 0.05
    last_tick = time.time()

    # Main Game Loop
    while True:
        key = stdscr.getch()
        player.handle_input(key)
        is_night = game.pass_time()

        # Update enemy states at a fixed tick rate
        now = time.time()
        if now - last_tick >= tick_rate:
            last_tick = now
            for enemy in enemies: enemy.brain()

        stdscr.erase()
        display.mode(display, generated_world, stdscr, is_night)
        stdscr.refresh()

curses.wrapper(game_loop)
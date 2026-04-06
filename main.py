from src.seed import world
from src.render import render
from src.entities import player
from src.spawner import spawn_enemies
import curses
import time

# Initialize the world
generated_world = world(xy=[200, 200], spread=3)
generated_world.generate()

# Initialize the player and enemy entities
player = player(generated_world, xy=[25, 25])
enemies = spawn_enemies(generated_world, count=25)

def game(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    display = render(mode="terminal")
    tick_rate = 0.05  # 50ms per tick
    last_tick = time.time()

    # Main Game Loop
    while True:
        key = stdscr.getch()
        player.handle_input(key)

        now = time.time()
        if now - last_tick >= tick_rate:
            last_tick = now
            # Update enemy states
            for enemy in enemies: enemy.brain()

        stdscr.erase()
        display.mode(display, generated_world, stdscr)
        stdscr.refresh()

curses.wrapper(game)
from src.seed import world
from src.render import render
from src.entities import player
from src.properties import game
import curses, time

# Initialize the world
generated_world = world(xy=[200, 200], spread=3)
generated_world.generate()

# Initialize the player and game state
player = player(generated_world, xy=[25, 25])

events_of_day = [
    (10, "Dawn", 0.7),
    (60, "Morning", 0.85),
    (120, "Afternoon", 1.0),
    (180, "Evening", 0.5),
    (240, "Night", 0.25)
]
game = game(generated_world, events_of_day)

enemies = game.spawn_enmies(count=25)

def game_loop(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    display = render(mode="terminal")
    tick_rate = 0.05
    last_tick = time.time()

    display.set_brightness(events_of_day[0][2]) # Dawn brightness

    # Main Game Loop
    while True:
        key = stdscr.getch()
        player.handle_input(key)

        # Update enemy states at a fixed tick rate
        now = time.time()
        if now - last_tick >= tick_rate:
            last_tick = now
            event = game.pass_time(tick_rate)
            if event:
                display.set_brightness(event[2])
            for enemy in enemies: enemy.brain()

        stdscr.erase()
        display.mode(display, generated_world, stdscr)
        stdscr.refresh()

curses.wrapper(game_loop)
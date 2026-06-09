from src.seed import world
from src.render import render
from src.entities import player
from src.properties import game
import curses, time

# Initialize the world
generated_world = world(xy=[100, 100], spread=3)
generated_world.generate()

# Initialize the player and game state
player = player(
    generated_world, 
    xy=[25, 25]
)

game = game(
    generated_world, 
    events_of_day = [
        # Hour, Brightness, Event Name
        (1,     0.7,        "DAWN"),
        (6,     0.85,       "MORNING"),
        (12,    1.0,        "AFTERNOON"),
        (18,    0.5,        "EVENING"),
        (24,    0.25,       "NIGHT")
    ],
    world_events = [
        # Chance, Event Name
        (80,    "PEACE"),
        (0.005, "RAID"),
        (0.01,  "FLASH_STORM"),
    ],
    tick_rate=0.05,
    seconds_per_hour=2
)

game.spawn_entities(entity="human", count=1)

# Maain Game Loop
def game_loop(stdscr):
    # Setup Rendering
    curses.curs_set(0)
    stdscr.nodelay(True) # non blocking input
    display = render(mode="terminal")
    last_frame = time.perf_counter()

    display.set_brightness(game.events_of_day[0][1]) # Dawn brightness

    # Main Game Loop
    while True:
        key = stdscr.getch()
        player.handle_input(key)        
        game.game_tick(display)
        game.select_world_event()
        last_frame = display.fps_counter(last_frame)

        stdscr.erase()
        display.mode(display, generated_world, stdscr)
        stdscr.refresh()

curses.wrapper(game_loop)
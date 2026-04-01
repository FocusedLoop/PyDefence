# Handle user input, key bindings, and navigation logic
class inputHandler:
    def __init__(self, world, player):
        # Process Input and return the corresponding action
        nav = navigation(world, player)

        # TODO: MAY NEED TO CHNAGE TO LAMBDA FUNCTION TO AVOID CALLING THE FUNCTION IMMEDIATELY
        self.key_bindings = {
            'w': lambda: nav.move('MOVE_UP'),
            'a': lambda: nav.move('MOVE_LEFT'),
            's': lambda: nav.move('MOVE_DOWN'),
            'd': lambda: nav.move('MOVE_RIGHT'),
            'q': lambda: exit()
        }
    
    def handle_input(self, key):
        if key == ord('q'):
            exit()
        if key != -1:
            action = self.key_bindings.get(chr(key))
            if action:
                action()
    
# Take w(acsess the map) -> matrix of tile types
class navigation:
    def __init__(self, world, player):
        self.world = world
        self.player = player

    # Validate the move based on world boundaries and obstacles
    def move(self, direction):
        x, y = self.player.xy
        if direction == 'MOVE_UP':
            new_x, new_y = x - 1, y
        elif direction == 'MOVE_DOWN':
            new_x, new_y = x + 1, y
        elif direction == 'MOVE_LEFT':
            new_x, new_y = x, y - 1
        elif direction == 'MOVE_RIGHT':
            new_x, new_y = x, y + 1
        else:
            return False

        if self.world.validateMove(new_x, new_y):
            map_data = self.world.map
            # Clear old tile
            old_index = x * map_data['xy'][1] + y
            map_data['nodes'][old_index].type = ("empty", 0)
            # Set new tile
            new_index = new_x * map_data['xy'][1] + new_y
            map_data['nodes'][new_index].type = ("player", -1)
            self.player.xy = [new_x, new_y]
            return True
        return False
    
# TODO MOVE BELLOW TO SEPARATE FILES
class player:
    def __init__(self, world, xy=[25, 25]):
        self.type = "player", -1
        self.xy = xy
        self.health = 100
        self.starting_position(world)
    
    # Place player on the map at the starting position
    def starting_position(self, world):
        map_data = world.map
        index = self.xy[0] * map_data['xy'][1] + self.xy[1]
        map_data['nodes'][index].type = self.type
        
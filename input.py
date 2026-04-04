# Handle user input, key bindings, and worldInteraction logic
class inputHandler:
    def __init__(self, world, entity):
        # Process Input and return the corresponding action
        controller = entityController(world, entity)

        # TODO: MAY NEED TO CHNAGE TO LAMBDA FUNCTION TO AVOID CALLING THE FUNCTION IMMEDIATELY
        self.key_bindings = {
            'w': lambda: controller.move('MOVE_UP'),
            'a': lambda: controller.move('MOVE_LEFT'),
            's': lambda: controller.move('MOVE_DOWN'),
            'd': lambda: controller.move('MOVE_RIGHT'),
            'e': lambda: controller.interact('PLACE'),
            'r': lambda: controller.interact('REMOVE'),
            'q': lambda: exit()
        }
    
    def handle_input(self, key):
        if key != -1:
            action = self.key_bindings.get(chr(key))
            if action: action()
    
# Take w(acsess the map) >> matrix of tile types
class entityController:
    def __init__(self, world, entity):
        self.world = world
        self.entity = entity

    # Validate the move based on world boundaries and obstacles
    def move(self, direction):
        x, y = self.entity.xy
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
            self.world.clearTile(x, y)
            new_pos = self.world.setTile(new_x, new_y, self.entity.type)
            if new_pos != [-1, -1]:
                self.entity.xy = new_pos

            return True
        return False

    def interact(self, action):
        object_x, object_y = self.entity.xy

        # Place a object in front of the player
        if action == 'PLACE':
            object_x, object_y = object_x - 1, object_y
            index = object_x * self.world.map['xy'][1] + object_y # TODO: TURN INTO A METHOD IN THE WORLD CLASS >> CheckTile(x, y)
            if self.world.map['nodes'][index].type == ("empty", 0):
                self.world.setTile(object_x, object_y, ("tree", 8))
        
        if action == 'REMOVE':
            object_x, object_y = object_x - 1, object_y
            index = object_x * self.world.map['xy'][1] + object_y
            if self.world.map['nodes'][index].type != ("enemy", 2):
                self.world.clearTile(object_x, object_y)
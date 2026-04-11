import random as rand
from .input import entityController, inputHandler

class entity:
    def __init__(self, world, xy=[0, 0], type=("entity", 1)):
        self.type = type
        self.xy = xy
        self.health = 100
        self.starting_position(world)
    
    # Place player on the map at the starting position
    def starting_position(self, world):
        map_data = world.map
        index = self.xy[0] * map_data['xy'][1] + self.xy[1]
        map_data['nodes'][index].type = self.type

class player(entity):
    def __init__(self, world, xy=[0, 0], type=("player", 1)):
        entity.__init__(self, world, xy, type)
        self.input = inputHandler(world, self)
        self.handle_input = self.input.handle_input

# TODO: MOVE ENEMY STATE AND POSSIBLE ACTIONS TO ENTITY
class humans(entity, entityController):
    def __init__(self, world, xy=[0, 0], state = [], actions = [], type=("human", 3)):
        entity.__init__(self, world, xy, type)
        entityController.__init__(self, world, self)


class enemy(entity, entityController):
    def __init__(self, world, xy=[0, 0], state = [], actions = [], type=("enemy", 2)):
        entity.__init__(self, world, xy, type)
        entityController.__init__(self, world, self)

        self.state = [
            ("TOWARDS_PLAYERS", 0.65),
            ("OBSTACLE_AVOIDANCE", 0.2),
            ("RANDOM_MOVE", 0.15)
            
        ] + state
        self.last_direction = None
        self.possible_actions = [
            "MOVE_UP",
            "MOVE_DOWN",
            "MOVE_LEFT",
            "MOVE_RIGHT",
        ] + actions
    
    # State the actions of the entity
    # TODO: IMRPOVE AI CHOICE MAKING, SPERATE CLASS WITH STACK OF ACTIONS AND PROBABILITIES
    def brain(self):
        states, weights = zip(*self.state)
        chosen = rand.choices(states, weights)[0]
        if chosen == "TOWARDS_PLAYERS":
            self.move_towards_player()
        elif chosen == "RANDOM_MOVE":
            self.random_move()
        elif chosen == "OBSTACLE_AVOIDANCE":
            self.avoid_obstacles()
    
    # Move towards the player by comparing the enemy's position to the player's position and moving in the direction that reduces the distance
    def move_towards_player(self):
        player_positions = self.world.findPlayersPosition()
        if not player_positions:
            return
            
        player_x, player_y = player_positions[0]  # TODO: HANDLE MULTIPLE PLAYERS
        enemy_x, enemy_y = self.xy[0] - player_x, self.xy[1] - player_y
        if abs(enemy_x) > abs(enemy_y):
            if enemy_x > 0:
                self.move("MOVE_UP")
            else:
                self.move("MOVE_DOWN")
        else:
            if enemy_y > 0:
                self.move("MOVE_LEFT")
            else:
                self.move("MOVE_RIGHT")
    
    # Avoid obstacles by checking the surrounding tiles and trying to move in a different direction if the path towards the player is blocked.
    def avoid_obstacles(self):
        enemy_x, enemy_y = self.xy

        # TODO MOVE LOGIC CLOSE TO self.state
        opposites = {
            "MOVE_UP": "MOVE_DOWN", 
            "MOVE_DOWN": "MOVE_UP",
            "MOVE_LEFT": "MOVE_RIGHT", 
            "MOVE_RIGHT": "MOVE_LEFT"
        }

        directions = {
            "MOVE_UP": (enemy_x - 1, enemy_y),
            "MOVE_DOWN": (enemy_x + 1, enemy_y),
            "MOVE_LEFT": (enemy_x, enemy_y - 1),
            "MOVE_RIGHT": (enemy_x, enemy_y + 1)
        }

        # Try all passable directions except the opposite of the last move
        for dir, (nx, ny) in directions.items():
            if dir == opposites.get(self.last_direction):
                continue
            if self.world.CheckTile(nx, ny) in [("empty", 0), ("player", 1)]:
                if self.move(dir):
                    self.last_direction = dir
                    return

        # If stuck, allow backtracking as a last resort
        backward = opposites.get(self.last_direction)
        if backward and self.move(backward):
            self.last_direction = backward

    # Randomly move the entity in one of the possible directions
    def random_move(self):
        chosen = rand.choice(self.possible_actions)
        self.move(chosen)


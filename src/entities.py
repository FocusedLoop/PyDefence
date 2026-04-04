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
        

class enemy(entity, entityController):
    def __init__(self, world, xy=[0, 0], state = [], actions = [], type=("enemy", 2)):
        entity.__init__(self, world, xy, type)
        entityController.__init__(self, world, self)

        self.state = [
            "TOWARDS_PLAYERS",
            #"RANDOM_MOVE"
            #"OBSTACLE_AVOIDANCE"
        ] + state
        self.possible_actions = [
            "MOVE_UP",
            "MOVE_DOWN",
            "MOVE_LEFT",
            "MOVE_RIGHT",
        ] + actions
        
        # self.starting_position(world)
    
    # State the actions of the entity
    # TODO: IMRPOVE AI CHOICE MAKING, SPERATE CLASS WITH STACK OF ACTIONS AND PROBABILITIES
    def brain(self):
        chosen = rand.choice(self.state)
        if chosen == "TOWARDS_PLAYERS":
            self.move_towards_player(self.world)
        elif chosen == "RANDOM_MOVE":
            self.random_move(self.world)
        elif chosen == "OBSTACLE_AVOIDANCE":
            self.avoid_obstacles(self.world)
    
    # TDOD: FINISH
    def move_towards_player(self, world):
        player_positions = world.findPlayersPosition()
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
    
    # TODO: COMPLETE, ADD A ACTION QUEUE FOR THE ENEMY
    # MAYBE STATE QUEUE INSTEAD, NEED A WAY TO POP IT WHEN THE PLAYER HAS MOVED TO A NEW POSITION
    def avoid_obstacles(self, world):
        pass
        # enemy_x, enemy_y = self.xy

        # for 
        # if self.world.CheckTile()
    
    # Randomly move the entity in one of the possible directions
    def random_move(self, world):
        chosen = rand.choice(self.possible_actions)
        self.move(chosen)


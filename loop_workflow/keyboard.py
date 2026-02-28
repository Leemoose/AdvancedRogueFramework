import pygame

from .bindings import Bindings
from .keyboard_utility import *
from navigation_utility import pathfinding
from src.core.enums import LoopType
from logging_config import get_logger, log_high_priority
from src.core.directions import Directions
import time

logger = get_logger(__name__)

class Keyboard():
    """
    Keyboard translates any player input into either a change of gamestate or an action. Any complicated checks
    should be done in the action, not here.
    First the player input or key is translated to a keyboard input (this allows inputs to change if we want).
    Then, depending on which mode the game is in, it will do a series of if else statements to pick correct action.
    """
    def __init__(self):
        self.key_bindings = {}
        set_key_bindings(self.key_bindings)
        self.key_player_bindings = Bindings(self)
        self.key_queue = []
        self.last_action_time = pygame.time.get_ticks()
    

    def get_key_has_binding(self, key):
        return key in self.key_bindings

    def get_key_binding(self, key, shift_pressed):
        #This shift key needs to be fixed
        if shift_pressed:
            return self.get_key_after_shift(key)
        if self.get_key_has_binding(key):
            new_key = self.key_bindings[key]
            if self.key_player_bindings.has_binding(self.key_bindings[key]):
                return self.key_player_bindings.use_keybinding(new_key)
            else:
                return new_key
        return -1

    def get_key_after_shift(self, key):
        src = r"`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./"
        dest = r'~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
        if key <= 10000:
            ch = chr(key)
            if ch in src:
                ch = dest[src.index(ch) - 1]
                return ch
    
    def get_adjacent_tile_to_key(self, loop, x_tile, y_tile):
        xdiff = x_tile - loop.player.x
        ydiff = y_tile - loop.player.y
        options = {(1,1): "n",
                (1,0): "right",
                (1,-1): "u",
                (0,1): "down",
                (0,-1): "up",
                (-1,1): "b",
                (-1,0): "left",
                (-1,-1): "y"}
        return options[(xdiff, ydiff)]

    def get_has_waited_sufficiently(self):
        return time.time() - self.last_action_time > 0.1

    def set_continous_movement_keys(self, keys):
        if self.get_has_waited_sufficiently():
            if keys[pygame.K_UP] == True:
                self.set_next_key(self.get_key_binding(pygame.K_UP, False))
            elif keys[pygame.K_DOWN] == True:
                self.set_next_key(self.get_key_binding(pygame.K_DOWN, False))
            elif keys[pygame.K_LEFT] == True:
                self.set_next_key(self.get_key_binding(pygame.K_LEFT, False))
            elif keys[pygame.K_RIGHT] == True:
                self.set_next_key(self.get_key_binding(pygame.K_RIGHT, False))
            elif keys[pygame.K_TAB] == True:
                self.set_next_key(self.get_key_binding(pygame.K_TAB, False))
            elif keys[pygame.K_PERIOD] == True:
                self.set_next_key(self.get_key_binding(pygame.K_PERIOD, False))


    def move_nonadjacent(self, loop, x_tile, y_tile):
        player = loop.player
        if (not loop.generator.in_map(x_tile, y_tile)) or (not loop.generator.tile_map.get_seen(x_tile, y_tile)):
                return
        if not player.path:
            player.path = []
        #Think this could be done more simple?
        npc_ids = loop.generator.interact_map.dict
        npc_dict = {}
        
        for key in npc_ids.subjects:
            npc = npc_ids.get_subject(key)
            npc_dict[(npc.x, npc.y)] = npc

        if not (x_tile, y_tile) in npc_dict.keys():
            def target_condition(position_tuple):
                return position_tuple[0] == x_tile and position_tuple[1] == y_tile
            def end_pathing(loop):
                loop.change_loop(LoopType.action)
        else: # special targetting if npc is target, path to adjacent to npc and then interact with npc
            def target_condition(position_tuple):
                for dir in Directions.ALL_8:
                    if position_tuple[0] + dir[0] == x_tile and position_tuple[1] + dir[1] == y_tile:
                        return True
                return False
            def end_pathing(loop):
                loop.change_loop(LoopType.action)
                return self.get_adjacent_tile_to_key(loop, x_tile, y_tile) #This got changed by me, might cause bug

        player.path = pathfinding.conditional_bfs(loop.generator.tile_map.get_map(), (player.x, player.y), target_condition, loop.generator.interact_map.dict)
        loop.change_loop(LoopType.pathing)
        loop.after_pathing = end_pathing
        
    #For some reason the item is not working correctly here
    def get_key_from_mouse(self, loop, x_tile, y_tile):
        player = loop.player
        if player.get_distance(x_tile, y_tile) == 0:
            if not loop.generator.item_map.get_has_no_entity(player.x, player.y):
                return "g"
            elif loop.generator.tile_map.get_entity(player.get_x(),player.get_y()).has_trait("stairs") or loop.generator.tile_map.get_entity(player.get_x(),player.get_y()).has_trait("gateway"):
                return ">"  #Needs to be able to work with upstairs as well
        elif loop.player.get_distance(x_tile, y_tile) < 1.5:
            return self.get_adjacent_tile_to_key(loop, x_tile, y_tile)
        else:
            return self.move_nonadjacent(loop, x_tile, y_tile)


    def targetting_mouse_to_keyboard(self, loop, x_tile, y_tile):
        if loop.generator.tile_map.in_map(x_tile, y_tile):
            if x_tile != loop.targets.target_current[0] or y_tile != loop.targets.target_current[1]:
                if loop.generator.tile_map.get_passable(x_tile, y_tile):
                    loop.targets.target_current = (x_tile, y_tile)
                    loop.add_target((x_tile, y_tile))
                    loop.update_screen = True
            else:
                return "return"

    def get_has_queue(self):
        return len(self.key_queue) > 0

    def get_next_key(self):
        if self.get_has_queue():
            return self.key_queue.pop(0)
        else:
            log_high_priority(logger, "You tried to get next key in sequence but it doesn't exist")
            return None

    def set_next_key(self, key):
        self.last_action_time = time.time()
        self.key_queue.append(key)

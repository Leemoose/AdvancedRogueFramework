from logging_config import get_logger
from objects import Objects
from character_implementation import character as C, statistics, Body, Fighter, Mage
from navigation_utility import pathfinding
from loop_workflow import LoopType
from character_implementation import Inventory
from item_implementation.consumables.potions import MightPotion
from src.core.player_config import PlayerConfig
from src.core.directions import Directions
from src.core.movement import MovementValidator
# New spell system
from spell_system import give_spell

logger = get_logger(__name__)


class Player(Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1000, "Player")  # TileID.PLAYER from asset_registry.py
        logger.debug("Initializing Player at position (%d, %d)", x, y)
        self.character = C.Character(self, mana=PlayerConfig.STARTING_MANA, health=PlayerConfig.STARTING_HEALTH)
        self.mage = Mage(self)
        self.inventory = Inventory(self)
        self.body = Body(self)
        self.fighter = Fighter(self)
        self.statistics = statistics.StatTracker()
        self.traits["player"] = True

        self.level = 1
        self.max_level = PlayerConfig.MAX_LEVEL

        self.visited_stairs = []
        self.stat_points = 0
        self.stat_decisions = [0, 0, 0, 0]  # used at loop levelling to alget_entity points

        self.path = []
        self.explore_path = []
        self.quests = []
        self.quest_recieved = False

        self.character.status.invincible = PlayerConfig.DEBUG_MODE

        if PlayerConfig.DEBUG_MODE:
            # Give debug spells using the new spell system
            give_spell(self, 'burning_attack')
            give_spell(self, 'sap_vitality')
            give_spell(self, 'blink')
            self.stat_points = PlayerConfig.DEBUG_STARTING_STAT_POINTS
            self.inventory.get_item(MightPotion())
        logger.debug("Player initialization complete")

    def get_render_text(self):
        statustext = [status1.get_name() for status1 in self.character.status.get_status_effects()]
        text = ["Name: " + self.get_name() + " (level " + str(self.get_level()) + ")",
                "Health: " + str(self.get_attribute("health")) + " / " + str(self.get_attribute("max_health")),
                "Mana: " + str(self.get_attribute("mana")) + " / " + str(self.get_attribute("max_mana")),
                "Strength: " + str(self.get_attribute("strength")) + "  Dexterity: " + str(self.get_attribute("dexterity")),
                "Endurance: " + str(self.get_attribute("endurance")) + "  Intelligence: " + str(self.get_attribute("intelligence")),
                "Armor: " + str(self.get_attribute("armor")),
                "Gold: " + str(self.get_attribute("gold")),
                "Status: " + str(statustext)]
        return text

    def change_attribute(self, attribute, change):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence','endurance',"dexterity"]:
            return self.character.change_attribute(attribute, change)
        elif attribute in ['armor']:
            return self.character.attributes.change_armor(change)

    def get_inventory(self):
        return self.inventory.get_inventory()

    def get_action_cost(self, action):
        return self.character.get_action_cost(action)

    def spend_energy(self, action_type: str) -> bool:
        """
        Deduct energy for performing an action.

        Args:
            action_type: The type of action (e.g., "move", "attack", "grab")

        Returns:
            True if energy was deducted, False if action type not found
        """
        if action_type in self.character.action_costs:
            self.character.energy -= self.character.action_costs[action_type]
            return True
        return False

    def gain_experience(self, experience):
        self.character.attributes.change_experience(experience)
        self.check_for_levelup()

    def attack_move(self, move_x, move_y, loop):
        from_pos = (self.x, self.y)
        to_pos = (self.x + move_x, self.y + move_y)
        x, y = to_pos

        # Use MovementValidator to check if movement is possible
        move_result = MovementValidator.can_move_to(loop, from_pos, to_pos, self.character)

        if move_result.reason == "Cannot take action":
            self.spend_energy("move")
            loop.add_message("The player is petrified and cannot move.")
        elif move_result:
            # Valid movement
            self.move(move_x, move_y, loop)
        elif loop.generator.in_map(x, y):
            # Movement blocked but position is valid - check for combat or interaction
            if loop.generator.monster_map.get_has_entity(x, y):
                defender = loop.generator.monster_map.get_entity(x, y)
                self.attack(defender, loop)
            elif loop.generator.interact_map.get_has_entity(x, y):
                self.do_interact(loop, input_direction=(move_x, move_y))
            elif move_result.reason == "Movement restricted":
                loop.add_message("You are currently restricted!")
            else:
                loop.add_message("You cannot move there")

    def move(self, move_x, move_y, loop):
        if loop.generator.get_passable((self.get_x() + move_x, self.get_y() + move_y)) and self.character.can_move() and self.character.can_take_action():
            self.spend_energy("move")
            self.y += move_y
            self.x += move_x
            self.statistics.add_move_details()
            if loop.generator.tile_map.get_entity(self.x, self.y).has_terrain():
                loop.generator.tile_map.get_entity(self.x, self.y).apply_terrain_effects(self)
                for message in loop.generator.tile_map.get_entity(self.x, self.y).get_terrain_message():
                    loop.add_message(message)
        else:
            loop.add_message("You can't move there")

    def attack(self, defender, loop):
        if defender.has_trait("monster"):
            if self.character.can_take_action() and self.get_distance(defender.get_x(), defender.get_y()) <= self.fighter.get_range():
                self.spend_energy("attack")
                #Set target to the defender
                damage = self.fighter.do_attack(defender, loop)
                self.statistics.add_attack_details(damage)
                loop.add_message(f"The player attacked for {damage} damage", (220,20,60))
            else:
                loop.add_message("You cannot currently take actions")

    def autopath(self, loop):
        logger.debug("Beginning autopath")
        if self.character.needs_rest():
            loop.after_rest = LoopType.pathing
            loop.change_loop(LoopType.resting)
            return
        loop.after_rest = LoopType.action # in case we rested need to reset this to default

        if len(loop.generator.get_monsters_in_sight()) > 0:
                loop.add_message("A monster interrupted your exploration.")
                loop.change_loop(LoopType.action)
                return False

        if self.path:
            x, y = self.path.pop(0)
            logger.debug("Moving to (%d, %d)", x, y)
            # if (x == self.x and y == self.y):
            #     # Pathfinding messed up - pop this just in case
            #     x, y = self.path.pop(0)
            self.move(x - self.x, y - self.y, loop)
            #loop.time_passes(self.character.energy)
            #self.character.energy = 0 #need to find a way to make time pass as autoexplore happens

            # auto pickup gold
            for item in loop.generator.item_map.get_all_entities():
                if item.has_trait("gold"):
                    if self.get_distance(item.x, item.y) <= 1:
                        self.do_grab(item, loop)

            self.explore_path.append((x, y))
            loop.update_screen = True

        if not self.path:
            still_pathing = loop.after_pathing(loop) # whatever we set after_pathing to should change away from pathing LoopType if needed

        self.character.energy = 0
        #if not all_seen:
            #shadowcasting.compute_fov(loop)
            # self.autoexplore(loop)
        return True

    def autoexplore(self, loop):
        logger.debug("Beginning autoexplore")

        # auto pickup gold
        good_item_locations = []
        good_item_dict = {}
        for item in loop.generator.item_map.get_all_entities():
            if item.has_trait("gold") or item.has_trait("potion") or item.has_trait("scroll"):
                good_item_locations.append((item.x, item.y))
                good_item_dict[(item.x, item.y)] = item

        all_seen, unseen = loop.generator.get_all_seen()
        if all_seen and len(good_item_dict) == 0:
            loop.change_loop(LoopType.action)
            loop.add_message("Finished exploring this level. Press s to path to stairs")
            loop.update_screen = True
            self.path = []
            return False

        if len(self.path) <= 1:
            start = (self.x, self.y)

            # special case to make sure we don't path to gold we are standing on
            if start in good_item_locations:
                self.do_grab(good_item_dict[start], loop)
                good_item_locations.remove(start)


            # Attempt to redo autoexplore with simpler BFS
            # in-line end condition so we can use tile_map
            def autoexplore_condition(position_tuple):
                return position_tuple in good_item_locations or \
                       (loop.generator.get_passable((position_tuple[0], position_tuple[1])) and \
                        not loop.generator.tile_map.get_seen(position_tuple[0],position_tuple[1]))

            self.path = pathfinding.conditional_bfs(loop.generator.tile_map.get_map(), start, autoexplore_condition, loop.generator.interact_map.dict)
            logger.debug("The autoexplore path is %s", self.path)

            if not self.path:
                self.path = []
                loop.change_loop(LoopType.action)
                return False
            else:
                loop.after_pathing = self.autoexplore

        return True

    def find_stairs(self, loop):
        tile_map = loop.generator.tile_map
        if len(self.path) <= 1:
            start = (self.x, self.y)
            all_stairs_seen = []
            to_visit_stairs = []

            # Include down stairs
            for stairs in loop.generator.tile_map.get_stairs():
                if stairs.get_level_change() == 1 and stairs.get_seen():
                    all_stairs_seen.append(stairs.get_location())
                    if stairs.get_location() not in self.visited_stairs and stairs.get_location() != start:
                        to_visit_stairs.append(stairs.get_location())

            # Also include gateways
            for gateway in loop.generator.tile_map.get_gateway():
                if gateway.get_seen():
                    all_stairs_seen.append(gateway.get_location())
                    if gateway.get_location() not in self.visited_stairs and gateway.get_location() != start:
                        to_visit_stairs.append(gateway.get_location())

            if len(all_stairs_seen) == 0:
                loop.add_message("You have not found the stairs or a gateway yet")
                loop.change_loop(LoopType.action)
                return

            # special case to avoid trying to path to current location
            if len(all_stairs_seen) == 1:
                if all_stairs_seen[0] == start:
                    loop.add_message("You have not found a different staircase or portal yet")
                    loop.change_loop(LoopType.action)
                    return
                else:
                    # if we move away from the only seen staircase, still try to path back to it
                    to_visit_stairs = all_stairs_seen

            # if visited all stairs once, allow cycle of pathing to repeat
            if len(to_visit_stairs) == 0:
                to_visit_stairs = [self.visited_stairs[0]] # specically return to first pathed staircase to make the pathing more cyclical
                if start == to_visit_stairs[0]:
                    to_visit_stairs = [self.visited_stairs[1]] # all_stairs_seen length >= 2 and to_visit_stairs length = 0 => self.visited_stairs >= 2

                self.visited_stairs = []
                if start in all_stairs_seen:
                    self.visited_stairs.append(start)

            def stairs_condition(position_tuple):
                return position_tuple in to_visit_stairs

            self.path = pathfinding.conditional_bfs(tile_map.get_map(), start, stairs_condition, loop.generator.interact_map.dict)
            if not self.path: # checks null and empty
                self.path = []
                loop.change_loop(LoopType.action)
                return

            def after_stairs(loop):
                player = loop.player
                player.visited_stairs.append((player.x, player.y))
                loop.change_loop(LoopType.action)
            loop.after_pathing = after_stairs

    def check_for_levelup(self):
        while self.level != self.max_level and self.character.attributes.can_level_up():
            self.level += 1
            self.stat_points += 2
            self.character.level_up()

    def modify_stat_decisions(self, i, increase=True):  # 0 = strength, 1 = dexterity, 2 = endurance, 3 = intelligence
        if increase:
            if self.stat_points > sum(self.stat_decisions):
                self.stat_decisions[i] += 1
        else:
            if self.stat_decisions[i] > 0:
                self.stat_decisions[i] -= 1

    def apply_level_up(self):
        self.character.level_up_stats(self.stat_decisions[0], self.stat_decisions[1], self.stat_decisions[2],
                                      self.stat_decisions[3])
        self.stat_points -= sum(self.stat_decisions)
        self.stat_decisions = [0, 0, 0, 0]

    def smart_attack(self, loop):
        """
        1. Get all visible monsters
        2. Get monster closest to us
        3. Get monster with lowest health and attack
        """
        logger.debug("Entering smart_attack")
        attack_target = None
        distance = 1000

        tile_map = loop.generator.tile_map
        for monster in loop.generator.monster_map.get_all_entities():
            monster_x, monster_y = monster.get_location()
            if tile_map.get_entity(monster_x, monster_y).visible:
                new_distance = self.get_distance(monster_x, monster_y)
                if new_distance < distance:
                    attack_target = monster
                    distance = new_distance
                elif new_distance == distance:
                    if attack_target.character.get_health() > monster.character.get_health():
                        attack_target = monster
        if attack_target is not None:
            if distance <= 1.5:
                self.attack(attack_target, loop)
            else:
                path = pathfinding.astar(tile_map.get_map(), self.get_location(), attack_target.get_location(),
                                         loop.generator.monster_map, self)
                path.pop(0)
                x, y = path[0]
                playerx, playery = self.get_location()
                self.move(x - playerx, y - playery, loop)
        logger.debug("Exiting smart_attack, target=%s", attack_target)

    def down_stairs(self, loop):
        current_tile = loop.generator.tile_map.get_entity(self.x, self.y)

        # Check for gateway first
        if current_tile.has_trait("gateway"):
            logger.debug("Player using gateway at (%d, %d)", self.x, self.y)
            self.do_gateway(loop)
        elif current_tile.has_trait("stairs") and current_tile.get_level_change() == 1:
            logger.debug("Player going down stairs at (%d, %d)", self.x, self.y)
            self.do_stairs(loop)
        elif self.character.can_take_action():
            loop.add_message("There are no stairs or gateway here!")

    def up_stairs(self, loop):
        if (loop.generator.tile_map.get_entity(self.x, self.y).has_trait("stairs")
                and loop.generator.tile_map.get_entity(self.x, self.y).get_level_change() == -1):
            self.do_stairs(loop)
        elif self.character.can_take_action():
            loop.add_message("There are no stairs here!")

    def do_stairs(self, loop):
        self.spend_energy("move")
        if self.character.can_take_action():
            loop.change_floor()
            logger.debug("Floor changed successfully")
        else:
            loop.add_message("You can't move!")

    def do_gateway(self, loop):
        """Use a gateway to travel to another branch."""
        self.spend_energy("move")
        if self.character.can_take_action():
            loop.change_branch()
            logger.debug("Branch changed successfully via gateway")
        else:
            loop.add_message("You can't move!")

    def cast_spell(self, *args):
        self.mage.cast_spell(*args)

    def add_quest(self, quest):
        self.quests.append(quest)
        self.quest_recieved = True

    def do_grab(self, item, loop):
        if self.inventory.can_grab(item) and self.character.can_grab(item):
            self.statistics.add_item_pickup_details(item)
            # add time
            self.inventory.do_grab(item, loop)

    def do_drop(self, item, item_map):
        if self.inventory.can_drop(item) and self.character.can_drop(item):
            #add stats, time
            self.inventory.do_drop(item, item_map)
            return True
        else:
            return False

    def do_equip(self, item):
        if self.body.can_equip(item) and item.can_be_equipped(self):
            self.body.equip(item, self.character.get_attribute("Strength"))
            # self.energy -= self.action_costs["equip"]

    def do_unequip(self, item):
        if item is None:
            return
        if self.body.can_unequip(item) and item.can_be_unequipped(self):
            self.body.unequip(item)
            #self.energy -= self.action_costs["unequip"]

    def do_interact(self, loop, input_direction=None):
        if input_direction is None:
            directions = Directions.ALL_8
        else:
            directions = [input_direction]
        for x, y in directions:
            if loop.generator.interact_map.get_has_entity(x + self.get_x(), y + self.get_y()):
                loop.generator.interact_map.get_entity(x + self.x, y + self.y).interact(loop)

    def do_defend(self, attacker, loop):
        return self.fighter.do_defend()

    def get_level(self):
        return self.level

    def get_attribute(self, attribute):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence','endurance',"dexterity", "armor", "health", "mana","max_health", "max_mana"]:
            return self.character.get_attribute(attribute)




    """
    """





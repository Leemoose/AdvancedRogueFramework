from logging_config import get_logger

logger = get_logger(__name__)

class Target:
    def __init__(self, parent):
        self.parent = parent

        self.target_coordinates = (parent.player.get_x(), parent.player.get_y())
        self.target_current = parent.player

        self.origin_range_coordinates = (parent.player.get_x(), parent.player.get_y())
        self.range = None

        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None
        self.temp_cast = None
        self.quick_cast = False

        self.queued_action = None #working on this


    def set_queued_action(self, action):
        self.queued_action = action

    def get_has_queued_action(self):
        return self.queued_action is not None

    def use_queued_action(self, loop):
        if self.queued_action is not None:
            self.queued_action(self.get_target(), loop)

    def set_target(self, target):
        if target is None:
            self.target_current = self.parent.player
            self.target_coordinates = (self.parent.player.get_x(), self.parent.player.get_y())
        else:
            x, y = target
            if self.parent.generator.tile_map.in_map(x,y) and self.parent.generator.tile_map.get_visible(x,y):
                if self.parent.generator.monster_map.get_has_entity(x, y):
                    self.target_current = self.parent.generator.monster_map.get_entity(x, y)
                elif self.parent.generator.item_map.get_has_entity(x, y):
                    self.target_current = self.parent.generator.item_map.get_entity(x, y)
                else:
                    self.target_current = self.parent.generator.tile_map.get_entity(x, y)
                self.target_coordinates = target

    def set_target_range(self, origin, range):
        self.origin_range_coordinates = origin
        self.range = range

    def get_range(self):
        return self.range

    #Used for when the entity is not on the map
    def set_entity_target(self, entity):
        self.target_current = entity

    def get_target(self):
        return self.target_current

    def get_target_coordinates(self):
        return self.target_coordinates

    def get_origin_range_coordinates(self):
        return self.origin_range_coordinates

    def adjust(self, xdelta, ydelta):
        x, y = self.get_target_coordinates()
        tile_map = self.parent.generator.tile_map
        if (tile_map.get_passable(x + xdelta, y + ydelta) and tile_map.get_seen(x + xdelta,y + ydelta)
                and (self.get_range() is None or tile_map.get_distance(x + xdelta,self.origin_range_coordinates[0], y + ydelta, self.origin_range_coordinates[1]) <= self.range)):
            self.set_target((x+xdelta, y + ydelta))


    def store_skill(self, index_to_cast, skill_to_cast, caster, temp_cast = False, quick_cast=False):
        self.index_to_cast = index_to_cast
        self.skill_to_cast = skill_to_cast
        self.caster = caster
        self.temp_cast = temp_cast
        self.quick_cast = quick_cast

    def void_skill(self):
        if self.temp_cast:
            self.caster.inventory.ready_scroll = None
        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None
        self.temp_cast = False
        self.set_queued_action(None)
        self.range = None

    def cast_on_target(self, loop):
        x, y = self.target_current
        monster_map = loop.generator.monster_map
        if not loop.generator.tile_map.get_visible(x,y):
            loop.add_message("You can't see that location")
        elif monster_map.get_has_entity(x,y):
            if not self.skill_to_cast.targets_monster:
                loop.add_message("You can't cast " + self.skill_to_cast.name + " on a space with a monster")
                self.void_skill()
                return
            monster = monster_map.get_entity(x,y)
            if self.skill_to_cast.castable(monster):
                if self.temp_cast:
                    self.skill_to_cast.try_to_activate(monster, loop)
                    self.caster.inventory.ready_scroll.consume_scroll(self.caster)
                    loop.add_message("You cast " + str(self.skill_to_cast.name) + " on " + monster.name)
                    self.void_skill()
                else:
                    self.caster.cast_skill(self.index_to_cast, monster, loop, self.quick_cast)
                    loop.add_message("You cast " + str(self.skill_to_cast.name) + " on " + monster.name)
                    self.void_skill()
            else:
                loop.add_message("You can't cast " + self.skill_to_cast.name + " on " + monster.name + " right now")
                self.void_skill()
        else:
            if not self.skill_to_cast.targets_monster:
                if self.temp_cast:
                    self.skill_to_cast.try_to_activate((x, y), loop)
                    self.caster.inventory.ready_scroll.consume_scroll(self.caster)
                    loop.add_message("You cast " + str(self.skill_to_cast.name))
                    self.void_skill()
                else:
                    self.caster.cast_skill(self.index_to_cast, (x, y), loop)
                    loop.add_message("You cast " + str(self.skill_to_cast.name))
                    self.void_skill()
            else:
                loop.add_message("Not a valid target there")
        self.range = None



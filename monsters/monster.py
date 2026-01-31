"""
Base Monster class for all monsters in the game.

All specific monster types should inherit from this class and be placed
in their own submodule under the monsters package.
"""

from monster_implementation import MonsterAI, create_base_behaviors
import objects as O
from character_implementation import character as C
from character_implementation import Inventory, Body, Fighter, Mage


class Monster(O.Objects):
    """Base class for all monsters."""

    def __init__(self, x=-1, y=-1, render_tag=-1, name="Unknown monster",
                 experience_given=0, rarity="Common", health=10,
                 min_damage=2, max_damage=3, mana=0, gold=0):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.character = C.Character(self, health=health, mana=mana,
                                     experience_given=experience_given)
        self.brain = MonsterAI(self, create_base_behaviors())
        self.inventory = Inventory(self, gold=gold)
        self.body = Body(self, min_damage=min_damage, max_damage=max_damage)
        self.fighter = Fighter(self)
        self.mage = Mage(self)
        self.level = 1

        self.traits["monster"] = True
        self.skills = []
        self.rarity = rarity

        # Can be overridden by subclasses
        self.description = f"This is a {self.name}. It wants to eat you."

        # Whether this monster blocks auto-explore
        self.stops_autoexplore = True

        # Restriction for terrain (e.g., "deep water" for golems)
        self.restriction = ""

        # Day/night state for Forest branch
        self.nightified = False

    def nightify(self):
        """Make monster stronger for nighttime in Forest. Increases damage."""
        if not self.nightified:
            self.nightified = True
            # Increase unarmed damage at night
            self.body.unarmed.damage_min += 2
            self.body.unarmed.damage_max += 3

    def dayify(self):
        """Revert monster to daytime stats in Forest."""
        if self.nightified:
            self.nightified = False
            # Remove night damage bonus
            self.body.unarmed.damage_min -= 2
            self.body.unarmed.damage_max -= 3

    def get_attribute(self, attribute):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence', 'endurance', "dexterity",
                        "armor", "health", "mana", "max_health", "max_mana"]:
            return self.character.get_attribute(attribute)

    def get_render_text(self):
        text = [
            "Name: " + self.get_name() + " (level " + str(self.get_level()) + ")",
            "Health: " + str(self.get_attribute("health")) + " / " + str(self.get_attribute("max_health")),
            "Mana: " + str(self.get_attribute("mana")) + " / " + str(self.get_attribute("max_mana")),
            "Strength: " + str(self.get_attribute("strength")) + "  Dexterity: " + str(self.get_attribute("dexterity")),
            "Endurance: " + str(self.get_attribute("endurance")) + "  Intelligence: " + str(self.get_attribute("intelligence")),
            "Armor: " + str(self.get_attribute("armor")),
            "Gold: " + str(self.get_attribute("gold")),
            "Status: " + str(self.character.status.get_status_effects())
        ]
        return text

    def get_inventory(self):
        return self.inventory.get_inventory()

    def get_is_awake(self):
        return self.character.get_is_awake()

    def get_description(self):
        return self.description

    def get_level(self):
        return self.level

    def get_string_description(self):
        description = []
        description.append(self.get_name())
        description.append("Level: " + str(self.get_level()))
        description.append("Health: " + str(self.character.get_health()) + "/" + str(self.character.get_max_health()))
        effects = self.character.get_status_effects()
        status = ""
        for effect in effects:
            status += ", " + effect.description()
        description.append("Status: " + status)
        description.append("Description: " + self.get_description())
        return description

    def do_attack(self, target, loop):
        self.character.change_energy(-self.character.get_action_cost("attack"))
        return self.fighter.do_attack(target, loop)

    def do_grab(self, item, loop):
        if self.inventory.can_grab(item) and self.character.can_grab(item):
            self.inventory.do_grab(item, loop)
            return True
        else:
            return False

    def do_drop(self, item, item_map):
        if self.inventory.can_drop(item) and self.character.can_drop(item):
            self.inventory.do_drop(item, item_map)
            return True
        else:
            return False

    def do_defend(self, attacker, loop):
        return self.fighter.do_defend()

    def move(self, move_x, move_y, loop):
        monster_map = loop.generator.monster_map
        generator = loop.generator
        if not self.character.can_take_action():
            self.character.energy -= self.character.action_costs["move"]
        elif generator.get_passable((self.x + move_x, self.y + move_y)):
            self.character.energy -= self.character.action_costs["move"]
            monster_map.move_entity(self.x, self.y, self.x + move_x, self.y + move_y)
            self.set_location(self.x + move_x, self.y + move_y)

    def do_unequip(self, item):
        if item is not None and self.body.can_unequip(item) and item.can_be_unequipped(self):
            self.body.unequip(item)

    def change_attribute(self, attribute, change):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence', 'endurance', "dexterity"]:
            return self.character.change_attribute(attribute, change)
        elif attribute in ['armor']:
            return self.character.attributes.change_armor(change)

    def __str__(self):
        return self.name

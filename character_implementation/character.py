import random
from logging_config import get_logger, log_high_priority
from .attributes import Attributes
from .status import Status
from loop_workflow.looptype import LoopType

logger = get_logger(__name__)

"""
Character is the meat of
"""
class Character():
    def __init__(self, parent, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, health = 100, mana = 0, health_regen=0.2, mana_regen=0.2, invincible=False, experience_given = 0):
        self.parent = parent
        self.attributes = Attributes(self, endurance, intelligence, dexterity, strength, health, mana, health_regen, mana_regen, experience_given = experience_given)
        self.status = Status(self, invincible)
        self.energy = 0

        self.main_weapon = None


        self.action_costs = {"attack": 100,
                             "move": 100,
                             "grab": 30,
                             "equip": 100,
                             "unequip": 50,
                             "quaff": 10,
                             "read": 20,
                             "drop": 10,
                             "activate": 25
                            }

        self.skills = []
        logger.debug(f"Character initialized for {parent.name}")



    def set_action_cost(self, action, newcost):
        self.action_costs[action] = newcost

    def get_action_cost(self, action):
        return self.action_costs[action]

    def change_action_cost(self, action, change):
        self.action_costs[action] += change

    def get_all_action_costs(self):
        return self.action_costs

    def change_energy(self, energy):
        self.energy += energy

    def can_grab(self, item):
        return True #Should check if any conditions would apply (like effects)

    def can_drop(self, item):
        return True

    def is_alive(self):
        if self.attributes.get_health() <= 0 and not self.status.get_invincible():
            self.alive = False
            return False
        return True

    def take_damage(self, dealer, damage):
        if damage > 0:
            for effect in self.status.get_status_effects():
                if effect.has_trait("asleep"):
                    effect.duration = 0
        if damage < 0:
            damage = 0
        self.attributes.change_health(-damage)
        if not self.is_alive():
            #if hasattr(dealer, "experience"): # acts as a check for it its a player
            dealer.statistics.add_killed_monster(self.parent)
            dealer.gain_experience(self.attributes.get_experience_given())
            logger.debug(f"Experience given: {self.attributes.get_experience_given()}")
            logger.debug(f"Dealer experience now: {dealer.character.attributes.get_experience()}")
        return self.is_alive()


    def skill_damage_increase(self):
        return int(((self.attributes.get_intelligence()) * 1.5 ) // 2)

    def skill_duration_increase(self):
        return (self.attributes.get_intelligence() // 3)

    def wait(self):
        self.change_energy(-self.action_costs["move"])

    def level_up(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.attributes.level_up()


    def level_up_stats(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.attributes.change_endurance(endurance_up)
        self.attributes.change_intelligence(intelligence_up)
        self.attributes.change_dexterity(dexterity_up)
        self.attributes.change_strength(strength_up)


    def tick_all_status_effects(self, loop):
        status_messages = [self.parent.name + " " + mes for mes in
                           self.status.get_status_messages()]  # Still need to fix
        for message in status_messages:
            loop.add_message(message)
        self.status.tick_all_status_effects()

              #  loop.add_message(message)

    def quaff(self, potion, item_dict, item_map):
        if potion.consumeable and potion.equipment_type == "Potiorb":
            potion.activate(self.parent)
            self.change_energy(-self.action_costs["quaff"])
            return True

    def activate(self, item, loop):
        if item.consumeable:
            item.activate(self.parent)
            self.change_energy(-self.action_costs["activate"])
            return True

    def read(self, scroll, loop, item_dict, item_map):
        if scroll.consumeable and scroll.equipment_type == "Scrorb":
            scroll.activate(self.parent, loop)
            self.change_energy(-self.action_costs["read"])
            return True
        elif scroll.equipment_type == "Book":
            scroll.activate(self.parent, loop)
            self.change_energy(-self.action_costs["read"])


    def tick_cooldowns(self):
        if self.parent.has_trait("monster"):
            for skill in self.skills: # monsters still use skill system instead of spells
                skill.tick_cooldown()
        else:
            for skill in self.player.known_spells: # players use spell system
                skill.tick_cooldown()

    def cast_skill(self, skill_num, target, loop, quick_cast=False):
        self.parent.mage.cast_spell(skill_num, target, loop, quick_cast)

    # should be outdated and unused with updated spell system
    # def cast_skill_by_name(self, skill_name, target, loop):
    #     for skill in self.skills:
    #         if skill.name == skill_name:
    #             self.energy -= skill.action_cost
    #             return skill.try_to_activate(target, loop)
    #     return False

    def tick_regen(self):
        self.attributes.change_health(self.attributes.get_health_regen())
        self.attributes.change_mana(self.attributes.get_mana_regen())

    def needs_rest(self):
        # skills_ready = True
        for skill in self.parent.mage.known_spells:
            if skill.ready != 0:
                return True
        return self.attributes.get_health() < self.attributes.get_max_health() or self.attributes.get_mana() < self.attributes.get_max_mana()


    def rest(self, loop, returnLoop):
        logger.debug(f"{self.parent.name} begins to rest")
        if not self.status.get_safe_rest():
            loop.add_message("Your ring is draining your health, it is not safe to rest now.")
            loop.change_loop(LoopType.action)
        elif not self.needs_rest(): # and returnLoop == L.LoopType.action: <- Don't think we need this?
            loop.add_message("No point in resting right now.")
            loop.change_loop(returnLoop)
        else:
            tile_map = loop.generator.tile_map
            no_monster_active = True
            for monster in loop.generator.monster_map.get_all_entities():
                if monster.get_is_awake():
                    no_monster_active = False
                    break
            if no_monster_active: # if you've rested peacefully for 50 turns, your probably not getting hunted, if we dont put this check, rest sometimes seems laggy
                # can freely rest to full health
                if self.needs_rest():
                    self.attributes.change_health(self.attributes.get_max_health())
                    self.attributes.change_mana(self.attributes.get_max_mana())

                for skill in loop.player.mage.known_spells:
                    skill.ready = 0
                for effect in self.status.get_status_effects():
                    if effect.duration > 0: # remove any non-permanent effects
                        self.status.remove_status_effect(effect)
                loop.add_message("You rest for a while")
                loop.change_loop(returnLoop)
                logger.debug(f"{self.parent.name} rested successfully")
            else:
                loop.add_message("You cannot rest while enemies are nearby.")
                loop.change_loop(LoopType.action)
                logger.debug(f"{self.parent.name} cannot rest - enemies nearby")
                # for monster in loop.generator.monster_map.get_all_entities():
                #     monster_loc = monster.get_location()
                #     if tile_map.get_entity(monster_loc[0],monster_loc[1]).get_visible():
                #         loop.add_message("You cannot rest while enemies are nearby.")
                #         loop.change_loop("action")
                #         return


    def add_skill(self, new_skill):
        for skill in self.parent.mage.known_spells:
            if skill.name == new_skill.name:
                logger.debug(f"Skill {new_skill.name} already known, not adding")
                return
        self.parent.mage.add_spell(new_skill)
        logger.debug(f"Added skill {new_skill.name}")

    def remove_skill(self, skill_name):
        for skill in self.parent.mage.known_spells:
            if skill.name == skill_name:
                self.parent.mage.known_spells.remove(skill)
                if skill in self.parent.mage.quick_cast_spells:
                    idx = self.parent.mage.quick_cast_spells.index(skill)
                    self.parent.mage.quick_cast_spells[idx] = None
                logger.debug(f"Removed skill {skill_name}")
                break




    """
    This section is for pass along calls for attributes, make any changes in the child function, not here
    """
    def get_health(self):
        return self.attributes.get_health()

    def get_max_health(self):
        return self.attributes.get_max_health()

    def get_mana(self):
        return self.attributes.get_mana()

    def get_max_mana(self):
        return self.attributes.get_max_mana()

    def get_attribute(self, attribute):
        attribute = attribute.lower()
        if attribute == "strength":
            return self.attributes.get_strength()
        elif attribute == "intelligence":
            return self.attributes.get_intelligence()
        elif attribute == "endurance":
            return self.attributes.get_endurance()
        elif attribute == "dexterity":
            return self.attributes.get_dexterity()
        elif attribute == "armor":
            return self.attributes.get_armor()
        elif attribute == "health":
            return self.attributes.get_health()
        elif attribute == "max_health":
            return self.attributes.get_max_health()
        elif attribute == "mana":
            return self.attributes.get_mana()
        elif attribute == "max_mana":
            return self.attributes.get_max_mana()

    def get_experience(self):
        return self.attributes.get_experience()

    def change_attribute(self, attribute, change):
        attribute = attribute.lower()
        if attribute == "strength":
            self.attributes.change_strength(change)
        elif attribute == "intelligence":
            self.attributes.change_intelligence(change)
        elif attribute == "endurance":
            self.attributes.change_endurance(change)
        elif attribute == "dexterity":
            self.attributes.change_dexterity(change)
        else:
            log_high_priority(logger, "You tried to change an attribute '%s' but it doesn't exist", attribute)

    def change_strength(self, change):
        self.attributes.change_strength(change)

    def change_health(self, change):
        self.attributes.change_health(change)

    def change_max_health(self, change):
        self.attributes.change_max_health(change)

    def change_mana(self, change):
        self.attributes.change_mana(change)

    def get_strength(self):
        return self.attributes.get_strength()

    def get_intelligence(self):
        return self.attributes.get_intelligence()

    def get_endurance(self):
        return self.attributes.get_endurance()

    def get_dexterity(self):
        return self.attributes.get_dexterity()

    """
    This section is for pass along calls for status effects, make any changes in the child function, not here
    """

    def get_status_effects(self):
        return self.status.get_status_effects()

    def can_take_action(self):
        return self.status.can_take_actions

    def can_move(self):
        return self.status.can_move and self.status.can_take_actions

    def get_is_awake(self):
        return self.status.get_is_awake()

    def get_flee(self):
        return self.status.get_flee()

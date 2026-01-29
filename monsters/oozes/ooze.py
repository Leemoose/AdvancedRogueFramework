from monsters.monster import Monster
from monster_implementation import MonsterAI, create_ooze_behaviors
import random

"""
Oozes are slow moving monsters that will destroy any item they touch. Sometimes they destroy the attackers weapon.
"""

class Ooze(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1000, name="Ooze"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=5, health=5, gold=0)
        self.brain = MonsterAI(self, create_ooze_behaviors())
        self.description = "These amorphous blobs of translucent, gelatinous matter emerge from the depths of the rifts. Their bodies pulse with a sickly green glow, fueled by the chaotic energies of their environment. Rift Slimes mindlessly dissolve anything they touch with acidic secretions, leaving behind only a faint, acrid odor. They show no preference or intelligence, simply drawn to any item_implementation they encounter, which they swiftly corrode beyond recognition.."
        self.character.action_costs["grab"] = 0
        self.character.action_costs["move"] = 300
        self.traits["oozes"] = True

    def do_defend(self, attacker, loop):
        chance_to_destroy_weapon = random.randint(1, 100)
        if chance_to_destroy_weapon <= 5:
            weapon = attacker.body.get_weapon()
            if weapon.get_can_be_destroyed() and weapon.get_range() <= 1.5:
                weapon.set_destroy(True)
                attacker.body.unequip(weapon)
                attacker.inventory.remove_item(weapon)
                loop.add_message("The oozes destroys the weapon of the attacker!")
            else:
                attacker.character.take_damage(self, 1)
        return self.fighter.do_defend()

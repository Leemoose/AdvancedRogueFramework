"""
WEAPONS
"""
from item_implementation.equipment import Equipment
# from skills import MagicMissile
import random

class Weapon(Equipment):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name="Unknown weapon", damage_min=0, damage_max=0,
                 armor_piercing=0, attack_cost=80, range = 1.5):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name)
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.armor_piercing = armor_piercing
        self.equipment_type = "Weapon"
        self.slots_taken = 1
        self.on_hit = []
        self.on_damage = []
        self.effective = []
        self.attack_cost = attack_cost
        self.diff_action_cost = 0
        self.range = range
        self.traits["weapon"] = True
        self.slot = "hand_slot"

    def can_be_equipped(self, entity):
        return super().can_be_equipped(entity)

    def get_armor_piercing(self):
        return self.armor_piercing

    def get_damage_min(self):
        return self.damage_min

    def get_damage_max(self):
        return self.damage_max

    def get_range(self):
        return self.range

    def get_damage(self):
        damage = random.randint(self.damage_min, self.damage_max)
        return damage

    def get_on_hit_effect(self):
        return self.on_hit
    def get_has_on_hit_effect(self):
        return len(self.on_hit) > 0

    def get_on_damage_effect(self):
        return self.on_damage

    def get_has_on_damage_effect(self):
        return len(self.on_damage) > 0

    def add_on_damage_effect(self, effect):
        self.on_damage.append(effect)






#
# class MagicWand(Weapon):
#     def __init__(self, render_tag):
#         super().__init__(-1, -1, 0, render_tag, "Magic Wand")
#         self.melee = True
#         self.name = "Magic Wand"
#         self.description = "A wand that you can use to cast magic missile. You can also use it in melee but why would you?"
#         self.damage_min = 1
#         self.damage_max = 5
#         self.magic_missile_damage = 6
#         self.magic_missile_range = 6
#         self.magic_missile_cost = 10
#         self.magic_missile_cooldown = 3
#         self.attached_skill_exists = True
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Common"
#
#         self.attached_skill_exists = True
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return MagicMissile(owner, self.magic_missile_cooldown,
#                               self.magic_missile_cost,
#                               self.magic_missile_damage,
#                               self.magic_missile_range,
#                               action_cost=100)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted cast a stronger magic missile"
#         if self.level == 6:
#             self.description = "A wand that you can use to cast an immensely powerful magic missile. It's been enchanted as much as possible."
#
#         # level up improves magic missile
#         self.magic_missile_damage += 2
#         self.magic_missile_range += 1
#         self.magic_missile_cooldown -= 1
#         if self.magic_missile_cooldown < 0:
#             self.magic_missile_cooldown = 0
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#



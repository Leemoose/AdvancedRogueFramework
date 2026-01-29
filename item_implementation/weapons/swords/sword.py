from item_implementation.weapons.weapons import Weapon


"""
SWORDS
 + Specialness lies with armor piercing
 * Average damage
 * Average attack speed
"""


class Sword(Weapon):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=4800, name="Sword", damage_min=2, damage_max=3,
                 armor_piercing=2, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.melee = True
        self.description = "Could be rounder honestly."

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more damaging."
        if self.level == 6:
            self.description = "A sword that has been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 2


#
# class LongSword(Sword):
#     def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Longsword", damage_min=4, damage_max=12,
#                  armor_piercing=8, attack_cost=80):
#         super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
#                          damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
#         self.required_strength = 3
#
#
# class Claymore(Sword):
#     def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Claymore", damage_min=8, damage_max=20,
#                  armor_piercing=8, attack_cost=80):
#         super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
#                          damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
#         self.required_strength = 5
#
#
# class TwoHandedSword(Sword):
#     def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Two Handed Sword", damage_min=4, damage_max=12,
#                  armor_piercing=10, attack_cost=80):
#         super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
#                          damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
#         self.slots_taken = 2
#         self.required_strength = 5
#
#
# class GreatSword(TwoHandedSword):
#     def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Greatsword", damage_min=8, damage_max=20,
#                  armor_piercing=15, attack_cost=80):
#         super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
#                          damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
#         self.required_strength = 8
#
#
# ################################################
# class SleepingSword(Sword):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.melee = True
#         self.name = "Sleeping Sword"
#         self.description = "...on the treetops. When the wind blows"
#         self.can_be_levelled = False
#
#         self.on_hit = (lambda inflictor: Asleep(8))
#         self.change_to_hit = 25
#         self.on_hit_description = f"The target is sleeping."
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Legendary"
#
#     def attack(self):
#         hit = random.randint(1, 100)
#         if hit < self.change_to_hit:
#             return (super().attack(), self.on_hit)
#         else:
#             return (super().attack(), None)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " the cradle will rock."
#         if self.level == 6:
#             self.description = "Death is the greatest sleep of all."
#             self.damage_min = 1
#             self.damage_max = 100
#         self.damage_min += 2
#         self.damage_max += 3
#         if self.damage_min > self.damage_max:
#             self.damage_min = self.damage_max
#
#
# class FlamingSword(Weapon):
#     def __init__(self, render_tag):
#         super().__init__(-1, -1, 0, render_tag, "Flaming Sword")
#         self.melee = True
#         self.name = "Flaming Sword"
#         self.description = "A sword that is on fire. You can channel its fire to cast a Burning Attack at a distant foe. "
#         self.damage_min = 5
#         self.damage_max = 8
#
#         self.on_hit_burn = 4
#         self.on_hit_burn_duration = 3
#         self.on_hit = (lambda inflictor: Burn(self.on_hit_burn, self.on_hit_burn_duration, inflictor))
#         self.on_hit_description = f"Burns the target for {self.on_hit_burn} damage over {self.on_hit_burn_duration} turns."
#
#         self.skill_cooldown = 8
#         self.skill_cost = 20
#         self.skill_damage = 3
#         self.skill_burn_damage = 4
#         self.skill_burn_duration = 3
#         self.skill_range = 4
#         self.attached_skill_exists = True
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Legendary"
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.BurningAttack(owner, self.skill_cooldown,
#                                self.skill_cost,
#                                self.skill_damage,
#                                self.skill_burn_damage,
#                                self.skill_burn_duration,
#                                self.skill_range)
#
#     def attack(self):
#         return (super().attack(), self.on_hit)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to hit harder and burn stronger."
#         if self.level == 6:
#             self.description = "A sword that burns intensely. It's burning strike has reached its maximum potency. It's been enchanted as much as possible."
#         self.damage_min += 2
#         self.damage_max += 3
#
#         self.skill_damage += 2
#         self.skill_cooldown -= 1
#         if self.skill_cooldown < 5:
#             self.skill_cooldown = 5
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#

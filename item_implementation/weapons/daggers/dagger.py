from item_implementation.weapons.weapons import Weapon

""""
DAGGERS
+ Specialize in fast attack speed (works well with on hit effects and attack move combinations).
- Low damage (does poorly against armor)
- No armor piercing
"""


class Dagger(Weapon):
    def __init__(self, render_tag=321, attack_cost=20):
        super().__init__(-1, -1, 0, render_tag, name = "Basic dagger", attack_cost= attack_cost, damage_min=1, damage_max=3)
        self.description = "I swear that tip is getting rounder... Larry!. Enchanting it might make it more pointy and precise."

    def activate(self, entity):
        self.wearer = entity
        self.diff_action_cost = max(entity.get_action_cost("attack") - self.attack_cost,
                                    (entity.get_action_cost("attack")) / 2)
        entity.character.change_action_cost("attack", entity.get_action_cost("attack") - self.diff_action_cost)

    def deactivate(self, entity):
        self.wearer = None
        entity.character.change_action_cost("attack", entity.get_action_cost("attack") + self.diff_action_cost)
        self.diff_action_cost = 0

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more precise."
        if self.level == 6:
            self.description = "A dagger that always strikes accurately, never dealing less than full damage. It's been enchanted as much as possible."
        self.damage_min += 0
        self.damage_max += 5
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max

#
# class ScreamingDagger(Dagger):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.melee = True
#         self.name = "Screaming Dagger"
#         self.description = "The sound of thousands dead souls. "
#         self.damage_min = 1
#         self.damage_max = 1
#         self.can_be_levelled = False
#
#         self.on_hit = (lambda inflictor: Tormented(5))
#         self.on_hit_description = f"Torments the target for half health damage over."
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Legendary"
#
#     def attack(self):
#         return (super().attack(), self.on_hit)
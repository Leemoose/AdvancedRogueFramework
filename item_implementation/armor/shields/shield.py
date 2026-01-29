from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class Shield(Armor):
    def __init__(self, x=-1, y=-1, render_tag=3400, name="Shield"):
        super().__init__(x=x, y=y, id_tag=0, render_tag=render_tag, name=name)
        self.equipment_type = "Shield"
        self.name = name
        self.offhand = True
        self.slot = "hand_slot"
        self.traits["shield"] = True
        self.description = "A shield that you can use to block things."


#
# class BasicShield(Shield):
#     def __init__(self, x=-1, y=-1, render_tag=311):
#         super().__init__(x=x, y=y, render_tag=render_tag, name="Basic Shield")
#         self.armor = 3
#         self.description = "A shield that you can use to block things."
#         self.stats = statUpgrades(base_end=1, max_end=3, base_arm=1, max_arm=6)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to be more protective."
#         if self.level == 6:
#             self.description = "A shield that you can use to block nearly anything. It's been enchanted as much as possible."
#
#
# class Aegis(Shield):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Aegis")
#         self.description = "A shield with the face of a horrifying monster on it. It can turn your enemies to stone"
#         self.required_strength = 2
#
#         self.skill_cooldown = 12
#         self.skill_cost = 20
#         self.skill_duration = 3
#         self.skill_activation_chance = 0.3
#         self.skill_range = 3
#
#         self.attached_skill_exists = True
#
#         self.rarity = "Legendary"
#         self.stats = statUpgrades(base_str=1, max_str=2, base_end=2, max_end=3, base_arm=2, max_arm=7)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Petrify(owner, self.skill_cooldown,
#                          self.skill_cost,
#                          self.skill_duration,
#                          self.skill_activation_chance,
#                          self.skill_range)
#
#     def level_up(self):
#         self.enchant()
#
#         self.skill_activation_chance += 0.2
#         if self.skill_activation_chance > 1.0:
#             self.skill_activation_chance = 1.0
#
#         self.skill_range += 1
#         if self.skill_range > 6:
#             self.skill_range = 6
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#
#         if self.level == 2:
#             self.description += " It's been enchanted to be even uglier."
#         if self.level == 6:
#             self.description = "A shield with the face of a horrifying monster on it. It can turn your enemies to stone for longer. It's been enchanted as much as possible."
#
#
# class TowerShield(Shield):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Tower Shield")
#         self.description = "A massive shield that can block nearly anything but is unwieldy to use"
#         self.required_strength = 3
#         self.stats = statUpgrades(base_str=1, max_str=2, base_dex=-2, max_dex=0, base_end=2, max_end=4, base_arm=5,
#                                   max_arm=10)
#
#     def level_up(self):
#         self.enchant()
#         # if self.wearer != None:
#         #     self.wearer.dexterity += 1
#         if self.level == 2:
#             self.description += " It's been enchanted to be less unwieldy."
#         if self.level == 6:
#             self.description = "A massive shield that can block nearly anything. It's been enchanted as much as possible."
#
#
# class MagicFocus(Shield):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Magic Focus")
#         self.armor = 0
#         self.description = "An orb that takes your offhand but lets you cast even more powerful spells."
#         self.intelligence_buff = 6
#
#         self.rarity = "Rare"
#         self.stats = statUpgrades(base_int=2, max_int=6)
#
#     def level_up(self):
#         self.enchant()
#
#         if self.level == 2:
#             self.description += " It's been enchanted to be more effective."
#         if self.level == 6:
#             self.description = "An orb that takes your offhand but lets you cast the most powerful spells. It's been enchanted as much as possible."

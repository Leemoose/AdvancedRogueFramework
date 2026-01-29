"""
BOOTS
"""
from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class Boots(Armor):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Boots")
        self.equipment_type = "Boots"
        self.name = "Boots"
        self.description = "Boots that are incredibly comfortable but only offer a little protection"
        self.stats = statUpgrades(base_dex=1, max_dex=2, base_arm=1, max_arm=4)
        self.slot = "boots_slot"
        self.traits["boots"] = True

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Boots that are somehow incredibly comfy and tough at the same time. It's been enchanted as much as possible."

#
# class BlackenedBoots(Boots):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Boots"
#         self.name = "Blackened Boots"
#         self.cursed = True
#         self.description = "A dark spirit dwells in these boots."
#         self.rarity = "Legendary"
#         self.stats = statUpgrades(base_str=-2, max_str=1,
#                                   base_dex=4, max_dex=7,
#                                   base_int=-2, max_int=1,
#                                   base_end=-2, max_end=0,
#                                   base_arm=1, max_arm=4)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " You see the quickest path in a sea of blood."
#         if self.level == 6:
#             self.description = "You ride on screaming winds."
#
#
# class BootsOfEscape(Boots):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Boots"
#         self.name = "Boots of Escape"
#         self.armor = 0
#         self.description = "Boots that let you cast the skill flee"
#
#         self.skill_cooldown = 40
#         self.skill_cost = 25
#         self.dex_buff = 10
#         self.str_debuff = 5
#         self.int_debuff = 5
#         self.duration = 4
#         self.rarity = "Rare"
#
#         self.attached_skill_exists = True
#         self.stats = statUpgrades(base_dex=3, max_dex=8,
#                                   base_arm=1, max_arm=3)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Escape(owner, self.skill_cooldown,
#                         self.skill_cost,
#                         self_fear=False,
#                         dex_buff=self.dex_buff,
#                         str_debuff=self.str_debuff,
#                         int_debuff=self.int_debuff,
#                         haste_duration=self.duration,
#                         activation_threshold=1.1,
#                         action_cost=1)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to let you flee on a shorter cooldown."
#         if self.level == 6:
#             self.description = "Boots that let you flee at the drop of a hat. It's been enchanted as much as possible."
#         self.skill_cooldown -= 5
#         if self.skill_cooldown < 5:
#             self.skill_cooldown = 5
#         self.skill_cost -= 2
#         if self.skill_cost < 10:
#             self.skill_cost = 10
#         self.duration += 1
#         if self.duration > 6:
#             self.duration = 6
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#
#
# class AssassinBoots(Boots):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Boots"
#         self.name = "Assassin Boots"
#         self.description = "Boots to help you move in the shadows."
#         self.rarity = "Rare"
#         self.stats = statUpgrades(base_dex=2, max_dex=5,
#                                   base_str=-2, max_str=0,
#                                   base_int=1, max_int=3,
#                                   base_end=-2, max_end=0,
#                                   base_arm=1, max_arm=3)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to make you feel more nimble."
#         if self.level == 6:
#             self.description = "Boots to help you move in the shadows. It's been enchanted as much as possible."

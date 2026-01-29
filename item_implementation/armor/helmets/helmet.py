"""
HELMETS
"""
from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class Helmet(Armor):
    def __init__(self, render_tag= 3200, name="Helmet"):
        super().__init__(-1, -1, 0, render_tag, name = name)
        self.equipment_type = "Helmet"
        self.description = "A helmet that protects your head. You like how round it is."
        self.attached_skill_exists = False
        self.attached_skill = None
        self.stats = statUpgrades(base_str=0, max_str=2,
                                  base_end=1, max_end=1,
                                  base_arm=1, max_arm=3)
        self.slot = "helmet_slot"
        self.traits["helmet"] = True

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A round helmet that protects your head from nearly anything. It's been enchanted as much as possible."

#
# class VikingHelmet(Helmet):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Viking Helmet")
#         self.equipment_type = "Helmet"
#         self.name = "Viking Helmet"
#         self.description = "A helmet that lets you go berserk below a quarter health."
#
#         self.skill_cooldown = 0
#         self.skill_cost = 0
#         self.skill_duration = 10
#         self.skill_threshold = 0.25
#         self.strength_increase = 5
#
#         self.rarity = "Legendary"
#         self.str_buff = 3
#
#         self.attached_skill_exists = True
#         self.stats = statUpgrades(base_str=3, max_str=6,
#                                   base_dex=1, max_dex=3,
#                                   base_int=-1, max_int=-3,
#                                   base_end=-1, max_end=-3,
#                                   base_arm=1, max_arm=3)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Berserk(owner, self.skill_cooldown, self.skill_cost, self.skill_duration, self.skill_threshold,
#                          self.strength_increase, action_cost=1)
#
#     def level_up(self):
#         self.enchant()
#         if self.description == 2:
#             self.description += " It's been enchanted to lower the damage you need to take before going berserk"
#         if self.level == 6:
#             self.description = "A helmet that lets you go berserk below three quarters. It's been enchanted as much as possible"
#         self.skill_threshold += 0.2
#         if self.skill_threshold > 0.75:
#             self.skill_threshold = 0.75
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#
#
# class SpartanHelmet(Helmet):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Spartan Helmet")
#         self.equipment_type = "Helmet"
#         self.name = "Spartan Helmet"
#         self.description = "A helmet for a mighty warrior who doesn't need things like magic to help him"
#
#         self.required_strength = 2
#
#         self.str_buff = 2
#         self.end_buff = 4
#         self.int_debuff = 5
#
#         self.rarity = "Rare"
#         self.stats = statUpgrades(base_str=1, max_str=3,
#                                   base_int=-5, max_int=0,
#                                   base_end=3, max_end=4,
#                                   base_arm=1, max_arm=3)
#
#     def level_up(self):
#         self.enchant()
#
#         if self.level == 2:
#             self.description += " It's been enchanted to make you even tougher"
#         if self.level == 6:
#             self.description = "A helmet for the greatest of warriors who shuns magic. It's been enchanted as much as possible."
#
#
# class GreatHelm(Helmet):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Great Helm")
#         self.equipment_type = "Helmet"
#         self.name = "Great Helm"
#         self.armor = 4
#         self.required_strength = 3
#         self.description = "A helmet that fully covers your face for maximum protection although it restricts your movement a bit."
#         self.dex_debuff = 4
#
#         self.rarity = "Rare"
#
#         self.stats = statUpgrades(base_dex=-4, max_dex=0,
#                                   base_arm=4, max_arm=8)
#
#     def level_up(self):
#         self.enchant()
#
#         if self.level == 2:
#             self.description += " It's been enchanted to be less restrictive."
#         if self.level == 6:
#             self.description = "A helmet that fully covers your face for maximum protection without restricting you at all. It's been enchanted as much as possible."
#
#
# class ThiefHood(Helmet):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Thief Hood")
#         self.equipment_type = "Helmet"
#         self.name = "Thief Hood"
#         self.description = "A hood that helps you move faster and think more cleverly."
#
#         self.dex_buff = 3
#         self.int_buff = 2
#
#         self.rarity = "Rare"
#
#         self.stats = statUpgrades(base_dex=3, max_dex=5,
#                                   base_int=1, max_int=4)
#
#     def level_up(self):
#         self.enchant()
#
#         if self.level == 2:
#             self.description += " It's been enchanted to be more effective."
#         if self.level == 6:
#             self.description = "A hood that gives you the physical and mental speed of a master thief. It's been enchanted as much as possible."
#
#
# class WizardHat(Helmet):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Wizard Hat")
#         self.equipment_type = "Helmet"
#         self.name = "Wizard Hat"
#         self.description = "A hat that makes you feel more magical."
#         self.mana_buff = 20
#
#         self.rarity = "Rare"
#
#         self.stats = statUpgrades(base_int=3, max_int=6)
#
#     def activate(self, entity):
#         entity.character.max_mana += self.mana_buff
#
#     def deactivate(self, entity):
#         entity.character.max_mana -= self.mana_buff
#         if entity.mana >= entity.character.max_mana:
#             entity.mana = entity.character.max_mana
#
#     def level_up(self):
#         self.enchant()
#         self.mana_buff += 10
#
#         if self.wearer != None:
#             self.wearer.max_mana += self.mana_buff
#
#         if self.level == 2:
#             self.description += " It's been enchanted to be more effective."
#         if self.level == 6:
#             self.description = "A hat that makes you feel like you can cast spells for all eternity. It's been enchanted as much as possible."

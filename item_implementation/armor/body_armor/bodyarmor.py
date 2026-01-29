"""
BODY ARMORS
"""
from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class BodyArmor(Armor):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Body Armor"
        self.name = name
        self.description = "A piece of armor that covers your chest."
        self.stats = statUpgrades(base_str=1, max_str=1, base_end=1, max_end=4, base_arm=1, max_arm=4)
        self.slot = "body_armor_slot"
        self.traits["body_armor"] = True
#
# class Chestarmor(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Chest Plate")
#         self.description = "A reliable piece of armor that covers your chest."
#         self.required_strength = 3
#         self.wearer = None
#         self.stats = statUpgrades(base_int=-2, max_int=0, base_arm=2, max_arm=8)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to be more protective."
#         if self.level == 6:
#             self.description = "A chest plate that absorbs most hits for you. It's been enchanted as much as possible."
#
#
# class GildedArmor(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Gilded Armor")
#         self.description = "A piece of golden armor studded with gems. Just wearing it makes you feel like you can ignore trivial things like status effects."
#         self.required_strength = 1
#
#         self.skill_cooldown = 5
#         self.skill_cost = 15
#         self.activation_chance = 0.5
#
#         self.attached_skill_exists = True
#
#         self.rarity = "Rare"
#
#         self.stats = statUpgrades(base_str=1, max_str=3,
#                                   base_dex=1, max_dex=1,
#                                   base_int=1, max_int=3,
#                                   base_end=1, max_end=1,
#                                   base_arm=1, max_arm=3)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.ShrugOff(owner, self.skill_cooldown, self.skill_cost, self.activation_chance, action_cost=100)
#
#     def level_up(self):
#         self.enchant()
#
#         self.skill_cooldown -= 1
#         if self.skill_cooldown < 3:
#             self.skill_cooldown = 3
#         self.skill_cost -= 2
#         if self.skill_cost < 8:
#             self.skill_cost = 8
#         self.activation_chance += 0.1
#         if self.activation_chance > 1.0:
#             self.activation_chance = 1.0
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#
#         if self.level == 2:
#             self.description += " It's been enchanted to make you feel more invincible."
#         if self.level == 6:
#             self.description = "A work of art covered in gold and studded in gemstones. Let's you always ignore a status condition. It's been enchanted as much as possible."
#
#
# class WarlordArmor(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Warlord Armor")
#         self.description = "Frightening armor that belonged to a famous warrior. Wearing it makes you stronger and your enemies more terrified."
#         self.armor = 3
#         self.required_strength = 1
#         self.strength_buff = 2
#
#         self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
#
#         self.skill_cooldown = 12
#         self.skill_cost = 10
#         self.skill_duration = 3
#         self.skill_activation_chance = 0.5
#         self.skill_range = 2
#
#         self.attached_skill_exists = True
#
#         self.rarity = "Legendary"
#
#         self.stats = statUpgrades(base_str=2, max_str=5,
#                                   base_dex=-3, max_dex=-1,
#                                   base_end=1, max_end=4,
#                                   base_arm=2, max_arm=5)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Terrify(owner, self.skill_cooldown,
#                          self.skill_cost,
#                          self.skill_duration,
#                          self.skill_activation_chance,
#                          self.skill_range)
#
#     def activate(self, entity):
#         self.wearer = entity
#         return super().activate(entity)
#
#     def deactivate(self, entity):
#         self.wearer = None
#         return super().deactivate(entity)
#
#     def level_up(self):
#         self.enchant()
#
#         self.skill_activation_chance += 0.1
#         if self.skill_activation_chance > 1.0:
#             self.skill_activation_chance = 1.0
#         self.skill_range += 1
#         if self.skill_range > 5:
#             self.skill_range = 5
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#
#         if self.level == 2:
#             self.description += " It's been enchanted to make you more strong and frightening"
#         if self.level == 6:
#             self.description = "Frightening armor that marks you as a famous warrior who fought in many battles. Your enemies are terrified even from a distance. It's been enchanted as much as possible."
#
#
# class BloodstainedArmor(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Bloodstained Armor")
#         self.description = "A maligment aura surronds this armor."
#         self.required_strength = 3
#         self.cursed = True
#         self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
#         self.rarity = "Legendary"
#         self.stats = statUpgrades(base_str=2, max_str=6,
#                                   base_dex=-2, max_dex=0,
#                                   base_end=1, max_end=4,
#                                   base_arm=2, max_arm=5)
#
#     def activate(self, entity):
#         self.wearer = entity
#         return super().activate(entity)
#
#     def deactivate(self, entity):
#         self.wearer = None
#         return super().deactivate(entity)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been enchanted to make its aura stronger"
#         if self.level == 6:
#             self.description = "An immensely menacing aura surround you and this armor bounds to your soul. It's been enchanted as much as possible."
#
#
# class WizardRobe(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Wizard Robe")
#         self.description = "A robe that makes you feel like you can cast spells all day long."
#         self.armor = 1
#         self.mana_buff = 20
#         self.mana_regen_buff = 3
#         self.intelligence_buff = 5
#
#         self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
#
#         self.rarity = "Rare"
#         self.stats = statUpgrades(base_str=-2, max_str=0,
#                                   base_int=2, max_int=5)
#
#     def activate(self, entity):
#         entity.character.max_mana += self.mana_buff
#         entity.character.mana_regen += self.mana_regen_buff
#         return super().activate(entity)
#
#     def deactivate(self, entity):
#         entity.character.max_mana -= self.mana_buff
#         entity.character.mana_regen -= self.mana_regen_buff
#         return super().deactivate(entity)
#
#     def level_up(self):
#         self.enchant()
#         self.mana_buff += 10
#         self.mana_regen_buff += 5
#
#         if self.wearer != None:
#             self.wearer.max_mana += 10
#             self.wearer.mana_regen += 5
#
#         if self.level == 2:
#             self.description += " It's been enchanted to make you more magical"
#         if self.level == 6:
#             self.description = "A robe that makes you feel like you can cast spells for all eternity. It's been enchanted as much as possible."
#
#
# class KarateGi(BodyArmor):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Karate Gi")
#         self.description = "A gi that makes your unarmed combat stronger."
#         self.damage_boost_min = 2
#         self.damage_boost_max = 4
#
#         self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
#
#         self.rarity = "Rare"
#
#         self.stats = statUpgrades(base_str=1, max_str=1,
#                                   base_dex=3, max_dex=6,
#                                   base_int=0, max_int=0,
#                                   base_end=2, max_end=6,
#                                   base_arm=1, max_arm=3)
#
#     def activate(self, entity):
#         entity.character.unarmed_damage_min += self.damage_boost_min
#         entity.character.unarmed_damage_max += self.damage_boost_max
#         return super().activate(entity)
#
#     def deactivate(self, entity):
#         entity.character.unarmed_damage_min -= self.damage_boost_min
#         entity.character.unarmed_damage_max -= self.damage_boost_max
#         return super().deactivate(entity)
#
#     def level_up(self):
#         self.enchant()
#         self.damage_boost_min += 1
#         self.damage_boost_max += 1
#         if self.wearer != None:
#             self.wearer.unarmed_damage_min += 1
#             self.wearer.unarmed_damage_max += 1
#         if self.level == 2:
#             self.description += " It's been enchanted to make your fists stronger"
#         if self.level == 6:
#             self.description = "A gi that lets you punch through anything. It's been enchanted as much as possible."
#

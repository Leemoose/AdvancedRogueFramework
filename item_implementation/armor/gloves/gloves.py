from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class Gloves(Armor):
    def __init__(self, render_tag = 3100):
        super().__init__(-1,-1, 0, render_tag = render_tag, name = "Gloves")
        self.equipment_type = "Gloves"
        self.description = "Gloves to keep your hands toasty warm. Enchanting is especially effective on these."
        self.stats = statUpgrades(base_arm = 1, max_arm = 7)
        self.slot = "gloves_slot"
        self.traits["gloves"] = True

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Gloves that are incredibly warm and tough at the same time. It's been enchanted as much as possible."
#
# class Gauntlets(Gloves):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Gloves"
#         self.description = "Iron gauntlets that protect your hands. It's hard to enchant for some reason"
#         self.name = "Gauntlets"
#         self.stats = statUpgrades(base_dex = -1, max_dex = 0,
#                                   base_end = 4, max_end = 10,
#                                   base_arm = 4, max_arm = 6)
#
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It's been slightly enchanted to be more protective."
#         if self.level == 6:
#             self.description = "Iron gauntlets that feel stronger than adamantium. It's been enchanted as much as possible."
#
# class BoxingGloves(Gloves):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Gloves"
#         self.description = "Gloves that make your unarmed combat stronger."
#         self.name = "Boxing Gloves"
#         self.damage_boost_min = 1
#         self.damage_boost_max = 3
#         self.stats = statUpgrades(base_str = 1, max_str = 5,
#                                   base_dex = 1, max_dex = 5,
#                                   base_arm = 0, max_arm = 2)
#
#     def activate(self, entity):
#         entity.fighter.change_unarmed_attack(self.damage_boost_min, self.damage_boost_max)
#
#
#     def deactivate(self, entity):
#         entity.fighter.change_unarmed_attack(-self.damage_boost_min, -self.damage_boost_max)
#
#     def level_up(self):
#         self.enchant()
#         self.damage_boost_min += 1
#         self.damage_boost_max += 3
#         if self.wearer != None:
#             self.wearer.unarmed_damage_min += 1
#             self.wearer.unarmed_damage_max += 3
#         if self.level == 2:
#             self.description += " It's been enchanted to make your fists stronger"
#         if self.level == 6:
#             self.description = "Gloves that let you punch through anything. It's been enchanted as much as possible."
#
# class HealingGloves(Gloves):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Gloves"
#         self.description = "Gloves that let you heal yourself."
#         self.name = "Healing Gloves"
#         self.armor = 0
#
#         # self, parent, cooldown, cost, heal_amount, activation_threshold, action_cost):
#         self.skill_cooldown = 15
#         self.skill_cost = 25
#         self.heal_amount = 35
#         self.activation_threshold = 1.1
#         self.action_cost = 100
#         self.rarity = "Rare"
#
#         self.attached_skill_exists = True
#
#         self.stats = statUpgrades(base_int = 1, max_int = 3,
#                                   base_end = 1, max_end = 1,
#                                   base_arm = 2, max_arm = 5)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Heal(owner, self.skill_cooldown,
#                         self.skill_cost,
#                         self.heal_amount,
#                         self.activation_threshold,
#                         self.action_cost)
#
#     def level_up(self):
#         self.enchant()
#         self.skill_cooldown -= 1
#         if self.skill_cooldown < 10:
#             self.skill_cooldown = 10
#         self.skill_cost -= 5
#         if self.skill_cost < 10:
#             self.skill_cost = 10
#         self.heal_amount += 15
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#         if self.level == 2:
#             self.description += " It's been enchanted to heal more."
#         if self.level == 6:
#             self.description = "Gloves that lets life surge through you. It's been enchanted as much as possible."
#
# class LichHand(Gloves):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.equipment_type = "Gloves"
#         self.description = "Immense power is sworn to whoever if brave enough to sacrifice their hand and some of their max life to the hand. If you dare, it enhances all your stats and allows you to embrace the lich's immortality briefly."
#         self.name = "Lich Hand"
#         self.armor = 0
#         self.cursed = True
#
#         self.skill_cooldown = 20
#         self.skill_cost = 30
#         self.skill_duration = 4
#
#         self.health_cost = 2 # 1 / health cost is how much is removed
#
#
#         self.rarity = "Legendary"
#
#         self.attached_skill_exists = True
#         self.health_removed = 0
#
#         self.stats = statUpgrades(base_str = 2, max_str = 3,
#                                   base_dex = 3, max_dex = 4,
#                                   base_int = 3, max_int = 4,
#                                   base_end = 1, max_end = 2,
#                                   base_arm = 0, max_arm = 2)
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.Invinciblity(owner, self.skill_cost, self.skill_cooldown, self.skill_duration, activation_threshold=1.1, by_scroll=False)
#
#     def activate(self, entity):
#         self.health_removed = entity.character.get_max_health() // self.health_cost
#         entity.character.change_max_health(-self.health_removed)
#         if entity.character.get_health() > entity.character.get_max_health():
#             entity.character.change_health(entity.character.get_max_health() - entity.character.get_health())
#
#     def deactivate(self, entity):
#         entity.character.change_max_health(self.health_removed)
#
#     def level_up(self):
#         self.enchant()
#         self.skill_cooldown -= 2
#         if self.skill_cooldown < 10:
#             self.skill_cooldown = 10
#         self.skill_cost -= 2
#         if self.skill_cost < 10:
#             self.skill_cost = 10
#
#         if self.wearer != None:
#             self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
#             self.wearer.add_skill(self.attached_skill(self.wearer.parent))
#         if self.level == 2:
#             self.description += " Your power grows."
#         if self.level == 6:
#             self.description = "A hand that lets you embrace the lich's immortality. It's been enchanted as much as possible."

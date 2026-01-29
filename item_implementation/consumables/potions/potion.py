"""
POTIONS
"""
from item_implementation.items import Item

class Potion(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potiorb"
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A potior that does something."
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.traits["potion"] = True

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)



#
# class DexterityPotion(Potion):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Dexterity Potiorb")
#         self.description = "A potiorb that makes you more dexterous for a few turns."
#         self.action_description = "Gain 5 dexterity temporarily."
#         self.rarity = "Rare"
#
#     def activate_once(self, entity):
#         effect = Haste(5, 5)
#         entity.character.add_status_effect(effect)
#
# class PermanentDexterityPotion(Potion):
#     def __init__(self, render_tag, dexterity=1):
#         super().__init__(render_tag, "Permanent Dex Potiorb")
#         self.description = "Speed in a bottle"
#         self.action_description = "Gain 1 dexterity."
#         self.rarity = "Rare"
#         self.dexterity_addition = dexterity
#
#     def activate_once(self, entity):
#         entity.character.change_attribute("Dexterity", self.dexterity_addition)
#
# class PermanentStrengthPotion(Potion):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Permanent Str Potiorb")
#         self.description = "Strength in a bottle"
#         self.action_description = "Gain 1 strength."
#         self.rarity = "Rare"
#
#     def activate_once(self, entity):
#         entity.character.change_attribute("Strength", 1)
#
# class CurePotion(Potion):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Cure Potiorb")
#         self.description = "A potiorb that cures you of all status effects."
#         self.action_description = "Remove all status effects."
#         self.rarity = "Rare"
#
#     def activate_once(self, entity):
#         for effect in entity.character.status_effects:
#             if not effect.positive:
#                 effect.remove(entity)
#         entity.status_effects = []
#
# class ManaPotion(Potion):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Mana Potiorb")
#         self.description = "A potiorb that restores your mana."
#         self.action_description = "Gain 20 + 10% max mana."
#         self.rarity = "Common"
#
#     def activate_once(self, entity):
#         entity.character.change_mana(20 + (entity.character.max_mana // 10))

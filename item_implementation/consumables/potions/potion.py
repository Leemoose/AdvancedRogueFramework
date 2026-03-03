"""
POTIONS
"""
from item_implementation.items import Item
from potion_system.tag_effects import TagEffectRegistry, UsageContext

class Potion(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potion"
        self.consumeable = True
        self.throwable = True
        self.stackable = True
        self.stacks = 1
        self.range = 5
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A potion that does something."
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.tags = []
        self.traits["potion"] = True

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def throw(self, x, y, loop):
        monster_map = loop.generator.monster_map
        player = loop.player

        if player.get_x() == x and player.get_y() == y:
            self.apply_to_entity(player, loop)
        elif monster_map.get_has_entity(x, y):
            monster = monster_map.get_entity(x, y)
            self.apply_to_entity(monster, loop)
        else:
            tile = loop.generator.tile_map.get_entity(x, y)
            self.apply_to_tile(tile, loop)

    def apply_to_entity(self, entity, loop):
        loop.add_message(f"The {self.name} splashes onto {entity.name}!", (200, 200, 200))
        TagEffectRegistry.apply_effects(self.tags, UsageContext.THROW, entity, loop)

    def apply_to_tile(self, tile, loop):
        loop.add_message(f"The {self.name} shatters on the ground!", (200, 200, 200))
        TagEffectRegistry.apply_effects(self.tags, UsageContext.THROW, tile, loop)

    def quaff(self, entity):
        pass

    def apply_to_equipment(self, equipment, loop):
        loop.add_message(f"You apply the {self.name} to your {equipment.name}!", (200, 200, 200))
        TagEffectRegistry.apply_effects(self.tags, UsageContext.APPLY, equipment, loop)

    def activate(self, entity):
        TagEffectRegistry.apply_effects(self.tags, UsageContext.DRINK, entity, None)
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

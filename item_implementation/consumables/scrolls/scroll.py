from logging_config import get_logger
from item_implementation.items import Item

logger = get_logger(__name__)

class Scroll(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Scroll"
        self.consumeable = True
        self.stackable = True
        self.equipable = False
        self.throwable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = False
        self.description = "A scroll that does something."
        self.yendorb = False
        self.traits["scroll"] = True

        self.rarity = "Common"

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity, loop):
        pass

    def activate(self, entity, loop):
        self.activate_once(entity, loop)
        entity.inventory.ready_scroll = self

    def consume_scroll(self, entity):
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)
#
# class MassTormentScroll(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Mass Torment Scrorb")
#         self.description = "Must kill everything."
#         self.rarity = "Rare"
#         self.skill = MassTorment(None)
#
#     def activate_once(self, entity, loop):
#         self.skill.parent = entity
#         self.skill.activate(loop, bypass = True)
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")
#
# class InvincibilityScroll(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Invincibility Scrorb")
#         self.description = "Death cannot hold me back."
#         self.rarity = "Legendary"
#         self.skill = Invinciblity(self, 0, 5, 0)
#
#     def activate_once(self, entity, loop):
#         self.skill.parent = entity
#         self.skill.activate(loop, bypass = True)
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")
#
# class CallingScroll(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "The Scrorb of Calling")
#         self.description = "Read at your own peril."
#         self.rarity = "Rare"
#         self.skill = Awaken_Monsters(None, None, None)
#
#     def activate_once(self, entity, loop):
#         self.skill.activate(loop, bypass = True)
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")
#
# # class SleepScroll(Scroll):
# #     def __init__(self, render_tag):
# #         super().__init__(render_tag, "Sleeping Scrorb")
# #         self.description = "A guide to monster lullabies."
# #         self.rarity = "Rare"
# #         self.skill = Monster_Lullaby(None, None, None)
# #
# #     def activate_once(self, entity, loop):
# #         self.skill.activate(loop, bypass = True)
# #         self.consume_scroll(entity)
# #         loop.change_loop("inventory")
#
# class ExperienceScroll(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Experience Scrorb")
#         self.description = "Orb you glad you picked this up."
#         self.rarity = "Legendary"
#         self.experience = 50
#
#     def activate_once(self, entity, loop):
#         entity.experience += entity.experience_to_next_level
#         entity.check_for_levelup()
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")
#
#
# class EnchantScrorb(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Enchant Scrorb")
#         self.description = "A scrorb that enchants an item."
#         self.rarity = "Extra Common"
#
#     def activate_once(self, entity, loop):
#         loop.limit_inventory = "equipment"
#         loop.change_loop("enchant")
#
# class BurningAttackScrorb(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Flame Scrorb")
#         self.description = "A scrorb that lets you cast burning attack once."
#         self.rarity = "Common"
#
#     def activate_once(self, entity, loop):
#         entity.character.ready_skill = BurningAttack(entity, 0, 0, 5, 4, 6, 7)
#         loop.start_targetting()
#         loop.targets.store_skill(0, entity.character.ready_skill, entity, temp_cast=True)
#
# class BlinkScrorb(Scroll):
#     def __init__(self, render_tag=6100):
#         super().__init__(render_tag, "Blink Scrorb")
#         self.description = "A scrorb that lets you cast blink once."
#         self.rarity = "Rare"
#
#     def activate_once(self, entity, loop):
#         entity.character.ready_skill = Blink(entity)
#         loop.start_targetting(start_on_player=True)
#         loop.targets.store_skill(0, entity.character.ready_skill, entity, temp_cast=True)
#
# class MassHealScrorb(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Mass Heal Scrorb")
#         self.description = "A scrorb that lets you cast mass heal once."
#         self.rarity = "Rare"
#         self.skill = MassHeal(None)
#
#     def activate_once(self, entity, loop):
#         self.skill.parent = entity
#         self.skill.activate(loop, bypass = True)
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")
#

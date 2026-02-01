from item_implementation.items import Item
from src.core.enums import LoopType

class Book(Item):
    def __init__(self, render_tag, skill, name = "Book"):
        super().__init__(-1, -1, 0, render_tag, name = name)
        self.name = "Book"
        self.equipment_type = "Book"
        self.traits["book"] = True
        self.consumeable = True
        self.stackable = False
        self.equipable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = True
        self.description = "A book that does something."
        self.yendorb = False
        self.rarity = "Rare"

        self.skill = skill
        self.attached_skill = None

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def mark_owner(self, entity):
        self.attached_skill = self.skill(entity)

    def activate(self, entity, loop):
        if self.attached_skill.can_learn(entity):
            new_skill = self.skill(entity)
            entity.character.add_skill(new_skill)
            self.destroy = True
            entity.inventory.remove_item(self)
            loop.change_loop(LoopType.inventory)
        else:
            loop.add_message("You do not have enough intelligence to learn this spell.")

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill.description() # temporarily attach skill to nothing to get name
        else:
            return None

#class BookofSummoning(Book):
#    def __init__(self, render_tag = 6200):
#        self.school = spell.SummonSchool()
#        self.skill = self.school.random_spell()
#        super().__init__(render_tag, skill = self.skill, name = "Book of Summoning")
#        self.name = "Book of Summoning"
#
# class BookofSpace(Book):
#     def __init__(self, render_tag = 6200):
#         self.school = SpaceSchool()
#         self.skill = self.school.random_spell()
#         super().__init__(render_tag, skill = self.skill, name = "Book of Space")
#         self.name = "Book of Space"
#
# class BookofFire(Book):
#     def __init__(self, render_tag = 6200):
#         self.school = FireSchool()
#         self.skill = self.school.random_spell()
#         super().__init__(render_tag, skill = self.skill, name = "Book of Fire")
#         self.name = "Book of Fire"
#
# class BookofHypnosis(Book):
#     def __init__(self, render_tag = 6200):
#         self.school = MindSchool()
#         self.skill = self.school.random_spell()
#         super().__init__(render_tag, skill = self.skill, name = "Book of Hypnosis")
#         self.name = "Book of Hypnosis"
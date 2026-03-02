from typing import Dict
import random
from potion_system import PotionTag
from item_implementation.items import Item

class Ingredient(Item):
    def __init__(self, render_tag, name, tagDict: Dict[PotionTag, float]):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potion"
        self.consumeable = True
        self.throwable = True
        self.stackable = True
        self.stacks = 1
        self.range = 3
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A ingredient that does something."
        self.action_description = "Could be used to craft something"
        self.rarity = "Common"
        self.traits["ingredient"] = True
        self.name = name

        self.tagNames = list(tagDict.keys())
        self.tagProbs = list(tagDict.values())
        if sum(self.tagProbs) != 1.0:
            self.tagNames.append(PotionTag.Nothing)
            self.tagProbs.append(1.0 - sum(self.tagProbs))
        assert(sum(self.tagProbs) == 1.0)
        if len(self.tagNames) != 1:
            self.basic = True
        else:
            self.basic = False

    def GetTagsList(self):
        return list(self.tagDict.keys())
    
    def GetTagAtActivate(self) -> str:
        return random.choice(self.tagNames, self.tagProbs)

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def throw(self, x, y, loop):
        pass

    def quaff(self, entity):
        pass

    def apply_to_equipment(self, entity):
        pass

    def apply_to_environment(self, entity):
        pass

    def apply_to_skin(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)

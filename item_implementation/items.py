
from objects import Objects


# not equippable or consumable

class Item(Objects):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name=-1):
        super().__init__(x, y, id_tag, render_tag, name)
        self.equipable = False
        self.dropable = True
        self.consumeable = False
        self.equipped = False
        self.indestructible = False
        self.destroy = False
        self.description = "Its a " + self.name + "."
        self.stackable = False
        self.yendorb = False
        self.can_be_levelled = True
        self.level = 1
        self.attached_skill_exists = False
        self.equipment_type = None
        self.traits["item"] = True
        self.rarity = "Common"

    def get_string_description(self):
        description = []
        description.append(self.get_name())
        description.append("Equipment Type " + str(self.equipment_type))
        return description

    def set_destroy(self, destroy):
        if not self.indestructible:
            self.destroy = destroy

    def get_can_be_destroyed(self):
        return not self.indestructible



class Gold(Item):
    def __init__(self, amount, x=-1, y=-1, id_tag = -1, render_tag = 210, name = "Gold"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["gold"] = True
        self.amount = amount

class DestroyedDummy(Item):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 125, name = "Destroyed Dummy"):
        super().__init__(x,y, id_tag, render_tag, name)

"""
GLOVES
"""

"""
PANTS
"""




####################################
class Consumeable(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A consumeable item."
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.yendorb = False
        self.traits["consumeable"] = True

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


class YellowFlowerPetal(Consumeable):
    def __init__(self, render_tag = 4200):
        super().__init__(render_tag, "Yellow Flower Petal")
        self.description = "A yellow flower petal."
        self.action_description = "Heal by 5."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.character.change_health(5 + (entity.character.get_max_health() // 50))




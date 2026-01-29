"""
ARMORS
SHIELDS
"""
from item_implementation.equipment import Equipment
class Armor(Equipment):
    def __init__(self, x=-1,y=-1, id_tag=-1, render_tag = 1, name = "Armor"):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag = render_tag, name = name)
        self.name = "Armor"

    def can_be_equipped(self, entity):
        return (entity.get_attribute("Strength")) >= self.required_strength and self.equipable



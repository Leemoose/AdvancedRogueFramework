"""
ARMORS
SHIELDS
"""
from item_implementation.equipment import Equipment
class Armor(Equipment):
    def __init__(self, x=-1,y=-1, id_tag=-1, render_tag = 4000, name = "Armor"):  # TileID.ARMOR_BASIC
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag = render_tag, name = name)
        self.name = "Armor"
        self.on_hit = []
        self.on_damage = []

    def get_on_hit_effect(self):
        return self.on_hit

    def get_on_damage_effect(self):
        return self.on_damage

    def add_on_damage_effect(self, effect):
        self.on_damage.append(effect)

    def can_be_equipped(self, entity):
        return (entity.get_attribute("Strength")) >= self.required_strength and self.equipable



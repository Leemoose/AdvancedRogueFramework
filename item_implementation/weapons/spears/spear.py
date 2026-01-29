from item_implementation.weapons.weapons import Weapon
class Spear(Weapon):
    def __init__(self, render_tag=4500):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Spear", damage_min=2, damage_max=3)
        self.melee = True
        self.range = 2.9
        self.name = "Basic spear"
        self.description = "It is a spear"

    def level_up(self):
        self.damage_min += 1
        self.damage_max += 1



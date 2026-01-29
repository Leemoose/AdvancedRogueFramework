from item_implementation.weapons import Weapon

class Bow(Weapon):  # Still working
    def __init__(self, render_tag=4400):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Bow", damage_min=1, damage_max=2, range = 6)
        self.description = "A ranged weapon"
        self.effective.append("wood")
        self.traits["ranged_weapon"] = True

    def level_up(self):
        self.enchant()
        self.damage_min += 1
        self.damage_max += 2
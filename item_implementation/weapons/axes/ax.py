from item_implementation.weapons.weapons import Weapon

class Axe(Weapon):
    def __init__(self, render_tag=4600):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Axe", damage_min=3, damage_max=4)
        self.melee = True
        self.name = "Basic Axe"
        self.description = "An axe with a round edge (could be rounder). A solid weapon for a solid warrior."
        self.effective.append("wood")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An axe with the roundest edge ever seen. It's been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 3




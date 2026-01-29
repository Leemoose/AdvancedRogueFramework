from item_implementation.weapons.weapons import Weapon

"""
HAMMERS
+ Specializes in high damage
+ Solid armor piercing
- High required strength
- Low attack speed
"""

class Hammer(Weapon):
    def __init__(self, render_tag = 4700):
        super().__init__(-1, -1, 0, render_tag, "Hammer", damage_min=2, damage_max=5)
        self.melee = True
        self.name = "Hammer"
        self.description = "A hammer that you wish was more spherical. High damage potential but hard to get a solid hit in."
        self.effective.append("stone")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to hit harder"
        if self.level == 6:
            self.description = "A hammer with incredible damage potential. Still not the easiest to get a clean hit in. It's been enchanted as much as possible."
        self.damage_min += 3
        self.damage_max += 3

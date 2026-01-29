from .sword import Sword

class BroadSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=4800, name="Broadsword", damage_min=4, damage_max=5,
                 armor_piercing=4, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.required = 1

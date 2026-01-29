from item_implementation.weapons.weapons import Weapon

class Unarmed(Weapon):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name="Unarmed", min_damage=2, max_damage=3,
                 armor_piercing=0, attack_cost=100):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=min_damage,
                         damage_max=max_damage, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.melee = True
        self.description = "Bare hands."
        self.indestructible = True
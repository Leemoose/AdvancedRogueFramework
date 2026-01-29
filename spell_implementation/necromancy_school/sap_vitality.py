from spell_implementation import Spell

class SapVitality(Spell):
    def __init__(self, parent, name = "Sap Vitality", cooldown = 5, cost= 5, range = 5, action_cost = 50, damage = 3):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.damage = damage
        self.targetted = True
        self.targets_monster = True
        self.render_tag = 904

    def activate(self, defender, loop):
        self.parent.character.change_mana(-self.cost)
        defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
        self.parent.character.change_health(self.damage+ self.parent.character.skill_damage_increase())
        return True  # return true if successfully cast, burningAttack cannot fail

    def castable(self, target):
        return super().castable(target) and self.in_range(target)

    def full_description(self):
        desc = "Deals a small amount of damage, healing for the same amount.\n\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

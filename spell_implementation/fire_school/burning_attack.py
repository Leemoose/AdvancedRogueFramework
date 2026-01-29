from spell_implementation import Spell
from spell_implementation.effects import Burn
from src.core.constants import INFINITE_DURATION
class BurningAttack(Spell):
    def __init__(self, parent, name = "Burning Attack", cooldown = 10, cost= 5, range = 5, action_cost = 50, damage = 3, burn_damage = 3, burn_duration=5):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.damage = damage
        self.burn_damage = burn_damage
        self.targetted = True
        self.targets_monster = True
        self.burn_duration = burn_duration
        self.render_tag = 904

    def activate(self, defender, loop):
        self.parent.character.change_mana(-self.cost)
        defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
        effect = Burn(self.burn_duration + self.parent.character.skill_duration_increase(),
                        self.burn_damage + self.parent.character.skill_damage_increase(), self.parent)
        defender.character.status.add_status_effect(effect)
        return True  # return true if successfully cast, burningAttack cannot fail

    def castable(self, target):
        return super().castable(target) and self.in_range(target)

    def description(self):
        if self.burn_duration == INFINITE_DURATION:
            return self.name + "(" + str(self.cost) + " cost, " + str(
                self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage at range " + str(
                self.range) + ", " + str(self.burn_damage) + " burn damage permanently)"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(
            self.damage) + " damage at range " + str(self.range) + ", " + str(
            self.burn_damage) + " burn damage for " + str(self.burn_duration) + " turns)"

    def full_description(self):
        desc = "Throw a small bolt of fire at a target that sets the target ablaze.\n\n"
        desc += f"Deals {self.damage} at range {self.range}\n"
        desc += f"Burns target for {self.burn_damage} burn damage every turn for {self.burn_duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

from spell_implementation.effects.effect import StatusEffect
from src.core.constants import INFINITE_DURATION
class Burn(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Burn", "is burning for " + str(damage) + "damage", duration)
        self.damage = damage
        self.inflictor = inflictor

    def apply_effect(self, target):
        pass

    def tick(self, target):
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)

    def remove(self, target):
        pass
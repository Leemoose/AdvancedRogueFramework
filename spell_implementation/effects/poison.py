from .effect import StatusEffect
from src.core.constants import INFINITE_DURATION
class Poison(StatusEffect):
    def __init__(self, inflictor, duration = 2, damage = 3):
        super().__init__(801, "Poison", "is being poisoned for " + str(damage) + "damage", duration)
        self.damage = damage
        self.inflictor = inflictor
        self.cumulative = True

    def tick(self, target):
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)
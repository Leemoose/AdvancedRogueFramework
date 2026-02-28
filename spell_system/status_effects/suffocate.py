
from src.core.constants import INFINITE_DURATION
from .base import StatusEffect


class Suffocate(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Suffocate", f"is suffocating for {damage} damage", duration)
        self.damage = damage
        self.inflictor = inflictor
        self.time_to_suffocate = 3

    def tick(self, target):
        self.time_to_suffocate -= 1
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        elif self.time_to_suffocate <= 0:
            target.take_damage(self.inflictor, self.damage)

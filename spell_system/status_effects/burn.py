"""Burn status effect - fire damage over time."""

from src.core.constants import INFINITE_DURATION
from .base import StatusEffect


class Burn(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Burn", f"is burning for {damage} damage", duration)
        self.damage = damage
        self.inflictor = inflictor

    def tick(self, target):
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)

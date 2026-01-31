"""Bleed status effect - damage over time from physical wounds."""

from src.core.constants import INFINITE_DURATION
from .base import StatusEffect


class Bleed(StatusEffect):
    """DoT effect from physical damage, deals damage each turn."""

    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Bleeding", "is bleeding", duration)
        self.damage = damage
        self.inflictor = inflictor
        self.positive = False

    def tick(self, target):
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)

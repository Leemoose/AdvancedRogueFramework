"""Weak status effect - reduces target's strength."""

from .base import StatusEffect


class Weak(StatusEffect):
    """Debuff that reduces target's strength temporarily."""

    def __init__(self, duration, strength_reduction):
        super().__init__(803, "Weak", "feels weak", duration)
        self.strength_reduction = strength_reduction
        self.positive = False

    def apply_effect(self, target):
        target.change_attribute("strength", -self.strength_reduction)

    def remove(self, target):
        target.change_attribute("strength", self.strength_reduction)

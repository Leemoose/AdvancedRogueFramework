"""Invincible status effect - prevents death."""

from .base import StatusEffect


class Invincible(StatusEffect):
    """Buff that prevents the target from dying."""

    def __init__(self, duration):
        super().__init__(806, "Invincible", "can't be killed", duration)
        self.positive = True

    def apply_effect(self, target):
        target.invincible = True

    def remove(self, target):
        target.invincible = False
        # Ensure at least 1 HP after invincibility ends
        target.health = max(1, target.health)

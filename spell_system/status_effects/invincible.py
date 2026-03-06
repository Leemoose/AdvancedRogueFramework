"""Invincible status effect - prevents death."""

from .base import StatusEffect


class Invincible(StatusEffect):
    """Buff that prevents the target from dying."""

    def __init__(self, duration):
        super().__init__(806, "Invincible", "can't be killed", duration)
        self.positive = True

    def apply_effect(self, target):
        target.character.status.invincible = True

    def remove(self, target):
        target.character.status.invincible = False
        # Ensure at least 1 HP after invincibility ends
        if target.character.get_health() < 1:
            target.character.change_health(1 - target.character.get_health())

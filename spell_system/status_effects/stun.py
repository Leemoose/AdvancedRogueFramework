"""Stun/Paralyze status effect - prevents all actions."""

from .base import StatusEffect


class Stun(StatusEffect):
    """Debuff that prevents the target from taking any actions."""

    def __init__(self, duration):
        super().__init__(802, "Stunned", "is stunned", duration)
        self.positive = False

    def apply_effect(self, target):
        target.character.status.can_take_actions = False

    def remove(self, target):
        target.character.status.can_take_actions = True


# Alias for backwards compatibility
Paralyze = Stun

"""Root status effect - prevents movement."""

from .base import StatusEffect


class Root(StatusEffect):
    """Debuff that prevents the target from moving."""

    def __init__(self, inflictor, duration=5):
        super().__init__(801, "Rooted", "is rooted", duration)
        self.inflictor = inflictor
        self.positive = False

    def apply_effect(self, target):
        target.character.status.can_move = False

    def remove(self, target):
        target.character.status.can_move = True

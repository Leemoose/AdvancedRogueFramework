"""Charm status effect - makes monsters friendly."""

from .base import StatusEffect


class Charm(StatusEffect):
    """Debuff that makes a monster temporarily friendly."""

    def __init__(self, duration, inflictor):
        super().__init__(806, "Charmed", "is charmed", duration)
        self.inflictor = inflictor
        self.old_brain = None
        self.positive = False  # Negative from monster's perspective

    def apply_effect(self, target):
        if target.has_trait("monster"):
            self.old_brain = target.brain
            target.make_friendly()

    def remove(self, target):
        if target.has_trait("monster"):
            target.brain = self.old_brain

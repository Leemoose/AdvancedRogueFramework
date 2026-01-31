"""Haste status effect - increases dexterity/speed."""

from .base import StatusEffect


class Haste(StatusEffect):
    """Buff that increases target's dexterity temporarily."""

    def __init__(self, duration, dexterity_bonus):
        super().__init__(804, "Haste", "feels fast", duration)
        self.dexterity_bonus = dexterity_bonus
        self.positive = True

    def apply_effect(self, target):
        target.change_attribute("dexterity", self.dexterity_bonus)

    def remove(self, target):
        target.change_attribute("dexterity", -self.dexterity_bonus)

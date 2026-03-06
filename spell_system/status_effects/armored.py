"""Invincible status effect - prevents death."""

from .base import StatusEffect


class Armored(StatusEffect):
    """Buff that temporarily raises armor."""

    def __init__(self, duration, armor_increase):
        super().__init__(806, "Armored", "has raised defense", duration)
        self.positive = True
        self.armor_increase = armor_increase

    def apply_effect(self, target):
        target.character.attributes.change_armor(self.armor_increase)

    def remove(self, target):
        target.character.attributes.change_armor(-self.armor_increase)

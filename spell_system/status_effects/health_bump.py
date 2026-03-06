
from .base import StatusEffect


class HealthBump(StatusEffect):

    def __init__(self, duration):
        super().__init__(806, "Health Bump", "has gained temporary hit points", duration)
        self.positive = True
        self.max_health_increase = 1

    def apply_effect(self, target):
        self.max_health_increase = target.character.get_max_health() // 2
        target.character.change_max_health(self.max_health_increase)
        target.character.change_health(self.max_health_increase)

    def remove(self, target):
        target.character.change_max_health(-self.max_health_increase)
        if target.character.get_health() > target.character.get_max_health():
            overflow = target.character.get_health() - target.character.get_max_health()
            target.character.change_health(-overflow)
        if target.character.get_health() < 1:
            target.character.change_health(1 - target.character.get_health())


from .base import StatusEffect


class HealthBump(StatusEffect):

    def __init__(self, duration):
        super().__init__(806, "Health Bump", "has gained temporary hit points", duration)
        self.positive = True
        self.max_health_increase = 1

    def apply_effect(self, target):
        self.max_health_increase = target.get_max_health() // 2
        target.change_max_health(self.max_health_increase)
        target.get_health(self.max_health_increase)

    def remove(self, target):
        target.change_max_health(-self.max_health_increase)
        target.health = max(1, target.health)

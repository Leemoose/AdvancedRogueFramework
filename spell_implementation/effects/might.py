from .effect import StatusEffect
class Might(StatusEffect):
    def __init__(self, duration, strength):
        super().__init__(803, "Might", "feels strong", duration)
        self.strength = strength
        self.positive = True

    def apply_effect(self, target):
        target.change_attribute("strength", self.strength)

    def remove(self, target):
        target.change_attribute("strength", -self.strength)
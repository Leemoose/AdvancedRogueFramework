"""Sleep status effect - target is unconscious."""

from .base import StatusEffect


class Sleep(StatusEffect):
    """Debuff that puts the target to sleep."""

    def __init__(self, duration):
        super().__init__(806, "Asleep", "is sleeping", duration)
        self.traits["asleep"] = True
        self.positive = False

    def apply_effect(self, target):
        target.character.status.set_awake(False)

    def remove(self, target):
        target.character.status.set_awake(True)

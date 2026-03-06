
from .base import StatusEffect


class Silence(StatusEffect):

    def __init__(self, duration):
        super().__init__(806, "Silence", "is silenced", duration)
        self.traits["silence"] = True
        self.positive = False

    def apply_effect(self, target):
        target.character.status.set_can_spellcast(False)

    def remove(self, target):
        target.character.status.set_can_spellcast(True)

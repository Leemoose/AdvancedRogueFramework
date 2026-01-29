from .effect import StatusEffect
from .slow import Slow

class Berserk(StatusEffect):
    def __init__(self, duration):
        super().__init__(802, "Berserk", "is berserking", duration)
        self.added_health = 0
        self.added_strength = 0
        self.added_damage = 0

    def apply_effect(self, target):
        self.added_health = target.character.get_max_health() // 5
        self.added_strength = target.character.get_strength() // 3
        self.added_damage = target.fighter.get_base_damage() // 2

        target.character.change_max_health(self.added_health)
        target.character.change_strength( self.added_strength)
        target.fighter.change_base_damage( self.added_damage)

        target.character.status.set_can_spellcast(False)

    def remove(self, target):
        target.character.change_max_health( - self.added_health)
        target.character.change_strength( - self.added_strength)
        target.fighter.change_base_damage(- self.added_damage)

        target.character.status.set_can_spellcast(True)

        target.character.status.add_status_effect(Slow(target, duration = 5))

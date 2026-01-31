"""
Hobgoblin - A larger, more dangerous goblin with teleportation abilities.

Hobgoblins use blink strike to close distances and deal heavy damage,
then flee when wounded.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_hobgoblin_behaviors
from spell_system import give_spell


class Hobgoblin(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2102,  # New render tag for hobgoblin
            name="Hobgoblin",
            experience_given=20,
            health=25,
            mana=15,
            min_damage=4,
            max_damage=8,
            gold=10
        )

        # Hobgoblin AI - blink strike + combat + flee
        self.brain = MonsterAI(self, create_hobgoblin_behaviors())

        # Give blink strike spell
        give_spell(self, 'blink_strike',
                   cooldown=10,
                   cost=3,
                   range=5,
                   effects_overrides=[
                       {},  # blink_to_target params
                       {'amount': 15}  # damage amount
                   ])

        self.strength = 5
        self.dexterity = 5
        self.endurance = 3
        self.intelligence = 4

        self.traits["goblin"] = True
        self.traits["hobgoblin"] = True

        self.description = (
            "The older, more dangerous cousin of its smaller green relatives. "
            "Hobgoblins tower over regular goblins with bulging muscles and "
            "cunning eyes. They possess an unnatural ability to blink through "
            "space, appearing next to their prey in an instant before delivering "
            "a devastating strike. When wounded, they will flee to fight another day."
        )

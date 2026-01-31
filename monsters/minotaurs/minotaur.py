"""
Minotaur - A powerful bull-like creature that can shrug off crowd control.

Minotaurs are slow but incredibly strong. They have a 75% chance to
break free from stun and root effects each turn.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_minotaur_behaviors


class Minotaur(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2210,  # Minotaur sprite
            name="Minotaur",
            experience_given=30,
            health=40,
            min_damage=6,
            max_damage=12,
            gold=15
        )

        # Minotaur AI - shrug off CC + aggressive combat
        self.brain = MonsterAI(self, create_minotaur_behaviors())

        # Slow but powerful
        self.character.change_action_cost("move", 120)

        self.strength = 8
        self.dexterity = 2
        self.endurance = 5
        self.intelligence = 0

        self.traits["minotaur"] = True
        self.traits["beast"] = True

        self.description = (
            "A large, angry bull-man with mighty horns and rippling muscles. "
            "The Minotaur is a fearsome creature of raw strength and fury. "
            "Its thick hide and stubborn will allow it to shrug off effects "
            "that would incapacitate lesser creatures. Once it locks onto prey, "
            "it charges relentlessly until one of them falls."
        )

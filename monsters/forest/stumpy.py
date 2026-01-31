"""
Stumpy - An animated tree stump seeking vengeance.

Stumpy waits in ambush until prey comes close, then attacks with
twisted roots and poisonous sap. Vulnerable to fire.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_stumpy_behaviors


class Stumpy(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2300,  # Stumpy sprite
            name="Stumpy",
            experience_given=20,
            health=15,
            min_damage=3,
            max_damage=8,
            gold=5
        )

        # Stumpy AI - ambush predator
        self.brain = MonsterAI(self, create_stumpy_behaviors())

        self.strength = 4
        self.dexterity = 2
        self.endurance = 6
        self.intelligence = 2

        # Wooden armor
        self.character.attributes.change_armor(8)

        self.traits["stumpy"] = True
        self.traits["wood"] = True
        self.traits["plant"] = True

        self.description = (
            "An ancient, gnarled tree stump brought to life by dark magic, "
            "Stumpy harbors a deep, burning desire for vengeance. Its twisted "
            "roots writhe with malicious intent, and its hollow eyes glow with "
            "a sinister, green light. With bark as tough as iron and splintered "
            "limbs that lash out like whips, this vengeful stump seeks retribution "
            "for the countless trees felled by human hands. Beware its crushing "
            "roots and poisonous sap."
        )

"""
Treant - A massive animated tree guardian.

Treants are slow but incredibly powerful forest guardians with high
health and armor. Their attacks can root enemies in place.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_treant_behaviors


class Treant(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2310,  # Treant sprite
            name="Treant",
            experience_given=50,
            health=60,
            min_damage=8,
            max_damage=20,
            gold=25
        )

        # Treant AI - slow but powerful
        self.brain = MonsterAI(self, create_treant_behaviors())

        # Very slow movement
        self.character.change_action_cost("move", 150)

        self.strength = 10
        self.dexterity = 1
        self.endurance = 12
        self.intelligence = 4

        # Heavy wooden armor
        self.character.attributes.change_armor(12)

        self.traits["treant"] = True
        self.traits["wood"] = True
        self.traits["plant"] = True

        self.description = (
            "Towering over the forest canopy, the Treant is a massive and "
            "malevolent guardian with bark-covered armor tough as iron. Its "
            "glowing green eyes and deep, rumbling growl instill fear in all "
            "who hear it. Driven by an ancient grudge, it uses devastating "
            "root lash attacks to ensnare and immobilize foes, protecting its "
            "sacred domain with relentless strength. The Treant's presence warps "
            "the forest, darkening and twisting the environment as it exacts "
            "vengeance on any who defile its home."
        )

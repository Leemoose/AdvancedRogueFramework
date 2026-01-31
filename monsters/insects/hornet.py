"""
Hornet - A fast, aggressive flying insect with a paralyzing sting.

Hornets are fragile but fast. They swarm enemies with paralyzing attacks.
Spawned by Insect Nests when they are damaged.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_hornet_behaviors


class Hornet(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2340,  # Hornet sprite
            name="Hornet",
            experience_given=15,
            health=8,
            min_damage=2,
            max_damage=5,
            gold=2
        )

        # Hornet AI - aggressive fast attacker
        self.brain = MonsterAI(self, create_hornet_behaviors())

        # Fast movement, slow attack (stinging takes time)
        self.character.change_action_cost("move", 50)
        self.character.change_action_cost("attack", 150)

        self.strength = 2
        self.dexterity = 10
        self.endurance = 1
        self.intelligence = 0

        self.traits["hornet"] = True
        self.traits["insect"] = True
        self.traits["flying"] = True

        self.description = (
            "A vicious flying insect with a painful, paralyzing sting. "
            "Though fragile, Hornets are fast and aggressive, swarming "
            "enemies in overwhelming numbers. Their stingers can temporarily "
            "paralyze prey, leaving them vulnerable to the swarm."
        )

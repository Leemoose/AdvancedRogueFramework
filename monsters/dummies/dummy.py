"""
Dummy - A training dummy that doesn't attack or move.

The Dummy is a practice target. It won't attack back but has high
health regeneration, making it difficult to destroy unless you deal
enough damage quickly.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_dummy_behaviors


class Dummy(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2250,  # Dummy sprite
            name="Training Dummy",
            experience_given=0,  # No XP from dummies
            health=25,
            min_damage=0,
            max_damage=0,
            gold=0
        )

        # Dummy AI - does nothing
        self.brain = MonsterAI(self, create_dummy_behaviors())

        # Dummy has no stats
        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.intelligence = 0

        # High health regeneration - repairs itself if not one-shot
        self.character.health_regen = 50

        # Doesn't stop auto-explore
        self.stops_autoexplore = False

        self.traits["dummy"] = True
        self.traits["wood"] = True
        self.traits["construct"] = True

        self.description = (
            "A training dummy that will not move or attack, but seems to "
            "repair itself if not destroyed quickly. Useful for practicing "
            "combat techniques without real danger. The wooden frame is "
            "surprisingly resilient."
        )

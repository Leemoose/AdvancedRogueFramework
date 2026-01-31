"""
Squid - A small, frail aquatic creature.

Squids are weak water creatures that shimmer with bioluminescence.
They lack offensive capabilities and rely on evasion.

NOTE: Water branch not yet implemented. Has water attribute but
not added to monster generator.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_water_monster_behaviors


class Squid(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2400,  # Squid sprite
            name="Squid",
            experience_given=10,
            health=10,
            min_damage=1,
            max_damage=3,
            gold=3
        )

        # Basic water monster AI
        self.brain = MonsterAI(self, create_water_monster_behaviors())

        self.strength = 0
        self.dexterity = 6
        self.endurance = 0
        self.intelligence = 4

        self.traits["squid"] = True
        self.traits["water"] = True
        self.traits["aquatic"] = True

        self.description = (
            "A small, frail creature that lacks any mysterious power. Its "
            "translucent body shimmers with bioluminescent patterns, emitting "
            "a faint glow in the dark rift waters. With delicate, tentacle-like "
            "appendages, it navigates the currents with grace but lacks offensive "
            "capabilities. Despite its vulnerability, the Squid possesses keen "
            "survival instincts, using camouflage and swift movements to evade "
            "predators."
        )

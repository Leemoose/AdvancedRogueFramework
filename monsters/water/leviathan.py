"""
Leviathan - A massive, terrifying eel-like sea creature.

Leviathans are powerful water predators with high health and strength.
Their bioluminescent patterns and glowing red eyes strike fear into prey.

NOTE: Water branch not yet implemented. Has water attribute but
not added to monster generator.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_water_monster_behaviors


class Leviathan(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2410,  # Leviathan sprite
            name="Leviathan",
            experience_given=60,
            health=100,
            min_damage=10,
            max_damage=25,
            gold=50
        )

        # Water monster AI
        self.brain = MonsterAI(self, create_water_monster_behaviors())

        self.strength = 15
        self.dexterity = 6
        self.endurance = 10
        self.intelligence = 4

        self.traits["leviathan"] = True
        self.traits["water"] = True
        self.traits["aquatic"] = True

        self.description = (
            "A massive, eel-like creature with bioluminescent patterns along "
            "its body. Its eyes glow a menacing red, and its mouth is filled "
            "with rows of razor-sharp teeth. The Leviathan is an apex predator "
            "of the deep waters, feared by all other aquatic creatures. Its "
            "serpentine body can crush ships and its jaws can tear through "
            "the toughest armor."
        )

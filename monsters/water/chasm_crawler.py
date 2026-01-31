"""
Chasm Crawler - An armored, semi-aquatic predator.

Chasm Crawlers have thick chitinous armor and powerful mandibles.
They patrol both submerged caverns and rocky terrain.

NOTE: Water branch not yet implemented. Has water attribute but
not added to monster generator.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_water_monster_behaviors


class ChasmCrawler(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2420,  # Chasm Crawler sprite
            name="Chasm Crawler",
            experience_given=40,
            health=60,
            min_damage=8,
            max_damage=15,
            gold=30
        )

        # Water monster AI
        self.brain = MonsterAI(self, create_water_monster_behaviors())

        self.strength = 12
        self.dexterity = 4
        self.endurance = 8
        self.intelligence = 2

        # Heavy chitinous armor
        self.character.attributes.change_armor(10)

        self.traits["chasm_crawler"] = True
        self.traits["water"] = True
        self.traits["aquatic"] = True

        self.description = (
            "The Chasm Crawler is a formidable predator of the rocky depths, "
            "adorned in thick, chitinous armor that seamlessly blends with its "
            "environment. With a segmented body designed for agility and strength, "
            "it maneuvers effortlessly through both submerged caverns and dry "
            "rocky terrain. Equipped with powerful mandibles capable of crushing "
            "solid stone, it tunnels through rock formations with remarkable ease. "
            "This semi-aquatic creature patrols its territory with vigilance, "
            "defending its hunting grounds against intruders with swift, precise strikes."
        )

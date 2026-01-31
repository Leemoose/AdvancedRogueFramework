"""
Golem - A slow but incredibly tough stone construct.

Golems are animated stone guardians. They move very slowly but have
high health and armor. Cannot traverse deep water.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_golem_behaviors


class Golem(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2220,  # Golem sprite
            name="Golem",
            experience_given=35,
            health=35,
            min_damage=5,
            max_damage=15,
            gold=20
        )

        # Golem AI - slow but relentless
        self.brain = MonsterAI(self, create_golem_behaviors())

        # Very slow movement
        self.character.change_action_cost("move", 200)

        self.strength = 6
        self.dexterity = 0
        self.endurance = 8
        self.intelligence = 2

        # Stone construct - armored
        self.character.attributes.change_armor(5)

        self.traits["golem"] = True
        self.traits["stone"] = True
        self.traits["construct"] = True

        # Restriction for deep water (cannot swim)
        self.restriction = "deep water"

        self.description = (
            "Forged from the very bedrock of the earth and brought to life by "
            "ancient, powerful magic, the Stone Golem is a formidable guardian. "
            "Towering and imposing, its massive body is composed of jagged boulders "
            "and smooth stones, seamlessly held together by an unyielding mystical "
            "force. Glowing runes etched into its surface pulse with a dim, ethereal "
            "light. Slow but relentless, the Stone Golem is an unstoppable force "
            "of nature, driven by an unbreakable duty to protect its domain."
        )

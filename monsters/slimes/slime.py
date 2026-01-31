"""
Slime - A slow, gelatinous creature that picks up items.

Different from Ooze (which destroys items). Slimes mindlessly collect
anything they touch, drawn to shiny objects.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_slime_behaviors


class Slime(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=1100,  # Same as old framework
            name="Slime",
            experience_given=5,
            health=5,
            min_damage=1,
            max_damage=3,
            gold=0
        )

        # Slime-specific setup
        self.brain = MonsterAI(self, create_slime_behaviors())

        # Very slow movement but instant item grabbing
        self.character.change_action_cost("move", 200)
        self.character.change_action_cost("grab", 0)

        self.traits["slime"] = True

        self.description = (
            "These amorphous blobs of translucent, gelatinous matter emerge from "
            "the depths of the rifts. Their bodies pulse with a sickly green glow, "
            "fueled by the chaotic energies of their environment. Rift Slimes "
            "mindlessly absorb anything they touch, drawn to items which they "
            "swiftly engulf. They show no preference or intelligence, simply "
            "collecting whatever they encounter."
        )

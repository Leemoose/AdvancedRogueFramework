"""
Raptor - A terrifyingly fast prehistoric predator.

Raptors are incredibly fast and aggressive. They close distances quickly
and strike with lethal precision.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_raptor_behaviors


class Raptor(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2230,  # Raptor sprite
            name="Velociraptor",
            experience_given=30,
            health=20,
            min_damage=5,
            max_damage=10,
            gold=12
        )

        # Raptor AI - very aggressive and fast
        self.brain = MonsterAI(self, create_raptor_behaviors())

        # Very fast movement
        self.character.change_action_cost("move", 50)

        self.strength = 5
        self.dexterity = 12
        self.endurance = 2
        self.intelligence = 3

        self.traits["raptor"] = True
        self.traits["beast"] = True
        self.traits["dinosaur"] = True

        self.description = (
            "The Raptor is a terrifying predator from an ancient era. Its sleek, "
            "scaly body is covered in iridescent feathers that shimmer with "
            "otherworldly hues. With razor-sharp claws and teeth honed to "
            "perfection, it moves with lethal grace and speed. The Raptor's eyes, "
            "glowing with predatory intelligence, lock onto prey with unerring "
            "precision. This cunning hunter uses shadows and surroundings to its "
            "advantage, striking with blinding speed and ruthless efficiency."
        )

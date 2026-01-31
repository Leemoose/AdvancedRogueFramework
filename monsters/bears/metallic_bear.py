"""
Metallic Bear - An armored bear that enters fury mode when wounded.

The Metallic Bear is a terrifying forest predator. When its health
drops low, it enters a devastating fury mode with increased damage
and attack speed.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_metallic_bear_behaviors


class MetallicBear(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2320,  # Metallic Bear sprite
            name="Metallic Bear",
            experience_given=45,
            health=40,
            min_damage=8,
            max_damage=15,
            gold=30
        )

        # Metallic Bear AI - fury mode when low health
        self.brain = MonsterAI(self, create_metallic_bear_behaviors())

        self.strength = 12
        self.dexterity = 5
        self.endurance = 10
        self.intelligence = 1

        # Metallic armor
        self.character.attributes.change_armor(15)

        self.traits["metallic_bear"] = True
        self.traits["beast"] = True
        self.traits["metal"] = True

        self.description = (
            "This imposing creature, with fur interwoven with metallic threads, "
            "gleams ominously as it prowls through the forest. Its powerful, "
            "ironclad muscles and razor-sharp claws make it a fearsome opponent. "
            "When the Metallic Bear's health drops low, it enters a terrifying "
            "fury mode, its eyes glowing with an intense, fiery light. In this "
            "state, it becomes even more dangerous, dealing increased damage and "
            "attacking with blinding speed. The sound of clashing metal and its "
            "ferocious roars echo through the trees."
        )

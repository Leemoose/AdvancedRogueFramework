"""
Tormentorb - A floating orb that torments victims with psychic damage and slowing.

Tormentorbs hover menacingly and attack from range with their torment ability,
dealing damage based on the target's health and slowing their movements.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_tormentorb_behaviors
from spell_system import give_spell


class Tormentorb(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2240,  # Tormentorb sprite
            name="Tormentorb",
            experience_given=65,
            health=45,
            mana=50,
            min_damage=4,
            max_damage=8,
            gold=25
        )

        # Tormentorb AI - torment spell + slow combat
        self.brain = MonsterAI(self, create_tormentorb_behaviors())

        # Give torment spell
        give_spell(self, 'torment',
                   cooldown=10,
                   cost=5,
                   range=5,
                   effects_overrides=[
                       {'amount': 10},  # damage
                       {'duration': 3, 'amount': 50}  # slow duration and amount
                   ])

        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 12

        # High armor floating orb
        self.character.attributes.change_armor(6)

        self.traits["orb"] = True
        self.traits["magical"] = True
        self.traits["floating"] = True

        self.description = (
            "A floating orb of malevolent energy that can torment and slow "
            "victims with its gaze. The Tormentorb hovers silently, its surface "
            "swirling with dark energies. When it focuses its attention on a "
            "creature, waves of psychic anguish wash over them, sapping their "
            "strength and slowing their movements. Its armored shell makes it "
            "difficult to destroy."
        )

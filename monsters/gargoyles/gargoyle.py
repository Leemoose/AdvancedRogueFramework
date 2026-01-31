"""
Gargoyle - A stone sentinel with a petrifying gaze.

Gargoyles can turn enemies to stone temporarily with their magical gaze.
They are tough and armored, blending with stone architecture.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_gargoyle_behaviors
from spell_system import give_spell


class Gargoyle(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2200,  # Gargoyle sprite
            name="Gargoyle",
            experience_given=20,
            health=20,
            mana=20,
            min_damage=3,
            max_damage=7,
            gold=8
        )

        # Gargoyle AI - petrify gaze + combat
        self.brain = MonsterAI(self, create_gargoyle_behaviors())

        # Give petrify spell (30% activation chance built into behavior)
        give_spell(self, 'petrify',
                   cooldown=10,
                   cost=5,
                   range=4,
                   effects_overrides=[
                       {'duration': 3}  # 3 turn stun
                   ])

        self.strength = 2
        self.dexterity = 0
        self.endurance = 6
        self.intelligence = 5

        # Stone creature - armored
        self.character.attributes.change_armor(3)

        self.traits["gargoyle"] = True
        self.traits["stone"] = True

        self.description = (
            "Carved from ancient stone and imbued with dark magic from the depths "
            "of the rifts, the Gargoyle is a sentinel of terror and stone-cold fury. "
            "Perched high atop jagged spires and crumbling ruins, its chiseled form "
            "blends seamlessly with the twisted architecture. With wings stretched "
            "wide, resembling weathered stone veined with iridescent minerals, the "
            "Gargoyle looms over its domain like a silent sentinel. Its glowing "
            "azure eyes can turn creatures to stone with a single gaze."
        )

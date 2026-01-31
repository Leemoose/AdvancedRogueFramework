"""
Goblin Shaman - A twisted goblin spellcaster that summons reinforcements.

The Shaman commands lesser goblins through dark rituals and will flee
when threatened.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_goblin_shaman_behaviors
from spell_system import give_spell


class GoblinShaman(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2101,  # New render tag for shaman
            name="Goblin Shaman",
            experience_given=25,
            health=20,
            mana=30,
            min_damage=2,
            max_damage=5,
            gold=15
        )

        # Shaman AI - summons goblins and flees
        self.brain = MonsterAI(self, create_goblin_shaman_behaviors())

        # Give summon goblin spell
        give_spell(self, 'summon_goblin',
                   cooldown=15,
                   cost=5,
                   range=4)

        self.strength = 1
        self.dexterity = 1
        self.endurance = 1
        self.intelligence = 5

        self.traits["goblin"] = True
        self.traits["shaman"] = True

        self.description = (
            "A twisted figure draped in tattered robes adorned with crude bones "
            "and fetishes, the Goblin Shaman is a malevolent conduit of dark magic. "
            "With hunched posture and gnarled fingers clutching a gnarled staff, "
            "its yellowed eyes gleam with a sinister intelligence. The Shaman's skin "
            "is marked with mystical runes that pulse with a sickly green glow, "
            "channeling the chaotic energies of the rifts. In battle, it summons "
            "swarms of lesser goblins, overwhelming foes with sheer numbers."
        )

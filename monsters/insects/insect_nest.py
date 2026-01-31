"""
Insect Nest - An immobile hive that spawns hornets when damaged.

The Insect Nest cannot move or attack directly. When damaged, it
releases a swarm of hornets to defend itself. Vulnerable to fire.
"""

from monsters.monster import Monster
from monster_implementation import MonsterAI, create_insect_nest_behaviors


class InsectNest(Monster):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2330,  # Insect Nest sprite
            name="Insect Nest",
            experience_given=40,
            health=25,
            min_damage=0,
            max_damage=0,
            gold=15
        )

        # Nest AI - immobile, spawns on damage
        self.brain = MonsterAI(self, create_insect_nest_behaviors())

        # Cannot move
        self.character.movable = False

        self.strength = 0
        self.dexterity = 0
        self.endurance = 5
        self.intelligence = 0

        self.traits["insect_nest"] = True
        self.traits["structure"] = True
        self.traits["wood"] = True

        self.description = (
            "Nestled within the forest, this immobile structure is a pulsating "
            "hive of malevolent activity. Each strike against the Insect Nest "
            "provokes a swarm of flying, venomous insects that emerge in a "
            "frenzied cloud to defend their home. Though these insects are "
            "fragile with low health, their venomous bites can quickly overwhelm "
            "and debilitate attackers. The nest itself is powerless, relying "
            "entirely on the relentless defense of its swarming guardians."
        )

    def do_defend(self, attacker, loop):
        """When damaged, spawn a hornet."""
        from monsters.insects.hornet import Hornet

        # Find nearby empty tile for hornet
        location = loop.generator.get_nearest_empty_tile(self.get_location())
        if location is not None:
            hornet = Hornet()
            loop.generator.summoner.append((hornet, location[0], location[1]))
            loop.add_message(f"A hornet emerges from the {self.name}!")

        return self.fighter.do_defend()

"""
Looter - A specialized goblin focused on grabbing items at incredible speed.

Looters prioritize stealing items over combat and are extremely fast
at picking things up. They flee at the first sign of danger.
"""

from monsters.goblins.goblin import Goblin
from monster_implementation import MonsterAI, create_looter_behaviors


class Looter(Goblin):
    def __init__(self, x=-1, y=-1):
        super().__init__(
            x=x, y=y,
            render_tag=2100,  # New render tag for looter
            name="Looter", 
            experience_given=25,
            health=15,
            min_damage=3,
            max_damage=6,
            rarity="Rare"
        )

        # Override with looter behaviors - prioritizes items
        self.brain = MonsterAI(self, create_looter_behaviors())

        # Extremely fast movement and grabbing
        self.character.action_costs["move"] = 25
        self.character.action_costs["grab"] = 1

        self.dexterity = 8

        self.traits["looter"] = True

        self.description = (
            "A particularly quick and greedy goblin, the Looter lives for "
            "the thrill of snatching treasure. Its nimble fingers and "
            "lightning-fast reflexes allow it to grab items almost instantly. "
            "Looters care more about loot than fighting and will flee at "
            "the first opportunity if threatened. Chase them down quickly "
            "or watch your valuables disappear!"
        )

"""
Summon School Spells

Focused on summoning creatures to fight for you.
"""

from old.spell_builder import spell, Schools
from ..effects.builders import summon

__all__ = ['summon_goblin', 'summon_skeleton', 'summon_wolf', 'summon_golem']


summon_goblin = spell(
    "summon_goblin", "Summon Goblin",
    school=Schools.SUMMON, level=1, cost=3, cooldown=10, range=3,
    action_cost=75, targeting="ground", icon=9130,
    tags=["summon", "minion"],
    effects=[
        summon("goblin", duration=20),
    ],
    description="""Summon a weak goblin to fight for you.

The goblin is fragile but can distract enemies
and deal minor damage."""
)


summon_skeleton = spell(
    "summon_skeleton", "Summon Skeleton",
    school=Schools.SUMMON, level=2, cost=5, cooldown=15, range=3,
    action_cost=75, targeting="ground", icon=9131,
    required_intelligence=5,
    tags=["summon", "minion", "undead"],
    effects=[
        summon("skeleton", duration=30),
    ],
    description="""Raise a skeleton warrior from the ground.

Skeletons are resilient and make excellent front-line fighters."""
)


summon_wolf = spell(
    "summon_wolf", "Summon Wolf",
    school=Schools.SUMMON, level=2, cost=6, cooldown=20, range=3,
    action_cost=75, targeting="ground", icon=9132,
    required_intelligence=5,
    tags=["summon", "minion", "beast"],
    effects=[
        summon("wolf", duration=25),
    ],
    description="""Call a wolf companion to your side.

Wolves are fast and deal good damage, but are fragile."""
)


summon_golem = spell(
    "summon_golem", "Summon Golem",
    school=Schools.SUMMON, level=4, cost=15, cooldown=50, range=3,
    action_cost=100, targeting="ground", icon=9133,
    required_intelligence=15,
    tags=["summon", "minion", "construct", "ultimate"],
    effects=[
        summon("golem", duration=40),
    ],
    description="""Create a powerful stone golem.

Golems are slow but incredibly tough and deal
massive damage."""
)

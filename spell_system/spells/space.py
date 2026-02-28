"""
Space School Spells

Focused on teleportation and movement manipulation.
"""

from old.spell_builder import spell, Schools
from ..effects.builders import (
    damage, message, blink, teleport,
    swap_positions, blink_to_target
)

__all__ = ['blink_spell', 'teleport_spell', 'banish', 'dimensional_swap', 'blink_strike']


blink_spell = spell(
    "blink", "Blink",
    school=Schools.SPACE, level=1, cost=3, cooldown=5, range=5,
    action_cost=25, targeting="ground", icon=9110,
    tags=["space", "movement", "utility"],
    effects=[
        blink(distance=5),
    ],
    description="""Instantly teleport a short distance in any direction.

Great for escaping danger or closing gaps quickly."""
)


teleport_spell = spell(
    "teleport", "Teleport",
    school=Schools.SPACE, level=2, cost=8, cooldown=20, range=0,
    action_cost=50, targeting="self", icon=9111,
    required_intelligence=5,
    tags=["space", "movement", "escape"],
    effects=[
        teleport(target="self"),
    ],
    description="""Teleport yourself to a random location on the current floor.

Useful for escaping dangerous situations, but the
destination is unpredictable."""
)


banish = spell(
    "teleport_other", "Banish",
    school=Schools.SPACE, level=3, cost=12, cooldown=25, range=6,
    action_cost=75, targeting="enemy", icon=9112,
    required_intelligence=10,
    tags=["space", "control", "utility"],
    effects=[
        teleport(target="other"),
        message("{target} is banished to a distant location!"),
    ],
    description="""Teleport an enemy to a random location.

Useful for removing a dangerous foe from combat
or separating enemies."""
)


dimensional_swap = spell(
    "swap", "Dimensional Swap",
    school=Schools.SPACE, level=4, cost=10, cooldown=15, range=8,
    action_cost=50, targeting="enemy", icon=9113,
    required_intelligence=12,
    tags=["space", "movement", "tactical"],
    effects=[
        swap_positions(),
    ],
    description="""Swap positions with any visible creature.

Can be used offensively to reposition enemies
or defensively to escape."""
)


blink_strike = spell(
    "blink_strike", "Blink Strike",
    school=Schools.SPACE, level=2, cost=5, cooldown=8, range=5,
    action_cost=75, targeting="enemy", icon=9114,
    required_intelligence=5,
    tags=["space", "movement", "damage"],
    effects=[
        blink_to_target(),
        damage(15, "physical", scales=False),
    ],
    description="""Teleport directly to a target and strike them.

Combines dimensional magic with a devastating melee
attack in one swift motion."""
)

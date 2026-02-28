"""
Mind School Spells

Focused on control, debuffs, and mental manipulation.
"""

from old.spell_builder import spell, Schools
from ..effects.builders import damage, apply_status, self_buff, message

__all__ = ['lethargy', 'weaken', 'empower', 'petrifying_gaze', 'torment']


lethargy = spell(
    "slow", "Lethargy",  # id stays "slow" for backward compat
    school=Schools.MIND, level=1, cost=4, cooldown=8, range=6,
    action_cost=50, targeting="enemy", icon=9120,
    tags=["mind", "debuff", "control"],
    effects=[
        apply_status("slow", duration=5, amount=50, scales=True),
    ],
    description="""Slow a target's movements and reactions.

The affected creature takes longer to perform all actions."""
)


weaken = spell(
    "weaken", "Weaken",
    school=Schools.MIND, level=2, cost=5, cooldown=10, range=6,
    action_cost=50, targeting="enemy", icon=9121,
    required_intelligence=5,
    tags=["mind", "debuff"],
    effects=[
        apply_status("weak", duration=8, amount=3),
    ],
    description="""Sap the strength from a target.

The affected creature deals reduced physical damage."""
)


empower = spell(
    "empower", "Empower",
    school=Schools.MIND, level=2, cost=6, cooldown=15, range=0,
    action_cost=50, targeting="self", icon=9122,
    required_intelligence=5,
    tags=["mind", "buff"],
    effects=[
        self_buff("might", duration=10, amount=5),
    ],
    description="""Enhance your physical strength through mental focus.

Temporarily increases your strength stat."""
)


petrifying_gaze = spell(
    "petrify", "Petrifying Gaze",
    school=Schools.MIND, level=3, cost=8, cooldown=10, range=4,
    action_cost=75, targeting="enemy", icon=9123,
    required_intelligence=8,
    tags=["mind", "control", "stun"],
    effects=[
        apply_status("stun", duration=3),
        message("{target} is turned to stone!"),
    ],
    description="""Turn a creature to stone temporarily.

The target is completely paralyzed and cannot take any
actions while petrified."""
)


torment = spell(
    "torment", "Torment",
    school=Schools.MIND, level=3, cost=10, cooldown=10, range=5,
    action_cost=100, targeting="enemy", icon=9124,
    required_intelligence=8,
    tags=["mind", "damage", "debuff"],
    effects=[
        damage(10, "psychic", scales=True),
        apply_status("slow", duration=3, amount=50),
    ],
    description="""Inflict mental anguish that damages and slows the target.

The tormented creature suffers damage based on their
current health and becomes sluggish."""
)

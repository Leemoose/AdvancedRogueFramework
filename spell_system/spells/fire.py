"""
Fire School Spells

Focused on direct damage and damage-over-time effects.
"""

from old.spell_builder import spell, Schools
from ..effects.builders import damage, apply_status, aoe_damage, message

__all__ = ['burning_attack', 'fireball', 'burning_circle', 'inferno']


burning_attack = spell(
    "burning_attack", "Burning Attack",
    school=Schools.FIRE, level=1, cost=5, cooldown=10, range=5,
    action_cost=50, targeting="enemy", icon=9102,
    tags=["fire", "damage", "dot"],
    effects=[
        damage(3, "fire", scales=True),
        apply_status("burn", duration=5, damage=3, scales=True),
    ],
    description="""Throw a small bolt of fire at a target that sets the target ablaze.

Deals direct fire damage and applies a burn effect that deals
additional damage each turn."""
)


fireball = spell(
    "fireball", "Fireball",
    school=Schools.FIRE, level=2, cost=10, cooldown=15, range=8,
    action_cost=75, targeting="ground", icon=9103,
    required_intelligence=5,
    tags=["fire", "damage", "aoe"],
    effects=[
        aoe_damage(15, radius=2, center="target", scales=True),
    ],
    description="""Hurl an explosive ball of fire at a location.

Explodes on impact, dealing fire damage to all creatures
in the blast radius."""
)


burning_circle = spell(
    "burning_circle", "Burning Circle",
    school=Schools.FIRE, level=3, cost=8, cooldown=12, range=0,
    action_cost=50, targeting="self", icon=9104,
    required_intelligence=8,
    tags=["fire", "damage", "aoe", "defensive"],
    effects=[
        aoe_damage(10, radius=1, center="caster", include_caster=False, scales=True),
        message("A ring of fire erupts around {caster}!"),
    ],
    description="""Create a ring of fire around yourself.

Damages and burns all adjacent enemies. Does not affect the caster."""
)


inferno = spell(
    "inferno", "Inferno",
    school=Schools.FIRE, level=4, cost=20, cooldown=25, range=10,
    action_cost=100, targeting="ground", icon=9105,
    required_intelligence=15,
    tags=["fire", "damage", "aoe", "ultimate"],
    effects=[
        aoe_damage(25, radius=3, center="target", scales=True),
    ],
    description="""Unleash a massive firestorm at a location.

Deals heavy fire damage in a large area and sets all
targets ablaze with an intense burn."""
)

"""
Necromancy School Spells

Focused on life drain, poison, and dark magic.
"""

from old.spell_builder import spell, Schools
from ..effects.builders import (
    lifesteal, apply_status, self_buff,
    self_damage, restore_mana
)

__all__ = ['sap_vitality', 'poison_touch', 'life_tap', 'dark_pact']


sap_vitality = spell(
    "sap_vitality", "Sap Vitality",
    school=Schools.NECROMANCY, level=1, cost=5, cooldown=5, range=5,
    action_cost=50, targeting="enemy", icon=9102,
    tags=["necromancy", "damage", "heal", "lifesteal"],
    effects=[
        lifesteal(3, scales=True),
    ],
    description="""Drain the life force from a target.

Deals damage to the target and heals the caster for
the same amount."""
)


poison_touch = spell(
    "poison_touch", "Poison Touch",
    school=Schools.NECROMANCY, level=2, cost=4, cooldown=8, range=4,
    action_cost=50, targeting="enemy", icon=9106,
    required_intelligence=3,
    tags=["necromancy", "dot", "poison"],
    effects=[
        apply_status("poison", duration=5, damage=4, scales=True),
    ],
    description="""Infect a target with deadly poison.

The poison deals damage over time and can stack
with itself."""
)


life_tap = spell(
    "life_tap", "Life Tap",
    school=Schools.NECROMANCY, level=2, cost=0, cooldown=10, range=0,
    action_cost=25, targeting="self", icon=9107,
    required_intelligence=5,
    tags=["necromancy", "utility", "self-damage"],
    effects=[
        self_damage(10),
        restore_mana(15),
    ],
    description="""Sacrifice health to restore mana.

Converts a portion of your health into magical energy.
Use with caution."""
)


dark_pact = spell(
    "dark_pact", "Dark Pact",
    school=Schools.NECROMANCY, level=3, cost=10, cooldown=30, range=0,
    action_cost=50, targeting="self", icon=9108,
    required_intelligence=10,
    tags=["necromancy", "buff", "risky"],
    effects=[
        self_buff("berserk", duration=8),
    ],
    description="""Enter a berserk state, gaining immense power at a cost.

Greatly increases combat stats but prevents spellcasting
and applies a penalty when the effect ends."""
)

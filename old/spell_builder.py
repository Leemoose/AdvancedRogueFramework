"""
Spell builder - Pythonic API for defining spells without YAML.

This module provides the `spell` function and `Schools` enum for defining spells
as Python objects that auto-register with the spell registry.

Usage:
    from spell_system.spell_builder import spell, Schools
    from spell_system.effects.builders import damage, apply_status

    burning_attack = spell(
        "burning_attack", "Burning Attack",
        school=Schools.FIRE, level=1, cost=5, cooldown=10, range=5,
        effects=[
            damage(3, "fire", scales=True),
            apply_status("burn", duration=5, damage=3, scales=True),
        ],
        description="Throw a bolt of fire that burns the target."
    )
"""

from enum import Enum
from typing import List, Optional, Union
from old.spell_data import SpellData, EffectData


class Schools(str, Enum):
    """Magic school identifiers."""
    FIRE = "fire"
    MIND = "mind"
    NECROMANCY = "necromancy"
    SPACE = "space"
    SUMMON = "summon"
    GENERAL = "general"


# Global registry of all defined spells
# This is populated when spell modules are imported
_spell_definitions: dict = {}


def spell(
    id: str,
    name: str,
    *,  # Force keyword arguments after this
    school: Union[Schools, str] = Schools.GENERAL,
    level: int = 1,
    cost: int = 5,
    cooldown: int = 5,
    range: int = 5,
    action_cost: int = 50,
    targeting: str = "enemy",
    icon: int = 9100,
    required_intelligence: int = 0,
    tags: Optional[List[str]] = None,
    effects: Optional[List[EffectData]] = None,
    description: str = "",
) -> SpellData:
    """
    Define a spell and register it in the global spell registry.

    This is the primary way to create spells in the Python-based spell system.
    Spells defined with this function are automatically available to the game
    when the spell module is imported.

    Args:
        id: Unique spell identifier (e.g., "burning_attack")
        name: Display name (e.g., "Burning Attack")
        school: Magic school (use Schools enum or string)
        level: Spell level within school (1-4 typically)
        cost: Mana cost
        cooldown: Turns before can cast again
        range: -1 for unlimited, 0 for self, positive for distance
        action_cost: Energy/AP cost (usually 25-100)
        targeting: "self", "enemy", "ally", "ground", "direction"
        icon: Render tag for UI
        required_intelligence: Minimum INT to learn
        tags: List of tags (e.g., ["fire", "damage", "dot"])
        effects: List of EffectData from effect builders
        description: Full description text

    Returns:
        SpellData object (also stored in global registry)

    Example:
        burning_attack = spell(
            "burning_attack", "Burning Attack",
            school=Schools.FIRE, level=1, cost=5, cooldown=10, range=5,
            effects=[
                damage(3, "fire", scales=True),
                apply_status("burn", duration=5, damage=3, scales=True),
            ],
            description="Throw a bolt of fire that burns the target."
        )
    """
    # Convert school enum to string if needed
    school_str = school.value if isinstance(school, Schools) else school

    # Build effects tuple
    effects_tuple = tuple(effects) if effects else ()

    # Build tags tuple
    tags_tuple = tuple(tags) if tags else ()

    # Create SpellData
    spell_data = SpellData(
        id=id,
        name=name,
        school=school_str,
        description=description,
        cost=cost,
        cooldown=cooldown,
        range=range,
        action_cost=action_cost,
        targeting=targeting,
        icon=icon,
        effects=effects_tuple,
        level=level,
        required_intelligence=required_intelligence,
        tags=tags_tuple,
    )

    # Register globally
    _spell_definitions[id] = spell_data

    return spell_data


def get_all_spell_definitions() -> dict:
    """Get all registered spell definitions."""
    return _spell_definitions.copy()


def get_spell_definition(spell_id: str) -> Optional[SpellData]:
    """Get a specific spell definition by ID."""
    return _spell_definitions.get(spell_id)


def get_spells_by_school(school: Union[Schools, str]) -> List[SpellData]:
    """Get all spells in a school, sorted by level."""
    school_str = school.value if isinstance(school, Schools) else school
    spells = [s for s in _spell_definitions.values() if s.school == school_str]
    return sorted(spells, key=lambda s: s.level)


def clear_spell_definitions():
    """Clear all registered spells. Mainly for testing."""
    _spell_definitions.clear()

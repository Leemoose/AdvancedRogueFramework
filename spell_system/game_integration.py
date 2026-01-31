"""
Game integration module for the spell system.

This module handles initialization and provides convenience functions
for integrating the spell system with the rest of the game.
"""

import os
from .spell_registry import SpellRegistry, get_registry
from .spell import Spell
from logging_config import get_logger

logger = get_logger(__name__)


def initialize_spell_system(spells_dir: str = None):
    """
    Initialize the spell system by loading all spell data.

    Should be called once at game start.

    Args:
        spells_dir: Path to directory containing spell YAML files.
                   Defaults to spell_system/data/
    """
    if spells_dir is None:
        # Default to data/ directory relative to this module
        module_dir = os.path.dirname(os.path.abspath(__file__))
        spells_dir = os.path.join(module_dir, 'data')

    registry = get_registry()
    registry.load_spells(spells_dir)

    logger.info(f"Spell system initialized with {len(registry.get_all_spells())} spells")
    logger.info(f"Schools: {registry.get_all_schools()}")

    return registry


def give_spell(entity, spell_id: str, **overrides) -> bool:
    """
    Give a spell to an entity (player or monster).

    Args:
        entity: The entity to give the spell to (must have .mage attribute)
        spell_id: ID of the spell to give
        **overrides: Optional overrides for spell properties (cost, cooldown, range, etc.)

    Returns:
        True if spell was successfully added
    """
    registry = get_registry()
    spell = registry.create_spell(spell_id, entity, **overrides)

    if spell is None:
        logger.warning(f"Could not create spell: {spell_id}")
        return False

    entity.mage.add_spell(spell)
    logger.debug(f"Gave spell {spell_id} to {entity.name}")
    return True


def give_school_spells(entity, school: str, max_level: int = None):
    """
    Give all spells from a school up to a certain level.

    Args:
        entity: The entity to give spells to
        school: The magic school name
        max_level: Maximum spell level to give (None = all levels)
    """
    registry = get_registry()
    spells = registry.get_spells_by_school(school)

    for spell_data in spells:
        if max_level is None or spell_data.level <= max_level:
            give_spell(entity, spell_data.id)


def get_starter_spells() -> list:
    """
    Get a list of starter spell IDs for new players.

    Returns:
        List of spell IDs suitable for starting characters
    """
    return ['burning_attack', 'sap_vitality']


def give_starter_spells(entity):
    """Give the standard starter spells to an entity."""
    for spell_id in get_starter_spells():
        give_spell(entity, spell_id)


# Compatibility layer: Create old-style spell from new system
class LegacySpellWrapper:
    """
    Wraps the new Spell class to provide backward compatibility
    with code expecting the old Spell interface.

    This allows gradual migration of the codebase.
    """

    def __init__(self, new_spell: Spell):
        self._spell = new_spell

    def __getattr__(self, name):
        # Delegate to the new spell
        return getattr(self._spell, name)

    @property
    def parent(self):
        """Old code uses .parent, new code uses .caster."""
        return self._spell.caster

    @property
    def required_intelligence(self):
        return self._spell.data.required_intelligence

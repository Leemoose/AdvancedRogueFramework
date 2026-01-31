"""
School - base class for spell schools.

Spell schools group related spells and can be learned from books.
The actual spell definitions are in data/*.yaml files.
"""

from logging_config import get_logger

logger = get_logger(__name__)


class School:
    """Base class for spell schools (fire, necromancy, etc.)."""

    def __init__(self, name: str):
        self.name = name

    def get_spells(self):
        """Get all spells in this school from the registry."""
        from .spell_registry import get_registry
        return get_registry().get_spells_by_school(self.name)

    def get_spell_at_level(self, level: int):
        """Get the spell at a specific level."""
        from .spell_registry import get_registry
        return get_registry().get_spell_by_school_level(self.name, level)

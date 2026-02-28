"""
ClassSpellRegistry - Registry for the class-based spell system.

Manages spell class registration and instantiation for casters.
Works alongside the existing SpellRegistry for backward compatibility.
"""

from typing import Dict, List, Optional, Type
from .base_spell import BaseSpell
from logging_config import get_logger

logger = get_logger(__name__)


class ClassSpellRegistry:
    """
    Central registry for class-based spell definitions.

    Usage:
        # At game start
        registry = ClassSpellRegistry()
        registry.load_spells()

        # When player learns a spell
        spell = registry.create_spell('burning_attack', player)
        player.mage.add_spell(spell)
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern - only one registry exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._spell_classes: Dict[str, Type[BaseSpell]] = {}
        self._schools: Dict[str, List[str]] = {}  # school -> list of spell ids
        self._initialized = True

    def load_spells(self):
        """Load all spell classes from the class_spells package."""
        from . import class_spells

        # Get all spell classes from the package
        for name in dir(class_spells):
            obj = getattr(class_spells, name)
            if isinstance(obj, type) and issubclass(obj, BaseSpell) and obj is not BaseSpell:
                self.register_spell(obj)

        logger.info(f"Loaded {len(self._spell_classes)} class-based spells")

    def register_spell(self, spell_class: Type[BaseSpell]):
        """
        Register a spell class in the registry.

        Args:
            spell_class: A class that inherits from BaseSpell
        """
        # Generate ID from class name (e.g., BurningAttack -> burning_attack)
        spell_id = self._class_to_id(spell_class)

        self._spell_classes[spell_id] = spell_class

        # Track by school
        school = getattr(spell_class, 'school', 'general')
        if school not in self._schools:
            self._schools[school] = []
        if spell_id not in self._schools[school]:
            self._schools[school].append(spell_id)

        logger.debug(f"Registered spell class: {spell_id} ({school})")

    def _class_to_id(self, spell_class: Type[BaseSpell]) -> str:
        """Convert class name to spell ID (CamelCase to snake_case)."""
        name = spell_class.__name__
        # Convert CamelCase to snake_case
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)

    # ---- Lookup methods ----

    def get_spell_class(self, spell_id: str) -> Optional[Type[BaseSpell]]:
        """Get spell class by ID."""
        return self._spell_classes.get(spell_id)

    def create_spell(self, spell_id: str, caster) -> Optional[BaseSpell]:
        """
        Create a spell instance for a caster.

        Args:
            spell_id: The spell ID (e.g., 'burning_attack')
            caster: The entity that will own the spell

        Returns:
            Spell instance or None if spell not found
        """
        spell_class = self.get_spell_class(spell_id)
        if spell_class is None:
            logger.warning(f"Unknown spell: {spell_id}")
            return None

        return spell_class(caster)

    def get_spells_by_school(self, school: str) -> List[Type[BaseSpell]]:
        """Get all spell classes in a school."""
        spell_ids = self._schools.get(school, [])
        return [self._spell_classes[sid] for sid in spell_ids]

    def get_all_schools(self) -> List[str]:
        """Get list of all magic schools."""
        return list(self._schools.keys())

    def get_all_spell_ids(self) -> List[str]:
        """Get all registered spell IDs."""
        return list(self._spell_classes.keys())

    def get_all_spell_classes(self) -> List[Type[BaseSpell]]:
        """Get all registered spell classes."""
        return list(self._spell_classes.values())

    def get_learnable_spells(self, intelligence: int) -> List[Type[BaseSpell]]:
        """Get all spell classes the entity can learn based on intelligence."""
        return [
            s for s in self._spell_classes.values()
            if getattr(s, 'required_intelligence', 0) <= intelligence
        ]

    # ---- Utility ----

    def clear(self):
        """Clear all registered spells (for testing)."""
        self._spell_classes.clear()
        self._schools.clear()


# Convenience function
def get_class_registry() -> ClassSpellRegistry:
    """Get the global class-based spell registry instance."""
    return ClassSpellRegistry()

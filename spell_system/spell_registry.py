"""
SpellRegistry - central registry for all spell definitions.

Loads spell data from Python modules and provides lookup methods.
This is a singleton that should be initialized once at game start.
"""

from typing import Dict, List, Optional
from old.spell_data import SpellData
from old.spell import Spell
from logging_config import get_logger

logger = get_logger(__name__)


class SpellRegistry:
    """
    Central registry for all spell definitions.

    Usage:
        # At game start
        registry = SpellRegistry()
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
        self._spells: Dict[str, SpellData] = {}
        self._schools: Dict[str, List[str]] = {}  # school -> list of spell ids
        self._initialized = True

    def load_spells(self, spells_dir: str = None):
        """
        Load all spell definitions from Python modules.

        The spells_dir parameter is kept for backward compatibility but is ignored.
        Spells are now loaded from the spell_system.spells package.
        """
        # Import the spells package, which triggers spell registration
        from . import spells  # noqa: F401
        from old.spell_builder import get_all_spell_definitions

        # Get all spells that were registered via the spell() function
        spell_defs = get_all_spell_definitions()

        for spell_id, spell_data in spell_defs.items():
            self._register_spell(spell_data)

        logger.info(f"Loaded {len(self._spells)} spells from Python modules")

    def _register_spell(self, spell: SpellData):
        """Register a spell in the registry."""
        self._spells[spell.id] = spell

        # Track by school
        if spell.school not in self._schools:
            self._schools[spell.school] = []
        if spell.id not in self._schools[spell.school]:
            self._schools[spell.school].append(spell.id)

        logger.debug(f"Registered spell: {spell.id} ({spell.school})")

    # ---- Lookup methods ----

    def get_spell_data(self, spell_id: str) -> Optional[SpellData]:
        """Get spell data by ID."""
        return self._spells.get(spell_id)

    def create_spell(self, spell_id: str, caster, **overrides) -> Optional[Spell]:
        """
        Create a spell instance for a caster.

        Args:
            spell_id: The spell ID to create
            caster: The entity that will own the spell
            **overrides: Optional overrides for spell properties (cost, cooldown, etc.)
        """
        spell_data = self.get_spell_data(spell_id)
        if spell_data is None:
            logger.warning(f"Unknown spell: {spell_id}")
            return None

        if overrides:
            spell_data = self._apply_overrides(spell_data, overrides)

        return Spell(caster, spell_data)

    def _apply_overrides(self, spell_data: SpellData, overrides: dict) -> SpellData:
        """Create a new SpellData with overridden values.

        Special key 'effects_overrides' can be a list of dicts to override
        effect parameters by index. Example:
            effects_overrides=[{'amount': 10}, {'damage': 5}]
        """
        from old.spell_data import EffectData

        effects_overrides = overrides.pop('effects_overrides', None)

        # Build new effects tuple if overrides provided
        effects = spell_data.effects
        if effects_overrides:
            new_effects = []
            for i, effect in enumerate(effects):
                if i < len(effects_overrides) and effects_overrides[i]:
                    # Merge override params with existing
                    new_params = dict(effect.params)
                    new_params.update(effects_overrides[i])
                    new_effects.append(EffectData(type=effect.type, params=new_params))
                else:
                    new_effects.append(effect)
            effects = tuple(new_effects)

        current = {
            'id': spell_data.id,
            'name': spell_data.name,
            'school': spell_data.school,
            'description': spell_data.description,
            'cost': spell_data.cost,
            'cooldown': spell_data.cooldown,
            'range': spell_data.range,
            'action_cost': spell_data.action_cost,
            'targeting': spell_data.targeting,
            'icon': spell_data.icon,
            'effects': effects,
            'level': spell_data.level,
            'required_intelligence': spell_data.required_intelligence,
            'tags': spell_data.tags,
        }

        for key, value in overrides.items():
            if key in current:
                current[key] = value

        return SpellData(**current)

    def get_spells_by_school(self, school: str) -> List[SpellData]:
        """Get all spells in a school."""
        spell_ids = self._schools.get(school, [])
        return [self._spells[sid] for sid in spell_ids]

    def get_spell_by_school_level(self, school: str, level: int) -> Optional[SpellData]:
        """Get the spell at a specific level in a school."""
        for spell in self.get_spells_by_school(school):
            if spell.level == level:
                return spell
        return None

    def get_all_schools(self) -> List[str]:
        """Get list of all magic schools."""
        return list(self._schools.keys())

    def get_all_spells(self) -> List[SpellData]:
        """Get all registered spells."""
        return list(self._spells.values())

    def get_learnable_spells(self, intelligence: int) -> List[SpellData]:
        """Get all spells the entity can learn based on intelligence."""
        return [s for s in self._spells.values() if s.required_intelligence <= intelligence]

    # ---- Utility ----

    def clear(self):
        """Clear all registered spells (for testing)."""
        self._spells.clear()
        self._schools.clear()


# Convenience function
def get_registry() -> SpellRegistry:
    """Get the global spell registry instance."""
    return SpellRegistry()

"""
SpellData - immutable spell definitions loaded from YAML files.

This separates the spell template (what the spell IS) from the spell instance
(a spell owned by a specific caster with cooldown state).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class EffectData:
    """
    Immutable definition of a single spell effect.

    Effects are the building blocks of spells. Each effect has a type
    (damage, heal, apply_status, etc.) and parameters specific to that type.
    """
    type: str  # e.g., "damage", "heal", "apply_status", "lifesteal"
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EffectData':
        """Create an EffectData from a dictionary (YAML parsing)."""
        effect_type = data.get('type', 'unknown')
        params = {k: v for k, v in data.items() if k != 'type'}
        return cls(type=effect_type, params=params)


@dataclass(frozen=True)
class SpellData:
    """
    Immutable spell definition loaded from YAML.

    This is the template that defines what a spell does. Actual spell
    instances are created by binding this data to a caster.
    """
    id: str                          # Unique identifier, e.g., "burning_attack"
    name: str                        # Display name, e.g., "Burning Attack"
    school: str                      # Magic school, e.g., "fire", "necromancy"
    description: str                 # Full description text
    cost: int                        # Mana cost
    cooldown: int                    # Turns before can cast again
    range: int                       # -1 for unlimited, 0 for self, positive for distance
    action_cost: int                 # Energy/AP cost (usually 50-100)
    targeting: str                   # "self", "enemy", "ally", "ground", "direction"
    icon: int                        # Render tag for UI
    effects: tuple                   # Tuple of EffectData (immutable)
    level: int = 1                   # Spell level within school
    required_intelligence: int = 0   # Minimum INT to learn
    tags: tuple = field(default_factory=tuple)  # e.g., ("fire", "damage", "dot")

    @classmethod
    def from_dict(cls, spell_id: str, data: Dict[str, Any]) -> 'SpellData':
        """Create a SpellData from a dictionary (YAML parsing)."""
        # Parse effects list into EffectData objects
        effects_raw = data.get('../spell_system/effects', [])
        effects = tuple(EffectData.from_dict(e) for e in effects_raw)

        # Parse tags
        tags = tuple(data.get('tags', []))

        return cls(
            id=spell_id,
            name=data.get('name', spell_id.replace('_', ' ').title()),
            school=data.get('school', 'general'),
            description=data.get('description', ''),
            cost=data.get('cost', 5),
            cooldown=data.get('cooldown', 5),
            range=data.get('range', 5),
            action_cost=data.get('action_cost', 50),
            targeting=data.get('../spell_system/targeting', 'enemy'),
            icon=data.get('icon', 9100),
            effects=effects,
            level=data.get('level', 1),
            required_intelligence=data.get('required_intelligence', 0),
            tags=tags
        )

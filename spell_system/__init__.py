# Spell system - Python-based spells with composable effect building blocks

from old.spell import Spell, SpellContext
from old.spell_data import SpellData, EffectData
from .spell_registry import SpellRegistry, get_registry
from old.spell_builder import spell, Schools, get_all_spell_definitions
from .school import School
from .effects import EffectFactory
from .effects.builders import (
    damage, heal, lifesteal, apply_status, self_buff, message, custom,
    aoe_damage, teleport, blink, swap_positions, blink_to_target,
    summon, restore_mana, self_damage,
)
from .status_effects import StatusEffectFactory
from old.game_integration import (
    initialize_spell_system,
    give_spell,
    give_school_spells,
    give_starter_spells,
    get_starter_spells,
)

__all__ = [
    # Core classes
    'Spell',
    'SpellContext',
    'SpellData',
    'EffectData',
    'SpellRegistry',
    'get_registry',
    'School',
    'Schools',
    'EffectFactory',
    'StatusEffectFactory',
    # Spell builder
    'spell',
    'get_all_spell_definitions',
    # Effect builders
    'damage',
    'heal',
    'lifesteal',
    'apply_status',
    'self_buff',
    'message',
    'custom',
    'aoe_damage',
    'teleport',
    'blink',
    'swap_positions',
    'blink_to_target',
    'summon',
    'restore_mana',
    'self_damage',
    # Game integration
    'initialize_spell_system',
    'give_spell',
    'give_school_spells',
    'give_starter_spells',
    'get_starter_spells',
]

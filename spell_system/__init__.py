# Spell system - data-driven spells with composable effects

from .spell import Spell, SpellContext
from .spell_data import SpellData, EffectData
from .spell_registry import SpellRegistry, get_registry
from .school import School
from .effects import EffectFactory
from .status_effects import StatusEffectFactory
from .game_integration import (
    initialize_spell_system,
    give_spell,
    give_school_spells,
    give_starter_spells,
    get_starter_spells,
)

__all__ = [
    'Spell',
    'SpellContext',
    'SpellData',
    'EffectData',
    'SpellRegistry',
    'get_registry',
    'School',
    'EffectFactory',
    'StatusEffectFactory',
    'initialize_spell_system',
    'give_spell',
    'give_school_spells',
    'give_starter_spells',
    'get_starter_spells',
]

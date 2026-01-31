"""
BaseEffect - abstract base class for all spell effects.

Effects are the building blocks of spells. Each effect does one thing:
damage, heal, apply status, teleport, summon, etc.

To create a new effect type:
1. Create a class that inherits from BaseEffect
2. Implement the execute() method
3. Register it in EffectFactory
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseEffect(ABC):
    """
    Abstract base class for spell effects.

    Effects receive parameters from the spell data and a context
    containing the caster, target, and game state.
    """

    def __init__(self, params: Dict[str, Any]):
        """
        Initialize the effect with parameters from spell data.

        Args:
            params: Dictionary of effect-specific parameters
        """
        self.params = params

    @abstractmethod
    def execute(self, context) -> bool:
        """
        Execute the effect.

        Args:
            context: SpellContext with caster, target, loop, etc.

        Returns:
            True if effect executed successfully
        """
        pass

    def get_param(self, key: str, default=None):
        """Get a parameter value with optional default."""
        return self.params.get(key, default)

    def get_scaled_value(self, key: str, context, default: int = 0) -> int:
        """
        Get a parameter value scaled by caster's intelligence.

        If the param ends with '_scales', the value is added to the
        caster's skill_damage_increase (for damage) or skill_duration_increase.
        """
        base = self.get_param(key, default)
        scales = self.get_param('scales_with_intelligence', False)

        if scales and 'damage' in key:
            return base + context.get_skill_damage_bonus()
        elif scales and 'duration' in key:
            return base + context.get_skill_duration_bonus()

        return base

"""
Base effect class for the class-based spell system.

Effects are instantiated with their parameters and apply() is called
with a target and context. This differs from the old system where
effects were created from dictionaries.
"""

from abc import ABC, abstractmethod
from typing import Any
from logging_config import get_logger

logger = get_logger(__name__)


class Effect(ABC):
    """
    Abstract base class for spell effects.

    Effects are instantiated with their base parameters at spell definition time,
    then apply() is called at cast time with the target and context.

    Example:
        effect = DamageEffect(base=10, damage_type="fire")
        effect.apply(target_entity, context)
    """

    @abstractmethod
    def apply(self, target: Any, context) -> bool:
        """
        Apply this effect to a target.

        Args:
            target: The target - can be an entity or a position tuple (x, y)
                    depending on the effect type
            context: SpellContext with caster, loop, and helper methods

        Returns:
            True if effect applied successfully, False otherwise
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"

"""
ApplyStatusEffect - applies a status effect to a target entity.
"""

from typing import Type
from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)


class ApplyStatusEffect(Effect):
    """
    Apply a status effect to a target entity.

    Args:
        status_class: The status effect class to instantiate (e.g., Burn, Slow)
        duration: Base duration in turns
        scales_duration: Whether duration scales with caster's intelligence
        scales_damage: Whether damage (if applicable) scales with caster's intelligence
        **kwargs: Additional arguments passed to the status effect constructor
    """

    def __init__(
        self,
        status_class: Type,
        duration: int,
        scales_duration: bool = True,
        scales_damage: bool = True,
        **kwargs
    ):
        self.status_class = status_class
        self.duration = duration
        self.scales_duration = scales_duration
        self.scales_damage = scales_damage
        self.kwargs = kwargs

    def apply(self, target, context) -> bool:
        """Apply the status effect to target entity."""
        if target is None:
            logger.warning("ApplyStatusEffect: No target provided")
            return False

        if not hasattr(target, 'character'):
            logger.warning(f"ApplyStatusEffect: Target {target} has no character component")
            return False

        # Calculate scaled duration
        duration = self.duration
        if self.scales_duration:
            duration += context.get_skill_duration_bonus()

        # Build kwargs for status effect
        effect_kwargs = self.kwargs.copy()

        # Scale damage if applicable
        if self.scales_damage and 'damage' in effect_kwargs:
            effect_kwargs['damage'] += context.get_skill_damage_bonus()

        # Create the status effect instance
        try:
            # Most status effects take (duration, ...) or (inflictor, duration, ...)
            # We'll try to be flexible here
            effect = self._create_status_effect(duration, context.caster, effect_kwargs)
            target.character.add_status_effect(effect)
            logger.debug(f"ApplyStatusEffect: Applied {self.status_class.__name__} to {target.name}")
            return True
        except Exception as e:
            logger.error(f"ApplyStatusEffect: Failed to create {self.status_class.__name__}: {e}")
            return False

    def _create_status_effect(self, duration: int, inflictor, kwargs: dict):
        """
        Create the status effect instance, handling various constructor signatures.
        """
        # Try common signatures
        try:
            # Signature: (duration, damage, inflictor) - e.g., Burn
            if 'damage' in kwargs:
                return self.status_class(duration, kwargs['damage'], inflictor)
        except TypeError:
            pass

        try:
            # Signature: (inflictor, duration, damage) - e.g., Poison
            if 'damage' in kwargs:
                return self.status_class(inflictor, duration, kwargs['damage'])
        except TypeError:
            pass

        try:
            # Signature: (inflictor, duration) - e.g., Slow, Root
            return self.status_class(inflictor, duration)
        except TypeError:
            pass

        try:
            # Signature: (duration, amount) - e.g., Might, Weak
            if 'amount' in kwargs:
                return self.status_class(duration, kwargs['amount'])
        except TypeError:
            pass

        try:
            # Signature: (duration) - e.g., Stun, Invincible
            return self.status_class(duration)
        except TypeError:
            pass

        # Fallback: pass everything as kwargs
        return self.status_class(duration=duration, inflictor=inflictor, **kwargs)

    def __repr__(self):
        return f"ApplyStatusEffect({self.status_class.__name__}, duration={self.duration})"

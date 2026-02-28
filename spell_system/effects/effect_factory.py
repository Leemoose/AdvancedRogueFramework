"""
EffectFactory - creates effect instances from effect data.

This is the central place where effect types are registered and created.
To add a new effect type, add it to the EFFECT_TYPES dictionary.
"""

from typing import Dict, Type, Optional
from .base_effect import BaseEffect
from old.spell_data import EffectData
from logging_config import get_logger

logger = get_logger(__name__)


class EffectFactory:
    """
    Factory for creating spell effects from data.

    Usage:
        effect_data = EffectData(type='damage', params={'amount': 10})
        effect = EffectFactory.create(effect_data, context)
        effect.execute(context)
    """

    # Registry of effect types
    # Maps effect type string -> effect class
    _effect_types: Dict[str, Type[BaseEffect]] = {}

    @classmethod
    def register(cls, effect_type: str, effect_class: Type[BaseEffect]):
        """Register an effect type."""
        cls._effect_types[effect_type] = effect_class
        logger.debug(f"Registered effect type: {effect_type}")

    @classmethod
    def create(cls, effect_data: EffectData, context) -> Optional[BaseEffect]:
        """
        Create an effect instance from effect data.

        Args:
            effect_data: EffectData with type and params
            context: SpellContext (used for validation)

        Returns:
            BaseEffect instance or None if type unknown
        """
        effect_class = cls._effect_types.get(effect_data.type)

        if effect_class is None:
            logger.warning(f"Unknown effect type: {effect_data.type}")
            return None

        return effect_class(effect_data.params)

    @classmethod
    def get_registered_types(cls) -> list:
        """Get list of all registered effect types."""
        return list(cls._effect_types.keys())


# ============================================================
# Built-in Effect Implementations
# ============================================================

class DamageEffect(BaseEffect):
    """
    Deal direct damage to target.

    Params:
        amount: Base damage amount
        damage_type: Type of damage (fire, ice, physical, etc.)
        scales_with_intelligence: If True, add skill_damage_bonus
    """

    def execute(self, context) -> bool:
        if context.target is None:
            return False

        amount = self.get_scaled_value('amount', context, 0)
        damage_type = self.get_param('damage_type', 'magical')

        context.target.character.take_damage(context.caster, amount)
        logger.debug(f"{context.caster.name} deals {amount} {damage_type} damage to {context.target.name}")
        return True


class HealEffect(BaseEffect):
    """
    Heal the caster or target.

    Params:
        amount: Base heal amount
        target: "self" or "target" (default: "self")
        scales_with_intelligence: If True, add skill_damage_bonus
    """

    def execute(self, context) -> bool:
        amount = self.get_scaled_value('amount', context, 0)
        heal_target = self.get_param('target', 'self')

        if heal_target == 'self':
            entity = context.caster
        else:
            entity = context.target
            if entity is None:
                return False

        entity.character.change_health(amount)
        logger.debug(f"{entity.name} heals for {amount}")
        return True


class LifestealEffect(BaseEffect):
    """
    Deal damage and heal for the same amount.

    Params:
        amount: Base damage/heal amount
        scales_with_intelligence: If True, add skill_damage_bonus
    """

    def execute(self, context) -> bool:
        if context.target is None:
            return False

        amount = self.get_scaled_value('amount', context, 0)

        # Deal damage
        context.target.character.take_damage(context.caster, amount)
        # Heal caster
        context.caster.character.change_health(amount)

        logger.debug(f"{context.caster.name} drains {amount} life from {context.target.name}")
        return True


class ApplyStatusEffect(BaseEffect):
    """
    Apply a status effect to the target.

    Params:
        status: Status effect type (burn, poison, slow, etc.)
        duration: Effect duration in turns
        damage: Per-tick damage (for DoT effects)
        scales_with_intelligence: If True, scale duration/damage
    """

    def execute(self, context) -> bool:
        if context.target is None:
            return False

        status_type = self.get_param('status')
        duration = self.get_scaled_value('duration', context, 5)
        damage = self.get_scaled_value('damage', context, 0)

        # Import here to avoid circular imports
        from ..status_effects import StatusEffectFactory

        effect = StatusEffectFactory.create(
            status_type,
            duration=duration,
            damage=damage,
            inflictor=context.caster
        )

        if effect:
            context.target.character.status.add_status_effect(effect)
            logger.debug(f"Applied {status_type} to {context.target.name} for {duration} turns")
            return True

        return False


class SelfBuffEffect(BaseEffect):
    """
    Apply a status effect to the caster.

    Params:
        status: Status effect type
        duration: Effect duration
        amount: Buff amount (stat increase)
    """

    def execute(self, context) -> bool:
        status_type = self.get_param('status')
        duration = self.get_scaled_value('duration', context, 5)
        amount = self.get_param('amount', 0)

        from ..status_effects import StatusEffectFactory

        effect = StatusEffectFactory.create(
            status_type,
            duration=duration,
            amount=amount,
            inflictor=context.caster
        )

        if effect:
            context.caster.character.status.add_status_effect(effect)
            logger.debug(f"Applied {status_type} buff to {context.caster.name}")
            return True

        return False


class MessageEffect(BaseEffect):
    """
    Display a message in the game log.

    Params:
        message: The message template (can use {caster}, {target})
    """

    def execute(self, context) -> bool:
        message = self.get_param('message', '')

        # Simple template substitution
        message = message.replace('{caster}', context.caster.name)
        if context.target:
            message = message.replace('{target}', context.target.name)

        context.add_message(message)
        return True


class CustomEffect(BaseEffect):
    """
    Execute a custom Python function.

    This is the escape hatch for effects that can't be built from
    composable parts. Use sparingly!

    Params:
        handler: Name of the handler function in custom_handlers.py
    """

    def execute(self, context) -> bool:
        handler_name = self.get_param('handler')
        if not handler_name:
            return False

        from . import custom_handlers
        handler = getattr(custom_handlers, handler_name, None)

        if handler is None:
            logger.warning(f"Unknown custom handler: {handler_name}")
            return False

        return handler(context, self.params)


# ============================================================
# Register all built-in effects
# ============================================================

EffectFactory.register('damage', DamageEffect)
EffectFactory.register('heal', HealEffect)
EffectFactory.register('lifesteal', LifestealEffect)
EffectFactory.register('apply_status', ApplyStatusEffect)
EffectFactory.register('self_buff', SelfBuffEffect)
EffectFactory.register('message', MessageEffect)
EffectFactory.register('custom', CustomEffect)

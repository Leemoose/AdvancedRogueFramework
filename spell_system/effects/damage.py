"""
Damage effect - deals damage to a target entity.
"""

from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)


class DamageEffect(Effect):
    """
    Deal damage to a target entity.

    Args:
        base: Base damage amount
        damage_type: Type of damage (fire, ice, physical, etc.) - for future use
        scales: Whether damage scales with caster's intelligence
    """

    def __init__(self, base: int, damage_type: str = "physical", scales: bool = True):
        self.base = base
        self.damage_type = damage_type
        self.scales = scales

    def apply(self, target, context) -> bool:
        """Apply damage to target entity."""
        if target is None:
            logger.warning("DamageEffect: No target provided")
            return False

        if not hasattr(target, 'character'):
            logger.warning(f"DamageEffect: Target {target} has no character component")
            return False

        damage = self.base
        if self.scales:
            damage += context.get_skill_damage_bonus()

        target.character.take_damage(context.caster, damage)
        logger.debug(f"DamageEffect: Dealt {damage} {self.damage_type} damage to {target.name}")

        return True

    def __repr__(self):
        return f"DamageEffect(base={self.base}, type={self.damage_type}, scales={self.scales})"

"""
Heal effect - restores health to a target entity.
"""

from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)


class HealEffect(Effect):
    """
    Restore health to a target entity.

    Args:
        base: Base heal amount
        scales: Whether healing scales with caster's intelligence
    """

    def __init__(self, base: int, scales: bool = True):
        self.base = base
        self.scales = scales

    def apply(self, target, context) -> bool:
        """Apply healing to target entity."""
        if target is None:
            logger.warning("HealEffect: No target provided")
            return False

        if not hasattr(target, 'character'):
            logger.warning(f"HealEffect: Target {target} has no character component")
            return False

        amount = self.base
        if self.scales:
            amount += context.get_skill_damage_bonus()  # Use same scaling as damage

        target.character.heal(amount)
        logger.debug(f"HealEffect: Healed {target.name} for {amount}")
        context.add_message(f"{target.name} is healed for {amount}!")

        return True

    def __repr__(self):
        return f"HealEffect(base={self.base}, scales={self.scales})"

"""
Mana-related effects - restore or drain mana.
"""

from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)


class RestoreManaEffect(Effect):
    """
    Restore mana to a target entity.

    Args:
        base: Base mana amount to restore
        scales: Whether amount scales with caster's intelligence
    """

    def __init__(self, base: int, scales: bool = False):
        self.base = base
        self.scales = scales

    def apply(self, target, context) -> bool:
        """Restore mana to target entity."""
        if target is None:
            logger.warning("RestoreManaEffect: No target provided")
            return False

        if not hasattr(target, 'character'):
            logger.warning(f"RestoreManaEffect: Target {target} has no character component")
            return False

        amount = self.base
        if self.scales:
            amount += context.get_skill_damage_bonus()

        target.character.change_mana(amount)
        logger.debug(f"RestoreManaEffect: Restored {amount} mana to {target.name}")
        context.add_message(f"{target.name} restores {amount} mana!")

        return True

    def __repr__(self):
        return f"RestoreManaEffect(base={self.base}, scales={self.scales})"


class DrainManaEffect(Effect):
    """
    Drain mana from a target entity.

    Args:
        base: Base mana amount to drain
        scales: Whether amount scales with caster's intelligence
        transfer_to_caster: Whether drained mana goes to the caster
    """

    def __init__(self, base: int, scales: bool = True, transfer_to_caster: bool = False):
        self.base = base
        self.scales = scales
        self.transfer_to_caster = transfer_to_caster

    def apply(self, target, context) -> bool:
        """Drain mana from target entity."""
        if target is None:
            logger.warning("DrainManaEffect: No target provided")
            return False

        if not hasattr(target, 'character'):
            logger.warning(f"DrainManaEffect: Target {target} has no character component")
            return False

        amount = self.base
        if self.scales:
            amount += context.get_skill_damage_bonus()

        # Don't drain more than target has
        actual_drain = min(amount, target.character.mana)
        target.character.change_mana(-actual_drain)

        if self.transfer_to_caster and actual_drain > 0:
            context.caster.character.change_mana(actual_drain)
            context.add_message(f"Drained {actual_drain} mana from {target.name}!")
        else:
            context.add_message(f"{target.name} loses {actual_drain} mana!")

        logger.debug(f"DrainManaEffect: Drained {actual_drain} mana from {target.name}")
        return True

    def __repr__(self):
        return f"DrainManaEffect(base={self.base}, transfer={self.transfer_to_caster})"

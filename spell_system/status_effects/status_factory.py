"""
StatusEffectFactory - creates status effects by type.

Provides a clean API for creating status effects by name,
used by the spell effect system.
"""

from typing import Optional
from logging_config import get_logger

from .base import StatusEffect
from .burn import Burn
from .poison import Poison
from .slow import Slow
from .might import Might
from .berserk import Berserk
from .weak import Weak
from .haste import Haste
from .fear import Fear
from .charm import Charm
from .root import Root
from .bleed import Bleed
from .stun import Stun
from .invincible import Invincible
from .sleep import Sleep

logger = get_logger(__name__)


# Creator functions for each status effect type
def _create_burn(duration: int = 5, damage: int = 3, inflictor=None, **_) -> Burn:
    return Burn(duration, damage, inflictor)


def _create_poison(duration: int = 2, damage: int = 3, inflictor=None, **_) -> Poison:
    return Poison(inflictor, duration, damage)


def _create_slow(duration: int = 5, inflictor=None, **_) -> Slow:
    return Slow(inflictor, duration)


def _create_might(duration: int = 10, amount: int = 5, **_) -> Might:
    return Might(duration, amount)


def _create_berserk(duration: int = 10, **_) -> Berserk:
    return Berserk(duration)


def _create_weak(duration: int = 10, amount: int = 3, **_) -> Weak:
    return Weak(duration, amount)


def _create_haste(duration: int = 10, amount: int = 3, **_) -> Haste:
    return Haste(duration, amount)


def _create_fear(duration: int = 5, inflictor=None, **_) -> Fear:
    return Fear(duration, inflictor)


def _create_charm(duration: int = 10, inflictor=None, **_) -> Charm:
    return Charm(duration, inflictor)


def _create_root(duration: int = 5, inflictor=None, **_) -> Root:
    return Root(inflictor, duration)


def _create_bleed(duration: int = 5, damage: int = 2, inflictor=None, **_) -> Bleed:
    return Bleed(duration, damage, inflictor)


def _create_stun(duration: int = 2, **_) -> Stun:
    return Stun(duration)


def _create_invincible(duration: int = 5, **_) -> Invincible:
    return Invincible(duration)


def _create_sleep(duration: int = 5, **_) -> Sleep:
    return Sleep(duration)


class StatusEffectFactory:
    """Factory for creating status effect instances by type."""

    _creators = {
        # Damage over time
        'burn': _create_burn,
        'fire': _create_burn,
        'poison': _create_poison,
        'bleed': _create_bleed,
        # Stat modifiers
        'might': _create_might,
        'strength': _create_might,
        'weak': _create_weak,
        'haste': _create_haste,
        'slow': _create_slow,
        # Crowd control
        'stun': _create_stun,
        'paralyze': _create_stun,
        'root': _create_root,
        'sleep': _create_sleep,
        # Mind effects
        'fear': _create_fear,
        'charm': _create_charm,
        # Special
        'berserk': _create_berserk,
        'invincible': _create_invincible,
    }

    @classmethod
    def create(cls, effect_type: str, **kwargs) -> Optional[StatusEffect]:
        """
        Create a status effect by type.

        Args:
            effect_type: Name of the effect (burn, poison, slow, etc.)
            **kwargs: Effect-specific parameters (duration, damage, etc.)

        Returns:
            StatusEffect instance or None if type unknown
        """
        effect_type = effect_type.lower()
        creator = cls._creators.get(effect_type)

        if creator is None:
            logger.warning(f"Unknown status effect type: {effect_type}")
            return None

        return creator(**kwargs)

    @classmethod
    def get_available_types(cls) -> list:
        """Get list of available status effect types."""
        return list(cls._creators.keys())

    @classmethod
    def register(cls, effect_type: str, creator):
        """
        Register a new status effect type.

        Args:
            effect_type: Name for the effect type
            creator: Function that creates the effect (receives **kwargs)
        """
        cls._creators[effect_type.lower()] = creator

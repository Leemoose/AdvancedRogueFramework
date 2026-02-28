"""
Target type enumeration for spells.
"""

from enum import Enum, auto


class TargetType(Enum):
    """
    Defines how a spell selects its target.

    Used by the UI/input system to determine what kind of targeting
    interface to show the player.
    """

    # No target needed - spell affects caster or area around caster
    SELF = auto()

    # Target a single enemy
    SINGLE_ENEMY = auto()

    # Target a single ally
    SINGLE_ALLY = auto()

    # Target any single entity (enemy or ally)
    SINGLE_ANY = auto()

    # Target a ground position
    GROUND = auto()

    # Target a direction (for line/cone effects)
    DIRECTION = auto()

    # No targeting - instant cast
    NONE = auto()

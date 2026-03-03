"""
Core enums used across the game.
These are placed here to avoid circular imports between packages.
"""

from enum import Enum, auto


class LoopType(Enum):
    """
    Game state/loop types. Controls which screen and input handler is active.

    Moved from loop_workflow/looptype.py to break circular dependency
    between display_generation and loop_workflow packages.
    """
    none = -1
    action = auto()
    spell = auto()
    inventory = auto()
    equipment = auto()
    main = auto()
    classes = auto()
    items = auto()
    examine = auto()
    trade = auto()
    paused = auto()
    targeting = auto()
    specific_examine = auto()
    enchant = auto()
    quest = auto()
    level_up = auto()
    victory = auto()
    help = auto()
    death = auto()
    story = auto()
    resting = auto()
    pathing = auto()
    binding = auto()
    spell_individual = auto()
    quickcast = auto()
    apply_potion = auto()
    crafting = auto()

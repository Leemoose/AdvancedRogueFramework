"""
Input action mappings and helper functions for key handling.

This module provides:
- DIRECTION_KEYS: Maps direction keys to (dx, dy) tuples
- Key-to-action mappings for each game screen
- Helper functions to reduce elif chains in key_screens.py
"""

from src.core.enums import LoopType


# =============================================================================
# DIRECTION MAPPINGS
# =============================================================================

# Maps direction key names to (dx, dy) movement deltas
DIRECTION_KEYS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "y": (-1, -1),  # up-left
    "u": (1, -1),   # up-right
    "b": (-1, 1),   # down-left
    "n": (1, 1),    # down-right
}


def is_direction_key(key):
    """Check if key is a movement direction."""
    return key in DIRECTION_KEYS


def get_direction(key):
    """Get (dx, dy) for a direction key, or None if not a direction."""
    return DIRECTION_KEYS.get(key)


# =============================================================================
# EQUIPMENT SLOT MAPPINGS
# =============================================================================

# Maps keys to equipment slot names for the equipment screen
EQUIPMENT_SLOT_KEYS = {
    "q": "shield",
    "a": "amulet",
    "z": "ring",
    "w": "helmet",
    "s": "body_armor",
    "x": "boots",
    "d": "weapon",
    "c": "gloves",
    "p": "pants",
    "r": "ring",
}


def get_equipment_slot(key):
    """Get equipment slot name for a key, or None if not an equipment key."""
    return EQUIPMENT_SLOT_KEYS.get(key)


# =============================================================================
# INVENTORY FILTER MAPPINGS
# =============================================================================

# Maps number keys to inventory filter types
INVENTORY_FILTER_KEYS = {
    "1": "item",
    "2": "potion",
    "3": "scroll",
    "4": "equipment",
    "5": "weapon",
}


def get_inventory_filter(key):
    """Get inventory filter type for a number key, or None."""
    return INVENTORY_FILTER_KEYS.get(key)


# =============================================================================
# QUICK CAST / SKILL NUMBER HELPERS
# =============================================================================

QUICK_CAST_KEYS = frozenset("12345678")


def is_quick_cast_key(key):
    """Check if key is a quick cast slot (1-8)."""
    return key in QUICK_CAST_KEYS


def get_skill_index(key):
    """Convert a number key to 0-based skill index, or None."""
    if key in QUICK_CAST_KEYS:
        return int(key) - 1
    return None


# =============================================================================
# QUEST NUMBER KEYS
# =============================================================================

QUEST_NUMBER_KEYS = frozenset("123456789")


def is_quest_number_key(key):
    """Check if key selects a quest number."""
    return key in QUEST_NUMBER_KEYS


# =============================================================================
# LETTER KEY HELPERS (for inventory item selection)
# =============================================================================

def key_to_index(key):
    """
    Convert a lowercase letter key to a 0-based index.
    'a' -> 0, 'b' -> 1, etc.
    Returns None if not a single lowercase letter.
    """
    if isinstance(key, str) and len(key) == 1 and 'a' <= key <= 'z':
        return ord(key) - ord('a')
    return None


def index_to_key(index):
    """Convert a 0-based index to a letter key. 0 -> 'a', 1 -> 'b', etc."""
    if 0 <= index <= 25:
        return chr(ord('a') + index)
    return None


# =============================================================================
# ACTION SCREEN KEY MAPPINGS
# =============================================================================

# Actions that change the game screen/mode (no additional logic needed)
ACTION_SCREEN_CHANGES = {
    "i": (LoopType.inventory, "main"),      # (loop_type, inventory_type or None)
    "e": (LoopType.equipment, None),
    "q": (LoopType.inventory, "potion"),
    "r": (LoopType.inventory, "scroll"),
    "p": (LoopType.spell, None),
    "esc": (LoopType.paused, None),
    "c": (LoopType.quest, None),
}


def get_action_screen_change(key):
    """
    Get screen change info for an action key.
    Returns (LoopType, inventory_filter) or None.
    inventory_filter is None for non-inventory screens.
    """
    return ACTION_SCREEN_CHANGES.get(key)


# =============================================================================
# ITEM SCREEN ACTION MAPPINGS
# =============================================================================

# Simple item actions that just call a player method
ITEM_ACTIONS = {
    "d": "drop",
    "e": "equip",
    "u": "unequip",
    "q": "quaff",
    "r": "read",
    "a": "activate",
    "t": "throw"
}


def get_item_action(key):
    """Get the item action name for a key, or None."""
    return ITEM_ACTIONS.get(key)


# =============================================================================
# MAIN SCREEN KEY MAPPINGS
# =============================================================================

MAIN_SCREEN_ACTIONS = {
    "l": "load",
    "h": "help",
    "s": "story",
}


def get_main_screen_action(key):
    """Get main screen action for a key, or None."""
    return MAIN_SCREEN_ACTIONS.get(key)


# =============================================================================
# PAUSED SCREEN KEY MAPPINGS
# =============================================================================

PAUSED_SCREEN_ACTIONS = {
    "m": "main_menu",
    "s": "save",
    "q": "quit",
    "b": "binding",
}


def get_paused_action(key):
    """Get paused screen action for a key, or None."""
    return PAUSED_SCREEN_ACTIONS.get(key)

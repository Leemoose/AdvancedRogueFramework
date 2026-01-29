"""
Game Constants and Magic Numbers
================================

This module centralizes all constants used throughout the game,
replacing scattered magic numbers with named, documented values.

Tile ID Ranges:
- 0-99: Basic tiles (walls, floors, stairs)
- 100-999: Items and equipment
- 1000-1999: Monsters
- 2000-2999: NPCs and interactables
- 3000-3999: Armor and equipment slots
- 4000-4999: Weapons
- 5000+: Special effects and UI

Entity States:
- NO_ENTITY (-1): Empty cell marker
"""

from enum import Enum, auto
from typing import Tuple

# ==============================================================================
# ENTITY MARKERS
# ==============================================================================

NO_ENTITY: int = -1  # Sentinel value for empty map cells
NO_ID: int = -1      # Unassigned entity ID
INFINITE_DURATION: int = -100  # Special value for permanent status effects


# ==============================================================================
# TILE ID RANGES
# ==============================================================================

class TileIDRange:
    """Defines ID ranges for different entity types."""

    # Environment
    BASIC_TILES_START = 0
    BASIC_TILES_END = 99

    # Items
    ITEMS_START = 100
    CONSUMABLES_START = 400
    RINGS_START = 500
    AMULETS_START = 550
    ARMOR_START = 600
    BOOTS_START = 700
    GLOVES_START = 750
    HELMETS_START = 770
    ITEMS_END = 999

    # Monsters
    MONSTERS_START = 1000
    GOBLIN_ID = 1010
    KOBOLD_ID = 1020
    ORC_ID = 1030
    MONSTERS_END = 1999

    # NPCs
    NPCS_START = 2000
    NPCS_END = 2999

    # Equipment slots
    EQUIPMENT_START = 3000
    HELMET_SLOT = 3200
    RING_SLOT = 3500
    AMULET_SLOT = 3600
    EQUIPMENT_END = 3999

    # Weapons
    WEAPONS_START = 4000
    SWORD_ID = 4800
    WEAPONS_END = 4999


# ==============================================================================
# GAME LOOP STATES
# ==============================================================================

class LoopType(Enum):
    """
    Enumeration of all possible game states.

    The game uses a state machine where each LoopType represents
    a distinct mode of player interaction.
    """
    NONE = auto()

    # Main gameplay
    ACTION = auto()       # Normal exploration/combat
    TARGETING = auto()    # Selecting a target for spell/ability
    EXAMINE = auto()      # Looking at items/monsters
    RESTING = auto()      # Auto-rest until healed
    PATHING = auto()      # Auto-explore/auto-travel

    # Menus
    MAIN = auto()         # Main menu
    PAUSED = auto()       # Pause menu
    HELP = auto()         # Help screen
    STORY = auto()        # Story/lore screen

    # Character management
    INVENTORY = auto()    # Inventory screen
    EQUIPMENT = auto()    # Equipment screen
    ITEMS = auto()        # Item details
    LEVEL_UP = auto()     # Level up stat selection
    SPELL = auto()        # Spell selection
    SPELL_INDIVIDUAL = auto()  # Single spell details
    BINDING = auto()      # Key binding configuration
    QUICKCAST = auto()    # Quick spell selection
    CLASSES = auto()      # Class selection

    # Interactions
    TRADE = auto()        # NPC trading
    QUEST = auto()        # Quest log
    ENCHANT = auto()      # Item enchanting

    # Examination
    SPECIFIC_EXAMINE = auto()  # Detailed item/monster info

    # End states
    VICTORY = auto()
    DEATH = auto()


# ==============================================================================
# RARITY LEVELS
# ==============================================================================

class Rarity(Enum):
    """Item and monster rarity classifications."""
    EXTRA_COMMON = "Extra Common"
    COMMON = "Common"
    RARE = "Rare"
    LEGENDARY = "Legendary"
    UNIQUE = "Unique"


# ==============================================================================
# EQUIPMENT SLOTS
# ==============================================================================

class EquipmentSlot(Enum):
    """Valid equipment slot identifiers."""
    HELMET = "helmet_slot"
    BODY_ARMOR = "body_armor_slot"
    GLOVES = "gloves_slot"
    BOOTS = "boots_slot"
    PANTS = "pants_slot"
    WEAPON = "weapon_slot"
    OFF_HAND = "off_hand_slot"
    RING = "ring_slot"
    AMULET = "amulet_slot"


# ==============================================================================
# DISPLAY CONSTANTS
# ==============================================================================

TILE_SIZE: int = 32  # Size of tiles in pixels


# ==============================================================================
# GAME TIME SYSTEM
# ==============================================================================

class GameTime:
    """
    Constants for the energy-based turn system.

    The game uses an energy system where each turn represents a fixed
    amount of energy expenditure. Actions consume energy, and when a
    character's energy drops below zero, game time advances.
    """
    ENERGY_PER_TURN = 100  # Energy units that constitute one game turn


# ==============================================================================
# ACTION COSTS
# ==============================================================================

class ActionCost:
    """
    Default action costs in energy units.

    The game uses an energy system where actions have varying costs.
    When energy drops below 0, time passes and monsters take turns.
    """
    MOVE = 100
    ATTACK = 100
    GRAB = 50
    REST = 100
    CAST_SPELL = 100
    USE_ITEM = 50
    EQUIP = 50
    UNEQUIP = 50

    # Fast monsters
    FAST_MOVE = 80
    FAST_ATTACK = 80

    # Slow creatures
    SLOW_MOVE = 300


# ==============================================================================
# COLORS (RGB)
# ==============================================================================

class Colors:
    """Standard color definitions for the game UI."""
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)
    PURPLE: Tuple[int, int, int] = (128, 0, 128)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    LIGHT_GRAY: Tuple[int, int, int] = (192, 192, 192)
    DARK_GRAY: Tuple[int, int, int] = (64, 64, 64)

    # UI Colors
    HEALTH_RED: Tuple[int, int, int] = (220, 20, 60)
    MANA_BLUE: Tuple[int, int, int] = (65, 105, 225)
    POISON_GREEN: Tuple[int, int, int] = (50, 205, 50)
    EXPERIENCE_GOLD: Tuple[int, int, int] = (255, 215, 0)

    # Message colors
    MSG_DEFAULT: Tuple[int, int, int] = (255, 255, 255)
    MSG_DAMAGE: Tuple[int, int, int] = (255, 100, 100)
    MSG_HEAL: Tuple[int, int, int] = (100, 255, 100)
    MSG_INFO: Tuple[int, int, int] = (200, 200, 255)
    MSG_WARNING: Tuple[int, int, int] = (255, 255, 100)


# ==============================================================================
# DUNGEON GENERATION
# ==============================================================================

class DungeonConfig:
    """Configuration for dungeon generation."""
    MIN_ROOM_SIZE = 4
    MAX_ROOM_SIZE = 12
    MIN_ROOMS = 5
    MAX_ROOMS = 15
    CORRIDOR_WIDTH = 1
    MAX_DEPTH = 10


# ==============================================================================
# DEBUG FLAGS
# ==============================================================================

DEBUG_MODE: bool = False  # Set to True to enable debug output
SHOW_PATHFINDING: bool = False
SHOW_FOV_DEBUG: bool = False

"""
Asset Registry
==============

Centralizes all tile asset IDs and paths, replacing hardcoded render_tags
throughout the codebase.

Tile ID Ranges:
- 0-99: Basic tiles (walls, floors, stairs, doors)
- 100-199: Pants, NPCs
- 200-299: Player assets
- 300-399: Weapons
- 400-499: Consumables (potions, scrolls, books)
- 500-599: Rings, Amulets
- 600-699: Body armor
- 700-749: Boots
- 750-799: Gloves
- 770-799: Helmets
- 800-899: Empty equipment slot icons
- 900-999: Skills/UI
- 1000-1999: Monsters
- 2000-2999: Dungeon tiles
- 3000-3999: Crawl items/equipment
- 4000-4999: Special items, orbs, scrolls
- 5000-5999: Player equipment overlays
- 6000-6999: Interactables
- 9000+: UI elements

Note: Negative IDs represent shaded/dark variants of tiles (e.g., -1 is shaded colorful_wall)
"""

from typing import Dict, Any, Optional


class TileID:
    """Named constants for commonly used tile IDs."""

    # ==========================================================================
    # Basic tiles (0-99)
    # ==========================================================================
    PLACEHOLDER = 0
    COLORFUL_WALL = 1
    COLORFUL_FLOOR = 2
    FLOOR_DIRTY = 3
    FLOOR_DIRTY_ALT = 4
    RED_CARPET = 5
    WOODEN_FLOOR = 6
    FOREST_WALL = 7
    OCEAN_FLOOR = 8
    SAND_FLOOR = 9
    DEEP_OCEAN = 10
    WALL_ROUNDED = 11
    FLOOR_ROUNDED = 12
    FOREST_FLOOR = 13
    OCEAN_WALL = 14
    STONE_FLOOR = 15

    # Fire effect
    FIRE = 20

    # Doors
    DOOR_CLOSED = 30
    DOOR_OPEN = 31

    # UI stat indicators
    STAT_UP = 50
    STAT_DOWN = 51

    # Stairs and transitions
    STAIRS_UP = 90
    STAIRS_DOWN = 91
    GATEWAY = 92

    # ==========================================================================
    # Pants and NPCs (100-199)
    # ==========================================================================
    PANTS = 100

    # NPCs
    SHOPKEEPER = 110
    KING = 120
    GUARD = 121
    SPEECH_BUBBLE = 122
    SENSEI = 123
    TRAINING_DUMMY = 124
    DESTROYED_DUMMY = 125
    ARCHMAGE = 126

    # ==========================================================================
    # Player assets (200-299)
    # ==========================================================================
    PLAYER_LEGACY = 200  # Legacy player sprite
    PLAYER_UNDER_ARMOR = -200  # Player base layer (negative)
    PLAYER_BOOTS_OVERLAY = 201
    PLAYER_GLOVES_OVERLAY = 202
    PLAYER_HELMET_OVERLAY = 203
    PLAYER_ARMOR_OVERLAY = 204

    # Gold
    GOLD = 210

    # ==========================================================================
    # Weapons (300-399)
    # ==========================================================================
    # Axes
    BASIC_AXE = 300
    BLEEDING_AXE = 303

    # Hammers
    HAMMER = 301
    CRUSHING_HAMMER = 302

    # Shields (311-319)
    SHIELD_BASIC = 311
    SHIELD_AEGIS = 312
    SHIELD_TOWER = 313
    MAGIC_FOCUS = 314

    # Daggers
    DAGGER = 321
    SCREAMING_DAGGER = 322

    # Special swords
    BURNING_SWORD = 331
    MAGIC_WAND = 332

    # Swords
    SWORD = 340
    SLEEPING_SWORD = 341

    # Ranged
    BOW = 351

    # ==========================================================================
    # Consumables (400-499)
    # ==========================================================================
    # Orbs/Potions
    HEALTH_ORB = 401
    MANA_ORB = 402
    CURING_ORB = 403
    MIGHT_ORB = 404
    HASTE_ORB = 405

    # Scrolls
    SCROLL = 450

    # Books
    BOOK = 480

    # ==========================================================================
    # Jewelry (500-599)
    # ==========================================================================
    # Rings
    RING_GREEN_GOLD = 500
    RING_BLOOD = 501
    RING_BLUE = 502
    RING_RED = 503
    RING_BONE = 504
    RING_TELEPORT = 505

    # Amulets
    AMULET = 550

    # ==========================================================================
    # Body Armor (600-699)
    # ==========================================================================
    ARMOR_BASIC = 600
    ARMOR_LEATHER = 601
    ARMOR_GOLDEN = 602
    ARMOR_WARMONGER = 603
    ARMOR_WIZARD_ROBE = 604
    ARMOR_KARATE_GI = 605
    ARMOR_BLOODSTAINED = 606

    # ==========================================================================
    # Boots (700-749)
    # ==========================================================================
    BOOTS_BASIC = 700
    BOOTS_ESCAPE = 701
    BOOTS_BLACKENED = 702
    BOOTS_ASSASSIN = 703

    # ==========================================================================
    # Gloves (750-769)
    # ==========================================================================
    GLOVES_BASIC = 750
    GLOVES_GAUNTLETS = 751
    GLOVES_BOXING = 752
    GLOVES_HEALER = 753
    GLOVES_LICH_HAND = 754

    # ==========================================================================
    # Helmets (770-799)
    # ==========================================================================
    HELMET_BASIC = 770
    HELMET_VIKING = 771
    HELMET_SPARTAN = 772
    HELMET_GREAT = 773
    HELMET_THIEF_HOOD = 774
    HELMET_WIZARD_HAT = 775

    # ==========================================================================
    # Empty Equipment Slot Icons (800-899)
    # ==========================================================================
    # Closed slot icons
    EMPTY_ARMOR = 801
    EMPTY_BOOTS = 802
    EMPTY_GLOVES = 803
    EMPTY_HELMET = 804
    EMPTY_WEAPON = 805
    EMPTY_SHIELD = 806
    EMPTY_RING = 807

    # Open slot icons (highlighted/selected)
    EMPTY_ARMOR_OPEN = 811
    EMPTY_BOOTS_OPEN = 812
    EMPTY_GLOVES_OPEN = 813
    EMPTY_HELMET_OPEN = 814
    EMPTY_WEAPON_OPEN = 815
    EMPTY_SHIELD_OPEN = 816
    EMPTY_RING_OPEN = 817
    EMPTY_PANTS_OPEN = 818
    EMPTY_PANTS = 819
    EMPTY_AMULET_OPEN = 820
    EMPTY_AMULET = 821

    # ==========================================================================
    # Skills/UI (900-999)
    # ==========================================================================
    TARGET = 901
    SKILL_PLACEHOLDER = 902
    SKILL_GUN = 903
    SKILL_BURNING_ATTACK = 904
    SKILL_MAGIC_MISSILE = 905
    SKILL_PETRIFY = 906
    SKILL_SHRUG_OFF = 907
    SKILL_BERSERK = 908
    SKILL_BLOOD_PACT = 909
    SKILL_TERRIFY = 910
    SKILL_ESCAPE = 911
    SKILL_HEAL = 912
    SKILL_TORMENT = 913
    SKILL_TELEPORT = 914
    SKILL_INVINCIBLE = 915

    # ==========================================================================
    # Monsters (1000-1999)
    # ==========================================================================
    BROWN_OOZE = 1000
    GOBLIN = 1010
    KOBOLD = 1020
    ORC_KNIGHT = 1030
    JUMPING_SPIDER = 1040
    SKELETON = 1050
    SKELETON_CENTAUR = 1051

    # ==========================================================================
    # Dungeon Tiles - Crawl (2000-2999)
    # ==========================================================================
    CRAWL_FLOOR_BLOOD = 2000
    CRAWL_WALL_STONE = 2100
    CRAWL_TRAP_ZOT = 2200

    # ==========================================================================
    # Crawl Items/Equipment (3000-3999)
    # ==========================================================================
    CRAWL_LEATHER_ARMOR = 3000
    CRAWL_GLOVES = 3100
    CRAWL_HELMET = 3200
    CRAWL_PANTS = 3300
    CRAWL_BUCKLER = 3400
    CRAWL_RING = 3500
    CRAWL_AMULET = 3600
    CRAWL_POTION = 3700

    # ==========================================================================
    # Special Items (4000-4999)
    # ==========================================================================
    # Orbs
    FOREST_ORB = 4000
    OCEAN_ORB = 4010

    # Consumables
    YELLOW_FLOWER_PETAL = 4200
    CRAWL_SCROLL = 4300

    # Weapons (crawl variants)
    CRAWL_BOW = 4400
    CRAWL_SPEAR = 4500
    CRAWL_WAR_AXE = 4600
    CRAWL_HAMMER = 4700
    CRAWL_LONG_SWORD = 4800
    CRAWL_DAGGER = 4900

    # ==========================================================================
    # Player Equipment Overlays - Crawl (5000-5999)
    # ==========================================================================
    PLAYER = 5000  # Main player sprite (crawl human_m)
    PLAYER_GLOVES_CRAWL = 5100
    PLAYER_BOOTS_CRAWL = 5200
    PLAYER_HEAD_CRAWL = 5300
    PLAYER_BODY_CRAWL = 5400
    PLAYER_LEGS_CRAWL = 5500

    # ==========================================================================
    # Interactables (6000-6999)
    # ==========================================================================
    BLOOD_FOUNTAIN = 6000
    DRY_FOUNTAIN = 6010
    ORCISH_IDOL = 6100

    # ==========================================================================
    # UI Elements (9000+)
    # ==========================================================================
    UI_BUTTON_STOCK = 9000


# Mapping of equipment slot types to their empty icon IDs
EMPTY_SLOT_ICONS: Dict[str, int] = {
    'armor': TileID.EMPTY_ARMOR,
    'boots': TileID.EMPTY_BOOTS,
    'gloves': TileID.EMPTY_GLOVES,
    'helmet': TileID.EMPTY_HELMET,
    'weapon': TileID.EMPTY_WEAPON,
    'shield': TileID.EMPTY_SHIELD,
    'ring': TileID.EMPTY_RING,
    'pants': TileID.EMPTY_PANTS,
    'amulet': TileID.EMPTY_AMULET,
}

# Mapping of equipment slot types to their open/selected icon IDs
EMPTY_SLOT_ICONS_OPEN: Dict[str, int] = {
    'armor': TileID.EMPTY_ARMOR_OPEN,
    'boots': TileID.EMPTY_BOOTS_OPEN,
    'gloves': TileID.EMPTY_GLOVES_OPEN,
    'helmet': TileID.EMPTY_HELMET_OPEN,
    'weapon': TileID.EMPTY_WEAPON_OPEN,
    'shield': TileID.EMPTY_SHIELD_OPEN,
    'ring': TileID.EMPTY_RING_OPEN,
    'pants': TileID.EMPTY_PANTS_OPEN,
    'amulet': TileID.EMPTY_AMULET_OPEN,
}

# Skill ID to name mapping for UI display
SKILL_NAMES: Dict[int, str] = {
    TileID.SKILL_PLACEHOLDER: "Placeholder",
    TileID.SKILL_GUN: "Gun",
    TileID.SKILL_BURNING_ATTACK: "Burning Attack",
    TileID.SKILL_MAGIC_MISSILE: "Magic Missile",
    TileID.SKILL_PETRIFY: "Petrify",
    TileID.SKILL_SHRUG_OFF: "Shrug Off",
    TileID.SKILL_BERSERK: "Berserk",
    TileID.SKILL_BLOOD_PACT: "Blood Pact",
    TileID.SKILL_TERRIFY: "Terrify",
    TileID.SKILL_ESCAPE: "Escape",
    TileID.SKILL_HEAL: "Heal",
    TileID.SKILL_TORMENT: "Torment",
    TileID.SKILL_TELEPORT: "Teleport",
    TileID.SKILL_INVINCIBLE: "Invincible",
}

# Monster ID to name mapping
MONSTER_NAMES: Dict[int, str] = {
    TileID.BROWN_OOZE: "Brown Ooze",
    TileID.GOBLIN: "Goblin",
    TileID.KOBOLD: "Kobold",
    TileID.ORC_KNIGHT: "Orc Knight",
    TileID.JUMPING_SPIDER: "Jumping Spider",
    TileID.SKELETON: "Skeleton",
    TileID.SKELETON_CENTAUR: "Skeleton Centaur",
}


def get_render_tag(name: str) -> int:
    """Get a tile ID by name.

    Args:
        name: The name of the tile (e.g., 'goblin', 'stairs_down')

    Returns:
        The tile ID number

    Raises:
        KeyError: If the tile name is not found
    """
    try:
        return getattr(TileID, name.upper())
    except AttributeError:
        raise KeyError(f"Tile '{name}' not found in asset registry")


def get_shaded_id(tile_id: int) -> int:
    """Get the shaded (dark) variant of a tile ID.

    Many tiles have shaded variants stored at negative IDs.
    For example, tile 1 (colorful_wall) has shaded variant at -1.

    Args:
        tile_id: The base tile ID

    Returns:
        The shaded variant ID (negative of the input)
    """
    return -abs(tile_id)


def has_shaded_variant(tile_id: int) -> bool:
    """Check if a tile ID has a known shaded variant.

    Based on the tiles defined in static_configs.py that have negative counterparts.

    Args:
        tile_id: The tile ID to check

    Returns:
        True if a shaded variant exists
    """
    # These tiles have shaded variants based on static_configs.py
    TILES_WITH_SHADED = {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,  # Basic floors/walls
        30, 31,  # Doors
        50, 51,  # Stat indicators
        90, 91, 92,  # Stairs
        200,  # Player
        902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915,  # Skills
    }
    return abs(tile_id) in TILES_WITH_SHADED


def get_empty_slot_icon(slot_type: str, is_open: bool = False) -> int:
    """Get the empty slot icon for an equipment slot.

    Args:
        slot_type: The type of equipment slot ('armor', 'boots', etc.)
        is_open: Whether to get the open/highlighted variant

    Returns:
        The tile ID for the empty slot icon

    Raises:
        KeyError: If the slot type is not recognized
    """
    icons = EMPTY_SLOT_ICONS_OPEN if is_open else EMPTY_SLOT_ICONS
    if slot_type not in icons:
        raise KeyError(f"Unknown equipment slot type: {slot_type}")
    return icons[slot_type]


def get_skill_name(skill_id: int) -> Optional[str]:
    """Get the display name for a skill.

    Args:
        skill_id: The skill's tile ID

    Returns:
        The skill name, or None if not found
    """
    return SKILL_NAMES.get(skill_id)


def get_monster_name(monster_id: int) -> Optional[str]:
    """Get the display name for a monster.

    Args:
        monster_id: The monster's tile ID

    Returns:
        The monster name, or None if not found
    """
    return MONSTER_NAMES.get(monster_id)

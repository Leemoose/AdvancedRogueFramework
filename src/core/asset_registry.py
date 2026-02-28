"""
Asset Registry
==============

Centralizes all tile asset IDs and paths, replacing hardcoded render_tags
throughout the codebase.

================================================================================
                            ASSET ID NUMBERING SCHEME
================================================================================

This file uses a consistent, scalable numbering system designed for future growth.

DESIGN PRINCIPLES:
- Each major category gets a 1000-block (0-999, 1000-1999, etc.)
- Within categories, subcategories get 100-blocks
- Individual items are spaced by 10 to allow variants
  (e.g., sword=3000, burning_sword=3001, frost_sword=3002)
- Related "crawl" variants live next to their base items

================================================================================
                              ID RANGE REFERENCE
================================================================================

| Range       | Category           | Subcategories                              |
|-------------|--------------------|--------------------------------------------|
| 0-999       | ENVIRONMENT        |                                            |
|   0-99      |   System           | 0=placeholder                              |
|   100-199   |   Floors           | 100=colorful, 110=dirty, 120=carpet...    |
|   200-299   |   Walls            | 200=colorful, 210=rounded, 220=forest...  |
|   300-399   |   Doors            | 300=closed, 301=open, 310=locked...       |
|   400-499   |   Stairs           | 400=up, 410=down, 420=gateway             |
|   500-599   |   Effects          | 500=fire, 510=ice, 520=poison...          |
|   600-699   |   Traps            | 600=zot_trap...                           |
|   700-799   |   Interactables    | 700=fountain, 710=dry_fountain, 720=idol  |
|   800-999   |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 1000-1999   | CHARACTERS         |                                            |
|   1000-1099 |   Player           | 1000=base, 1010=under_armor, 1020=overlay |
|   1100-1199 |   NPCs             | 1100=shopkeeper, 1110=king, 1120=guard... |
|   1200-1299 |   Gold/Currency    | 1200=gold                                 |
|   1300-1999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 2000-2999   | MONSTERS           |                                            |
|   2000-2099 |   Oozes/Slimes     | 2000=brown_ooze, 2010=green_ooze...       |
|   2100-2199 |   Goblins          | 2100=goblin, 2110=goblin_chief...         |
|   2200-2299 |   Kobolds          | 2200=kobold, 2210=kobold_shaman...        |
|   2300-2399 |   Orcs             | 2300=orc, 2310=orc_knight, 2320=warlord   |
|   2400-2499 |   Spiders          | 2400=spider, 2410=jumping_spider...       |
|   2500-2599 |   Undead           | 2500=skeleton, 2510=skeleton_centaur...   |
|   2600-2999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 3000-3999   | WEAPONS            |                                            |
|   3000-3099 |   Swords           | 3000=basic, 3001=sleeping, 3002=burning   |
|   3100-3199 |   Axes             | 3100=basic, 3101=bleeding...              |
|   3200-3299 |   Hammers          | 3200=basic, 3201=crushing...              |
|   3300-3399 |   Daggers          | 3300=basic, 3301=screaming...             |
|   3400-3499 |   Bows/Ranged      | 3400=bow, 3410=crossbow...                |
|   3500-3599 |   Wands/Staves     | 3500=wand, 3510=magic_focus...            |
|   3600-3699 |   Shields          | 3600=basic, 3601=aegis, 3602=tower...     |
|   3700-3999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 4000-4999   | ARMOR              |                                            |
|   4000-4099 |   Body Armor       | 4000=basic, 4001=leather, 4002=golden...  |
|   4100-4199 |   Helmets          | 4100=basic, 4101=viking, 4102=spartan...  |
|   4200-4299 |   Gloves           | 4200=basic, 4201=gauntlets, 4202=boxing...|
|   4300-4399 |   Boots            | 4300=basic, 4301=escape, 4302=blackened...|
|   4400-4499 |   Pants            | 4400=basic...                             |
|   4500-4999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 5000-5999   | ACCESSORIES        |                                            |
|   5000-5099 |   Rings            | 5000=green_gold, 5001=blood, 5002=blue... |
|   5100-5199 |   Amulets          | 5100=basic...                             |
|   5200-5999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 6000-6999   | CONSUMABLES        |                                            |
|   6000-6099 |   Potions/Orbs     | 6000=health, 6001=mana, 6002=curing...    |
|   6100-6199 |   Scrolls          | 6100=basic...                             |
|   6200-6299 |   Books            | 6200=basic...                             |
|   6300-6399 |   Food             | Reserved                                   |
|   6400-6499 |   Special          | 6400=flower_petal...                      |
|   6500-6999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 7000-7999   | SPECIAL ITEMS      |                                            |
|   7000-7099 |   Key Orbs         | 7000=forest_orb, 7001=ocean_orb...        |
|   7100-7999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 8000-8999   | UI - EQUIPMENT     |                                            |
|   8000-8099 |   Empty Slots      | 8000=armor, 8001=boots, 8002=gloves...    |
|   8100-8199 |   Empty Slots Open | 8100=armor, 8101=boots...                 |
|   8200-8299 |   Player Overlays  | 8200=boots, 8201=gloves, 8202=helmet...   |
|   8300-8999 |   Reserved         |                                            |
|-------------|--------------------|--------------------------------------------|
| 9000-9999   | UI - SKILLS/MISC   |                                            |
|   9000-9099 |   System UI        | 9000=target, 9001=stat_up, 9002=stat_down |
|   9100-9199 |   Attack Skills    | 9100=placeholder, 9101=burning_attack...  |
|   9200-9299 |   Defense Skills   | 9200=shrug_off, 9201=invincible...        |
|   9300-9399 |   Buff Skills      | 9300=berserk, 9301=blood_pact...          |
|   9400-9499 |   Utility Skills   | 9400=escape, 9401=teleport...             |
|   9500-9599 |   Heal Skills      | 9500=heal...                              |
|   9600-9699 |   Debuff Skills    | 9600=petrify, 9601=terrify, 9602=torment  |
|   9700-9899 |   Reserved         |                                            |
|   9900-9999 |   Misc UI          | 9900=button_stock, 9901=speech_bubble     |
|-------------|--------------------|--------------------------------------------|

FOG OF WAR:
- Fog-of-war shading is applied programmatically via pygame's BLEND_RGB_MULT
- No separate shaded tile assets are needed
- See display.py draw_single_tile() for implementation

ADDING NEW ASSETS:
1. Find the appropriate category and subcategory above
2. Use the next available ID within that subcategory
3. Add the constant to the TileID class below
4. Add the asset loading line to static_configs.py
5. Update any relevant dictionaries (SKILL_NAMES, MONSTER_NAMES, etc.)

================================================================================
"""

from typing import Dict


class TileID:
    """
    Named constants for all tile IDs in the game.

    Organized by category following the numbering scheme documented above.
    Each section is clearly labeled with its ID range.
    """

    # ==========================================================================
    # ENVIRONMENT (0-999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # System/Placeholder (0-99)
    # --------------------------------------------------------------------------
    PLACEHOLDER = 0

    # --------------------------------------------------------------------------
    # Floors (100-199)
    # Subcategories: 100=colorful, 110=dirty, 120=carpet, 130=wood, 140=stone,
    #                150=forest, 160=sand, 170=ocean, 180=blood, 190=rounded,
    #                195=new_fantasy
    # --------------------------------------------------------------------------
    COLORFUL_FLOOR = 100
    FLOOR_DIRTY = 110
    FLOOR_DIRTY_ALT = 111
    RED_CARPET = 120
    WOODEN_FLOOR = 130
    STONE_FLOOR = 140
    FOREST_FLOOR = 150
    DENSE_FOREST_FLOOR = 151  # Dense forest theme floor
    SAND_FLOOR = 160
    OCEAN_FLOOR = 170
    DEEP_OCEAN = 171
    CRAWL_FLOOR_BLOOD = 180
    FLOOR_ROUNDED = 190
    NEW_FANTASY_FLOOR = 195  # Dark fantasy stone floor

    # --------------------------------------------------------------------------
    # Walls (200-299)
    # Subcategories: 200=colorful, 210=rounded, 220=forest, 230=ocean, 240=stone,
    #                250=new_fantasy
    # --------------------------------------------------------------------------
    COLORFUL_WALL = 200
    WALL_ROUNDED = 210
    FOREST_WALL = 220
    DENSE_FOREST_WALL = 221  # Dense forest theme wall
    OCEAN_WALL = 230
    CRAWL_WALL_STONE = 240
    NEW_FANTASY_WALL = 250  # Dark fantasy brick wall

    # --------------------------------------------------------------------------
    # Doors (300-399)
    # Subcategories: 300=basic (closed/open), 310=locked, 320=new_fantasy
    # --------------------------------------------------------------------------
    DOOR_CLOSED = 300
    DOOR_OPEN = 301
    NEW_FANTASY_DOOR_CLOSED = 320  # Dark fantasy wooden door
    NEW_FANTASY_DOOR_OPEN = 321    # Dark fantasy door (open)
    DENSE_FOREST_DOOR_CLOSED = 322  # Dense forest theme door (closed)
    DENSE_FOREST_DOOR_OPEN = 323    # Dense forest theme door (open)

    # --------------------------------------------------------------------------
    # Stairs and Transitions (400-499)
    # Subcategories: 400=up, 410=down, 420=gateway, 430=new_fantasy
    # --------------------------------------------------------------------------
    STAIRS_UP = 400
    STAIRS_DOWN = 410
    GATEWAY = 420
    NEW_FANTASY_STAIRS_UP = 430    # Dark fantasy stairs ascending
    NEW_FANTASY_STAIRS_DOWN = 431  # Dark fantasy stairs descending
    NEW_FANTASY_PORTAL = 432       # Dark fantasy magical portal
    DENSE_FOREST_STAIRS_UP = 433   # Dense forest theme stairs up
    DENSE_FOREST_STAIRS_DOWN = 434 # Dense forest theme stairs down
    DENSE_FOREST_PORTAL = 435      # Dense forest theme portal

    # --------------------------------------------------------------------------
    # Effects (500-599)
    # Subcategories: 500=fire, 510=ice, 520=poison, etc.
    # --------------------------------------------------------------------------
    FIRE = 500

    # --------------------------------------------------------------------------
    # Traps (600-699)
    # --------------------------------------------------------------------------
    CRAWL_TRAP_ZOT = 600

    # --------------------------------------------------------------------------
    # Interactables (700-799)
    # Subcategories: 700=fountains, 710=idols, 720=campfires, 730=plants,
    #                740=orb_pedestals
    # --------------------------------------------------------------------------
    BLOOD_FOUNTAIN = 700
    DRY_FOUNTAIN = 701
    ORCISH_IDOL = 710
    CAMPFIRE = 720
    CAMPFIRE_BURNT = 721
    YELLOW_PLANT = 730
    FOREST_ORB_PEDESTAL = 740
    FOREST_ORB_PEDESTAL_EMPTY = 741
    OCEAN_ORB_PEDESTAL = 742
    OCEAN_ORB_PEDESTAL_EMPTY = 743

    # ==========================================================================
    # CHARACTERS (1000-1999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Player Assets (1000-1099)
    # 1000=base sprites, 1010=under armor, 1020+=overlays
    # --------------------------------------------------------------------------
    PLAYER = 1000                   # Main player sprite (crawl human_m)
    PLAYER_LEGACY = 1001            # Legacy player sprite
    PLAYER_UNDER_ARMOR = -1000      # Player base layer (negative for under-layer)
    PLAYER_BOOTS_OVERLAY = 1020
    PLAYER_GLOVES_OVERLAY = 1021
    PLAYER_HELMET_OVERLAY = 1022
    PLAYER_ARMOR_OVERLAY = 1023
    PLAYER_LEGS_OVERLAY = 1024
    # Crawl-style player overlays
    PLAYER_GLOVES_CRAWL = 1030
    PLAYER_BOOTS_CRAWL = 1031
    PLAYER_HEAD_CRAWL = 1032
    PLAYER_BODY_CRAWL = 1033
    PLAYER_LEGS_CRAWL = 1034

    # --------------------------------------------------------------------------
    # NPCs (1100-1199)
    # --------------------------------------------------------------------------
    SHOPKEEPER = 1100
    KING = 1110
    GUARD = 1111
    SENSEI = 1120
    ARCHMAGE = 1121
    TRAINING_DUMMY = 1130
    DESTROYED_DUMMY = 1131

    # --------------------------------------------------------------------------
    # Gold/Currency (1200-1299)
    # --------------------------------------------------------------------------
    GOLD = 1200

    # ==========================================================================
    # MONSTERS (2000-2999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Oozes/Slimes (2000-2099)
    # --------------------------------------------------------------------------
    BROWN_OOZE = 2000

    # --------------------------------------------------------------------------
    # Goblins (2100-2199)
    # --------------------------------------------------------------------------
    GOBLIN = 2100

    # --------------------------------------------------------------------------
    # Kobolds (2200-2299)
    # --------------------------------------------------------------------------
    KOBOLD = 2200

    # --------------------------------------------------------------------------
    # Orcs (2300-2399)
    # --------------------------------------------------------------------------
    ORC_KNIGHT = 2300

    # --------------------------------------------------------------------------
    # Spiders (2400-2499)
    # --------------------------------------------------------------------------
    JUMPING_SPIDER = 2400

    # --------------------------------------------------------------------------
    # Undead (2500-2599)
    # --------------------------------------------------------------------------
    SKELETON = 2500
    SKELETON_CENTAUR = 2501

    # ==========================================================================
    # WEAPONS (3000-3999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Swords (3000-3099)
    # Base sword=3000, variants follow: sleeping=3001, burning=3002, etc.
    # --------------------------------------------------------------------------
    SWORD = 3000
    SLEEPING_SWORD = 3001
    BURNING_SWORD = 3002
    CRAWL_LONG_SWORD = 3010

    # --------------------------------------------------------------------------
    # Axes (3100-3199)
    # --------------------------------------------------------------------------
    BASIC_AXE = 3100
    BLEEDING_AXE = 3101
    CRAWL_WAR_AXE = 3110

    # --------------------------------------------------------------------------
    # Hammers (3200-3299)
    # --------------------------------------------------------------------------
    HAMMER = 3200
    CRUSHING_HAMMER = 3201
    CRAWL_HAMMER = 3210

    # --------------------------------------------------------------------------
    # Daggers (3300-3399)
    # --------------------------------------------------------------------------
    DAGGER = 3300
    SCREAMING_DAGGER = 3301
    CRAWL_DAGGER = 3310

    # --------------------------------------------------------------------------
    # Bows/Ranged (3400-3499)
    # --------------------------------------------------------------------------
    BOW = 3400
    CRAWL_BOW = 3401
    CRAWL_SPEAR = 3410

    # --------------------------------------------------------------------------
    # Wands/Staves (3500-3599)
    # --------------------------------------------------------------------------
    MAGIC_WAND = 3500
    MAGIC_FOCUS = 3501

    # --------------------------------------------------------------------------
    # Shields (3600-3699)
    # --------------------------------------------------------------------------
    SHIELD_BASIC = 3600
    SHIELD_AEGIS = 3601
    SHIELD_TOWER = 3602
    CRAWL_BUCKLER = 3610

    # ==========================================================================
    # ARMOR (4000-4999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Body Armor (4000-4099)
    # --------------------------------------------------------------------------
    ARMOR_BASIC = 4000
    ARMOR_LEATHER = 4001
    ARMOR_GOLDEN = 4002
    ARMOR_WARMONGER = 4003
    ARMOR_WIZARD_ROBE = 4004
    ARMOR_KARATE_GI = 4005
    ARMOR_BLOODSTAINED = 4006
    CRAWL_LEATHER_ARMOR = 4010

    # --------------------------------------------------------------------------
    # Helmets (4100-4199)
    # --------------------------------------------------------------------------
    HELMET_BASIC = 4100
    HELMET_VIKING = 4101
    HELMET_SPARTAN = 4102
    HELMET_GREAT = 4103
    HELMET_THIEF_HOOD = 4104
    HELMET_WIZARD_HAT = 4105
    CRAWL_HELMET = 4110

    # --------------------------------------------------------------------------
    # Gloves (4200-4299)
    # --------------------------------------------------------------------------
    GLOVES_BASIC = 4200
    GLOVES_GAUNTLETS = 4201
    GLOVES_BOXING = 4202
    GLOVES_HEALER = 4203
    GLOVES_LICH_HAND = 4204
    CRAWL_GLOVES = 4210

    # --------------------------------------------------------------------------
    # Boots (4300-4399)
    # --------------------------------------------------------------------------
    BOOTS_BASIC = 4300
    BOOTS_ESCAPE = 4301
    BOOTS_BLACKENED = 4302
    BOOTS_ASSASSIN = 4303

    # --------------------------------------------------------------------------
    # Pants (4400-4499)
    # --------------------------------------------------------------------------
    PANTS = 4400
    CRAWL_PANTS = 4401

    # ==========================================================================
    # ACCESSORIES (5000-5999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Rings (5000-5099)
    # --------------------------------------------------------------------------
    RING_GREEN_GOLD = 5000
    RING_BLOOD = 5001
    RING_BLUE = 5002
    RING_RED = 5003
    RING_BONE = 5004
    RING_TELEPORT = 5005
    CRAWL_RING = 5010

    # --------------------------------------------------------------------------
    # Amulets (5100-5199)
    # --------------------------------------------------------------------------
    AMULET = 5100
    CRAWL_AMULET = 5110

    # ==========================================================================
    # CONSUMABLES (6000-6999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Potions/Orbs (6000-6099)
    # --------------------------------------------------------------------------
    HEALTH_ORB = 6000
    MANA_ORB = 6001
    CURING_ORB = 6002
    MIGHT_ORB = 6003
    HASTE_ORB = 6004
    CRAWL_POTION = 6010

    # --------------------------------------------------------------------------
    # Scrolls (6100-6199)
    # --------------------------------------------------------------------------
    SCROLL = 6100
    CRAWL_SCROLL = 6110

    # --------------------------------------------------------------------------
    # Books (6200-6299)
    # --------------------------------------------------------------------------
    BOOK = 6200

    # --------------------------------------------------------------------------
    # Special Consumables (6400-6499)
    # --------------------------------------------------------------------------
    YELLOW_FLOWER_PETAL = 6400

    # ==========================================================================
    # SPECIAL ITEMS (7000-7999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Key Orbs (7000-7099)
    # --------------------------------------------------------------------------
    FOREST_ORB = 7000
    OCEAN_ORB = 7001

    # ==========================================================================
    # UI - EQUIPMENT SLOTS (8000-8999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Empty Slot Icons - Closed (8000-8099)
    # --------------------------------------------------------------------------
    EMPTY_ARMOR = 8000
    EMPTY_BOOTS = 8001
    EMPTY_GLOVES = 8002
    EMPTY_HELMET = 8003
    EMPTY_WEAPON = 8004
    EMPTY_SHIELD = 8005
    EMPTY_RING = 8006
    EMPTY_PANTS = 8007
    EMPTY_AMULET = 8008

    # --------------------------------------------------------------------------
    # Empty Slot Icons - Open/Selected (8100-8199)
    # --------------------------------------------------------------------------
    EMPTY_ARMOR_OPEN = 8100
    EMPTY_BOOTS_OPEN = 8101
    EMPTY_GLOVES_OPEN = 8102
    EMPTY_HELMET_OPEN = 8103
    EMPTY_WEAPON_OPEN = 8104
    EMPTY_SHIELD_OPEN = 8105
    EMPTY_RING_OPEN = 8106
    EMPTY_PANTS_OPEN = 8107
    EMPTY_AMULET_OPEN = 8108

    # --------------------------------------------------------------------------
    # Player Equipment Overlays for Display (8200-8299)
    # Used in equipment screen to show equipped items on player
    # --------------------------------------------------------------------------
    EQUIP_DISPLAY_BOOTS = 8200
    EQUIP_DISPLAY_GLOVES = 8201
    EQUIP_DISPLAY_HELMET = 8202
    EQUIP_DISPLAY_ARMOR = 8203
    EQUIP_DISPLAY_LEGS = 8204

    # ==========================================================================
    # UI - SKILLS AND MISC (9000-9999)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # System UI (9000-9099)
    # --------------------------------------------------------------------------
    TARGET = 9000
    STAT_UP = 9001
    STAT_DOWN = 9002

    # --------------------------------------------------------------------------
    # Attack Skills (9100-9199)
    # --------------------------------------------------------------------------
    SKILL_PLACEHOLDER = 9100
    SKILL_GUN = 9101
    SKILL_BURNING_ATTACK = 9102
    SKILL_MAGIC_MISSILE = 9103

    # --------------------------------------------------------------------------
    # Defense Skills (9200-9299)
    # --------------------------------------------------------------------------
    SKILL_SHRUG_OFF = 9200
    SKILL_INVINCIBLE = 9201

    # --------------------------------------------------------------------------
    # Buff Skills (9300-9399)
    # --------------------------------------------------------------------------
    SKILL_BERSERK = 9300
    SKILL_BLOOD_PACT = 9301

    # --------------------------------------------------------------------------
    # Utility Skills (9400-9499)
    # --------------------------------------------------------------------------
    SKILL_ESCAPE = 9400
    SKILL_TELEPORT = 9401

    # --------------------------------------------------------------------------
    # Heal Skills (9500-9599)
    # --------------------------------------------------------------------------
    SKILL_HEAL = 9500

    # --------------------------------------------------------------------------
    # Debuff Skills (9600-9699)
    # --------------------------------------------------------------------------
    SKILL_PETRIFY = 9600
    SKILL_TERRIFY = 9601
    SKILL_TORMENT = 9602

    # --------------------------------------------------------------------------
    # Misc UI (9900-9999)
    # --------------------------------------------------------------------------
    UI_BUTTON_STOCK = 9900
    SPEECH_BUBBLE = 9901


# ==============================================================================
# LOOKUP DICTIONARIES
# ==============================================================================

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

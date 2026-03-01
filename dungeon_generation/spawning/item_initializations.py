"""
Item Spawn Configuration
========================

Defines which items can spawn and where they appear in the dungeon.
Uses a data-driven approach for easier maintenance.

To add new items:
1. Import the item class from item_implementation
2. Add entry to SPAWN_CONFIG with (ItemClass, min_floor, max_floor)
"""
from item_implementation import (
    # Weapons
    Bow, Spear, Axe, Hammer, Dagger, Sword, BroadSword,
    # Armor
    Shield, LeatherArmor, Helmet, Gloves, Pants,
    # Accessories
    Ring, Amulet,
    # Consumables
    HealthPotion, MightPotion,
    # Ingredients
    FireLily, RockVine,
)
from .spawn_params import ItemSpawnParams


# Item spawn configuration: (ItemClass, constructor_args, min_floor, max_floor)
# Use None for constructor_args if no args needed
# Floor restrictions per GAME_BALANCE_PLAN.md
SPAWN_CONFIG = [
    # WEAPONS - tiered by floor availability
    (Dagger,     None,   1, 10),  # Basic, available early
    (Sword,      None,   1, 10),  # Balanced weapon
    (Bow,        None,   1, 10),  # Ranged option
    (Spear,      None,   2, 10),  # Slightly better, floor 2+
    (Axe,        None,   3, 10),  # High damage, floor 3+
    (Hammer,     None,   4, 10),  # Very high damage, floor 4+
    (BroadSword, None,   5, 10),  # Superior sword, floor 5+

    # ARMOR
    (LeatherArmor, None, 1, 10),  # Basic protection
    (Gloves,       None, 1, 10),  # Basic slot filler
    (Pants,        None, 1, 10),  # Basic slot filler
    (Helmet,       None, 2, 10),  # Head protection, floor 2+
    (Shield,     (3400,), 3, 10), # Off-hand defense, floor 3+

    # ACCESSORIES - appear on deeper floors
    (Ring,   None, 4, 10),  # Stat boosts, floor 4+
    (Amulet, None, 5, 10),  # Stat boosts, floor 5+

    # CONSUMABLES
    (HealthPotion, None,   1, 10),  # Common healing
    (MightPotion,  (404,), 3, 10),  # Damage boost, floor 3+

    # INGREDIENTS
    (FireLily, None,   1, 10),  # basic fire tag ingredient
    (MightPotion,  None, 1, 10),  # basic stone tag ingredient
]


def _create_spawn_params():
    """Generate ItemSpawns list from configuration."""
    spawns = []
    for item_class, args, min_floor, max_floor in SPAWN_CONFIG:
        if args is None:
            item = item_class()
        else:
            item = item_class(*args)
        spawns.append(ItemSpawnParams(item, minFloor=min_floor, maxFloor=max_floor))
    return spawns


# Generate the spawn list
ItemSpawns = _create_spawn_params()

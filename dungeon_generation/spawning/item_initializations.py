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
)
from .spawn_params import ItemSpawnParams


# Item spawn configuration: (ItemClass, constructor_args, min_floor, max_floor)
# Use None for constructor_args if no args needed
SPAWN_CONFIG = [
    # Weapons - available throughout dungeon
    (Bow,        None,   1, 10),
    (Spear,      None,   1, 10),
    (Axe,        None,   1, 10),
    (Hammer,     None,   1, 10),
    (Dagger,     None,   1, 10),
    (Sword,      None,   1, 10),
    (BroadSword, None,   2, 10),  # Slightly better, appears from floor 2

    # Shields
    (Shield,     (3400,), 1, 10),

    # Armor
    (LeatherArmor, None, 1, 10),
    (Helmet,       None, 1, 10),
    (Gloves,       None, 1, 10),
    (Pants,        None, 1, 10),

    # Accessories
    (Ring,   None, 1, 10),
    (Amulet, None, 1, 10),

    # Consumables
    (HealthPotion, None,   1, 10),
    (MightPotion,  (404,), 1, 10),
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

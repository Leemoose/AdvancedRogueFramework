"""
Spawning System
===============

Unified spawning system for items, monsters, and interactables.
This consolidates the duplicate code from spawnparams.py and
dungeon_generation/spawning/ into a single, well-organized module.
"""

from .spawn_params import (
    SpawnParams,
    ItemSpawnParams,
    MonsterSpawnParams,
    InteractableSpawnParams,
)
from .spawner import (
    ItemSpawner,
    MonsterSpawner,
    InteractableSpawner,
)
from .spawn_config import (
    ITEM_SPAWNS,
    MONSTER_SPAWNS,
    INTERACTABLE_SPAWNS,
    RARITY_DISTRIBUTIONS,
)

"""
Spawn Configuration
===================

Default spawn configurations for items, monsters, and interactables.
These are placeholder configurations - the actual game uses the legacy
spawnparams.py until full migration.

To migrate:
1. Import spawn definitions from spawnparams.py
2. Convert to the new SpawnParams classes
3. Register in the appropriate list below
"""

from typing import List
from .spawn_params import ItemSpawnParams, MonsterSpawnParams, InteractableSpawnParams

# These will be populated during migration from spawnparams.py
ITEM_SPAWNS: List[ItemSpawnParams] = []
MONSTER_SPAWNS: List[MonsterSpawnParams] = []
INTERACTABLE_SPAWNS: List[InteractableSpawnParams] = []

# Rarity distributions by floor (common, rare, legendary)
RARITY_DISTRIBUTIONS = {
    "equipment": [
        (0.9, 0.1, 0.0),  # Floor 1
        (0.7, 0.3, 0.0),  # Floor 2
        (0.5, 0.4, 0.1),  # Floor 3
        (0.3, 0.6, 0.1),  # Floor 4
        (0.3, 0.5, 0.2),  # Floor 5
        (0.3, 0.5, 0.2),  # Floor 6
        (0.3, 0.4, 0.3),  # Floor 7
        (0.3, 0.4, 0.3),  # Floor 8
        (0.3, 0.3, 0.4),  # Floor 9
        (0.3, 0.3, 0.4),  # Floor 10
    ],
    "consumables": [
        (0.7, 0.3, 0.0),  # Floors 1-10 (same for all)
    ] * 10,
    "monsters": [
        (1.0, 0.0),  # Floor 1
        (0.8, 0.2),  # Floor 2
        (0.2, 0.8),  # Floor 3
        (0.7, 0.3),  # Floor 4
        (0.5, 0.5),  # Floor 5
        (0.2, 0.8),  # Floor 6
        (0.7, 0.3),  # Floor 7
        (0.3, 0.7),  # Floor 8
        (0.0, 1.0),  # Floor 9
        (0.0, 1.0),  # Floor 10
    ],
}

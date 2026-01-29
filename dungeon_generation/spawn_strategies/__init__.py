"""
Spawn Strategies Package
========================

Monster spawn placement strategies for dungeon generation.

This package provides different strategies for placing monsters
in the dungeon during generation. Each strategy implements the
MonsterSpawnStrategy interface from base.py.

Available strategies:
    - MonsterSpawnStrategy: Abstract base class defining the interface
    - RandomSpawnStrategy: Places monsters at random valid locations
    - EliteWithGroupStrategy: Places elite monster surrounded by minions
    - GuardingItemsStrategy: Places monsters near valuable items

Usage:
    from dungeon_generation.spawn_strategies import (
        MonsterSpawnStrategy,
        RandomSpawnStrategy,
        EliteWithGroupStrategy,
        GuardingItemsStrategy
    )

    # Use the random strategy with custom parameters
    strategy = RandomSpawnStrategy(
        avoid_corridors=True,
        avoid_stairs=True,
        max_attempts=500
    )

    # Use the elite group strategy for boss encounters
    elite_strategy = EliteWithGroupStrategy(
        elite_radius=3,
        prefer_large_rooms=True,
        formation='cluster'  # or 'circle', 'line'
    )

    # Use guarding items strategy for treasure rooms
    guard_strategy = GuardingItemsStrategy(
        guard_radius_min=2,
        guard_radius_max=4,
        guard_chance=0.7
    )

    # Place monsters using the strategy
    strategy.place_monsters(dungeon_generator, monster_list)
"""

from .base import MonsterSpawnStrategy
from .random_spawn import RandomSpawnStrategy
from .elite_group import EliteWithGroupStrategy
from .guarding_items import GuardingItemsStrategy

__all__ = [
    "MonsterSpawnStrategy",
    "RandomSpawnStrategy",
    "EliteWithGroupStrategy",
    "GuardingItemsStrategy",
]

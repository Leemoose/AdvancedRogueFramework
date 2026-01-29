"""
Entity Spawners
===============

Classes that handle spawning entities on dungeon floors.

This is the UNIFIED version that replaces:
- spawnparams.py (ItemSpawner, MonsterSpawner classes)
- dungeon_generation/spawning/item_spawner.py
- dungeon_generation/spawning/monster_spawner.py
"""

from __future__ import annotations
from typing import List, Optional, Any, Dict, Callable
from dataclasses import dataclass, field
import random
import logging

from .spawn_params import (
    SpawnParams,
    ItemSpawnParams,
    MonsterSpawnParams,
    InteractableSpawnParams,
)

logger = logging.getLogger(__name__)


class BaseSpawner:
    """
    Base class for entity spawners.

    Provides common functionality for filtering spawn params by
    depth, branch, and rarity.
    """

    def __init__(self, spawn_params: List[SpawnParams]):
        """
        Initialize the spawner with spawn parameters.

        Args:
            spawn_params: List of spawn parameter objects.
        """
        self.spawn_params = spawn_params
        self._categorize_by_rarity()

    def _categorize_by_rarity(self) -> None:
        """Sort spawn params into rarity buckets."""
        self._by_rarity: Dict[str, List[SpawnParams]] = {
            "Extra Common": [],
            "Common": [],
            "Rare": [],
            "Legendary": [],
        }

        for params in self.spawn_params:
            rarity = params.rarity
            if rarity in self._by_rarity:
                self._by_rarity[rarity].append(params)

    def get_allowed_at_depth(
        self,
        depth: int,
        branch: str = "all",
        rarity: Optional[str] = None
    ) -> List[SpawnParams]:
        """
        Get spawn params that can spawn at the given depth.

        Args:
            depth: Dungeon depth.
            branch: Dungeon branch.
            rarity: Optional filter by rarity.

        Returns:
            List of allowed spawn parameters.
        """
        source = self._by_rarity.get(rarity, self.spawn_params) if rarity else self.spawn_params

        return [
            p for p in source
            if p.allowed_at_depth(depth, branch)
        ]

    def weighted_choice(self, params: List[SpawnParams]) -> Optional[SpawnParams]:
        """
        Select a spawn param weighted by their weight values.

        Args:
            params: List of spawn parameters to choose from.

        Returns:
            Selected SpawnParams or None if empty.
        """
        if not params:
            return None

        total_weight = sum(p.weight for p in params)
        if total_weight <= 0:
            return random.choice(params)

        roll = random.uniform(0, total_weight)
        cumulative = 0

        for p in params:
            cumulative += p.weight
            if roll <= cumulative:
                return p

        return params[-1]  # Fallback


class ItemSpawner(BaseSpawner):
    """
    Spawns items on dungeon floors.

    Handles equipment, consumables, and other items with
    rarity-based distribution.
    """

    # Rarity distribution by floor: (common, rare, legendary)
    EQUIPMENT_DISTRIBUTIONS = [
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
    ]

    CONSUMABLE_DISTRIBUTIONS = [
        (0.7, 0.3, 0.0),  # Floor 1-10 (same for all)
    ] * 10

    def __init__(self, spawn_params: List[ItemSpawnParams]):
        """
        Initialize item spawner.

        Args:
            spawn_params: List of item spawn parameters.
        """
        super().__init__(spawn_params)

        # Separate items by type for different spawn logic
        self._equipment = [p for p in spawn_params if self._is_equipment(p)]
        self._consumables = [p for p in spawn_params if self._is_consumable(p)]
        self._scrolls = [p for p in spawn_params if self._is_scroll(p)]

        # Debug/testing force spawns
        self.force_spawns: List[tuple] = []

    @staticmethod
    def _is_equipment(params: ItemSpawnParams) -> bool:
        """Check if item params are for equipment."""
        if hasattr(params.entity, 'equipable'):
            return params.entity.equipable
        return False

    @staticmethod
    def _is_consumable(params: ItemSpawnParams) -> bool:
        """Check if item params are for consumables."""
        if hasattr(params.entity, 'equipment_type'):
            return params.entity.equipment_type in ["Potiorb", "Potion"]
        return False

    @staticmethod
    def _is_scroll(params: ItemSpawnParams) -> bool:
        """Check if item params are for scrolls."""
        if hasattr(params.entity, 'equipment_type'):
            return params.entity.equipment_type in ["Scrorb", "Scroll"]
        return False

    def count_equipment(self, depth: int) -> int:
        """Calculate number of equipment items to spawn."""
        return random.randint(int(2 + 0.2 * depth), int(3 + 0.3 * depth))

    def count_consumables(self, depth: int) -> int:
        """Calculate number of consumables to spawn."""
        return random.randint(int(2 + 0.1 * depth), int(3 + 0.2 * depth))

    def count_scrolls(self, depth: int) -> int:
        """Calculate number of scrolls to spawn."""
        return random.randint(int(2 + 0.1 * depth), int(3 + 0.2 * depth))

    def spawn_items(
        self,
        depth: int,
        branch: str = "Dungeon"
    ) -> List[Any]:
        """
        Generate items for a dungeon floor.

        Args:
            depth: Dungeon depth (1-10).
            branch: Dungeon branch name.

        Returns:
            List of item instances to place on the floor.
        """
        depth = min(depth, 10)  # Cap at floor 10 distributions
        items = []

        # Handle forced spawns (for debugging)
        for name, count in self.force_spawns:
            matching = [p for p in self.spawn_params if p.entity.name == name]
            if matching:
                for _ in range(count):
                    items.append(matching[0].get_fresh_copy())

        # Spawn equipment
        equipment_at_depth = self.get_allowed_at_depth(depth, branch)
        equipment_at_depth = [p for p in equipment_at_depth if self._is_equipment(p)]

        for _ in range(self.count_equipment(depth)):
            item = self._spawn_with_rarity(
                equipment_at_depth,
                depth,
                self.EQUIPMENT_DISTRIBUTIONS[depth - 1]
            )
            if item:
                items.append(item)

        # Spawn consumables
        consumables_at_depth = self.get_allowed_at_depth(depth, branch)
        consumables_at_depth = [p for p in consumables_at_depth if self._is_consumable(p)]

        for _ in range(self.count_consumables(depth)):
            item = self._spawn_with_rarity(
                consumables_at_depth,
                depth,
                self.CONSUMABLE_DISTRIBUTIONS[depth - 1]
            )
            if item:
                items.append(item)

        # Spawn scrolls
        scrolls_at_depth = self.get_allowed_at_depth(depth, branch)
        scrolls_at_depth = [p for p in scrolls_at_depth if self._is_scroll(p)]

        for _ in range(self.count_scrolls(depth)):
            item = self._spawn_with_rarity(
                scrolls_at_depth,
                depth,
                self.EQUIPMENT_DISTRIBUTIONS[depth - 1]  # Use equipment distribution
            )
            if item:
                items.append(item)

        return items

    def _spawn_with_rarity(
        self,
        params: List[ItemSpawnParams],
        depth: int,
        distribution: tuple
    ) -> Optional[Any]:
        """
        Spawn an item based on rarity distribution.

        Args:
            params: Available spawn parameters.
            depth: Current depth.
            distribution: (common_chance, rare_chance, legendary_chance)

        Returns:
            Spawned item or None.
        """
        if not params:
            return None

        # Split by rarity
        common = [p for p in params if p.rarity == "Common"]
        rare = [p for p in params if p.rarity == "Rare"]
        legendary = [p for p in params if p.rarity == "Legendary"]

        # Handle missing rarities with fallbacks
        if not rare:
            rare = common
        if not legendary:
            legendary = rare if rare else common

        # Roll for rarity
        roll = random.random()
        common_chance, rare_chance, legendary_chance = distribution

        if roll < common_chance and common:
            params_pool = common
        elif roll < common_chance + rare_chance and rare:
            params_pool = rare
        elif legendary:
            params_pool = legendary
        else:
            params_pool = common if common else params

        if not params_pool:
            return None

        # Select and create item
        selected = self.weighted_choice(params_pool)
        if selected and isinstance(selected, ItemSpawnParams):
            return selected.get_leveled_copy(depth)

        return None

    # Legacy method name
    def spawnItems(self, depth: int) -> List[Any]:
        """Legacy alias."""
        return self.spawn_items(depth)


class MonsterSpawner(BaseSpawner):
    """
    Spawns monsters on dungeon floors.

    Supports tiered encounters, pack spawning, and boss monsters.
    """

    # Rarity distribution by floor: (normal, elite)
    MONSTER_DISTRIBUTIONS = [
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
    ]

    def __init__(self, spawn_params: List[MonsterSpawnParams]):
        """
        Initialize monster spawner.

        Args:
            spawn_params: List of monster spawn parameters.
        """
        super().__init__(spawn_params)

        # Separate regular monsters from bosses
        self._normal_monsters = [p for p in spawn_params if not p.is_boss]
        self._boss_monsters = [p for p in spawn_params if p.is_boss]

        # Separate by special types
        self._elite_monsters = [
            p for p in self._normal_monsters
            if hasattr(p.entity, 'orb') and p.entity.orb
        ]
        self._regular_monsters = [
            p for p in self._normal_monsters
            if not hasattr(p.entity, 'orb') or not p.entity.orb
        ]

        # Debug/testing force spawns
        self.force_spawn: Optional[tuple] = None

    def count_monsters(self, depth: int) -> int:
        """Calculate number of monsters to spawn."""
        if depth >= 10:
            return 1  # Boss floor
        return random.randint(int(5 + 0.5 * depth), int(8 + 1.0 * depth))

    def _get_monster_level(self, depth: int) -> int:
        """
        Calculate monster level based on depth.

        This consolidates the duplicated random_level() functions.
        """
        if depth < 4:
            return random.randint(0, 1)
        elif depth < 7:
            return random.randint(2, 5)
        else:
            return random.randint(6, 9)

    def spawn_monsters(
        self,
        depth: int,
        branch: str = "Dungeon"
    ) -> List[Any]:
        """
        Generate monsters for a dungeon floor.

        Args:
            depth: Dungeon depth (1-10).
            branch: Dungeon branch name.

        Returns:
            List of monster instances to place on the floor.
        """
        depth = min(depth, 10)
        monsters = []

        # Handle special branches
        if branch == "Ocean":
            return self._spawn_ocean_monsters(depth)

        # Handle forced spawns (debugging)
        if self.force_spawn:
            name, count = self.force_spawn
            matching = [p for p in self.spawn_params if p.entity.name == name]
            if matching:
                for _ in range(count):
                    level = self._get_monster_level(depth)
                    monsters.append(matching[0].get_leveled_copy(level))

        # Get available monsters for this depth
        regular_at_depth = self.get_allowed_at_depth(depth, branch)
        regular_at_depth = [p for p in regular_at_depth if p in self._regular_monsters]

        elite_at_depth = self.get_allowed_at_depth(depth, branch)
        elite_at_depth = [p for p in elite_at_depth if p in self._elite_monsters]

        # Fallback if no elites available
        if not elite_at_depth:
            elite_at_depth = regular_at_depth

        # Spawn monsters
        distribution = self.MONSTER_DISTRIBUTIONS[depth - 1]

        for _ in range(self.count_monsters(depth)):
            roll = random.random()
            level = self._get_monster_level(depth)

            if roll < distribution[0] and regular_at_depth:
                # Normal monster
                selected = self.weighted_choice(regular_at_depth)
            elif elite_at_depth:
                # Elite/special monster
                selected = self.weighted_choice(elite_at_depth)
            elif regular_at_depth:
                # Fallback to normal
                selected = self.weighted_choice(regular_at_depth)
            else:
                continue

            if selected:
                monsters.append(selected.get_leveled_copy(level))

        return monsters

    def _spawn_ocean_monsters(self, depth: int) -> List[Any]:
        """Handle special ocean branch spawning."""
        monsters = []

        # Filter for water-capable monsters
        water_monsters = [
            p for p in self.spawn_params
            if hasattr(p.entity, 'attributes') and 'water' in p.entity.attributes
        ]

        if not water_monsters:
            logger.warning("No water monsters defined for Ocean branch")
            return monsters

        for _ in range(self.count_monsters(depth)):
            level = self._get_monster_level(depth)
            selected = self.weighted_choice(water_monsters)
            if selected:
                monsters.append(selected.get_leveled_copy(level))

        return monsters

    # Legacy method name
    def spawnMonsters(self, branch: str, depth: int) -> List[Any]:
        """Legacy alias."""
        return self.spawn_monsters(depth, branch)


class InteractableSpawner(BaseSpawner):
    """
    Spawns interactable objects like fountains, altars, and NPCs.
    """

    def spawn_interactables(
        self,
        depth: int,
        branch: str = "Dungeon"
    ) -> List[Any]:
        """
        Generate interactables for a dungeon floor.

        Args:
            depth: Dungeon depth.
            branch: Dungeon branch name.

        Returns:
            List of interactable instances.
        """
        interactables = []

        allowed = self.get_allowed_at_depth(depth, branch)

        for params in allowed:
            if isinstance(params, InteractableSpawnParams):
                # Unique items only spawn once
                if params.unique:
                    interactables.append(params.get_fresh_copy())
                else:
                    # Non-unique can spawn multiple times
                    count = random.randint(0, 2)
                    for _ in range(count):
                        interactables.append(params.get_fresh_copy())

        return interactables

"""
Spawn Parameters
================

Data classes that define spawn rules for entities.

This is the UNIFIED version that replaces:
- spawnparams.py (ItemSpawnParams, MonsterSpawnParams)
- dungeon_generation/spawning/spawn_params.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, List
import copy
import random

from src.core.constants import Rarity


@dataclass
class SpawnParams:
    """
    Base spawn parameters for any entity.

    Attributes:
        entity: The template entity to spawn (will be deep copied).
        min_floor: Minimum dungeon depth for this spawn.
        max_floor: Maximum dungeon depth for this spawn.
        branch: Which dungeon branch this can spawn in ("all" for any).
        rarity: Rarity classification affecting spawn chance.
        weight: Relative weight for random selection (higher = more common).
    """
    entity: Any
    min_floor: int = 1
    max_floor: int = 10
    branch: str = "all"
    rarity: str = "Common"
    weight: float = 1.0

    def allowed_at_depth(self, depth: int, branch: str = "all") -> bool:
        """
        Check if this entity can spawn at the given depth and branch.

        Args:
            depth: Current dungeon depth.
            branch: Current dungeon branch.

        Returns:
            True if spawning is allowed.
        """
        depth_ok = self.min_floor <= depth <= self.max_floor
        branch_ok = self.branch == "all" or self.branch == branch
        return depth_ok and branch_ok

    def get_fresh_copy(self) -> Any:
        """
        Create a deep copy of the template entity.

        Returns:
            A new instance of the entity.
        """
        return copy.deepcopy(self.entity)

    # Legacy method names for compatibility
    def AllowedAtDepth(self, depth: int, branch: str = "all") -> bool:
        """Legacy alias for allowed_at_depth."""
        return self.allowed_at_depth(depth, branch)

    def GetFreshCopy(self) -> Any:
        """Legacy alias for get_fresh_copy."""
        return self.get_fresh_copy()


@dataclass
class ItemSpawnParams(SpawnParams):
    """
    Spawn parameters for items.

    Additional Attributes:
        min_count: Minimum number to spawn per floor.
        max_count: Maximum number to spawn per floor.
        can_level: Whether the item can be enchanted/leveled.
    """
    min_count: int = 0
    max_count: int = 1
    can_level: bool = True

    def get_spawn_count(self) -> int:
        """
        Get random number of items to spawn.

        Returns:
            Number between min_count and max_count (inclusive).
        """
        return random.randint(self.min_count, self.max_count)

    def get_leveled_copy(self, depth: int) -> Any:
        """
        Get a copy with random level-ups based on depth.

        Args:
            depth: Current dungeon depth.

        Returns:
            Leveled copy of the item.
        """
        item = self.get_fresh_copy()

        if not self.can_level:
            return item

        if not hasattr(item, 'can_be_levelled') or not item.can_be_levelled:
            return item

        # Deeper floors have chance for higher level items
        level_ups = self._calculate_level_ups(depth)
        for _ in range(level_ups):
            if hasattr(item, 'level_up'):
                item.level_up()

        return item

    @staticmethod
    def _calculate_level_ups(depth: int) -> int:
        """
        Calculate number of level-ups based on depth.

        This consolidates the random_level() logic that was
        duplicated in multiple files.

        Args:
            depth: Current dungeon depth.

        Returns:
            Number of level-ups to apply.
        """
        if depth < 4:
            return 0
        elif depth < 7:
            return random.randint(0, 2)
        else:
            return random.randint(0, 3)

    # Legacy method names
    def GetNumberToSpawn(self) -> int:
        """Legacy alias."""
        return self.get_spawn_count()


@dataclass
class MonsterSpawnParams(SpawnParams):
    """
    Spawn parameters for monsters.

    Additional Attributes:
        group: Group identifier for pack spawning (e.g., "goblins").
        is_boss: Whether this is a boss monster.
        level_variance: Random variance in monster level.
    """
    group: Optional[str] = None
    is_boss: bool = False
    level_variance: int = 0

    def get_leveled_copy(self, depth: int) -> Any:
        """
        Get a copy with stats scaled for the given depth.

        Monsters get stat increases based on dungeon depth to
        maintain challenge as the player progresses.

        Args:
            depth: Current dungeon depth.

        Returns:
            Leveled copy of the monster.
        """
        monster = self.get_fresh_copy()

        # Apply level variance
        if self.level_variance > 0:
            level_adjust = random.randint(-self.level_variance, self.level_variance)
            depth = max(1, depth + level_adjust)

        # Level up the monster
        for level in range(depth):
            if hasattr(monster, 'character') and hasattr(monster.character, 'level_up'):
                # Alternate between stat combinations
                if level % 2 == 0:
                    monster.character.level_up(1, 0, 1, 0)  # str, dex, end, int
                else:
                    monster.character.level_up(0, 1, 0, 1)

                # Restore health/mana after level up
                if hasattr(monster.character, 'health') and hasattr(monster.character, 'max_health'):
                    monster.character.health = monster.character.max_health
                if hasattr(monster.character, 'mana') and hasattr(monster.character, 'max_mana'):
                    monster.character.mana = monster.character.max_mana

        return monster

    # Legacy method names
    def GetLeveledCopy(self, depth: int) -> Any:
        """Legacy alias."""
        return self.get_leveled_copy(depth)


@dataclass
class BossSpawnParams(MonsterSpawnParams):
    """
    Spawn parameters for boss monsters.

    Bosses spawn at specific depths and are guaranteed unique.
    """

    def __init__(
        self,
        monster: Any,
        depth: int,
        branch: str = "Dungeon",
        **kwargs
    ):
        """
        Create boss spawn params for a specific depth.

        Args:
            monster: The boss monster template.
            depth: The exact depth where this boss spawns.
            branch: Dungeon branch for the boss.
            **kwargs: Additional SpawnParams arguments.
        """
        super().__init__(
            entity=monster,
            min_floor=depth,
            max_floor=depth,
            branch=branch,
            is_boss=True,
            rarity="Legendary",
            **kwargs
        )


@dataclass
class InteractableSpawnParams(SpawnParams):
    """
    Spawn parameters for interactable objects.

    Used for things like fountains, altars, NPCs, etc.

    Additional Attributes:
        unique: Whether only one can exist per floor.
        requires_room: Whether it must spawn inside a room.
    """
    unique: bool = False
    requires_room: bool = True

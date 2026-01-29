"""
Base Monster Spawn Strategy
============================

Abstract base class defining the interface for monster spawning strategies.
Strategies handle how and where monsters are placed in the dungeon.

Usage:
    class MyStrategy(MonsterSpawnStrategy):
        def place_monsters(self, dungeon_generator, monsters):
            # Custom placement logic
            pass
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable, Any, TYPE_CHECKING
import random

from logging_config import get_logger

if TYPE_CHECKING:
    # Avoid circular imports - only import for type checking
    from dungeon_generation.mapping import DungeonGenerator

logger = get_logger(__name__)


class MonsterSpawnStrategy(ABC):
    """
    Abstract base class for monster spawning strategies.

    Defines the interface that all spawn strategies must implement,
    along with helper methods for finding valid spawn locations.
    """

    @abstractmethod
    def place_monsters(
        self,
        dungeon_generator: "DungeonGenerator",
        monsters: List[Any]
    ) -> None:
        """
        Place monsters in the dungeon.

        Args:
            dungeon_generator: The dungeon generator instance providing
                map access and placement methods.
            monsters: List of monsters to place. May contain individual
                monsters or lists of monsters (packs).
        """
        pass

    def find_valid_location(
        self,
        dungeon_generator: "DungeonGenerator",
        condition: Optional[Callable[[Tuple[int, int]], bool]] = None,
        max_attempts: int = 1000
    ) -> Optional[Tuple[int, int]]:
        """
        Find a valid spawn location that satisfies the given condition.

        Args:
            dungeon_generator: The dungeon generator instance.
            condition: Optional callable that takes (x, y) and returns True
                if the location is valid. If None, only checks passability.
            max_attempts: Maximum number of random attempts before giving up.

        Returns:
            A tuple (x, y) of a valid location, or None if no location found.
        """
        width = dungeon_generator.get_width()
        height = dungeon_generator.get_height()

        for attempt in range(max_attempts):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if not dungeon_generator.get_passable((x, y)):
                continue

            if condition is not None and not condition((x, y)):
                continue

            return (x, y)

        logger.warning(
            "Could not find valid spawn location after %d attempts",
            max_attempts
        )
        return None

    def find_valid_locations_in_area(
        self,
        dungeon_generator: "DungeonGenerator",
        center: Tuple[int, int],
        radius: int,
        count: int,
        condition: Optional[Callable[[Tuple[int, int]], bool]] = None,
        shuffle: bool = True
    ) -> List[Tuple[int, int]]:
        """
        Find multiple valid locations within an area around a center point.

        Args:
            dungeon_generator: The dungeon generator instance.
            center: The center point (x, y) to search around.
            radius: The search radius (manhattan distance).
            count: The number of valid locations needed.
            condition: Optional additional condition for valid locations.
            shuffle: Whether to shuffle the search order for variety.

        Returns:
            List of valid (x, y) locations found. May contain fewer than
            'count' locations if not enough valid spots exist in the area.
        """
        cx, cy = center

        # Generate all offsets within the radius
        offsets = [
            (dx, dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
        ]

        if shuffle:
            random.shuffle(offsets)

        locations: List[Tuple[int, int]] = []

        for dx, dy in offsets:
            if len(locations) >= count:
                break

            x, y = cx + dx, cy + dy

            if not dungeon_generator.get_passable((x, y)):
                continue

            if condition is not None and not condition((x, y)):
                continue

            locations.append((x, y))

        return locations

    def is_on_stairs(
        self,
        dungeon_generator: "DungeonGenerator",
        x: int,
        y: int
    ) -> bool:
        """
        Check if a location is on stairs.

        Args:
            dungeon_generator: The dungeon generator instance.
            x: The x coordinate.
            y: The y coordinate.

        Returns:
            True if the location is on stairs, False otherwise.
        """
        return dungeon_generator.get_is_on_stairs(x, y)

    def is_in_corridor(
        self,
        dungeon_generator: "DungeonGenerator",
        x: int,
        y: int
    ) -> bool:
        """
        Check if a location is in a corridor (narrow passage).

        Args:
            dungeon_generator: The dungeon generator instance.
            x: The x coordinate.
            y: The y coordinate.

        Returns:
            True if the location is in a corridor, False otherwise.
        """
        return dungeon_generator.get_is_in_corridor(x, y)

    def make_spawn_condition(
        self,
        dungeon_generator: "DungeonGenerator",
        avoid_corridors: bool = False,
        avoid_stairs: bool = True
    ) -> Callable[[Tuple[int, int]], bool]:
        """
        Create a spawn condition function based on common restrictions.

        Args:
            dungeon_generator: The dungeon generator instance.
            avoid_corridors: If True, exclude corridor locations.
            avoid_stairs: If True, exclude stair locations.

        Returns:
            A callable that takes (x, y) and returns True if valid.
        """
        def condition(location: Tuple[int, int]) -> bool:
            x, y = location

            if avoid_stairs and self.is_on_stairs(dungeon_generator, x, y):
                return False

            if avoid_corridors and self.is_in_corridor(dungeon_generator, x, y):
                return False

            return True

        return condition

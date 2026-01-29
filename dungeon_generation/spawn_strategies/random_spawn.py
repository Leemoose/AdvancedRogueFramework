"""
Random Spawn Strategy
=====================

A spawn strategy that places monsters at random valid locations
in the dungeon. Supports both individual monsters and packs (groups
of monsters placed in clusters).

This strategy is refactored from the original mapping_utility.py
placement logic, with bounded retries instead of infinite loops.

Usage:
    strategy = RandomSpawnStrategy(
        avoid_corridors=False,
        avoid_stairs=True,
        max_attempts=1000
    )
    strategy.place_monsters(dungeon_generator, monsters)
"""

from typing import List, Tuple, Optional, Any, TYPE_CHECKING
import random

from logging_config import get_logger

from .base import MonsterSpawnStrategy

if TYPE_CHECKING:
    from dungeon_generation.mapping import DungeonGenerator

logger = get_logger(__name__)


class RandomSpawnStrategy(MonsterSpawnStrategy):
    """
    Spawns monsters at random valid locations in the dungeon.

    Handles both individual monsters and packs (lists of monsters).
    Individual monsters are placed at random passable locations,
    while packs are placed in clusters within a search radius.

    Attributes:
        avoid_corridors: If True, monsters won't spawn in corridors.
        avoid_stairs: If True, monsters won't spawn on stair tiles.
        max_attempts: Maximum attempts to find a valid location before
            giving up (prevents infinite loops).
        pack_search_radius: Radius to search for adjacent tiles when
            placing monster packs.
    """

    def __init__(
        self,
        avoid_corridors: bool = False,
        avoid_stairs: bool = True,
        max_attempts: int = 1000,
        pack_search_radius: int = 2
    ) -> None:
        """
        Initialize the random spawn strategy.

        Args:
            avoid_corridors: If True, exclude corridor locations from spawning.
                Defaults to False.
            avoid_stairs: If True, exclude stair locations from spawning.
                Defaults to True.
            max_attempts: Maximum number of random location attempts before
                giving up on placing a monster. Defaults to 1000.
            pack_search_radius: Radius around the anchor point to search for
                pack member locations. Defaults to 2 (covers a 5x5 area).
        """
        self.avoid_corridors = avoid_corridors
        self.avoid_stairs = avoid_stairs
        self.max_attempts = max_attempts
        self.pack_search_radius = pack_search_radius

    def place_monsters(
        self,
        dungeon_generator: "DungeonGenerator",
        monsters: List[Any]
    ) -> None:
        """
        Place all monsters in the dungeon.

        Iterates through the monster list and handles each entry based
        on whether it's an individual monster or a pack (list of monsters).

        Args:
            dungeon_generator: The dungeon generator instance.
            monsters: List of monsters to place. Individual monsters are
                placed directly, while lists are treated as packs.
        """
        logger.debug(
            "Spawning monsters for depth %d, branch %s",
            dungeon_generator.get_depth(),
            dungeon_generator.get_branch()
        )

        placed_count = 0
        pack_count = 0

        for monster_entry in monsters:
            if isinstance(monster_entry, list):
                # Monster entry is a pack (list of monsters)
                if self._place_pack(dungeon_generator, monster_entry):
                    pack_count += 1
                    placed_count += len(monster_entry)
            else:
                # Monster entry is a single monster
                if self._place_single_monster(dungeon_generator, monster_entry):
                    placed_count += 1

        logger.debug(
            "Finished spawning monsters: %d individuals, %d packs (%d total placed)",
            placed_count - (pack_count * 2 if pack_count > 0 else 0),  # Approximate
            pack_count,
            placed_count
        )

    def _place_single_monster(
        self,
        dungeon_generator: "DungeonGenerator",
        monster: Any
    ) -> bool:
        """
        Place a single monster at a random valid location.

        Args:
            dungeon_generator: The dungeon generator instance.
            monster: The monster to place.

        Returns:
            True if the monster was successfully placed, False otherwise.
        """
        condition = self.make_spawn_condition(
            dungeon_generator,
            avoid_corridors=self.avoid_corridors,
            avoid_stairs=self.avoid_stairs
        )

        location = self.find_valid_location(
            dungeon_generator,
            condition=condition,
            max_attempts=self.max_attempts
        )

        if location is None:
            logger.warning(
                "Failed to find valid location for monster: %s",
                getattr(monster, 'name', str(monster))
            )
            return False

        x, y = location
        dungeon_generator.place_monster_at_location(monster, x, y)
        logger.debug(
            "Placed monster %s at (%d, %d)",
            getattr(monster, 'name', str(monster)),
            x, y
        )
        return True

    def _place_pack(
        self,
        dungeon_generator: "DungeonGenerator",
        pack: List[Any]
    ) -> bool:
        """
        Place a pack of monsters in a cluster.

        Finds an anchor point with enough adjacent passable tiles to
        fit all pack members, then places the monsters at those locations.

        Args:
            dungeon_generator: The dungeon generator instance.
            pack: List of monsters to place as a pack.

        Returns:
            True if all pack members were successfully placed, False otherwise.
        """
        pack_size = len(pack)
        if pack_size == 0:
            return True

        logger.debug("Placing pack of %d monsters", pack_size)

        condition = self.make_spawn_condition(
            dungeon_generator,
            avoid_corridors=self.avoid_corridors,
            avoid_stairs=self.avoid_stairs
        )

        # Try to find an anchor point with enough nearby valid locations
        locations = self._find_pack_locations(
            dungeon_generator,
            pack_size,
            condition
        )

        if locations is None:
            logger.warning(
                "Failed to find valid locations for pack of %d monsters",
                pack_size
            )
            # Fall back to placing monsters individually
            return self._place_pack_individually(dungeon_generator, pack)

        # Place each monster in the pack at its assigned location
        for i, monster in enumerate(pack):
            if i >= len(locations):
                logger.warning(
                    "Not enough locations found for pack member %d/%d",
                    i + 1, pack_size
                )
                break

            x, y = locations[i]
            dungeon_generator.place_monster_at_location(monster, x, y)
            logger.debug(
                "Placed pack member %s at (%d, %d)",
                getattr(monster, 'name', str(monster)),
                x, y
            )

        logger.debug("Pack placed successfully")
        return True

    def _find_pack_locations(
        self,
        dungeon_generator: "DungeonGenerator",
        pack_size: int,
        condition: Any
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find a set of adjacent locations suitable for a monster pack.

        Searches for an anchor point with enough passable tiles in the
        surrounding area to accommodate all pack members.

        Args:
            dungeon_generator: The dungeon generator instance.
            pack_size: Number of locations needed.
            condition: The spawn condition function.

        Returns:
            List of (x, y) locations if found, None otherwise.
        """
        for attempt in range(self.max_attempts):
            # Find a random anchor point
            anchor = self.find_valid_location(
                dungeon_generator,
                condition=condition,
                max_attempts=1  # Single attempt per iteration
            )

            if anchor is None:
                continue

            # Search for enough valid locations around the anchor
            locations = self.find_valid_locations_in_area(
                dungeon_generator,
                center=anchor,
                radius=self.pack_search_radius,
                count=pack_size,
                condition=condition,
                shuffle=True  # Randomize arrangement
            )

            if len(locations) >= pack_size:
                return locations

        return None

    def _place_pack_individually(
        self,
        dungeon_generator: "DungeonGenerator",
        pack: List[Any]
    ) -> bool:
        """
        Fallback: place pack members as individual monsters.

        Used when we can't find a location with enough adjacent tiles
        for the entire pack.

        Args:
            dungeon_generator: The dungeon generator instance.
            pack: List of monsters to place individually.

        Returns:
            True if any monsters were placed, False if none could be placed.
        """
        logger.debug(
            "Falling back to individual placement for pack of %d",
            len(pack)
        )

        placed_any = False
        for monster in pack:
            if self._place_single_monster(dungeon_generator, monster):
                placed_any = True

        return placed_any

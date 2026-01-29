"""
Guarding Items Monster Spawn Strategy
=====================================

Monster spawn strategy that places monsters near valuable items,
creating "guards" that protect rare and legendary loot.

This strategy prioritizes placing monsters near high-value items
while distributing remaining monsters randomly across the map.
"""

import random
from typing import List, Optional, Tuple, Set, TYPE_CHECKING

from logging_config import get_logger

from .base import MonsterSpawnStrategy

if TYPE_CHECKING:
    from ..mapping import DungeonGenerator

logger = get_logger(__name__)

# Rarity tiers in order of priority (highest first)
RARITY_PRIORITY = {
    "Mythic": 5,
    "YENDORB": 5,
    "Legendary": 4,
    "Rare": 3,
    "Common": 1,
    "Extra Common": 0,
}


class GuardingItemsStrategy(MonsterSpawnStrategy):
    """
    Monster spawn strategy that positions monsters to guard valuable items.

    This strategy finds items already placed on the map and positions monsters
    nearby to create a "guarding" effect. Rare and legendary items receive
    priority for guard placement.

    Attributes:
        guard_radius_min: Minimum distance from item for guard placement (default: 2)
        guard_radius_max: Maximum distance from item for guard placement (default: 4)
        guard_chance: Probability a monster guards an item vs random placement (default: 0.5)
        prefer_rare_items: Whether to prioritize rare/legendary items (default: True)

    Example:
        strategy = GuardingItemsStrategy(
            guard_radius_min=2,
            guard_radius_max=4,
            guard_chance=0.7,
            prefer_rare_items=True
        )
        strategy.place_monsters(monsters, dungeon_generator)
    """

    def __init__(
        self,
        guard_radius_min: int = 2,
        guard_radius_max: int = 4,
        guard_chance: float = 0.5,
        prefer_rare_items: bool = True
    ):
        """
        Initialize the GuardingItemsStrategy.

        Args:
            guard_radius_min: Minimum tiles from item for guard placement (default: 2)
            guard_radius_max: Maximum tiles from item for guard placement (default: 4)
            guard_chance: Probability (0-1) that a monster guards an item (default: 0.5)
            prefer_rare_items: Prioritize guarding rare/legendary items (default: True)
        """
        self.guard_radius_min = guard_radius_min
        self.guard_radius_max = guard_radius_max
        self.guard_chance = guard_chance
        self.prefer_rare_items = prefer_rare_items

        # Track which items already have guards assigned
        self._guarded_items: Set[int] = set()

        logger.info(
            "GuardingItemsStrategy initialized: radius=%d-%d, chance=%.2f, prefer_rare=%s",
            guard_radius_min, guard_radius_max, guard_chance, prefer_rare_items
        )

    def place_monsters(
        self,
        dungeon_generator: 'DungeonGenerator',
        monsters: List
    ) -> None:
        """
        Place monsters on the map, prioritizing positions near valuable items.

        Monsters are placed in the following order:
        1. Monsters assigned to guard valuable items (based on guard_chance)
        2. Remaining monsters placed randomly

        Args:
            monsters: List of monster objects to place (can include packs as lists)
            dungeon_generator: The dungeon generator with tile_map, item_map, etc.

        Returns:
            List of monsters that were successfully placed
        """
        logger.debug(
            "Placing %d monster entries with guarding strategy",
            len(monsters)
        )

        # Reset guarded items tracking for this placement session
        self._guarded_items.clear()

        # Get all items on the map and sort by rarity if preferred
        items = self._get_sorted_items(dungeon_generator)
        logger.debug("Found %d items on map for potential guarding", len(items))

        placed_monsters: List = []
        monsters_to_place = list(monsters)  # Copy to avoid modifying original

        # First pass: assign guards to items
        for item in items:
            if not monsters_to_place:
                break

            # Check if we should assign a guard to this item
            if random.random() > self.guard_chance:
                continue

            # Skip already guarded items
            item_id = getattr(item, 'id_tag', id(item))
            if item_id in self._guarded_items:
                continue

            # Try to place a monster as a guard
            monster = monsters_to_place[0]
            if self._place_guard(monster, item, dungeon_generator):
                monsters_to_place.pop(0)
                self._guarded_items.add(item_id)

                if isinstance(monster, list):
                    placed_monsters.extend(monster)
                    logger.debug(
                        "Placed pack of %d monsters guarding %s",
                        len(monster), getattr(item, 'name', 'item')
                    )
                else:
                    placed_monsters.append(monster)
                    logger.debug(
                        "Placed %s guarding %s",
                        getattr(monster, 'name', 'monster'),
                        getattr(item, 'name', 'item')
                    )

        # Second pass: place remaining monsters randomly
        for monster in monsters_to_place:
            if self._place_random(monster, dungeon_generator):
                if isinstance(monster, list):
                    placed_monsters.extend(monster)
                else:
                    placed_monsters.append(monster)

        logger.info(
            "Guarding strategy complete: %d monsters placed, %d items guarded",
            len(placed_monsters), len(self._guarded_items)
        )

        return placed_monsters

    def _get_sorted_items(self, dungeon_generator: 'DungeonGenerator') -> List:
        """
        Get all items from the map, optionally sorted by rarity.

        Args:
            dungeon_generator: The dungeon generator containing item_map

        Returns:
            List of items, sorted by rarity priority if prefer_rare_items is True
        """
        items = dungeon_generator.item_map.get_all_entities()

        if not self.prefer_rare_items:
            return items

        # Sort by rarity priority (highest first)
        def get_rarity_priority(item) -> int:
            rarity = getattr(item, 'rarity', 'Common')
            return RARITY_PRIORITY.get(rarity, 1)

        sorted_items = sorted(items, key=get_rarity_priority, reverse=True)

        if sorted_items:
            logger.debug(
                "Sorted %d items by rarity, highest: %s (%s)",
                len(sorted_items),
                getattr(sorted_items[0], 'name', 'unknown'),
                getattr(sorted_items[0], 'rarity', 'Common')
            )

        return sorted_items

    def _place_guard(
        self,
        monster,
        item,
        dungeon_generator: 'DungeonGenerator'
    ) -> bool:
        """
        Place a monster (or pack) as a guard near an item.

        Args:
            monster: Monster object or list of monsters (pack) to place
            item: Item to guard
            dungeon_generator: The dungeon generator

        Returns:
            True if placement was successful, False otherwise
        """
        item_x = item.x
        item_y = item.y

        # Get valid guard positions within the radius
        guard_positions = self._get_guard_positions(
            item_x, item_y, dungeon_generator
        )

        if not guard_positions:
            logger.debug(
                "No valid guard positions near item at (%d, %d)",
                item_x, item_y
            )
            return False

        if isinstance(monster, list):
            # Place a pack of monsters
            return self._place_pack_near_item(
                monster, guard_positions, dungeon_generator
            )
        else:
            # Place a single monster
            position = random.choice(guard_positions)
            dungeon_generator.place_monster_at_location(
                monster, position[0], position[1]
            )
            return True

    def _get_guard_positions(
        self,
        item_x: int,
        item_y: int,
        dungeon_generator: 'DungeonGenerator'
    ) -> List[Tuple[int, int]]:
        """
        Get all valid positions for a guard around an item.

        Valid positions are:
        - Within guard_radius_min to guard_radius_max of the item
        - Passable terrain
        - Not on the item itself

        Args:
            item_x: Item X coordinate
            item_y: Item Y coordinate
            dungeon_generator: The dungeon generator

        Returns:
            List of (x, y) tuples representing valid guard positions
        """
        positions: List[Tuple[int, int]] = []

        # Check all positions within the guard radius
        for dx in range(-self.guard_radius_max, self.guard_radius_max + 1):
            for dy in range(-self.guard_radius_max, self.guard_radius_max + 1):
                x = item_x + dx
                y = item_y + dy

                # Skip the item's own position
                if dx == 0 and dy == 0:
                    continue

                # Check distance is within bounds
                distance = abs(dx) + abs(dy)  # Manhattan distance
                if distance < self.guard_radius_min:
                    continue
                if distance > self.guard_radius_max:
                    continue

                # Check if position is valid for monster placement
                if dungeon_generator.get_passable((x, y)):
                    positions.append((x, y))

        return positions

    def _place_pack_near_item(
        self,
        pack: List,
        guard_positions: List[Tuple[int, int]],
        dungeon_generator: 'DungeonGenerator'
    ) -> bool:
        """
        Place a pack of monsters near an item.

        Tries to find enough contiguous positions for the entire pack.

        Args:
            pack: List of monster objects to place
            guard_positions: Available positions near the item
            dungeon_generator: The dungeon generator

        Returns:
            True if the entire pack was placed, False otherwise
        """
        pack_size = len(pack)

        if len(guard_positions) < pack_size:
            logger.debug(
                "Not enough guard positions (%d) for pack of %d",
                len(guard_positions), pack_size
            )
            return False

        # Shuffle positions and take enough for the pack
        random.shuffle(guard_positions)
        selected_positions = guard_positions[:pack_size]

        # Place each monster in the pack
        for i, monster in enumerate(pack):
            x, y = selected_positions[i]
            dungeon_generator.place_monster_at_location(monster, x, y)

        return True

    def _place_random(
        self,
        monster,
        dungeon_generator: 'DungeonGenerator'
    ) -> bool:
        """
        Place a monster (or pack) at a random location.

        Falls back to random placement for monsters not assigned as guards.

        Args:
            monster: Monster object or list of monsters (pack) to place
            dungeon_generator: The dungeon generator

        Returns:
            True if placement was successful, False otherwise
        """
        if isinstance(monster, list):
            return self._place_random_pack(monster, dungeon_generator)
        else:
            return self._place_random_single(monster, dungeon_generator)

    def _place_random_single(
        self,
        monster,
        dungeon_generator: 'DungeonGenerator'
    ) -> bool:
        """
        Place a single monster at a random passable location.

        Args:
            monster: Monster object to place
            dungeon_generator: The dungeon generator

        Returns:
            True if placement was successful
        """
        x, y = dungeon_generator.get_random_passable_location()
        dungeon_generator.place_monster_at_location(monster, x, y)
        logger.debug(
            "Placed %s randomly at (%d, %d)",
            getattr(monster, 'name', 'monster'), x, y
        )
        return True

    def _place_random_pack(
        self,
        pack: List,
        dungeon_generator: 'DungeonGenerator'
    ) -> bool:
        """
        Place a pack of monsters at random adjacent locations.

        Finds a location with enough adjacent passable tiles for the pack.

        Args:
            pack: List of monster objects to place
            dungeon_generator: The dungeon generator

        Returns:
            True if the pack was successfully placed
        """
        pack_size = len(pack)
        max_attempts = 100
        area_to_check = 2

        # Generate direction offsets for checking adjacent tiles
        directions = [
            (dx, dy)
            for dx in range(-area_to_check, area_to_check + 1)
            for dy in range(-area_to_check, area_to_check + 1)
        ]

        for attempt in range(max_attempts):
            x, y = dungeon_generator.get_random_passable_location()
            locations: List[Tuple[int, int]] = []

            random.shuffle(directions)
            for dx, dy in directions:
                check_x, check_y = x + dx, y + dy
                if dungeon_generator.get_passable((check_x, check_y)):
                    locations.append((check_x, check_y))
                    if len(locations) >= pack_size:
                        break

            if len(locations) >= pack_size:
                # Place the pack
                for i, monster in enumerate(pack):
                    loc_x, loc_y = locations[i]
                    dungeon_generator.place_monster_at_location(monster, loc_x, loc_y)

                logger.debug(
                    "Placed pack of %d monsters randomly near (%d, %d)",
                    pack_size, x, y
                )
                return True

        logger.warning(
            "Failed to place pack of %d monsters after %d attempts",
            pack_size, max_attempts
        )
        return False

    def reset(self) -> None:
        """
        Reset the strategy state for a new dungeon level.

        Clears the tracked guarded items set.
        """
        self._guarded_items.clear()
        logger.debug("GuardingItemsStrategy reset")

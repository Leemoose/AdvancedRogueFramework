"""
Map System
==========

Provides 2D grid-based maps for storing entities, tiles, and tracking data.

This module fixes the critical list initialization bug from the original
maps.py and provides a cleaner, more robust interface.

Key Classes:
- GameMap: Base class for all 2D maps
- EntityMap: Stores entities (monsters, items) by position
- TileMap: Stores terrain tiles with visibility tracking
- TrackingMap: Stores tracking data and navigation info
"""

from __future__ import annotations
from typing import (
    TypeVar, Generic, Optional, List, Iterator,
    Tuple, Any, Callable, Dict
)
from dataclasses import dataclass, field
import random
import logging

from src.core.constants import NO_ENTITY

# Type variable for generic map contents
T = TypeVar('T')

# Logger for map operations
logger = logging.getLogger(__name__)


@dataclass
class MapBounds:
    """
    Represents the boundaries of a map region.

    Attributes:
        x_min: Minimum x coordinate (inclusive)
        y_min: Minimum y coordinate (inclusive)
        x_max: Maximum x coordinate (exclusive)
        y_max: Maximum y coordinate (exclusive)
    """
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    def contains(self, x: int, y: int) -> bool:
        """Check if a point is within bounds."""
        return (self.x_min <= x < self.x_max and
                self.y_min <= y < self.y_max)

    @property
    def width(self) -> int:
        return self.x_max - self.x_min

    @property
    def height(self) -> int:
        return self.y_max - self.y_min


class GameMap(Generic[T]):
    """
    Base class for 2D grid-based maps.

    This provides the core functionality for storing and retrieving
    data in a 2D grid structure. It properly initializes the 2D list
    to avoid the aliasing bug in the original code.

    Type Parameters:
        T: The type of data stored in each cell.

    Attributes:
        width: Number of columns in the map.
        height: Number of rows in the map.

    Example:
        >>> game_map = GameMap(10, 10, default=0)
        >>> game_map.set(5, 5, 42)
        >>> game_map.get(5, 5)
        42
    """

    def __init__(
        self,
        width: int,
        height: int,
        default: T = None
    ):
        """
        Initialize a new map.

        Args:
            width: Number of columns.
            height: Number of rows.
            default: Default value for each cell.

        Note:
            This properly creates independent rows to avoid the aliasing
            bug where modifying one cell affects others.
        """
        self.width = width
        self.height = height
        self._default = default

        # CRITICAL FIX: Create each row independently
        # The original code used [[-1] * height] * width which creates
        # width references to the SAME list object. This version creates
        # independent lists for each column.
        self._grid: List[List[T]] = [
            [default for _ in range(height)]
            for _ in range(width)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within map boundaries.

        Args:
            x: Horizontal position to check.
            y: Vertical position to check.

        Returns:
            True if the position is valid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int) -> Optional[T]:
        """
        Get the value at a position.

        Args:
            x: Horizontal position.
            y: Vertical position.

        Returns:
            The value at (x, y) or None if out of bounds.
        """
        if self.in_bounds(x, y):
            return self._grid[x][y]
        return None

    def set(self, x: int, y: int, value: T) -> bool:
        """
        Set the value at a position.

        Args:
            x: Horizontal position.
            y: Vertical position.
            value: Value to store.

        Returns:
            True if successful, False if out of bounds.
        """
        if self.in_bounds(x, y):
            self._grid[x][y] = value
            return True
        logger.warning(f"Attempted to set value outside map bounds: ({x}, {y})")
        return False

    def clear(self, x: int, y: int) -> bool:
        """
        Reset a position to the default value.

        Args:
            x: Horizontal position.
            y: Vertical position.

        Returns:
            True if successful, False if out of bounds.
        """
        return self.set(x, y, self._default)

    def fill(self, value: T) -> None:
        """
        Fill the entire map with a value.

        Args:
            value: Value to fill the map with.
        """
        for x in range(self.width):
            for y in range(self.height):
                self._grid[x][y] = value

    def fill_region(
        self,
        x_start: int,
        y_start: int,
        x_end: int,
        y_end: int,
        value: T
    ) -> None:
        """
        Fill a rectangular region with a value.

        Args:
            x_start: Left boundary (inclusive).
            y_start: Top boundary (inclusive).
            x_end: Right boundary (exclusive).
            y_end: Bottom boundary (exclusive).
            value: Value to fill with.
        """
        for x in range(max(0, x_start), min(self.width, x_end)):
            for y in range(max(0, y_start), min(self.height, y_end)):
                self._grid[x][y] = value

    def get_random_position(
        self,
        condition: Optional[Callable[[T], bool]] = None
    ) -> Optional[Tuple[int, int]]:
        """
        Get a random position, optionally matching a condition.

        Args:
            condition: Optional function that returns True for valid cells.

        Returns:
            (x, y) tuple or None if no valid position found after many attempts.
        """
        max_attempts = self.width * self.height * 2

        for _ in range(max_attempts):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if condition is None or condition(self._grid[x][y]):
                return (x, y)

        return None

    def iterate_all(self) -> Iterator[Tuple[int, int, T]]:
        """
        Iterate over all cells in the map.

        Yields:
            (x, y, value) tuples for each cell.
        """
        for x in range(self.width):
            for y in range(self.height):
                yield x, y, self._grid[x][y]

    def iterate_region(
        self,
        x_start: int,
        y_start: int,
        x_end: int,
        y_end: int
    ) -> Iterator[Tuple[int, int, T]]:
        """
        Iterate over cells in a rectangular region.

        Args:
            x_start: Left boundary (inclusive).
            y_start: Top boundary (inclusive).
            x_end: Right boundary (exclusive).
            y_end: Bottom boundary (exclusive).

        Yields:
            (x, y, value) tuples for each cell in the region.
        """
        for x in range(max(0, x_start), min(self.width, x_end)):
            for y in range(max(0, y_start), min(self.height, y_end)):
                yield x, y, self._grid[x][y]

    def copy(self) -> 'GameMap[T]':
        """
        Create a deep copy of this map.

        Returns:
            New GameMap with copied data.
        """
        new_map = GameMap(self.width, self.height, self._default)
        for x in range(self.width):
            for y in range(self.height):
                new_map._grid[x][y] = self._grid[x][y]
        return new_map

    def get_raw_grid(self) -> List[List[T]]:
        """
        Get direct access to the underlying grid.

        Returns:
            The 2D list backing this map.

        Warning:
            Modifying the returned list will affect the map.
            Use copy() if you need an independent copy.
        """
        return self._grid

    # Legacy compatibility aliases
    def get_map(self) -> List[List[T]]:
        """Legacy alias for get_raw_grid."""
        return self._grid

    def get_width(self) -> int:
        """Legacy accessor."""
        return self.width

    def get_height(self) -> int:
        """Legacy accessor."""
        return self.height

    def in_map(self, x: int, y: int) -> bool:
        """Legacy alias for in_bounds."""
        return self.in_bounds(x, y)


class EntityMap(GameMap[Any]):
    """
    Map specialized for storing game entities.

    Entities are stored by reference and can be retrieved by position.
    Also maintains a list of all entities for iteration.

    This is used for monster maps and item maps.
    """

    def __init__(self, width: int, height: int):
        """
        Initialize an entity map.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        super().__init__(width, height, default=NO_ENTITY)
        self._entities: List[Any] = []

    def place_entity(self, entity: Any) -> bool:
        """
        Place an entity on the map at its current position.

        Args:
            entity: Entity with x and y attributes.

        Returns:
            True if successfully placed.
        """
        x, y = entity.x, entity.y

        if not self.in_bounds(x, y):
            logger.warning(f"Cannot place entity outside map: {entity} at ({x}, {y})")
            return False

        self.set(x, y, entity)
        if entity not in self._entities:
            self._entities.append(entity)
        return True

    def place_thing(self, entity: Any) -> bool:
        """Legacy alias for place_entity."""
        return self.place_entity(entity)

    def remove_entity(self, entity: Any) -> bool:
        """
        Remove an entity from the map.

        Args:
            entity: Entity to remove.

        Returns:
            True if successfully removed.
        """
        x, y = entity.x, entity.y

        if self.in_bounds(x, y) and self.get(x, y) == entity:
            self.clear(x, y)

        if entity in self._entities:
            self._entities.remove(entity)
            return True
        return False

    def remove_thing(self, entity: Any) -> bool:
        """Legacy alias for remove_entity."""
        return self.remove_entity(entity)

    def move_entity(self, entity: Any, new_x: int, new_y: int) -> bool:
        """
        Move an entity to a new position.

        Args:
            entity: Entity to move.
            new_x: New x coordinate.
            new_y: New y coordinate.

        Returns:
            True if move was successful.
        """
        if not self.in_bounds(new_x, new_y):
            return False

        old_x, old_y = entity.x, entity.y

        # Clear old position if this entity was there
        if self.in_bounds(old_x, old_y) and self.get(old_x, old_y) == entity:
            self.clear(old_x, old_y)

        # Update entity position
        entity.x = new_x
        entity.y = new_y

        # Place at new position
        self.set(new_x, new_y, entity)
        return True

    def get_entity(self, x: int, y: int) -> Optional[Any]:
        """
        Get the entity at a position.

        Args:
            x: Horizontal position.
            y: Vertical position.

        Returns:
            Entity at the position, or None if empty/out of bounds.
        """
        result = self.get(x, y)
        return None if result == NO_ENTITY else result

    def has_entity(self, x: int, y: int) -> bool:
        """
        Check if there's an entity at a position.

        Args:
            x: Horizontal position.
            y: Vertical position.

        Returns:
            True if an entity exists at the position.
        """
        return self.get(x, y) != NO_ENTITY

    def get_has_entity(self, x: int, y: int) -> bool:
        """Legacy alias for has_entity."""
        return self.has_entity(x, y)

    def get_has_no_entity(self, x: int, y: int) -> bool:
        """Check if a position is empty."""
        return self.in_bounds(x, y) and not self.has_entity(x, y)

    def get_all_entities(self) -> List[Any]:
        """
        Get a list of all entities on the map.

        Returns:
            List of all entities.
        """
        return self._entities.copy()

    def get_entities_in_region(
        self,
        x_start: int,
        y_start: int,
        x_end: int,
        y_end: int
    ) -> List[Any]:
        """
        Get all entities within a rectangular region.

        Args:
            x_start: Left boundary (inclusive).
            y_start: Top boundary (inclusive).
            x_end: Right boundary (exclusive).
            y_end: Bottom boundary (exclusive).

        Returns:
            List of entities in the region.
        """
        return [
            e for e in self._entities
            if x_start <= e.x < x_end and y_start <= e.y < y_end
        ]

    def clear_entity(self, x: int, y: int) -> None:
        """
        Clear an entity from a specific position.

        Args:
            x: Horizontal position.
            y: Vertical position.
        """
        entity = self.get_entity(x, y)
        if entity is not None:
            self.remove_entity(entity)
        else:
            self.clear(x, y)

    # Legacy compatibility
    def place_entity_at(self, x: int, y: int, entity: Any) -> bool:
        """Place an entity at specific coordinates."""
        entity.x = x
        entity.y = y
        return self.place_entity(entity)


class TileMap(GameMap[Any]):
    """
    Map specialized for terrain tiles with visibility tracking.

    Maintains separate grids for:
    - Tiles (terrain)
    - Visibility (currently visible)
    - Seen (previously explored)
    - Passability (can walk through)
    """

    def __init__(self, width: int, height: int):
        """
        Initialize a tile map.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        super().__init__(width, height, default=None)

        # Visibility tracking
        self._visible: GameMap[bool] = GameMap(width, height, default=False)
        self._seen: GameMap[bool] = GameMap(width, height, default=False)
        self._passable: GameMap[bool] = GameMap(width, height, default=True)

        # Special tile tracking
        self._stairs: List[Any] = []

    def set_tile(self, x: int, y: int, tile: Any) -> bool:
        """
        Place a tile at a position.

        Args:
            x: Horizontal position.
            y: Vertical position.
            tile: Tile object to place.

        Returns:
            True if successful.
        """
        if not self.in_bounds(x, y):
            return False

        self.set(x, y, tile)

        # Update passability from tile
        if hasattr(tile, 'passable'):
            self._passable.set(x, y, tile.passable)

        # Track stairs
        if hasattr(tile, 'has_trait') and tile.has_trait('stairs'):
            if tile not in self._stairs:
                self._stairs.append(tile)

        return True

    def get_tile(self, x: int, y: int) -> Optional[Any]:
        """Get the tile at a position."""
        return self.get(x, y)

    def is_passable(self, x: int, y: int) -> bool:
        """Check if a position can be walked through."""
        result = self._passable.get(x, y)
        return result if result is not None else False

    def get_passable(self, pos: Tuple[int, int]) -> bool:
        """Legacy accessor for passability."""
        return self.is_passable(pos[0], pos[1])

    def set_passable(self, x: int, y: int, passable: bool) -> None:
        """Set the passability of a position."""
        self._passable.set(x, y, passable)

    def is_visible(self, x: int, y: int) -> bool:
        """Check if a position is currently visible."""
        result = self._visible.get(x, y)
        return result if result is not None else False

    def set_visible(self, x: int, y: int, visible: bool) -> None:
        """Set the visibility of a position."""
        self._visible.set(x, y, visible)
        if visible:
            self._seen.set(x, y, True)

    def is_seen(self, x: int, y: int) -> bool:
        """Check if a position has ever been seen."""
        result = self._seen.get(x, y)
        return result if result is not None else False

    def get_seen(self, x: int, y: int) -> bool:
        """Legacy accessor for seen status."""
        return self.is_seen(x, y)

    def clear_visibility(self) -> None:
        """Reset all visibility (but keep seen status)."""
        self._visible.fill(False)

    def get_stairs(self) -> List[Any]:
        """Get all stairs on this map."""
        return self._stairs.copy()

    def get_passable_map_copy(self) -> GameMap[bool]:
        """
        Get a copy of the passability map.

        Returns:
            New GameMap with passability data.

        Note:
            Fixed spelling from original 'get_passible_map_copy'.
        """
        return self._passable.copy()

    # Legacy spelling alias
    def get_passible_map_copy(self) -> GameMap[bool]:
        """Legacy spelling alias for get_passable_map_copy."""
        return self.get_passable_map_copy()


class TrackingMap(GameMap[int]):
    """
    Map for storing tracking data like room IDs and navigation info.

    Used during dungeon generation to track which room each tile
    belongs to, and for pathfinding calculations.
    """

    def __init__(self, width: int, height: int):
        """
        Initialize a tracking map.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        super().__init__(width, height, default=-1)

    def set_room_id(self, x: int, y: int, room_id: int) -> None:
        """Set the room ID for a tile."""
        self.set(x, y, room_id)

    def get_room_id(self, x: int, y: int) -> int:
        """Get the room ID for a tile (-1 if no room)."""
        result = self.get(x, y)
        return result if result is not None else -1

    def get_tiles_in_room(self, room_id: int) -> List[Tuple[int, int]]:
        """
        Get all tiles belonging to a specific room.

        Args:
            room_id: The room ID to search for.

        Returns:
            List of (x, y) coordinates in the room.
        """
        tiles = []
        for x, y, value in self.iterate_all():
            if value == room_id:
                tiles.append((x, y))
        return tiles

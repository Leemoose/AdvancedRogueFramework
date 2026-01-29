"""
Maps Module
===========

Base map class for storing 2D grid data.
"""

import random
from logging_config import get_logger, is_debug_mode
from src.core.constants import NO_ENTITY

logger = get_logger(__name__)


class Maps:
    """
    Base map class for storing 2D grid data.

    Note: The entity_map initialization was fixed to properly create
    independent row lists. The original code created aliased lists.
    """

    def __init__(self, width: int, height: int):
        logger.debug("Initializing Maps with width=%d, height=%d", width, height)
        self.width = width
        self.height = height
        self.entity_map = [[NO_ENTITY for _ in range(self.height)] for _ in range(self.width)]
        logger.debug("Entity map initialized: %dx%d grid", len(self.entity_map), len(self.entity_map[0]) if self.entity_map else 0)

    def get_map(self):
        """Return the entity map."""
        return self.entity_map

    def get_width(self) -> int:
        """Return map width."""
        return self.width

    def get_height(self) -> int:
        """Return map height."""
        return self.height

    def get_entity(self, x: int, y: int):
        """
        Get entity at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Entity at (x, y) or -1 if out of bounds
        """
        if self.in_map(x, y):
            entity = self.entity_map[x][y]
            logger.debug("get_entity(%d, %d) -> %r", x, y, entity)
            return entity
        else:
            logger.debug("get_entity(%d, %d) -> NO_ENTITY (out of bounds)", x, y)
            return NO_ENTITY

    def get_has_no_entity(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) has no entity.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if no entity at (x, y), False otherwise
        """
        if self.in_map(x, y):
            result = not self.get_has_entity(x, y)
            logger.debug("get_has_no_entity(%d, %d) -> %s", x, y, result)
            return result
        else:
            logger.debug("get_has_no_entity(%d, %d) -> False (out of bounds)", x, y)
            return False

    def get_has_entity(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) has an entity.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if entity exists at (x, y), False otherwise
        """
        if self.in_map(x, y):
            result = (self.entity_map[x][y] != NO_ENTITY)
            logger.debug("get_has_entity(%d, %d) -> %s (value=%r)", x, y, result, self.entity_map[x][y])
            return result
        elif not self.in_map(x, y):
            logger.warning("get_has_entity: Attempted to check entity outside map bounds at (%d, %d)", x, y)
            return False
        else:
            return False

    def get_random_no_entity_location(self) -> tuple:
        """
        Get a random location that has no entity.

        Returns:
            Tuple (x, y) of a random empty location

        Warning:
            This can loop indefinitely if no empty locations exist.
        """
        logger.debug("Searching for random empty location...")
        attempts = 0
        max_attempts = self.width * self.height * 2  # Safety limit

        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)

        while self.get_has_no_entity(x, y) == False:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            attempts += 1
            if attempts > max_attempts:
                logger.error("get_random_no_entity_location: Exceeded max attempts (%d). Map may be full.", max_attempts)
                break

        logger.debug("Found empty location at (%d, %d) after %d attempts", x, y, attempts)
        return (x, y)

    def get_distance(self, x1: int, x2: int, y1: int, y2: int) -> float:
        """
        Calculate Euclidean distance between two points.

        Args:
            x1, y1: First point coordinates
            x2, y2: Second point coordinates

        Returns:
            Distance between the points, or None if either point is out of bounds
        """
        if self.in_map(x1, y1) and self.in_map(x2, y2):
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)
            logger.debug("get_distance((%d,%d) to (%d,%d)) -> %.2f", x1, y1, x2, y2, distance)
            return distance
        else:
            logger.warning("get_distance: One or both points out of bounds: (%d,%d), (%d,%d)", x1, y1, x2, y2)
            return None

    def in_map(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within map bounds.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if (x, y) is within bounds
        """
        result = x >= 0 and x < self.width and y >= 0 and y < self.height
        # Only log at trace level to avoid spam
        if is_debug_mode():
            logger.debug("in_map(%d, %d) -> %s (bounds: 0-%d, 0-%d)", x, y, result, self.width - 1, self.height - 1)
        return result

    def place_entity(self, x: int, y: int, entity) -> bool:
        """
        Place an entity at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            entity: The entity to place

        Returns:
            True if placement successful, False otherwise
        """
        if self.in_map(x, y):
            old_entity = self.entity_map[x][y]
            self.entity_map[x][y] = entity
            logger.debug("place_entity: Placed %r at (%d, %d), replaced %r", entity, x, y, old_entity)
            return True
        else:
            logger.error("place_entity: Attempted to place entity %r outside map bounds at (%d, %d)", entity, x, y)
            return False

    def clear_entity(self, x: int, y: int) -> bool:
        """
        Clear the entity at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if cleared successfully, False otherwise
        """
        if self.in_map(x, y):
            old_entity = self.entity_map[x][y]
            self.entity_map[x][y] = NO_ENTITY
            logger.debug("clear_entity: Cleared (%d, %d), was %r", x, y, old_entity)
            return True
        else:
            logger.error("clear_entity: Attempted to clear entity outside map bounds at (%d, %d)", x, y)
            return False

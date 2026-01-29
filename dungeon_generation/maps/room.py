"""
Room Module
===========

Room class for dungeon generation.
"""

from logging_config import get_logger

logger = get_logger(__name__)


class Room:
    """
    Represents a rectangular room in the dungeon.

    Attributes:
        x: Left edge X coordinate
        y: Top edge Y coordinate
        width: Room width in tiles
        height: Room height in tiles
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        logger.debug("Creating Room at (%d, %d), size %dx%d", x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other: 'Room') -> bool:
        """
        Check if this room intersects with another room.

        Uses a 1-tile buffer to prevent rooms from being directly adjacent.

        Args:
            other: Another Room to check intersection with

        Returns:
            True if rooms intersect (including buffer zone)
        """
        xPositive = min(self.x + self.width + 1, other.x + other.width + 1) > max(self.x, other.x)
        yPositive = min(self.y + self.height + 1, other.y + other.height + 1) > max(self.y, other.y)
        result = xPositive and yPositive

        if result:
            logger.debug("Room (%d,%d %dx%d) intersects with (%d,%d %dx%d)",
                        self.x, self.y, self.width, self.height,
                        other.x, other.y, other.width, other.height)

        return result

    def GetCenterX(self) -> int:
        """Return the X coordinate of the room's center."""
        return self.x + self.width // 2

    def GetCenterY(self) -> int:
        """Return the Y coordinate of the room's center."""
        return self.y + self.height // 2

    def __repr__(self) -> str:
        return f"Room(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

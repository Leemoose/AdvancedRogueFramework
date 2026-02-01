"""
Base Generator Module
=====================

Abstract base class for map generators.

Provides common functionality and defines the interface that all
dungeon map generators must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Any, TYPE_CHECKING

from logging_config import get_logger

from ..tiles import Floor, Wall

if TYPE_CHECKING:
    from ..maps.room import Room

logger = get_logger(__name__)


class MapGenerator(ABC):
    """
    Abstract base class for dungeon map generators.

    All map generators should inherit from this class and implement
    the generate method to create their specific map layout.

    Attributes:
        width: Map width in tiles
        height: Map height in tiles
        rooms: List of Room objects created during generation
        entity_map: 2D list of tile entities (Floor, Wall, etc.)

    Subclasses must implement:
        - generate(): Creates the dungeon layout

    Helper methods provided:
        - create_floor(): Create a Floor tile at given coordinates
        - create_wall(): Create a Wall tile at given coordinates
        - create_empty_entity_map(): Create a map filled with Wall tiles
        - set_floor(): Replace a tile with a Floor at given coordinates
        - set_wall(): Replace a tile with a Wall at given coordinates
        - is_wall(): Check if tile at coordinates is a Wall
        - is_floor(): Check if tile at coordinates is a Floor
    """

    def __init__(self, width: int, height: int):
        """
        Initialize the base map generator.

        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        logger.debug("Initializing MapGenerator: %dx%d", width, height)
        self.width = width
        self.height = height
        self.rooms: List['Room'] = []
        self.entity_map: List[List[Any]] = []

    @abstractmethod
    def generate(self) -> None:
        """
        Generate the map layout.

        This method must be implemented by subclasses to create their
        specific map layout by populating entity_map and rooms.

        The entity_map should be a width x height 2D list of Tile objects
        (Floor, Wall, etc.).
        """
        pass

    def get_width(self) -> int:
        """Return the map width."""
        return self.width

    def get_height(self) -> int:
        """Return the map height."""
        return self.height

    def get_rooms(self) -> List['Room']:
        """Return the list of rooms in the map."""
        return self.rooms

    def get_entity_map(self) -> List[List[Any]]:
        """Return the 2D list of tile entities."""
        return self.entity_map

    def create_floor(self, x: int, y: int) -> Floor:
        """
        Create a Floor tile at the given coordinates.

        Args:
            x: X coordinate for the tile
            y: Y coordinate for the tile

        Returns:
            A new Floor tile instance
        """
        return Floor(x, y)

    def create_wall(self, x: int, y: int) -> Wall:
        """
        Create a Wall tile at the given coordinates.

        Args:
            x: X coordinate for the tile
            y: Y coordinate for the tile

        Returns:
            A new Wall tile instance
        """
        return Wall(x, y)

    def create_empty_entity_map(self) -> List[List[Any]]:
        """
        Create an entity map filled with Wall tiles.

        Returns:
            A 2D list of Wall tile objects
        """
        logger.debug("Creating empty entity map with walls")
        self.entity_map = [
            [self.create_wall(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]
        return self.entity_map

    def set_floor(self, x: int, y: int) -> None:
        """
        Set the tile at (x, y) to a Floor.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.entity_map[x][y] = self.create_floor(x, y)

    def set_wall(self, x: int, y: int) -> None:
        """
        Set the tile at (x, y) to a Wall.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.entity_map[x][y] = self.create_wall(x, y)

    def is_wall(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is a Wall.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if the tile is a Wall
        """
        return self.entity_map[x][y].has_trait("wall")

    def is_floor(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is a Floor (passable).

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if the tile is passable
        """
        return self.entity_map[x][y].is_passable()

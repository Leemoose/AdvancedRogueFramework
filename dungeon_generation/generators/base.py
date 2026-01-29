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
        track_map_render: 2D list of characters representing the map
                         ('.' for floor, 'x' for wall)
        entity_map: 2D list of tile entities (Floor, Wall, etc.)

    Subclasses must implement:
        - generate(): Creates the dungeon layout

    Helper methods provided:
        - create_floor(): Create a Floor tile at given coordinates
        - create_wall(): Create a Wall tile at given coordinates
        - create_empty_render_map(): Create an empty ASCII render map
        - create_entity_map_from_render(): Convert ASCII map to tile entities
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
        self.track_map_render: List[List[str]] = []
        self.entity_map: List[List[Any]] = []

    @abstractmethod
    def generate(self) -> None:
        """
        Generate the map layout.

        This method must be implemented by subclasses to create their
        specific map layout by populating track_map_render, rooms, and
        optionally entity_map.

        The track_map_render should be a width x height 2D list where:
        - '.' represents floor tiles
        - 'x' represents wall tiles

        After generation, entity_map can be populated by calling
        create_entity_map_from_render() or by custom logic.
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

    def get_track_map_render(self) -> List[List[str]]:
        """Return the ASCII render map."""
        return self.track_map_render

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

    def create_empty_render_map(self) -> List[List[str]]:
        """
        Create an empty ASCII render map filled with wall characters.

        The render map uses 'x' for walls and '.' for floors. This is an
        intermediate representation used during generation before converting
        to actual tile entities.

        Returns:
            A 2D list of 'x' characters representing an all-wall map
        """
        return [['x' for _ in range(self.height)] for _ in range(self.width)]

    def create_entity_map_from_render(self) -> List[List[Any]]:
        """
        Convert the ASCII render map to a 2D list of tile entities.

        Interprets the track_map_render characters and creates appropriate tile
        objects. Edge tiles are always converted to walls for safety.

        Returns:
            A 2D list of tile entities (Floor or Wall objects)

        Note:
            - Edge tiles (x=0, y=0, x=width-1, y=height-1) are always walls
            - Unknown characters default to walls
        """
        logger.debug("Converting render map to entity map")
        entity_map: List[List[Any]] = []
        wall_count = 0
        floor_count = 0

        for x in range(self.width):
            column: List[Any] = []
            for y in range(self.height):
                text = self.track_map_render[x][y]

                # Edge tiles must be walls for map boundaries
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    column.append(self.create_wall(x, y))
                    wall_count += 1
                elif text == "x":
                    column.append(self.create_wall(x, y))
                    wall_count += 1
                elif text == ".":
                    column.append(self.create_floor(x, y))
                    floor_count += 1
                else:
                    # Unknown character, default to wall
                    logger.warning("Unknown tile '%s' at (%d, %d), defaulting to wall", text, x, y)
                    column.append(self.create_wall(x, y))
                    wall_count += 1

            entity_map.append(column)

        logger.debug("Entity map created: %d walls, %d floors", wall_count, floor_count)
        self.entity_map = entity_map
        return entity_map

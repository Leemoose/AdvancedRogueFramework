"""
TileMap Module
==============

This map is responsible for all the tiles in the game.
Supports multiple generation strategies via the generators package.
"""

import random
from typing import TYPE_CHECKING
from logging_config import get_logger

from .maps import Maps
from .map_utility import place_stairs, place_gateways, add_ocean_water, apply_forest_theme

# Import generators - use lazy loading to avoid circular imports
if TYPE_CHECKING:
    from ..generators.base import MapGenerator

logger = get_logger(__name__)


def _get_generator(mapData) -> 'MapGenerator':
    """
    Factory function to create the appropriate generator based on mapData.

    Args:
        mapData: MapData configuration object

    Returns:
        A MapGenerator instance configured for the requested type
    """
    from ..generators import (
        RoomsAndCorridorsGenerator,
        CaveGenerator,
        PillarHallGenerator
    )

    generator_type = getattr(mapData, 'generator_type', 'rooms_corridors')
    generator_params = getattr(mapData, 'generator_params', {})

    logger.debug("Creating generator: type=%s", generator_type)

    if generator_type == 'cave':
        return CaveGenerator(
            width=mapData.width,
            height=mapData.height,
            fill_probability=generator_params.get('fill_probability', 0.45),
            smooth_iterations=generator_params.get('smooth_iterations', 5),
            wall_threshold=generator_params.get('wall_threshold', 5),
            connect_regions=generator_params.get('connect_regions', True)
        )
    elif generator_type == 'pillar_hall':
        return PillarHallGenerator(
            width=mapData.width,
            height=mapData.height,
            pillar_spacing=generator_params.get('pillar_spacing', 4),
            pillar_size=generator_params.get('pillar_size', 1),
            border_width=generator_params.get('border_width', 1),
            randomize_pillars=generator_params.get('randomize_pillars', True),
            pillar_density=generator_params.get('pillar_density', 0.8)
        )
    else:
        # Default: rooms_corridors
        return RoomsAndCorridorsGenerator(
            width=mapData.width,
            height=mapData.height,
            num_rooms=mapData.numRooms,
            room_size=mapData.roomSize,
            circularity=mapData.circularity
        )


class TileMap(Maps):
    """
    Map class that holds all tile objects for a dungeon floor.

    Supports multiple generation strategies:
        - rooms_corridors: Traditional rooms connected by L-shaped corridors
        - cave: Cellular automata organic cave shapes
        - pillar_hall: Open space with pillar columns

    The generator type is determined by mapData.generator_type.
    """

    def __init__(self, mapData, depth: int, branch: str, gateway_data=None):
        """
        Initialize the TileMap.

        Args:
            mapData: MapData configuration object
            depth: Floor depth (1-indexed)
            branch: Dungeon branch name
            gateway_data: Optional GatewayData for inter-branch connections
        """
        logger.info("Initializing TileMap: depth=%d, branch=%s", depth, branch)
        super().__init__(mapData.width, mapData.height)
        self.mapData = mapData
        self.stairs = []
        self.gateway = []
        self.rooms = []
        self.depth = depth
        self.branch = branch

        # Use generator strategy to create map
        generator_type = getattr(mapData, 'generator_type', 'rooms_corridors')
        logger.debug("Using generator: %s", generator_type)

        generator = _get_generator(mapData)
        generator.generate()

        # Copy results from generator
        self.rooms = generator.get_rooms()
        self.entity_map = generator.get_entity_map()

        # Apply ocean water for Ocean branch
        if branch == "Ocean":
            logger.debug("Adding ocean water...")
            add_ocean_water(self)

        # Apply forest theme for Forest branch
        if branch == "Forest":
            logger.debug("Applying forest theme...")
            apply_forest_theme(self)

        logger.debug("Placing stairs...")
        place_stairs(self)

        # Place gateways if gateway_data is provided
        if gateway_data is not None:
            logger.debug("Placing gateways...")
            place_gateways(self, gateway_data)

        logger.info("TileMap initialization complete: %d rooms, %d stairs, %d gateways",
                   len(self.rooms), len(self.stairs), len(self.gateway))

    def __str__(self) -> str:
        """Return ASCII representation of the map."""
        map_str = ""
        for row in self.get_map():
            for block in row:
                if block.passable:
                    map_str += "."
                else:
                    map_str += "x"
            map_str += "\n"
        return map_str

    def get_depth(self) -> int:
        """Return the dungeon depth (floor number)."""
        return self.depth

    def get_branch(self) -> str:
        """Return the dungeon branch name."""
        return self.branch

    def get_num_rooms(self) -> int:
        """Return the configured number of rooms for this map."""
        return self.mapData.get_numRooms()

    def get_tag(self, x: int, y: int) -> str:
        """Get the render tag of the tile at (x, y)."""
        return self.get_entity(x, y).get_render_tag()

    def get_stairs(self) -> list:
        """Return list of all stairs on this floor."""
        return self.stairs

    def get_gateway(self) -> list:
        """Return list of all gateways on this floor."""
        return self.gateway

    def place_tile(self, tile) -> None:
        """
        Place a tile object at its coordinates.

        Args:
            tile: Tile object with get_x() and get_y() methods
        """
        logger.debug("place_tile: %s at (%d, %d)", type(tile).__name__, tile.get_x(), tile.get_y())
        self.place_entity(tile.get_x(), tile.get_y(), tile)

    def get_passable(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is passable.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if tile exists and is passable
        """
        if self.in_map(x, y) and self.get_entity(x, y).is_passable():
            return True
        else:
            return False

    def get_visible(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is currently visible.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if tile exists and is visible
        """
        if self.in_map(x, y) and self.get_entity(x, y).get_visible():
            return True
        else:
            return False

    def get_seen(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) has been seen.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if tile exists and has been seen
        """
        if self.in_map(x, y) and self.get_entity(x, y).get_seen():
            return True
        else:
            return False

    def get_is_all_visible(self) -> bool:
        """
        Check if all floor tiles have been seen.

        Returns:
            True if every floor tile has been seen
        """
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.get_entity(x, y).has_trait("floor") and not self.get_entity(x, y).get_seen():
                    logger.debug("get_is_all_visible: Found unseen floor at (%d, %d)", x, y)
                    return False
        logger.debug("get_is_all_visible: All floors seen")
        return True

    def get_next_not_visible_coordinate(self) -> tuple:
        """
        Find the next unseen floor tile.

        Returns:
            Tuple (x, y) of unseen floor, or (-1, -1) if all seen
        """
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.get_entity(x, y).has_trait("floor") and not self.get_entity(x, y).get_seen():
                    logger.debug("get_next_not_visible_coordinate: Found at (%d, %d)", x, y)
                    return (x, y)
        logger.debug("get_next_not_visible_coordinate: No unseen floors")
        return (-1, -1)

    def mark_visible(self, x: int, y: int) -> None:
        """Mark the tile at (x, y) as seen."""
        self.get_entity(x, y).set_seen(True)
        logger.debug("mark_visible: (%d, %d) now seen", x, y)

    def overlaps_any(self, room) -> bool:
        """
        Check if a room overlaps with any existing room.

        Args:
            room: Room to check for overlaps

        Returns:
            True if room overlaps with any existing room
        """
        for other in self.rooms:
            if room.intersects(other):
                logger.debug("overlaps_any: Room at (%d,%d) overlaps with room at (%d,%d)",
                           room.x, room.y, other.x, other.y)
                return True
        return False

    def get_point_in_squircle(self, x: int, y: int, circularity: float) -> bool:
        """
        Check if a point is inside the map's squircle boundary.

        Args:
            x: X coordinate
            y: Y coordinate
            circularity: Circularity factor (0 = square, 1 = circle)

        Returns:
            True if point is inside the squircle
        """
        originX = 1.0 * (self.width - 1) / 2
        originY = 1.0 * (self.height - 1) / 2
        radius = max(self.width, self.height) / 2

        radiusSqrd = radius ** 2
        squircConst = ((1 - circularity) / radius) ** 2
        localX = x - originX
        localY = y - originY

        xSqrd = localX ** 2
        ySqrd = localY ** 2

        squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

        return squircleVal < radiusSqrd

    def get_in_squircle(self, room, circularity: float) -> bool:
        """
        Check if an entire room fits inside the map's squircle boundary.

        Args:
            room: Room to check
            circularity: Circularity factor

        Returns:
            True if room fits inside the squircle
        """
        return (self.get_point_in_squircle(room.x, room.y, circularity) and
                self.get_point_in_squircle(room.x + room.width - 1,
                                          room.y + room.width - 1,
                                          circularity))

    def get_random_location(self, stairs_block: bool = True) -> tuple:
        """
        Get a random passable location from the tile map.

        Args:
            stairs_block: Whether stairs block placement (unused currently)

        Returns:
            Tuple (x, y) of a random passable location
        """
        logger.debug("Finding random passable location")
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)

        attempts = 0
        while not self.get_passable(startx, starty):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
            attempts += 1

        logger.debug("Found passable location (%d, %d) after %d attempts", startx, starty, attempts)
        return startx, starty

    def get_circularity(self) -> float:
        """Return the map's circularity setting."""
        return self.mapData.get_circularity()

    def get_room_size(self) -> int:
        """Return the maximum room size setting."""
        return self.mapData.get_roomSize()

    def apply_tide(self, tide_level: int) -> None:
        """
        Apply water terrain based on tide level.

        Tiles flood when tide_level > tile.elevation.
        - Deep water: tide is significantly above elevation
        - Shallow water: tide is slightly above elevation
        - Dry: tide is at or below elevation

        Args:
            tide_level: Current tide level (0-50)
        """
        from dungeon_generation.terrain import ShallowWaterTerrain, DeepWaterTerrain

        # Deep water requires tide to be this much above elevation
        deep_water_margin = 15

        for x in range(self.width):
            for y in range(self.height):
                tile = self.get_entity(x, y)

                # Skip tiles that aren't part of the ocean system
                if tile.elevation == 0 or tile.elevation is None:
                    continue

                # Clear existing water first
                tile.remove_terrain("water")

                if tide_level - deep_water_margin >= tile.get_elevation():
                    tile.add_terrain(DeepWaterTerrain(x, y))
                elif tide_level >= tile.get_elevation():
                    tile.add_terrain(ShallowWaterTerrain(x, y))


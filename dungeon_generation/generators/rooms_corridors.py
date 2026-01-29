"""
Rooms and Corridors Generator Module
====================================

Implements the classic roguelike dungeon generation algorithm:
randomly placed rooms connected by L-shaped corridors.

Features:
    - Configurable room count, size, and circularity
    - Squircle-shaped rooms (blend between square and circle)
    - L-shaped corridors connecting room centers
    - Overlap detection to prevent room collisions
"""

import random
from typing import List, Optional

from logging_config import get_logger

from .base import MapGenerator
from ..maps.room import Room

logger = get_logger(__name__)


class RoomsAndCorridorsGenerator(MapGenerator):
    """
    Generates dungeons using the rooms-and-corridors algorithm.

    This is the traditional roguelike dungeon generation method where
    rectangular (or squircle-shaped) rooms are randomly placed on the map
    and then connected with L-shaped corridors.

    Attributes:
        width: Map width in tiles (inherited from MapGenerator)
        height: Map height in tiles (inherited from MapGenerator)
        num_rooms: Target number of rooms to generate
        room_size: Maximum room dimension (rooms are randomly sized up to this)
        circularity: Shape factor for rooms (0 = square, 1 = circle)

    Example:
        generator = RoomsAndCorridorsGenerator(
            width=80, height=40,
            num_rooms=10, room_size=8, circularity=0.5
        )
        generator.generate()
        rooms = generator.get_rooms()
        render_map = generator.get_track_map_render()
    """

    def __init__(
        self,
        width: int,
        height: int,
        num_rooms: int = 10,
        room_size: int = 8,
        circularity: float = 0.5
    ):
        """
        Initialize the Rooms and Corridors generator.

        Args:
            width: Map width in tiles
            height: Map height in tiles
            num_rooms: Target number of rooms to create (default: 10)
            room_size: Maximum room dimension in tiles (default: 8)
            circularity: Room shape factor, 0=square, 1=circle (default: 0.5)
        """
        super().__init__(width, height)

        self.num_rooms = num_rooms
        self.room_size = room_size
        self.circularity = circularity

        logger.info(
            "RoomsAndCorridorsGenerator initialized: %dx%d, num_rooms=%d, "
            "room_size=%d, circularity=%.2f",
            width, height, num_rooms, room_size, circularity
        )

    def generate(self) -> None:
        """
        Generate a dungeon with rooms connected by corridors.

        Creates a map by:
        1. Creating an empty render map (all walls)
        2. Placing rooms at random non-overlapping positions
        3. Carving squircle-shaped rooms into the render map
        4. Connecting adjacent rooms with L-shaped corridors
        5. Optionally converting the render map to tile entities
        """
        logger.info(
            "Generating rooms and corridors map: %dx%d, target rooms=%d",
            self.width, self.height, self.num_rooms
        )

        # Initialize the map with all walls
        self._initialize_map()

        # Place all rooms
        self._construct_rooms()

        # Connect rooms with corridors
        self._connect_all_rooms()

        logger.info(
            "Map generation complete: %d rooms created and connected",
            len(self.rooms)
        )

    def _initialize_map(self) -> None:
        """Initialize the map with all wall tiles."""
        logger.debug("Initializing map with walls")
        self.track_map_render = self.create_empty_render_map()

    def _construct_rooms(self) -> None:
        """
        Create and place all rooms on the map.

        Attempts to place num_rooms rooms. Some may fail to be placed
        if the map becomes too crowded.
        """
        logger.info("Constructing %d rooms", self.num_rooms)

        for room_num in range(self.num_rooms):
            size = random.randint(4, self.room_size)
            logger.debug(
                "Room %d/%d: generating with size %d",
                room_num + 1, self.num_rooms, size
            )

            room = self._place_room(size, size)
            if room is not None:
                self.rooms.append(room)
                self._carve_room(room)

        logger.info("Room construction complete: %d rooms created", len(self.rooms))

    def _place_room(
        self,
        room_width: int,
        room_height: int
    ) -> Optional[Room]:
        """
        Attempt to place a room on the map without overlapping existing rooms.

        Args:
            room_width: Width of the room to place
            room_height: Height of the room to place

        Returns:
            The placed Room object, or None if placement failed
        """
        max_tries = 100
        logger.debug(
            "Attempting to place room: size=%dx%d, circularity=%.2f",
            room_width, room_height, self.circularity
        )

        # Initial random position
        start_x = random.randint(1, self.width - room_width - 1)
        start_y = random.randint(1, self.height - room_height - 1)
        room = Room(start_x, start_y, room_width, room_height)
        tries = 0

        # Try to find a non-overlapping position
        while (
            self._overlaps_any(room) and
            self._room_in_squircle(room) and
            tries < max_tries
        ):
            room.x = random.randint(1, self.width - room_width - 1)
            room.y = random.randint(1, self.height - room_height - 1)
            tries += 1
            if tries % 20 == 0:
                logger.debug("Room placement: %d/%d attempts", tries, max_tries)

        if tries < max_tries:
            logger.info(
                "Room placed at (%d, %d), size %dx%d after %d tries",
                room.x, room.y, room_width, room_height, tries
            )
            return room
        else:
            logger.warning("Failed to place room after %d attempts", max_tries)
            return None

    def _overlaps_any(self, room: Room) -> bool:
        """
        Check if a room overlaps with any existing room.

        Args:
            room: The room to check

        Returns:
            True if room overlaps with any existing room
        """
        for other in self.rooms:
            if room.intersects(other):
                logger.debug(
                    "Room at (%d,%d) overlaps with room at (%d,%d)",
                    room.x, room.y, other.x, other.y
                )
                return True
        return False

    def _point_in_squircle(self, x: int, y: int) -> bool:
        """
        Check if a point is inside the map's squircle boundary.

        A squircle is a shape between a square and a circle, controlled
        by the circularity parameter.

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if the point is inside the squircle
        """
        origin_x = (self.width - 1) / 2.0
        origin_y = (self.height - 1) / 2.0
        radius = max(self.width, self.height) / 2.0

        radius_sqrd = radius ** 2
        squirc_const = ((1 - self.circularity) / radius) ** 2
        local_x = x - origin_x
        local_y = y - origin_y

        x_sqrd = local_x ** 2
        y_sqrd = local_y ** 2

        squircle_val = x_sqrd + y_sqrd - squirc_const * x_sqrd * y_sqrd

        return squircle_val < radius_sqrd

    def _room_in_squircle(self, room: Room) -> bool:
        """
        Check if an entire room fits inside the map's squircle boundary.

        Args:
            room: Room to check

        Returns:
            True if the room fits inside the squircle
        """
        return (
            self._point_in_squircle(room.x, room.y) and
            self._point_in_squircle(room.x + room.width - 1, room.y + room.height - 1)
        )

    def _carve_room(self, room: Room) -> None:
        """
        Carve a squircle-shaped room into the render map.

        Uses squircle geometry to create rooms that blend between
        square and circular shapes based on the circularity parameter.

        Args:
            room: The room to carve
        """
        logger.debug(
            "Carving room at (%d, %d), size %dx%d, circularity=%.2f",
            room.x, room.y, room.width, room.height, self.circularity
        )

        origin_x = (room.width - 1) / 2.0
        origin_y = (room.height - 1) / 2.0
        radius = max(room.width, room.height) / 2.0

        radius_sqrd = radius ** 2
        squirc_const = ((1 - self.circularity) / radius) ** 2

        tiles_carved = 0
        for x in range(room.width):
            for y in range(room.height):
                local_x = x - origin_x
                local_y = y - origin_y

                x_sqrd = local_x ** 2
                y_sqrd = local_y ** 2

                squircle_val = x_sqrd + y_sqrd - squirc_const * x_sqrd * y_sqrd

                if squircle_val < radius_sqrd:
                    self.track_map_render[x + room.x][y + room.y] = "."
                    tiles_carved += 1

        logger.debug("Carved %d tiles for room", tiles_carved)

    def _connect_all_rooms(self) -> None:
        """
        Connect all rooms with corridors.

        Connects each room to the next one in the list, ensuring
        the entire dungeon is traversable.
        """
        logger.debug("Connecting %d rooms", len(self.rooms))

        for i in range(len(self.rooms) - 1):
            logger.debug("Connecting room %d to room %d", i, i + 1)
            self._connect_rooms(self.rooms[i], self.rooms[i + 1])

        logger.info(
            "Room connection complete: %d corridors created",
            max(0, len(self.rooms) - 1)
        )

    def _connect_rooms(self, room1: Room, room2: Room) -> None:
        """
        Connect two rooms with an L-shaped corridor.

        The corridor goes horizontally from room1's center to an intermediate
        corner point, then vertically to room2's center.

        Args:
            room1: First room to connect
            room2: Second room to connect
        """
        corner_x = room1.GetCenterX()
        corner_y = room2.GetCenterY()

        logger.debug(
            "Connecting rooms: (%d,%d) center=(%d,%d) to (%d,%d) center=(%d,%d) "
            "via corner (%d,%d)",
            room1.x, room1.y, room1.GetCenterX(), room1.GetCenterY(),
            room2.x, room2.y, room2.GetCenterX(), room2.GetCenterY(),
            corner_x, corner_y
        )

        # First corridor segment (room1 center to corner)
        lower1_x = min(room1.GetCenterX(), corner_x)
        upper1_x = max(room1.GetCenterX(), corner_x) + 1
        lower1_y = min(room1.GetCenterY(), corner_y)
        upper1_y = max(room1.GetCenterY(), corner_y) + 1

        tiles_carved_1 = 0
        for x in range(lower1_x, upper1_x):
            for y in range(lower1_y, upper1_y):
                if self.track_map_render[x][y] == "x":
                    self.track_map_render[x][y] = "."
                    tiles_carved_1 += 1

        # Second corridor segment (corner to room2 center)
        lower2_x = min(room2.GetCenterX(), corner_x)
        upper2_x = max(room2.GetCenterX(), corner_x) + 1
        lower2_y = min(room2.GetCenterY(), corner_y)
        upper2_y = max(room2.GetCenterY(), corner_y) + 1

        tiles_carved_2 = 0
        for x in range(lower2_x, upper2_x):
            for y in range(lower2_y, upper2_y):
                if self.track_map_render[x][y] == "x":
                    self.track_map_render[x][y] = "."
                    tiles_carved_2 += 1

        logger.debug(
            "Corridor carved: %d + %d = %d tiles",
            tiles_carved_1, tiles_carved_2, tiles_carved_1 + tiles_carved_2
        )

    def __str__(self) -> str:
        """Return ASCII representation of the generated map."""
        if not self.track_map_render:
            return "<Map not generated>"

        lines = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.track_map_render[x][y]
            lines.append(row)
        return "\n".join(lines)

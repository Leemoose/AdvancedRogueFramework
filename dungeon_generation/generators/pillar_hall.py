"""
Pillar Hall Generator Module
============================

Generates open hall maps with regularly or semi-regularly spaced pillars.
Creates a large open area with structural pillars, suitable for arena-style
encounters or grand hall areas in the dungeon.
"""

import random
from typing import List, Optional

from logging_config import get_logger

from .base import MapGenerator
from ..tiles import Floor, Wall
from ..maps.room import Room

logger = get_logger(__name__)


class PillarHallGenerator(MapGenerator):
    """
    Generator for open pillar hall maps.

    Creates a large open floor area surrounded by walls, with pillars
    placed in a regular or semi-regular grid pattern throughout the space.

    Attributes:
        pillar_spacing: Distance between pillar centers (default 4)
        pillar_size: Size of each pillar, 1 for single tile, 2 for 2x2 (default 1)
        border_width: Thickness of the wall border (default 1)
        randomize_pillars: Whether to add random offset to pillar positions (default True)
        pillar_density: Probability that a pillar spot contains a pillar (default 0.8)
    """

    def __init__(
        self,
        width: int,
        height: int,
        pillar_spacing: int = 4,
        pillar_size: int = 1,
        border_width: int = 1,
        randomize_pillars: bool = True,
        pillar_density: float = 0.8
    ):
        """
        Initialize the Pillar Hall Generator.

        Args:
            width: Map width in tiles
            height: Map height in tiles
            pillar_spacing: Distance between pillar centers (minimum 2)
            pillar_size: Size of each pillar (1 or 2 for 2x2 pillars)
            border_width: Thickness of the wall border (minimum 1)
            randomize_pillars: Add random offset (+-1) to pillar positions
            pillar_density: Probability (0.0-1.0) that each pillar spot has a pillar
        """
        super().__init__(width, height)

        # Validate and store parameters
        self.pillar_spacing = max(2, pillar_spacing)
        self.pillar_size = max(1, min(2, pillar_size))
        self.border_width = max(1, border_width)
        self.randomize_pillars = randomize_pillars
        self.pillar_density = max(0.0, min(1.0, pillar_density))

        logger.info(
            "PillarHallGenerator initialized: %dx%d, spacing=%d, pillar_size=%d, "
            "border=%d, randomize=%s, density=%.2f",
            width, height, self.pillar_spacing, self.pillar_size,
            self.border_width, self.randomize_pillars, self.pillar_density
        )

    def generate(self) -> None:
        """
        Generate the pillar hall map.

        Creates a large open room with walls around the border and
        pillars placed in a grid pattern within the open space.
        """
        logger.info("Generating pillar hall map: %dx%d", self.width, self.height)

        # Initialize the map with all walls
        self._initialize_map()

        # Carve out the open floor area
        self._carve_floor_area()

        # Place pillars in the open area
        self._place_pillars()

        # Create the room object for spawn compatibility
        self._create_room()

        logger.info(
            "Pillar hall generation complete: %d rooms, floor area %dx%d",
            len(self.rooms),
            self.width - 2 * self.border_width,
            self.height - 2 * self.border_width
        )

    def _initialize_map(self) -> None:
        """Initialize the map with all wall tiles."""
        logger.debug("Initializing map with walls")
        self.create_empty_entity_map()

    def _carve_floor_area(self) -> None:
        """
        Carve out the open floor area within the border.

        The floor area excludes the border_width tiles around all edges.
        """
        logger.debug("Carving floor area with border_width=%d", self.border_width)

        floor_start_x = self.border_width
        floor_end_x = self.width - self.border_width
        floor_start_y = self.border_width
        floor_end_y = self.height - self.border_width

        floor_tiles = 0
        for x in range(floor_start_x, floor_end_x):
            for y in range(floor_start_y, floor_end_y):
                self.set_floor(x, y)
                floor_tiles += 1

        logger.debug("Carved %d floor tiles", floor_tiles)

    def _place_pillars(self) -> None:
        """
        Place pillars in a grid pattern across the open floor area.

        Pillars are placed starting from the inner edge of the floor area,
        spaced according to pillar_spacing. Random offsets and density
        are applied based on configuration.
        """
        logger.debug(
            "Placing pillars: spacing=%d, size=%d, randomize=%s, density=%.2f",
            self.pillar_spacing, self.pillar_size,
            self.randomize_pillars, self.pillar_density
        )

        # Calculate the area where pillars can be placed
        # Leave some margin from the border to avoid pillars touching walls
        pillar_margin = self.border_width + 1
        pillar_area_start_x = pillar_margin
        pillar_area_end_x = self.width - pillar_margin - (self.pillar_size - 1)
        pillar_area_start_y = pillar_margin
        pillar_area_end_y = self.height - pillar_margin - (self.pillar_size - 1)

        pillar_count = 0
        skipped_count = 0

        # Iterate through pillar grid positions
        x = pillar_area_start_x
        while x < pillar_area_end_x:
            y = pillar_area_start_y
            while y < pillar_area_end_y:
                # Check density - skip some pillars randomly
                if random.random() > self.pillar_density:
                    logger.debug("Skipping pillar at grid position (%d, %d) due to density", x, y)
                    skipped_count += 1
                    y += self.pillar_spacing
                    continue

                # Calculate actual pillar position with optional random offset
                pillar_x = x
                pillar_y = y

                if self.randomize_pillars:
                    # Add random offset of -1, 0, or +1
                    offset_x = random.randint(-1, 1)
                    offset_y = random.randint(-1, 1)

                    # Ensure pillar stays within valid area
                    pillar_x = max(
                        pillar_area_start_x,
                        min(pillar_area_end_x - 1, x + offset_x)
                    )
                    pillar_y = max(
                        pillar_area_start_y,
                        min(pillar_area_end_y - 1, y + offset_y)
                    )

                # Place the pillar
                self._place_single_pillar(pillar_x, pillar_y)
                pillar_count += 1

                y += self.pillar_spacing
            x += self.pillar_spacing

        logger.info("Placed %d pillars, skipped %d due to density", pillar_count, skipped_count)

    def _place_single_pillar(self, x: int, y: int) -> None:
        """
        Place a single pillar at the given position.

        For pillar_size=1, places a single wall tile.
        For pillar_size=2, places a 2x2 block of wall tiles.

        Args:
            x: X coordinate for pillar placement
            y: Y coordinate for pillar placement
        """
        for dx in range(self.pillar_size):
            for dy in range(self.pillar_size):
                px = x + dx
                py = y + dy

                # Verify we're within bounds and not overwriting border
                if (self.border_width <= px < self.width - self.border_width and
                        self.border_width <= py < self.height - self.border_width):
                    self.set_wall(px, py)
                    logger.debug("Placed pillar tile at (%d, %d)", px, py)

    def _create_room(self) -> None:
        """
        Create a single room covering the entire floor area.

        This ensures spawn systems can find valid floor positions
        within the pillar hall.
        """
        # The room represents the entire open floor area
        room_x = self.border_width
        room_y = self.border_width
        room_width = self.width - 2 * self.border_width
        room_height = self.height - 2 * self.border_width

        room = Room(room_x, room_y, room_width, room_height)
        self.rooms.append(room)

        logger.debug(
            "Created room at (%d, %d), size %dx%d",
            room_x, room_y, room_width, room_height
        )

    def get_pillar_positions(self) -> List[tuple]:
        """
        Get a list of all pillar positions after generation.

        Useful for debugging or for systems that need to know
        where pillars are located.

        Returns:
            List of (x, y) tuples for all pillar tiles
        """
        pillars = []
        for x in range(self.border_width, self.width - self.border_width):
            for y in range(self.border_width, self.height - self.border_width):
                if self.is_wall(x, y):
                    pillars.append((x, y))
        return pillars

    def __str__(self) -> str:
        """Return ASCII representation of the generated map."""
        if not self.entity_map:
            return "<Map not generated>"

        lines = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.entity_map[x][y].is_passable():
                    row += "."
                else:
                    row += "x"
            lines.append(row)
        return "\n".join(lines)

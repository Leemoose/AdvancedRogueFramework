"""
Cave Generator Module
=====================

Generates organic cave-like maps using cellular automata algorithm.

The algorithm works by:
1. Starting with random noise (walls/floors based on fill_probability)
2. Applying smoothing iterations using neighbor counting rules
3. Optionally connecting disconnected floor regions with tunnels
4. Identifying large floor areas as "rooms" for spawn placement

Example usage:
    generator = CaveGenerator(80, 50)
    generator.generate()
    entity_map = generator.get_entity_map()
    rooms = generator.get_rooms()
"""

import random
from typing import List, Set, Tuple, Optional
from collections import deque

from logging_config import get_logger
from .base import MapGenerator
from ..tiles import Floor, Wall
from ..maps.room import Room

logger = get_logger(__name__)


class CaveGenerator(MapGenerator):
    """
    Cave map generator using cellular automata.

    Creates organic, cave-like dungeon layouts by simulating cellular
    growth patterns. The resulting caves have natural-looking irregular
    walls and open spaces.

    Attributes:
        fill_probability: Initial probability for a tile to be a wall (0.0-1.0)
        smooth_iterations: Number of smoothing passes to apply
        wall_threshold: Number of wall neighbors needed to become/stay a wall
        connect_regions: Whether to connect disconnected floor regions
        min_room_size: Minimum floor area to be considered a "room"
    """

    # 8-directional neighbor offsets
    NEIGHBORS = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

    def __init__(
        self,
        width: int,
        height: int,
        fill_probability: float = 0.45,
        smooth_iterations: int = 5,
        wall_threshold: int = 5,
        connect_regions: bool = True,
        min_room_size: int = 16
    ):
        """
        Initialize the cave generator.

        Args:
            width: Map width in tiles
            height: Map height in tiles
            fill_probability: Initial wall probability (default 0.45)
            smooth_iterations: Number of smoothing passes (default 5)
            wall_threshold: Neighbor count to become wall (default 5)
            connect_regions: Whether to ensure connectivity (default True)
            min_room_size: Minimum tiles for a region to be a "room" (default 16)
        """
        super().__init__(width, height)
        self.fill_probability = fill_probability
        self.smooth_iterations = smooth_iterations
        self.wall_threshold = wall_threshold
        self.connect_regions = connect_regions
        self.min_room_size = min_room_size

        logger.info(
            "CaveGenerator initialized: %dx%d, fill=%.2f, iterations=%d, "
            "threshold=%d, connect=%s",
            width, height, fill_probability, smooth_iterations,
            wall_threshold, connect_regions
        )

    def generate(self) -> None:
        """
        Generate the cave map.

        Uses a temporary boolean grid for cellular automata processing,
        then converts to entity_map with Tile objects at the end.
        Also populates rooms list with Room objects for large floor areas.
        """
        logger.info("Starting cave generation")

        # Step 1: Initialize with random noise (using bool grid for efficiency)
        self._initialize_noise()
        logger.debug("Noise initialization complete")

        # Step 2: Apply cellular automata smoothing
        for iteration in range(self.smooth_iterations):
            self._smooth_map()
            logger.debug("Smoothing iteration %d/%d complete",
                        iteration + 1, self.smooth_iterations)

        # Step 3: Ensure borders are walls
        self._enforce_borders()
        logger.debug("Border enforcement complete")

        # Step 4: Find and connect disconnected regions
        if self.connect_regions:
            regions = self._find_regions()
            logger.debug("Found %d floor regions", len(regions))
            if len(regions) > 1:
                self._connect_all_regions(regions)
                logger.debug("Region connection complete")

        # Step 5: Create Room objects from large floor areas
        self._create_rooms()

        # Step 6: Convert bool grid to entity_map with Tile objects
        self._convert_to_entity_map()

        logger.info(
            "Cave generation complete: %d rooms created",
            len(self.rooms)
        )

    def _initialize_noise(self) -> None:
        """
        Initialize the map with random noise.

        Each tile has fill_probability chance of being a wall.
        Border tiles are always walls.
        Uses a boolean grid (True = wall, False = floor) for efficiency.
        """
        # Use bool grid: True = wall, False = floor
        self._wall_grid: List[List[bool]] = []

        for x in range(self.width):
            column = []
            for y in range(self.height):
                # Border tiles are always walls
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    column.append(True)
                elif random.random() < self.fill_probability:
                    column.append(True)
                else:
                    column.append(False)
            self._wall_grid.append(column)

    def _smooth_map(self) -> None:
        """
        Apply one iteration of cellular automata smoothing.

        Rules:
        - If a tile has >= wall_threshold wall neighbors, it becomes a wall
        - If a tile has >= (9 - wall_threshold) floor neighbors, it becomes floor
        - Otherwise, it stays the same
        """
        new_grid: List[List[bool]] = []

        for x in range(self.width):
            column = []
            for y in range(self.height):
                wall_count = self._count_wall_neighbors(x, y)

                if wall_count >= self.wall_threshold:
                    column.append(True)
                elif wall_count <= 9 - self.wall_threshold - 1:
                    # More floors than threshold, becomes floor
                    column.append(False)
                else:
                    # Keep current state
                    column.append(self._wall_grid[x][y])
            new_grid.append(column)

        self._wall_grid = new_grid

    def _count_wall_neighbors(self, x: int, y: int) -> int:
        """
        Count wall neighbors around a tile (including the tile itself).

        Out-of-bounds tiles count as walls to encourage walls at edges.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Number of wall tiles in the 3x3 area centered on (x, y)
        """
        count = 0

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy

                if not self._in_bounds(nx, ny):
                    # Out of bounds counts as wall
                    count += 1
                elif self._wall_grid[nx][ny]:
                    count += 1

        return count

    def _in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _enforce_borders(self) -> None:
        """Ensure all border tiles are walls."""
        for x in range(self.width):
            self._wall_grid[x][0] = True
            self._wall_grid[x][self.height - 1] = True

        for y in range(self.height):
            self._wall_grid[0][y] = True
            self._wall_grid[self.width - 1][y] = True

    def _find_regions(self) -> List[Set[Tuple[int, int]]]:
        """
        Find all disconnected floor regions using flood fill.

        Returns:
            List of sets, each containing (x, y) tuples for a connected region
        """
        visited: Set[Tuple[int, int]] = set()
        regions: List[Set[Tuple[int, int]]] = []

        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in visited and not self._wall_grid[x][y]:
                    region = self._flood_fill(x, y, visited)
                    if region:
                        regions.append(region)

        # Sort regions by size (largest first)
        regions.sort(key=len, reverse=True)
        return regions

    def _flood_fill(
        self,
        start_x: int,
        start_y: int,
        visited: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        """
        Flood fill from a starting point to find connected floor tiles.

        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            visited: Set of already visited coordinates (modified in place)

        Returns:
            Set of (x, y) tuples in the connected region
        """
        region: Set[Tuple[int, int]] = set()
        queue: deque = deque([(start_x, start_y)])

        while queue:
            x, y = queue.popleft()

            if (x, y) in visited:
                continue
            if not self._in_bounds(x, y):
                continue
            if self._wall_grid[x][y]:
                continue

            visited.add((x, y))
            region.add((x, y))

            # Add 4-directional neighbors (more natural tunnels)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    queue.append((nx, ny))

        return region

    def _connect_all_regions(self, regions: List[Set[Tuple[int, int]]]) -> None:
        """
        Connect all regions to the largest region with tunnels.

        Uses a simple strategy: connect each smaller region to the
        closest point in the largest (main) region.

        Args:
            regions: List of region sets, sorted by size (largest first)
        """
        if len(regions) <= 1:
            return

        main_region = regions[0]

        for i in range(1, len(regions)):
            smaller_region = regions[i]

            # Find closest points between main region and smaller region
            closest_main, closest_small = self._find_closest_points(
                main_region, smaller_region
            )

            if closest_main and closest_small:
                # Carve tunnel between the two points
                self._carve_tunnel(closest_main, closest_small)

                # Add smaller region to main region
                main_region.update(smaller_region)

                logger.debug(
                    "Connected region %d (size %d) via tunnel (%d,%d)->(%d,%d)",
                    i, len(smaller_region),
                    closest_small[0], closest_small[1],
                    closest_main[0], closest_main[1]
                )

    def _find_closest_points(
        self,
        region_a: Set[Tuple[int, int]],
        region_b: Set[Tuple[int, int]]
    ) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Find the closest pair of points between two regions.

        Args:
            region_a: First region
            region_b: Second region

        Returns:
            Tuple of (point_in_a, point_in_b) that are closest together
        """
        best_distance = float('inf')
        best_a: Optional[Tuple[int, int]] = None
        best_b: Optional[Tuple[int, int]] = None

        # Sample points if regions are very large to improve performance
        sample_a = region_a if len(region_a) <= 100 else random.sample(list(region_a), 100)
        sample_b = region_b if len(region_b) <= 100 else random.sample(list(region_b), 100)

        for ax, ay in sample_a:
            for bx, by in sample_b:
                distance = abs(ax - bx) + abs(ay - by)  # Manhattan distance
                if distance < best_distance:
                    best_distance = distance
                    best_a = (ax, ay)
                    best_b = (bx, by)

        return best_a, best_b

    def _carve_tunnel(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> None:
        """
        Carve a tunnel between two points using L-shaped corridor.

        Args:
            start: Starting (x, y) coordinate
            end: Ending (x, y) coordinate
        """
        x1, y1 = start
        x2, y2 = end

        # Randomly choose horizontal-first or vertical-first
        if random.random() < 0.5:
            # Horizontal then vertical
            self._carve_horizontal_tunnel(x1, x2, y1)
            self._carve_vertical_tunnel(y1, y2, x2)
        else:
            # Vertical then horizontal
            self._carve_vertical_tunnel(y1, y2, x1)
            self._carve_horizontal_tunnel(x1, x2, y2)

    def _carve_horizontal_tunnel(self, x1: int, x2: int, y: int) -> None:
        """Carve a horizontal tunnel at y from x1 to x2."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self._in_bounds(x, y) and not self._is_border(x, y):
                self._wall_grid[x][y] = False

    def _carve_vertical_tunnel(self, y1: int, y2: int, x: int) -> None:
        """Carve a vertical tunnel at x from y1 to y2."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self._in_bounds(x, y) and not self._is_border(x, y):
                self._wall_grid[x][y] = False

    def _is_border(self, x: int, y: int) -> bool:
        """Check if a tile is on the map border."""
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def _create_rooms(self) -> None:
        """
        Create Room objects from large connected floor areas.

        Finds connected floor regions and creates bounding-box Room objects
        for regions larger than min_room_size. These rooms are used for
        spawn placement compatibility with the existing dungeon system.
        """
        self.rooms = []
        visited: Set[Tuple[int, int]] = set()

        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in visited and not self._wall_grid[x][y]:
                    region = self._flood_fill(x, y, visited)

                    if len(region) >= self.min_room_size:
                        room = self._region_to_room(region)
                        self.rooms.append(room)
                        logger.debug(
                            "Created room from region: %d tiles -> "
                            "Room(x=%d, y=%d, w=%d, h=%d)",
                            len(region), room.x, room.y,
                            room.width, room.height
                        )

    def _region_to_room(self, region: Set[Tuple[int, int]]) -> Room:
        """
        Convert a set of floor tiles to a Room bounding box.

        Args:
            region: Set of (x, y) floor tile coordinates

        Returns:
            Room object representing the bounding box of the region
        """
        min_x = min(pos[0] for pos in region)
        max_x = max(pos[0] for pos in region)
        min_y = min(pos[1] for pos in region)
        max_y = max(pos[1] for pos in region)

        return Room(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

    def _convert_to_entity_map(self) -> None:
        """
        Convert the boolean wall grid to entity_map with Tile objects.

        Called after all generation is complete to create the final
        entity_map that TileMap expects.
        """
        logger.debug("Converting wall grid to entity map")
        self.entity_map = []
        wall_count = 0
        floor_count = 0

        for x in range(self.width):
            column = []
            for y in range(self.height):
                if self._wall_grid[x][y]:
                    column.append(self.create_wall(x, y))
                    wall_count += 1
                else:
                    column.append(self.create_floor(x, y))
                    floor_count += 1
            self.entity_map.append(column)

        # Clean up temporary grid
        del self._wall_grid

        logger.debug("Entity map created: %d walls, %d floors", wall_count, floor_count)

    def __str__(self) -> str:
        """Return ASCII representation of the cave map."""
        if not self.entity_map:
            return "<CaveGenerator: not generated>"

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

"""
Map Utility Module
==================

Utility functions for dungeon map generation including room placement,
corridor carving, and stair placement.
"""

import random
from logging_config import get_logger, log_high_priority

from .room import Room
from dungeon_generation.tiles import UpStairs, DownStairs, Floor, Wall, Gateway

logger = get_logger(__name__)


def place_room(tilemap, rWidth: int, rHeight: int, circularity: float) -> bool:
    """
    Attempt to place a room on the tilemap.

    Args:
        tilemap: The tilemap to place the room on
        rWidth: Room width
        rHeight: Room height
        circularity: Circularity factor for room shape

    Returns:
        True if room was placed, False if placement failed after max tries
    """
    MaxTries = 100
    logger.debug("Attempting to place room: size=%dx%d, circularity=%.2f", rWidth, rHeight, circularity)

    startX = random.randint(1, tilemap.get_width() - rWidth - 1)
    startY = random.randint(1, tilemap.get_height() - rHeight - 1)
    room = Room(startX, startY, rWidth, rHeight)
    tries = 0

    while (tilemap.overlaps_any(room) and tilemap.get_in_squircle(room, circularity) and tries < MaxTries):
        room.x = random.randint(1, tilemap.get_width() - rWidth - 1)
        room.y = random.randint(1, tilemap.get_height() - rHeight - 1)
        tries += 1
        if tries % 20 == 0:
            logger.debug("Room placement: %d/%d attempts", tries, MaxTries)

    if tries < MaxTries:
        tilemap.rooms.append(room)
        logger.info("Room placed at (%d, %d), size %dx%d after %d tries",
                   room.x, room.y, rWidth, rHeight, tries)
        carve_room(tilemap, room, circularity)
        return True
    else:
        logger.warning("Failed to place room after %d attempts", MaxTries)
        return False


def construct_rooms(tilemap) -> None:
    """
    Construct all rooms for the tilemap and connect them.

    Args:
        tilemap: The tilemap to construct rooms on
    """
    num_rooms = tilemap.get_num_rooms()
    logger.info("Constructing %d rooms", num_rooms)

    for roomNum in range(num_rooms):
        size = random.randint(4, tilemap.get_room_size())
        logger.debug("Room %d/%d: generating with size %d", roomNum + 1, num_rooms, size)
        place_room(tilemap, size, size, tilemap.get_circularity())

    # Connect Rooms
    logger.debug("Connecting %d rooms", len(tilemap.rooms))
    for i in range(len(tilemap.rooms) - 1):
        logger.debug("Connecting room %d to room %d", i, i + 1)
        connect_rooms(tilemap, tilemap.rooms[i], tilemap.rooms[i + 1])

    logger.info("Room construction complete: %d rooms created and connected", len(tilemap.rooms))


def connect_rooms(tilemap, room1: Room, room2: Room) -> None:
    """
    Connect two rooms with a corridor.

    Args:
        tilemap: The tilemap containing the rooms
        room1: First room to connect
        room2: Second room to connect
    """
    cornerX: int = room1.GetCenterX()
    cornerY: int = room2.GetCenterY()

    logger.debug("Connecting rooms: (%d,%d) center=(%d,%d) to (%d,%d) center=(%d,%d) via corner (%d,%d)",
                room1.x, room1.y, room1.GetCenterX(), room1.GetCenterY(),
                room2.x, room2.y, room2.GetCenterX(), room2.GetCenterY(),
                cornerX, cornerY)

    # First corridor segment (room1 to corner)
    lower1X = min(room1.GetCenterX(), cornerX)
    upper1X = max(room1.GetCenterX(), cornerX) + 1
    lower1Y = min(room1.GetCenterY(), cornerY)
    upper1Y = max(room1.GetCenterY(), cornerY) + 1

    tiles_carved_1 = 0
    for x in range(lower1X, upper1X):
        for y in range(lower1Y, upper1Y):
            if tilemap.track_map_render[x][y] == "x":
                tilemap.track_map_render[x][y] = "."
                tiles_carved_1 += 1

    # Second corridor segment (corner to room2)
    lower2X = min(room2.GetCenterX(), cornerX)
    upper2X = max(room2.GetCenterX(), cornerX) + 1
    lower2Y = min(room2.GetCenterY(), cornerY)
    upper2Y = max(room2.GetCenterY(), cornerY) + 1

    tiles_carved_2 = 0
    for x in range(lower2X, upper2X):
        for y in range(lower2Y, upper2Y):
            if tilemap.track_map_render[x][y] == "x":
                tilemap.track_map_render[x][y] = "."
                tiles_carved_2 += 1

    logger.debug("Corridor carved: %d + %d = %d tiles", tiles_carved_1, tiles_carved_2, tiles_carved_1 + tiles_carved_2)


def carve_room(tilemap, room: Room, circularity: float) -> None:
    """
    Carve out a room in the tilemap's render map using squircle geometry.

    Args:
        tilemap: The tilemap to carve
        room: The room to carve
        circularity: Circularity factor (0 = square, 1 = circle)
    """
    logger.debug("Carving room at (%d, %d), size %dx%d, circularity=%.2f",
                room.x, room.y, room.width, room.height, circularity)

    originX = 1.0 * (room.width - 1) / 2
    originY = 1.0 * (room.height - 1) / 2
    radius = max(room.width, room.height) / 2

    radiusSqrd = radius ** 2
    squircConst = ((1 - circularity) / radius) ** 2

    tiles_carved = 0
    for x in range(room.width):
        for y in range(room.height):
            localX = x - originX
            localY = y - originY

            xSqrd = localX ** 2
            ySqrd = localY ** 2

            squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

            if squircleVal < radiusSqrd:
                tilemap.track_map_render[x + room.x][y + room.y] = "."
                tiles_carved += 1

    logger.debug("Carved %d tiles for room", tiles_carved)


def place_stairs(tilemap) -> None:
    """
    Place stairs (up and down) on the tilemap.

    Args:
        tilemap: The tilemap to place stairs on
    """
    logger.info("Placing stairs on floor depth=%d, branch=%s", tilemap.get_depth(), tilemap.get_branch())

    # Place upstairs
    startx, starty = tilemap.get_random_location()
    upstairs = UpStairs(startx, starty)
    tilemap.stairs.append(upstairs)
    tilemap.place_tile(upstairs)
    logger.debug("Placed UpStairs at (%d, %d)", startx, starty)

    # Place downstairs (2 sets)
    for i in range(2):
        startx, starty = tilemap.get_random_location()
        downstairs = DownStairs(startx, starty)
        tilemap.stairs.append(downstairs)
        tilemap.place_tile(downstairs)
        logger.debug("Placed DownStairs #%d at (%d, %d)", i + 1, startx, starty)

    # Additional upstairs for non-first floors
    if tilemap.get_depth() != 1:
        startx, starty = tilemap.get_random_location()
        upstairs = UpStairs(startx, starty)
        tilemap.stairs.append(upstairs)
        tilemap.place_tile(upstairs)
        logger.debug("Placed additional UpStairs at (%d, %d) (depth > 1)", startx, starty)

    logger.info("Stairs placement complete: %d total stairs", len(tilemap.stairs))


def place_gateways(tilemap, gateway_data) -> None:
    """
    Place gateways on the tilemap based on gateway_data configuration.

    Args:
        tilemap: The tilemap to place gateways on
        gateway_data: GatewayData configuration object containing connection info
    """
    branch = tilemap.get_branch()
    depth = tilemap.get_depth()

    logger.info("Placing gateways on floor depth=%d, branch=%s", depth, branch)

    if not gateway_data.has_gateway(branch, depth):
        logger.debug("No gateways configured for %s floor %d", branch, depth)
        return

    destinations = gateway_data.get_destinations(branch, depth)
    logger.debug("Found %d gateway destinations for %s floor %d", len(destinations), branch, depth)

    for dest in destinations:
        # Check spawn chance for random connections
        conn = gateway_data.get_connection(branch, depth, dest.branch, dest.depth)
        if conn and conn.spawn_chance < 1.0:
            if random.random() > conn.spawn_chance:
                logger.debug("Gateway to %s floor %d skipped (spawn_chance=%.2f)",
                           dest.branch, dest.depth, conn.spawn_chance)
                continue

        # Place the gateway
        startx, starty = tilemap.get_random_location()

        # Create gateway - it will be paired later during init_game
        gateway = Gateway(startx, starty, level=depth, branch=branch)
        tilemap.gateway.append(gateway)
        tilemap.place_tile(gateway)

        logger.debug("Placed Gateway at (%d, %d) for connection to %s floor %d",
                    startx, starty, dest.branch, dest.depth)

    logger.info("Gateway placement complete: %d total gateways", len(tilemap.gateway))


def render_to_map(tilemap) -> None:
    """
    Convert the ASCII render map to actual tile objects.

    Args:
        tilemap: The tilemap to render

    Raises:
        Exception: If render map dimensions don't match tilemap dimensions
    """
    logger.debug("Rendering track_map_render to entity_map")
    logger.debug("Tilemap dimensions: %dx%d", tilemap.width, tilemap.height)
    logger.debug("Render map dimensions: %dx%d",
                len(tilemap.track_map_render),
                len(tilemap.track_map_render[0]) if tilemap.track_map_render else 0)

    if tilemap.width != len(tilemap.track_map_render) or tilemap.height != len(tilemap.track_map_render[0]):
        error_msg = (f"Map size mismatch: tilemap={tilemap.width}x{tilemap.height}, "
                    f"render_map={len(tilemap.track_map_render)}x{len(tilemap.track_map_render[0])}")
        log_high_priority(logger, error_msg)
        return

    tilemap.entity_map = []
    wall_count = 0
    floor_count = 0
    edge_override_count = 0

    # First pass: create basic tiles
    for x in range(tilemap.width):
        temp = []
        for y in range(tilemap.height):
            text = tilemap.track_map_render[x][y]

            # Edge tiles must be walls
            if x == 0 or y == 0 or x == tilemap.width - 1 or y == tilemap.height - 1:
                if text != "x":
                    logger.warning("Edge tile at (%d, %d) was '%s', overriding to wall", x, y, text)
                    edge_override_count += 1
                temp.append(Wall(x, y))
                wall_count += 1
            elif text == "x":
                temp.append(Wall(x, y))
                wall_count += 1
            elif text == ".":
                temp.append(Floor(x, y))
                floor_count += 1
            else:
                logger.warning("Unknown tile '%s' at (%d, %d), defaulting to wall", text, x, y)
                temp.append(Wall(x, y))
                wall_count += 1

        tilemap.entity_map.append(temp)

    # Second pass: add water for Ocean branch
    if tilemap.get_branch() == "Ocean":
        _add_ocean_water(tilemap)

    logger.info("Render complete: %d walls, %d floors, %d edge overrides",
               wall_count, floor_count, edge_override_count)


def _add_ocean_water(tilemap) -> None:
    """
    Calculate elevation for Ocean branch maps.

    Sets elevation on floor tiles based on distance from shore (walls/stairs).
    Lower elevation = center of large spaces (floods first).
    Higher elevation = closer to shore (floods later).
    Tiles near stairs have elevation=None and never flood.
    The actual water terrain is applied by the tide system.
    """
    logger.info("Calculating elevations for Ocean branch")

    # First pass: mark tiles near stairs as protected (elevation=None)
    _mark_protected_tiles(tilemap)

    # Second pass: calculate distance from shore for all floor tiles
    max_depth = 0
    depths = {}

    for x in range(1, tilemap.width - 1):
        for y in range(1, tilemap.height - 1):
            tile = tilemap.entity_map[x][y]
            if not tile.has_trait("floor"):
                continue
            if tile.elevation == -1:
                continue  # Protected tile, skip

            # Calculate distance to shore
            depth = _calculate_distance_to_shore(tilemap, x, y)
            depths[(x, y)] = depth
            max_depth = max(max_depth, depth)

    # Third pass: invert depths to get elevation (high at shore, low in center)
    # Also reset protected tiles from -1 to None
    for x in range(tilemap.width):
        for y in range(tilemap.height):
            tile = tilemap.entity_map[x][y]
            if tile.elevation == -1:
                tile.elevation = None  # Protected: never floods
            elif (x, y) in depths:
                # Invert: shoreline (depth=0) gets high elevation, center gets low
                tile.elevation = max_depth - depths[(x, y)]

    # Log statistics
    elevation_counts = {}
    for x in range(tilemap.width):
        for y in range(tilemap.height):
            tile = tilemap.entity_map[x][y]
            if hasattr(tile, 'elevation') and tile.elevation is not None:
                elev = tile.elevation
                elevation_counts[elev] = elevation_counts.get(elev, 0) + 1

    logger.info("Ocean elevations calculated (0=center, %d=shore): %s", max_depth, elevation_counts)


def _mark_protected_tiles(tilemap) -> None:
    """
    Mark tiles near stairs as protected from flooding (elevation=None).

    Tiles within 2 spaces of any stairs will never have water.
    We set elevation to a sentinel value temporarily, then keep it as None.
    """
    protected_radius = 2

    for x in range(tilemap.width):
        for y in range(tilemap.height):
            tile = tilemap.entity_map[x][y]
            if tile.has_trait("stairs") or tile.has_trait("gateway"):
                # Mark all tiles within radius as protected
                for dx in range(-protected_radius, protected_radius + 1):
                    for dy in range(-protected_radius, protected_radius + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < tilemap.width and 0 <= ny < tilemap.height:
                            neighbor = tilemap.entity_map[nx][ny]
                            if hasattr(neighbor, 'elevation'):
                                # Use a special marker; will remain None after processing
                                neighbor.elevation = -1  # Temporary marker


def _calculate_distance_to_shore(tilemap, x: int, y: int) -> int:
    """
    Calculate distance to shore (walls or protected tiles).

    Returns:
        Distance value (0 = adjacent to wall/protected, higher = further from shore)
    """
    # Check if adjacent to wall or protected tile
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < tilemap.width and 0 <= ny < tilemap.height:
                neighbor = tilemap.entity_map[nx][ny]
                if neighbor.has_trait("wall"):
                    return 0  # Adjacent to wall = shoreline
                if hasattr(neighbor, 'elevation') and neighbor.elevation == -1:
                    return 0  # Adjacent to protected area = shoreline

    # Use minimum cardinal distance to wall/protected as depth
    return _min_distance_to_shore(tilemap, x, y)


def _min_distance_to_shore(tilemap, x: int, y: int) -> int:
    """
    Find minimum distance to shore (wall or protected tile) in any cardinal direction.

    Args:
        tilemap: The tilemap to check
        x: X coordinate
        y: Y coordinate

    Returns:
        Minimum distance to shore in any cardinal direction
    """
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, W, E
    min_dist = float('inf')

    for dx, dy in directions:
        dist = 0
        cx, cy = x + dx, y + dy
        while 0 < cx < tilemap.width - 1 and 0 < cy < tilemap.height - 1:
            tile = tilemap.entity_map[cx][cy]
            if tile.has_trait("wall"):
                break
            if hasattr(tile, 'elevation') and tile.elevation == -1:
                break
            dist += 1
            cx += dx
            cy += dy
        min_dist = min(min_dist, dist)

    return min_dist if min_dist != float('inf') else 0

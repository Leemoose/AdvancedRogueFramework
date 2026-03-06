"""
Map Utility Module
==================

Utility functions for dungeon map generation including stair placement
and ocean water calculations.
"""

import random
from logging_config import get_logger

from dungeon_generation.tiles import UpStairs, DownStairs, Gateway

logger = get_logger(__name__)


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


def add_ocean_water(tilemap) -> None:
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

    for x in range(1, tilemap.width - 1):
        for y in range(1, tilemap.height - 1):
            tile = tilemap.entity_map[x][y]
            if not tile.has_trait("floor"):
                continue
            if tile.elevation == 0:
                continue  # Protected tile, skip

            # Calculate distance to shore
            depth = _calculate_distance_to_shore(tilemap, x, y)
            tile.elevation = - (depth * 10 + random.randint(0,10))

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
                                neighbor.elevation = 0  # Temporary marker


def _calculate_distance_to_shore(tilemap, x: int, y: int) -> int:
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
            if hasattr(tile, 'elevation') and tile.elevation == 0:
                break
            dist += 1
            cx += dx
            cy += dy
        min_dist = min(min_dist, dist)

    return min_dist if min_dist != float('inf') else 0


def apply_forest_theme(tilemap) -> None:
    """
    Apply forest-themed tiles to the tilemap for the Forest branch.

    Swaps default tiles (grass/path floors, wall, doors, stairs, portal)
    to dense forest variants.

    Args:
        tilemap: The tilemap to apply forest theme to
    """
    logger.info("Applying forest theme to tilemap")

    # Define render tag mappings (default -> forest theme)
    # Maps all grass/path floor variants + wall/door/stairs/portal defaults
    tile_mappings = {
        100: 151,  # Floor: GRASS_1 -> DENSE_FOREST_FLOOR
        101: 151,  # Floor: GRASS_2 -> DENSE_FOREST_FLOOR
        102: 151,  # Floor: GRASS_3 -> DENSE_FOREST_FLOOR
        103: 151,  # Floor: GRASS_4 -> DENSE_FOREST_FLOOR
        104: 151,  # Floor: PATH_1 -> DENSE_FOREST_FLOOR
        105: 151,  # Floor: PATH_2 -> DENSE_FOREST_FLOOR
        106: 151,  # Floor: PATH_3 -> DENSE_FOREST_FLOOR
        107: 151,  # Floor: PATH_4 -> DENSE_FOREST_FLOOR
        200: 221,  # Wall: DEFAULT -> DENSE_FOREST_WALL
        300: 322,  # Door closed: DEFAULT -> DENSE_FOREST_DOOR_CLOSED
        301: 323,  # Door open: DEFAULT -> DENSE_FOREST_DOOR_OPEN
        400: 433,  # Stairs up: DEFAULT -> DENSE_FOREST_STAIRS_UP
        410: 434,  # Stairs down: DEFAULT -> DENSE_FOREST_STAIRS_DOWN
        420: 435,  # Portal: DEFAULT -> DENSE_FOREST_PORTAL
    }

    tiles_changed = 0

    for x in range(tilemap.width):
        for y in range(tilemap.height):
            tile = tilemap.entity_map[x][y]
            current_tag = tile.get_render_tag()

            if current_tag in tile_mappings:
                tile.render_tag = tile_mappings[current_tag]
                tiles_changed += 1

    logger.info("Forest theme applied: %d tiles changed", tiles_changed)

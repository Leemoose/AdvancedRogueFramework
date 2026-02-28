"""
Targeting functions for spells.

These functions take a target (entity, position, or direction) and context,
and return a list of actual targets (entities or positions) to apply effects to.
"""

from typing import List, Tuple, Any, Optional
from logging_config import get_logger

logger = get_logger(__name__)


def get_single_target(target, context) -> List:
    """
    Return the target as a single-element list.

    Args:
        target: An entity or position
        context: SpellContext

    Returns:
        [target] if target exists, [] otherwise
    """
    if target is None:
        return []
    return [target]


def get_enemies_in_radius(
    center,
    radius: int,
    context,
    include_center: bool = True
) -> List:
    """
    Get all enemy entities within radius of center position.

    Args:
        center: Center point - can be (x, y) tuple or entity
        radius: Radius in tiles (uses circular distance)
        context: SpellContext
        include_center: Whether to include entity at exact center

    Returns:
        List of enemy entities within radius
    """
    cx, cy = _get_position(center)
    if cx is None:
        return []

    enemies = []
    monster_map = context.monster_map

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            # Circular radius check
            if dx * dx + dy * dy > radius * radius:
                continue

            if not include_center and dx == 0 and dy == 0:
                continue

            x, y = cx + dx, cy + dy

            # Check for entity at this position
            entity = context.get_entity_at(x, y)
            if entity is not None:
                # Don't include the caster
                if entity != context.caster:
                    enemies.append(entity)

    logger.debug(f"get_enemies_in_radius: Found {len(enemies)} enemies within radius {radius} of ({cx}, {cy})")
    return enemies


def get_entities_in_radius(
    center,
    radius: int,
    context,
    include_center: bool = True,
    include_caster: bool = False
) -> List:
    """
    Get all entities (enemies and allies) within radius of center position.

    Args:
        center: Center point - can be (x, y) tuple or entity
        radius: Radius in tiles (uses circular distance)
        context: SpellContext
        include_center: Whether to include entity at exact center
        include_caster: Whether to include the caster if in range

    Returns:
        List of entities within radius
    """
    cx, cy = _get_position(center)
    if cx is None:
        return []

    entities = []

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue

            if not include_center and dx == 0 and dy == 0:
                continue

            x, y = cx + dx, cy + dy
            entity = context.get_entity_at(x, y)

            if entity is not None:
                if entity == context.caster and not include_caster:
                    continue
                entities.append(entity)

    logger.debug(f"get_entities_in_radius: Found {len(entities)} entities within radius {radius}")
    return entities


def get_positions_in_radius(
    center,
    radius: int,
    context,
    include_center: bool = True,
    passable_only: bool = False
) -> List[Tuple[int, int]]:
    """
    Get all positions within radius of center.

    Args:
        center: Center point - can be (x, y) tuple or entity
        radius: Radius in tiles (uses circular distance)
        context: SpellContext
        include_center: Whether to include the center position
        passable_only: Only return passable tiles

    Returns:
        List of (x, y) positions within radius
    """
    cx, cy = _get_position(center)
    if cx is None:
        return []

    positions = []

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue

            if not include_center and dx == 0 and dy == 0:
                continue

            x, y = cx + dx, cy + dy

            if passable_only and not context.get_passable(x, y):
                continue

            positions.append((x, y))

    logger.debug(f"get_positions_in_radius: Found {len(positions)} positions within radius {radius}")
    return positions


def get_adjacent_positions(center, context) -> List[Tuple[int, int]]:
    """
    Get all 8 adjacent positions to center.

    Args:
        center: Center point - can be (x, y) tuple or entity
        context: SpellContext

    Returns:
        List of 8 adjacent (x, y) positions
    """
    cx, cy = _get_position(center)
    if cx is None:
        return []

    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    return [(cx + dx, cy + dy) for dx, dy in directions]


def get_passable_adjacent_positions(center, context) -> List[Tuple[int, int]]:
    """
    Get adjacent positions that are passable.

    Args:
        center: Center point - can be (x, y) tuple or entity
        context: SpellContext

    Returns:
        List of passable adjacent (x, y) positions
    """
    positions = get_adjacent_positions(center, context)
    return [(x, y) for x, y in positions if context.get_passable(x, y)]


def get_line_positions(
    start,
    end,
    context,
    include_start: bool = False,
    include_end: bool = True,
    stop_at_blocked: bool = True
) -> List[Tuple[int, int]]:
    """
    Get positions in a line from start to end using Bresenham's algorithm.

    Args:
        start: Starting position - can be (x, y) tuple or entity
        end: Ending position - can be (x, y) tuple or entity
        context: SpellContext
        include_start: Whether to include starting position
        include_end: Whether to include ending position
        stop_at_blocked: Stop the line at non-passable tiles

    Returns:
        List of (x, y) positions along the line
    """
    x0, y0 = _get_position(start)
    x1, y1 = _get_position(end)

    if x0 is None or x1 is None:
        return []

    positions = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0

    while True:
        # Check if we should include this position
        is_start = (x == x0 and y == y0)
        is_end = (x == x1 and y == y1)

        if is_start and not include_start:
            pass
        elif is_end and not include_end:
            pass
        else:
            if stop_at_blocked and not context.get_passable(x, y) and not is_start:
                break
            positions.append((x, y))

        if x == x1 and y == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return positions


def get_cone_positions(
    origin,
    direction: Tuple[int, int],
    length: int,
    context,
    angle_width: int = 90
) -> List[Tuple[int, int]]:
    """
    Get positions in a cone from origin in a direction.

    Args:
        origin: Starting position - can be (x, y) tuple or entity
        direction: Direction tuple (dx, dy) normalized to -1, 0, or 1
        length: How far the cone extends
        context: SpellContext
        angle_width: Cone angle in degrees (90 = quarter circle)

    Returns:
        List of (x, y) positions in the cone
    """
    import math

    ox, oy = _get_position(origin)
    if ox is None:
        return []

    dx, dy = direction
    if dx == 0 and dy == 0:
        return []

    # Calculate base angle of the direction
    base_angle = math.atan2(dy, dx)
    half_angle = math.radians(angle_width / 2)

    positions = []

    # Check all positions within length distance
    for check_dx in range(-length, length + 1):
        for check_dy in range(-length, length + 1):
            if check_dx == 0 and check_dy == 0:
                continue

            # Check distance
            dist = math.sqrt(check_dx * check_dx + check_dy * check_dy)
            if dist > length:
                continue

            # Check angle
            pos_angle = math.atan2(check_dy, check_dx)
            angle_diff = abs(pos_angle - base_angle)

            # Normalize angle difference
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff

            if angle_diff <= half_angle:
                x, y = ox + check_dx, oy + check_dy
                positions.append((x, y))

    return positions


def _get_position(target) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract (x, y) position from various target types.

    Args:
        target: Can be (x, y) tuple, entity with get_location(), or None

    Returns:
        (x, y) tuple or (None, None) if invalid
    """
    if target is None:
        return None, None

    if isinstance(target, tuple) and len(target) == 2:
        return target[0], target[1]

    if hasattr(target, 'get_location'):
        return target.get_location()

    if hasattr(target, 'x') and hasattr(target, 'y'):
        return target.x, target.y

    logger.warning(f"_get_position: Cannot extract position from {type(target)}")
    return None, None

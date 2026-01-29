"""
Direction vectors for 2D grid movement.

This module provides centralized direction constants for consistent use across
the roguelike game. All direction vectors use the convention (dx, dy) where:
- Positive x is East (right)
- Negative x is West (left)
- Positive y is South (down)
- Negative y is North (up)

Note: This follows screen coordinate conventions where y increases downward.
"""

from typing import List, Tuple


class Directions:
    """
    Centralized direction vectors for grid-based movement and neighbor checking.

    This class provides constant lists of direction vectors for different types
    of movement patterns. Use these constants instead of hardcoding direction
    lists throughout the codebase.

    Attributes:
        CARDINAL_4: The four cardinal directions (North, South, East, West).
            Use for basic 4-way movement or when diagonal movement is not allowed.

        DIAGONAL_4: The four diagonal directions (NE, SW, SE, NW).
            Use when only diagonal movement is needed.

        ALL_8: All eight directions combining cardinal and diagonal.
            Use for standard 8-way movement or checking all neighbors.

    Example:
        >>> from src.core.directions import Directions
        >>> for dx, dy in Directions.CARDINAL_4:
        ...     neighbor_x = current_x + dx
        ...     neighbor_y = current_y + dy
    """

    CARDINAL_4: List[Tuple[int, int]] = [
        (0, 1),   # South (down)
        (0, -1),  # North (up)
        (1, 0),   # East (right)
        (-1, 0),  # West (left)
    ]
    """
    The four cardinal directions: North, South, East, West.

    Order: South, North, East, West
    Vectors: (0, 1), (0, -1), (1, 0), (-1, 0)
    """

    DIAGONAL_4: List[Tuple[int, int]] = [
        (1, 1),   # Southeast
        (-1, -1), # Northwest
        (1, -1),  # Northeast
        (-1, 1),  # Southwest
    ]
    """
    The four diagonal directions: NE, SW, SE, NW.

    Order: Southeast, Northwest, Northeast, Southwest
    Vectors: (1, 1), (-1, -1), (1, -1), (-1, 1)
    """

    ALL_8: List[Tuple[int, int]] = CARDINAL_4 + DIAGONAL_4
    """
    All eight directions combining cardinal and diagonal movement.

    This is the most common direction list used for:
    - Standard 8-way movement
    - Checking all adjacent neighbors
    - Pathfinding algorithms

    Order: South, North, East, West, Southeast, Northwest, Northeast, Southwest
    """

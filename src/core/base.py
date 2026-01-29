"""
Base Game Object
================

Provides the foundational class for all game entities including
players, monsters, items, tiles, and interactables.

This replaces the original objects.py with improved:
- Type hints
- Documentation
- Property-based access
- Consistent interface
"""

from __future__ import annotations
from typing import Dict, Tuple, Optional, List, Any
from dataclasses import dataclass, field
import math

from .constants import NO_ENTITY, NO_ID


@dataclass
class Position:
    """
    Represents a 2D position in the game world.

    Attributes:
        x: Horizontal position (column)
        y: Vertical position (row)
    """
    x: int = -1
    y: int = -1

    def __iter__(self):
        """Allow unpacking: x, y = position"""
        yield self.x
        yield self.y

    def as_tuple(self) -> Tuple[int, int]:
        """Return position as (x, y) tuple."""
        return (self.x, self.y)

    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def manhattan_distance_to(self, other: 'Position') -> int:
        """Calculate Manhattan distance to another position."""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def chebyshev_distance_to(self, other: 'Position') -> int:
        """Calculate Chebyshev (chess king) distance to another position."""
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def is_adjacent_to(self, other: 'Position') -> bool:
        """Check if this position is adjacent to another (including diagonals)."""
        return self.chebyshev_distance_to(other) == 1

    def is_valid(self) -> bool:
        """Check if position has been set (not -1, -1)."""
        return self.x >= 0 and self.y >= 0


class GameObject:
    """
    Base class for all game entities.

    This provides common functionality for anything that exists
    in the game world, including position, identification, and
    trait-based capabilities.

    Attributes:
        position: The entity's location in the game world.
        id_tag: Unique identifier assigned by the ID system.
        render_tag: ID used to look up the visual representation.
        name: Human-readable name.
        description: Extended description for examination.
        traits: Dictionary of boolean flags for capabilities/properties.

    Example:
        >>> obj = GameObject(x=5, y=10, name="Test Object")
        >>> obj.add_trait("visible")
        >>> obj.has_trait("visible")
        True
        >>> obj.get_distance(0, 0)
        11.180339887498949
    """

    def __init__(
        self,
        x: int = -1,
        y: int = -1,
        id_tag: int = NO_ID,
        render_tag: int = NO_ENTITY,
        name: str = "Unknown object"
    ):
        """
        Initialize a game object.

        Args:
            x: Horizontal position (defaults to -1, unplaced)
            y: Vertical position (defaults to -1, unplaced)
            id_tag: Unique entity ID (assigned by game)
            render_tag: ID for visual lookup in tile dictionary
            name: Human-readable name
        """
        self._position = Position(x, y)
        self.id_tag = id_tag
        self.render_tag = render_tag
        self.name = name
        self.description = ""
        self._traits: Dict[str, bool] = {"object": True}

    def __str__(self) -> str:
        """Return the object's name when converted to string."""
        return self.name

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"{self.__class__.__name__}(name='{self.name}', pos={self.position})"

    # ==========================================================================
    # POSITION PROPERTIES AND METHODS
    # ==========================================================================

    @property
    def position(self) -> Position:
        """Get the entity's position."""
        return self._position

    @position.setter
    def position(self, value: Tuple[int, int] | Position) -> None:
        """Set position from tuple or Position object."""
        if isinstance(value, Position):
            self._position = value
        else:
            self._position = Position(value[0], value[1])

    @property
    def x(self) -> int:
        """Get horizontal position."""
        return self._position.x

    @x.setter
    def x(self, value: int) -> None:
        """Set horizontal position."""
        self._position.x = value

    @property
    def y(self) -> int:
        """Get vertical position."""
        return self._position.y

    @y.setter
    def y(self, value: int) -> None:
        """Set vertical position."""
        self._position.y = value

    def get_location(self) -> Tuple[int, int]:
        """
        Get position as tuple.

        Returns:
            (x, y) tuple of current position.

        Note:
            Maintained for backward compatibility.
            Prefer using the position property directly.
        """
        return self._position.as_tuple()

    def set_location(self, x: int, y: int) -> None:
        """
        Set position from coordinates.

        Args:
            x: New horizontal position
            y: New vertical position

        Note:
            Maintained for backward compatibility.
            Prefer setting position property directly.
        """
        self._position.x = x
        self._position.y = y

    def get_distance(self, x: int, y: int) -> float:
        """
        Calculate Euclidean distance to a point.

        Args:
            x: Target x coordinate
            y: Target y coordinate

        Returns:
            Distance as a float.
        """
        return self._position.distance_to(Position(x, y))

    def is_in_square(
        self,
        x_start: int,
        x_end: int,
        y_start: int,
        y_end: int
    ) -> bool:
        """
        Check if entity is within a rectangular region.

        Args:
            x_start: Left boundary (inclusive)
            x_end: Right boundary (exclusive)
            y_start: Top boundary (inclusive)
            y_end: Bottom boundary (exclusive)

        Returns:
            True if entity is within the region.
        """
        return (
            x_start <= self.x < x_end and
            y_start <= self.y < y_end
        )

    # ==========================================================================
    # IDENTIFICATION METHODS
    # ==========================================================================

    def get_id_tag(self) -> int:
        """Get the unique entity ID."""
        return self.id_tag

    def set_id(self, new_id: int) -> None:
        """
        Assign a new entity ID.

        Args:
            new_id: The ID to assign.

        Note:
            Renamed from gain_ID for clarity.
        """
        self.id_tag = new_id

    # Legacy method name
    gain_ID = set_id

    def get_render_tag(self) -> int:
        """Get the visual lookup ID."""
        return self.render_tag

    def set_render_tag(self, render_tag: int) -> None:
        """Set the visual lookup ID."""
        self.render_tag = render_tag

    def get_name(self) -> str:
        """Get the human-readable name."""
        return self.name

    def get_render_text(self) -> List[str]:
        """
        Get text for examination display.

        Returns:
            List containing [name, description].
        """
        return [self.name, self.description]

    # ==========================================================================
    # TRAIT SYSTEM
    # ==========================================================================

    def has_trait(self, trait: str) -> bool:
        """
        Check if entity has a specific trait.

        Traits are boolean flags that indicate capabilities or
        properties (e.g., "visible", "passable", "stackable").

        Args:
            trait: The trait name to check.

        Returns:
            True if the entity has the trait, False otherwise.
        """
        return self._traits.get(trait, False)

    def add_trait(self, trait: str) -> None:
        """
        Add a trait to this entity.

        Args:
            trait: The trait name to add.
        """
        self._traits[trait] = True

    def remove_trait(self, trait: str) -> None:
        """
        Remove a trait from this entity.

        Args:
            trait: The trait name to remove.
        """
        self._traits[trait] = False

    def get_all_traits(self) -> Dict[str, bool]:
        """
        Get all traits for this entity.

        Returns:
            Dictionary of trait names to boolean values.
        """
        return self._traits.copy()

    @property
    def traits(self) -> Dict[str, bool]:
        """Direct access to traits dictionary for legacy code."""
        return self._traits

    # ==========================================================================
    # LEGACY COMPATIBILITY
    # ==========================================================================

    # These methods exist for backward compatibility with the original codebase.
    # New code should use the property-based accessors instead.

    def get_x(self) -> int:
        """Get horizontal position (legacy)."""
        return self.x

    def get_y(self) -> int:
        """Get vertical position (legacy)."""
        return self.y

    def get_is_in_square(
        self,
        x_start: int,
        x_end: int,
        y_start: int,
        y_end: int
    ) -> bool:
        """Legacy alias for is_in_square."""
        return self.is_in_square(x_start, x_end, y_start, y_end)

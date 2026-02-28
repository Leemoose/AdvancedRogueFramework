"""
Terrain modification effects - modify tiles at target positions.
"""

from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)

class TerrainEffect(Effect):
    """
    Set terrain to a specific terrain type at a position.

    Args:
        terrain_class: The terrain class to place
        **terrain_kwargs: Arguments passed to terrain constructor
    """

    def __init__(self, terrain_class, **terrain_kwargs):
        self.terrain_class = terrain_class
        self.terrain_kwargs = terrain_kwargs

    def apply(self, position, context) -> bool:
        """Place terrain at position."""
        if position is None or not isinstance(position, tuple):
            logger.warning(f"SetTerrainEffect: Invalid position {position}")
            return False

        x, y = position

        try:
            terrain = self.terrain_class(x=x, y=y, **self.terrain_kwargs)
            #need to fix with getting tile and use add terrain function
            context.tile_map.track_map[x][y].get = terrain
            logger.debug(f"SetTerrainEffect: Placed {self.terrain_class.__name__} at ({x}, {y})")
            return True
        except Exception as e:
            logger.warning(f"SetTerrainEffect: Failed to place terrain at ({x}, {y}): {e}")
            return False

    def __repr__(self):
        return f"SetTerrainEffect({self.terrain_class.__name__})"

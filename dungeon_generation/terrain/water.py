"""
Water terrain effects for the Ocean branch tide system.

ShallowWaterTerrain: Slows entities walking through it
DeepWaterTerrain: Blocks movement for non-flying entities
"""

from .terrain import Terrain
from spell_system.status_effects import Slow
from src.core.asset_registry import TileID
from logging_config import get_logger

logger = get_logger(__name__)


class ShallowWaterTerrain(Terrain):
    """Shallow water terrain - slows movement."""

    def __init__(self, x=-1, y=-1, render_tag=TileID.OCEAN_FLOOR):
        super().__init__(x=x, y=y, effects=[Slow], duration=1,
                         render_tag=render_tag, name="Shallow Water")
        self.traits["shallow_water"] = True
        self.traits["water"] = True

    def get_terrain_message(self):
        return "You wade through shallow water."


class DeepWaterTerrain(Terrain):
    """
    Deep water terrain - blocks movement for non-flying entities.

    Unlike other terrain, this doesn't apply a status effect but instead
    prevents movement entirely (handled by the tile's passability).
    """

    def __init__(self, x=-1, y=-1, render_tag=TileID.DEEP_OCEAN):
        super().__init__(x=x, y=y, effects=[], duration=0,
                         render_tag=render_tag, name="Deep Water")
        self.traits["deep_water"] = True
        self.traits["water"] = True
        self.passable = False

    def get_terrain_message(self):
        return "Deep water blocks your path."


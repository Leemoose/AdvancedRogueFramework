
from .terrain import Terrain
from src.core.asset_registry import TileID
from logging_config import get_logger

logger = get_logger(__name__)


class Pit(Terrain):
#To do, add effect to effects that drops you to next floor
    def __init__(self, x=-1, y=-1, render_tag=TileID.OCEAN_FLOOR):
        #Need to change render tag
        super().__init__(x=x, y=y, effects=[], duration=1,
                         render_tag=render_tag, name="Pit")
        self.traits["pit"] = True

    def get_terrain_message(self):
        return "The pit drops you to the floor below."


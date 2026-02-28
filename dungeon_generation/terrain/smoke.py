
from .terrain import Terrain
from src.core.asset_registry import TileID
from logging_config import get_logger

logger = get_logger(__name__)


class Smoke(Terrain):
#Needs to be checked if working properly
    def __init__(self, x=-1, y=-1, render_tag=TileID.OCEAN_FLOOR):
        #Need to change render tag
        super().__init__(x=x, y=y, effects=[], duration=1,
                         render_tag=render_tag, name="Smoke")
        self.traits["smoke"] = True
        self.vision_radius = 3

    def get_terrain_message(self):
        return "The smoke blocks your eyesight."

    def is_blocking_vision(self, origin = None):
        if origin is not None:
            if self.get_distance(origin[0], origin[1]) <= self.vision_radius:
                return False
        return True


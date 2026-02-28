
from .terrain import Terrain
from spell_system.status_effects import Slow, Suffocate
from src.core.asset_registry import TileID
from logging_config import get_logger

logger = get_logger(__name__)


class Quicksand(Terrain):

    def __init__(self, x=-1, y=-1, render_tag=TileID.OCEAN_FLOOR):
        #Need to change render tag
        super().__init__(x=x, y=y, effects=[Slow, Suffocate], duration=1,
                         render_tag=render_tag, name="Quicksand")
        self.traits["quicksand"] = True

    def get_terrain_message(self):
        return "The quicksand slows your movement and begins to bury you."


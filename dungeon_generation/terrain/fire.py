
from .terrain import Terrain
from spell_system.status_effects import Burn
from src.core.asset_registry import TileID
from logging_config import get_logger

logger = get_logger(__name__)


class Fire(Terrain):

    def __init__(self, x=-1, y=-1, render_tag=-1, duration=1):
        #Need to change render tag
        super().__init__(x=x, y=y, effects=[Burn], duration=duration,
                         render_tag=render_tag, name="Fire")
        self.traits["fire"] = True

    def get_terrain_message(self):
        return "The fire burns you."


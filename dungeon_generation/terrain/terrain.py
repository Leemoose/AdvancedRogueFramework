from objects import Objects
from global_vars import global_bugtesting
from logging_config import get_logger

logger = get_logger(__name__)

class Terrain(Objects):
    def __init__(self, x = -1, y = -1, effects = [], render_tag = -1, duration = 1, name = "Terrain"):
        super().__init__(x = x, y = y, render_tag = render_tag, name = name)
        self.traits["terrain"] = True
        self.effects = effects
        self.duration = duration
        #duration not currently used
        self.passable = True
        self.blocks_vision = False

    def apply_effects(self, target):
        for effect in self.effects:
            if effect.has_trait("status_effect"):
                target.character.status.add_status_effect(effect(self, duration = self.duration))
                logger.debug("The terrain applied %s to %s", effect, target.name)
            elif effect.has_trait("effect"):
                pass
                #Want to make sure we have more robust system for one time effects


    def get_terrain_message(self):
        return f"The ground is covered in {self.name}"

    def is_passable(self, entity = None):
        #Need to add variable for flyers
        return self.passable

    def is_blocking_vision(self, origin = False):
        return self.blocks_vision

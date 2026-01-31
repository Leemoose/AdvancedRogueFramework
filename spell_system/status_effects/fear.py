"""Fear status effect - causes monsters to flee."""

from logging_config import get_logger
from .base import StatusEffect

logger = get_logger(__name__)


class Fear(StatusEffect):
    """Debuff that makes monsters flee from the inflictor."""

    def __init__(self, duration, inflictor):
        super().__init__(806, "Fear", "is scared", duration)
        self.inflictor = inflictor
        self.old_flee_tendency = ()
        self.positive = False

    def apply_effect(self, target):
        logger.debug("Applying fear effect to %s", target)
        if target.parent.has_trait("monster"):
            self.old_flee_tendency = target.parent.brain.get_tendency("flee")
            target.parent.brain.change_tendency("flee", (1000, 0))
            target.parent.flee = True
            logger.debug("The %s is inflicted with fear", target)

    def remove(self, target):
        if target.parent.has_trait("monster"):
            target.parent.brain.change_tendency("flee", self.old_flee_tendency)
            target.parent.flee = False

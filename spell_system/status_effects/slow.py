"""Slow status effect - increases action costs."""

import copy
from logging_config import get_logger
from .base import StatusEffect

logger = get_logger(__name__)


class Slow(StatusEffect):
    def __init__(self, inflictor, duration=5, cumulative=False):
        super().__init__(805, "Slow", "feels slow", duration, cumulative=cumulative)
        self.action_cost_change = {}

    def apply_effect(self, target):
        logger.debug("Applying Slow effect to target")
        self.action_cost_change = copy.deepcopy(target.character.get_all_action_costs())
        for action in self.action_cost_change:
            target.character.change_action_cost(action, self.action_cost_change[action])
            logger.debug("Action cost for %s increased by %s", action, self.action_cost_change[action])

    def remove(self, target):
        logger.debug("Removing Slow effect from target")
        for action in self.action_cost_change:
            target.character.change_action_cost(action, -self.action_cost_change[action])
            logger.debug("Action cost for %s decreased by %s", action, self.action_cost_change[action])

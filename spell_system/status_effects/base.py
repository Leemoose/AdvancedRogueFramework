"""
Base StatusEffect class for all status effects.
"""

from logging_config import get_logger
from objects import Objects
from src.core.constants import INFINITE_DURATION

logger = get_logger(__name__)


class StatusEffect(Objects):
    """Base class for all status effects."""

    def __init__(self, id_tag, name, message, duration, cumulative=False):
        self.id_tag = id_tag
        self.name = name
        self.duration = duration
        self.active = True
        self.message = message
        self.positive = False
        self.traits = {"status_effect": True}
        self.cumulative = cumulative

    def get_duration(self):
        return self.duration

    def is_cumulative(self):
        return self.cumulative

    def apply_effect(self, target):
        """Override in subclass to apply the effect."""
        pass

    def description(self):
        if self.duration == INFINITE_DURATION:
            return self.name + " (permanent)"
        return self.name + " (" + str(self.duration) + ")"

    def tick(self, target):
        """Called each turn. Override for DoT effects."""
        if self.duration == INFINITE_DURATION:
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def remove(self, target):
        """Override in subclass to clean up when effect ends."""
        pass

    def change_duration(self, change):
        self.duration += change

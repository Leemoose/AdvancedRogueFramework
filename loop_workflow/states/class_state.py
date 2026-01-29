"""
Class selection state.
"""

from logging_config import get_logger
from ..game_states import GameState
from ..looptype import LoopType
from display_generation import create_class_screen

logger = get_logger(__name__)


class ClassState(GameState):
    """
    Class selection screen.

    Allows the player to choose their character class.
    """

    loop_type = LoopType.classes

    def create_display(self, display):
        create_class_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        # Currently no input handling defined for classes screen
        # This is a placeholder for future implementation
        if key == "esc":
            self._change_state(LoopType.action)
        return True

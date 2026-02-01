"""
Automated states: resting, auto-pathing.

These states handle continuous automated actions where the game
runs without player input until interrupted or completed.
"""

from logging_config import get_logger
from ..game_states import GameState
from src.core.enums import LoopType

logger = get_logger(__name__)


class RestingState(GameState):
    """
    Resting state where the player heals over time.

    Any input interrupts the rest. The game continues processing
    time passage while resting.
    """

    loop_type = LoopType.resting

    def create_display(self, display):
        # Uses the same display as action state
        from display_generation import create_display
        create_display(display, self.loop)

    def update_display(self, display):
        # Same rendering as action state
        from navigation_utility import shadowcasting
        self.loop.clean_up()
        shadowcasting.compute_fov(self.loop)
        display.update_display(self.loop)

    def handle_input(self, key):
        """Any input interrupts rest."""
        self.loop.add_message("Input detected. Ending rest early.")
        self._change_state(LoopType.action)
        return True

    def tick(self):
        """Process resting each frame."""
        self.loop.player.character.rest(self.loop, LoopType.action)


class PathingState(GameState):
    """
    Auto-pathing state for exploration and traveling to destinations.

    The player automatically moves along a calculated path. Any input
    interrupts the pathing.
    """

    loop_type = LoopType.pathing

    def create_display(self, display):
        # Uses the same display as action state
        from display_generation import create_display
        create_display(display, self.loop)

    def update_display(self, display):
        # Same rendering as action state
        from navigation_utility import shadowcasting
        self.loop.clean_up()
        shadowcasting.compute_fov(self.loop)
        display.update_display(self.loop)

    def handle_input(self, key):
        """Any input interrupts auto-pathing."""
        self.loop.add_message("Input detected. Ending exploration early.")
        self.loop.player.path = []
        self._change_state(LoopType.action)
        return True

    def tick(self):
        """Process one step of auto-pathing each frame."""
        self.loop.player.autopath(self.loop)
        self.loop.pathing_count += 1
        self.loop.time_passes(100)

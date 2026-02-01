"""
Key binding state for rebinding controls.
"""

from logging_config import get_logger
from ..game_states import GameState
from src.core.enums import LoopType
from display_generation import create_binding_screen

logger = get_logger(__name__)


class BindingState(GameState):
    """
    Key binding configuration screen.

    Two-phase process:
    1. Select the source key to rebind
    2. Select the target key(s) to map to
    """

    loop_type = LoopType.binding

    def create_display(self, display):
        create_binding_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self._change_state(LoopType.action)
            self.loop.clear_message()
            return True

        bindings = self.loop.keyboard.key_bindings

        if not bindings.accepting_binding:
            self._handle_source_key_selection(key, bindings)
        else:
            self._handle_target_key_selection(key, bindings)

        return True

    def _handle_source_key_selection(self, key, bindings):
        """Phase 1: Select the source key to rebind."""
        if key == "return":
            bindings.accepting_binding = True
            self.loop.clear_message()
            self.loop.add_message(
                "Please enter the keys you want to map to (click return when done): "
            )
        else:
            bindings.temp_binding = key
            self.loop.clear_message()
            self.loop.add_message(f"The key you have chosen is: {key}")

    def _handle_target_key_selection(self, key, bindings):
        """Phase 2: Select the target key(s) to map to."""
        if key == "return":
            bindings.save_key_binding()
            self._change_state(LoopType.action)
            self.loop.clear_message()
        else:
            bindings.temp_binding_map.append(key)
            self.loop.clear_message()
            keys_str = " ".join(bindings.temp_binding_map)
            self.loop.add_message(f"The keys you have chosen are: {keys_str}")

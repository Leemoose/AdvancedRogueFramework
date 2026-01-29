"""
Menu states: main menu, pause, help, story.

These states handle navigation menus and information screens.
"""

from logging_config import get_logger
from ..game_states import GameState
from ..looptype import LoopType
from ..input_actions import get_main_screen_action, get_paused_action
from display_generation import (
    create_main_screen,
    create_pause_screen,
    create_help_screen,
    create_story_screen,
)

logger = get_logger(__name__)


class MainMenuState(GameState):
    """
    Main menu state shown at game start.

    Options: New Game, Load Game, Help, Story, Quit
    """

    loop_type = LoopType.main

    def create_display(self, display):
        create_main_screen(display, self.loop)

    def update_display(self, display):
        display.update_main(self.loop)

    def handle_input(self, key):
        if key == "esc":
            return False  # Quit game

        action = get_main_screen_action(key)
        if action == "load":
            self.loop.load_game()
        elif action == "help":
            self._change_state(LoopType.help)
        elif action == "story":
            self._change_state(LoopType.story)
        else:
            self._change_state(LoopType.action)

        return True


class PausedState(GameState):
    """
    Pause menu state.

    Options: Resume, Save, Key Bindings, Main Menu, Quit
    """

    loop_type = LoopType.paused

    def create_display(self, display):
        create_pause_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen_without_fill(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self._change_state(LoopType.action)
            return True

        action = get_paused_action(key)
        if action == "main_menu":
            self._return_to_main_menu()
        elif action == "save":
            self._save_game()
        elif action == "quit":
            return False
        elif action == "binding":
            self._change_state(LoopType.binding)
            self.loop.add_message(
                "Please enter the key you want to map from (click return when done):"
            )

        return True

    def _return_to_main_menu(self):
        """Return to main menu, clearing game data."""
        self._change_state(LoopType.main)
        self.loop.clear_data()
        self.loop.init_game()

    def _save_game(self):
        """Save the current game state."""
        self.loop.memory.update_memory(
            self.loop.get_depth(),
            self.loop.get_branch()
        )
        self.loop.memory.save_objects()


class HelpState(GameState):
    """
    Help screen showing game controls and information.
    """

    loop_type = LoopType.help

    def create_display(self, display):
        create_help_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self._change_state(LoopType.main)
        return True


class StoryState(GameState):
    """
    Story/lore screen showing game backstory.
    """

    loop_type = LoopType.story

    def create_display(self, display):
        create_story_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self._change_state(LoopType.main)
        return True

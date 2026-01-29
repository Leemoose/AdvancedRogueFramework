"""
Modal states: death, victory, quest, trade, level up.

These states handle overlay screens and dialogs.
"""

from logging_config import get_logger
from ..game_states import GameState
from ..looptype import LoopType
from ..input_actions import key_to_index, is_quest_number_key
from display_generation import (
    create_death_screen,
    create_victory_screen,
    create_quest_screen,
    create_trade_screen,
    create_level_up,
    update_level_up,
)

logger = get_logger(__name__)


class DeathState(GameState):
    """
    Death screen shown when the player dies.

    Press Escape to return to main menu.
    """

    loop_type = LoopType.death

    def create_display(self, display):
        create_death_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self.loop.clear_data()
            self.loop.init_game()
        return True


class VictoryState(GameState):
    """
    Victory screen shown when the player wins.

    Any key returns to main menu.
    """

    loop_type = LoopType.victory

    def create_display(self, display):
        create_victory_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        self._change_state(LoopType.main)
        self.loop.clear_data()
        self.loop.init_game()
        return True


class QuestState(GameState):
    """
    Quest log screen showing active quests.

    Number keys select different quests to view details.
    """

    loop_type = LoopType.quest

    def create_display(self, display):
        create_quest_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen_without_fill(self.loop)

    def handle_input(self, key):
        logger.debug("Key that you are inputting for quest is: %s", key)

        if key == "esc":
            self._change_state(LoopType.action)
            return True

        if is_quest_number_key(key):
            self.loop.display.quest_number = int(key)
            logger.debug("The new quest number is %s", int(key))
            self._change_state(LoopType.quest)

        return True


class TradeState(GameState):
    """
    Trading/dialog screen for NPC interaction.

    Handles both conversation and item trading.
    """

    loop_type = LoopType.trade

    def create_display(self, display):
        create_trade_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen_without_fill(self.loop)

    def handle_input(self, key):
        if key == "esc":
            self._exit_trade()
            return True

        # Advance dialogue with no options
        if key == "return" and self.loop.dialogue_options == 0:
            self.loop.next_dialogue = True
            return True

        # Select a dialogue option
        if self.loop.dialogue_options > 0 and key in "123456789":
            self._select_dialogue_option(key)
            return True

        # Trade mode: select items with letter keys
        if self.loop.npc_focus.purpose == "trade":
            self._handle_trade_selection(key)
            return True

        # Continue talking if no options
        if self.loop.npc_focus.talking and self.loop.dialogue_options == 0:
            self.loop.next_dialogue = True

        return True

    def _exit_trade(self):
        """Exit trading/dialog and return to action."""
        self._change_state(LoopType.action)
        self.loop.next_dialogue = False
        self.loop.dialogue_options = 0
        self.loop.player_choice = -1

    def _select_dialogue_option(self, key):
        """Select a numbered dialogue option."""
        if int(key) <= self.loop.dialogue_options:
            self.loop.npc_focus.change_purpose(int(key), self.loop)
            self.loop.player_choice = int(key)
            self.loop.next_dialogue = False

    def _handle_trade_selection(self, key):
        """Handle selecting an item to buy in trade mode."""
        index = key_to_index(key)
        if index is not None and index < len(self.loop.npc_focus.items):
            self.loop.npc_focus.take_gold(index, self.loop)


class LevelUpState(GameState):
    """
    Level up screen for allocating stat points.

    Navigate with arrow keys, confirm with Enter.
    """

    loop_type = LoopType.level_up

    def create_display(self, display):
        create_level_up(display, self.loop)

    def update_display(self, display):
        update_level_up(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._cancel_level_up(player)
            return True

        if key == "return":
            self._confirm_level_up(player)
            return True

        # Navigation within stat selection
        self._navigate_stats(key, player)
        return True

    def _cancel_level_up(self, player):
        """Cancel level up without applying changes."""
        self._change_state(LoopType.action)
        self.loop.current_stat = 0
        player.stat_decisions = [0, 0, 0, 0]

    def _confirm_level_up(self, player):
        """Apply level up choices."""
        player.apply_level_up()
        self.loop.current_stat = 0
        self._change_state(LoopType.action)

    def _navigate_stats(self, key, player):
        """Handle arrow key navigation in stat selection."""
        if key == "up" and self.loop.current_stat > 0:
            self.loop.current_stat -= 1
        elif key == "down" and self.loop.current_stat < 3:
            self.loop.current_stat += 1
        elif key == "left":
            player.modify_stat_decisions(self.loop.current_stat, increase=False)
        elif key == "right":
            player.modify_stat_decisions(self.loop.current_stat, increase=True)

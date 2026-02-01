"""
Spell states: spell list, individual spell, quickcast assignment.

These states handle the magic system UI.
"""

from logging_config import get_logger
from ..game_states import GameState
from src.core.enums import LoopType
from ..input_actions import key_to_index, is_quick_cast_key, get_skill_index
from display_generation import (
    create_spellcasting,
    create_spell_window,
    create_quickcast_select,
    update_spell_window,
    update_quickcast_select,
)

logger = get_logger(__name__)


class SpellListState(GameState):
    """
    Spell list screen showing all known spells.

    The player can select a spell to view details or cast.
    """

    loop_type = LoopType.spell

    def create_display(self, display):
        create_spellcasting(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._change_state(LoopType.action)
            self.loop.current_spell = None
            return True

        index = key_to_index(key)
        if index is not None and 0 <= index < len(player.mage.known_spells):
            self.loop.current_spell = index
            self._change_state(LoopType.spell_individual)

        return True


class SpellIndividualState(GameState):
    """
    Individual spell detail screen.

    Shows spell details and allows casting or assigning to quickcast.
    """

    loop_type = LoopType.spell_individual

    def create_display(self, display):
        create_spell_window(display, self.loop)

    def update_display(self, display):
        update_spell_window(self.loop)

    def handle_input(self, key):
        player = self.loop.player
        skill_num = self.loop.current_spell

        if key == "esc":
            self._change_state(LoopType.spell)
            self.loop.current_spell = None
            return True

        if key == "q":
            self._change_state(LoopType.quickcast)
            return True

        if key == "c":
            self._cast_spell(player, skill_num)

        return True

    def _cast_spell(self, player, skill_num):
        """Attempt to cast the spell, entering targeting if needed."""
        spell = player.mage.known_spells[skill_num]

        if not spell.targetted:
            # Non-targeted spell: cast immediately if possible
            if spell.castable(player):
                logger.debug("Casted a spell.")
                player.cast_spell(skill_num, player, self.loop)
            else:
                self.loop.add_message(f"You can't cast {spell.name} right now.")
            self.loop.current_spell = None
        else:
            # Targeted spell: enter targeting mode
            self.loop.start_targetting(start_on_player=(not spell.targets_monster))
            self.loop.targets.store_skill(skill_num, spell, player.character)
            self.loop.current_spell = None


class QuickcastState(GameState):
    """
    Quickcast assignment screen.

    Allows assigning a spell to a number key for quick casting.
    """

    loop_type = LoopType.quickcast

    def create_display(self, display):
        create_quickcast_select(display, self.loop)

    def update_display(self, display):
        update_quickcast_select(self.loop)

    def handle_input(self, key):
        player = self.loop.player
        spell = player.mage.known_spells[self.loop.current_spell]

        if key == "esc":
            self._change_state(LoopType.spell_individual)
            return True

        if key == "p":
            self._change_state(LoopType.spell)
            return True

        if is_quick_cast_key(key):
            skill_num = get_skill_index(key)
            if skill_num < len(player.mage.quick_cast_spells):
                player.mage.set_quick_cast(spell, skill_num)
                self._change_state(LoopType.action)

        return True

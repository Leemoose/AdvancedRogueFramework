"""
Crafting states: crafting screen for combining ingredients into potions.

Players select up to 3 ingredients, then mix them to create a potion.
"""

import copy

from logging_config import get_logger
from ..game_states import GameState
from src.core.enums import LoopType
from ..input_actions import key_to_index
from display_generation import create_crafting, update_crafting
from potion_system import craft_potions

logger = get_logger(__name__)


class CraftingState(GameState):
    """
    Crafting screen for combining 3 ingredients into a potion.

    Controls:
        - A-Z: Select ingredient from list (fills next empty slot)
        - C: Cancel (return all selected ingredients to inventory)
        - M / Return: Mix ingredients (requires 3 slots filled)
        - Esc: Exit crafting (returns any selected ingredients)
    """

    loop_type = LoopType.crafting

    def create_display(self, display):
        create_crafting(display, self.loop)

    def update_display(self, display):
        update_crafting(display, self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._return_ingredients(player)
            self._exit_crafting(player)
            return True

        # Cancel: return all ingredients to inventory, stay on screen
        if key == "c":
            if len(self.loop.crafting_list) > 0:
                self._return_ingredients(player)
                self._refresh()
            return True

        # Mix: craft potion if 3 ingredients selected
        if key == "m" or key == "return":
            if len(self.loop.crafting_list) > 0:
                potion = craft_potions.craft_potion(self.loop.crafting_list)
                player.inventory.get_item(potion)
                self.loop.crafting_list = []
                self._exit_crafting(player)
            return True

        # Letter keys select ingredients into next empty slot
        index = key_to_index(key)
        if index is not None:
            items = player.inventory.get_limit_inventory(limit="ingredient")
            if index < len(items) and len(self.loop.crafting_list) < 3:
                item = items[index]
                # Copy one unit off the stack for the crafting slot
                single = copy.copy(item)
                single.stacks = 1
                self.loop.crafting_list.append(single)
                # Decrement the stack in inventory (remove if empty)
                item.stacks -= 1
                if item.stacks <= 0:
                    player.inventory.remove_item(item)
                self._refresh()
            return True

        return True

    def _return_ingredients(self, player):
        """Return all selected ingredients back to the player's inventory."""
        for item in self.loop.crafting_list:
            player.inventory.get_item(item)
        self.loop.crafting_list = []

    def _refresh(self):
        """Re-render the crafting screen to reflect updated state."""
        self._change_state(LoopType.crafting)

    def _exit_crafting(self, player):
        """Handle exiting the crafting screen."""
        self._change_state(LoopType.action)
        player.inventory.change_limit_inventory("item")
        self.loop.crafting_list = []

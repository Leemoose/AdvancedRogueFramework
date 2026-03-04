"""
Inventory states: inventory, equipment, item details, enchant.

These states handle item management, equipment, and item interactions.
"""

from logging_config import get_logger
from ..game_states import GameState
from src.core.enums import LoopType
from ..input_actions import (
    get_equipment_slot,
    get_inventory_filter,
    get_item_action,
    key_to_index,
)
from display_generation import create_inventory, create_equipment, create_crafting, update_crafting
from potion_system import craft_potions

logger = get_logger(__name__)


class CraftingState(GameState):
    """
    Inventory screen showing all items.

    The player can filter by item type and select items to interact with.
    """

    loop_type = LoopType.crafting

    def create_display(self, display):
        create_crafting(display, self.loop)

    def update_display(self, display):
        update_crafting(display, self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._exit_inventory(player)
            return True

        # Letter keys select items
        index = key_to_index(key)
        if index is not None:
            # import ipdb; ipdb.set_trace()
            items = player.inventory.get_limit_inventory(limit="ingredient")
            if index < len(items):
                if len(self.loop.crafting_list) < 3:
                    print("Crafting: " + str(items[index]));
                    self.loop.crafting_list.append(items[index])
                    player.inventory.remove_item(items[index])
                    return True

        if key == "return":
            print("Crafting!!")
            potion = craft_potions.craft_potion(self.loop.crafting_list)
            player.inventory.get_item(potion)
            self._exit_inventory(player)
            return True


        return True

    def _exit_inventory(self, player):
        """Handle exiting the inventory screen."""
        self._change_state(LoopType.action)
        player.inventory.change_limit_inventory("item")
        self.loop.crafting_list = []


# class ItemScreenState(GameState):
#     """
#     Item detail screen for interacting with a specific item.

#     Options: Drop, Equip/Unequip, Quaff, Read, Activate
#     """

#     loop_type = LoopType.items

#     def create_display(self, display):
#         display.update_entity(self.loop, item_screen=True, create=True)

#     def update_display(self, display):
#         display.update_entity(self.loop)

#     def handle_input(self, key):
#         player = self.loop.player
#         item = self.loop.targets.get_target()
#         item_map = self.loop.generator.item_map

#         if key == "esc":
#             self._exit_item_screen(item)
#             return True

#         action = get_item_action(key)
#         self._perform_item_action(action, player, item, item_map)
#         # Refresh the current screen
#      #       self._change_state(LoopType.items)
#         return True

#     def _perform_item_action(self, action, player, item, item_map):
#         """Execute the item action based on key press."""
#         if action == "drop":
#             if player.do_drop(item, item_map):
#                 self._change_state(LoopType.inventory)
#         elif action == "equip":
#             player.do_equip(item)
#         elif action == "unequip":
#             player.do_unequip(item)
#         elif action == "quaff":
#             if player.character.quaff(item, None, item_map):
#                 self._change_state(LoopType.inventory)
#         elif action == "read":
#             player.character.read(item, self.loop, None, item_map)
#         elif action == "activate":
#             if player.character.activate(item, self.loop):
#                 self._change_state(LoopType.inventory)
#         elif action == "apply":
#             if item.has_trait("potion"):
#                 self._change_state(LoopType.apply_potion)
#         elif action == "throw":
#             self.loop.targets.set_target_range(player.get_location(), item.range)
#             self.loop.targets.set_queued_action(player.do_throw)
#             player.inventory.hotkey_item = item
#             self._change_state(LoopType.action)
#             self.loop.start_targetting()


#     def _exit_item_screen(self, item):
#         """Handle exiting the item detail screen."""
#         player = self.loop.player
#         if player.inventory.limit_inventory == "item":
#             self._change_state(LoopType.inventory)
#         elif item.equipable and item.equipped:
#             self._change_state(LoopType.equipment)
#         else:
#             self._change_state(LoopType.inventory)

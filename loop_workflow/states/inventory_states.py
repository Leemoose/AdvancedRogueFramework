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
from display_generation import create_inventory, create_equipment

logger = get_logger(__name__)


class InventoryState(GameState):
    """
    Inventory screen showing all items.

    The player can filter by item type and select items to interact with.
    """

    loop_type = LoopType.inventory

    def create_display(self, display):
        create_inventory(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._exit_inventory(player)
            return True

        # Number keys filter inventory by type
        inventory_filter = get_inventory_filter(key)
        if inventory_filter:
            player.inventory.change_active_inventory("main")
            player.inventory.change_limit_inventory(inventory_filter)
            self._change_state(LoopType.inventory)
            return True

        # Key "6" switches to orb inventory
        if key == "6":
            player.inventory.change_active_inventory("orb")
            self._change_state(LoopType.inventory)
            return True

        # Letter keys select items
        index = key_to_index(key)
        if index is not None:
            items = player.inventory.get_limit_inventory()
            if index < len(items):
                self.loop.targets.set_entity_target(items[index])
                self._change_state(LoopType.items)

        return True

    def _exit_inventory(self, player):
        """Handle exiting the inventory screen."""
        if player.inventory.limit_inventory == "item":
            self._change_state(LoopType.action)
        else:
            self._change_state(LoopType.equipment)
        player.inventory.change_limit_inventory("item")


class EquipmentState(GameState):
    """
    Equipment screen showing equipped items by slot.

    The player can select slots to view and change equipment.
    """

    loop_type = LoopType.equipment

    def create_display(self, display):
        create_equipment(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            player.inventory.change_limit_inventory("item")
            self._change_state(LoopType.action)
            return True

        slot = get_equipment_slot(key)
        if slot:
            player.inventory.change_limit_inventory(slot)
            self._change_state(LoopType.inventory)

        return True


class ItemScreenState(GameState):
    """
    Item detail screen for interacting with a specific item.

    Options: Drop, Equip/Unequip, Quaff, Read, Activate
    """

    loop_type = LoopType.items

    def create_display(self, display):
        display.update_entity(self.loop, item_screen=True, create=True)

    def update_display(self, display):
        display.update_entity(self.loop)

    def handle_input(self, key):
        player = self.loop.player
        item = self.loop.targets.get_target()
        item_map = self.loop.generator.item_map

        if key == "esc":
            self._exit_item_screen(item)
            return True

        action = get_item_action(key)
        self._perform_item_action(action, player, item, item_map)
        # Refresh the current screen
     #       self._change_state(LoopType.items)
        return True

    def _perform_item_action(self, action, player, item, item_map):
        """Execute the item action based on key press."""
        if action == "drop":
            if player.do_drop(item, item_map):
                self._change_state(LoopType.inventory)
        elif action == "equip":
            player.do_equip(item)
        elif action == "unequip":
            player.do_unequip(item)
        elif action == "quaff":
            if player.character.quaff(item, None, item_map):
                self._change_state(LoopType.inventory)
        elif action == "read":
            player.character.read(item, self.loop, None, item_map)
        elif action == "activate":
            if player.character.activate(item, self.loop):
                self._change_state(LoopType.inventory)
        elif action == "apply":
            if item.has_trait("potion"):
                self._change_state(LoopType.apply_potion)
        elif action == "throw":
            self.loop.targets.set_target_range(player.get_location(), item.range)
            self.loop.targets.set_queued_action(player.do_throw)
            player.inventory.hotkey_item = item
            self._change_state(LoopType.action)
            self.loop.start_targetting()


    def _exit_item_screen(self, item):
        """Handle exiting the item detail screen."""
        player = self.loop.player
        if player.inventory.limit_inventory == "item":
            self._change_state(LoopType.inventory)
        elif item.equipable and item.equipped:
            self._change_state(LoopType.equipment)
        else:
            self._change_state(LoopType.inventory)


class EnchantState(GameState):
    """
    Enchantment screen for upgrading items with scrolls.

    Shows enchantable items and allows selecting one to enchant.
    """

    loop_type = LoopType.enchant

    def create_display(self, display):
        create_inventory(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._cancel_enchant(player)
            return True

        enchantable = player.inventory.get_enchantable()
        index = key_to_index(key)
        if index is not None:
            inventory = player.get_inventory()
            if index < len(inventory) and inventory[index] in enchantable:
                self._enchant_item(player, inventory[index])

        return True

    def _cancel_enchant(self, player):
        """Cancel enchantment and return to action."""
        self._change_state(LoopType.action)
        player.inventory.change_limit_inventory("item")
        player.inventory.ready_scroll = None

    def _enchant_item(self, player, item):
        """Apply enchantment to the selected item."""
        player.inventory.ready_scroll.consume_scroll(player)
        item.level_up()
        self._change_state(LoopType.action)
        player.inventory.change_limit_inventory("item")
        self.loop.update_screen = True


class ApplyPotionState(GameState):
    """
    Selection screen for applying a potion to equipped gear.

    Shows only currently equipped items and allows selecting one
    to apply the stored potion to.
    """

    loop_type = LoopType.apply_potion

    def create_display(self, display):
        from display_generation import create_apply_potion_screen
        create_apply_potion_screen(display, self.loop)

    def update_display(self, display):
        display.update_screen(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        if key == "esc":
            self._change_state(LoopType.inventory)
            return True

        equipped = self._get_equipped_items(player)
        index = key_to_index(key)
        if index is not None and index < len(equipped):
            self._apply_potion(player, equipped[index])

        return True

    def _get_equipped_items(self, player):
        """Return flat list of all currently equipped items."""
        equipped = []
        for slot_items in player.body.equipment_slots.values():
            for item in slot_items:
                if item is not None:
                    equipped.append(item)
        return equipped

    def _apply_potion(self, player, equipment):
        """Apply the stored potion to the selected equipment."""
        potion = self.loop.targets.get_target()
        potion.apply_to_equipment(equipment, self.loop)
        potion.stacks -= 1
        if potion.stacks <= 0:
            potion.destroy = True
            player.inventory.remove_item(potion)
        self._change_state(LoopType.inventory)
        self.loop.update_screen = True

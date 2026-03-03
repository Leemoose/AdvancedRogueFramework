import pygame, pygame_gui
from .ui_constants import UILayout
from .ui_utils import setup_panel_screen


def create_crafting(display, loop):
    player = loop.player

    # Use shared setup helper (eliminates ~15 lines of duplicate code)
    panel_layout = setup_panel_screen(display, "Inventory")
    sidebar_layout = UILayout.get_inventory_sidebar_layout(display.screen_width, display.screen_height, num_buttons=5)

    # Inventory item buttons
    for i, item in enumerate(player.inventory.get_limit_inventory(limit="ingredient")):
        item_name = item.name
        if item.stackable:
            item_name = item.name + " (x" + str(item.stacks) + ")"
        if item.can_be_levelled:
            item_level = item.level
            if item_level > 1:
                item_name = item_name + " (+" + str(item_level - 1) + ")"
        if item.equipped:
            item_name = item_name + " (equipped)"
        btn_x, btn_y = UILayout.get_panel_button_position(panel_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (panel_layout['button_width'], panel_layout['button_height'])),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    # Sidebar filter buttons (left side)
    sidebar_buttons = [
        ("1. Ingredient 1", "1"),
        ("2. Ingredient 2", "2"),
        ("3. Ingredient 3", "3"),
        ("4. Mix!", "m"),
    ]

    for i, (text, action) in enumerate(sidebar_buttons):
        btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y, sidebar_layout['button_width'], sidebar_layout['button_height'])),
            text=text,
            manager=display.uiManager,
            starting_height=1)
        button.action = action

    display.uiManager.draw_ui(display.win)

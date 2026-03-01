import pygame, pygame_gui
from .ui_constants import UILayout
from .ui_utils import setup_panel_screen


def create_apply_potion_screen(display, loop):
    player = loop.player

    panel_layout = setup_panel_screen(display, "Apply Potion to Equipment")

    # Build flat list of equipped items
    equipped = []
    for slot_items in player.body.equipment_slots.values():
        for item in slot_items:
            if item is not None:
                equipped.append(item)

    for i, item in enumerate(equipped):
        item_name = item.name
        if item.can_be_levelled:
            item_level = item.level
            if item_level > 1:
                item_name = item_name + " (+" + str(item_level - 1) + ")"
        btn_x, btn_y = UILayout.get_panel_button_position(panel_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (panel_layout['button_width'], panel_layout['button_height'])),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    display.uiManager.draw_ui(display.win)

import pygame, pygame_gui
from .ui_constants import UILayout
from .ui_utils import setup_panel_screen, draw_on_button, draw_box_over_button


def create_crafting(display, loop):
    player = loop.player
    crafting_list = loop.crafting_list

    # Use shared setup helper
    panel_layout = setup_panel_screen(display, "Crafting")
    sidebar_layout = UILayout.get_inventory_sidebar_layout(display.screen_width, display.screen_height, num_buttons=6)

    # Inventory item buttons (only ingredients not already selected)
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
        if item.has_trait("ingredient"):
            item_tags = item.GetTagString()
            item_name += item_tags
        btn_x, btn_y = UILayout.get_panel_button_position(panel_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (panel_layout['button_width'], panel_layout['button_height'])),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    # --- Sidebar: 3 ingredient slots + Cancel + Mix + Preview ---
    tileDict = loop.tileDict

    for slot_index in range(3):
        btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, slot_index)
        btn_w = sidebar_layout['button_width']
        btn_h = sidebar_layout['button_height']

        if slot_index < len(crafting_list):
            ingredient = crafting_list[slot_index]
            slot_text = str(slot_index + 1) + ". " + ingredient.name
        else:
            slot_text = str(slot_index + 1) + ". (empty)"

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y, btn_w, btn_h)),
            text=slot_text,
            manager=display.uiManager,
            starting_height=1)
        button.action = ""

        # Draw ingredient image on the slot button if filled
        if slot_index < len(crafting_list):
            ingredient = crafting_list[slot_index]
            if ingredient.render_tag in tileDict.tiles:
                img = pygame.transform.scale(
                    tileDict.tiles[ingredient.render_tag],
                    (int(btn_h * 0.8), int(btn_h * 0.8)))
                draw_on_button(button, img, button_size=(btn_w, btn_h), shrink=False)

    # Cancel button (slot 3)
    btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, 3)
    btn_w = sidebar_layout['button_width']
    btn_h = sidebar_layout['button_height']
    cancel_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x, btn_y, btn_w, btn_h)),
        text="Cancel",
        manager=display.uiManager,
        starting_height=1)
    cancel_button.action = "c"


    # Mix button (slot 4)
    btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, 4)
    mix_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x, btn_y, btn_w, btn_h)),
        text="Mix!",
        manager=display.uiManager,
        starting_height=1)
    mix_button.action = "m"

    # Preview placeholder (slot 5)
    btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, 5)
    preview_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x, btn_y, btn_w, btn_h)),
        text="Preview: ???",
        manager=display.uiManager,
        starting_height=1)
    preview_button.action = ""

    display.uiManager.draw_ui(display.win)

def update_crafting(display, loop):
    # TODO: only update if loop.crafting_list changes
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
        if item.has_trait("ingredient"):
            item_tags = item.GetTagString()
            item_name += item_tags
        btn_x, btn_y = UILayout.get_panel_button_position(panel_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (panel_layout['button_width'], panel_layout['button_height'])),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    # Sidebar filter buttons (left side)
    active_ingredients = loop.crafting_list
    sidebar_buttons = []
    for i in range(len(active_ingredients)):
        sidebar_buttons.append((f"{i + 1}. {active_ingredients[i].name + active_ingredients[i].GetTagString()}", str(i + 1)))
    for i in range(len(active_ingredients), 3):
        sidebar_buttons.append((f"{i+ 1}. Ingredient {i + 1}", str(i + 1)))
    sidebar_buttons.append(("4. Mix! (press enter)", "return"))

    for i, (text, action) in enumerate(sidebar_buttons):
        btn_x, btn_y = UILayout.get_sidebar_button_position(sidebar_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y, sidebar_layout['button_width'], sidebar_layout['button_height'])),
            text=text,
            manager=display.uiManager,
            starting_height=1)
        button.action = action

    display.uiManager.draw_ui(display.win)

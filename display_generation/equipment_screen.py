import pygame_gui, pygame
from .ui_constants import UILayout
from .ui_utils import setup_panel_screen
from src.core.asset_registry import TileID


def create_equipment(display, loop):
    player = loop.player
    tileMap = loop.tileDict

    # Use shared setup helper (eliminates ~15 lines of duplicate code)
    layout = setup_panel_screen(display, "Equipment", layout_func='equipment')

    medium_w = layout['medium_button_width']
    medium_h = layout['medium_button_height']
    small_w = layout['small_button_width']
    small_h = layout['small_button_height']
    first_col_x = layout['first_col_x']
    outer_cols_y = layout['outer_cols_y']
    middle_col_y = layout['middle_col_y']
    margin_h = layout['margin_height']
    margin_w = layout['margin_width']
    small_margin_w = layout['small_margin_width']

    # Shield slot
    shield_equipped = False
    for item in player.body.get_items_in_equipment_slot("hand_slot"):
        if item.equipment_type == "Shield" and item.equipped:
            shield_equipped = True
            break
    two_handed_equipped = False
    for item in player.body.get_items_in_equipment_slot("hand_slot"):
        if item.equipment_type == "Weapon" and item.slots_taken > 1 and item.equipped:
            two_handed_equipped = True
    if shield_equipped:
        pre_text = "change "
        img = pygame.transform.scale(tileMap.tiles[player.body.get_shield().render_tag], (medium_w, medium_h))
    elif two_handed_equipped:
        pre_text = "change "
        img = pygame.transform.scale(tileMap.tiles[player.body.get_weapon().render_tag], (medium_w, medium_h))
    else:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Shield":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_SHIELD_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_SHIELD], (medium_w, medium_h))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_x, outer_cols_y), (medium_w, medium_h)),
        text=pre_text + "shield",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "q", (medium_w, medium_h))
    button.action = 'q'

    # Ring slots
    rings = player.body.equipment_slots["ring_slot"]
    ring_keys = ["r", "z"]

    for i, ring in enumerate(rings):
        if ring is not None:
            img = pygame.transform.scale(
                tileMap.tiles[player.body.get_nth_item_in_equipment_slot("ring_slot", i).render_tag],
                (small_w, small_h))
        else:
            available_slot = False
            for item in player.get_inventory():
                if item.equipment_type == "Ring" and (not item.equipped):
                    available_slot = True
                    break
            if available_slot:
                img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_RING_OPEN], (small_w, small_h))
            else:
                img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_RING], (small_w, small_h))
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (first_col_x + (small_w + small_margin_w) * i, outer_cols_y + (medium_h + margin_h)),
                (small_w, small_h)),
            text="ring " + str(i + 1),
            manager=display.uiManager,
            object_id='#equipment_button')
        display.draw_on_button(button, img, ring_keys[i], (small_w, small_h))
        button.action = ring_keys[i]

    # Amulet slot
    if player.body.get_num_free_equipment_slots("amulet_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Amulet":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_AMULET_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_AMULET], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("amulet_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x, outer_cols_y + 2 * (medium_h + margin_h)),
            (medium_w, medium_h)),
        text=pre_text + "amulet",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "a", (medium_w, medium_h))
    button.action = 'a'

    # Helmet slot
    if player.body.get_num_free_equipment_slots("helmet_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Helmet":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_HELMET_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_HELMET], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("helmet_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + medium_w + margin_w, middle_col_y),
            (medium_w, medium_h)),
        text=pre_text + "helmet",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "w", (medium_w, medium_h))
    button.action = 'w'

    # Body armor slot
    if player.body.get_num_free_equipment_slots("body_armor_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Body Armor":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_ARMOR_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_ARMOR], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("body_armor_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + medium_w + margin_w, middle_col_y + (medium_h + margin_h)),
            (medium_w, medium_h)),
        text=pre_text + "armor",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "s", (medium_w, medium_h))
    button.action = 's'

    # Boots slot
    if player.body.get_num_free_equipment_slots("boots_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Boots":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_BOOTS_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_BOOTS], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("boots_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + medium_w + margin_w, middle_col_y + 2 * (medium_h + margin_h)),
            (medium_w, medium_h)),
        text=pre_text + "boots",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "x", (medium_w, medium_h))
    button.action = 'x'

    # Weapon slot
    weapon_equipped = False
    for item in player.body.get_items_in_equipment_slot("hand_slot"):
        if item.equipment_type == "Weapon" and item.equipped:
            weapon_equipped = True
            break
    if not weapon_equipped:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Weapon":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_WEAPON_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_WEAPON], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(tileMap.tiles[player.body.get_weapon().render_tag], (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + 2 * (medium_w + margin_w), outer_cols_y),
            (medium_w, medium_h)),
        text=pre_text + "weapon",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "d", (medium_w, medium_h), shrink=True)
    button.action = 'd'

    # Gloves slot
    if player.body.get_num_free_equipment_slots("gloves_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Gloves":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_GLOVES_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_GLOVES], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("gloves_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + 2 * (medium_w + margin_w), outer_cols_y + (medium_h + margin_h)),
            (medium_w, medium_h)),
        text=pre_text + "gloves",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "c", (medium_w, medium_h))
    button.action = 'c'

    # Pants slot
    if player.body.get_num_free_equipment_slots("pants_slot") != 0:
        available_slot = False
        for item in player.get_inventory():
            if item.equipment_type == "Pants":
                available_slot = True
                break
        if available_slot:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_PANTS_OPEN], (medium_w, medium_h))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[TileID.EMPTY_PANTS], (medium_w, medium_h))
    else:
        pre_text = "change "
        img = pygame.transform.scale(
            tileMap.tiles[player.body.get_nth_item_in_equipment_slot("pants_slot", 0).render_tag],
            (medium_w, medium_h))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_x + 2 * (medium_w + margin_w), outer_cols_y + 2 * (medium_h + margin_h)),
            (medium_w, medium_h)),
        text=pre_text + "pants",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "p", (medium_w, medium_h))
    button.action = 'p'

    # Character stats panel
    display.draw_character_stats(player,
                                 margin_from_left=first_col_x + 3 * (medium_w + margin_w),
                                 margin_from_top=middle_col_y,
                                 width=medium_w * 2,
                                 height=medium_h * 3 + margin_h * 2)
    display.uiManager.draw_ui(display.win)

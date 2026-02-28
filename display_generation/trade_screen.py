import pygame, pygame_gui

from .ui import MessageBox, DialogueInteraction
from .ui_constants import UIColors, UILayout

def create_trade_screen(display, loop):
    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None

    layout = UILayout.get_trade_screen_layout(display.screen_width, display.screen_height)

    num_option_buttons = len(loop.npc_focus.options)
    option_button_height = min((layout['popup_height'] - layout['title_height']) * 2 // 3 // (num_option_buttons + 1), 100)
    option_margin_height = (layout['popup_height'] - layout['title_height']) * 2 // 3 // (num_option_buttons + 1) // (num_option_buttons + 1)

    pygame.draw.rect(display.win, UIColors.SCREEN_OVERLAY_BG,
                     pygame.Rect(layout['popup_x'] - 10, layout['popup_y'] - 10,
                                 layout['popup_width'] + 20, layout['popup_height'] + 20))
    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    display.draw_escape_button(layout['popup_x'], layout['popup_y'],
                               layout['popup_width'], layout['popup_height'])
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['popup_x'], layout['popup_y']),
                                  (layout['popup_width'], layout['title_height'])),
        text=loop.npc_focus.name,
        manager=display.uiManager,
        object_id='#title_label')

    if loop.npc_focus.purpose == "trade":
        for i, weapon in enumerate(loop.npc_focus.items):
            img = pygame.transform.scale(loop.tileDict.tiles[weapon.render_tag],
                                         (layout['button_width'], layout['button_height']))
            btn_x, btn_y = UILayout.get_trade_item_position(layout, i)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((btn_x, btn_y),
                                          (layout['button_width'], layout['button_height'])),
                text=str(weapon.name),
                manager=display.uiManager,
                object_id='#equipment_button')
            display.draw_on_button(button, img, chr(ord("a") + i),
                                   (layout['button_width'], layout['button_height']))
            button.action = chr(ord("a") + i)

    else:
        npc = loop.npc_focus
        npc_tile = loop.tileDict.tile_string(npc.render_tag)
        display.win.blit(pygame.transform.scale(npc_tile, (layout['player_size'], layout['player_size'])),
                         (layout['npc_x'], layout['player_y']))

        dialogue_panel = DialogueInteraction(
            rect=pygame.Rect((layout['dialogue_x'], layout['dialogue_y']),
                             (layout['dialogue_width'], layout['dialogue_height'])),
            manager=display.uiManager,
            loop=loop,
            npc=loop.npc_focus,
            max_messages=4,
            bubble_gap=layout['dialogue_height'] // 20)

        display.uiManager.draw_ui(display.win)

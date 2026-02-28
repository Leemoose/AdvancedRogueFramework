import pygame, pygame_gui
from .action_screen import *
from .ui_constants import UIColors, UILayout

def create_quickcast_select(display, loop):
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]
    tileDict = loop.tileDict
    spell = entity

    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None
    display.win.fill(UIColors.BLACK)

    layout = UILayout.get_entity_popup_layout(display.screen_width, display.screen_height)

    entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                          (layout['image_width'], layout['image_height']))

    pygame.draw.rect(display.win, UIColors.POPUP_BG,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    display.win.blit(entity_image, (layout['image_x'], layout['image_y']))

    display.draw_escape_button(layout['popup_x'], layout['popup_y'],
                               layout['popup_width'], layout['popup_height'])

    entity_name = entity.name
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['message_x'], layout['message_y']),
                                  (layout['message_width'], layout['message_height'])),
        text=entity_name,
        manager=display.uiManager,
        object_id='#title_small')

    entity_text = ""
    entity_text += entity.full_description() + "<br><br>"
    entity_text += f"Select 1-7 to assign {spell.name} a quickcast slot"

    create_skill_bar(display, loop, display_empty=True)

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((layout['text_x'], layout['text_y']),
                                  (layout['text_width'], layout['text_height'])),
        html_text=entity_text,
        manager=display.uiManager)

    display.uiManager.draw_ui(display.win)

def update_quickcast_select(loop):
    display = loop.display
    tileDict = loop.tileDict
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]

    layout = UILayout.get_entity_popup_layout(display.screen_width, display.screen_height)

    display.update_screen(loop)

    entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                          (layout['image_width'], layout['image_height']))

    pygame.draw.rect(display.win, UIColors.POPUP_BG,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    display.win.blit(entity_image, (layout['image_x'], layout['image_y']))

    display.uiManager.draw_ui(display.win)

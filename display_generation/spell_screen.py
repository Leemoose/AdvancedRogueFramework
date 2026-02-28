import pygame, pygame_gui
from .action_screen import *
from .ui_constants import UIColors, UILayout
from .ui_utils import setup_panel_screen


def create_spellcasting(display, loop):
    player = loop.player

    # Use shared setup helper (eliminates ~15 lines of duplicate code)
    panel_layout = setup_panel_screen(display, "Known Spells")

    # Spell buttons
    for i, spell in enumerate(player.mage.known_spells):
        spell_name = spell.name
        btn_x, btn_y = UILayout.get_panel_button_position(panel_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (panel_layout['button_width'], panel_layout['button_height'])),
            text=chr(ord("a") + i) + ". " + spell_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    display.uiManager.draw_ui(display.win)

def create_spell_window(display, loop):
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]
    tileDict = loop.tileDict

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

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['button_x'], layout['button_y']),
                                  (layout['button_width'], layout['button_height'])),
        text="Cast",
        manager=display.uiManager)
    button.action = "c"

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['button_x'] + layout['button_width'] + layout['button_spacing'],
                                   layout['button_y']),
                                  (layout['button_width'], layout['button_height'])),
        text="Set (q)uickcast",
        manager=display.uiManager)
    button.action = "q"

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((layout['text_x'], layout['text_y']),
                                  (layout['text_width'], layout['text_height'])),
        html_text=entity_text,
        manager=display.uiManager)

    display.uiManager.draw_ui(display.win)

def update_spell_window(loop):
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

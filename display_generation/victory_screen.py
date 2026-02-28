import pygame, pygame_gui
from .ui_constants import UIColors, UILayout

def create_victory_screen(display, loop):
    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None
    player = loop.player
    layout = UILayout.get_victory_screen_layout(display.screen_width, display.screen_height)

    pygame.draw.rect(display.win, UIColors.BLACK, pygame.Rect(
        layout['popup_x'] - layout['border_width'] // 2,
        layout['popup_y'] - layout['border_width'] // 2,
        layout['popup_width'] + layout['border_width'],
        layout['popup_height'] + layout['border_width']))
    pygame.draw.rect(display.win, UIColors.POPUP_BG,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['message_x'], layout['message_y']),
                                  (layout['message_width'], layout['message_height'])),
        text="Victory!",
        manager=display.uiManager,
        object_id='#title_label')

    html_text = "You have defeated the dungeon and achieved maximum orb-iness!<br><br>"
    html_text += "You reached level " + str(player.level) + ".<br>"
    html_text += "You killed " + str(player.statistics.total_monsters_killed) + " monsters along the way.<br>"

    pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((layout['text_x'], layout['text_y']),
                                  (layout['text_width'], layout['text_height'])),
        html_text=html_text,
        manager=display.uiManager)
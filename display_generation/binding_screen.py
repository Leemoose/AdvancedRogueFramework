import pygame, pygame_gui
from .ui import MessageBox
from .ui_constants import UIColors, UILayout

def create_binding_screen(display, loop):
    display.uiManager.clear_and_reset()
    layout = UILayout.get_centered_popup_layout(display.screen_width, display.screen_height)

    message_y = layout['content_y'] + layout['content_height'] // 3
    message_height = display.screen_height - message_y - layout['popup_y']

    pygame.draw.rect(display.win, UIColors.SCREEN_OVERLAY_BG,
                     pygame.Rect(layout['popup_x'] - layout['overlay_padding'],
                                 layout['popup_y'] - layout['overlay_padding'],
                                 layout['popup_width'] + layout['overlay_padding'] * 2,
                                 layout['popup_height'] + layout['overlay_padding'] * 2))
    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    display.draw_escape_button(layout['popup_x'], layout['popup_y'],
                               layout['popup_width'], layout['popup_height'])
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['title_x'], layout['title_y']),
                                  (layout['title_width'], layout['title_height'])),
        text="Bindings",
        manager=display.uiManager,
        object_id='#title_label')
    text_box = MessageBox(
        pygame.Rect((layout['popup_x'], message_y),
                    (layout['popup_width'], message_height)),
        manager=display.uiManager,
        loop=loop)

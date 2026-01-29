import pygame, pygame_gui
from .ui_constants import UILayout

def create_pause_screen(display, loop):
    display.uiManager.clear_and_reset()
    layout = UILayout.get_pause_screen_layout(display.screen_width, display.screen_height, num_buttons=5)

    buttons_config = [
        ('Unpause', 'esc'),
        ('Return to (m)enu', 'm'),
        ('(B)indings', 'b'),
        ('(S)ave', 's'),
        ('(Q)uit', 'q'),
    ]

    for i, (text, action) in enumerate(buttons_config):
        btn_x, btn_y = UILayout.get_pause_button_position(layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (layout['button_width'], layout['button_height'])),
            text=text,
            manager=display.uiManager,
            starting_height=1000)
        button.action = action
import pygame, pygame_gui
from .ui_constants import UILayout

def create_main_screen(display, loop):
    layout = UILayout.get_main_screen_layout(display.screen_width, display.screen_height)

    display.uiManager.clear_and_reset()

    imp = pygame.image.load('assets/title_screen.jpg')
    display.win.blit(imp, (0, 0))

    # Create buttons using layout helper
    buttons_config = [
        ('Play', 'return'),
        ('Load', 'l'),
        ('The Story So Far', 's'),
        ('Help', 'h'),
        ('Quit', 'esc')
    ]

    for i, (text, action) in enumerate(buttons_config):
        btn_x, btn_y = UILayout.get_main_screen_button_position(layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y), (layout['button_width'], layout['button_height'])),
            text=text,
            manager=display.uiManager)
        button.action = action

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['title_x'], layout['title_y']), (layout['title_width'], layout['title_height'])),
        text="Orbworld: The Orb of Destiny",
        manager=display.uiManager,
        object_id='#title_label')

import pygame
import pygame_gui
from .ui_constants import UILayout

def create_death_screen(display, loop):
    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None
    layout = UILayout.get_death_screen_layout(display.screen_width, display.screen_height)

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['button_x'], layout['button_y']),
                                  (layout['button_width'], layout['button_height'])),
        text='Return to Main Menu',
        manager=display.uiManager,
        starting_height=10000)
    button.action = "esc"

    text_box = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['button_x'], layout['message_y']),
                                  (layout['button_width'], layout['button_height'])),
        text="You have died.",
        manager=display.uiManager
    )
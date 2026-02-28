import pygame, pygame_gui
from .ui_constants import UILayout

def create_help_screen(display, loop):
    layout = UILayout.get_info_screen_layout(display.screen_width, display.screen_height)

    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['button_x'], layout['button_y']),
                                  (layout['button_width'], layout['button_height'])),
        text='Return to Main Menu',
        manager=display.uiManager)
    button.action = "esc"

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['title_x'], layout['title_y']),
                                  (layout['title_width'], layout['title_height'])),
        text="Action Shortcuts",
        manager=display.uiManager,
        object_id='#title_label')

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((layout['message_x'], layout['message_y']),
                                  (layout['message_width'], layout['message_height'])),
        html_text="Action Screen: <br>" +
                  "Inventory: i || Equipments: e || Potions: q || Scrolls: r <br>" +
                  "Autoexplore: o || Find Stairs: s || Wait: . || Rest: z <br>" +
                  "Examine: x || Save: / || Pause: esc <br>" +
                  "Grab: g || Allocate stats: l <br>" +
                  "Downstairs: > || Upstairs: < <br>" +
                  "Skills: 1-8 <br>" +
                  "Up / Down / Left / Right --> Arrow keys <br>" +
                  "Up - Left / Up - Right / Down - Left / Down - Right --> y / u / n / b <br>"
        ,
        manager=display.uiManager
    )

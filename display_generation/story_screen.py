import pygame, pygame_gui
from .ui_constants import UILayout

def create_story_screen(display, loop):
    layout = UILayout.get_info_screen_layout(display.screen_width, display.screen_height)

    display.uiManager.clear_and_reset()

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['button_x'], layout['button_y']),
                                  (layout['button_width'], layout['button_height'])),
        text='Return to Main Menu',
        manager=display.uiManager)
    button.action = "esc"

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((layout['title_x'], layout['title_y']),
                                  (layout['title_width'], layout['title_height'])),
        text="The Story So Far",
        manager=display.uiManager,
        object_id='#title_label')

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((layout['message_x'], layout['message_y']),
                                  (layout['message_width'], layout['message_height'])),
        html_text=
        "Awakened by recent excavations, a terrible evil has descened up on the land. <br><br>" +
        "The ORB of YENDORB - an ancient, malignant artifact designed to bring orbiness<br>" +
        "into the world. The device has grown a dungeon around itdisplay, and filled it<br>" +
        "with unspeakable horrors to defend it. While it waits, it expands its magical power - <br>" +
        "should it finish charging, all of existence will be made round.<br><br>" +
        "As a Cornerian knight, you cannot let this evil continue! Delve deep into this<br>" +
        "incomprehensible place, where roundess is power. Slay the aberrations that defend it, and<br>" +
        "retrieve the orb before it completes its task. The fate of the world depends on you!<br>"
        ,
        manager=display.uiManager
    )
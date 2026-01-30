import pygame, pygame_gui
from logging_config import get_logger
from .ui_constants import UILayout
from .ui_utils import setup_popup_screen

logger = get_logger(__name__)


def create_quest_screen(display, loop):
    num_options = len(loop.player.quests)

    # Use shared setup helper (eliminates ~20 lines of duplicate code)
    popup_layout = setup_popup_screen(display, "Active Quests")
    option_layout = UILayout.get_option_buttons_layout(popup_layout, num_options)
    message_layout = UILayout.get_popup_message_layout(popup_layout, option_layout)

    text = ""
    if display.quest_number < 1 or display.quest_number > len(loop.player.quests):
        logger.warning("The current quest number does not line up with something that can be displayed")
    else:
        text = loop.player.quests[display.quest_number - 1].get_description(loop)

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_layout['message_x'], message_layout['message_y']),
                                  (message_layout['message_width'], message_layout['message_height'])),
        html_text=text,
        manager=display.uiManager
    )

    options = loop.player.quests
    for i in range(len(options)):
        btn_x, btn_y = UILayout.get_option_button_position(option_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (option_layout['button_width'], option_layout['button_height'])),
            text=chr(ord("1") + i) + ". " + "{}".format(options[i].name),
            manager=display.uiManager)
        button.action = chr(ord("1") + i)

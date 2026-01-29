import pygame, pygame_gui
from .ui_constants import UIColors, UILayout

def create_class_screen(display, loop):
    display.uiManager.clear_and_reset()

    num_options = 3
    popup_layout = UILayout.get_centered_popup_layout(display.screen_width, display.screen_height)
    option_layout = UILayout.get_option_buttons_layout(popup_layout, num_options)
    message_layout = UILayout.get_popup_message_layout(popup_layout, option_layout)

    # Calculate message area with reduced height to leave room for bottom buttons
    message_height = message_layout['message_height'] * 2 // 3

    # Bottom action buttons layout
    num_bottom_buttons = 2
    bottom_button_width = min(popup_layout['popup_width'] // (num_bottom_buttons + 1), 300)
    bottom_button_spacing = popup_layout['popup_width'] // (num_bottom_buttons + 1) // (num_bottom_buttons + 1)
    bottom_button_y = message_layout['message_y'] + message_height
    bottom_button_height = min(popup_layout['popup_y'] + popup_layout['popup_height'] - bottom_button_y, 60)

    pygame.draw.rect(display.win, UIColors.SCREEN_OVERLAY_BG,
                     pygame.Rect(popup_layout['popup_x'] - popup_layout['overlay_padding'],
                                 popup_layout['popup_y'] - popup_layout['overlay_padding'],
                                 popup_layout['popup_width'] + popup_layout['overlay_padding'] * 2,
                                 popup_layout['popup_height'] + popup_layout['overlay_padding'] * 2))
    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(popup_layout['popup_x'], popup_layout['popup_y'],
                                 popup_layout['popup_width'], popup_layout['popup_height']))

    display.draw_escape_button(popup_layout['popup_x'], popup_layout['popup_y'],
                               popup_layout['popup_width'], popup_layout['popup_height'])
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((popup_layout['title_x'], popup_layout['title_y']),
                                  (popup_layout['title_width'], popup_layout['title_height'])),
        text="Classes",
        manager=display.uiManager,
        object_id='#title_label')

    if loop.class_selection is None:
        text = "Choose a class above."
    else:
        chosen_class = loop.class_selection
        text = ""
        text += chosen_class.name + ":\n"
        text += "Description: " + chosen_class.get_description() + "\n"
        text += "Spells: "
        for spell in chosen_class.get_spell_names():
            text += spell + ", "
        text = text[:-2]  # removes last comma
        text += "\n"
        text += "Items: "
        for item in chosen_class.get_items():
            text += item.name + ", "
        text = text[:-2]  # removes last comma
        text += "\n"

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_layout['message_x'], message_layout['message_y']),
                                  (message_layout['message_width'], message_height)),
        html_text=text,
        manager=display.uiManager
    )

    # Class option buttons
    options = loop.get_available_classes()
    for i in range(len(options)):
        btn_x, btn_y = UILayout.get_option_button_position(option_layout, i)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (option_layout['button_width'], option_layout['button_height'])),
            text=chr(ord("1") + i) + ". " + "{}".format(options[i].name),
            manager=display.uiManager)
        button.action = chr(ord("1") + i)

    # Continue button
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (popup_layout['popup_x'] + bottom_button_spacing + bottom_button_width * 0 + bottom_button_spacing * 0,
             bottom_button_y),
            (bottom_button_width, bottom_button_height)),
        text='Continue',
        manager=display.uiManager)
    button.action = "return"

    # Main Menu button
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (popup_layout['popup_x'] + bottom_button_spacing + bottom_button_width * 1 + bottom_button_spacing * 1,
             bottom_button_y),
            (bottom_button_width, bottom_button_height)),
        text='Main Menu',
        manager=display.uiManager)
    button.action = "esc"

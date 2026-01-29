import pygame, pygame_gui
from .ui import StatChangeText, StatDownButton, StatUpButton, LevelUpHeader
from .ui_constants import UIColors, UILayout

def create_level_up(display, loop):
    player = loop.player
    tileDict = loop.tileDict

    layout = UILayout.get_levelup_screen_layout(display.screen_width, display.screen_height)

    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(layout['popup_x'] - layout['border_width'] // 2,
                                 layout['popup_y'] - layout['border_width'] // 2,
                                 layout['popup_width'] + layout['border_width'],
                                 layout['popup_height'] + layout['border_width']))
    pygame.draw.rect(display.win, UIColors.POPUP_BG,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))

    for i in range(4):
        stat_pos = UILayout.get_levelup_stat_position(layout, i)

        stat_change_left = pygame.transform.scale(tileDict.tiles[51],
                                                  (layout['stat_button_width'], layout['stat_button_height']))
        stat_change_left_dark = pygame.transform.scale(tileDict.tiles[-51],
                                                       (layout['stat_button_width'], layout['stat_button_height']))
        stat_change_right = pygame.transform.scale(tileDict.tiles[50],
                                                   (layout['stat_button_width'], layout['stat_button_height']))
        stat_change_right_dark = pygame.transform.scale(tileDict.tiles[-50],
                                                        (layout['stat_button_width'], layout['stat_button_height']))

        button = StatDownButton(
            rect=pygame.Rect((stat_pos['down_button_x'], stat_pos['down_button_y']),
                             (layout['stat_button_width'], layout['stat_button_height'])),
            manager=display.uiManager,
            player=player,
            img1=stat_change_left,
            img2=stat_change_left_dark,
            index=i)
        button.action = "left"
        button.row = i

        StatChangeText(
            rect=pygame.Rect((stat_pos['text_x'], stat_pos['text_y']),
                             (layout['stat_button_width'], layout['stat_button_height'])),
            manager=display.uiManager,
            player=player,
            index=i)

        button_2 = StatUpButton(
            rect=pygame.Rect((stat_pos['up_button_x'], stat_pos['up_button_y']),
                             (layout['stat_button_width'], layout['stat_button_height'])),
            manager=display.uiManager,
            player=player,
            img1=stat_change_right,
            img2=stat_change_right_dark,
            index=i)
        button_2.action = "right"
        button_2.row = i

    display.draw_escape_button(layout['message_x'], layout['message_y'],
                               layout['stat_line_width'] + layout['stat_button_spacing_width'],
                               layout['popup_height'])

    LevelUpHeader(
        rect=pygame.Rect((layout['message_x'], layout['message_y']),
                         (layout['message_width'], layout['message_height'])),
        manager=display.uiManager,
        player=player)

    # Stat labels
    stat_descriptions = [
        "Str (currently " + str(player.character.get_strength()) + ") - increase your damage and wear heavier armor",
        "Dex (currently " + str(player.character.get_dexterity()) + ") - increase your dodge chance and action speed",
        "En (currently " + str(player.character.get_endurance()) + ") - increase your defense and your max health",
        "Int (currently " + str(player.character.get_intelligence()) + ") - increase your max mana and skill damage",
    ]

    for i, description in enumerate(stat_descriptions):
        stat_pos = UILayout.get_levelup_stat_position(layout, i)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((stat_pos['label_x'], stat_pos['label_y']),
                                      (layout['stat_line_width'], layout['stat_line_height'])),
            text=description,
            manager=display.uiManager,
            object_id='#stat_label')

    # Confirmation button
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((layout['confirm_button_x'], layout['confirm_button_y']),
                                  (layout['confirm_button_width'], layout['confirm_button_height'])),
        text="Confirm",
        manager=display.uiManager)
    button.action = "return"
    button.row = None

def update_level_up(loop):
    line_to_outline = loop.current_stat
    display = loop.display
    player = loop.player

    layout = UILayout.get_levelup_screen_layout(display.screen_width, display.screen_height)

    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(layout['popup_x'] - layout['border_width'] // 2,
                                 layout['popup_y'] - layout['border_width'] // 2,
                                 layout['popup_width'] + layout['border_width'],
                                 layout['popup_height'] + layout['border_width']))
    pygame.draw.rect(display.win, UIColors.POPUP_BG,
                     pygame.Rect(layout['popup_x'], layout['popup_y'],
                                 layout['popup_width'], layout['popup_height']))
    pygame.draw.rect(display.win, UIColors.BLACK, pygame.Rect((0, 0), (display.screen_width // 2, 40)))

    for i in range(0, 4):
        stat_pos = UILayout.get_levelup_stat_position(layout, i)
        if i == loop.current_stat:
            color = UIColors.BLACK
        else:
            color = UIColors.POPUP_BG
        pygame.draw.rect(display.win, color,
                         pygame.Rect(layout['stat_outline_x'], stat_pos['outline_y'],
                                     layout['stat_outline_width'], layout['stat_outline_height']))

    display.uiManager.draw_ui(display.win)

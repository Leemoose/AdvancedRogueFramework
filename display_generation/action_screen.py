import pygame_gui, pygame

from .ui import FPSCounter, MessageBox, DepthDisplay, StatBox, SkillButton, HealthBar, ManaBar
from .ui_constants import UILayout

def create_skill_bar(display, loop, display_empty=False):
    player = loop.player
    tileDict = loop.tileDict

    num_skills = len(player.mage.quick_cast_spells) + 1
    layout = UILayout.get_skill_bar_layout(display.screen_width, display.screen_height, num_skills)

    if player.mage.quick_cast_spells.count(None) == len(player.mage.quick_cast_spells):
        display.draw_empty_box(layout['skill_bar_x'], layout['skill_bar_y'],
                               layout['skill_bar_width'], layout['skill_bar_height'])
    else:
        display.draw_empty_box(layout['skill_bar_x'], layout['skill_bar_y'],
                               layout['skill_bar_width'], layout['skill_bar_height'])
        for i, skill in enumerate(player.mage.quick_cast_spells):
            if skill is None:
                if display_empty:
                    img1 = None
                    img2 = None
                else:
                    continue
            else:
                img1 = pygame.transform.scale(tileDict.tiles[skill.render_tag],
                                              (layout['button_width'], layout['button_height']))
                img2 = pygame.transform.scale(tileDict.tiles[-skill.render_tag],
                                              (layout['button_width'], layout['button_height']))
            btn_x, btn_y = UILayout.get_skill_button_position(layout, i)
            button = SkillButton(
                rect=pygame.Rect((btn_x, btn_y),
                                 (layout['button_width'], layout['button_height'])),
                manager=display.uiManager,
                player=player,
                index=i,
                img1=img1,
                img2=img2,
                loop=loop,
                object_id='#skill_button')
            button.action = chr(ord("1") + i)

        # "All Spells" button
        btn_x, btn_y = UILayout.get_skill_button_position(layout, num_skills - 1)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (layout['button_width'], layout['button_height'])),
            text="All S(p)ells",
            manager=display.uiManager,
            starting_height=800)
        button.action = "p"

def create_display(display, loop):
    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None
    fps_counter = FPSCounter(
        pygame.Rect((0, 0), (400, 40)),
        display.uiManager
    )

    player = loop.player

    action_layout = UILayout.get_action_screen_layout(display.screen_width, display.screen_height, display.textSize)

    num_tiles_wide = action_layout['action_width'] // display.textSize
    num_tiles_height = action_layout['action_height'] // display.textSize

    r_x = num_tiles_wide // 2
    r_y = num_tiles_height // 2

    display.x_start = player.x - r_x
    display.x_end = player.x + r_x
    display.y_start = player.y - r_y
    display.y_end = player.y + r_y

    # Writing messages
    text_box = MessageBox(
        pygame.Rect((display.screen_width * 2 // 5, action_layout['message_y']),
                    (action_layout['message_panel_width'], action_layout['message_panel_height'])),
        manager=display.uiManager,
        loop=loop)

    # Map box
    display.draw_empty_box(action_layout['map_x'], action_layout['map_y'],
                           action_layout['map_width'], action_layout['map_height'])

    # Depth
    display.depth_label = DepthDisplay(
        pygame.Rect((action_layout['map_x'], action_layout['map_y']),
                    (action_layout['map_message_width'], action_layout['map_message_height'])),
        manager=display.uiManager,
        loop=loop)

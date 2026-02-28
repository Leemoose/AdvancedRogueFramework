"""
UI Utility Functions
====================

This module contains shared utility functions for UI operations,
eliminating duplicate code across display.py and ui.py.

Includes:
    - Button drawing utilities
    - Status text formatting
    - Help bar rendering
    - Panel/popup screen setup helpers
"""

import pygame
import pygame_gui
from typing import Tuple, Optional, List, Dict, Any


def draw_image_on_button_states(
    button,
    img: Optional[pygame.Surface],
    offset: Tuple[int, int] = (0, 0),
    text: Optional[pygame.Surface] = None,
    text_pos: Optional[Tuple[int, int]] = None
) -> None:
    """
    Draw an image (and optionally text) on all button states.

    This is the shared implementation that replaces duplicate draw_on_button()
    methods found in display.py, ui.py (SkillButton, StatDownButton, StatUpButton).

    Args:
        button: pygame_gui UIButton with drawable_shape.states
        img: Surface to blit onto button (can be None)
        offset: Position offset for the image
        text: Optional text surface to blit
        text_pos: Position for the text surface
    """
    states = ['normal', 'hovered', 'disabled', 'selected', 'active']

    for state in states:
        if img is not None:
            button.drawable_shape.states[state].surface.blit(img, offset)
        if text is not None and text_pos is not None:
            button.drawable_shape.states[state].surface.blit(text, text_pos)

    button.drawable_shape.active_state.has_fresh_surface = True


def draw_on_button(
    button,
    img: Optional[pygame.Surface],
    letter: str = "",
    button_size: Optional[Tuple[int, int]] = None,
    shrink: bool = False,
    offset_factor: int = 10,
    text_offset: Tuple[int, float] = (15, 0.8),
    font_path: str = 'freesansbold.ttf',
    font_size: int = 20
) -> None:
    """
    Draw an image and optional letter label on a button.

    Replaces the identical draw_on_button() implementations in:
    - display.py:322-341
    - ui.py:533-554 (SkillButton)

    Args:
        button: pygame_gui UIButton
        img: Image surface to draw (can be None for SkillButton when no skill assigned)
        letter: Letter/number label to draw in corner
        button_size: Size of button for scaling calculations
        shrink: Whether to shrink the image to 80% size
        offset_factor: Divisor for calculating offset when shrinking
        text_offset: Tuple of (x_divisor, y_multiplier) for text positioning
        font_path: Path to font file
        font_size: Size of font for letter
    """
    offset = (0, 0)

    if shrink and img is not None and button_size is not None:
        # Shrink image to 80% of button size
        new_width = button_size[0] * 4 // 5
        new_height = button_size[1] * 4 // 5
        img = pygame.transform.scale(img, (new_width, new_height))
        offset = (button_size[0] // offset_factor, button_size[1] // offset_factor)

    # Prepare text if letter provided and button_size known
    text_surface = None
    text_pos = None
    if button_size and letter:
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(letter, True, (255, 255, 255))
        text_pos = (button_size[0] // text_offset[0], int(button_size[1] * text_offset[1]))

    draw_image_on_button_states(button, img, offset, text_surface, text_pos)


def draw_simple_image_on_button(button, img: pygame.Surface) -> None:
    """
    Draw an image on all button states with no offset or text.

    Replaces the simple draw_on_button() implementations in:
    - ui.py:611-618 (StatDownButton)
    - ui.py:651-658 (StatUpButton)

    Args:
        button: pygame_gui UIButton
        img: Image surface to draw
    """
    draw_image_on_button_states(button, img, (0, 0))


def draw_text_on_button(
    button,
    text: str,
    button_size: Tuple[int, int],
    font_path: str = 'freesansbold.ttf',
    font_size: int = 20,
    color: Tuple[int, int, int] = (255, 255, 255),
    center: bool = True
) -> None:
    """
    Draw text on all button states.

    Args:
        button: pygame_gui UIButton
        text: Text to render
        button_size: Size of button for positioning
        font_path: Path to font file
        font_size: Size of font
        color: Text color
        center: Whether to center the text
    """
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, color)

    if center:
        text_pos = (
            button_size[0] // 2 - text_surface.get_width() // 2,
            button_size[1] // 2 - text_surface.get_height() // 2
        )
    else:
        text_pos = (10, 10)  # Default offset from corner

    draw_image_on_button_states(button, None, (0, 0), text_surface, text_pos)


def draw_box_over_button(
    button,
    button_size: Tuple[int, int],
    color: Tuple[int, int, int] = (69, 73, 78),
    border: int = 5
) -> None:
    """
    Draw a filled box over a button (used to gray out disabled buttons).

    Args:
        button: pygame_gui UIButton
        button_size: Size of button
        color: Fill color
        border: Border width to leave unfilled
    """
    rect = (border, border, button_size[0] - border * 2, button_size[1] - border * 2)

    for state in ['normal', 'hovered', 'disabled', 'selected', 'active']:
        pygame.draw.rect(button.drawable_shape.states[state].surface, color, rect)

    button.drawable_shape.active_state.has_fresh_surface = True


# ==============================================================================
# STATUS TEXT UTILITY
# ==============================================================================

def get_status_text(entity) -> str:
    """
    Get formatted status text for an entity.

    This is the shared implementation that replaces the duplicate "HORRIBLE HACK"
    code in both display.py and ui.py.

    Args:
        entity: Entity with character.status and health attributes

    Returns:
        Formatted status string like "Healthy" or "Wounded, Poisoned (3)"
    """
    status = "Healthy"
    if entity.character.get_health() < entity.character.get_max_health() * 2 // 3:
        status = "Wounded"

    effects = entity.character.status.get_status_effects()
    for effect in effects:
        status += ", " + effect.description()

    return status


# ==============================================================================
# HELP BAR RENDERING
# ==============================================================================

def draw_help_bar(
    surface: pygame.Surface,
    text: str,
    screen_width: int,
    screen_height: int,
    bar_height: int = 25,
    padding: int = 10,
    bg_color: Tuple[int, int, int] = (30, 30, 30),
    text_color: Tuple[int, int, int] = (200, 200, 200),
    font_path: str = 'freesansbold.ttf',
    font_size: int = 14
) -> None:
    """
    Draw a contextual help bar at the bottom of the screen.

    Args:
        surface: Surface to draw on
        text: Help text to display
        screen_width: Width of screen
        screen_height: Height of screen
        bar_height: Height of help bar
        padding: Horizontal padding
        bg_color: Background color
        text_color: Text color
        font_path: Font file path
        font_size: Font size
    """
    if not text:
        return

    # Draw background
    bar_rect = pygame.Rect(0, screen_height - bar_height, screen_width, bar_height)
    pygame.draw.rect(surface, bg_color, bar_rect)

    # Draw text
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, text_color)
    text_x = padding
    text_y = screen_height - bar_height + (bar_height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))


# ==============================================================================
# SCREEN SETUP HELPERS
# ==============================================================================

def setup_panel_screen(
    display,
    title: str,
    layout_func: str = 'panel'
) -> Dict[str, Any]:
    """
    Common setup for panel-style screens (inventory, spells, equipment, etc.).

    Handles the duplicated initialization pattern found in:
    - inventory_screen.py
    - spell_screen.py
    - equipment_screen.py
    - And others...

    Args:
        display: The Display instance
        title: Screen title to display
        layout_func: Which layout to use ('panel' or 'equipment')

    Returns:
        Dict containing the panel layout values for further customization
    """
    from .ui_constants import UIColors, UILayout

    # Clear and fill - only need to do once, not twice
    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated when returning to action screen
    display.menu_buttons = None
    display.win.fill(UIColors.BLACK)

    # Get layout based on type
    if layout_func == 'equipment':
        layout = UILayout.get_equipment_screen_layout(display.screen_width, display.screen_height)
        panel_x = layout['panel_x']
        panel_y = 0
        title_x = layout['title_x']
        title_y = layout['title_y']
    else:
        layout = UILayout.get_panel_screen_layout(display.screen_width, display.screen_height)
        panel_x = layout['panel_x']
        panel_y = layout['panel_y']
        title_x = layout['title_x']
        title_y = layout['title_y']

    # Draw panel background
    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(panel_x, panel_y,
                                 layout['panel_width'], layout['panel_height']))

    # Draw escape button
    if layout_func == 'equipment':
        display.draw_escape_button(title_x, title_y,
                                   layout['panel_width'], layout['panel_height'])
    else:
        display.draw_escape_button(layout['button_x'], layout['button_y'],
                                   layout['panel_width'], layout['panel_height'])

    # Draw title
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((title_x, title_y),
                                  (layout['title_width'], layout['title_height'])),
        text=title,
        manager=display.uiManager,
        object_id='#title_label')

    return layout


def setup_popup_screen(
    display,
    title: str,
    overlay: bool = True
) -> Dict[str, Any]:
    """
    Common setup for popup/modal screens (quest, dialogue, etc.).

    Args:
        display: The Display instance
        title: Popup title to display
        overlay: Whether to draw semi-transparent overlay

    Returns:
        Dict containing the popup layout values
    """
    from .ui_constants import UIColors, UILayout

    display.uiManager.clear_and_reset()
    # Clear menu_buttons reference so they will be recreated
    display.menu_buttons = None

    popup_layout = UILayout.get_centered_popup_layout(display.screen_width, display.screen_height)

    # Draw overlay if requested
    if overlay:
        pygame.draw.rect(display.win, UIColors.SCREEN_OVERLAY_BG,
                         pygame.Rect(popup_layout['popup_x'] - popup_layout['overlay_padding'],
                                     popup_layout['popup_y'] - popup_layout['overlay_padding'],
                                     popup_layout['popup_width'] + popup_layout['overlay_padding'] * 2,
                                     popup_layout['popup_height'] + popup_layout['overlay_padding'] * 2))

    # Draw popup background
    pygame.draw.rect(display.win, UIColors.BLACK,
                     pygame.Rect(popup_layout['popup_x'], popup_layout['popup_y'],
                                 popup_layout['popup_width'], popup_layout['popup_height']))

    # Draw escape button and title
    display.draw_escape_button(popup_layout['popup_x'], popup_layout['popup_y'],
                               popup_layout['popup_width'], popup_layout['popup_height'])

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((popup_layout['title_x'], popup_layout['title_y']),
                                  (popup_layout['title_width'], popup_layout['title_height'])),
        text=title,
        manager=display.uiManager,
        object_id='#title_label')

    return popup_layout


def create_item_buttons(
    display,
    items: list,
    layout: Dict[str, Any],
    format_func=None
) -> None:
    """
    Create buttons for a list of items (inventory, spells, quests, etc.).

    Args:
        display: The Display instance
        items: List of items to create buttons for
        layout: Panel layout dict with button positioning
        format_func: Optional function to format item name (item) -> str
    """
    for i, item in enumerate(items):
        if format_func:
            item_name = format_func(item)
        else:
            item_name = getattr(item, 'name', str(item))

        btn_x, btn_y = layout.get('get_button_position', lambda l, i: (
            l['button_x'], l['button_y'] + i * (l['button_height'] + 5)
        ))(layout, i)

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y),
                                      (layout['button_width'], layout['button_height'])),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

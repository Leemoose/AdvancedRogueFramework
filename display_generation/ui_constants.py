"""
UI Constants and Layout Configuration
======================================

This module centralizes all UI-related constants including colors, layout
parameters, and sizing. This replaces hardcoded magic numbers scattered
throughout display.py and ui.py.
"""

from typing import Tuple, Dict

# ==============================================================================
# COLORS (RGB/RGBA)
# ==============================================================================

class UIColors:
    """Game UI color palette - single source of truth for all colors."""

    # Base colors
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    TRANSPARENT: Tuple[int, int, int, int] = (0, 0, 0, 0)

    # UI Backgrounds
    PANEL_BG: Tuple[int, int, int] = (69, 73, 78)
    POPUP_BG: Tuple[int, int, int] = (112, 128, 144)  # Slate gray - entity popup
    BUTTON_DISABLED: Tuple[int, int, int] = (69, 73, 78)
    EXAMINE_WINDOW_BORDER: Tuple[int, int, int] = (100, 100, 100)

    # Minimap colors
    MINIMAP_FLOOR: Tuple[int, int, int] = (131, 131, 131)
    MINIMAP_WALL: Tuple[int, int, int] = (100, 100, 100)
    MINIMAP_MONSTER: Tuple[int, int, int] = (207, 207, 207)
    MINIMAP_ITEM: Tuple[int, int, int] = (0, 200, 0)
    MINIMAP_STAIRS: Tuple[int, int, int] = (0, 0, 200)
    MINIMAP_GATEWAY: Tuple[int, int, int] = (0, 75, 100)
    MINIMAP_PLAYER: Tuple[int, int, int] = (150, 100, 50)
    MINIMAP_INTERACT: Tuple[int, int, int] = (200, 100, 0)

    # HUD colors
    EXP_BAR: Tuple[int, int, int] = (150, 150, 150)
    EXP_BAR_BORDER: Tuple[int, int, int] = (150, 150, 150)

    # Dialogue colors
    DIALOGUE_DEFAULT: Tuple[int, int, int] = (252, 252, 252)
    DIALOGUE_CHOICE: Tuple[int, int, int] = (185, 185, 185)
    DIALOGUE_NPC: Tuple[int, int, int] = (255, 255, 255)
    DIALOGUE_TEXT: Tuple[int, int, int] = (0, 0, 0)

    # Fog of war
    FOG_MULT: Tuple[int, int, int] = (100, 100, 100)

    # Screen backgrounds
    SCREEN_OVERLAY_BG: Tuple[int, int, int] = (50, 50, 50)  # Semi-dark overlay for screens
    SCREEN_BORDER: Tuple[int, int, int] = (0, 0, 0)  # Screen borders

    # Help bar colors
    HELP_BAR_BG: Tuple[int, int, int] = (30, 30, 30)
    HELP_BAR_TEXT: Tuple[int, int, int] = (200, 200, 200)
    HELP_BAR_KEY: Tuple[int, int, int] = (255, 255, 100)


# ==============================================================================
# LAYOUT CONFIGURATION
# ==============================================================================

class UILayout:
    """Centralized UI layout configuration - replaces hardcoded position math."""

    # Screen region ratios
    GAME_AREA_HEIGHT_RATIO = 5 / 6  # Game area takes 5/6 of screen
    HUD_HEIGHT_RATIO = 1 / 6        # HUD takes 1/6 of screen

    # Orb sizes
    ORB_SIZE = 180

    # Minimap configuration
    MINIMAP_WIDTH = 200
    MINIMAP_HEIGHT = 100
    MINIMAP_OFFSET_FROM_RIGHT = 250  # Offset from right edge
    MINIMAP_TILE_SIZE = 5

    # Menu buttons
    BUTTON_WIDTH = 130
    BUTTON_HEIGHT = 40
    BUTTON_SPACING = 10
    BUTTON_LEFT_OFFSET_RATIO = 1 / 5  # Left offset as ratio of screen width
    BUTTON_LEFT_PADDING = 20

    # Experience bar
    EXP_BAR_HEIGHT = 10
    EXP_BAR_PADDING = 3

    # Examine window
    EXAMINE_WINDOW_WIDTH = 350
    EXAMINE_PICTURE_SIZE = 100
    EXAMINE_LINE_SPACING = 15

    # Entity popup window
    ENTITY_SCREEN_WIDTH_RATIO = 1 / 2
    ENTITY_SCREEN_HEIGHT_RATIO = 1 / 2
    ENTITY_IMAGE_SIZE_RATIO = 1 / 20  # Image size relative to screen width
    ENTITY_BUTTON_WIDTH_RATIO = 1 / 10
    ENTITY_BUTTON_HEIGHT_RATIO = 1 / 30

    # Dialogue
    DIALOGUE_BUBBLE_GAP = 10
    DIALOGUE_BUBBLE_PADDING = 5
    DIALOGUE_MAX_BUBBLE_WIDTH_RATIO = 4 / 5

    # Font sizes
    FONT_SIZE_SMALL = 12
    FONT_SIZE_MEDIUM = 20
    FONT_SIZE_LARGE = 24
    FONT_SIZE_TITLE = 25

    # Button drawing
    BUTTON_IMAGE_SHRINK_RATIO = 4 / 5  # Shrink images to 80% on buttons
    BUTTON_IMAGE_OFFSET_FACTOR = 10

    # Help bar
    HELP_BAR_HEIGHT = 25
    HELP_BAR_PADDING = 10

    # Escape button (close button)
    ESCAPE_BUTTON_SIZE = 40

    # Quest popup
    QUEST_POPUP_WIDTH = 300
    QUEST_POPUP_HEIGHT = 100
    QUEST_POPUP_TEXT_OFFSET = 25

    # Fog of war tile
    FOG_TILE_SIZE = 32

    # Screen to tile conversion offset (click precision adjustment)
    SCREEN_TO_TILE_OFFSET = 10

    # Examine window
    EXAMINE_OFFSET_FROM_LEFT = 0
    EXAMINE_ENTITY_OFFSET = 10  # Offset for entity image from window edge
    EXAMINE_TEXT_OFFSET = 10    # Offset for text from entity image

    # Examine window height offset from game area
    EXAMINE_WINDOW_BOTTOM_OFFSET = 100

    # Help bar font size
    HELP_BAR_FONT_SIZE = 14

    # Main screen layout
    MAIN_SCREEN_NUM_BUTTONS = 5
    MAIN_SCREEN_BUTTON_HEIGHT_RATIO = 1 / 8
    MAIN_SCREEN_BUTTON_BOTTOM_RATIO = 95 / 100  # Distance from top as ratio
    MAIN_SCREEN_TITLE_WIDTH_RATIO = 5 / 6
    MAIN_SCREEN_TITLE_HEIGHT_RATIO = 2 / 3
    MAIN_SCREEN_TITLE_OFFSET_RATIO = 1 / 12  # Offset from edges

    @classmethod
    def get_game_area_height(cls, screen_height: int) -> int:
        """Get the height of the main game area."""
        return int(screen_height * cls.GAME_AREA_HEIGHT_RATIO)

    @classmethod
    def get_hud_height(cls, screen_height: int) -> int:
        """Get the height of the HUD area."""
        return screen_height - cls.get_game_area_height(screen_height)

    @classmethod
    def get_health_orb_position(cls, screen_width: int, screen_height: int) -> Tuple[int, int]:
        """Get position for health orb."""
        orb_x = screen_width * 2 // 5 - cls.ORB_SIZE
        orb_y = screen_height - cls.ORB_SIZE
        return (orb_x, orb_y)

    @classmethod
    def get_mana_orb_position(cls, screen_width: int, screen_height: int) -> Tuple[int, int]:
        """Get position for mana orb."""
        orb_x = screen_width * 3 // 5
        orb_y = screen_height - cls.ORB_SIZE
        return (orb_x, orb_y)

    @classmethod
    def get_minimap_rect(cls, screen_width: int, game_area_height: int) -> Tuple[int, int, int, int]:
        """Get minimap position and size as (left, top, width, height)."""
        left = screen_width - cls.MINIMAP_OFFSET_FROM_RIGHT
        top = game_area_height - cls.MINIMAP_HEIGHT
        return (left, top, cls.MINIMAP_WIDTH, cls.MINIMAP_HEIGHT)

    @classmethod
    def get_exp_bar_rect(cls, screen_width: int, game_area_height: int) -> Tuple[int, int, int, int]:
        """Get experience bar position and size as (x, y, width, height)."""
        x = screen_width * 2 // 5 + cls.EXP_BAR_PADDING
        y = game_area_height - cls.EXP_BAR_HEIGHT
        width = screen_width // 5 - cls.EXP_BAR_PADDING * 2
        return (x, y, width, cls.EXP_BAR_HEIGHT)

    @classmethod
    def get_examine_window_rect(cls, screen_height: int, game_area_height: int) -> Tuple[int, int, int, int]:
        """Get examine window position and size as (x, y, width, height)."""
        top = game_area_height - cls.MINIMAP_HEIGHT
        height = screen_height - top
        return (0, top, cls.EXAMINE_WINDOW_WIDTH, height)

    @classmethod
    def get_menu_button_position(cls, screen_width: int, game_area_height: int, index: int) -> Tuple[int, int]:
        """Get position for a menu button by index."""
        x = screen_width // 5 + cls.BUTTON_LEFT_PADDING
        y = game_area_height + index * (cls.BUTTON_HEIGHT + cls.BUTTON_SPACING)
        return (x, y)

    @classmethod
    def get_entity_popup_rect(cls, screen_width: int, screen_height: int) -> Tuple[int, int, int, int]:
        """Get entity popup window position and size."""
        width = int(screen_width * cls.ENTITY_SCREEN_WIDTH_RATIO)
        height = int(screen_height * cls.ENTITY_SCREEN_HEIGHT_RATIO)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        return (x, y, width, height)

    @classmethod
    def get_entity_popup_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get all entity popup window layout values as a dictionary."""
        popup_x, popup_y, popup_width, popup_height = cls.get_entity_popup_rect(screen_width, screen_height)

        image_size = screen_width // 20
        button_width = screen_width // 10
        button_height = screen_height // 30

        return {
            'popup_x': popup_x,
            'popup_y': popup_y,
            'popup_width': popup_width,
            'popup_height': popup_height,
            'message_width': popup_width,
            'message_height': screen_height // 10,
            'message_x': popup_x,
            'message_y': popup_y,
            'image_width': image_size,
            'image_height': image_size,
            'image_x': popup_x + screen_width // 50,
            'image_y': popup_y,
            'button_width': button_width,
            'button_height': button_height,
            'button_x': screen_width // 2 - button_width * 3 // 2,
            'button_y': popup_y + popup_height - button_height - screen_height // 50,
            'button_spacing': button_width // 2,
            'text_x': popup_x + popup_width // 20,
            'text_y': popup_y + screen_height // 10,
            'text_width': popup_width * 11 // 12,
            'text_height': popup_height * 3 // 5,
        }

    @classmethod
    def get_message_position(cls, screen_width: int, screen_height: int, line_index: int) -> Tuple[int, int]:
        """Get position for a message line."""
        x = screen_width * 12 // 100
        y = screen_height * (85 + line_index * 3) // 100
        return (x, y)

    @classmethod
    def get_examine_entity_position(cls, window_height: int, entity_size: int) -> int:
        """Get vertical center position for entity in examine window."""
        return window_height // 2 - entity_size // 2

    @classmethod
    def get_examine_text_offset(cls, window_height: int, num_lines: int) -> int:
        """Get vertical offset for text in examine window."""
        return window_height // 2 - num_lines * cls.EXAMINE_LINE_SPACING // 2

    @classmethod
    def get_tile_viewport(cls, screen_width: int, screen_height: int, tile_size: int) -> dict:
        """
        Calculate tile viewport dimensions for the game area.

        Returns dict with:
            - num_tiles_wide: number of tiles that fit horizontally
            - num_tiles_height: number of tiles that fit vertically
            - center_x: x-coordinate of center tile (r_x)
            - center_y: y-coordinate of center tile (r_y)
        """
        game_area_height = cls.get_game_area_height(screen_height)
        num_tiles_wide = screen_width // tile_size
        num_tiles_height = game_area_height // tile_size
        return {
            'num_tiles_wide': num_tiles_wide,
            'num_tiles_height': num_tiles_height,
            'center_x': num_tiles_wide // 2,
            'center_y': num_tiles_height // 2
        }

    @classmethod
    def get_player_viewport_bounds(cls, player_x: int, player_y: int, center_x: int, center_y: int) -> dict:
        """
        Calculate the visible tile bounds centered on the player.

        Returns dict with:
            - x_start: left bound of visible area
            - x_end: right bound of visible area
            - y_start: top bound of visible area
            - y_end: bottom bound of visible area
        """
        return {
            'x_start': player_x - center_x,
            'x_end': player_x + center_x,
            'y_start': player_y - center_y,
            'y_end': player_y + center_y
        }

    @classmethod
    def get_minimap_viewport(cls, player_x: int, player_y: int, width: int, height: int) -> dict:
        """
        Calculate minimap viewport dimensions and bounds.

        Returns dict with:
            - num_tiles_wide: number of minimap tiles horizontally
            - num_tiles_height: number of minimap tiles vertically
            - center_x: center tile x (r_map_x)
            - center_y: center tile y (r_map_y)
            - x_start: left bound of minimap area
            - x_end: right bound of minimap area
            - y_start: top bound of minimap area
            - y_end: bottom bound of minimap area
        """
        num_tiles_wide = width // cls.MINIMAP_TILE_SIZE
        num_tiles_height = height // cls.MINIMAP_TILE_SIZE
        center_x = num_tiles_wide // 2
        center_y = num_tiles_height // 2
        return {
            'num_tiles_wide': num_tiles_wide,
            'num_tiles_height': num_tiles_height,
            'center_x': center_x,
            'center_y': center_y,
            'x_start': player_x - center_x,
            'x_end': player_x + center_x,
            'y_start': player_y - center_y,
            'y_end': player_y + center_y
        }

    @classmethod
    def get_minimap_tile_rect(cls, left_offset: int, top_offset: int,
                               tile_x: int, tile_y: int, x_start: int, y_start: int) -> Tuple[int, int, int, int]:
        """
        Calculate pixel rectangle for a minimap tile.

        Returns (x, y, width, height) for the tile rectangle.
        """
        x = left_offset + cls.MINIMAP_TILE_SIZE * (tile_x - x_start)
        y = top_offset + cls.MINIMAP_TILE_SIZE * (tile_y - y_start)
        return (x, y, cls.MINIMAP_TILE_SIZE, cls.MINIMAP_TILE_SIZE)

    @classmethod
    def get_minimap_player_rect(cls, left_offset: int, top_offset: int,
                                 center_x: int, center_y: int) -> Tuple[int, int, int, int]:
        """
        Calculate pixel rectangle for the player marker on minimap.

        Returns (x, y, width, height) for the player rectangle.
        """
        x = left_offset + center_x * cls.MINIMAP_TILE_SIZE
        y = top_offset + center_y * cls.MINIMAP_TILE_SIZE
        return (x, y, cls.MINIMAP_TILE_SIZE, cls.MINIMAP_TILE_SIZE)

    @classmethod
    def get_minimap_viewport_outline_rect(cls, left_offset: int, top_offset: int,
                                           minimap_tiles_wide: int, minimap_tiles_height: int,
                                           game_tiles_wide: int, game_tiles_height: int) -> Tuple[int, int, int, int]:
        """
        Calculate pixel rectangle for the viewport outline on minimap.

        Returns (x, y, width, height) for the viewport outline rectangle.
        """
        x = left_offset + (minimap_tiles_wide - game_tiles_wide) * cls.MINIMAP_TILE_SIZE // 2
        y = top_offset + (minimap_tiles_height - game_tiles_height) * cls.MINIMAP_TILE_SIZE // 2
        width = game_tiles_wide * cls.MINIMAP_TILE_SIZE
        height = game_tiles_height * cls.MINIMAP_TILE_SIZE
        return (x, y, width, height)

    @classmethod
    def get_main_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """
        Calculate main screen layout for buttons and title.

        Returns dict with:
            - button_width: width of each button
            - button_height: height of each button
            - button_y: y position for buttons (offset from top)
            - button_spacing: spacing between buttons
            - button_x_start: x position for first button
            - title_width: width of title label
            - title_height: height of title label
            - title_x: x position for title
            - title_y: y position for title
        """
        num_buttons = cls.MAIN_SCREEN_NUM_BUTTONS
        button_width = screen_width // (num_buttons + 1)
        button_height = int(screen_height * cls.MAIN_SCREEN_BUTTON_HEIGHT_RATIO)
        button_y = int(screen_height * cls.MAIN_SCREEN_BUTTON_BOTTOM_RATIO) - button_height
        button_spacing = screen_width // (num_buttons + 1) // (num_buttons + 1)
        button_x_start = button_spacing

        title_width = int(screen_width * cls.MAIN_SCREEN_TITLE_WIDTH_RATIO)
        title_height = int(screen_height * cls.MAIN_SCREEN_TITLE_HEIGHT_RATIO)
        title_offset = int(screen_width * cls.MAIN_SCREEN_TITLE_OFFSET_RATIO)

        return {
            'num_buttons': num_buttons,
            'button_width': button_width,
            'button_height': button_height,
            'button_y': button_y,
            'button_spacing': button_spacing,
            'button_x_start': button_x_start,
            'title_width': title_width,
            'title_height': title_height,
            'title_x': title_offset,
            'title_y': int(screen_height * cls.MAIN_SCREEN_TITLE_OFFSET_RATIO)
        }

    @classmethod
    def get_main_screen_button_position(cls, layout: dict, button_index: int) -> Tuple[int, int]:
        """
        Get position for a main screen button by index.

        Args:
            layout: dict from get_main_screen_layout()
            button_index: 0-based index of the button

        Returns (x, y) position for the button.
        """
        x = layout['button_x_start'] + button_index * (layout['button_width'] + layout['button_spacing'])
        return (x, layout['button_y'])

    # ==========================================================================
    # GENERIC SCREEN LAYOUT HELPERS
    # ==========================================================================

    # Screen overlay constants (for popup/dialog screens)
    SCREEN_OVERLAY_PADDING = 10  # Padding around overlay background
    SCREEN_BORDER_WIDTH = 8      # Border width for popup windows

    # Common screen size ratios
    POPUP_2_3_RATIO = 2 / 3      # 2/3 screen size popup
    POPUP_1_2_RATIO = 1 / 2      # 1/2 screen size popup
    POPUP_4_9_RATIO = 4 / 9      # 4/9 screen size popup (trade screen)

    # Info screen ratios (story, help)
    INFO_SCREEN_BUTTON_WIDTH_RATIO = 1 / 4
    INFO_SCREEN_BUTTON_HEIGHT_RATIO = 1 / 8
    INFO_SCREEN_BUTTON_BOTTOM_RATIO = 95 / 100
    INFO_SCREEN_MESSAGE_SIZE_RATIO = 1 / 2
    INFO_SCREEN_TITLE_WIDTH_RATIO = 1 / 2
    INFO_SCREEN_TITLE_HEIGHT_RATIO = 1 / 10

    # Pause screen ratios
    PAUSE_SCREEN_WIDTH_RATIO = 1 / 3
    PAUSE_SCREEN_HEIGHT_RATIO = 1 / 2
    PAUSE_SCREEN_BUTTON_WIDTH_RATIO = 9 / 10  # Relative to pause screen width

    # Full panel screen ratios (inventory, equipment, spell)
    PANEL_SCREEN_WIDTH_RATIO = 1 / 2
    PANEL_TITLE_HEIGHT_RATIO = 1 / 10
    PANEL_TITLE_TOP_RATIO = 1 / 30
    PANEL_BUTTON_WIDTH_RATIO = 1 / 5
    PANEL_BUTTON_HEIGHT_RATIO = 1 / 30
    PANEL_BUTTON_SPACING_RATIO = 1 / 100

    # Equipment screen specific
    EQUIPMENT_MEDIUM_BUTTON_WIDTH_RATIO = 1 / 8
    EQUIPMENT_MEDIUM_BUTTON_HEIGHT_RATIO = 1 / 5
    EQUIPMENT_SMALL_BUTTON_WIDTH_RATIO = 1 / 16
    EQUIPMENT_SMALL_BUTTON_HEIGHT_RATIO = 1 / 8
    EQUIPMENT_MARGIN_HEIGHT_RATIO = 1 / 30
    EQUIPMENT_MARGIN_WIDTH_RATIO = 1 / 30

    # Level up screen specific
    LEVELUP_STAT_LINE_HEIGHT_RATIO = 1 / 10
    LEVELUP_STAT_LINE_SPACING_RATIO = 1 / 30
    LEVELUP_STAT_BUTTON_WIDTH_RATIO = 1 / 30
    LEVELUP_STAT_BUTTON_HEIGHT_RATIO = 1 / 20

    # Action screen specific
    ACTION_SCREEN_WIDTH_RATIO = 4 / 5
    ACTION_SCREEN_HEIGHT_RATIO = 5 / 6
    SKILL_BAR_HEIGHT_RATIO = 1 / 6
    SKILL_BUTTON_HEIGHT_RATIO = 3 / 4

    @classmethod
    def get_centered_popup_layout(cls, screen_width: int, screen_height: int,
                                   width_ratio: float = 2/3, height_ratio: float = 2/3) -> dict:
        """
        Get layout for a centered popup window.

        Returns dict with popup dimensions and title layout.
        """
        popup_width = int(screen_width * width_ratio)
        popup_height = int(screen_height * height_ratio)
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2

        title_height = popup_height // 6

        return {
            'popup_x': popup_x,
            'popup_y': popup_y,
            'popup_width': popup_width,
            'popup_height': popup_height,
            'title_x': popup_x,
            'title_y': popup_y,
            'title_width': popup_width,
            'title_height': title_height,
            'content_y': popup_y + title_height,
            'content_height': popup_height - title_height,
            'overlay_padding': cls.SCREEN_OVERLAY_PADDING,
        }

    @classmethod
    def get_info_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """
        Get layout for info screens (story, help).

        Returns dict with button, message, and title layout.
        """
        button_width = screen_width // 4
        button_height = screen_height // 8
        button_y = int(screen_height * cls.INFO_SCREEN_BUTTON_BOTTOM_RATIO) - button_height
        button_x = (screen_width - button_width) // 2

        message_width = screen_width // 2
        message_height = screen_height // 2
        message_x = screen_width // 4
        message_y = screen_height // 4

        title_width = screen_width // 2
        title_height = screen_height // 10
        title_x = screen_width // 4
        title_y = screen_height // 10

        return {
            'button_width': button_width,
            'button_height': button_height,
            'button_x': button_x,
            'button_y': button_y,
            'message_width': message_width,
            'message_height': message_height,
            'message_x': message_x,
            'message_y': message_y,
            'title_width': title_width,
            'title_height': title_height,
            'title_x': title_x,
            'title_y': title_y,
        }

    @classmethod
    def get_pause_screen_layout(cls, screen_width: int, screen_height: int, num_buttons: int = 5) -> dict:
        """
        Get layout for pause screen with vertical button list.

        Returns dict with pause screen and button layout.
        """
        pause_width = screen_width // 3
        pause_height = screen_height // 2
        pause_x = (screen_width - pause_width) // 2
        pause_y = screen_height // 4

        button_width = pause_width * 9 // 10
        button_height = pause_height // (num_buttons + 1)
        button_spacing = pause_height // (num_buttons + 1) // (num_buttons + 1)
        button_x = pause_x + (pause_width - button_width) // 2

        return {
            'pause_x': pause_x,
            'pause_y': pause_y,
            'pause_width': pause_width,
            'pause_height': pause_height,
            'button_width': button_width,
            'button_height': button_height,
            'button_spacing': button_spacing,
            'button_x': button_x,
            'num_buttons': num_buttons,
        }

    @classmethod
    def get_pause_button_position(cls, layout: dict, button_index: int) -> Tuple[int, int]:
        """Get position for a pause screen button by index."""
        y = layout['pause_y'] + layout['button_spacing'] + button_index * (layout['button_height'] + layout['button_spacing'])
        return (layout['button_x'], y)

    @classmethod
    def get_death_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get layout for death screen."""
        message_width = screen_width // 4
        message_height = screen_height // 5
        message_x = (screen_width - message_width) // 2
        message_y = (screen_height - message_height) // 2

        button_width = screen_width // 8
        button_height = screen_height // 12
        button_x = (screen_width - button_width) // 2
        button_y = message_y + message_height - button_height - 10

        return {
            'message_width': message_width,
            'message_height': message_height,
            'message_x': message_x,
            'message_y': message_y,
            'button_width': button_width,
            'button_height': button_height,
            'button_x': button_x,
            'button_y': button_y,
        }

    @classmethod
    def get_panel_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """
        Get layout for full-height panel screens (inventory, spell list).

        Returns dict with panel dimensions and button layout.
        """
        panel_width = screen_width // 2
        panel_x = screen_width // 4

        title_width = screen_width // 2
        title_height = screen_height // 10
        title_x = screen_width // 4
        title_y = screen_height // 30

        button_width = screen_width // 5
        button_height = screen_height // 30
        button_x = screen_width * 2 // 5
        button_y = screen_height // 10 + screen_height // 30 + screen_height // 30
        button_spacing = screen_height // 100

        return {
            'panel_width': panel_width,
            'panel_height': screen_height,
            'panel_x': panel_x,
            'panel_y': 0,
            'title_width': title_width,
            'title_height': title_height,
            'title_x': title_x,
            'title_y': title_y,
            'button_width': button_width,
            'button_height': button_height,
            'button_x': button_x,
            'button_y': button_y,
            'button_spacing': button_spacing,
        }

    @classmethod
    def get_panel_button_position(cls, layout: dict, button_index: int) -> Tuple[int, int]:
        """Get position for a panel screen item button by index."""
        y = layout['button_y'] + button_index * (layout['button_height'] + layout['button_spacing'])
        return (layout['button_x'], y)

    @classmethod
    def get_inventory_sidebar_layout(cls, screen_width: int, screen_height: int, num_buttons: int = 5) -> dict:
        """Get layout for inventory sidebar filter buttons."""
        selection_x = screen_width // 16
        selection_y = screen_height // 4
        button_height = (screen_height - selection_y * 2) / (num_buttons + 1)
        button_width = screen_width // 8
        button_spacing = button_height / (num_buttons + 1)

        return {
            'selection_x': selection_x,
            'selection_y': selection_y,
            'button_width': button_width,
            'button_height': button_height,
            'button_spacing': button_spacing,
            'right_x': 13 * screen_width // 16,  # Right side buttons
        }

    @classmethod
    def get_sidebar_button_position(cls, layout: dict, button_index: int, right_side: bool = False) -> Tuple[int, int]:
        """Get position for a sidebar button by index."""
        x = layout['right_x'] if right_side else layout['selection_x']
        y = layout['selection_y'] + layout['button_spacing'] + button_index * (layout['button_height'] + layout['button_spacing'])
        return (x, y)

    @classmethod
    def get_equipment_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get layout for equipment screen with grid of equipment slots."""
        panel_width = screen_width * 2 // 3
        panel_x = screen_width // 3

        title_width = screen_width // 2
        title_height = screen_height // 10
        title_x = screen_width // 4
        title_y = screen_height // 30

        medium_button_width = screen_width // 8
        medium_button_height = screen_height // 5
        small_button_width = screen_width // 16 - screen_width // 120
        small_button_height = screen_height // 8

        first_col_x = screen_width // 4
        outer_cols_y = screen_height // 5
        middle_col_y = screen_height // 5

        margin_height = screen_height // 30
        margin_width = screen_width // 30
        small_margin_width = screen_width // 60

        return {
            'panel_width': panel_width,
            'panel_height': screen_height,
            'panel_x': panel_x,
            'title_width': title_width,
            'title_height': title_height,
            'title_x': title_x,
            'title_y': title_y,
            'medium_button_width': medium_button_width,
            'medium_button_height': medium_button_height,
            'small_button_width': small_button_width,
            'small_button_height': small_button_height,
            'first_col_x': first_col_x,
            'outer_cols_y': outer_cols_y,
            'middle_col_y': middle_col_y,
            'margin_height': margin_height,
            'margin_width': margin_width,
            'small_margin_width': small_margin_width,
        }

    @classmethod
    def get_option_buttons_layout(cls, popup_layout: dict, num_options: int, max_width: int = 300) -> dict:
        """
        Get layout for horizontal option buttons in a popup.

        Args:
            popup_layout: dict from get_centered_popup_layout()
            num_options: number of option buttons
            max_width: maximum button width
        """
        button_width = min(popup_layout['popup_width'] // (num_options + 1), max_width)
        button_height = popup_layout['content_height'] // 8
        button_spacing = button_width // (num_options + 1)
        button_y = popup_layout['content_y']

        return {
            'button_width': button_width,
            'button_height': button_height,
            'button_spacing': button_spacing,
            'button_x': popup_layout['popup_x'],
            'button_y': button_y,
            'num_options': num_options,
        }

    @classmethod
    def get_option_button_position(cls, layout: dict, button_index: int) -> Tuple[int, int]:
        """Get position for an option button by index."""
        x = layout['button_x'] + layout['button_spacing'] + button_index * (layout['button_width'] + layout['button_spacing'])
        return (x, layout['button_y'])

    @classmethod
    def get_popup_message_layout(cls, popup_layout: dict, buttons_layout: dict = None) -> dict:
        """
        Get layout for message/text area in a popup.

        Args:
            popup_layout: dict from get_centered_popup_layout()
            buttons_layout: optional dict from get_option_buttons_layout()
        """
        if buttons_layout:
            message_y = buttons_layout['button_y'] + buttons_layout['button_height'] + 10
        else:
            message_y = popup_layout['content_y']

        message_height = popup_layout['popup_y'] + popup_layout['popup_height'] - message_y - popup_layout['popup_y']

        return {
            'message_x': popup_layout['popup_x'],
            'message_y': message_y,
            'message_width': popup_layout['popup_width'],
            'message_height': message_height,
        }

    @classmethod
    def get_levelup_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get layout for level up screen with stat adjustment controls."""
        popup = cls.get_centered_popup_layout(screen_width, screen_height, 1/2, 1/2)

        stat_line_x = popup['popup_x'] + popup['popup_width'] // 6
        stat_line_y = popup['popup_y'] + popup['popup_height'] // 4
        stat_line_width = popup['popup_width'] * 2 // 3
        stat_line_height = popup['popup_height'] // 10
        stat_line_spacing = popup['popup_height'] // 30

        stat_button_width = popup['popup_width'] // 30
        stat_button_height = popup['popup_height'] // 20
        stat_button_x = popup['popup_x'] + popup['popup_width'] // 24
        stat_button_y = stat_line_y + stat_button_height // 2
        stat_button_spacing_width = stat_button_width
        stat_text_x = stat_button_x + stat_button_width + stat_button_width // 8

        stat_outline_x = stat_button_x - stat_button_width // 2
        stat_outline_y = stat_line_y - popup['popup_height'] // 30
        stat_outline_width = stat_line_width + popup['popup_width'] // 5
        stat_outline_height = stat_line_height + popup['popup_height'] // 20

        confirm_button_width = popup['popup_width'] // 6
        confirm_button_height = stat_button_height * 2
        confirm_button_x = stat_outline_width + stat_outline_x - confirm_button_width
        confirm_button_y = stat_line_y + 4 * (stat_line_height + stat_line_spacing) + stat_line_height + stat_line_spacing * 3 // 4

        return {
            **popup,
            'border_width': cls.SCREEN_BORDER_WIDTH,
            'stat_line_x': stat_line_x,
            'stat_line_y': stat_line_y,
            'stat_line_width': stat_line_width,
            'stat_line_height': stat_line_height,
            'stat_line_spacing': stat_line_spacing,
            'stat_button_width': stat_button_width,
            'stat_button_height': stat_button_height,
            'stat_button_x': stat_button_x,
            'stat_button_y': stat_button_y,
            'stat_button_spacing_width': stat_button_spacing_width,
            'stat_text_x': stat_text_x,
            'stat_outline_x': stat_outline_x,
            'stat_outline_y': stat_outline_y,
            'stat_outline_width': stat_outline_width,
            'stat_outline_height': stat_outline_height,
            'confirm_button_width': confirm_button_width,
            'confirm_button_height': confirm_button_height,
            'confirm_button_x': confirm_button_x,
            'confirm_button_y': confirm_button_y,
            'message_x': popup['popup_x'] + popup['popup_width'] // 4,
            'message_y': popup['popup_y'] + popup['popup_height'] // 30,
            'message_width': popup['popup_width'] // 2,
            'message_height': popup['popup_height'] // 10,
        }

    @classmethod
    def get_levelup_stat_position(cls, layout: dict, stat_index: int) -> dict:
        """Get positions for a stat row in level up screen."""
        y_offset = stat_index * (layout['stat_line_height'] + layout['stat_line_spacing'])
        return {
            'down_button_x': layout['stat_button_x'],
            'down_button_y': layout['stat_button_y'] + y_offset,
            'up_button_x': layout['stat_button_x'] + layout['stat_button_width'] + layout['stat_button_spacing_width'],
            'up_button_y': layout['stat_button_y'] + y_offset,
            'text_x': layout['stat_text_x'],
            'text_y': layout['stat_button_y'] + y_offset,
            'label_x': layout['stat_line_x'],
            'label_y': layout['stat_line_y'] + y_offset,
            'outline_y': layout['stat_outline_y'] + y_offset,
        }

    @classmethod
    def get_victory_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get layout for victory screen."""
        popup = cls.get_centered_popup_layout(screen_width, screen_height, 1/2, 1/2)

        message_width = popup['popup_width'] // 2
        message_height = popup['popup_height'] // 5
        message_x = popup['popup_x'] + popup['popup_width'] // 4
        message_y = popup['popup_y'] + popup['popup_height'] // 30

        text_x = popup['popup_x'] + popup['popup_width'] // 20
        text_y = popup['popup_y'] + popup['popup_height'] // 4
        text_width = popup['popup_width'] * 9 // 10
        text_height = popup['popup_height'] * 3 // 5

        return {
            **popup,
            'border_width': cls.SCREEN_BORDER_WIDTH,
            'message_x': message_x,
            'message_y': message_y,
            'message_width': message_width,
            'message_height': message_height,
            'text_x': text_x,
            'text_y': text_y,
            'text_width': text_width,
            'text_height': text_height,
        }

    @classmethod
    def get_trade_screen_layout(cls, screen_width: int, screen_height: int) -> dict:
        """Get layout for trade/dialogue screen."""
        popup = cls.get_centered_popup_layout(screen_width, screen_height, 4/9, 4/9)

        title_height = popup['popup_height'] // 5

        num_buttons_height = 4
        num_buttons_width = 8
        button_x = popup['popup_x'] + popup['popup_width'] // 2
        button_y = popup['popup_y'] + title_height
        button_width = (popup['popup_width'] // 2) // (num_buttons_width + 1)
        button_height = (popup['popup_height'] - title_height) * 2 // 3 // (num_buttons_height + 1)
        margin_height = (popup['popup_height'] - title_height) * 2 // 3 // (num_buttons_height + 1) // (num_buttons_height + 1)
        margin_width = (popup['popup_width'] // 2) // (num_buttons_width + 1) // (num_buttons_width + 1)

        option_button_width = popup['popup_width'] // 4
        option_button_x = popup['popup_x']
        option_button_y = popup['popup_y'] + title_height

        message_x = popup['popup_x']
        message_y = button_y + (popup['popup_height'] - title_height) * 2 // 3
        message_width = popup['popup_width']
        message_height = screen_height - message_y - popup['popup_y']

        player_size = popup['popup_width'] // 10
        player_x = popup['popup_x'] + popup['popup_width'] // 15
        player_y = popup['popup_y'] + popup['popup_height'] * 4 // 5
        npc_x = popup['popup_x'] + popup['popup_width'] * 9 // 11

        dialogue_width = popup['popup_width'] * 3 // 5
        dialogue_height = popup['popup_height'] * 4 // 5
        dialogue_x = popup['popup_x'] + popup['popup_width'] // 5
        dialogue_y = popup['popup_y'] + popup['popup_height'] // 6

        return {
            **popup,
            'title_height': title_height,
            'button_x': button_x,
            'button_y': button_y,
            'button_width': button_width,
            'button_height': button_height,
            'margin_height': margin_height,
            'margin_width': margin_width,
            'num_buttons_height': num_buttons_height,
            'num_buttons_width': num_buttons_width,
            'option_button_width': option_button_width,
            'option_button_x': option_button_x,
            'option_button_y': option_button_y,
            'message_x': message_x,
            'message_y': message_y,
            'message_width': message_width,
            'message_height': message_height,
            'player_size': player_size,
            'player_x': player_x,
            'player_y': player_y,
            'npc_x': npc_x,
            'dialogue_width': dialogue_width,
            'dialogue_height': dialogue_height,
            'dialogue_x': dialogue_x,
            'dialogue_y': dialogue_y,
        }

    @classmethod
    def get_trade_item_position(cls, layout: dict, item_index: int) -> Tuple[int, int]:
        """Get position for a trade item button by index (grid layout)."""
        row = item_index % layout['num_buttons_height']
        col = item_index // layout['num_buttons_height']
        x = layout['button_x'] + layout['margin_width'] + col * (layout['margin_width'] + layout['button_width'])
        y = layout['button_y'] + layout['margin_height'] + row * (layout['margin_height'] + layout['button_height'])
        return (x, y)

    @classmethod
    def get_action_screen_layout(cls, screen_width: int, screen_height: int, text_size: int) -> dict:
        """Get layout for action screen with skill bar."""
        action_width = screen_width * 3 // 4
        action_height = screen_height * 5 // 6

        message_x = 0
        message_width = action_width * 5 // 12

        stats_x = action_width
        stats_y = screen_height * 2 // 3
        stats_width = 400
        stats_height = screen_height // 3

        map_tile_size = 10
        map_x = action_width
        map_y = action_height - 100
        map_width = screen_width - action_width
        map_height = screen_height - map_y
        map_message_width = stats_width
        map_message_height = 30

        message_y = action_height
        message_panel_width = screen_width // 5
        message_panel_height = screen_height - action_height

        skill_bar_height = screen_height - action_height
        skill_bar_x = message_width
        skill_bar_y = action_height
        skill_bar_width = stats_x - skill_bar_x

        return {
            'action_width': action_width,
            'action_height': action_height,
            'message_x': message_x,
            'message_width': message_width,
            'message_y': message_y,
            'message_panel_width': message_panel_width,
            'message_panel_height': message_panel_height,
            'stats_x': stats_x,
            'stats_y': stats_y,
            'stats_width': stats_width,
            'stats_height': stats_height,
            'map_tile_size': map_tile_size,
            'map_x': map_x,
            'map_y': map_y,
            'map_width': map_width,
            'map_height': map_height,
            'map_message_width': map_message_width,
            'map_message_height': map_message_height,
            'skill_bar_x': skill_bar_x,
            'skill_bar_y': skill_bar_y,
            'skill_bar_width': skill_bar_width,
            'skill_bar_height': skill_bar_height,
        }

    @classmethod
    def get_skill_bar_layout(cls, screen_width: int, screen_height: int, num_skills: int) -> dict:
        """Get layout for skill bar buttons."""
        action_width = screen_width * 3 // 4
        action_height = screen_height * 5 // 6

        message_width = action_width * 5 // 12

        skill_bar_x = message_width
        skill_bar_y = action_height
        skill_bar_width = action_width - skill_bar_x
        skill_bar_height = screen_height - action_height

        button_width = (action_width - skill_bar_x) // (num_skills + 1)
        button_height = skill_bar_height * 3 // 4
        button_y = skill_bar_height // 8 + skill_bar_y
        button_spacing = (action_width - skill_bar_x) // (num_skills + 1) // (num_skills + 1)

        return {
            'skill_bar_x': skill_bar_x,
            'skill_bar_y': skill_bar_y,
            'skill_bar_width': skill_bar_width,
            'skill_bar_height': skill_bar_height,
            'button_width': button_width,
            'button_height': button_height,
            'button_y': button_y,
            'button_spacing': button_spacing,
            'num_skills': num_skills,
        }

    @classmethod
    def get_skill_button_position(cls, layout: dict, skill_index: int) -> Tuple[int, int]:
        """Get position for a skill bar button by index."""
        x = layout['skill_bar_x'] + layout['button_spacing'] + skill_index * (layout['button_spacing'] + layout['button_width'])
        return (x, layout['button_y'])


# ==============================================================================
# HELP TEXT - Action Discoverability
# ==============================================================================

class HelpText:
    """Contextual help text for different game states."""

    # Format: key in brackets, action name follows
    ACTION_SCREEN = "[↑↓←→]Move [G]rab [I]nventory [E]quipment [X]amine [.]Wait [Z]Rest [Tab]Attack [O]Explore"
    INVENTORY_SCREEN = "[A-Z]Select [Esc]Back [1-5]Filter [6]Orbs"
    EQUIPMENT_SCREEN = "[Q]Shield [W]Helm [A]Amulet [S]Armor [D]Weapon [X]Boots [C]Gloves [Z]Ring [P]ants [Esc]Back"
    TARGETING_SCREEN = "[↑↓←→]Move [Enter]Confirm [Esc]Cancel"
    EXAMINE_SCREEN = "[↑↓←→]Move [Enter]Details [Esc]Back"
    ITEM_SCREEN = "[E]quip [U]nequip [D]rop [Q]uaff [R]ead [A]ctivate [Esc]Back"
    SPELL_SCREEN = "[A-Z]Select spell [Esc]Back"
    SPELL_INDIVIDUAL = "[C]ast [Q]uick assign [Esc]Back"
    QUICKCAST_SCREEN = "[1-8]Assign slot [Esc]Back"
    LEVEL_UP_SCREEN = "[↑↓]Select stat [←→]Adjust [Enter]Confirm [Esc]Cancel"
    PAUSED_SCREEN = "[Esc]Resume [M]ain menu [S]ave [B]indings [Q]uit"
    DIALOGUE_SCREEN = "[Enter]Continue [1-9]Choose option [Esc]Exit"
    MAIN_SCREEN = "[Any]Start [L]oad [H]elp [S]tory [Esc]Quit"
    QUEST_SCREEN = "[1-9]Select quest [Esc]Back"

    @classmethod
    def get_help_for_state(cls, loop_type_name: str) -> str:
        """Get help text for a given game state."""
        help_mapping = {
            "action": cls.ACTION_SCREEN,
            "inventory": cls.INVENTORY_SCREEN,
            "equipment": cls.EQUIPMENT_SCREEN,
            "targeting": cls.TARGETING_SCREEN,
            "examine": cls.EXAMINE_SCREEN,
            "items": cls.ITEM_SCREEN,
            "spell": cls.SPELL_SCREEN,
            "spell_individual": cls.SPELL_INDIVIDUAL,
            "quickcast": cls.QUICKCAST_SCREEN,
            "level_up": cls.LEVEL_UP_SCREEN,
            "paused": cls.PAUSED_SCREEN,
            "trade": cls.DIALOGUE_SCREEN,
            "main": cls.MAIN_SCREEN,
            "quest": cls.QUEST_SCREEN,
            "specific_examine": cls.ITEM_SCREEN,
        }
        return help_mapping.get(loop_type_name.lower(), "")


# ==============================================================================
# TILE EQUIPMENT IDS (for player rendering)
# See asset_registry.py for the complete ID numbering scheme.
# ==============================================================================

class EquipmentTileIDs:
    """
    Tile IDs for equipment rendering on player sprite.

    These IDs correspond to TileID.PLAYER_*_CRAWL constants in asset_registry.py.
    Range: 1030-1034 (Player Crawl Overlays)
    """
    BOOTS = 1031       # TileID.PLAYER_BOOTS_CRAWL
    GLOVES = 1030      # TileID.PLAYER_GLOVES_CRAWL
    HELMET = 1032      # TileID.PLAYER_HEAD_CRAWL
    BODY_ARMOR = 1033  # TileID.PLAYER_BODY_CRAWL
    PANTS = 1034       # TileID.PLAYER_LEGS_CRAWL


# ==============================================================================
# UI ELEMENT IDS (for targeting cursor, etc)
# See asset_registry.py for the complete ID numbering scheme.
# ==============================================================================

class UITileIDs:
    """
    Tile IDs for UI elements.

    These IDs correspond to TileID constants in asset_registry.py.
    Range: 9000-9099 (System UI)
    """
    TARGETING_CURSOR = 9000  # TileID.TARGET

from .ui import *
from .ui_constants import UIColors, UILayout, HelpText, EquipmentTileIDs, UITileIDs
from .ui_utils import draw_on_button, get_status_text, draw_help_bar
import pygame
import pygame_gui
from src.core.enums import LoopType  # Moved from loop_workflow to break circular import
from src.core.asset_cache import AssetCache
from src.core.constants import NO_ENTITY
import warnings


class Display:
    """
    Display is responsible for put images in the screen. Currently have it set that each function will update a
    seperate part of the game.
    """
    def __init__(self, width, height, textSize, textWidth, textHeight):
        pygame.display.set_caption('Tiles')
        self.win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_width = width
        self.screen_height = height
        self.textWidth = textWidth
        self.textHeight = textHeight
        self.textSize = textSize

        tile_viewport = UILayout.get_tile_viewport(self.screen_width, self.screen_height, self.textSize)
        self.r_x = tile_viewport['center_x']
        self.r_y = tile_viewport['center_y']

        self.uiManager = pygame_gui.UIManager((width, height), "./assets/theme.json")
        self.windows = []
        self.clock = pygame.time.Clock()
        self.colorDict = None
        self.depth_label = None

        self.quest_number = -1

        # Cached UI elements to avoid creating every frame
        self.menu_buttons = None
        self.current_loop_type = None  # Track current loop for help bar

    def get_tile_screen_center(self):
        return (self.r_x, self.r_y)

    def get_tile_size(self):
        return self.textSize

    def get_pixel_location_from_entity_location(self, entity):
        return (self.textSize*(entity.get_x() - self.x_start), self.textSize*(entity.get_y() - self.y_start))
        

    def screen_to_tile(self, player, x, y):
        xplayerscreen, yplayerscreen = self.r_x * self.textSize + self.textSize // 2, self.r_y * self.textSize + self.textSize // 2
        xdiff = x - xplayerscreen + UILayout.SCREEN_TO_TILE_OFFSET
        ydiff = y - yplayerscreen + UILayout.SCREEN_TO_TILE_OFFSET
        return (player.x + xdiff // self.textSize, player.y + ydiff//self.textSize)

    def update_sizes(self):
        """Update screen dimensions and recreate UI elements if needed."""
        old_width, old_height = self.screen_width, self.screen_height
        self.screen_width, self.screen_height = self.win.get_size()

        # If size changed, recreate UI manager and persistent elements
        if old_width != self.screen_width or old_height != self.screen_height:
            self.handle_resize()

    def handle_resize(self):
        """Handle window resize by recreating UI elements."""
        # Recreate UI manager with new size
        self.uiManager = pygame_gui.UIManager(
            (self.screen_width, self.screen_height),
            "./assets/theme.json"
        )

        # Clear cached menu buttons so they get recreated
        self.menu_buttons = None

        # Clear depth label so it gets recreated
        self.depth_label = None

    def update_main(self, loop):
        # Main Screen
        self.win.fill(UIColors.BLACK)
        image_offset_from_left = 0
        image_offset_from_top = 0
        titlescreen = AssetCache.load('assets/titlescreen1.jpeg', (self.screen_width, self.screen_height))
        self.win.blit(titlescreen, (image_offset_from_left, image_offset_from_top))
        self.uiManager.draw_ui(self.win)

        font = pygame.font.Font('freesansbold.ttf', UILayout.FONT_SIZE_SMALL)

    def draw_player(self, loop):
        tileDict = loop.tileDict
        player = loop.player
        player_pixel_x, player_pixel_y = self.get_pixel_location_from_entity_location(player)
        #Draw base character depending on armor state
        self.win.blit(tileDict.tile_string(player.get_render_tag()), (player_pixel_x, player_pixel_y))
        #Draw equipment on top
        if player.body.get_num_free_equipment_slots("boots_slot") == 0:
            self.win.blit(tileDict.tile_string(EquipmentTileIDs.BOOTS), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("gloves_slot") == 0:
            self.win.blit(tileDict.tile_string(EquipmentTileIDs.GLOVES), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("helmet_slot") == 0:
            self.win.blit(tileDict.tile_string(EquipmentTileIDs.HELMET), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("body_armor_slot") == 0:
            self.win.blit(tileDict.tile_string(EquipmentTileIDs.BODY_ARMOR), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("pants_slot") == 0:
            self.win.blit(tileDict.tile_string(EquipmentTileIDs.PANTS), (player_pixel_x, player_pixel_y))

    def update_display(self, loop):
        self.win.fill(UIColors.BLACK)
        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        player = loop.player

        action_screen_height = UILayout.get_game_area_height(self.screen_height)
        tile_viewport = UILayout.get_tile_viewport(self.screen_width, self.screen_height, self.textSize)
        num_tiles_wide = tile_viewport['num_tiles_wide']
        num_tiles_height = tile_viewport['num_tiles_height']
        self.r_x = tile_viewport['center_x']
        self.r_y = tile_viewport['center_y']

        player_bounds = UILayout.get_player_viewport_bounds(player.x, player.y, self.r_x, self.r_y)
        self.x_start = player_bounds['x_start']
        self.x_end = player_bounds['x_end']
        self.y_start = player_bounds['y_start']
        self.y_end = player_bounds['y_end']

        mini_map_left_offset, mini_map_top_offset, mini_map_width, _ = UILayout.get_minimap_rect(self.screen_width, action_screen_height)
        mini_map_height = self.screen_height - mini_map_top_offset

       #Making all the tiles
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                tile = tile_map.get_entity(x, y)
                if tile != NO_ENTITY:
                    self.draw_single_tile(loop, tile)
        for item in item_map.get_all_entities():
            self.draw_single_entity(loop, item)
        for monster in monster_map.get_all_entities():
            self.draw_single_entity(loop, monster)

        self.draw_player(loop)
        self.uiManager.draw_ui(self.win)
        self.update_mini_map(loop, mini_map_left_offset, mini_map_top_offset, mini_map_width, mini_map_height, num_tiles_wide, num_tiles_height)
        self.draw_examine_window(loop, loop.targets.get_target_coordinates(), action_screen_height - UILayout.EXAMINE_WINDOW_BOTTOM_OFFSET)
        self.draw_health_and_mana_orbs(loop)
        self.draw_experience_bar(loop, action_screen_height)
        self.draw_menu_buttons(action_screen_height)
        self.depth_label.update(1)
        self.draw_context_help(loop._current_loop_type)

    def create_menu_buttons(self, action_screen_height):
        """Create menu buttons once - call on init or resize."""
        # Kill existing buttons if any
        if self.menu_buttons:
            for btn in self.menu_buttons:
                btn.kill()

        self.menu_buttons = []
        buttons = [("Inventory", "i"), ("Equipment", "e"), ("Spells", "p")]

        for i, (text, action) in enumerate(buttons):
            x, y = UILayout.get_menu_button_position(self.screen_width, action_screen_height, i)
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (x, y, UILayout.BUTTON_WIDTH, UILayout.BUTTON_HEIGHT)),
                text=text,
                manager=self.uiManager,
                starting_height=1000)  # Important! Need this to be high so it's above the panel.
            btn.action = action
            self.menu_buttons.append(btn)

    def draw_menu_buttons(self, action_screen_height):
        """Ensure menu buttons exist - creates them if needed."""
        if not self.menu_buttons:
            self.create_menu_buttons(action_screen_height)
    def draw_experience_bar(self, loop, action_screen_height):
        exp_x, exp_y, exp_width, exp_height = UILayout.get_exp_bar_rect(self.screen_width, action_screen_height)

        # Draw border
        border_rect = pygame.Rect(exp_x, exp_y, exp_width, exp_height)
        pygame.draw.rect(self.win, UIColors.EXP_BAR_BORDER, border_rect, 2)

        # Draw filled portion
        experience_percentage = loop.player.character.get_experience() / loop.player.character.attributes.get_experience_to_next_level()
        filled_rect = pygame.Rect(exp_x, exp_y, exp_width * experience_percentage, exp_height)
        pygame.draw.rect(self.win, UIColors.EXP_BAR, filled_rect)

    def draw_health_and_mana_orbs(self, loop):
        orb_size = UILayout.ORB_SIZE
        orb_full_size = (orb_size, orb_size)
        orb_half_size = (orb_size, orb_size // 2)

        health_orb_x, health_orb_y = UILayout.get_health_orb_position(self.screen_width, self.screen_height)
        mana_orb_x, mana_orb_y = UILayout.get_mana_orb_position(self.screen_width, self.screen_height)

        # Load overlay images (cached)
        orb_border = AssetCache.load("assets/status_orbs/itsmars_orb_border.png", orb_full_size)
        orb_highlight = AssetCache.load("assets/status_orbs/itsmars_orb_highlight.png", orb_full_size)
        orb_shadow = AssetCache.load("assets/status_orbs/itsmars_orb_shadow.png", orb_full_size)
        orb_back = AssetCache.load("assets/status_orbs/itsmars_orb_back1.png", orb_half_size)

        # Determine health orb fill image
        if loop.player.character.status.has_effect("Poison"):
            health_fill_path = "assets/status_orbs/poison_100.png"
        else:
            health_fill_path = "assets/status_orbs/health_100.png"

        # Calculate exact health percentage (0.0 to 1.0)
        health_ratio = loop.player.character.get_health() / loop.player.character.get_max_health()
        health_ratio = max(0.0, min(1.0, health_ratio))

        # Calculate exact mana percentage (0.0 to 1.0)
        mana_ratio = loop.player.character.get_mana() / loop.player.character.get_max_mana()
        mana_ratio = max(0.0, min(1.0, mana_ratio))

        # Load full fill images (cached)
        health_fill_full = AssetCache.load(health_fill_path, orb_full_size)
        mana_fill_full = AssetCache.load("assets/status_orbs/mana_100.png", orb_full_size)

        # Draw health orb: border first, then clipped fill, then overlays
        self.win.blit(orb_border, (health_orb_x, health_orb_y))
        self._draw_clipped_orb_fill(health_fill_full, health_orb_x, health_orb_y, orb_size, health_ratio)
        self.win.blit(orb_highlight, (health_orb_x, health_orb_y))
        self.win.blit(orb_shadow, (health_orb_x, health_orb_y))
        self.win.blit(orb_back, (health_orb_x, health_orb_y + orb_size // 2))

        # Draw mana orb: border first, then clipped fill, then overlays
        self.win.blit(orb_border, (mana_orb_x, mana_orb_y))
        self._draw_clipped_orb_fill(mana_fill_full, mana_orb_x, mana_orb_y, orb_size, mana_ratio)
        self.win.blit(orb_highlight, (mana_orb_x, mana_orb_y))
        self.win.blit(orb_shadow, (mana_orb_x, mana_orb_y))
        self.win.blit(orb_back, (mana_orb_x, mana_orb_y + orb_size // 2))

    def _draw_clipped_orb_fill(self, fill_surface, orb_x, orb_y, orb_size, fill_ratio):
        """Draw the fill portion of an orb, clipped from the top based on fill_ratio.

        Args:
            fill_surface: The full orb fill image (e.g., health_100.png)
            orb_x, orb_y: Top-left position of the orb
            orb_size: Size of the orb (width and height)
            fill_ratio: 0.0 (empty) to 1.0 (full)
        """
        if fill_ratio <= 0:
            return  # Nothing to draw

        # Calculate how many pixels to show from the bottom
        visible_height = int(orb_size * fill_ratio)
        if visible_height <= 0:
            return

        # The top of the visible portion (pixels to clip from top)
        clip_from_top = orb_size - visible_height

        # Create a subsurface that only includes the bottom portion
        clip_rect = pygame.Rect(0, clip_from_top, orb_size, visible_height)
        clipped_fill = fill_surface.subsurface(clip_rect)

        # Draw at the correct Y position (offset down by the clipped amount)
        self.win.blit(clipped_fill, (orb_x, orb_y + clip_from_top))



    def draw_single_entity(self, loop, entity):
        if entity.get_is_in_square(self.x_start, self.x_end, self.y_start, self.y_end):
            if loop.generator.tile_map.get_visible(entity.get_x(), entity.get_y()):
                entity_tile = pygame.transform.scale(loop.tileDict.tile_string(entity.get_render_tag()), (self.textSize, self.textSize))
                self.win.blit(entity_tile,self.get_pixel_location_from_entity_location(entity))

    def update_mini_map(self, loop, left_offset, top_offset, width, height, num_tiles_wide, num_tiles_height):
        """Draw the minimap showing explored areas."""
        player = loop.player
        minimap_vp = UILayout.get_minimap_viewport(player.x, player.y, width, height)
        x_map_start = minimap_vp['x_start']
        x_map_end = minimap_vp['x_end']
        y_map_start = minimap_vp['y_start']
        y_map_end = minimap_vp['y_end']
        r_map_x = minimap_vp['center_x']
        r_map_y = minimap_vp['center_y']
        num_map_tiles_wide = minimap_vp['num_tiles_wide']
        num_map_tiles_height = minimap_vp['num_tiles_height']

        floormap = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        interact_map = loop.generator.interact_map

        # Making all map tiles
        for x in range(x_map_start, x_map_end):
            for y in range(y_map_start, y_map_end):
                if floormap.in_map(x, y) and floormap.get_entity(x, y).get_seen():
                    rect_tuple = UILayout.get_minimap_tile_rect(left_offset, top_offset, x, y, x_map_start, y_map_start)
                    rectangle = pygame.Rect(*rect_tuple)
                    if floormap.get_entity(x, y).is_passable():
                        if floormap.get_entity(x, y).get_visible() and monster_map.get_has_entity(x, y):
                            pygame.draw.rect(self.win, UIColors.MINIMAP_MONSTER, rectangle)
                        elif item_map.get_has_entity(x, y):
                            pygame.draw.rect(self.win, UIColors.MINIMAP_ITEM, rectangle)
                        elif floormap.get_entity(x, y).has_trait("stairs"):
                            pygame.draw.rect(self.win, UIColors.MINIMAP_STAIRS, rectangle)
                        elif floormap.get_entity(x, y).has_trait("gateway"):
                            pygame.draw.rect(self.win, UIColors.MINIMAP_GATEWAY, rectangle)
                        else:
                            pygame.draw.rect(self.win, UIColors.MINIMAP_FLOOR, rectangle)
                    elif interact_map.get_has_entity(x, y):
                            pygame.draw.rect(self.win, UIColors.MINIMAP_INTERACT, rectangle)
                    else:
                        pygame.draw.rect(self.win, UIColors.MINIMAP_WALL, rectangle)

        player_rect = UILayout.get_minimap_player_rect(left_offset, top_offset, r_map_x, r_map_y)
        pygame.draw.rect(self.win, UIColors.MINIMAP_PLAYER, pygame.Rect(*player_rect))

        outline_rect = UILayout.get_minimap_viewport_outline_rect(
            left_offset, top_offset, num_map_tiles_wide, num_map_tiles_height, num_tiles_wide, num_tiles_height)
        pygame.draw.rect(self.win, UIColors.MINIMAP_PLAYER, pygame.Rect(*outline_rect), 1)


    def write_messages(self, messages):
        font = pygame.font.Font('freesansbold.ttf', UILayout.FONT_SIZE_SMALL)
        for i, message in enumerate(messages):
            text = font.render(message[0], True, message[1])
            msg_x, msg_y = UILayout.get_message_position(self.screen_width, self.screen_height, i)
            self.win.blit(text, (msg_x, msg_y))

    def draw_examine_window(self, loop, target, offset_from_top):
        tileDict = loop.tileDict
        floormap = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        interact_map = loop.generator.interact_map

        examine_offset_from_left = UILayout.EXAMINE_OFFSET_FROM_LEFT
        examine_offset_from_top = offset_from_top
        examine_window_height = self.screen_height - examine_offset_from_top
        entity_picture_size = UILayout.EXAMINE_PICTURE_SIZE
        examine_window_width = UILayout.EXAMINE_WINDOW_WIDTH
        line_spacing = UILayout.EXAMINE_LINE_SPACING
        entity_offset = UILayout.EXAMINE_ENTITY_OFFSET
        text_offset = UILayout.EXAMINE_TEXT_OFFSET

        font = pygame.font.Font('freesansbold.ttf', UILayout.FONT_SIZE_SMALL)
        pygame.draw.rect(self.win, UIColors.EXAMINE_WINDOW_BORDER,
                         pygame.Rect(examine_offset_from_left, examine_offset_from_top, examine_window_width,
                                     examine_window_height), 1)
        if target is not None:
            x, y = target
            if loop.generator.in_map(x, y) and floormap.get_entity(x, y).get_visible():
                if monster_map.get_has_entity(x, y):
                    entity = monster_map.get_entity(x, y)
                elif item_map.get_has_entity(x, y):
                    entity = item_map.get_entity(x, y)
                elif interact_map.get_has_entity(x, y):
                    entity = interact_map.get_entity(x, y)
                else:
                    entity = loop.player
            else:
                entity = loop.player

            tag = pygame.transform.scale(tileDict.tile_string(entity.get_render_tag()),
                                         (entity_picture_size, entity_picture_size))
            entity_y_pos = UILayout.get_examine_entity_position(examine_window_height, entity_picture_size)
            self.win.blit(tag, (examine_offset_from_left + entity_offset, examine_offset_from_top + entity_y_pos))

            num_lines = len(entity.get_render_text())
            text_y_offset = UILayout.get_examine_text_offset(examine_window_height, num_lines)
            description_offset_from_top = examine_offset_from_top + text_y_offset
            for i, descriptor in enumerate(entity.get_render_text()):
                text = font.render(descriptor, True, UIColors.WHITE)
                self.win.blit(text, (
                    examine_offset_from_left + entity_picture_size + text_offset, description_offset_from_top + i * line_spacing))
            return True
        return False

    def draw_on_button(self, button, img, letter="", button_size=None, shrink=False, offset_factor=10, text_offset=(15, 0.8)):
        """Draw image and letter on button - delegates to shared utility."""
        draw_on_button(button, img, letter, button_size, shrink, offset_factor, text_offset)


    def refresh_screen(self):
        self.uiManager.clear_and_reset()
        # Clear menu_buttons reference so they will be recreated
        self.menu_buttons = None

    def stat_text(self, entity, stat):
        return str(stat)

    def stat_modifier(self, entity, stat):
        if stat >= 0:
            return "+" + str(stat)
        else:
            return str(stat)


    def draw_character_stats(self, player, margin_from_left, margin_from_top, width, height):
        if player.character.get_strength() >= 0:
            strength_modifier = "+" + str(player.character.get_strength())
        else:
            strength_modifier = str(player.character.get_strength())
        weapon = player.body.get_weapon()
        
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            
            html_text = "Player<br><br>"
                        "Stats<br>"
                        "Strength: " + self.stat_text(player, player.character.get_strength()) + "<br>"
                        "Dexterity: " + self.stat_text(player, player.character.get_dexterity()) + "<br>"
                        "Endurance: " + self.stat_text(player, player.character.get_endurance()) + "<br>"
                        "Intelligence: " + self.stat_text(player, player.character.get_intelligence()) + "<br>" +
                        "Health: " + str(player.character.get_health()) + " / " + str(player.character.get_max_health()) + "<br>"
                        "Mana: " + str(player.character.get_mana()) + " / " + str(player.character.get_max_mana()) + "<br>"
                        "<br>"
                        "Damage: " + str(player.fighter.get_damage_min()) + " - " + str(player.fighter.get_damage_max()) + " (" + strength_modifier + ") <br>"
                        "Defense: " + str(player.character.attributes.get_armor()) + " <br>"
                        "Movement Delay: " + str(player.character.action_costs["move"]) + "<br>"
                        "Skill Damage Bonus: " + str(player.character.skill_damage_increase()) + "<br>"
                        "Effect Duration Bonus: " + str(player.character.skill_duration_increase()) + "<br>"
                        "<br>Known Skills:<br>"
                        + "<br>".join([str(i + 1) + ". " + skill.description() for i, skill in enumerate(player.mage.known_spells)])
                        ,
            manager=self.uiManager
        )

    def draw_empty_box(self, margin_from_left, margin_from_top, width, height):
        box = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            manager=self.uiManager
        )

    def draw_escape_button(self, windowX, windowY, window_width, window_height):
        buttonSize = UILayout.ESCAPE_BUTTON_SIZE

        buttonX = windowX + window_width - buttonSize
        buttonY = windowY

        esc_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((buttonX, buttonY), (buttonSize, buttonSize)),
            text="X",
            manager=self.uiManager,
            starting_height=1000)
        esc_button.action = "esc"


    def update_entity(self, loop, item_screen=True, create=False):
        entity = loop.targets.get_target()
        tileDict = loop.tileDict
        player = loop.player
        if create:
            self.uiManager.clear_and_reset()
            # Clear menu_buttons reference so they will be recreated
            self.menu_buttons = None
        self.win.fill(UIColors.BLACK)

        # Get layout values from centralized config
        layout = UILayout.get_entity_popup_layout(self.screen_width, self.screen_height)

        entity_screen_width = layout['popup_width']
        entity_screen_height = layout['popup_height']
        entity_offset_from_left = layout['popup_x']
        entity_offset_from_top = layout['popup_y']

        entity_message_width = layout['message_width']
        entity_message_height = layout['message_height']
        entity_message_offset_from_left = layout['message_x']
        entity_message_offset_from_top = layout['message_y']

        entity_image_width = layout['image_width']
        entity_image_height = layout['image_height']
        entity_image_offset_from_left = layout['image_x']
        entity_image_offset_from_top = layout['image_y']

        entity_button_width = layout['button_width']
        entity_button_height = layout['button_height']
        entity_button_offset_from_left = layout['button_x']
        entity_button_offset_from_top = layout['button_y']
        entity_button_offset_from_each_other = layout['button_spacing']

        entity_text_offset_from_left = layout['text_x']
        entity_text_offset_from_top = layout['text_y']
        entity_text_width = layout['text_width']
        entity_text_height = layout['text_height']

        buttons_drawn = 0

        entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                     (entity_image_width, entity_image_height))

        pygame.draw.rect(self.win, UIColors.POPUP_BG, pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

        self.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

        if (create == True):
            self.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

        entity_name = entity.name
        if create == True:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                          (entity_message_width, entity_message_height)),
                text=entity_name,
                manager=self.uiManager,
                object_id='#title_small')

        if item_screen:
            item = entity
            show = False
            if item.can_be_levelled:
                item_level = item.level
                if item_level > 1:
                    addition = " (+" + str(item_level - 1) + ")"
                    #
                    if create == True:
                        pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((entity_message_offset_from_left + entity_message_width * 4// 5, entity_message_offset_from_top),
                                                (entity_message_width // 4, entity_message_height)),
                        text=addition,
                        manager=self.uiManager,
                        object_id='#title_addition')
            pretext = ""
            action = ""
            if item.equipable:
                if item.equipped:
                    pretext = "Unequip"
                    action = "u"
                    show = True
                    if item.cursed:
                        show = False
                else:
                    pretext = "Equip"
                    action = "e"
                    show = True
            elif item.consumeable and item.equipment_type == "Potiorb":
                pretext = "Quaff"
                action = "q"
                show = True
            elif item.consumeable and item.equipment_type == "Scrorb" or item.equipment_type == "Book":
                pretext = "Read"
                action = "r"
                show = True
            elif item.consumeable and item.has_trait("consumeable"):
                pretext = "Activate"
                action = "a"
                show = True
            if create == True:
                if show:
                    button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((entity_button_offset_from_left, entity_button_offset_from_top),
                                                  (entity_button_width, entity_button_height)),
                        text=pretext,
                        manager=self.uiManager)
                    button.action = action

                buttons_drawn += 1

                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left + (entity_button_width + entity_button_offset_from_each_other) * buttons_drawn, entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text='Drop',
                    manager=self.uiManager)
                button.action = "d"

                buttons_drawn += 1


        entity_text = ""
        if entity.has_trait("item"):
            item = entity
            if entity.has_trait("equipment"):
                if item.equipped:
                    entity_text += "Currently equipped<br>"
                if item.cursed:
                    entity_text += "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>" + "Once equipped, it cannot be taken off" +  "</font></shadow><br>"
                entity_text += "Equipment type: " + item.equipment_type + "<br>"
                if item.required_strength >= 0:
                    if player.character.get_strength() < item.required_strength:
                        req_str_text = "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>Required Strength: " + str(item.required_strength) + "(Unequippable) </font></shadow><br>"
                    else:
                        req_str_text = "Required Strength: " + str(item.required_strength) + "<br>"
                    entity_text += req_str_text
                if item.has_trait("weapon"):
                    entity_text += "Damage: " + str(item.damage_min + player.fighter.get_base_damage()) + " - " + str(item.damage_max + player.fighter.get_base_damage()) + "<br>"
                    if item.on_hit:
                        entity_text += "On hit: " + item.on_hit_description + "<br>"

                stats = item.stats.GetStatsForLevel(item.level)
                if stats[2]> 0:
                    entity_text += "Intelligence: +" + str(stats[2]) + "<br>"
                elif stats[2]<0:
                    entity_text += "Intelligence: " + str(stats[2]) + "<br>"
                if stats[0] > 0:
                    entity_text += "Strength: +" + str(stats[0]) + "<br>"
                elif stats[0]<0:
                    entity_text += "Strength: " + str(stats[0]) + "<br>"
                if stats[1] > 0:
                    entity_text += "Dexterity: +" + str(stats[1]) + "<br>"
                elif stats[1]<0:
                    entity_text += "Dexterity: " + str(stats[1]) + "<br>"
                if stats[3] > 0:
                    entity_text += "Endurance: +" + str(stats[3]) + "<br>"
                elif stats[3]<0:
                    entity_text += "Endurance: " + str(stats[3]) + "<br>"
                if stats[4] > 0:
                    entity_text += "Armor: +" + str(stats[4]) + "<br>"
                elif stats[4]<0:
                    entity_text += "Armor: " + str(stats[4]) + "<br>"
            elif entity.has_trait("potion") or entity.has_trait("ring"):
                entity_text += "Effect: " + str(entity.action_description) + "<br>"
            if item.attached_skill_exists:
                entity_text += "Grants skill: " + item.get_attached_skill_description() + "<br>"

        elif entity.has_trait("monster"):
            entity_text += "Health: " + str(entity.character.get_health()) + " / " + str(entity.character.get_max_health()) + "<br>"
            entity_text += "Attack: " + str(entity.fighter.get_damage_min()) + " - " + str(entity.fighter.get_damage_max()) + "<br>"
            entity_text += "Armor: " + str(entity.character.attributes.get_armor()) + "<br>"
            for skill in entity.character.skills:
                entity_text += "Has skill: " + str(skill.name)+ "<br>"
            if entity.has_trait("orb"):
                entity_text += "It's very round.<br>"
                for i, skill in enumerate(entity.character.skills):
                    if i == 0:
                        entity_text += "Skills: "
                    entity_text += skill.description()
                    if i < len(entity.character.skills) - 1:
                        entity_text += ", "

        elif entity.has_trait("interactable"):
            pass

        entity_text += "<br>" + entity.description

        if create == True:
            text_box = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
                html_text = entity_text,
                manager=self.uiManager)

        self.uiManager.draw_ui(self.win)

    def update_questpopup_screen(self, loop, message):
        pygame.draw.rect(self.win, UIColors.BLACK,
                         pygame.Rect(0, 0, UILayout.QUEST_POPUP_WIDTH, UILayout.QUEST_POPUP_HEIGHT))
        font = pygame.font.SysFont("Arial", UILayout.FONT_SIZE_TITLE)
        text = font.render(message, True, UIColors.WHITE)
        self.win.blit(text, (UILayout.QUEST_POPUP_TEXT_OFFSET, UILayout.QUEST_POPUP_TEXT_OFFSET))

    #First draws the tiles, then darkens the ones that are out of range
    def draw_single_tile(self, loop, tile):
        if tile.get_visible() or tile.get_seen():
            tag = loop.tileDict.tile_string(tile.get_render_tag())
            self.win.blit(tag, (self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)))
            if loop.generator.interact_map.get_has_entity(tile.get_x(), tile.get_y()):
                entity = loop.generator.interact_map.get_entity(tile.get_x(), tile.get_y())
                print(entity.get_render_tag())
                tag = loop.tileDict.tile_string(entity.get_render_tag())
                self.win.blit(tag, (self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)))
            for terrain in tile.get_terrain():
                terrain_tag = loop.tileDict.tile_string(terrain.get_render_tag())
                self.win.blit(terrain_tag, (self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)))
        if tile.get_seen() and not tile.get_visible() or (loop._current_loop_type == LoopType.targeting and
                                                                loop.targets.get_range() is not None and
                                                                tile.get_distance(
                                                                    loop.targets.get_origin_range_coordinates()[0],
                                                                    loop.targets.get_origin_range_coordinates()[
                                                                        1]) > loop.targets.get_range()):
            fog_img = pygame.Surface((UILayout.FOG_TILE_SIZE, UILayout.FOG_TILE_SIZE))
            fog_img.fill(UIColors.FOG_MULT)
            self.win.blit(fog_img, (
            self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)),
                          special_flags=pygame.BLEND_RGB_MULT)

    def update_examine(self, target, loop):
        x, y = target
        tag = loop.tileDict.tile_string(UITileIDs.TARGETING_CURSOR)
        self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def draw_context_help(self, loop_type):
        """Draw contextual help bar at bottom of screen showing available actions."""
        loop_name = loop_type.name if hasattr(loop_type, 'name') else str(loop_type)
        help_text = HelpText.get_help_for_state(loop_name)
        if help_text:
            draw_help_bar(
                self.win,
                help_text,
                self.screen_width,
                self.screen_height,
                bar_height=UILayout.HELP_BAR_HEIGHT,
                padding=UILayout.HELP_BAR_PADDING,
                bg_color=UIColors.HELP_BAR_BG,
                text_color=UIColors.HELP_BAR_TEXT,
                font_size=UILayout.HELP_BAR_FONT_SIZE
            )

    def update_ui(self):
        deltaTime = self.clock.tick() / 1000
        self.uiManager.update(deltaTime)

    def update_screen(self, loop):
        self.win.fill(UIColors.BLACK)
        self.uiManager.draw_ui(self.win)

    def update_screen_without_fill(self, loop):
        self.uiManager.draw_ui(self.win)




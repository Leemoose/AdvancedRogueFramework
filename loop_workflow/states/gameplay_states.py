"""
Core gameplay states: action, targeting, examine.

These states handle the main gameplay loop where the player moves,
attacks, and interacts with the world.
"""

from logging_config import get_logger
from ..game_states import GameState
from ..looptype import LoopType
from ..input_actions import (
    get_direction,
    get_action_screen_change,
    is_quick_cast_key,
    get_skill_index,
)
from display_generation import create_display
from navigation_utility import shadowcasting
import pygame

logger = get_logger(__name__)


class ActionState(GameState):
    """
    Main gameplay state where the player moves and takes actions.

    This is the primary game state. The player can:
        - Move and attack with direction keys
        - Open inventory, equipment, spells with hotkeys
        - Interact with objects and NPCs
        - Use quick-cast spells
    """

    loop_type = LoopType.action

    def create_display(self, display):
        create_display(display, self.loop)

    def update_display(self, display):
        self._cleanup_dead_entities()
        shadowcasting.compute_fov(self.loop)
        self._update_mouse_target(display)
        display.update_display(self.loop)

    def handle_input(self, key):
        player = self.loop.player

        # Movement and attack
        direction = get_direction(key)
        if direction:
            player.attack_move(*direction, self.loop)
            return True

        # Screen changes (inventory, equipment, spells, etc.)
        screen_change = get_action_screen_change(key)
        if screen_change:
            self._handle_screen_change(screen_change, player)
            return True

        # Quick cast spells (1-8)
        if is_quick_cast_key(key):
            self._handle_quick_cast(player, key)
            return True

        # Other actions
        return self._handle_action_key(key, player)

    def _handle_screen_change(self, screen_change, player):
        """Process screen change requests from hotkeys."""
        loop_type, inventory_filter = screen_change
        if inventory_filter:
            if inventory_filter == "main":
                player.inventory.change_active_inventory("main")
            else:
                player.inventory.change_limit_inventory(inventory_filter)
        self._change_state(loop_type)

    def _handle_quick_cast(self, player, key):
        """Handle quick-casting a spell from the hotbar."""
        skill_num = get_skill_index(key)
        if skill_num >= len(player.mage.quick_cast_spells):
            return
        if player.mage.quick_cast_spells[skill_num] is None:
            return

        self.loop.targets.set_target_range(
            player.get_location(),
            player.fighter.get_range()
        )
        self.loop.targets.set_queued_action(
            player.mage.known_spells[skill_num].activate
        )
        self.loop.start_targetting()

    def _handle_action_key(self, key, player):
        """Handle non-movement action keys."""
        if key == "g":
            self._try_grab_item(player)
        elif key == "f":
            self._start_attack_targeting(player)
        elif key == "l":
            if player.stat_points > 0:
                self._change_state(LoopType.level_up)
        elif key == "s":
            self._handle_find_stairs(player)
        elif key == ">":
            player.down_stairs(self.loop)
        elif key == "<":
            player.up_stairs(self.loop)
        elif key == ".":
            player.character.wait()
            self.loop.add_message("The player waits.")
        elif key == "x":
            self._start_examine_mode(player)
        elif key == "o":
            self._handle_autoexplore(player)
        elif key == "t":
            player.do_interact(self.loop)
        elif key == "z":
            self.loop.after_rest = LoopType.action
            self._change_state(LoopType.resting)
        elif key == "tab":
            player.smart_attack(self.loop)
        return True

    def _try_grab_item(self, player):
        """Try to grab an item at the player's location."""
        for item in self.loop.generator.item_map.get_all_entities():
            if item.x == player.x and item.y == player.y:
                player.do_grab(item, self.loop)
                break

    def _start_attack_targeting(self, player):
        """Enter targeting mode for a ranged attack."""
        self.loop.targets.set_target_range(
            player.get_location(),
            player.fighter.get_range()
        )
        self.loop.targets.set_queued_action(player.attack)
        self.loop.start_targetting()

    def _handle_find_stairs(self, player):
        """Auto-path to stairs if found."""
        player.find_stairs(self.loop)
        if player.path:
            self._change_state(LoopType.pathing)

    def _start_examine_mode(self, player):
        """Enter examine mode centered on the player."""
        self._change_state(LoopType.examine)
        self.loop.targets.set_target(player.get_location())
        self.loop.set_target(player.get_location())
        self.loop.update_screen = True

    def _handle_autoexplore(self, player):
        """Start auto-exploration if a path is found."""
        player.autoexplore(self.loop)
        if player.path:
            self._change_state(LoopType.pathing)

    def _cleanup_dead_entities(self):
        """Remove destroyed items and dead monsters, drop their loot."""
        self.loop.clean_up()

    def _update_mouse_target(self, display):
        """Update the target based on mouse position."""
        mos_x, mos_y = pygame.mouse.get_pos()
        x, y = display.screen_to_tile(self.loop.player, mos_x, mos_y)
        self.loop.targets.set_target((x, y))

    def on_enter(self):
        """Reset pathing state when entering action mode."""
        super().on_enter()
        if self.loop.pathing_count != 0:
            logger.debug("Explored for %d turns", self.loop.pathing_count)
            self.loop.pathing_count = 0
            self.loop.after_pathing = lambda loop: loop.change_loop(LoopType.action)
            self.loop.player.path = []


class TargetingState(GameState):
    """
    State for selecting a target for an action (spell, ranged attack).

    The player uses direction keys to move the targeting cursor and
    Enter to confirm the target.
    """

    loop_type = LoopType.targeting

    def create_display(self, display):
        create_display(display, self.loop)

    def update_display(self, display):
        display.update_display(self.loop)
        display.update_examine(
            self.loop.targets.get_target_coordinates(),
            self.loop
        )

    def handle_input(self, key):
        targets = self.loop.targets

        direction = get_direction(key)
        if direction:
            targets.adjust(*direction)
            return True

        if key == "esc":
            self._cancel_targeting()
        elif key == "return":
            self._confirm_target()

        return True

    def _cancel_targeting(self):
        """Cancel targeting and return to action."""
        self.loop.targets.void_skill()
        self.loop.player.inventory.ready_scroll = None
        self._change_state(LoopType.action)

    def _confirm_target(self):
        """Confirm the current target and execute the queued action."""
        targets = self.loop.targets
        if targets.get_has_queued_action() is not None:
            targets.use_queued_action(self.loop)
        targets.void_skill()
        self._change_state(LoopType.action)


class ExamineState(GameState):
    """
    State for examining the map without taking actions.

    The player can move a cursor around to see information about
    tiles, monsters, and items.
    """

    loop_type = LoopType.examine

    def create_display(self, display):
        create_display(display, self.loop)

    def update_display(self, display):
        display.update_display(self.loop)
        display.update_examine(
            self.loop.targets.get_target_coordinates(),
            self.loop
        )

    def handle_input(self, key):
        targets = self.loop.targets

        direction = get_direction(key)
        if direction:
            targets.adjust(*direction)
            return True

        if key == "esc":
            targets.void_skill()
            self._change_state(LoopType.action)
        elif key == "return":
            self._change_state(LoopType.specific_examine)

        return True


class SpecificExamineState(GameState):
    """
    State for examining a specific entity in detail.

    Shows detailed information about a monster, item, or tile.
    """

    loop_type = LoopType.specific_examine

    def create_display(self, display):
        display.update_entity(self.loop, item_screen=False, create=True)

    def update_display(self, display):
        display.update_entity(self.loop, item_screen=False, create=True)

    def handle_input(self, key):
        if key == "esc":
            self._change_state(LoopType.examine)
        return True

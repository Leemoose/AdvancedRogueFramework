"""
Game Loop Controller.

The Loops class serves as the central coordinator for the game, managing:
    - State transitions between different game screens
    - Event processing (keyboard, mouse, window events)
    - Game time and monster AI updates
    - Player death and victory conditions

The actual state-specific logic (display, input handling) is delegated to
GameState subclasses via the StateManager.

Classes:
    Loops: Main game controller coordinating states and game logic
"""

from logging_config import get_logger

import item_implementation
from dungeon_generation import mapping as M
from dungeon_generation.configuration_data.gateway_data import GatewayData
import player
from navigation_utility import shadowcasting
from loop_workflow import MessageHandler, targets as T
from src.core.enums import LoopType  # Moved from loop_workflow to break circular imports
from loop_workflow.memory import Memory
from loop_workflow.game_states import StateManager
from loop_workflow.states import create_all_states
from src.core.constants import GameTime

from display_generation import *

import pygame
import pygame_gui

logger = get_logger(__name__)


class Loops:
    """
    Central game controller coordinating states and game logic.

    The Loops class is responsible for:
        - Managing the state machine via StateManager
        - Processing pygame events and dispatching to states
        - Running the monster AI loop
        - Tracking game time and status effects
        - Handling floor transitions
        - Managing game save/load

    Attributes:
        display: The Display instance for rendering
        state_manager: StateManager coordinating game states
        memory: Memory instance for save/load
        player: The player entity
        generator: Current dungeon floor generator
    """

    def __init__(self, tileDict, display, keyboard, dungeon_data):
        logger.debug("Initializing Loops")

        # Core references
        self.display = display
        self.tileDict = tileDict
        self.dungeon_data = dungeon_data
        self.keyboard = keyboard

        # Game state
        self.memory = Memory()
        self.generator = None
        self.messages = MessageHandler()
        # Use config values for initial position (-1,-1 means spawn at valid location later)
        from src.core.player_config import PlayerConfig
        self.player = player.Player(PlayerConfig.STARTING_X, PlayerConfig.STARTING_Y)
        self.targets = T.Target(self)

        # State management
        self.state_manager = StateManager(self)
        self._current_loop_type = LoopType.none
        self.update_screen = True

        # Level up state
        self.current_stat = 0
        self.current_spell = None

        # Time tracking
        self.timer = 0
        self.total_time = 0
        self.daytime = True  # True = day, False = night

        self.tide_level = -50  # Start at medium tide
        self.tide_direction = 1  # Start rising toward high tide

        # Quest state
        self.quest_recieved = False
        self.quest_completed = False

        # NPC interaction state
        self.next_dialogue = False
        self.dialogue_options = 0
        self.player_choice = -1
        self.npc_focus = None

        # Pathing and resting state
        self.rest_count = 0
        self.pathing_count = 0
        self.after_pathing = lambda x: False
        self.after_rest = None

        # Register all states
        self.state_manager.register_states(create_all_states(self))

        logger.debug("Loops initialization complete")

    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================

    def change_loop(self, new_loop):
        """
        Change to a new game state.

        Args:
            new_loop: LoopType enum of the target state
        """
        logger.debug("Changing loop from %s to %s", self._current_loop_type, new_loop)

        self._current_loop_type = new_loop
        self.update_screen = True

        self.state_manager.change_state(new_loop)
        self.state_manager.create_display(self.display)

    # =========================================================================
    # MAIN GAME LOOP
    # =========================================================================

    def action_loop(self, keyboard, display):
        """
        Main game loop iteration.

        This method:
            1. Processes pygame events (quit, keyboard, mouse, resize)
            2. Dispatches input to the current state
            3. Runs automated state updates (resting, pathing)
            4. Processes game time and monster AI
            5. Checks for player death

        Args:
            keyboard: Keyboard handler for input
            display: Display instance for rendering

        Returns:
            bool: False to quit the game, True to continue
        """
        logger.debug("Entering action_loop, state=%s", self._current_loop_type)

        # Process pygame events
        if not self._process_events(keyboard, display):
            return False

        # Process queued keyboard input
        if not self._process_keyboard_queue(keyboard):
            return False

        # Run state-specific tick (for automated states)
        self._run_state_tick()

        # Process game time and monster AI
        self._process_game_time()

        # Check for player death
        self._check_player_death()

        # Update display clock
        display.update_ui()
        logger.debug("Exiting action_loop")
        return True

    def _process_events(self, keyboard, display):
        """
        Process pygame events.

        Returns:
            bool: False if quit event received, True otherwise
        """
        events = pygame.event.get()

        if events:
            for event in events:
                if not self._handle_event(event, keyboard, display):
                    return False
        else:
            # No events - check for held movement keys
            keys = pygame.key.get_pressed()
            keyboard.set_continous_movement_keys(keys)

        return True

    def _handle_event(self, event, keyboard, display):
        """
        Handle a single pygame event.

        Returns:
            bool: False for quit event, True otherwise
        """
        if event.type == pygame.QUIT:
            logger.info("Quit event received")
            return False

        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event, keyboard)

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            self._handle_button_press(event, keyboard)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_click(event, keyboard, display)

        elif event.type == pygame.VIDEORESIZE:
            self._handle_resize()

        display.uiManager.process_events(event)
        return True

    def _handle_keydown(self, event, keyboard):
        """Process keyboard key press."""
        if event.mod == pygame.KMOD_NONE:
            keyboard.set_next_key(keyboard.get_key_binding(event.key, False))
        elif event.mod & pygame.KMOD_SHIFT and event.key:
            keyboard.set_next_key(keyboard.get_key_binding(event.key, True))

    def _handle_button_press(self, event, keyboard):
        """Process UI button press."""
        if hasattr(event.ui_element, "action"):
            if hasattr(event.ui_element, "row") and event.ui_element.row is not None:
                self.current_stat = event.ui_element.row
            keyboard.set_next_key(event.ui_element.action)

    def _handle_mouse_click(self, event, keyboard, display):
        """Process mouse click."""
        x, y = pygame.mouse.get_pos()
        x_tile, y_tile = display.screen_to_tile(self.player, x, y)

        if self._current_loop_type == LoopType.action:
            keyboard.set_next_key(keyboard.get_key_from_mouse(self, x_tile, y_tile))
        elif self._current_loop_type == LoopType.targeting:
            keyboard.targetting_mouse_to_keyboard(self, x_tile, y_tile)

    def _handle_resize(self):
        """Handle window resize event."""
        self.display.update_sizes()
        self.update_screen = True
        self.change_loop(self._current_loop_type)

    def _process_keyboard_queue(self, keyboard):
        """
        Process queued keyboard input.

        Returns:
            bool: False if input handler requests quit, True otherwise
        """
        while keyboard.get_has_queue():
            key = keyboard.get_next_key()
            if key is not None:
                result = self.state_manager.handle_input(key)
                if result is False:
                    return False
            self.update_screen = True

        return True

    def _run_state_tick(self):
        """Run state-specific tick for automated states."""
        self.state_manager.tick()

    def _process_game_time(self):
        """Process game time, energy, and monster AI."""
        if self.player.character.energy < 0:
            energy_spent = -self.player.character.energy
            self.time_passes(energy_spent)
            self.monster_loop(energy_spent)
            self.player.character.energy = 0

    def _check_player_death(self):
        """Check if player has died and transition to death screen."""
        is_alive = self.player.character.is_alive()
        is_invincible = self.player.character.status.get_invincible()

        if not is_alive and not is_invincible:
            if self._current_loop_type != LoopType.death:
                logger.info("Player has died, changing to death loop")
                self.change_loop(LoopType.death)

    # =========================================================================
    # RENDERING
    # =========================================================================

    def render_screen(self, display):
        """
        Render the current game state.

        Delegates rendering to the current state via StateManager.
        Also handles quest popup notifications.
        """
        self.state_manager.update_display(display)

        # Quest received popup
        if self.player.quest_recieved:
            quest_name = self.player.quests[-1].name
            display.update_questpopup_screen(self, f"{quest_name} Recieved")
            self.player.quest_recieved = False

        pygame.display.update()
        self.update_screen = False

    # =========================================================================
    # GAME LOGIC
    # =========================================================================

    def monster_loop(self, energy):
        """
        Process monster AI for all active monsters.

        Args:
            energy: Amount of energy to give to monsters
        """
        logger.debug("Entering monster_loop with energy=%d", energy)

        for monster in self.generator.monster_map.get_all_entities():
            if not monster.character.is_alive():
                continue

            if monster.get_is_awake():
                monster.character.energy += energy
                while monster.character.energy > 0:
                    monster.brain.rank_actions(self)
            elif self.generator.tile_map.get_seen(monster.x, monster.y):
                monster.character.status.set_awake(True)

        logger.debug("Exiting monster_loop")

    def clean_up(self):
        """Remove destroyed items and dead monsters, drop their loot."""
        self._cleanup_destroyed_items()
        self._cleanup_dead_monsters()

    def _cleanup_destroyed_items(self):
        """Remove items marked for destruction."""
        destroyed = [
            item for item in self.generator.item_map.get_all_entities()
            if item.destroy
        ]
        for item in destroyed:
            self.generator.item_map.remove_thing(item)

    def _cleanup_dead_monsters(self):
        """Remove dead monsters and drop their items/gold."""
        dead = [
            monster for monster in self.generator.monster_map.get_all_entities()
            if not monster.character.is_alive()
        ]

        for monster in dead:
            # Drop gold
            if monster.inventory.get_gold() > 0:
                gold = item_implementation.Gold(
                    monster.inventory.get_gold(),
                    x=monster.get_x(),
                    y=monster.get_y()
                )
                self.generator.item_map.place_thing(gold)

            # Drop items
            for item in monster.get_inventory():
                if item.equipped:
                    monster.character.unequip(item)
                monster.do_drop(item, self.generator.item_map)

            self.generator.monster_map.remove_thing(monster)

    def time_passes(self, time):
        """
        Process game time passage.

        Handles status effects, cooldowns, regeneration, quests,
        terrain effects, day/night cycles, and ocean tides.

        Args:
            time: Amount of time (in energy units) that has passed
        """
        self.timer += time

        for _ in range(int(self.timer // GameTime.ENERGY_PER_TURN)):
            self.total_time += 1
            self.player.statistics.add_turn_details()

            # Check for day/night transition (every 50 turns)
            if self.total_time % 50 == 0:
                self._toggle_daytime()

            # Update tide gradually in Ocean (every turn)
            if self.get_branch() == "Ocean":
                self._update_tide()

            # Player updates
            self.player.character.tick_all_status_effects(self)
            self.player.mage.tick_cooldowns()

            # Disable regen in Forest (per old game behavior)
            if self.get_branch() != "Forest":
                self.player.character.tick_regen()

            # Quest updates
            for quest in self.player.quests:
                quest.check_for_progress(self)

            # Player terrain effects
            player_tile = self.generator.tile_map.get_entity(
                self.player.x, self.player.y
            )
            if player_tile.has_terrain():
                player_tile.apply_terrain_effects(self.player)

            # Monster updates
            for monster in self.generator.monster_map.get_all_entities():
                monster.character.tick_all_status_effects(self)
                monster.character.tick_cooldowns()
                monster.character.tick_regen()

                monster_tile = self.generator.tile_map.get_entity(
                    monster.get_x(), monster.get_y()
                )
                if monster_tile.has_terrain():
                    monster_tile.apply_terrain_effects(monster)

        self.timer = self.timer % GameTime.ENERGY_PER_TURN

    def _toggle_daytime(self):
        """Toggle between day and night, affecting Forest monsters."""
        self.daytime = not self.daytime
        time_name = "day" if self.daytime else "night"
        self.add_message(f"The {time_name} has come.")

        if self.get_branch() == "Forest":
            self._apply_daytime_to_monsters()

    def _apply_daytime_to_monsters(self):
        """Apply day/night effects to all monsters on current floor."""
        for monster in self.generator.monster_map.get_all_entities():
            if self.daytime:
                monster.dayify()
            else:
                monster.nightify()

    def _update_tide(self):
        """
        Update tide level in Ocean.

        Tide oscillates between 0 (low) and 50 (high).
        Water coverage is determined by comparing tide_level to tile elevations.
        """
        # Update tide level
        self.tide_level += self.tide_direction

        # Reverse direction at extremes
        if self.tide_level >= -5:
            self.tide_level = -5
            self.tide_direction = -1
        elif self.tide_level <= -35:
            self.tide_level = -35
            self.tide_direction = 1

        # Apply water based on current tide level
        self.generator.tile_map.apply_tide(self.tide_level)

    def is_daytime(self):
        """Return True if it's daytime, False if nighttime."""
        return self.daytime

    def get_tide_level(self):
        """Return current tide level (0-50)."""
        return self.tide_level

    # =========================================================================
    # FLOOR TRANSITIONS
    # =========================================================================

    def change_floor(self, level_change = -1, random_location = False):
        """Handle player moving between dungeon floors via stairs."""
        logger.debug("Entering change_floor")

        # Process any pending energy
        if self.player.character.energy < 0:
            energy_spent = -self.player.character.energy
            self.time_passes(energy_spent)
            self.monster_loop(energy_spent)
            self.player.character.energy = 0

        playerx, playery = self.player.get_location()
        logger.debug("Player at stairs position (%d, %d)", playerx, playery)

        if not random_location:
            current_stairs = self.generator.tile_map.get_entity(playerx, playery)
            level_change = current_stairs.get_level_change()
            if not current_stairs.has_trait("stairs"):
                return

        # Calculate new level
        new_level = self.get_depth() + level_change

        # Block leaving the dungeon via up stairs on floor 1
        if new_level < 1:
            self.add_message("You can't leave the dungeon yet.")
            return

        new_generator = self.memory.get_saved_floor(self.get_branch(), new_level)

        if random_location:
            self.player.x, self.player.y = new_generator.get_tile_map().get_random_location()
        else:
        # Pair stairs if not already paired
            if not current_stairs.get_has_paired_stairs():
                for other_stairs in new_generator.tile_map.get_stairs():
                    is_unpaired = not other_stairs.get_has_paired_stairs()
                    is_opposite = other_stairs.get_level_change() != current_stairs.get_level_change()
                    if is_unpaired and is_opposite:
                        current_stairs.pair_stairs(other_stairs)
                        break

            # Move player to new floor
            self.player.x, self.player.y = current_stairs.get_paired_stairs().get_location()
        self.player.visited_stairs = []
        self.generator = new_generator

        # Apply day/night effects when changing floors in Forest
        if self.get_branch() == "Forest":
            self._apply_daytime_to_monsters()

        # Apply tide when changing floors in Ocean
        if self.get_branch() == "Ocean":
            self.generator.tile_map.apply_tide(self.tide_level)

        logger.info("Changed to floor %d in branch %s", new_level, self.get_branch())
        logger.debug("Exiting change_floor")

    def change_branch(self):
        """Handle player moving between dungeon branches via gateways."""
        logger.debug("Entering change_branch")

        # Process any pending energy
        if self.player.character.energy < 0:
            energy_spent = -self.player.character.energy
            self.time_passes(energy_spent)
            self.monster_loop(energy_spent)
            self.player.character.energy = 0

        playerx, playery = self.player.get_location()
        logger.debug("Player at gateway position (%d, %d)", playerx, playery)

        current_gateway = self.generator.tile_map.get_entity(playerx, playery)
        if not current_gateway.has_trait("gateway"):
            logger.warning("change_branch called but player not on gateway")
            return

        if not current_gateway.has_outgoing():
            logger.warning("Gateway has no outgoing connection")
            self.add_message("This gateway leads nowhere!")
            return

        # Get destination from the paired gateway
        dest_gateway = current_gateway.outgoing
        dest_branch = dest_gateway.get_branch()
        dest_depth = dest_gateway.get_depth()

        logger.info("Traveling through gateway from %s:%d to %s:%d",
                   self.get_branch(), self.get_depth(), dest_branch, dest_depth)

        # Move player to destination gateway location
        self.player.x, self.player.y = dest_gateway.get_location()
        self.player.visited_stairs = []

        # Update generator to destination floor
        self.generator = self.memory.get_saved_floor(dest_branch, dest_depth)

        # Update memory state
        self.memory.floor_level = dest_depth
        self.memory.branch = dest_branch

        self.add_message(f"You travel through the gateway to {dest_branch}.")

        # Apply day/night effects when entering Forest
        if dest_branch == "Forest":
            self._apply_daytime_to_monsters()

        # Apply tide when entering Ocean
        if dest_branch == "Ocean":
            self.generator.tile_map.apply_tide(self.tide_level)

        logger.info("Changed to branch %s floor %d", dest_branch, dest_depth)
        logger.debug("Exiting change_branch")

    # =========================================================================
    # GAME INITIALIZATION
    # =========================================================================

    def init_game(self):
        """Initialize a new game, generating all dungeon floors."""
        logger.info("Initializing game")

        # Create gateway data configuration
        self.gateway_data = GatewayData()

        # Generate all floors for all branches
        for branch in self.dungeon_data.get_branches():
            for level in range(1, self.dungeon_data.get_depth(branch) + 1):
                generator = M.DungeonGenerator(
                    level, self.player, branch, self.dungeon_data,
                    gateway_data=self.gateway_data
                )
                self.memory.set_floor(branch, level, generator)

        # Pair all gateways after all floors are generated
        self._pair_all_gateways()

        # Set initial memory state (player starts in Hub floor 1 for testing)
        self.memory.set_memory(1, "Hub", self.player, self.keyboard)
        self.generator = self.memory.get_current_saved_floor()

        # Position player at a gateway in Hub (or fallback to stairs)
        placed = False
        for gateway in self.generator.tile_map.get_gateway():
            x, y = gateway.get_location()
            self.player.x = x
            self.player.y = y
            self.targets.set_target((x, y))
            placed = True
            break

        if not placed:
            for stairs in self.generator.tile_map.get_stairs():
                if stairs.get_level_change() == -1:
                    x, y = stairs.get_location()
                    self.player.x = x
                    self.player.y = y
                    self.targets.set_target((x, y))
                    break

        logger.info("Game initialization complete")

    def _pair_all_gateways(self):
        """
        Pair all gateways based on gateway_data configuration.

        This creates the actual connections between gateway tiles on different floors.
        Must be called after all floors are generated.

        For one-way connections (like Hub -> branches), we create a "virtual" destination
        by using the up-stairs location on the destination floor as the arrival point.
        """
        logger.info("Pairing all gateways")

        # Get all lairs that have gateways
        gateway_lairs = self.gateway_data.get_all_gateway_lairs()

        for lair in gateway_lairs:
            source_branch = lair.branch
            source_depth = lair.depth

            # Check if this branch/depth exists in our generators
            if source_branch not in self.memory.generators:
                logger.warning("Branch %s not found in generators", source_branch)
                continue
            if source_depth not in self.memory.generators[source_branch]:
                logger.warning("Depth %d not found in branch %s", source_depth, source_branch)
                continue

            source_generator = self.memory.generators[source_branch][source_depth]
            source_gateways = list(source_generator.tile_map.get_gateway())

            # Get destinations for this lair
            destinations = self.gateway_data.get_destinations(source_branch, source_depth)

            # Match gateways to destinations
            gateway_index = 0
            for dest in destinations:
                dest_branch = dest.branch
                dest_depth = dest.depth

                # Check if destination exists
                if dest_branch not in self.memory.generators:
                    logger.warning("Destination branch %s not found", dest_branch)
                    continue
                if dest_depth not in self.memory.generators[dest_branch]:
                    logger.warning("Destination depth %d not found in branch %s", dest_depth, dest_branch)
                    continue

                # Find unpaired source gateway
                if gateway_index >= len(source_gateways):
                    logger.warning("Not enough gateways at %s:%d for all destinations",
                                 source_branch, source_depth)
                    break

                source_gateway = source_gateways[gateway_index]

                # Skip if this gateway is already paired
                if source_gateway.has_outgoing():
                    gateway_index += 1
                    continue

                dest_generator = self.memory.generators[dest_branch][dest_depth]
                dest_gateways = dest_generator.tile_map.get_gateway()

                # Try to find an unpaired gateway at destination
                dest_gateway = None
                for g in dest_gateways:
                    if not g.has_incoming():
                        dest_gateway = g
                        break

                if dest_gateway is None:
                    # No gateway at destination - create a virtual gateway at stairs location
                    # This handles one-way connections where destination doesn't have a return gateway
                    from dungeon_generation.tiles import Gateway

                    # Find up-stairs to use as arrival point
                    arrival_x, arrival_y = None, None
                    for stairs in dest_generator.tile_map.get_stairs():
                        if stairs.get_level_change() == -1:  # Up stairs
                            arrival_x, arrival_y = stairs.get_location()
                            break

                    # Fallback to any passable location
                    if arrival_x is None:
                        arrival_x, arrival_y = dest_generator.get_random_passable_location()

                    # Create virtual gateway (just for the destination point)
                    dest_gateway = Gateway(arrival_x, arrival_y, level=dest_depth, branch=dest_branch)
                    dest_generator.tile_map.gateway.append(dest_gateway)
                    logger.debug("Created virtual gateway at %s:%d (%d, %d)",
                               dest_branch, dest_depth, arrival_x, arrival_y)

                # Pair the gateways (one-way: source.outgoing -> dest)
                source_gateway.pair_gateway(dest_gateway)
                logger.info("Paired gateway: %s:%d -> %s:%d",
                           source_branch, source_depth, dest_branch, dest_depth)

                gateway_index += 1

        logger.info("Gateway pairing complete")

    def load_game(self):
        """Load a saved game."""
        logger.info("Loading game")

        self.memory.load_objects()
        self.update_screen = False
        self.generator = self.memory.get_current_saved_floor()
        self.player = self.memory.player
        self.player.character.energy = 0
        self.change_loop(LoopType.action)

        logger.info("Game loaded successfully")

    def clear_data(self):
        """Clear game data and reset to initial state."""
        logger.info("Clearing game data")

        self.change_loop(LoopType.main)
        self.update_screen = True
        self.memory = Memory()
        self.generator = None
        self.messages.clear_message()

    # =========================================================================
    # TARGETING HELPERS
    # =========================================================================

    def start_targetting(self, start_on_player=False):
        """
        Enter targeting mode for selecting a target.

        Args:
            start_on_player: If True, start cursor on player; otherwise on nearest monster
        """
        logger.debug("Starting targeting mode, start_on_player=%s", start_on_player)

        self.change_loop(LoopType.targeting)

        # Determine starting target
        if start_on_player:
            target = self.player
        else:
            from loop_workflow.loop_utility import get_closest_monster
            closest = get_closest_monster(self)
            origin = self.targets.get_origin_range_coordinates()
            max_range = self.targets.get_range()

            if max_range is not None and closest.get_distance(origin[0], origin[1]) > max_range:
                target = self.player
            else:
                target = closest

        self.targets.set_target(target.get_location())

    # =========================================================================
    # PASSTHROUGH METHODS
    # =========================================================================

    def get_branch(self):
        """Get current dungeon branch."""
        return self.generator.get_branch()

    def get_depth(self):
        """Get current dungeon depth."""
        return self.generator.get_depth()

    def get_width(self):
        """Get dungeon width."""
        return self.generator.get_width()

    def get_height(self):
        """Get dungeon height."""
        return self.generator.get_height()

    def add_message(self, message, color=(255, 255, 255)):
        """Add a message to the message log."""
        self.messages.add_message(message, color)

    def clear_message(self):
        """Clear all messages."""
        self.messages.clear_message()

    def set_target(self, target):
        """Set the current target."""
        self.targets.set_target(target)

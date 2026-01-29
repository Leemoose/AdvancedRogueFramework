"""
Game State Pattern Implementation.

This module implements a State pattern for the game loop system. Each game state
(action, inventory, targeting, etc.) is encapsulated in its own class with clear
responsibilities for:
    - Creating/initializing the display for that state
    - Updating/rendering the display each frame
    - Handling keyboard/mouse input

The StateManager coordinates state transitions and delegates to the current state.

Design principles:
    - Single Responsibility: Each state handles only its own logic
    - Open/Closed: New states can be added without modifying existing code
    - Dependency Inversion: States depend on abstractions (GameState), not concrete classes
"""

from abc import ABC, abstractmethod
from logging_config import get_logger
from .looptype import LoopType

logger = get_logger(__name__)


# =============================================================================
# ABSTRACT BASE CLASS
# =============================================================================

class GameState(ABC):
    """
    Abstract base class for all game states.

    Each state must implement:
        - create_display: Set up UI elements when entering the state
        - update_display: Render the state each frame
        - handle_input: Process keyboard/mouse input

    States can optionally override:
        - on_enter: Called when transitioning into this state
        - on_exit: Called when transitioning out of this state
        - tick: Called each frame for state-specific updates (e.g., auto-rest)
    """

    loop_type: LoopType = LoopType.none

    def __init__(self, loop):
        """
        Initialize state with reference to the main loop controller.

        Args:
            loop: The Loops instance that coordinates game state
        """
        self.loop = loop

    @abstractmethod
    def create_display(self, display):
        """
        Set up UI elements when entering this state.
        Called once when the state becomes active.
        """
        pass

    @abstractmethod
    def update_display(self, display):
        """
        Render the state each frame.
        Called every frame while this state is active.
        """
        pass

    @abstractmethod
    def handle_input(self, key):
        """
        Process keyboard input.

        Args:
            key: The key string from the keyboard handler

        Returns:
            bool: False to quit the game, True to continue
        """
        pass

    def on_enter(self):
        """Called when transitioning into this state. Override for setup logic."""
        logger.debug("Entering state: %s", self.loop_type)

    def on_exit(self):
        """Called when transitioning out of this state. Override for cleanup."""
        logger.debug("Exiting state: %s", self.loop_type)

    def tick(self):
        """
        Called each frame for state-specific updates.
        Override for states that need continuous processing (e.g., resting, pathing).
        """
        pass

    def _change_state(self, new_state):
        """Convenience method to request a state change."""
        self.loop.change_loop(new_state)


# =============================================================================
# STATE MANAGER
# =============================================================================

class StateManager:
    """
    Manages game state transitions and delegates to the current state.

    This class serves as the Context in the State pattern. It:
        - Maintains a registry of all available states
        - Handles state transitions with proper enter/exit callbacks
        - Delegates display and input handling to the current state
    """

    def __init__(self, loop):
        """
        Initialize the state manager.

        Args:
            loop: The Loops instance that coordinates game state
        """
        self.loop = loop
        self._states = {}
        self._current_state = None
        self._current_loop_type = LoopType.none

    def register_state(self, state):
        """
        Register a state instance with the manager.

        Args:
            state: A GameState subclass instance
        """
        self._states[state.loop_type] = state
        logger.debug("Registered state: %s", state.loop_type)

    def register_states(self, states):
        """Register multiple states at once."""
        for state in states:
            self.register_state(state)

    def change_state(self, new_loop_type):
        """
        Transition to a new state.

        Calls on_exit on the old state and on_enter on the new state.

        Args:
            new_loop_type: LoopType enum of the new state
        """
        # Skip if already in this state (unless forcing refresh)
        if new_loop_type == self._current_loop_type:
            return

        # Exit current state
        if self._current_state is not None:
            self._current_state.on_exit()

        # Enter new state
        self._current_loop_type = new_loop_type

        if new_loop_type in self._states:
            self._current_state = self._states[new_loop_type]
            self._current_state.on_enter()
            logger.debug("Changed to state: %s", new_loop_type)
        else:
            self._current_state = None
            logger.warning("No registered state for: %s", new_loop_type)

    def create_display(self, display):
        """Delegate display creation to current state."""
        if self._current_state is not None:
            self._current_state.create_display(display)

    def update_display(self, display):
        """Delegate display update to current state."""
        if self._current_state is not None:
            self._current_state.update_display(display)

    def handle_input(self, key):
        """
        Delegate input handling to current state.

        Returns:
            bool: False to quit the game, True to continue
        """
        if self._current_state is not None:
            return self._current_state.handle_input(key)
        return True

    def tick(self):
        """Delegate tick to current state for continuous processing."""
        if self._current_state is not None:
            self._current_state.tick()

    @property
    def current_loop_type(self):
        """Get the current state's loop type."""
        return self._current_loop_type

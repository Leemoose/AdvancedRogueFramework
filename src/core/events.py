"""
Event System for decoupling game components.

This module provides a simple pub/sub event system that allows game
components to communicate without direct dependencies. Components
subscribe to events they care about and emit events when things happen.

Example usage:
    from src.core.events import EventBus, GameEvent

    # Subscribe to events
    def on_monster_death(data):
        print(f"Monster {data['monster'].name} died!")

    EventBus.subscribe(GameEvent.MONSTER_DEATH, on_monster_death)

    # Emit events
    EventBus.emit(GameEvent.MONSTER_DEATH, {'monster': monster, 'killer': player})
"""
from enum import Enum, auto
from typing import Callable, Dict, List, Any, Optional
from logging_config import get_logger

logger = get_logger(__name__)


class GameEvent(Enum):
    """
    All game events that can be emitted/subscribed to.

    Events are grouped by system for organization.
    """
    # Combat events
    DAMAGE_DEALT = auto()
    MONSTER_DEATH = auto()
    PLAYER_DEATH = auto()

    # Item events
    ITEM_PICKED_UP = auto()
    ITEM_DROPPED = auto()
    ITEM_USED = auto()
    ITEM_EQUIPPED = auto()
    ITEM_UNEQUIPPED = auto()

    # Player events
    LEVEL_UP = auto()
    EXPERIENCE_GAINED = auto()
    HEALTH_CHANGED = auto()
    MANA_CHANGED = auto()

    # Spell events
    SPELL_CAST = auto()
    SPELL_LEARNED = auto()

    # World events
    FLOOR_CHANGED = auto()
    DOOR_OPENED = auto()
    TRAP_TRIGGERED = auto()

    # Status effects
    STATUS_APPLIED = auto()
    STATUS_REMOVED = auto()
    STATUS_TICK = auto()

    # Quest events
    QUEST_RECEIVED = auto()
    QUEST_UPDATED = auto()
    QUEST_COMPLETED = auto()

    # UI events
    MESSAGE_ADDED = auto()
    TARGET_CHANGED = auto()


class EventBus:
    """
    Central event bus for game-wide pub/sub communication.

    This is a class-based singleton pattern - all methods are classmethods
    so you don't need to pass around an instance.

    Thread Safety: This implementation is NOT thread-safe. For a single-threaded
    game loop, this is fine. If you need thread safety, add locks.
    """
    _subscribers: Dict[GameEvent, List[Callable[[Dict[str, Any]], None]]] = {}
    _enabled: bool = True

    @classmethod
    def subscribe(cls, event: GameEvent, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Subscribe a handler to an event type.

        Args:
            event: The GameEvent to listen for
            handler: Callback function that takes event data dict
        """
        if event not in cls._subscribers:
            cls._subscribers[event] = []

        if handler not in cls._subscribers[event]:
            cls._subscribers[event].append(handler)
            logger.debug("Subscribed handler to %s", event)

    @classmethod
    def unsubscribe(cls, event: GameEvent, handler: Callable[[Dict[str, Any]], None]) -> bool:
        """
        Unsubscribe a handler from an event type.

        Args:
            event: The GameEvent to stop listening to
            handler: The handler to remove

        Returns:
            True if handler was found and removed, False otherwise
        """
        if event in cls._subscribers and handler in cls._subscribers[event]:
            cls._subscribers[event].remove(handler)
            logger.debug("Unsubscribed handler from %s", event)
            return True
        return False

    @classmethod
    def emit(cls, event: GameEvent, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit an event to all subscribers.

        Args:
            event: The GameEvent type to emit
            data: Optional dict of event-specific data
        """
        if not cls._enabled:
            return

        if data is None:
            data = {}

        logger.debug("Emitting %s with data: %s", event, list(data.keys()))

        if event in cls._subscribers:
            for handler in cls._subscribers[event]:
                try:
                    handler(data)
                except Exception as e:
                    logger.error("Error in event handler for %s: %s", event, e)

    @classmethod
    def clear(cls, event: Optional[GameEvent] = None) -> None:
        """
        Clear subscribers.

        Args:
            event: If specified, clear only this event's subscribers.
                   If None, clear all subscribers.
        """
        if event is not None:
            cls._subscribers[event] = []
        else:
            cls._subscribers.clear()
        logger.debug("Cleared subscribers for %s", event if event else "all events")

    @classmethod
    def set_enabled(cls, enabled: bool) -> None:
        """Enable or disable event emission globally."""
        cls._enabled = enabled

    @classmethod
    def get_subscriber_count(cls, event: GameEvent) -> int:
        """Get number of subscribers for an event (for debugging)."""
        return len(cls._subscribers.get(event, []))


# Convenience functions for common patterns
def on_damage(handler: Callable[[Dict[str, Any]], None]) -> Callable:
    """Decorator to subscribe a function to damage events."""
    EventBus.subscribe(GameEvent.DAMAGE_DEALT, handler)
    return handler


def on_monster_death(handler: Callable[[Dict[str, Any]], None]) -> Callable:
    """Decorator to subscribe a function to monster death events."""
    EventBus.subscribe(GameEvent.MONSTER_DEATH, handler)
    return handler


def on_level_up(handler: Callable[[Dict[str, Any]], None]) -> Callable:
    """Decorator to subscribe a function to level up events."""
    EventBus.subscribe(GameEvent.LEVEL_UP, handler)
    return handler

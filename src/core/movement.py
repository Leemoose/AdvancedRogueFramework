"""
Movement System
===============

Provides movement validation and utilities.
"""

from typing import Tuple, Optional


class MovementResult:
    """Result of a movement validation check."""

    def __init__(self, can_move: bool, reason: str = ""):
        self.can_move = can_move
        self.reason = reason

    def __bool__(self):
        return self.can_move


class MovementValidator:
    """Validates movement for entities."""

    @staticmethod
    def can_move_to(loop, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                    character) -> MovementResult:
        """
        Check if a character can move to the target position.

        Args:
            loop: The game loop instance
            from_pos: Current (x, y) position
            to_pos: Target (x, y) position
            character: The character component to check

        Returns:
            MovementResult with success/failure and reason
        """
        x, y = to_pos

        # Check map bounds
        if not loop.generator.in_map(x, y):
            return MovementResult(False, "Out of bounds")

        # Check if character can act
        if not character.can_take_action():
            return MovementResult(False, "Cannot take action")

        # Check if character can move
        if not character.can_move():
            return MovementResult(False, "Movement restricted")

        # Check if tile is passable
        if not loop.generator.get_passable(to_pos):
            return MovementResult(False, "Tile blocked")

        return MovementResult(True, "OK")

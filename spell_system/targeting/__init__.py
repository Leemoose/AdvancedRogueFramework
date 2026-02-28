"""
Targeting system for spells.

Provides reusable functions to determine spell targets based on
different targeting patterns (single, AoE, adjacent, line, etc.)
"""

from .functions import (
    get_single_target,
    get_enemies_in_radius,
    get_entities_in_radius,
    get_positions_in_radius,
    get_adjacent_positions,
    get_passable_adjacent_positions,
    get_line_positions,
    get_cone_positions,
)

from .types import TargetType

__all__ = [
    'get_single_target',
    'get_enemies_in_radius',
    'get_entities_in_radius',
    'get_positions_in_radius',
    'get_adjacent_positions',
    'get_passable_adjacent_positions',
    'get_line_positions',
    'get_cone_positions',
    'TargetType',
]

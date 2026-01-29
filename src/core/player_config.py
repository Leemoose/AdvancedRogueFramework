"""
Player Configuration
====================

Centralizes player initialization constants and debug settings.
"""

class PlayerConfig:
    """Configuration for player initial state."""

    # Starting stats
    STARTING_HEALTH = 10
    STARTING_MANA = 5
    STARTING_X = 0
    STARTING_Y = 0

    # Level caps
    MAX_LEVEL = 20

    # Debug mode
    DEBUG_MODE = True  # Note: currently True in the codebase (player starts invincible)
    DEBUG_STARTING_STAT_POINTS = 20

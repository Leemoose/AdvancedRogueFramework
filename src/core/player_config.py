"""
Player Configuration
====================

Centralizes player initialization constants and debug settings.
"""

class PlayerConfig:
    """Configuration for player initial state."""

    # Starting stats
    STARTING_HEALTH = 25      # Increased from 10 - gives survivability for floor 1
    STARTING_MANA = 10        # Increased from 5 - allows 1-2 spell casts early
    STARTING_X = -1           # -1 signals spawn at valid location
    STARTING_Y = -1           # -1 signals spawn at valid location

    # Level caps
    MAX_LEVEL = 20

    # Debug mode
    DEBUG_MODE = True       # Disabled - player is no longer invincible
    DEBUG_STARTING_STAT_POINTS = 2  # Normal starting points

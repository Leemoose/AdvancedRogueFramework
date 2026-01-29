"""
Game Configuration
==================

Centralized configuration management for the game.
Replaces scattered global variables and magic numbers.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
import os


@dataclass
class DisplayConfig:
    """Display and rendering configuration."""
    tile_size: int = 32
    window_width: int = 1920
    window_height: int = 1080
    fullscreen: bool = False
    fps_limit: int = 60

    @property
    def tiles_wide(self) -> int:
        """Number of tiles that fit horizontally."""
        return self.window_width // self.tile_size

    @property
    def tiles_high(self) -> int:
        """Number of tiles that fit vertically."""
        return self.window_height // self.tile_size


@dataclass
class AudioConfig:
    """Audio settings."""
    master_volume: float = 1.0
    music_volume: float = 0.7
    sfx_volume: float = 1.0
    enabled: bool = True


@dataclass
class GameplayConfig:
    """Gameplay balance settings."""
    starting_health: int = 100
    starting_mana: int = 50
    base_move_cost: int = 100
    vision_radius: int = 8
    auto_pickup_gold: bool = True
    show_damage_numbers: bool = True


@dataclass
class DebugConfig:
    """Debug and development settings."""
    enabled: bool = False
    show_fps: bool = False
    show_coordinates: bool = False
    invincible: bool = False
    reveal_map: bool = False
    verbose_logging: bool = False


@dataclass
class GameConfig:
    """
    Master configuration container.

    Holds all game configuration in a single, serializable object.
    Can be saved to and loaded from JSON files.

    Usage:
        config = GameConfig()
        config.display.tile_size = 64
        config.save("settings.json")

        # Load existing config
        config = GameConfig.load("settings.json")
    """
    display: DisplayConfig = field(default_factory=DisplayConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    gameplay: GameplayConfig = field(default_factory=GameplayConfig)
    debug: DebugConfig = field(default_factory=DebugConfig)

    # Key bindings (action_name -> key_code)
    key_bindings: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default key bindings if not provided."""
        if not self.key_bindings:
            self._set_default_key_bindings()

    def _set_default_key_bindings(self):
        """Set up default keyboard controls."""
        import pygame
        self.key_bindings = {
            "move_up": pygame.K_w,
            "move_down": pygame.K_s,
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "move_up_left": pygame.K_q,
            "move_up_right": pygame.K_e,
            "move_down_left": pygame.K_z,
            "move_down_right": pygame.K_c,
            "wait": pygame.K_PERIOD,
            "inventory": pygame.K_i,
            "equipment": pygame.K_u,
            "spell_menu": pygame.K_m,
            "rest": pygame.K_r,
            "pickup": pygame.K_g,
            "examine": pygame.K_x,
            "help": pygame.K_SLASH,
            "pause": pygame.K_ESCAPE,
            "confirm": pygame.K_RETURN,
            "cancel": pygame.K_ESCAPE,
            "stairs_down": pygame.K_GREATER,
            "stairs_up": pygame.K_LESS,
            "autoexplore": pygame.K_o,
        }

    def save(self, filepath: str) -> None:
        """
        Save configuration to a JSON file.

        Args:
            filepath: Path to save the configuration file.
        """
        data = {
            "display": self.display.__dict__,
            "audio": self.audio.__dict__,
            "gameplay": self.gameplay.__dict__,
            "debug": self.debug.__dict__,
            "key_bindings": self.key_bindings,
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'GameConfig':
        """
        Load configuration from a JSON file.

        Args:
            filepath: Path to the configuration file.

        Returns:
            GameConfig instance with loaded settings.

        Note:
            Returns default config if file doesn't exist.
        """
        if not os.path.exists(filepath):
            return cls()

        with open(filepath, 'r') as f:
            data = json.load(f)

        config = cls()

        if "display" in data:
            for key, value in data["display"].items():
                if hasattr(config.display, key):
                    setattr(config.display, key, value)

        if "audio" in data:
            for key, value in data["audio"].items():
                if hasattr(config.audio, key):
                    setattr(config.audio, key, value)

        if "gameplay" in data:
            for key, value in data["gameplay"].items():
                if hasattr(config.gameplay, key):
                    setattr(config.gameplay, key, value)

        if "debug" in data:
            for key, value in data["debug"].items():
                if hasattr(config.debug, key):
                    setattr(config.debug, key, value)

        if "key_bindings" in data:
            config.key_bindings.update(data["key_bindings"])

        return config


# Global configuration instance
_config: Optional[GameConfig] = None


def get_config() -> GameConfig:
    """
    Get the global configuration instance.

    Creates a default config if none exists.

    Returns:
        The global GameConfig instance.
    """
    global _config
    if _config is None:
        _config = GameConfig()
    return _config


def set_config(config: GameConfig) -> None:
    """
    Set the global configuration instance.

    Args:
        config: The configuration to use globally.
    """
    global _config
    _config = config

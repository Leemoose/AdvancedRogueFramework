"""
Logging Configuration for RogueGame
====================================

Centralized logging setup with debug toggle support.
Logs are written to a file (debug.log) rather than the terminal.

Usage:
    from logging_config import get_logger, set_debug_mode, is_debug_mode

    logger = get_logger(__name__)
    logger.debug("This only shows when DEBUG_MODE is True")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error message")

To enable debug mode:
    1. Set DEBUG_MODE = True below, OR
    2. Call set_debug_mode(True) at runtime

Log file location: debug.log (in the game's root directory)
"""

import logging
import os
import sys
from typing import Optional

# =============================================================================
# DEBUG TOGGLE - Set to True to enable debug logging
# =============================================================================
DEBUG_MODE = True

# =============================================================================
# Log File Configuration
# =============================================================================
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")
LOG_TO_CONSOLE = False  # Set True to also print to terminal
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB max file size before rotation

# =============================================================================
# Logging Configuration
# =============================================================================

# Log format with timestamp, level, module, function, and line number for tracing
LOG_FORMAT_DEBUG = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
LOG_FORMAT_NORMAL = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

# Date format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# =============================================================================
# Noisy Modules - These get reduced logging to avoid spam
# Set to INFO to reduce noise from high-frequency calls
# =============================================================================
NOISY_MODULES = {
    # Game loop modules - these fire every frame
    "loops": logging.INFO,
    "__main__": logging.INFO,

    # High-frequency map operations
    "dungeon_generation.maps.maps": logging.INFO,  # in_map, get_entity called constantly

    # Character modules with lots of chatter
    "character_implementation.body_slot": logging.INFO,
    "character_implementation.status": logging.INFO,
    "character_implementation.character": logging.INFO,

    # Monster AI - very chatty during combat
    "monster_implementation.monster_ai": logging.INFO,
    "monster_implementation.do_actions_utility": logging.INFO,
    "monster_implementation.ranking_actions_utility": logging.INFO,
}

# Modules you want verbose DEBUG logging for (overrides NOISY_MODULES)
VERBOSE_MODULES = {
    # Uncomment modules you want to debug in detail:
    # "dungeon_generation.maps.map_utility": logging.DEBUG,
    # "dungeon_generation.maps.tilemap": logging.DEBUG,
}

# =============================================================================
# Logger Setup
# =============================================================================

_loggers: dict = {}
_file_handler: Optional[logging.Handler] = None
_console_handler: Optional[logging.Handler] = None
_initialized = False


def _get_log_level() -> int:
    """Get the appropriate log level based on DEBUG_MODE."""
    return logging.DEBUG if DEBUG_MODE else logging.INFO


def _get_log_format() -> str:
    """Get the appropriate log format based on DEBUG_MODE."""
    return LOG_FORMAT_DEBUG if DEBUG_MODE else LOG_FORMAT_NORMAL


def _setup_file_handler() -> logging.Handler:
    """Create and configure the file handler."""
    global _file_handler
    if _file_handler is None:
        # Use RotatingFileHandler to prevent huge log files
        from logging.handlers import RotatingFileHandler
        _file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=1,  # Keep 3 backup files
            encoding='utf-8'
        )
        _file_handler.setFormatter(logging.Formatter(_get_log_format(), DATE_FORMAT))
        _file_handler.setLevel(logging.DEBUG)  # File gets everything
    return _file_handler


def _setup_console_handler() -> logging.Handler:
    """Create and configure the console handler (optional)."""
    global _console_handler
    if _console_handler is None:
        _console_handler = logging.StreamHandler(sys.stdout)
        _console_handler.setFormatter(logging.Formatter(_get_log_format(), DATE_FORMAT))
        _console_handler.setLevel(logging.WARNING)  # Console only gets warnings+
    return _console_handler


def _initialize_logging():
    """Initialize the logging system."""
    global _initialized
    if _initialized:
        return

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Allow all levels, handlers control output

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Always add file handler
    root_logger.addHandler(_setup_file_handler())

    # Optionally add console handler
    if LOG_TO_CONSOLE:
        root_logger.addHandler(_setup_console_handler())

    _initialized = True

    # Log startup
    root_logger.info("=" * 60)
    root_logger.info("RogueGame Debug Log Started")
    root_logger.info("DEBUG_MODE: %s", DEBUG_MODE)
    root_logger.info("Log file: %s", LOG_FILE)
    root_logger.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance

    Example:
        logger = get_logger(__name__)
        logger.debug("Placing entity at (%d, %d)", x, y)
    """
    _initialize_logging()

    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)

    # Apply verbose module level first (highest priority)
    if name in VERBOSE_MODULES:
        logger.setLevel(VERBOSE_MODULES[name])
    # Then check noisy modules (reduce their verbosity)
    elif name in NOISY_MODULES:
        logger.setLevel(NOISY_MODULES[name])
    # Default level
    else:
        logger.setLevel(_get_log_level())

    _loggers[name] = logger
    return logger


def set_debug_mode(enabled: bool) -> None:
    """
    Enable or disable debug mode at runtime.

    Args:
        enabled: True to enable debug logging, False to disable

    Example:
        set_debug_mode(True)  # Enable debug output
        set_debug_mode(False)  # Disable debug output
    """
    global DEBUG_MODE
    DEBUG_MODE = enabled

    new_level = _get_log_level()
    new_format = _get_log_format()

    # Update file handler format
    if _file_handler is not None:
        _file_handler.setFormatter(logging.Formatter(new_format, DATE_FORMAT))

    # Update loggers (respecting noisy/verbose overrides)
    for name, logger in _loggers.items():
        if name in VERBOSE_MODULES:
            logger.setLevel(VERBOSE_MODULES[name])
        elif name in NOISY_MODULES:
            logger.setLevel(NOISY_MODULES[name])
        else:
            logger.setLevel(new_level)

    # Log the change
    root_logger = logging.getLogger()
    root_logger.info("Debug mode %s", "enabled" if enabled else "disabled")


def is_debug_mode() -> bool:
    """
    Check if debug mode is currently enabled.

    Returns:
        True if debug mode is enabled, False otherwise
    """
    return DEBUG_MODE


def set_module_level(module_name: str, level: int) -> None:
    """
    Set the log level for a specific module.

    Args:
        module_name: The module name (e.g., "dungeon_generation.maps")
        level: The logging level (e.g., logging.DEBUG, logging.INFO)

    Example:
        set_module_level("dungeon_generation.maps", logging.WARNING)
    """
    VERBOSE_MODULES[module_name] = level
    if module_name in _loggers:
        _loggers[module_name].setLevel(level)


def set_module_verbose(module_name: str) -> None:
    """
    Enable verbose (DEBUG) logging for a specific module.

    Useful for debugging specific areas without all the noise.

    Example:
        set_module_verbose("dungeon_generation.maps.tilemap")
    """
    set_module_level(module_name, logging.DEBUG)


def set_module_quiet(module_name: str) -> None:
    """
    Reduce logging for a specific module to INFO level.

    Example:
        set_module_quiet("loops")
    """
    set_module_level(module_name, logging.INFO)


def clear_log_file() -> None:
    """Clear the debug log file."""
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
        logging.getLogger().info("Log file cleared")


# =============================================================================
# Convenience Functions for Bug Tracing
# =============================================================================

def log_function_entry(logger: logging.Logger, *args, **kwargs) -> None:
    """
    Log function entry with arguments (useful for tracing).

    Example:
        def my_function(x, y):
            log_function_entry(logger, x=x, y=y)
    """
    if DEBUG_MODE:
        arg_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        logger.debug("ENTER: %s", arg_str if arg_str else "(no args)")


def log_function_exit(logger: logging.Logger, result=None) -> None:
    """
    Log function exit with optional return value.

    Example:
        def my_function(x, y):
            result = x + y
            log_function_exit(logger, result=result)
            return result
    """
    if DEBUG_MODE:
        logger.debug("EXIT: returned %r", result)


def log_high_priority(logger: logging.Logger, message: str, *args, **kwargs) -> None:
    """
    Log a high priority error message. Use this instead of raising exceptions
    to avoid breaking the game while still flagging serious issues.

    These messages are logged at ERROR level with a HIGH_PRIORITY prefix
    to make them easy to find and filter in logs.

    Args:
        logger: The logger instance to use
        message: The message format string
        *args: Format arguments for the message

    Example:
        log_high_priority(logger, "Invalid ID requested: %d", id_value)
    """
    logger.error("[HIGH_PRIORITY] " + message, *args, **kwargs)


# =============================================================================
# Backwards Compatibility with global_bugtesting
# =============================================================================

# This allows existing code using global_bugtesting to continue working
# while transitioning to the new logging system
global_bugtesting = DEBUG_MODE

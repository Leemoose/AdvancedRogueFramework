"""
Path utilities for PyInstaller bundled executables.

When running as a bundled executable, assets are extracted to a temporary
directory (_MEIPASS). This module provides a consistent way to locate
resources whether running from source or from a bundled executable.
"""
import sys
import os
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller.

    When running as a bundled executable, PyInstaller extracts data files
    to a temporary folder stored in sys._MEIPASS. When running from source,
    paths are relative to the project root.

    Args:
        relative_path: Path relative to the project root

    Returns:
        Absolute path to the resource
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as bundled executable
        base_path = sys._MEIPASS
    else:
        # Running from source - go up from src/core/ to project root
        base_path = Path(__file__).parent.parent.parent

    return os.path.join(base_path, relative_path)


def get_asset_path(asset_name: str) -> str:
    """Convenience function for assets folder."""
    return resource_path(os.path.join('assets', asset_name))


def get_data_path(filename: str) -> str:
    """Get path for data files (saves, config)."""
    # For bundled apps, use user's app data directory
    if hasattr(sys, '_MEIPASS'):
        # Use platform-appropriate location
        if sys.platform == 'darwin':
            data_dir = os.path.expanduser('~/Library/Application Support/RogueGame')
        elif sys.platform == 'win32':
            data_dir = os.path.join(os.environ.get('APPDATA', '.'), 'RogueGame')
        else:
            data_dir = os.path.expanduser('~/.roguegame')

        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, filename)
    else:
        # Running from source
        return resource_path(filename)

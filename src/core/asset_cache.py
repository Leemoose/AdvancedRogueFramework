"""
Asset caching system to prevent repeated image loading.

This module provides a centralized cache for pygame images to avoid
loading the same image multiple times, especially during render loops.
"""
import pygame
from typing import Optional, Tuple, Dict, Any


class AssetCache:
    """
    Centralized cache for pygame image assets.

    Prevents repeated disk reads by caching loaded images in memory.
    Supports optional scaling - cached images are keyed by (path, size) tuple.

    Usage:
        # Load and cache an image
        img = AssetCache.load("assets/player.png")

        # Load with specific size
        img = AssetCache.load("assets/orb.png", size=(64, 64))

        # Clear cache (e.g., on level change)
        AssetCache.clear()
    """
    _cache: Dict[Tuple[str, Optional[Tuple[int, int]]], pygame.Surface] = {}
    _stats: Dict[str, int] = {"hits": 0, "misses": 0}

    @classmethod
    def load(cls, path: str, size: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """
        Load an image from disk or return cached version.

        Args:
            path: Path to the image file
            size: Optional (width, height) tuple to scale the image

        Returns:
            pygame.Surface: The loaded (and optionally scaled) image
        """
        key = (path, size)

        if key in cls._cache:
            cls._stats["hits"] += 1
            return cls._cache[key]

        cls._stats["misses"] += 1

        # Load and convert for optimal blitting
        img = pygame.image.load(path).convert_alpha()

        if size is not None:
            img = pygame.transform.scale(img, size)

        cls._cache[key] = img
        return img

    @classmethod
    def preload(cls, paths: list, size: Optional[Tuple[int, int]] = None) -> None:
        """
        Preload multiple images into the cache.

        Args:
            paths: List of image file paths to preload
            size: Optional size to scale all images to
        """
        for path in paths:
            cls.load(path, size)

    @classmethod
    def clear(cls) -> None:
        """Clear all cached images."""
        cls._cache.clear()
        cls._stats = {"hits": 0, "misses": 0}

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """
        Get cache statistics for debugging.

        Returns:
            Dict with hits, misses, and cache size
        """
        return {
            "hits": cls._stats["hits"],
            "misses": cls._stats["misses"],
            "cached_images": len(cls._cache),
            "hit_rate": cls._stats["hits"] / max(1, cls._stats["hits"] + cls._stats["misses"])
        }

    @classmethod
    def is_cached(cls, path: str, size: Optional[Tuple[int, int]] = None) -> bool:
        """Check if an image is already in the cache."""
        return (path, size) in cls._cache

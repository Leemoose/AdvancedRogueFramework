"""
DEPRECATED: get_closest_monster has moved to navigation_utility.spatial_queries

This file re-exports for backwards compatibility.
New code should import from navigation_utility directly:
    from navigation_utility import get_closest_monster
"""

from navigation_utility.spatial_queries import get_closest_monster

__all__ = ['get_closest_monster']

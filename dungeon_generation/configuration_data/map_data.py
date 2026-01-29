"""
Map Data Module
===============

Configuration classes for dungeon map generation.
Supports multiple generator types and spawn strategies.
"""

from typing import Optional, Dict, Any


class MapData:
    """
    Configuration data for a single dungeon floor.

    Supports the legacy constructor for backwards compatibility while
    also providing the new generator_type and spawn_strategy options.

    Generator Types:
        - 'rooms_corridors' (default): Traditional rooms connected by L-corridors
        - 'cave': Cellular automata organic caves
        - 'pillar_hall': Open space with pillars

    Spawn Strategy Types:
        - 'random' (default): Random monster placement
        - 'elite_group': Elite monster with minion pack
        - 'guarding_items': Monsters positioned near items
    """

    def __init__(
        self,
        width: int,
        height: int,
        numRooms: int,
        roomSize: int,
        circularity: float,
        squarelike: int,
        generator_type: str = 'rooms_corridors',
        spawn_strategy: str = 'random',
        generator_params: Optional[Dict[str, Any]] = None,
        spawn_params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize map configuration.

        Args:
            width: Map width in tiles
            height: Map height in tiles
            numRooms: Number of rooms (for rooms_corridors generator)
            roomSize: Maximum room size (for rooms_corridors generator)
            circularity: Room shape factor, 0=square, 1=circle
            squarelike: Legacy parameter (kept for compatibility)
            generator_type: Which generator to use ('rooms_corridors', 'cave', 'pillar_hall')
            spawn_strategy: Which spawn strategy to use ('random', 'elite_group', 'guarding_items')
            generator_params: Additional params for the generator (overrides defaults)
            spawn_params: Additional params for the spawn strategy (overrides defaults)
        """
        self.width = width
        self.height = height
        self.numRooms = numRooms
        self.roomSize = roomSize
        self.circularity = circularity
        self.squarelike = squarelike
        self.generator_type = generator_type
        self.spawn_strategy = spawn_strategy
        self.generator_params = generator_params or {}
        self.spawn_params = spawn_params or {}

    def get_numRooms(self) -> int:
        return self.numRooms

    def get_circularity(self) -> float:
        return self.circularity

    def get_roomSize(self) -> int:
        return self.roomSize

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_generator_type(self) -> str:
        """Return the generator type for this floor."""
        return self.generator_type

    def get_spawn_strategy(self) -> str:
        """Return the spawn strategy type for this floor."""
        return self.spawn_strategy

    def get_generator_params(self) -> Dict[str, Any]:
        """Return additional generator parameters."""
        return self.generator_params

    def get_spawn_params(self) -> Dict[str, Any]:
        """Return additional spawn strategy parameters."""
        return self.spawn_params


# Convenience factory functions for common configurations

def rooms_corridors_map(
    width: int,
    height: int,
    num_rooms: int = 10,
    room_size: int = 8,
    circularity: float = 0.5
) -> MapData:
    """Create a MapData configured for rooms and corridors generation."""
    return MapData(
        width=width,
        height=height,
        numRooms=num_rooms,
        roomSize=room_size,
        circularity=circularity,
        squarelike=0,
        generator_type='rooms_corridors'
    )


def cave_map(
    width: int,
    height: int,
    fill_probability: float = 0.45,
    smooth_iterations: int = 5
) -> MapData:
    """Create a MapData configured for cave generation."""
    return MapData(
        width=width,
        height=height,
        numRooms=0,
        roomSize=0,
        circularity=0,
        squarelike=0,
        generator_type='cave',
        generator_params={
            'fill_probability': fill_probability,
            'smooth_iterations': smooth_iterations
        }
    )


def pillar_hall_map(
    width: int,
    height: int,
    pillar_spacing: int = 4,
    pillar_density: float = 0.8
) -> MapData:
    """Create a MapData configured for pillar hall generation."""
    return MapData(
        width=width,
        height=height,
        numRooms=1,
        roomSize=max(width, height),
        circularity=0,
        squarelike=0,
        generator_type='pillar_hall',
        generator_params={
            'pillar_spacing': pillar_spacing,
            'pillar_density': pillar_density
        }
    )
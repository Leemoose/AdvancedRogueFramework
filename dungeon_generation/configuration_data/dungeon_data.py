"""
Dungeon Data Module
===================

Configuration for all dungeon branches and their floor layouts.
Supports multiple generation strategies per floor.

Generator Types:
    - rooms_corridors: Traditional rooms connected by L-corridors (default)
    - cave: Cellular automata organic caves
    - pillar_hall: Open space with pillar columns

Spawn Strategy Types:
    - random: Random monster placement (default)
    - elite_group: Elite monster with minion pack
    - guarding_items: Monsters positioned near items
"""

from .map_data import MapData


class DungeonData:
    """
    Configuration data for all dungeon branches.

    Each branch contains a dictionary mapping floor depth to MapData
    configuration objects. The MapData specifies the generator type,
    spawn strategy, and their parameters.
    """

    def __init__(self):
        self.master_map_data = {}

        # Main Dungeon branch - demonstrates all generator types
        self.master_map_data["Dungeon"] = {
            # Floors 1-3: Standard rooms and corridors (easy floors)
            1: MapData(20, 30, 4, 5, 1.0, 1,
                       generator_type='rooms_corridors',
                       spawn_strategy='random'),
            2: MapData(20, 30, 4, 5, 1.0, 1,
                       generator_type='rooms_corridors',
                       spawn_strategy='random'),
            3: MapData(20, 30, 4, 5, 1.0, 1,
                       generator_type='rooms_corridors',
                       spawn_strategy='random'),

            # Floor 4: Square rooms, monsters guard items
            4: MapData(30, 30, 6, 5, 0.0, 0,
                       generator_type='rooms_corridors',
                       spawn_strategy='guarding_items',
                       spawn_params={'guard_chance': 0.4}),

            # Floor 5: Cave level - organic shapes
            5: MapData(35, 35, 7, 6, 0.2, 0,
                       generator_type='cave',
                       spawn_strategy='random',
                       generator_params={'fill_probability': 0.45, 'smooth_iterations': 5}),

            # Floor 6: Another cave, with elite packs
            6: MapData(35, 35, 8, 7, 0.3, 0,
                       generator_type='cave',
                       spawn_strategy='elite_group',
                       generator_params={'fill_probability': 0.42},
                       spawn_params={'formation': 'cluster'}),

            # Floor 7: Mixed - larger rooms
            7: MapData(40, 40, 9, 7, 0.5, 0,
                       generator_type='rooms_corridors',
                       spawn_strategy='random'),

            # Floor 8: More rooms, guarding items
            8: MapData(40, 40, 10, 8, 0.6, 0,
                       generator_type='rooms_corridors',
                       spawn_strategy='guarding_items',
                       spawn_params={'guard_chance': 0.6, 'guard_radius_max': 3}),

            # Floor 9: Pillar hall - mini-boss arena
            9: MapData(45, 45, 11, 9, 0.0, 0,
                       generator_type='pillar_hall',
                       spawn_strategy='elite_group',
                       generator_params={'pillar_spacing': 5, 'pillar_density': 0.7},
                       spawn_params={'formation': 'circle', 'elite_radius': 4}),

            # Floor 10: Final boss room - large pillar hall
            10: MapData(50, 50, 12, 10, 1.0, 0,
                        generator_type='pillar_hall',
                        spawn_strategy='elite_group',
                        generator_params={'pillar_spacing': 6, 'pillar_density': 0.6},
                        spawn_params={'formation': 'circle', 'elite_radius': 5})
        }

        # Forest branch (commented out - can be enabled)
        # self.master_map_data["Forest"] = {
        #     1: MapData(20, 30, 4, 5, 1.0, 1,
        #                generator_type='cave',
        #                spawn_strategy='random',
        #                generator_params={'fill_probability': 0.40}),
        #     2: MapData(60, 60, 15, 10, .05, 1,
        #                generator_type='cave',
        #                spawn_strategy='guarding_items'),
        #     3: MapData(60, 60, 15, 10, .1, 0,
        #                generator_type='cave',
        #                spawn_strategy='elite_group'),
        # }

        # Throne branch (commented out - can be enabled)
        # self.master_map_data["Throne"] = {
        #     1: MapData(20, 60, 4, 5, 1.0, 1,
        #                generator_type='pillar_hall',
        #                spawn_strategy='elite_group')
        # }

        # Hub branch (commented out - can be enabled)
        # self.master_map_data["Hub"] = {
        #     1: MapData(10, 10, 4, 5, 1.0, 1,
        #                generator_type='rooms_corridors',
        #                spawn_strategy='random')
        # }

    def get_branches(self):
        """Return all available branch names."""
        return self.master_map_data.keys()

    def get_depth(self, branch: str) -> int:
        """Return the maximum depth of a branch."""
        return len(self.master_map_data[branch])

    def get_map_data(self, branch: str, depth: int) -> MapData:
        """Get the MapData configuration for a specific branch and depth."""
        return self.master_map_data[branch][depth]

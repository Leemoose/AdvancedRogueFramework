import random
"""
Dungeon Generator Module
========================

Responsible for creating complete dungeon floors including:
- Map layout (via configurable generators)
- Monster spawning (via configurable strategies)
- Item spawning
- Interactable spawning

Supports multiple generation and spawning strategies:

Map Generators:
    - rooms_corridors: Traditional rooms connected by L-shaped corridors
    - cave: Cellular automata organic caves
    - pillar_hall: Open space with pillar columns

Spawn Strategies:
    - random: Random monster placement
    - elite_group: Elite monster with minion pack
    - guarding_items: Monsters positioned near items
"""

from typing import Optional, TYPE_CHECKING
from .spawning import branch_params, item_spawner, monster_spawner, interactable_spawner
from .maps import TileMap, TrackingMap
from .mapping_utility import (
    place_spawn_interactables,
    place_spawn_items,
    place_spawn_monster,
    place_pack,
    get_random_direction
)
from logging_config import get_logger, log_high_priority
from src.core.directions import Directions

if TYPE_CHECKING:
    from .spawn_strategies.base import MonsterSpawnStrategy

logger = get_logger(__name__)


def _get_spawn_strategy(mapData) -> Optional['MonsterSpawnStrategy']:
    """
    Factory function to create the appropriate spawn strategy based on mapData.

    Args:
        mapData: MapData configuration object

    Returns:
        A MonsterSpawnStrategy instance, or None to use legacy spawning
    """
    from .spawn_strategies import (
        RandomSpawnStrategy,
        EliteWithGroupStrategy,
        GuardingItemsStrategy
    )

    strategy_type = getattr(mapData, 'spawn_strategy', 'random')
    spawn_params = getattr(mapData, 'spawn_params', {})

    logger.debug("Creating spawn strategy: type=%s", strategy_type)

    if strategy_type == 'elite_group':
        return EliteWithGroupStrategy(
            elite_radius=spawn_params.get('elite_radius', 3),
            prefer_large_rooms=spawn_params.get('prefer_large_rooms', True),
            formation=spawn_params.get('formation', 'cluster')
        )
    elif strategy_type == 'guarding_items':
        return GuardingItemsStrategy(
            guard_radius_min=spawn_params.get('guard_radius_min', 2),
            guard_radius_max=spawn_params.get('guard_radius_max', 4),
            guard_chance=spawn_params.get('guard_chance', 0.5),
            prefer_rare_items=spawn_params.get('prefer_rare_items', True)
        )
    elif strategy_type == 'random':
        return RandomSpawnStrategy(
            avoid_corridors=spawn_params.get('avoid_corridors', False),
            avoid_stairs=spawn_params.get('avoid_stairs', True),
            max_attempts=spawn_params.get('max_attempts', 1000),
            pack_search_radius=spawn_params.get('pack_search_radius', 2)
        )
    else:
        # Unknown strategy, return None to use legacy
        logger.warning("Unknown spawn strategy '%s', using legacy spawning", strategy_type)
        return None


class DungeonGenerator:
    """
    Generates complete dungeon floors with map layout, monsters, and items.

    The generator uses configurable strategies for both map generation and
    monster spawning. Strategy types are specified in the MapData configuration.

    Attributes:
        mapData: Configuration for this floor
        spawn_params: Branch-specific spawn parameters
        tile_map: The generated tile map
        monster_map: Tracking map for monster positions
        interact_map: Tracking map for interactable positions
        item_map: Tracking map for item positions
        player: Reference to the player entity
        summoner: List of summoner entities

    Example:
        # Using default strategies (rooms_corridors + random spawning)
        generator = DungeonGenerator(depth=1, player=player, branch="Dungeon", dungeon_data=data)

        # Using custom strategies (configured in MapData)
        # mapData = MapData(..., generator_type='cave', spawn_strategy='elite_group')
    """

    def __init__(
        self,
        depth: int,
        player,
        branch: str,
        dungeon_data,
        use_legacy_spawning: bool = False
    ):
        """
        Initialize and generate a dungeon floor.

        Args:
            depth: Floor depth (1-indexed)
            player: Player entity reference
            branch: Dungeon branch name
            dungeon_data: DungeonData configuration object
            use_legacy_spawning: If True, use old spawn code (for backwards compatibility)
        """
        logger.debug("Initializing DungeonGenerator for depth %d, branch %s", depth, branch)
        self.mapData = dungeon_data.get_map_data(branch, depth)
        self.spawn_params = branch_params[branch]

        self.summoner = []

        # Generate the map using the configured generator
        self.tile_map = TileMap(self.mapData, depth, branch)
        self.monster_map = TrackingMap(self.get_width(), self.get_height())
        self.interact_map = TrackingMap(self.get_width(), self.get_height())
        self.item_map = TrackingMap(self.get_width(), self.get_height())

        self.player = player

        # Spawn interactables (always uses legacy for now)
        place_spawn_interactables(self, interactable_spawner)

        # Spawn items first (needed for guarding_items strategy)
        place_spawn_items(self, item_spawner)

        # Spawn monsters using configured strategy
        if use_legacy_spawning:
            logger.debug("Using legacy monster spawning")
            self._legacy_spawn_monsters()
        else:
            self._spawn_monsters_with_strategy()

        logger.debug("DungeonGenerator initialization complete")

    def _spawn_monsters_with_strategy(self) -> None:
        """Spawn monsters using the configured spawn strategy."""
        strategy = _get_spawn_strategy(self.mapData)

        # Generate the list of monsters to spawn
        monster_spawns = monster_spawner.spawnMonsters(
            self.get_depth(),
            self.get_branch()
        )

        if strategy is not None:
            logger.debug("Using spawn strategy: %s", type(strategy).__name__)
            # Flatten packs for strategy processing
            all_monsters = []
            for spawn in monster_spawns:
                if isinstance(spawn, list):
                    all_monsters.extend(spawn)
                else:
                    all_monsters.append(spawn)

            strategy.place_monsters(self, all_monsters)
        else:
            # Fallback to legacy placement
            self._legacy_spawn_monsters()

    def _legacy_spawn_monsters(self) -> None:
        """Legacy monster spawning for backwards compatibility."""
        monster_spawns = monster_spawner.spawnMonsters(
            self.get_depth(),
            self.get_branch()
        )
        for monster in monster_spawns:
            if isinstance(monster, list):
                place_pack(self, monster)
            else:
                place_spawn_monster(self, monster)
        logger.debug("Legacy spawning complete: %d monster groups", len(monster_spawns))

    def get_width(self):
        return self.mapData.get_width()

    def get_height(self):
        return self.mapData.get_height()

    def get_branch(self):
        return self.tile_map.get_branch()

    def get_depth(self):
        return self.tile_map.get_depth()
    def get_random_passable_location(self,stairs_block = True):
        start_x = random.randint(0, self.get_width() - 1)
        start_y = random.randint(0, self.get_height() - 1)
        count = 0
        while (not self.get_passable((start_x, start_y))) or (not stairs_block or self.get_is_on_stairs(start_x, start_y)):
            start_x = random.randint(0, self.get_width() - 1)
            start_y = random.randint(0, self.get_height() - 1)
            count += 1
            if count > 1000:
                log_high_priority(logger, "Stuck in infinite loop for checking random location.")
                return start_x, start_y
        return start_x, start_y

    def get_random_location(self, stairs_block = True, condition = None):
        candidates = []
        if condition is None:
            return self.get_random_passable_location(stairs_block)
        for x in range(0, self.get_width()):
            for y in range(0, self.get_height()):
                if condition((x, y)) or \
                    (not stairs_block or self.get_is_on_stairs(x, y)):
                    candidates.append((x, y))
        startx, starty = random.choice(candidates)
        return startx, starty

    def get_random_passable_location_not_in_hallway(self, stairs_block = True):
        x,y = self.get_random_passable_location(stairs_block)
        while self.get_is_in_corridor(x, y):
            x,y = self.get_random_passable_location(stairs_block)
        return x,y


    def get_monsters_in_sight(self):
        in_sight = []
        for monster in self.monster_map.get_all_entities():
            monster_x, monster_y = monster.get_location()
            if self.tile_map.get_entity(monster_x, monster_y).get_visible():
                in_sight.append(monster)
        return in_sight

    def get_all_seen(self):
        return self.tile_map.get_is_all_visible(), self.tile_map.get_next_not_visible_coordinate()

    def count_passable_neighbors(self, x, y):
        count = 0
        for direction in Directions.ALL_8:
            if self.get_passable((x + direction[0], y + direction[1])):
                count += 1
        return count

    # def get_nearest_exit (self, entity):
    #     # find the nearest exit to some entity, exit is adjacent to a tile with only tiles adjacent to it that are passable
    #     # if no such tile exists, return None
    #     list_of_exits = []
    #     for x in range(self.get_width()):
    #         for y in range(self.get_height()):
    #             if self.tile_map.get_entity(x,y).passable:
    #                 if self.count_passable_neighbors(x, y) == 2:
    #                     list_of_exits.append((x, y))
    #     entityx, entityy = entity.get_location()
    #     closest_exit = None
    #     closest_distance = 100000
    #     for exit in list_of_exits:
    #         distance = ((entityx - exit[0]) ** 2 + (entityy - exit[1]) ** 2) ** 0.5
    #         if distance < closest_distance:
    #             closest_distance = distance
    #             closest_exit = exit
    #     adjacent_to_exit = None
    #     for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
    #         # check all directions to find tile adjacent to exit that isnt an exit
    #         if self.tile_map.get_has_no_entity(closest_exit[0] + direction[0], closest_exit[1] + direction[1]):
    #             if self.count_passable_neighbors(closest_exit[0] + direction[0], closest_exit[1] + direction[1]) > 2:
    #                 # if tile has a character on it already
    #                 adjacent_to_exit = (closest_exit[0] + direction[0], closest_exit[1] + direction[1])
    #                 break
    #     return adjacent_to_exit

    def get_not_on_player(self, x, y):
        if self.player is None:
            return True
        else:
            return (x != self.player.get_x() or y != self.player.get_y())

    def get_passable(self, location):
        if type(location) is not tuple:
            logger.warning("You are trying to parse a non tuple")
        if location is None:
            return None
        elif (self.monster_map.get_has_no_entity(location[0], location[1])
              and self.get_not_on_player(location[0], location[1])
              and self.tile_map.get_passable(location[0], location[1])
              and self.interact_map.get_has_no_entity(location[0], location[1])):
            return True
        return False

    def get_visible(self, x, y):
        self.tile_map.get_visible(x, y)

    def get_nearest_empty_tile(self, location, move = False):
      #  import pdb; pdb.set_trace()
        if location is None:
            return None
        if not move and self.monster_map.get_has_no_entity(location[0], location[1]) and self.get_not_on_player(location[0], location[1]) and self.tile_map.get_has_no_entity(location[0], location[1]):
            return location
        for direction in Directions.ALL_8:
            if self.get_passable((location[0] + direction[0], location[1] + direction[1])):
                return (location[0] + direction[0], location[1] + direction[1])
        return None

    def in_map(self, x, y):
       return self.tile_map.in_map(x, y) and self.monster_map.in_map(x, y) and self.interact_map.in_map(x, y)


    def place_monster_at_location(self, creature, x, y):
        if self.get_passable((x, y)):
            creature.set_location(x, y)
            self.monster_map.place_thing(creature)
        else:
            logger.warning("Tried to place a creature at an invalid location")

    def place_item_at_location(self, item, x, y):
        if self.in_map(x, y):
            item.set_location(x, y)
            self.item_map.place_thing(item)
        else:
            logger.warning("Tried to place an item at an invalid location")

    def place_interactable_at_location(self, interactable, x, y):
        if self.get_passable((x, y)):
            interactable.set_location(x, y)
            self.interact_map.place_thing(interactable)
        else:
            logger.warning("Tried to place a interactable at an invalid location")

    def get_is_on_stairs(self, x, y):
        for stair in self.tile_map.stairs:
            if stair.get_x() == x and stair.get_y() == y:
                return True
        return False

    def get_is_in_corridor(self, x, y):
        count_passable = self.count_passable_neighbors(x, y)
        if count_passable > 6:
            return False
        else:
            directions = Directions.ALL_8
            min_passable = 8
            for dx, dy in directions:
                adj_x = x + dx
                adj_y = y + dy
                if self.tile_map.get_passable(adj_x, adj_y):
                    min_passable = min(min_passable, self.count_passable_neighbors(adj_x, adj_y))
            return min_passable < 3

    def get_passible_map_copy(self):
        tile_map = []
        for x in range(self.get_width()):
            new_row = []
            for y in range(self.get_height()):
                if self.get_passable((x, y)):
                    new_row.append(0)
                else:
                    new_row.append(-1)
            tile_map.append(new_row)
        return tile_map

    # def get_nearest_item(self, x, y):
    #     if self.item_map.get_has_entity(x, y):
    #         return (self.item_map.get_entity(x,y), x, y)
    #     else:
    #         queue = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    #         flood_map = self.get_passible_map_copy()
    #         return self.get_nearest_item_helper_function(x, y, queue, flood_map)


    # def get_nearest_item_helper_function(self, x, y, queue, flood_map):
    #     for direction in queue:
    #         xdelta, ydelta = direction
    #         if self.in_map(x + xdelta, y + ydelta) and flood_map[x + xdelta][y + ydelta] == 0:
    #             if self.item_map.get_has_entity(x + xdelta, y + ydelta):
    #                 return (self.item_map.get_entity(x + xdelta, y + ydelta), x, y)
    #             else:
    #                 flood_map[x + xdelta][y + ydelta] = -1
    #                 queue_additions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    #                 for direction in queue_additions:
    #                     if self.in_map(x + xdelta, y + ydelta) and flood_map[x + xdelta][y + ydelta] == 0:
    #                         queue.append(direction)
    #     return (None, -1, -1)








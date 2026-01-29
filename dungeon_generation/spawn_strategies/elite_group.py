"""
Elite With Group Spawn Strategy Module
=======================================

Spawn strategy that places an elite monster surrounded by minions
in a formation pattern within dungeon rooms.
"""

import math
import random
from typing import List, Optional, Tuple, Any, TYPE_CHECKING

from logging_config import get_logger
from .base import MonsterSpawnStrategy

if TYPE_CHECKING:
    from dungeon_generation.mapping import DungeonGenerator
    from dungeon_generation.maps.room import Room

logger = get_logger(__name__)


class EliteWithGroupStrategy(MonsterSpawnStrategy):
    """
    Spawn strategy that places the strongest monster as an elite
    surrounded by minion monsters in a specified formation.

    The elite is placed in a room (not a corridor) and minions
    are arranged around it based on the formation type.

    Attributes:
        elite_radius: Maximum distance from elite for minion placement.
        prefer_large_rooms: Whether to prioritize larger rooms for placement.
        formation: Arrangement pattern ('circle', 'cluster', or 'line').
    """

    # Rarity priority for determining elite status (higher = stronger)
    RARITY_PRIORITY = {
        'Boss': 4,
        'Legendary': 3,
        'Rare': 2,
        'Uncommon': 1,
        'Common': 0
    }

    def __init__(
        self,
        elite_radius: int = 3,
        prefer_large_rooms: bool = True,
        formation: str = 'cluster'
    ):
        """
        Initialize the EliteWithGroupStrategy.

        Args:
            elite_radius: Maximum distance from elite for minion placement.
                         Defaults to 3.
            prefer_large_rooms: Whether to prefer larger rooms for elite
                               placement. Defaults to True.
            formation: How to arrange minions around the elite.
                      Options: 'circle', 'cluster', 'line'. Defaults to 'cluster'.

        Raises:
            ValueError: If formation is not one of the valid options.
        """
        valid_formations = ('circle', 'cluster', 'line')
        if formation not in valid_formations:
            raise ValueError(
                f"Invalid formation '{formation}'. "
                f"Must be one of: {valid_formations}"
            )

        self.elite_radius = elite_radius
        self.prefer_large_rooms = prefer_large_rooms
        self.formation = formation

        logger.debug(
            "EliteWithGroupStrategy initialized: radius=%d, prefer_large=%s, formation=%s",
            elite_radius, prefer_large_rooms, formation
        )

    def place_monsters(
        self,
        dungeon_generator: "DungeonGenerator",
        monsters: List[Any]
    ) -> None:
        """
        Place monsters with the strongest as elite surrounded by minions.

        Args:
            dungeon_generator: The dungeon generator instance providing
                map access and placement methods.
            monsters: List of monsters to place. May contain individual
                monsters or lists of monsters (packs).
        """
        if not monsters:
            logger.debug("No monsters to place")
            return

        # Flatten any nested lists (packs) into individual monsters
        flat_monsters = self._flatten_monsters(monsters)

        if not flat_monsters:
            logger.debug("No monsters after flattening")
            return

        logger.info(
            "Placing %d monsters with EliteWithGroupStrategy",
            len(flat_monsters)
        )

        # Separate elite from minions
        elite, minions = self._identify_elite_and_minions(flat_monsters)

        if elite is None:
            logger.warning("Could not identify elite monster, falling back to random placement")
            self._fallback_random_placement(dungeon_generator, flat_monsters)
            return

        # Find suitable room for elite placement
        room = self._select_room(dungeon_generator)
        if room is None:
            logger.warning("No suitable room found, falling back to random placement")
            self._fallback_random_placement(dungeon_generator, flat_monsters)
            return

        # Create spawn condition that avoids corridors and stairs
        spawn_condition = self.make_spawn_condition(
            dungeon_generator,
            avoid_corridors=True,
            avoid_stairs=True
        )

        # Find position for elite within the room
        elite_pos = self._find_elite_position(room, dungeon_generator, spawn_condition)
        if elite_pos is None:
            logger.warning("Could not find elite position, falling back to random placement")
            self._fallback_random_placement(dungeon_generator, flat_monsters)
            return

        # Place the elite
        if self._place_monster_at(elite, elite_pos, dungeon_generator):
            logger.debug(
                "Placed elite '%s' at (%d, %d)",
                self._get_monster_name(elite),
                elite_pos[0], elite_pos[1]
            )
        else:
            logger.warning("Failed to place elite monster")
            self._fallback_random_placement(dungeon_generator, flat_monsters)
            return

        # Generate formation positions for minions
        minion_positions = self._generate_formation_positions(
            elite_pos, len(minions), dungeon_generator, spawn_condition
        )

        # Place minions
        for i, minion in enumerate(minions):
            if i < len(minion_positions):
                pos = minion_positions[i]
                if self._place_monster_at(minion, pos, dungeon_generator):
                    logger.debug(
                        "Placed minion '%s' at (%d, %d)",
                        self._get_monster_name(minion),
                        pos[0], pos[1]
                    )
                else:
                    # Fall back to random placement for this minion
                    self._place_monster_randomly(minion, dungeon_generator, spawn_condition)
            else:
                # Not enough formation positions, use random placement
                self._place_monster_randomly(minion, dungeon_generator, spawn_condition)

        logger.info("Elite group placement complete")

    def _flatten_monsters(self, monsters: List[Any]) -> List[Any]:
        """
        Flatten a list that may contain nested lists (packs) into individual monsters.

        Args:
            monsters: List that may contain monsters or lists of monsters.

        Returns:
            Flattened list of individual monster objects.
        """
        flat = []
        for item in monsters:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        return flat

    def _get_monster_name(self, monster: Any) -> str:
        """
        Get the name of a monster for logging purposes.

        Args:
            monster: The monster object.

        Returns:
            The monster's name as a string.
        """
        if hasattr(monster, 'get_name'):
            return monster.get_name()
        elif hasattr(monster, 'name'):
            return monster.name
        else:
            return str(monster)

    def _identify_elite_and_minions(
        self,
        monsters: List[Any]
    ) -> Tuple[Optional[Any], List[Any]]:
        """
        Identify the strongest monster as elite and the rest as minions.

        Elite is determined by:
        1. Boss flag (if present)
        2. Rarity level
        3. Character level/tier (if available)

        Args:
            monsters: List of monsters to analyze.

        Returns:
            Tuple of (elite_monster, list_of_minions).
        """
        if not monsters:
            return None, []

        if len(monsters) == 1:
            return monsters[0], []

        def get_monster_strength(monster: Any) -> Tuple[int, int, int]:
            """
            Calculate strength score for sorting.

            Returns tuple of (boss_priority, rarity_priority, level) for comparison.
            """
            # Check for boss flag
            boss_priority = 0
            if hasattr(monster, 'rarity'):
                rarity_str = monster.rarity if isinstance(monster.rarity, str) else str(monster.rarity)
                if rarity_str.lower() == 'boss':
                    boss_priority = 1

            # Get rarity priority
            rarity_priority = 0
            if hasattr(monster, 'rarity'):
                rarity = monster.rarity if isinstance(monster.rarity, str) else str(monster.rarity)
                rarity_priority = self.RARITY_PRIORITY.get(rarity, 0)

            # Get level/tier
            level = 0
            if hasattr(monster, 'level'):
                level = monster.level
            elif hasattr(monster, 'get_level'):
                level = monster.get_level()

            return (boss_priority, rarity_priority, level)

        # Sort monsters by strength (strongest first)
        sorted_monsters = sorted(monsters, key=get_monster_strength, reverse=True)

        elite = sorted_monsters[0]
        minions = sorted_monsters[1:]

        logger.debug(
            "Identified elite: '%s', minions count: %d",
            self._get_monster_name(elite),
            len(minions)
        )

        return elite, minions

    def _select_room(
        self,
        dungeon_generator: "DungeonGenerator"
    ) -> Optional["Room"]:
        """
        Select a suitable room for elite placement.

        Args:
            dungeon_generator: The dungeon generator instance.

        Returns:
            Selected Room object, or None if no suitable room found.
        """
        # Access rooms from the tile_map
        tile_map = getattr(dungeon_generator, 'tile_map', None)
        if tile_map is None:
            logger.debug("No tile_map available in dungeon_generator")
            return None

        rooms = getattr(tile_map, 'rooms', [])

        if not rooms:
            logger.debug("No rooms available in tile_map")
            return None

        if self.prefer_large_rooms:
            # Sort rooms by area (largest first)
            sorted_rooms = sorted(
                rooms,
                key=lambda r: r.width * r.height,
                reverse=True
            )
            # Pick from top 50% of largest rooms with some randomness
            top_rooms = sorted_rooms[:max(1, len(sorted_rooms) // 2)]
            selected = random.choice(top_rooms)
        else:
            selected = random.choice(rooms)

        logger.debug(
            "Selected room at (%d, %d), size %dx%d",
            selected.x, selected.y, selected.width, selected.height
        )

        return selected

    def _find_elite_position(
        self,
        room: "Room",
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> Optional[Tuple[int, int]]:
        """
        Find a suitable position for the elite within the room.

        Prefers the center of the room if available.

        Args:
            room: The room to search in.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            Tuple (x, y) position, or None if no position found.
        """
        center_x = room.GetCenterX()
        center_y = room.GetCenterY()

        # Try center first
        if self._is_valid_elite_position(center_x, center_y, dungeon_generator, condition):
            return (center_x, center_y)

        # Spiral outward from center
        for radius in range(1, max(room.width, room.height) // 2 + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:
                        x, y = center_x + dx, center_y + dy
                        if self._is_valid_elite_position(x, y, dungeon_generator, condition):
                            return (x, y)

        logger.debug("No valid elite position found in room")
        return None

    def _is_valid_elite_position(
        self,
        x: int,
        y: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> bool:
        """
        Check if a position is valid for elite placement.

        Args:
            x: X coordinate.
            y: Y coordinate.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            True if position is valid for elite placement.
        """
        # Check passability
        if not dungeon_generator.get_passable((x, y)):
            return False

        # Check spawn condition (avoids corridors and stairs)
        if not condition((x, y)):
            return False

        # Check if location is not already occupied by a monster
        monster_map = getattr(dungeon_generator, 'monster_map', None)
        if monster_map is not None:
            if hasattr(monster_map, 'get_has_entity'):
                if monster_map.get_has_entity(x, y):
                    return False
            elif hasattr(monster_map, 'get_has_no_entity'):
                if not monster_map.get_has_no_entity(x, y):
                    return False

        return True

    def _generate_formation_positions(
        self,
        elite_pos: Tuple[int, int],
        minion_count: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> List[Tuple[int, int]]:
        """
        Generate positions for minions based on formation type.

        Args:
            elite_pos: Position of the elite monster.
            minion_count: Number of minions to position.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            List of (x, y) positions for minions.
        """
        if self.formation == 'circle':
            return self._generate_circle_formation(
                elite_pos, minion_count, dungeon_generator, condition
            )
        elif self.formation == 'line':
            return self._generate_line_formation(
                elite_pos, minion_count, dungeon_generator, condition
            )
        else:  # cluster
            return self._generate_cluster_formation(
                elite_pos, minion_count, dungeon_generator, condition
            )

    def _generate_circle_formation(
        self,
        center: Tuple[int, int],
        count: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> List[Tuple[int, int]]:
        """
        Generate positions in a circle around the center.

        Args:
            center: Center position (elite location).
            count: Number of positions to generate.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            List of valid positions in circular arrangement.
        """
        positions: List[Tuple[int, int]] = []
        center_x, center_y = center

        if count == 0:
            return positions

        # Calculate angle between each minion
        angle_step = (2 * math.pi) / count

        for radius in range(1, self.elite_radius + 1):
            for i in range(count - len(positions)):
                angle = angle_step * (i + len(positions))
                x = center_x + int(round(radius * math.cos(angle)))
                y = center_y + int(round(radius * math.sin(angle)))

                if (x, y) not in positions:
                    if self._is_valid_minion_position(x, y, dungeon_generator, condition, positions):
                        positions.append((x, y))

                if len(positions) >= count:
                    break

            if len(positions) >= count:
                break

        logger.debug("Generated %d circle formation positions", len(positions))
        return positions

    def _generate_cluster_formation(
        self,
        center: Tuple[int, int],
        count: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> List[Tuple[int, int]]:
        """
        Generate positions in a random cluster around the center.

        Args:
            center: Center position (elite location).
            count: Number of positions to generate.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            List of valid positions in cluster arrangement.
        """
        center_x, center_y = center

        # Generate all valid positions within radius
        candidate_positions: List[Tuple[int, int]] = []
        for dx in range(-self.elite_radius, self.elite_radius + 1):
            for dy in range(-self.elite_radius, self.elite_radius + 1):
                if dx == 0 and dy == 0:
                    continue  # Skip elite position

                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= self.elite_radius:
                    x, y = center_x + dx, center_y + dy
                    if self._is_valid_minion_position(x, y, dungeon_generator, condition, []):
                        candidate_positions.append((x, y))

        # Shuffle and pick required number
        random.shuffle(candidate_positions)
        positions = candidate_positions[:count]

        logger.debug("Generated %d cluster formation positions", len(positions))
        return positions

    def _generate_line_formation(
        self,
        center: Tuple[int, int],
        count: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> List[Tuple[int, int]]:
        """
        Generate positions in a line from the center.

        The line direction is chosen randomly from valid directions.

        Args:
            center: Center position (elite location).
            count: Number of positions to generate.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            List of valid positions in line arrangement.
        """
        positions: List[Tuple[int, int]] = []
        center_x, center_y = center

        # Try different directions (8-directional)
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            line_positions: List[Tuple[int, int]] = []
            for distance in range(1, self.elite_radius + 1):
                x = center_x + dx * distance
                y = center_y + dy * distance
                if self._is_valid_minion_position(x, y, dungeon_generator, condition, line_positions):
                    line_positions.append((x, y))

            if len(line_positions) >= count:
                positions = line_positions[:count]
                break
            elif len(line_positions) > len(positions):
                positions = line_positions

        # If single direction not enough, try bidirectional line
        if len(positions) < count:
            for dx, dy in directions:
                line_positions = []
                # Extend in positive direction
                for distance in range(1, self.elite_radius + 1):
                    x = center_x + dx * distance
                    y = center_y + dy * distance
                    if self._is_valid_minion_position(x, y, dungeon_generator, condition, line_positions):
                        line_positions.append((x, y))
                # Extend in negative direction
                for distance in range(1, self.elite_radius + 1):
                    x = center_x - dx * distance
                    y = center_y - dy * distance
                    if self._is_valid_minion_position(x, y, dungeon_generator, condition, line_positions):
                        line_positions.append((x, y))

                if len(line_positions) >= count:
                    positions = line_positions[:count]
                    break

        logger.debug("Generated %d line formation positions", len(positions))
        return positions

    def _is_valid_minion_position(
        self,
        x: int,
        y: int,
        dungeon_generator: "DungeonGenerator",
        condition: Any,
        already_placed: List[Tuple[int, int]]
    ) -> bool:
        """
        Check if a position is valid for minion placement.

        Args:
            x: X coordinate.
            y: Y coordinate.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.
            already_placed: List of positions already assigned to other minions.

        Returns:
            True if position is valid for minion placement.
        """
        # Check if already assigned
        if (x, y) in already_placed:
            return False

        # Check passability
        if not dungeon_generator.get_passable((x, y)):
            return False

        # Check spawn condition
        if not condition((x, y)):
            return False

        # Check if location is not already occupied by a monster
        monster_map = getattr(dungeon_generator, 'monster_map', None)
        if monster_map is not None:
            if hasattr(monster_map, 'get_has_entity'):
                if monster_map.get_has_entity(x, y):
                    return False
            elif hasattr(monster_map, 'get_has_no_entity'):
                if not monster_map.get_has_no_entity(x, y):
                    return False

        return True

    def _place_monster_at(
        self,
        monster: Any,
        position: Tuple[int, int],
        dungeon_generator: "DungeonGenerator"
    ) -> bool:
        """
        Place a monster at the specified position.

        Args:
            monster: The monster object to place.
            position: Tuple (x, y) of the target position.
            dungeon_generator: The dungeon generator instance.

        Returns:
            True if placement was successful.
        """
        x, y = position

        # Update monster's location
        if hasattr(monster, 'set_location'):
            monster.set_location(x, y)
        else:
            monster.x = x
            monster.y = y

        # Update the monster map
        monster_map = getattr(dungeon_generator, 'monster_map', None)
        if monster_map is not None:
            if hasattr(monster_map, 'place_entity'):
                return monster_map.place_entity(x, y, monster)

        return True

    def _place_monster_randomly(
        self,
        monster: Any,
        dungeon_generator: "DungeonGenerator",
        condition: Any
    ) -> bool:
        """
        Place a monster at a random valid location.

        Args:
            monster: The monster to place.
            dungeon_generator: The dungeon generator instance.
            condition: Spawn condition function.

        Returns:
            True if placement was successful.
        """
        pos = self.find_valid_location(dungeon_generator, condition)
        if pos is not None:
            if self._place_monster_at(monster, pos, dungeon_generator):
                logger.debug(
                    "Placed '%s' at random position (%d, %d)",
                    self._get_monster_name(monster),
                    pos[0], pos[1]
                )
                return True
        return False

    def _fallback_random_placement(
        self,
        dungeon_generator: "DungeonGenerator",
        monsters: List[Any]
    ) -> None:
        """
        Fall back to random placement for all monsters.

        Used when the elite/group strategy cannot be applied.

        Args:
            dungeon_generator: The dungeon generator instance.
            monsters: List of monsters to place.
        """
        logger.debug("Using fallback random placement for %d monsters", len(monsters))

        # Create condition avoiding stairs
        condition = self.make_spawn_condition(
            dungeon_generator,
            avoid_corridors=False,
            avoid_stairs=True
        )

        placed_count = 0
        for monster in monsters:
            if self._place_monster_randomly(monster, dungeon_generator, condition):
                placed_count += 1

        logger.debug("Fallback placement: placed %d/%d monsters", placed_count, len(monsters))

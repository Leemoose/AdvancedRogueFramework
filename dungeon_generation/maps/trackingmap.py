"""
TrackingMap Module
==================

This map tracks items or monsters using an ID dictionary system.
"""

from logging_config import get_logger

from .id import ID
from .maps import Maps

logger = get_logger(__name__)


class TrackingMap(Maps):
    """
    Map that tracks entities (items or monsters) using unique IDs.

    Entities are stored in a dictionary and their IDs are placed on the map grid.
    """

    def __init__(self, width: int, height: int):
        logger.debug("Initializing TrackingMap: %dx%d", width, height)
        super().__init__(width, height)
        self.dict = ID()  # Unique to this floor
        logger.debug("TrackingMap initialized with empty ID dictionary")

    def place_thing(self, thing) -> None:
        """
        Place an entity on the map and register it with the ID system.

        Args:
            thing: Entity with x, y coordinates and ability to receive ID
        """
        logger.debug("place_thing: Placing %s at (%d, %d)", type(thing).__name__, thing.x, thing.y)
        self.dict.tag_subject(thing)
        self.place_entity(thing.x, thing.y, thing.get_id_tag())
        logger.debug("place_thing: %s assigned ID %d", type(thing).__name__, thing.get_id_tag())

    def get_num_entities(self) -> int:
        """Return the number of entities currently tracked."""
        count = self.dict.num_entities()
        logger.debug("get_num_entities: %d entities tracked", count)
        return count

    def remove_thing(self, thing):
        """
        Remove an entity from the map and ID system.

        Args:
            thing: Entity to remove (must have id_tag)

        Returns:
            The removed entity
        """
        logger.debug("remove_thing: Removing %s (ID=%d) from (%d, %d)",
                    type(thing).__name__, thing.id_tag, thing.x, thing.y)
        self.clear_entity(thing.x, thing.y)
        removed = self.dict.remove_subject(thing.id_tag)
        logger.debug("remove_thing: Successfully removed %s", type(removed).__name__)
        return removed

    def move_entity(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Move an entity from one location to another.

        Args:
            x1, y1: Source coordinates
            x2, y2: Destination coordinates
        """
        logger.debug("move_entity: Moving from (%d, %d) to (%d, %d)", x1, y1, x2, y2)
        entity_id = super().get_entity(x1, y1)
        self.place_entity(x2, y2, entity_id)
        self.clear_entity(x1, y1)
        logger.debug("move_entity: Entity ID %r moved successfully", entity_id)

    def get_entity(self, x: int, y: int):
        """
        Get the actual entity object at coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Entity object at (x, y) or -1 if no entity
        """
        if self.get_has_no_entity(x, y):
            logger.debug("get_entity(%d, %d): No entity", x, y)
            return -1
        else:
            entity_id = super().get_entity(x, y)
            entity = self.dict.get_subject(entity_id)
            logger.debug("get_entity(%d, %d): Found %s (ID=%r)",
                        x, y, type(entity).__name__, entity_id)
            return entity

    def get_all_entities(self) -> list:
        """Return list of all tracked entities."""
        entities = self.dict.all_entities()
        logger.debug("get_all_entities: Returning %d entities", len(entities))
        return entities

    def get_nearest_entity(self, x: int, y: int):
        """
        Find the entity nearest to the given coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Nearest entity or None if no entities exist
        """
        logger.debug("get_nearest_entity: Searching from (%d, %d)", x, y)
        lowest_distance = 10000
        closest_entity = None

        for entity in self.get_all_entities():
            distance = entity.get_distance(x, y)
            if distance < lowest_distance:
                lowest_distance = distance
                closest_entity = entity

        if closest_entity:
            logger.debug("get_nearest_entity: Found %s at distance %.2f",
                        type(closest_entity).__name__, lowest_distance)
        else:
            logger.debug("get_nearest_entity: No entities found")

        return closest_entity

    def __str__(self) -> str:
        """Return string representation of tracked entities."""
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.entity_map[x][y].render_tag) for y in range(self.height))
            allrows = allrows + row + "\n"
        return allrows

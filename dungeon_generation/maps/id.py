"""
ID Module
=========

ID tracking system for uniquely identifying entities (monsters and items).
"""

from logging_config import get_logger, log_high_priority
from src.core.constants import NO_ENTITY

logger = get_logger(__name__)


class ID:
    """
    ID management system for tracking unique entities.

    All unique entities (monsters and items) are tagged with an ID and stored
    in a dictionary. IDs are used in arrays and other data structures, and
    the ID can be used to retrieve the actual object.
    """

    def __init__(self):
        logger.debug("Initializing ID system")
        self.subjects = {}
        self.ID_count = 0

    def __str__(self) -> str:
        allrows = ""
        for entity in self.all_entities():
            allrows += ' '.join("Entity: {}, ID: {} \n".format(entity, entity.id_tag))
        return allrows

    def tag_subject(self, subject) -> None:
        """
        Assign a unique ID to a subject and register it.

        Args:
            subject: Entity to tag (must have gain_ID method)
        """
        self.ID_count += 1
        logger.debug("tag_subject: Assigning ID %d to %s", self.ID_count, type(subject).__name__)
        subject.gain_ID(self.ID_count)
        self.add_subject(subject)

    def get_subject(self, key: int):
        """
        Retrieve a subject by its ID.

        Args:
            key: The ID of the subject to retrieve

        Returns:
            The subject with the given ID

        Raises:
            Exception: If key is -1 or not found in subjects
        """
        if key in self.subjects:
            logger.debug("get_subject: Retrieved subject with ID %d", key)
            return self.subjects[key]
        elif key == NO_ENTITY:
            log_high_priority(logger, "get_subject: Attempted to get subject with NO_ENTITY ID (invalid)")
            return None
        else:
            log_high_priority(logger, "get_subject: ID %d not found in subjects", key)
            return None

    def remove_subject(self, key: int):
        """
        Remove and return a subject by its ID.

        Args:
            key: The ID of the subject to remove

        Returns:
            The removed subject

        Raises:
            Exception: If key is -1 or not found in subjects
        """
        if key in self.subjects:
            removed = self.subjects.pop(key)
            logger.debug("remove_subject: Removed subject with ID %d (%s)",
                        key, type(removed).__name__)
            return removed
        elif key == NO_ENTITY:
            log_high_priority(logger, "remove_subject: Attempted to remove subject with NO_ENTITY ID (invalid)")
            return None
        else:
            log_high_priority(logger, "remove_subject: ID %d not found in subjects", key)
            return None

    def add_subject(self, subject) -> None:
        """
        Add a subject to the tracking dictionary.

        Args:
            subject: Entity with id_tag attribute to add
        """
        logger.debug("add_subject: Adding %s with ID %d",
                    type(subject).__name__, subject.id_tag)
        self.subjects[subject.id_tag] = subject

    def all_entities(self) -> list:
        """Return a list of all tracked entities."""
        entities = list(self.subjects.values())
        logger.debug("all_entities: Returning %d entities", len(entities))
        return entities

    def num_entities(self) -> int:
        """Return the count of tracked entities."""
        return len(self.subjects)

    def has_subject(self, key: int) -> bool:
        """
        Check if a subject with the given ID exists.

        Args:
            key: The ID to check

        Returns:
            True if subject exists, False otherwise
        """
        return key in self.subjects

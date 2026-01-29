import copy
import random


class BaseSpawnParams:
    """Base class for all spawn parameter configurations."""

    def __init__(self, entity, minFloor=1, maxFloor=10, branch="all"):
        self.entity = entity
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.branch = branch

    def allowed_at_depth(self, depth: int, branch: str = "all") -> bool:
        """Check if this entity can spawn at the given depth and branch."""
        return (depth >= self.minFloor and
                depth <= self.maxFloor and
                (self.branch == "all" or self.branch == branch))

    def get_fresh_copy(self):
        """Return a deep copy of the entity."""
        return copy.deepcopy(self.entity)


class SpawnParams(BaseSpawnParams):
    """Generic spawn parameters for entities."""

    def __init__(self, entity, minFloor=1, maxFloor=10, branch="all"):
        super().__init__(entity, minFloor, maxFloor, branch)

    # Backward compatibility aliases
    def AllowedAtDepth(self, depth, branch="all"):
        """Backward compatible alias for allowed_at_depth."""
        return self.allowed_at_depth(depth, branch)

    def GetFreshCopy(self):
        """Backward compatible alias for get_fresh_copy."""
        return self.get_fresh_copy()


class InteractableSpawnParams(SpawnParams):
    """Spawn parameters for interactable entities."""

    def __init__(self, entity, minFloor=1, maxFloor=10, branch="all"):
        super().__init__(entity, minFloor, maxFloor, branch)


class ItemSpawnParams(BaseSpawnParams):
    """Spawn parameters for items."""

    def __init__(self, item, minFloor=1, maxFloor=10, branch="all"):
        super().__init__(item, minFloor, maxFloor, branch)
        # Backward compatibility: expose entity as item
        self.item = self.entity

    # Backward compatibility aliases
    def AllowedAtDepth(self, depth, branch="all"):
        """Backward compatible alias for allowed_at_depth."""
        return self.allowed_at_depth(depth, branch)

    def GetFreshCopy(self):
        """Backward compatible alias for get_fresh_copy."""
        return self.get_fresh_copy()


class MonsterSpawnParams(BaseSpawnParams):
    """Spawn parameters for monsters with additional attributes."""

    def __init__(self, monster, minFloor=1, maxFloor=10, branch="Dungeon", rarity="Common", group=None, boss=False):
        super().__init__(monster, minFloor, maxFloor, branch)
        # Backward compatibility: expose entity as monster
        self.monster = self.entity
        self.rarity = rarity
        self.group = group
        self.boss = boss

    # Backward compatibility aliases
    def AllowedAtDepth(self, depth, branch="Dungeon"):
        """Backward compatible alias for allowed_at_depth."""
        return self.allowed_at_depth(depth, branch)

    def GetLeveledCopy(self, depth):
        """Return a deep copy of the monster with level adjustments based on depth."""
        copied = copy.deepcopy(self.monster)

        for _ in range(depth):
            if (depth % 2 == 1):
                copied.character.level_up(1, 0, 1, 0)
            else:
                copied.character.level_up(0, 1, 0, 1)
        return copied


class BossSpawnParams(MonsterSpawnParams):
    """Spawn parameters for boss monsters."""

    def __init__(self, monster, depth, branch="Dungeon", rarity="Common", group=None):
        super().__init__(monster, minFloor=depth, maxFloor=depth, branch=branch, rarity=rarity, group=group, boss=True)

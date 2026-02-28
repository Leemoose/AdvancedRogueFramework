"""
SpellContext - Contains all context needed for spell execution.

Passed to effects so they can access caster stats, the game loop,
and accumulate messages.
"""

from typing import Optional, List, Any
from logging_config import get_logger

logger = get_logger(__name__)


class SpellContext:
    """
    Context object passed to all effects during spell execution.

    Provides access to:
    - Caster and their stats
    - Game loop and maps
    - Skill bonuses for scaling
    - Message accumulation
    """

    def __init__(self, caster, loop, target=None):
        """
        Initialize spell context.

        Args:
            caster: The entity casting the spell
            loop: The game loop (provides access to maps, generator, etc.)
            target: Raw target from input - can be entity, position tuple, or None
        """
        self.caster = caster
        self.loop = loop
        self.target = target
        self.messages: List[str] = []

    def get_skill_damage_bonus(self) -> int:
        """Get caster's bonus damage from skills/intelligence."""
        if hasattr(self.caster, 'character') and hasattr(self.caster.character, 'skill_damage_increase'):
            return self.caster.character.skill_damage_increase()
        return 0

    def get_skill_duration_bonus(self) -> int:
        """Get caster's bonus duration from skills/intelligence."""
        if hasattr(self.caster, 'character') and hasattr(self.caster.character, 'skill_duration_increase'):
            return self.caster.character.skill_duration_increase()
        return 0

    def add_message(self, msg: str):
        """Add a message to be displayed to the player."""
        self.messages.append(msg)
        logger.debug(f"Spell message: {msg}")

    @property
    def generator(self):
        """Shortcut to access the dungeon generator."""
        return self.loop.generator

    @property
    def tile_map(self):
        """Shortcut to access the tile map."""
        return self.loop.generator.tile_map

    @property
    def monster_map(self):
        """Shortcut to access the monster map."""
        return self.loop.generator.monster_map

    def get_passable(self, x: int, y: int) -> bool:
        """Check if a tile is passable."""
        return self.tile_map.get_passable(x, y)

    def has_entity_at(self, x: int, y: int) -> bool:
        """Check if there's an entity at position."""
        return not self.monster_map.get_has_no_entity(x, y)

    def get_entity_at(self, x: int, y: int) -> Optional[Any]:
        """Get entity at position, or None."""
        if self.has_entity_at(x, y):
            return self.monster_map.locate(x, y)
        return None

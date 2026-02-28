"""
BaseSpell - Base class for the class-based spell system.

Each spell is defined as a class that inherits from BaseSpell and specifies
its effects, targeting, and other properties as class attributes.

Example:
    class BurningAttack(BaseSpell):
        name = "Burning Attack"
        cost = 5
        cooldown = 10
        range = 5

        effects = [
            DamageEffect(base=3, damage_type="fire"),
            ApplyStatusEffect(Burn, duration=5, damage=3)
        ]
"""

from typing import List, Optional, Any
from .context import SpellContext
from .targeting import get_single_target, TargetType
from logging_config import get_logger

logger = get_logger(__name__)


class BaseSpell:
    """
    Base class for all spells in the class-based spell system.

    Subclasses define spell properties as class attributes and can override
    methods for custom behavior.

    Class Attributes:
        name: Display name of the spell
        cost: Mana cost to cast
        cooldown: Turns before spell can be cast again
        range: Maximum casting range (-1 for unlimited, 0 for self)
        action_cost: Energy/AP cost to cast
        icon: Render tag for UI display
        required_intelligence: Minimum INT to learn this spell
        target_type: How the spell selects targets (from TargetType enum)
        effects: List of Effect instances to apply to targets
        terrain_effects: List of Effect instances to apply to terrain positions
    """

    # Spell metadata
    name: str = "Unnamed Spell"
    description_text: str = ""
    school: str = "general"

    # Costs and cooldowns
    cost: int = 5
    cooldown: int = 10
    range: int = 5
    action_cost: int = 50

    # UI/display
    icon: int = 9100

    # Requirements
    required_intelligence: int = 0

    # Targeting
    target_type: TargetType = TargetType.SINGLE_ENEMY

    # Effects to apply
    effects: List[Any] = []
    terrain_effects: List[Any] = []

    def __init__(self, caster):
        """
        Create a spell instance bound to a caster.

        Args:
            caster: The entity that owns this spell
        """
        self.caster = caster
        self.ready: int = 0  # Cooldown tracker, 0 = ready

    # ---- Properties for compatibility with existing system ----

    @property
    def targetted(self) -> bool:
        """Whether this spell requires a target."""
        return self.target_type not in (TargetType.SELF, TargetType.NONE)

    @property
    def targets_monster(self) -> bool:
        """Whether this spell targets enemies."""
        return self.target_type == TargetType.SINGLE_ENEMY

    @property
    def targets_ground(self) -> bool:
        """Whether this spell targets ground positions."""
        return self.target_type == TargetType.GROUND

    @property
    def render_tag(self) -> int:
        """Render tag for UI (alias for icon)."""
        return self.icon

    # ---- Cooldown management ----

    def tick_cooldown(self):
        """Reduce cooldown by 1 turn."""
        if self.ready > 0:
            self.ready -= 1

    def reset_cooldown(self):
        """Reset cooldown to 0."""
        self.ready = 0

    def is_ready(self) -> bool:
        """Check if spell is off cooldown."""
        return self.ready == 0

    # ---- Targeting ----

    def get_targets(self, target, context: SpellContext) -> List:
        """
        Get the list of entity targets for this spell.

        Override this method for custom targeting logic (e.g., AoE spells).
        Default implementation returns single target.

        Args:
            target: Raw target from input (entity or position)
            context: SpellContext

        Returns:
            List of entities to apply effects to
        """
        return get_single_target(target, context)

    def get_terrain_targets(self, target, context: SpellContext) -> List:
        """
        Get the list of terrain positions for this spell.

        Override this method for spells that modify terrain.
        Default implementation returns empty list.

        Args:
            target: Raw target from input (entity or position)
            context: SpellContext

        Returns:
            List of (x, y) positions to apply terrain effects to
        """
        return []

    # ---- Casting ----

    def castable(self, target=None) -> bool:
        """
        Check if the spell can be cast.

        Args:
            target: Optional target to check range against

        Returns:
            True if spell can be cast
        """
        if not self.is_ready():
            return False

        if self.caster.character.get_mana() < self.cost:
            return False

        if target is not None and self.targetted:
            if not self.in_range(target):
                return False

        return True

    def in_range(self, target) -> bool:
        """
        Check if target is within spell range.

        Args:
            target: Target to check (entity or position)

        Returns:
            True if target is in range
        """
        if self.range == -1:  # Unlimited range
            return True

        if isinstance(target, tuple):
            target_x, target_y = target
        else:
            target_x, target_y = target.get_location()

        distance = self.caster.get_distance(target_x, target_y)
        return distance <= self.range

    def try_to_activate(self, target, loop) -> bool:
        """
        Attempt to cast the spell.

        Args:
            target: The target (entity, position, or None)
            loop: Game loop

        Returns:
            True if spell was cast successfully
        """
        if not self.castable(target):
            loop.add_message("You were unable to cast the spell.")
            return False

        self.ready = self.cooldown
        logger.info(f"Spell {self.name} activated by {self.caster.name}")
        return self.activate(target, loop)

    def activate(self, target, loop) -> bool:
        """
        Execute the spell.

        This is the main casting method. Override for complex custom behavior.
        Default implementation applies all effects to targets.

        Args:
            target: The target (entity, position, or None)
            loop: Game loop

        Returns:
            True if spell executed successfully
        """
        # Create context
        context = SpellContext(self.caster, loop, target)

        # Deduct mana cost
        self.caster.character.mana -= self.cost

        # Get targets
        entity_targets = self.get_targets(target, context)
        terrain_targets = self.get_terrain_targets(target, context)

        # Apply entity effects
        for t in entity_targets:
            for effect in self.effects:
                effect.apply(t, context)

        # Apply terrain effects
        for pos in terrain_targets:
            for effect in self.terrain_effects:
                effect.apply(pos, context)

        # Add any accumulated messages
        for msg in context.messages:
            loop.add_message(msg)

        return True

    # ---- Display ----

    def description(self) -> str:
        """Short description for spell list."""
        return f"{self.name} ({self.cost} mana, {self.cooldown} turn cd)"

    def full_description(self) -> str:
        """
        Full description for spell details.

        Override this for custom descriptions.
        """
        if self.description_text:
            return self.description_text
        return self.description()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(caster={self.caster.name})"

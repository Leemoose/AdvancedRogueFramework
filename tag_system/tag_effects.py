"""
TagEffectRegistry - maps PotionTag + UsageContext to effect callables.

Each tag can produce a different effect depending on how the potion is used:
drink, throw, or apply to equipment.

Effect functions have signature: (target, loop) -> None
  - For DRINK: target is the entity drinking
  - For THROW: target is the entity or tile hit
  - For APPLY: target is the equipment being coated
"""

from enum import Enum
from tag_system.tag_manager import PotionTag

class UsageContext(Enum):
    DRINK = "drink"
    THROW = "throw"
    APPLY = "apply"

class TagEffectRegistry:
    """
    Maps (PotionTag, UsageContext) pairs to callables that produce effects.

    Registry is class-level so it survives serialization without being
    stored on potion instances.
    """

    _registry = {}

    @classmethod
    def register(cls, tag, context, effect_fn):
        """
        Register an effect function for a tag + context pair.

        Args:
            tag: PotionTag enum value
            context: UsageContext enum value
            effect_fn: callable with signature (target, loop) -> None
        """
        cls._registry[(tag, context)] = effect_fn

    @classmethod
    def get_effects(cls, tags, context):
        """
        Return all effect functions for a set of tags in a given context.

        Args:
            tags: list of PotionTag values
            context: UsageContext enum value

        Returns:
            list of callables
        """
        effects = []
        for tag in tags:
            key = (tag, context)
            if key in cls._registry:
                effects.append(cls._registry[key])
        return effects

    @classmethod
    def apply_effects(cls, tags, context, target, loop):
        """
        Resolve and apply all effects for the given tags + context.

        Args:
            tags: list of PotionTag values
            context: UsageContext enum value
            target: entity, tile, or equipment depending on context
            loop: the Loops instance
        """
        effects = cls.get_effects(tags, context)
        for effect_fn in effects:
            effect_fn(target, loop)

    @classmethod
    def has_effects(cls, tags, context):
        """Check if any of the given tags have registered effects for this context."""
        for tag in tags:
            if (tag, context) in cls._registry:
                return True
        return False

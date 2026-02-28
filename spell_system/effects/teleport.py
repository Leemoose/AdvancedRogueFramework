"""
Teleportation effects - move entities to new locations.
"""

from .base import Effect
from logging_config import get_logger

logger = get_logger(__name__)


class TeleportToTargetEffect(Effect):
    """
    Teleport the caster to adjacent to a target entity.
    Used for blink-strike type abilities.
    """

    def __init__(self):
        pass

    def apply(self, target, context) -> bool:
        """Teleport caster adjacent to target."""
        if target is None:
            logger.warning("TeleportToTargetEffect: No target provided")
            return False

        caster = context.caster
        tx, ty = target.get_location()

        # Find adjacent empty tile to the target
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = tx + dx, ty + dy
            if context.get_passable(nx, ny) and not context.has_entity_at(nx, ny):
                old_x, old_y = caster.get_location()

                # Update monster map if caster is tracked there
                if hasattr(caster, 'traits') and caster.traits.get('monster'):
                    context.monster_map.move_entity(old_x, old_y, nx, ny)

                caster.set_location(nx, ny)
                context.add_message(f"{caster.name} blinks to {target.name}!")
                logger.debug(f"TeleportToTargetEffect: {caster.name} teleported from ({old_x}, {old_y}) to ({nx}, {ny})")
                return True

        context.add_message("No space to teleport to!")
        return False

    def __repr__(self):
        return "TeleportToTargetEffect()"


class TeleportToPositionEffect(Effect):
    """
    Teleport the caster to a target position.
    Used for blink/short-range teleport abilities.
    """

    def __init__(self):
        pass

    def apply(self, position, context) -> bool:
        """Teleport caster to position."""
        if position is None:
            logger.warning("TeleportToPositionEffect: No position provided")
            return False

        if isinstance(position, tuple):
            tx, ty = position
        else:
            # Position might be an entity - get its location
            tx, ty = position.get_location()

        caster = context.caster

        # Check if position is valid
        if not context.get_passable(tx, ty):
            context.add_message("Cannot teleport there - blocked!")
            return False

        if context.has_entity_at(tx, ty):
            context.add_message("Cannot teleport there - occupied!")
            return False

        old_x, old_y = caster.get_location()
        caster.set_location(tx, ty)
        context.add_message(f"{caster.name} teleports!")
        logger.debug(f"TeleportToPositionEffect: {caster.name} teleported from ({old_x}, {old_y}) to ({tx}, {ty})")

        return True

    def __repr__(self):
        return "TeleportToPositionEffect()"


class TeleportRandomEffect(Effect):
    """
    Teleport an entity to a random valid location.

    Args:
        target_self: If True, teleport caster. If False, teleport the target.
    """

    def __init__(self, target_self: bool = True):
        self.target_self = target_self

    def apply(self, target, context) -> bool:
        """Teleport entity to random location."""
        entity = context.caster if self.target_self else target

        if entity is None:
            logger.warning("TeleportRandomEffect: No entity to teleport")
            return False

        new_pos = context.generator.get_random_position()
        if new_pos:
            old_x, old_y = entity.get_location()
            entity.set_location(new_pos[0], new_pos[1])
            context.add_message(f"{entity.name} teleports to a random location!")
            logger.debug(f"TeleportRandomEffect: {entity.name} teleported from ({old_x}, {old_y}) to {new_pos}")
            return True

        context.add_message("The teleport fizzles...")
        return False

    def __repr__(self):
        return f"TeleportRandomEffect(target_self={self.target_self})"


class SwapPositionsEffect(Effect):
    """
    Swap positions between caster and target.
    """

    def __init__(self):
        pass

    def apply(self, target, context) -> bool:
        """Swap caster and target positions."""
        if target is None:
            logger.warning("SwapPositionsEffect: No target provided")
            return False

        caster = context.caster
        cx, cy = caster.get_location()
        tx, ty = target.get_location()

        caster.set_location(tx, ty)
        target.set_location(cx, cy)

        context.add_message(f"{caster.name} swaps places with {target.name}!")
        logger.debug(f"SwapPositionsEffect: Swapped {caster.name} and {target.name}")

        return True

    def __repr__(self):
        return "SwapPositionsEffect()"


class TeleportDownward(Effect):
    """
    Teleports to location on next floor
    """

    def __init__(self):
        pass

    def apply(self, target, context) -> bool:
        """Swap caster and target positions."""
        if target is None:
            logger.warning("TeleportDownward: No target provided")
            return False

        caster = context.caster
        if target.has_trait("player"):
            context.loop.change_floor()
            return True
        else:
            #Needs to be able to handle monsters
            return False

    def __repr__(self):
        return "TeleportDownward()"
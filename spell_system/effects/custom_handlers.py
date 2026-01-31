"""
Custom effect handlers for spells that need special logic.

These are the escape hatches for effects too complex to express in data.
Each handler receives (context, params) and returns True/False.

To add a new custom handler:
1. Define a function here with signature: handler(context, params) -> bool
2. Reference it in spell data: {type: custom, handler: your_handler_name}
"""

from logging_config import get_logger

logger = get_logger(__name__)


def teleport_random(context, params) -> bool:
    """Teleport the target (or caster) to a random location."""
    target_type = params.get('target', 'self')

    if target_type == 'self':
        entity = context.caster
    else:
        entity = context.target
        if entity is None:
            return False

    # Get a random valid position from the map
    generator = context.loop.generator
    new_pos = generator.get_random_position()

    if new_pos:
        old_x, old_y = entity.get_location()
        entity.set_location(new_pos[0], new_pos[1])
        context.add_message(f"{entity.name} teleports!")
        logger.debug(f"{entity.name} teleported from ({old_x}, {old_y}) to {new_pos}")
        return True

    context.add_message("The teleport fizzles...")
    return False


def blink_direction(context, params) -> bool:
    """Short-range directional teleport to a target location."""
    if context.target is None:
        return False

    caster = context.caster
    generator = context.loop.generator

    # Get target location (blink targets ground)
    if isinstance(context.target, tuple):
        tx, ty = context.target
    else:
        tx, ty = context.target.get_location()

    # Check if target location is valid
    if generator.get_passable((tx, ty)) and generator.monster_map.get_has_no_entity(tx, ty):
        old_x, old_y = caster.get_location()
        caster.set_location(tx, ty)
        context.add_message(f"{caster.name} blinks to a new location!")
        logger.debug(f"{caster.name} blinked from ({old_x}, {old_y}) to ({tx}, {ty})")
        return True

    context.add_message("Cannot blink there!")
    return False


def swap_positions(context, params) -> bool:
    """Swap positions with the target."""
    if context.target is None:
        return False

    caster = context.caster
    target = context.target

    cx, cy = caster.get_location()
    tx, ty = target.get_location()

    caster.set_location(tx, ty)
    target.set_location(cx, cy)

    context.add_message(f"{caster.name} swaps places with {target.name}!")
    return True


def aoe_damage(context, params) -> bool:
    """
    Deal damage in an area around the target or caster.

    Params:
        amount: Base damage
        radius: Area radius
        center: "target" or "caster" (default: "target")
        include_caster: Whether to damage caster if in range (default: False)
    """
    amount = params.get('amount', 10)
    radius = params.get('radius', 2)
    center_type = params.get('center', 'target')
    include_caster = params.get('include_caster', False)
    scales = params.get('scales_with_intelligence', False)

    if scales:
        amount += context.get_skill_damage_bonus()

    # Determine center point
    if center_type == 'caster':
        center = context.caster.get_location()
    elif isinstance(context.target, tuple):
        center = context.target
    elif context.target:
        center = context.target.get_location()
    else:
        return False

    cx, cy = center

    # Get all entities in range
    monster_map = context.loop.generator.monster_map
    hit_count = 0

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue  # Circle, not square

            x, y = cx + dx, cy + dy
            if monster_map.get_has_entity(x, y):
                entity = monster_map.get_entity(x, y)
                if entity == context.caster and not include_caster:
                    continue
                entity.character.take_damage(context.caster, amount)
                hit_count += 1

    context.add_message(f"The blast hits {hit_count} targets!")
    return hit_count > 0


def summon_creature(context, params) -> bool:
    """
    Summon a creature near the caster.

    Params:
        creature_type: Type of creature to summon
        duration: How long the summon lasts (turns)
    """
    creature_type = params.get('creature_type', 'goblin')
    duration = params.get('duration', 10)

    # This would need integration with the monster spawning system
    # Placeholder implementation
    context.add_message(f"You summon a {creature_type}!")
    logger.info(f"Summon creature not fully implemented: {creature_type}")
    return True


def restore_mana(context, params) -> bool:
    """
    Restore mana to the caster.

    Params:
        amount: Amount of mana to restore
    """
    amount = params.get('amount', 10)
    context.caster.character.change_mana(amount)
    context.add_message(f"You restore {amount} mana!")
    return True


def blink_to_target(context, params) -> bool:
    """
    Teleport directly adjacent to a target creature.
    Used for blink_strike and similar abilities.
    """
    if context.target is None:
        return False

    caster = context.caster
    target = context.target
    generator = context.loop.generator

    tx, ty = target.get_location()

    # Find adjacent empty tile to the target
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        nx, ny = tx + dx, ty + dy
        if generator.get_passable((nx, ny)) and generator.monster_map.get_has_no_entity(nx, ny):
            old_x, old_y = caster.get_location()
            # Update monster map if caster is a monster
            if hasattr(caster, 'traits') and caster.traits.get('monster'):
                generator.monster_map.move_entity(old_x, old_y, nx, ny)
            caster.set_location(nx, ny)
            context.add_message(f"{caster.name} blinks to {target.name}!")
            logger.debug(f"{caster.name} blink-striked from ({old_x}, {old_y}) to ({nx}, {ny})")
            return True

    context.add_message("No space to blink to!")
    return False

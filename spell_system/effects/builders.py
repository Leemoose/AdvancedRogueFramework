"""
Effect builders - functional building blocks for composing spell effects.

These functions return EffectData objects that can be combined into spells.
This provides a Pythonic API for defining spell effects without YAML.

Usage:
    from spell_system.effects.builders import damage, apply_status, heal

    effects = [
        damage(5, "fire", scales=True),
        apply_status("burn", duration=3, damage=2),
    ]
"""

from old.spell_data import EffectData


def damage(amount: int, damage_type: str = "magical", scales: bool = False) -> EffectData:
    """
    Create a damage effect.

    Args:
        amount: Base damage amount
        damage_type: Type of damage (fire, ice, physical, magical, psychic, etc.)
        scales: If True, add caster's skill_damage_bonus to damage

    Example:
        damage(5, "fire", scales=True)
    """
    return EffectData(
        type="damage",
        params={
            "amount": amount,
            "damage_type": damage_type,
            "scales_with_intelligence": scales,
        }
    )


def heal(amount: int, target: str = "self", scales: bool = False) -> EffectData:
    """
    Create a healing effect.

    Args:
        amount: Base heal amount
        target: "self" to heal caster, "target" to heal target
        scales: If True, add caster's skill_damage_bonus to heal

    Example:
        heal(10, target="self", scales=True)
    """
    return EffectData(
        type="heal",
        params={
            "amount": amount,
            "target": target,
            "scales_with_intelligence": scales,
        }
    )


def lifesteal(amount: int, scales: bool = False) -> EffectData:
    """
    Create a lifesteal effect (damage target, heal caster for same amount).

    Args:
        amount: Base damage/heal amount
        scales: If True, add caster's skill_damage_bonus

    Example:
        lifesteal(5, scales=True)
    """
    return EffectData(
        type="lifesteal",
        params={
            "amount": amount,
            "scales_with_intelligence": scales,
        }
    )


def apply_status(
    status: str,
    duration: int = 5,
    damage: int = 0,
    amount: int = 0,
    scales: bool = False
) -> EffectData:
    """
    Create an effect that applies a status to the target.

    Args:
        status: Status type (burn, poison, slow, stun, weak, fear, charm, root, bleed, sleep)
        duration: How many turns the status lasts
        damage: Per-turn damage (for DoT effects like burn, poison, bleed)
        amount: Generic amount parameter (e.g., slow percentage, stat reduction)
        scales: If True, scale duration and damage with intelligence

    Examples:
        apply_status("burn", duration=5, damage=3, scales=True)
        apply_status("slow", duration=3, amount=50)
        apply_status("stun", duration=2)
    """
    params = {
        "status": status,
        "duration": duration,
        "scales_with_intelligence": scales,
    }
    if damage > 0:
        params["damage"] = damage
    if amount > 0:
        params["amount"] = amount

    return EffectData(type="apply_status", params=params)


def self_buff(
    status: str,
    duration: int = 5,
    amount: int = 0,
    scales: bool = False
) -> EffectData:
    """
    Create an effect that applies a buff to the caster.

    Args:
        status: Buff type (might, haste, invincible, berserk)
        duration: How many turns the buff lasts
        amount: Buff strength (e.g., stat increase amount)
        scales: If True, scale duration with intelligence

    Examples:
        self_buff("might", duration=10, amount=5)
        self_buff("haste", duration=8, scales=True)
    """
    params = {
        "status": status,
        "duration": duration,
        "scales_with_intelligence": scales,
    }
    if amount > 0:
        params["amount"] = amount

    return EffectData(type="self_buff", params=params)


def message(text: str) -> EffectData:
    """
    Create an effect that displays a message in the game log.

    Args:
        text: Message template (can use {caster} and {target} placeholders)

    Examples:
        message("A ring of fire erupts around {caster}!")
        message("{target} is turned to stone!")
    """
    return EffectData(
        type="message",
        params={"message": text}
    )


def custom(handler: str, **params) -> EffectData:
    """
    Create a custom effect that calls a handler function.

    Args:
        handler: Name of handler function in custom_handlers.py
        **params: Parameters passed to the handler

    Examples:
        custom("aoe_damage", amount=15, radius=2, center="target", scales=True)
        custom("teleport_random", target="self")
        custom("summon_creature", creature_type="skeleton", duration=30)
    """
    return EffectData(
        type="custom",
        params={"handler": handler, **params}
    )


# Convenience aliases for common custom effects

def aoe_damage(
    amount: int,
    radius: int = 2,
    center: str = "target",
    include_caster: bool = False,
    scales: bool = False
) -> EffectData:
    """
    Create an area-of-effect damage effect.

    Args:
        amount: Base damage per target
        radius: Area radius in tiles
        center: "target" or "caster"
        include_caster: Whether to damage caster if in range
        scales: If True, add skill_damage_bonus

    Example:
        aoe_damage(15, radius=2, center="target", scales=True)
    """
    return custom(
        "aoe_damage",
        amount=amount,
        radius=radius,
        center=center,
        include_caster=include_caster,
        scales_with_intelligence=scales,
    )


def teleport(target: str = "self") -> EffectData:
    """
    Create a random teleport effect.

    Args:
        target: "self" to teleport caster, "other" to teleport target

    Example:
        teleport(target="self")
    """
    return custom("teleport_random", target=target)


def blink(distance: int = 5) -> EffectData:
    """
    Create a short-range directional blink effect.

    Args:
        distance: Maximum blink distance

    Example:
        blink(distance=5)
    """
    return custom("blink_direction", distance=distance)


def swap_positions() -> EffectData:
    """Create an effect that swaps caster and target positions."""
    return custom("swap_positions")


def blink_to_target() -> EffectData:
    """Create an effect that teleports caster adjacent to target."""
    return custom("blink_to_target")


def summon(creature_type: str, duration: int = 20) -> EffectData:
    """
    Create a summon creature effect.

    Args:
        creature_type: Type of creature (goblin, skeleton, wolf, golem)
        duration: How long the summon lasts in turns

    Example:
        summon("skeleton", duration=30)
    """
    return custom("summon_creature", creature_type=creature_type, duration=duration)


def restore_mana(amount: int) -> EffectData:
    """
    Create an effect that restores mana to the caster.

    Args:
        amount: Mana to restore

    Example:
        restore_mana(15)
    """
    return custom("restore_mana", amount=amount)


def self_damage(amount: int) -> EffectData:
    """
    Create an effect that damages the caster.

    Args:
        amount: Damage to deal to self

    Example:
        self_damage(10)  # For life tap
    """
    return EffectData(
        type="damage",
        params={
            "amount": amount,
            "target": "self",
        }
    )

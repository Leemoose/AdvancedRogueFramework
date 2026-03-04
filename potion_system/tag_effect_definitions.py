"""
Tag effect definitions - registers all PotionTag -> effect mappings.

Call register_all_tag_effects() once at game startup (alongside InitPotionTags).

Each effect function has signature: (target, loop) -> None
  - loop may be None when called from activate() (drink context).
    Guard all loop.add_message() calls accordingly.

Add new tag effects here. The registry and the definitions are kept
in separate files so the registry class stays clean.
"""

from potion_system.tag_manager import PotionTag
from potion_system.tag_effects import TagEffectRegistry, UsageContext
from spell_system.status_effects import *
import random


def _msg(loop, text, color):
    """Helper to safely send a message when loop may be None."""
    if loop is not None:
        loop.add_message(text, color)

# --- Fire tag effects ---

def fire_drink(target, loop):
    """Drinking fire: apply burn to self (harmful)."""
    effect = Burn(3, 2, None)
    target.character.status.add_status_effect(effect)
    _msg(loop, f"{target.name} feels a burning sensation!", (255, 100, 50))

def fire_throw(target, loop):
    """Throwing fire: burn the target."""
    if hasattr(target, 'character'):
        effect = Burn(5, 3, None)
        target.character.status.add_status_effect(effect)
        _msg(loop, f"{target.name} catches fire!", (255, 100, 50))
 
def fire_apply(target, loop):
    """Applying fire: coat equipment with fire."""
    # TODO: implement fire weapon coating once equipment effects exist
    _msg(loop, "The equipment glows with heat!", (255, 150, 50))

# --- Water tag effects ---

def water_drink(target, loop):
    """Drinking water: small heal."""
    target.character.change_health(5)
    _msg(loop, f"{target.name} feels refreshed.", (100, 150, 255))

def water_throw(target, loop):
    """Throwing water: slow the target."""
    if hasattr(target, 'character'):
        effect = Slow(None, duration=3)
        target.character.status.add_status_effect(effect)
        _msg(loop, f"{target.name} is drenched and slowed!", (100, 150, 255))

def water_apply(target, loop):
    """Applying water: clean equipment."""
    # TODO: implement water equipment effect
    _msg(loop, "The equipment looks cleaner.", (100, 150, 255))

# --- Steam tag effects ---

def steam_drink(target, loop):
    """Drinking steam: might buff (power of combined elements)."""
    effect = Might(5, 3)
    target.character.status.add_status_effect(effect)
    _msg(loop, f"{target.name} feels empowered by steam!", (200, 200, 255))

def steam_throw(target, loop):
    """Throwing steam: burn and slow."""
    if hasattr(target, 'character'):
        burn = Burn(3, 2, None)
        slow = Slow(None, duration=3)
        target.character.status.add_status_effect(burn)
        target.character.status.add_status_effect(slow)
        _msg(loop, f"{target.name} is engulfed in scalding steam!", (200, 200, 255))

def steam_apply(target, loop):
    """Applying steam: equipment effect."""
    # TODO: implement steam equipment effect
    _msg(loop, "Steam hisses off the equipment!", (200, 200, 255))


# --- Steam tag effects ---
def stone_drink(target, loop):
    """Drinking stone: armor buff"""
    effect = Armored(5, 3)
    target.character.status.add_status_effect(effect)
    _msg(loop, f"{target.name} skin grows rocklike!", (200, 200, 255))

def stone_throw(target, loop):
    """Throwing stone: create obstacle if empty, provide armor buff to enemy target otherwise (negative)"""
    if hasattr(target, 'character'):
        effect = Armored(5, 3)
        target.character.status.add_status_effect(effect)
        _msg(loop, f"{target.name} skin grows rocklike!", (200, 200, 255))

def stone_apply(target, loop):
    """Applying stone: equipment effect."""
    # TODO: implement stone equipment effect
    _msg(loop, "Stone grows on the equipment!", (200, 200, 255))

# --- magma tag effects ---
def magma_drink(target, loop):
    """Drinking magma: purified in magma (end a negative status effect)"""
    if target.character.status.has_negative_effects:
        negative_effects = target.character.status.get_all_negative_effects()
        effect = random.choice(negative_effects)
        target.character.status.remove_status_effect(effect)
        _msg(loop, f"{target.name} is purified by the heat of magma", (200, 200, 255))
    else:
        _msg(loop, f"{target.name} feels warmth inside", (200, 200, 255))

def magma_throw(target, loop):
    """Throwing magma: root and burn"""
    if hasattr(target, 'character'):
        burn = Burn(3, 3, None)
        root = Root(None, duration=3)
        target.character.status.add_status_effect(burn)
        target.character.status.add_status_effect(root)
        _msg(loop, f"{target.name} is immobilized by magma!", (200, 200, 255))

def magma_apply(target, loop):
    """Applying magma: equipment effect."""
    # TODO: implement stone equipment effect
    _msg(loop, "Magma engulfs the equipment!", (200, 200, 255))

def register_all_tag_effects():
    """Register all tag -> effect mappings. Call once at startup."""
    r = TagEffectRegistry

    # Fire
    r.register(PotionTag.Fire, UsageContext.DRINK, fire_drink)
    r.register(PotionTag.Fire, UsageContext.THROW, fire_throw)
    r.register(PotionTag.Fire, UsageContext.APPLY, fire_apply)

    # Water
    r.register(PotionTag.Water, UsageContext.DRINK, water_drink)
    r.register(PotionTag.Water, UsageContext.THROW, water_throw)
    r.register(PotionTag.Water, UsageContext.APPLY, water_apply)

    # Steam
    r.register(PotionTag.Steam, UsageContext.DRINK, steam_drink)
    r.register(PotionTag.Steam, UsageContext.THROW, steam_throw)
    r.register(PotionTag.Steam, UsageContext.APPLY, steam_apply)

    # Stone
    r.register(PotionTag.Stone, UsageContext.DRINK, stone_drink)
    r.register(PotionTag.Stone, UsageContext.THROW, stone_throw)
    r.register(PotionTag.Stone, UsageContext.APPLY, stone_apply)
    
    # Magma
    r.register(PotionTag.Magma, UsageContext.DRINK, magma_drink)
    r.register(PotionTag.Magma, UsageContext.THROW, magma_throw)
    r.register(PotionTag.Magma, UsageContext.APPLY, magma_apply)
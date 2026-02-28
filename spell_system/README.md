# Spell System v3

A Python-based spell system using composable effect building blocks.

## Overview

Spells are defined as Python objects using simple, composable building blocks:

```python
from spell_system import spell, Schools, damage, apply_status

burning_attack = spell(
    "burning_attack", "Burning Attack",
    school=Schools.FIRE, level=1, cost=5, cooldown=10, range=5,
    effects=[
        damage(3, "fire", scales=True),
        apply_status("burn", duration=5, damage=3, scales=True),
    ],
    description="Throw a bolt of fire that burns the target."
)
```

**Key benefits:**
- Pure Python - IDE support, type hints, debugging
- Composable effects - spells are built from small, reusable pieces
- Less code - 5-10 lines per spell
- Consistent with rest of codebase

## Directory Structure

```
spell_system/
├── __init__.py           # Main exports
├── spell.py              # Spell class (runtime instance)
├── spell_data.py         # SpellData class (immutable definition)
├── spell_builder.py      # spell() function and Schools enum
├── spell_registry.py     # Central registry for all spells
├── game_integration.py   # Convenience functions (give_spell, etc.)
├── effects/
│   ├── __init__.py
│   ├── base_effect.py    # BaseEffect abstract class
│   ├── effect_factory.py # Effect creation + built-in effects
│   ├── builders.py       # Effect building blocks (damage, heal, etc.)
│   └── custom_handlers.py# Custom handlers for complex effects
├── status_effects/
│   └── ...               # Status effect implementations
└── spells/               # Spell definitions by school
    ├── __init__.py
    ├── fire.py           # Fire school (burning_attack, fireball, etc.)
    ├── mind.py           # Mind school (lethargy, weaken, etc.)
    ├── necromancy.py     # Necromancy (sap_vitality, poison_touch, etc.)
    ├── space.py          # Space school (blink, teleport, etc.)
    └── summon.py         # Summon school (summon_goblin, etc.)
```

## Usage

### Initialization (at game start)

```python
from spell_system import initialize_spell_system

# Load all spell definitions
initialize_spell_system()
```

### Giving Spells to Entities

```python
from spell_system import give_spell, give_school_spells

# Give a specific spell
give_spell(player, 'burning_attack')

# Give all spells from a school up to level 2
give_school_spells(player, 'fire', max_level=2)

# Give with overrides (for monsters, items, etc.)
give_spell(lich, 'sap_vitality', cooldown=5, cost=3)
```

## Adding New Spells

### 1. Find the right school file

Spells are organized by school in `spell_system/spells/`:
- `fire.py` - damage and DoT
- `mind.py` - control and debuffs
- `necromancy.py` - lifesteal and dark magic
- `space.py` - teleportation
- `summon.py` - summoning creatures

### 2. Define your spell

```python
from ..spell_builder import spell, Schools
from ..effects.builders import damage, apply_status, heal

my_spell = spell(
    "spell_id", "Display Name",
    school=Schools.FIRE,  # or MIND, NECROMANCY, SPACE, SUMMON
    level=1,              # 1-4, determines unlock order
    cost=5,               # mana cost
    cooldown=10,          # turns before recast
    range=5,              # -1=unlimited, 0=self, positive=distance
    action_cost=50,       # energy cost (25-100)
    targeting="enemy",    # "self", "enemy", "ally", "ground"
    icon=9100,            # render tag for UI
    required_intelligence=0,
    tags=["fire", "damage"],
    effects=[
        damage(5, "fire", scales=True),
        apply_status("burn", duration=3, damage=2),
    ],
    description="Spell description text."
)
```

### 3. Add to `__all__`

```python
__all__ = ['existing_spell', 'my_spell']
```

## Effect Building Blocks

### Basic Effects

| Builder | Description | Example |
|---------|-------------|---------|
| `damage(amount, type, scales)` | Deal damage | `damage(5, "fire", scales=True)` |
| `heal(amount, target, scales)` | Heal self or target | `heal(10, target="self")` |
| `lifesteal(amount, scales)` | Damage + heal | `lifesteal(5, scales=True)` |
| `apply_status(status, ...)` | Apply debuff to target | `apply_status("burn", duration=5, damage=3)` |
| `self_buff(status, ...)` | Apply buff to caster | `self_buff("might", duration=10, amount=5)` |
| `message(text)` | Display message | `message("{target} is frozen!")` |

### Custom Effects

| Builder | Description | Example |
|---------|-------------|---------|
| `aoe_damage(amount, radius, center)` | Area damage | `aoe_damage(15, radius=2, center="target")` |
| `blink(distance)` | Short teleport | `blink(distance=5)` |
| `teleport(target)` | Random teleport | `teleport(target="self")` |
| `swap_positions()` | Swap with target | `swap_positions()` |
| `blink_to_target()` | Teleport to target | `blink_to_target()` |
| `summon(creature, duration)` | Summon creature | `summon("skeleton", duration=30)` |
| `restore_mana(amount)` | Restore mana | `restore_mana(15)` |
| `self_damage(amount)` | Damage self | `self_damage(10)` |

### Status Types

For `apply_status()` and `self_buff()`:

| Status | Effect | Key Params |
|--------|--------|------------|
| `burn` | Fire DoT | `damage` |
| `poison` | Poison DoT (stacks) | `damage` |
| `bleed` | Physical DoT | `damage` |
| `slow` | Reduced action speed | `amount` (%) |
| `stun` | Cannot act | - |
| `weak` | Reduced damage | `amount` |
| `fear` | Flee from caster | - |
| `charm` | Fight for caster | - |
| `root` | Cannot move | - |
| `sleep` | Cannot act, breaks on damage | - |
| `might` | Increased strength | `amount` |
| `haste` | Increased speed | - |
| `berserk` | Increased stats, can't cast | - |
| `invincible` | Take no damage | - |

## Adding Custom Effect Handlers

For effects too complex for building blocks, add a handler in `effects/custom_handlers.py`:

```python
def my_custom_effect(context, params) -> bool:
    """Description of what this does."""
    amount = params.get('amount', 10)

    # Access game state
    caster = context.caster
    target = context.target
    loop = context.loop

    # Do something
    target.character.take_damage(caster, amount)
    context.add_message(f"{caster.name} does something to {target.name}!")

    return True  # Success
```

Then use it in a spell:

```python
from ..effects.builders import custom

effects=[
    custom("my_custom_effect", amount=15, other_param="value"),
]
```

## API Reference

### spell_system module

```python
# Core
from spell_system import Spell, SpellData, EffectData

# Building
from spell_system import spell, Schools
from spell_system import damage, heal, lifesteal, apply_status, self_buff
from spell_system import aoe_damage, blink, teleport, summon

# Registry
from spell_system import get_registry, initialize_spell_system

# Game integration
from spell_system import give_spell, give_school_spells, give_starter_spells
```

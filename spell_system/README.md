# Spell System v2

A data-driven spell system that replaces the old class-based spell implementation.

## Overview

The new system separates spell definitions (data) from spell behavior (code):

- **Spell Data** (YAML files): Define what spells exist, their costs, effects, etc.
- **Effect System** (Python): Implements reusable effect types (damage, heal, apply_status, etc.)
- **Custom Handlers** (Python): Escape hatch for complex effects that can't be expressed in data

## Directory Structure

```
spell_system/
├── __init__.py           # Main exports
├── spell.py              # Spell class (runtime instance)
├── spell_data.py         # SpellData class (immutable definition)
├── spell_registry.py     # Central registry for all spells
├── game_integration.py   # Convenience functions for game integration
├── effects/
│   ├── __init__.py
│   ├── base_effect.py    # BaseEffect abstract class
│   ├── effect_factory.py # Effect creation + built-in effects
│   └── custom_handlers.py# Custom Python handlers for complex effects
├── status_effects/
│   ├── __init__.py
│   └── status_factory.py # Creates status effects by type
└── data/
    ├── fire.yaml         # Fire school spells
    ├── necromancy.yaml   # Necromancy school spells
    ├── space.yaml        # Space/teleport school spells
    ├── mind.yaml         # Mind/control school spells
    └── summon.yaml       # Summoning school spells
```

## Usage

### Initialization (at game start)

```python
from spell_system import initialize_spell_system

# Load all spell definitions from YAML files
initialize_spell_system()
```

### Giving Spells to Entities

```python
from spell_system import give_spell, give_school_spells

# Give a specific spell
give_spell(player, 'burning_attack')

# Give all spells from a school up to level 2
give_school_spells(player, 'fire', max_level=2)
```

### Creating Spells Directly

```python
from spell_system import get_registry

registry = get_registry()
spell = registry.create_spell('fireball', caster)
caster.mage.add_spell(spell)
```

## Adding New Spells

### Simple Spells (Data Only)

Add to the appropriate YAML file in `spell_system/data/`:

```yaml
spells:
  ice_bolt:
    name: "Ice Bolt"
    school: ice
    level: 1
    description: |
      Hurl a bolt of ice at an enemy.
      Deals cold damage and may slow the target.
    cost: 4
    cooldown: 6
    range: 6
    action_cost: 50
    targeting: enemy
    icon: 9200
    tags: [ice, damage, control]
    effects:
      - type: damage
        amount: 8
        damage_type: cold
        scales_with_intelligence: true
      - type: apply_status
        status: slow
        duration: 3
```

### Complex Spells (Custom Handler)

1. Add the handler in `effects/custom_handlers.py`:

```python
def freeze_time(context, params) -> bool:
    """Stop all enemies for one turn."""
    duration = params.get('duration', 1)
    # ... implementation ...
    return True
```

2. Reference it in YAML:

```yaml
time_stop:
  name: "Time Stop"
  effects:
    - type: custom
      handler: freeze_time
      duration: 2
```

## Available Effect Types

| Type | Description | Key Params |
|------|-------------|------------|
| `damage` | Deal damage to target | `amount`, `damage_type`, `scales_with_intelligence` |
| `heal` | Heal caster or target | `amount`, `target` ("self"/"target") |
| `lifesteal` | Damage + heal for same amount | `amount` |
| `apply_status` | Apply status effect to target | `status`, `duration`, `damage` |
| `self_buff` | Apply status effect to caster | `status`, `duration`, `amount` |
| `message` | Display message | `message` (can use {caster}, {target}) |
| `custom` | Run custom Python handler | `handler`, + handler-specific params |

## Migration from Old System

The old system in `spell_implementation/` is still present for backward compatibility.
Status effects are shared between systems (imported from `spell_implementation/effects/`).

To fully migrate:
1. Remove old spell class files (fire_school/, necromancy_school/, etc.)
2. Update any monster spell usage to use the new system
3. Update any scroll/item spell granting to use `give_spell()`

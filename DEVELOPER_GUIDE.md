# RogueGame Developer Guide

A comprehensive guide for developers contributing to this Python roguelike built with Pygame.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Systems](#core-systems)
3. [Adding New Monsters](#adding-new-monsters)
4. [Adding New Items](#adding-new-items)
5. [Adding New Spells](#adding-new-spells)
6. [Dungeon Generation](#dungeon-generation)
7. [Game States & UI](#game-states--ui)
8. [Monster AI (Behavior System)](#monster-ai-behavior-system)
9. [File Structure Reference](#file-structure-reference)
10. [Common Patterns](#common-patterns)

---

## Architecture Overview

The game follows a composition-based architecture where entities (Player, Monsters, Items) share components for their functionality.

```
Objects (base class)
    ├── Player
    │   ├── Character (stats, status effects, energy)
    │   ├── Inventory
    │   ├── Body (equipment slots)
    │   ├── Fighter (combat)
    │   └── Mage (spells)
    │
    ├── Monster
    │   ├── Character
    │   ├── Inventory
    │   ├── Body
    │   ├── Fighter
    │   ├── Mage
    │   └── MonsterAI (behaviors)
    │
    └── Item
        ├── Equipment (weapons, armor)
        └── Consumable (potions, scrolls)
```

### Main Entry Points

- **`loops.py`** - Main game controller (`Loops` class)
- **`player.py`** - Player entity
- **`objects.py`** - Base `Objects` class for all game entities

---

## Core Systems

### The Loops Class (`loops.py`)

Central game coordinator handling:

- **State transitions** - Managing different screens (action, inventory, targeting, etc.)
- **Event processing** - Keyboard, mouse, window events via Pygame
- **Game time** - Energy-based turn system and monster AI updates
- **Floor transitions** - Moving between dungeon levels

```python
# Main game loop (called every frame)
loop.action_loop(keyboard, display)

# Change game state
loop.change_loop(LoopType.inventory)

# Initialize a new game
loop.init_game()
```

### The Energy System

Actions cost energy. When a character's energy goes negative, time passes:

```python
# In character.py
self.action_costs = {
    "attack": 100,
    "move": 100,
    "grab": 30,
    "equip": 100,
    # ...
}
```

When `player.character.energy < 0`, the game calls:
1. `time_passes()` - Tick status effects, cooldowns, regeneration
2. `monster_loop()` - Give monsters energy and let them act

### The Trait System

Entities use a trait dictionary for type checking:

```python
self.traits["monster"] = True
self.traits["goblins"] = True

# Check traits
if entity.has_trait("monster"):
    # ...
```

---

## Adding New Monsters

### Step 1: Create the Monster Class

Create a new file in `monsters/<category>/` (e.g., `monsters/demons/demon.py`):

```python
from monsters.monster import Monster
from monster_implementation import MonsterAI, create_base_behaviors

class Demon(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1100, name="Demon",
                 experience_given=25, health=30, min_damage=5, max_damage=10,
                 rarity="Rare"):
        super().__init__(
            x=x, y=y, render_tag=render_tag, name=name,
            experience_given=experience_given, health=health,
            min_damage=min_damage, max_damage=max_damage,
            rarity=rarity, gold=10
        )
        # Use default behaviors or create custom ones
        self.brain = MonsterAI(self, create_base_behaviors())

        # Customize action costs (optional)
        self.character.action_costs["move"] = 80

        # Set description
        self.description = "A fearsome demon from the underworld."

        # Set base stats
        self.strength = 3
        self.dexterity = 2
        self.endurance = 2
        self.intelligence = 1

        # Add custom traits
        self.traits["demon"] = True
```

### Step 2: Register the Monster for Spawning

Edit `dungeon_generation/spawning/monster_initializations.py`:

```python
from monsters.demons.demon import Demon

# Add to the monster spawns list
MonsterSpawns.append(
    MonsterSpawnParams(
        Demon(),              # Instance of the monster
        minFloor=3,           # First floor it can appear
        maxFloor=10,          # Last floor it can appear
        branches=["Dungeon"], # Which branches
        rarity="Rare",        # Common or Rare
        group="demons",       # For pack spawning
        boss=False            # Is it a boss?
    )
)
```

### Step 3: Add Sprite

1. Add sprite image to `assets/` or `assets/crawl-tiles/`
2. Register in `static_configs.py`:

```python
tiles[1100] = image.load('assets/monsters/demon.png')
```

### Custom Monster Behaviors

Override `do_attack` for special attack effects:

```python
def do_attack(self, target, loop):
    self.character.change_energy(-self.character.get_action_cost("attack"))
    damage = self.fighter.do_attack(target, loop)
    if damage > 0:
        # Special effect: steal gold
        gold_taken = target.inventory.get_gold() // 2
        self.inventory.change_gold_amount(gold_taken)
        target.inventory.change_gold_amount(-gold_taken)
    return damage
```

---

## Adding New Items

### Equipment (Weapons, Armor)

Create in the appropriate subdirectory of `item_implementation/`:

```python
# item_implementation/weapons/swords/flaming_sword.py
from item_implementation.weapons.weapons import Weapon
from spell_implementation.effects.burn import Burn

class FlamingSword(Weapon):
    def __init__(self, render_tag=331):
        super().__init__(
            render_tag=render_tag,
            name="Flaming Sword",
            min_damage=5,
            max_damage=12
        )
        self.description = "A sword wreathed in eternal flames."
        self.rarity = "Rare"
        self.on_hit_effects = [self.apply_burn]

    def apply_burn(self, target, attacker, loop):
        effect = Burn(duration=3, damage=2, source=attacker)
        target.character.status.add_status_effect(effect)
```

### Consumables (Potions, Scrolls)

```python
# item_implementation/consumables/potions/fire_potion.py
from item_implementation.items import Consumeable

class FirePotion(Consumeable):
    def __init__(self, render_tag=406):
        super().__init__(render_tag, "Fire Resistance Potion")
        self.description = "Grants temporary fire resistance."
        self.equipment_type = "Potiorb"  # For potions
        self.traits["potion"] = True

    def activate_once(self, entity):
        # Add fire resistance status effect
        from spell_implementation.effects.fire_resist import FireResist
        entity.character.status.add_status_effect(FireResist(duration=20))
```

### Registering Items for Spawning

Edit `dungeon_generation/spawning/item_initializations.py`:

```python
from item_implementation.weapons.swords.flaming_sword import FlamingSword

SPAWN_CONFIG = [
    # ... existing items ...
    (FlamingSword, None, 3, 10),  # (Class, constructor_args, min_floor, max_floor)
]
```

---

## Adding New Spells

### Step 1: Create the Spell Class

Spells go in `spell_implementation/` organized by school:

```python
# spell_implementation/ice_school/frost_bolt.py
from spell_implementation import Spell
from spell_implementation.effects.slow import Slow

class FrostBolt(Spell):
    def __init__(self, parent, name="Frost Bolt", cooldown=8, cost=5,
                 range=6, action_cost=100, damage=4, slow_duration=3):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.damage = damage
        self.slow_duration = slow_duration
        self.targetted = True        # Requires target selection
        self.targets_monster = True  # Targets monsters
        self.render_tag = 920        # Icon asset ID

    def activate(self, defender, loop):
        # Deduct mana
        self.parent.character.change_mana(-self.cost)

        # Deal damage (scales with intelligence)
        total_damage = self.damage + self.parent.character.skill_damage_increase()
        defender.character.take_damage(self.parent, total_damage)

        # Apply slow effect
        effect = Slow(self.slow_duration + self.parent.character.skill_duration_increase())
        defender.character.status.add_status_effect(effect)

        loop.add_message(f"Frost bolt hits {defender.name}!")
        return True

    def castable(self, target):
        return super().castable(target) and self.in_range(target)

    def description(self):
        return f"{self.name}({self.cost} cost, {self.cooldown} CD, {self.damage} damage, slows)"
```

### Step 2: Add to a Spell School (Optional)

```python
# spell_implementation/ice_school/ice_school.py
from .frost_bolt import FrostBolt

ICE_SPELLS = [FrostBolt]
```

### Step 3: Add to Learnable Spells

Spells can be learned from books or granted by items. See `item_implementation/consumables/books/book.py`.

---

## Dungeon Generation

### Map Generators

Located in `dungeon_generation/generators/`:

| Generator | Description |
|-----------|-------------|
| `rooms_corridors.py` | Traditional rooms connected by L-shaped corridors |
| `cave.py` | Cellular automata organic caves |
| `pillar_hall.py` | Open space with pillar columns |

### Spawn Strategies

Located in `dungeon_generation/spawn_strategies/`:

| Strategy | Description |
|----------|-------------|
| `random_spawn.py` | Random monster placement |
| `elite_group.py` | Elite monster with minion pack |
| `guarding_items.py` | Monsters positioned near valuable items |

### Configuration

Dungeon layouts are configured in `dungeon_generation/configuration_data/`:

```python
# dungeon_data.py - Define branches and depths
# map_data.py - Define per-floor map parameters

class MapData:
    def __init__(self, width=50, height=50, generator_type='rooms_corridors',
                 spawn_strategy='random', spawn_params=None):
        # ...
```

### Adding a New Branch

1. Add branch configuration in `configuration_data/dungeon_data.py`
2. Add spawn parameters in `spawning/branch_params.py`
3. Add monster distributions in the branch params

---

## Game States & UI

### State Pattern

The game uses a State pattern (`loop_workflow/game_states.py`):

```python
class GameState(ABC):
    """Base class for all game states."""

    @abstractmethod
    def create_display(self, display): ...

    @abstractmethod
    def update_display(self, display): ...

    @abstractmethod
    def handle_input(self, key): ...

    def tick(self): ...  # For continuous updates (resting, pathing)
```

### Available States (`loop_workflow/looptype.py`)

| LoopType | Description |
|----------|-------------|
| `action` | Main gameplay - moving, attacking |
| `inventory` | Inventory management |
| `equipment` | Equipment/gear screen |
| `targeting` | Selecting spell targets |
| `spellbook` | Viewing known spells |
| `resting` | Auto-rest until healed |
| `pathing` | Auto-explore/auto-path |
| `levelup` | Allocating stat points |
| `death` | Game over screen |
| `victory` | Win screen |

### Adding a New Screen

1. Create screen in `display_generation/`:

```python
# display_generation/my_screen.py
def my_screen(display, loop):
    # Render your screen using display methods
    display.draw_text("Hello World", x=100, y=100)
```

2. Create state in `loop_workflow/states/`:

```python
# loop_workflow/states/my_state.py
from loop_workflow.game_states import GameState
from loop_workflow.looptype import LoopType

class MyState(GameState):
    loop_type = LoopType.my_state

    def create_display(self, display):
        pass

    def update_display(self, display):
        from display_generation.my_screen import my_screen
        my_screen(display, self.loop)

    def handle_input(self, key):
        if key == "escape":
            self._change_state(LoopType.action)
        return True
```

3. Register state in `loop_workflow/states/__init__.py`:

```python
def create_all_states(loop):
    return [
        # ... existing states ...
        MyState(loop),
    ]
```

4. Add LoopType enum in `loop_workflow/looptype.py`:

```python
class LoopType(Enum):
    # ... existing ...
    my_state = "my_state"
```

---

## Monster AI (Behavior System)

### Overview

Monsters use a behavior-based AI system (`monster_implementation/behaviors.py`). Each behavior:

1. **Ranks itself** (0-100 utility score, -1 if invalid)
2. **Executes** if selected as highest-ranked

### Creating Custom Behaviors

```python
from monster_implementation.behaviors import Behavior

class TeleportBehavior(Behavior):
    """Teleport away when health is low."""

    def __init__(self, tendency=(90, 10), threshold=0.3):
        super().__init__("teleport", tendency)
        self.threshold = threshold
        self.used = False

    def rank(self, ai, loop):
        if self.used:
            return -1
        char = ai.parent.character
        if char.get_health() / char.get_max_health() < self.threshold:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        x, y = loop.generator.get_random_passable_location()
        monster.set_location(x, y)
        loop.add_message(f"{monster.name} teleports away!")
        self.used = True
```

### Behavior Factory Functions

```python
# Add to monster_implementation/behaviors.py

def create_teleporter_behaviors():
    """Behaviors for a teleporting monster."""
    return [
        CombatBehavior(),
        MoveBehavior(),
        TeleportBehavior(),
        WaitBehavior(),
    ]
```

### Pre-built Behaviors

| Behavior | Description |
|----------|-------------|
| `CombatBehavior` | Attack player if in range |
| `MoveBehavior` | Path toward player |
| `WaitBehavior` | Do nothing (fallback) |
| `FleeBehavior` | Run away when low health |
| `FindItemBehavior` | Path to items on ground |
| `PickupBehavior` | Pick up items |
| `BerserkBehavior` | Activate berserk at low health |
| `SpinWebBehavior` | Create web terrain |
| `RangedCombatBehavior` | Attack from range only |
| `RepositionBehavior` | Maintain optimal distance |

---

## File Structure Reference

```
RogueGame-main/
├── loops.py                    # Main game controller
├── player.py                   # Player entity
├── objects.py                  # Base Objects class
├── static_configs.py           # Asset loading (TileDict)
├── logging_config.py           # Logging setup
│
├── character_implementation/   # Character components
│   ├── character.py           # Stats, energy, actions
│   ├── attributes.py          # STR, DEX, INT, END
│   ├── status.py              # Status effects
│   ├── inventory.py           # Item management
│   ├── body_slot.py           # Equipment slots
│   ├── fighter.py             # Combat calculations
│   └── mage.py                # Spell casting
│
├── monsters/                   # Monster definitions
│   ├── monster.py             # Base Monster class
│   ├── goblins/
│   ├── orcs/
│   ├── kobolds/
│   ├── spiders/
│   ├── oozes/
│   └── undead/
│
├── monster_implementation/     # Monster AI
│   └── behaviors.py           # Behavior-based AI system
│
├── item_implementation/        # Items
│   ├── items.py               # Base Item, Gold, Consumeable
│   ├── equipment.py           # Base Equipment class
│   ├── weapons/               # Weapon types
│   ├── armor/                 # Armor types
│   ├── talismans/             # Rings, amulets, orbs
│   └── consumables/           # Potions, scrolls, books
│
├── spell_implementation/       # Spells
│   ├── spell.py               # Base Spell class
│   ├── effects/               # Status effects (burn, slow, etc.)
│   ├── fire_school/
│   ├── necromancy_school/
│   └── mind_school/
│
├── dungeon_generation/         # Map generation
│   ├── mapping.py             # DungeonGenerator
│   ├── tiles.py               # Tile definitions
│   ├── maps/                  # TileMap, TrackingMap, Room
│   ├── generators/            # Map layout generators
│   ├── spawn_strategies/      # Monster placement strategies
│   ├── spawning/              # Monster/item spawn configs
│   ├── terrain/               # Terrain effects (web, etc.)
│   └── configuration_data/    # Branch/floor configs
│
├── display_generation/         # UI/Rendering
│   ├── display.py             # Main Display class
│   ├── main_screen.py         # Game world view
│   ├── inventory_screen.py
│   ├── spell_screen.py
│   └── ...                    # Other screens
│
├── loop_workflow/              # Game state management
│   ├── game_states.py         # State pattern implementation
│   ├── looptype.py            # LoopType enum
│   ├── states/                # State implementations
│   ├── keyboard.py            # Input handling
│   ├── bindings.py            # Key bindings
│   └── messages.py            # Message log
│
├── navigation_utility/         # Pathfinding & FOV
│   ├── pathfinding.py         # A* pathfinding
│   └── shadowcasting.py       # Field of view
│
└── assets/                     # Sprites and images
    ├── tiles/
    ├── player/
    ├── items/
    ├── skills/
    └── crawl-tiles/           # Dungeon Crawl tiles
```

---

## Common Patterns

### Getting Player Reference

```python
player = loop.player
```

### Getting Current Floor Data

```python
generator = loop.generator
tile_map = generator.tile_map
monster_map = generator.monster_map
item_map = generator.item_map
```

### Adding Messages to Log

```python
loop.add_message("Something happened!")
loop.add_message("Damage dealt!", (220, 20, 60))  # With color
```

### Checking Passability

```python
if loop.generator.get_passable((x, y)):
    # Tile is walkable and unoccupied
```

### Getting Distance

```python
distance = entity.get_distance(target_x, target_y)
```

### Spawning Entities

```python
# Monsters
loop.generator.monster_map.place_thing(monster)

# Items
loop.generator.item_map.place_thing(item)

# Interactables
loop.generator.interact_map.place_thing(interactable)
```

### Working with Status Effects

```python
# Add effect
entity.character.status.add_status_effect(effect)

# Check for effect
effects = entity.character.get_status_effects()

# Remove effect
entity.character.status.remove_status_effect(effect)
```

---

## Debugging Tips

1. **Enable logging**: Check `logging_config.py` for log levels
2. **Invincibility mode**: Player starts invincible if `character.status.invincible = True` in `player.py`
3. **Force spawn monsters**: Set `forceSpawn` in `monster_spawner.py`
4. **Debug spells**: Add test spells in `Player.__init__()` when invincible

---

## Updating This Guide

**Important**: When you make changes to the codebase, please update this documentation:

- New systems → Add new section
- New patterns → Add to Common Patterns
- Changed APIs → Update examples
- New file types → Update File Structure Reference

This keeps the guide accurate for future developers.
